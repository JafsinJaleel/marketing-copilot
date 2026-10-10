from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.llm.ollama_service import generate_text
from app.llm.campaign_generator import (
    generate_campaign as generate_campaign_llm,
)
from app.agents.intent_classifier import classify_intent
from app.agents.tool_selector import select_tools
from app.mcp.client import call_mcp_tool


class AgenticCampaignState(TypedDict):
    message: str

    # Intent
    intent: str

    # LLM tool selection
    use_product_tool: bool
    use_customer_tool: bool
    use_marketing_tool: bool

    # Extracted customer segment
    customer_segment: str

    # Execution tracking
    product_executed: bool
    customer_executed: bool
    marketing_executed: bool

    # Retrieved contexts
    product_context: str
    customer_context: str
    marketing_context: str
    combined_context: str

    # Output
    response: str
    campaign: str

    # Validation
    validation_status: str
    validation_message: str
    retry_count: int


# ============================================================
# 1. CLASSIFY INTENT
# ============================================================

def classify_request(state: AgenticCampaignState):
    result = classify_intent(state["message"])

    return {
        **state,
        "intent": result["intent"],
    }


# ============================================================
# 2. SELECT TOOLS + EXTRACT CUSTOMER SEGMENT
# ============================================================

def select_required_tools(state: AgenticCampaignState):

    selection = select_tools(state["message"])

    return {
        **state,

        "use_product_tool": selection["use_product_tool"],
        "use_customer_tool": selection["use_customer_tool"],
        "use_marketing_tool": selection["use_marketing_tool"],

        "customer_segment": selection.get(
            "customer_segment",
            "",
        ),

        "product_executed": False,
        "customer_executed": False,
        "marketing_executed": False,

        "product_context": "",
        "customer_context": "",
        "marketing_context": "",
        "combined_context": "",

        "response": "",
        "campaign": "",

        "validation_status": "",
        "validation_message": "",
        "retry_count": 0,
    }


# ============================================================
# 3. ROUTE TO FIRST MCP TOOL
# ============================================================

def route_first_tool(state: AgenticCampaignState):

    if (
        state["use_product_tool"]
        and not state["product_executed"]
    ):
        return "product_tool"

    if (
        state["use_customer_tool"]
        and not state["customer_executed"]
    ):
        return "customer_tool"

    if (
        state["use_marketing_tool"]
        and not state["marketing_executed"]
    ):
        return "marketing_tool"

    return "combine_context"


# ============================================================
# 4. PRODUCT MCP TOOL
# ============================================================

def execute_product_tool(state: AgenticCampaignState):

    result = call_mcp_tool(
        "product_search",
        {
            "query": state["message"],
        },
    )

    return {
        **state,
        "product_context": result,
        "product_executed": True,
    }


# ============================================================
# 5. CUSTOMER MCP TOOL
# ============================================================

def execute_customer_tool(state: AgenticCampaignState):

    segment = state["customer_segment"]

    # Safety fallback if no segment was extracted
    if not segment:
        segment = "Young Professionals"

    result = call_mcp_tool(
        "customer_search",
        {
            "segment": segment,
        },
    )

    return {
        **state,
        "customer_context": result,
        "customer_executed": True,
    }


# ============================================================
# 6. MARKETING MCP TOOL
# ============================================================

def execute_marketing_tool(state: AgenticCampaignState):

    result = call_mcp_tool(
        "marketing_guidelines_search",
        {
            "query": "marketing campaign rules and guidelines",
        },
    )

    return {
        **state,
        "marketing_context": result,
        "marketing_executed": True,
    }


# ============================================================
# 7. ROUTE TO NEXT MCP TOOL
# ============================================================

def route_next_tool(state: AgenticCampaignState):

    if (
        state["use_product_tool"]
        and not state["product_executed"]
    ):
        return "product_tool"

    if (
        state["use_customer_tool"]
        and not state["customer_executed"]
    ):
        return "customer_tool"

    if (
        state["use_marketing_tool"]
        and not state["marketing_executed"]
    ):
        return "marketing_tool"

    return "combine_context"


# ============================================================
# 8. COMBINE CONTEXT
# ============================================================

def combine_context(state: AgenticCampaignState):

    context_parts = []

    if state["product_context"]:
        context_parts.append(
            "===== PRODUCT INFORMATION =====\n"
            + state["product_context"]
        )

    if state["customer_context"]:
        context_parts.append(
            "===== CUSTOMER INFORMATION =====\n"
            + state["customer_context"]
        )

    if state["marketing_context"]:
        context_parts.append(
            "===== MARKETING GUIDELINES =====\n"
            + state["marketing_context"]
        )

    combined_context = "\n\n".join(context_parts)

    return {
        **state,
        "combined_context": combined_context,
    }


# ============================================================
# 9. INFORMATION RESPONSE
# ============================================================

def answer_information(state: AgenticCampaignState):

    system_prompt = """
You are an AI Marketing Copilot information assistant.

Answer the user's question using ONLY the retrieved context.

Rules:
1. Do not invent information.
2. Do not add unsupported product specifications.
3. Do not make unsupported claims.
4. If the context does not contain the answer, say that
   the information is not available.
5. Give a clear and concise answer.
"""

    user_prompt = f"""
User Question:
{state["message"]}

Retrieved Context:
{state["combined_context"]}
"""

    response = generate_text(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    return {
        **state,
        "response": response,
    }


# ============================================================
# 10. GENERATE CAMPAIGN
# ============================================================

def generate_campaign_node(state: AgenticCampaignState):

    campaign = generate_campaign_llm(
        user_request=state["message"],
        context=state["combined_context"],
    )

    return {
        **state,
        "campaign": campaign,
        "response": campaign,
    }


# ============================================================
# 11. VALIDATE CAMPAIGN
# ============================================================

def validate_campaign(state: AgenticCampaignState):

    campaign = state["campaign"]

    required_sections = [
        "Campaign Title:",
        "Target Audience:",
        "Headline:",
        "Body:",
        "Call To Action:",
    ]

    missing_sections = [
        section
        for section in required_sections
        if section not in campaign
    ]

    if missing_sections:

        return {
            **state,
            "validation_status": "failed",
            "validation_message": (
                "Missing sections: "
                + ", ".join(missing_sections)
            ),
        }

    return {
        **state,
        "validation_status": "passed",
        "validation_message": (
            "Campaign contains all required sections."
        ),
    }


# ============================================================
# 12. VALIDATION ROUTER
# ============================================================

def route_validation(state: AgenticCampaignState):

    if state["validation_status"] == "passed":
        return "finish"

    if state["retry_count"] < 1:
        return "retry"

    return "failed"


# ============================================================
# 13. RETRY CAMPAIGN
# ============================================================

def retry_campaign(state: AgenticCampaignState):

    retry_count = state["retry_count"] + 1

    retry_context = f"""
{state["combined_context"]}

IMPORTANT VALIDATION FEEDBACK:
{state["validation_message"]}

Generate the campaign again and make sure all required
sections are included.
"""

    campaign = generate_campaign_llm(
        user_request=state["message"],
        context=retry_context,
    )

    return {
        **state,
        "campaign": campaign,
        "response": campaign,
        "retry_count": retry_count,
    }


# ============================================================
# 14. FINISH
# ============================================================

def finish(state: AgenticCampaignState):

    return {
        **state,
        "response": state["campaign"],
    }


# ============================================================
# 15. FAILED
# ============================================================

def failed(state: AgenticCampaignState):

    return {
        **state,
        "response": (
            "Campaign generation failed validation after "
            "the maximum retry attempt."
        ),
    }


# ============================================================
# 16. BUILD LANGGRAPH
# ============================================================

graph = StateGraph(AgenticCampaignState)

graph.add_node(
    "classify_request",
    classify_request,
)

graph.add_node(
    "select_required_tools",
    select_required_tools,
)

graph.add_node(
    "product_tool",
    execute_product_tool,
)

graph.add_node(
    "customer_tool",
    execute_customer_tool,
)

graph.add_node(
    "marketing_tool",
    execute_marketing_tool,
)

graph.add_node(
    "combine_context",
    combine_context,
)

graph.add_node(
    "answer_information",
    answer_information,
)

graph.add_node(
    "generate_campaign",
    generate_campaign_node,
)

graph.add_node(
    "validate_campaign",
    validate_campaign,
)

graph.add_node(
    "retry_campaign",
    retry_campaign,
)

graph.add_node(
    "finish",
    finish,
)

graph.add_node(
    "failed",
    failed,
)


# ============================================================
# GRAPH EDGES
# ============================================================

graph.add_edge(
    START,
    "classify_request",
)

graph.add_edge(
    "classify_request",
    "select_required_tools",
)

graph.add_conditional_edges(
    "select_required_tools",
    route_first_tool,
    {
        "product_tool": "product_tool",
        "customer_tool": "customer_tool",
        "marketing_tool": "marketing_tool",
        "combine_context": "combine_context",
    },
)

graph.add_conditional_edges(
    "product_tool",
    route_next_tool,
    {
        "product_tool": "product_tool",
        "customer_tool": "customer_tool",
        "marketing_tool": "marketing_tool",
        "combine_context": "combine_context",
    },
)

graph.add_conditional_edges(
    "customer_tool",
    route_next_tool,
    {
        "product_tool": "product_tool",
        "customer_tool": "customer_tool",
        "marketing_tool": "marketing_tool",
        "combine_context": "combine_context",
    },
)

graph.add_conditional_edges(
    "marketing_tool",
    route_next_tool,
    {
        "product_tool": "product_tool",
        "customer_tool": "customer_tool",
        "marketing_tool": "marketing_tool",
        "combine_context": "combine_context",
    },
)


def route_after_context(
    state: AgenticCampaignState,
):

    if state["intent"] == "campaign":
        return "generate_campaign"

    return "answer_information"


graph.add_conditional_edges(
    "combine_context",
    route_after_context,
    {
        "generate_campaign": "generate_campaign",
        "answer_information": "answer_information",
    },
)

graph.add_edge(
    "answer_information",
    END,
)

graph.add_edge(
    "generate_campaign",
    "validate_campaign",
)

graph.add_conditional_edges(
    "validate_campaign",
    route_validation,
    {
        "finish": "finish",
        "retry": "retry_campaign",
        "failed": "failed",
    },
)

graph.add_edge(
    "retry_campaign",
    "validate_campaign",
)

graph.add_edge(
    "finish",
    END,
)

graph.add_edge(
    "failed",
    END,
)


agent = graph.compile()


# ============================================================
# 17. TEST FUNCTION
# ============================================================

def run_test(request: str):

    initial_state: AgenticCampaignState = {
        "message": request,

        "intent": "",

        "use_product_tool": False,
        "use_customer_tool": False,
        "use_marketing_tool": False,

        "customer_segment": "",

        "product_executed": False,
        "customer_executed": False,
        "marketing_executed": False,

        "product_context": "",
        "customer_context": "",
        "marketing_context": "",
        "combined_context": "",

        "response": "",
        "campaign": "",

        "validation_status": "",
        "validation_message": "",

        "retry_count": 0,
    }

    result = agent.invoke(initial_state)

    print("\n")
    print("=" * 70)
    print("REQUEST")
    print("=" * 70)
    print(request)

    print("\nINTENT")
    print("-" * 70)
    print(result["intent"])

    print("\nLLM TOOL SELECTION")
    print("-" * 70)

    print(
        "Product Tool:",
        result["use_product_tool"],
    )

    print(
        "Customer Tool:",
        result["use_customer_tool"],
    )

    print(
        "Marketing Tool:",
        result["use_marketing_tool"],
    )

    print(
        "Customer Segment:",
        result["customer_segment"],
    )

    print("\nMCP TOOLS EXECUTED")
    print("-" * 70)

    if result["product_executed"]:
        print("✓ Product MCP Tool")

    if result["customer_executed"]:
        print("✓ Customer MCP Tool")

    if result["marketing_executed"]:
        print("✓ Marketing Guidelines MCP Tool")

    print("\nRESPONSE")
    print("=" * 70)
    print(result["response"])

    if result["intent"] == "campaign":

        print("\nVALIDATION")
        print("-" * 70)

        print(result["validation_status"])

        print(result["validation_message"])

        print("\nRETRY COUNT")
        print("-" * 70)

        print(result["retry_count"])


# ============================================================
# 18. TEST CASES
# ============================================================

if __name__ == "__main__":

    test_requests = [

        "What are the features of the wireless headphones?",

        "What customers are in the young professionals segment?",

        "What marketing guidelines should I follow?",

        "Create a marketing campaign for wireless headphones targeting young professionals.",

        "Create a marketing campaign for SmartFit Watch targeting working professionals.",
    ]

    for request in test_requests:
        run_test(request)

    print("\n")
    print("=" * 70)
    print("MCP-INTEGRATED AGENTIC AI TEST COMPLETED")
    print("=" * 70)