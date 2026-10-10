from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.tools.registry import get_tool
from app.llm.campaign_generator import generate_campaign


# ============================================================
# AGENT STATE
# ============================================================

class MultiToolAgentState(TypedDict):
    message: str

    product_context: str
    customer_context: str
    marketing_context: str

    combined_context: str

    campaign: str

    validation_status: str
    validation_message: str

    retry_count: int


# ============================================================
# 1. COLLECT PRODUCT INFORMATION
# ============================================================

def get_product_context(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    tool = get_tool("search_product")

    if tool is None:
        raise ValueError(
            "search_product tool is not registered."
        )

    result = tool(state["message"])

    return {
        **state,
        "product_context": result,
    }


# ============================================================
# 2. COLLECT CUSTOMER INFORMATION
# ============================================================

def get_customer_context(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    tool = get_tool(
        "search_customer_audience"
    )

    if tool is None:
        raise ValueError(
            "search_customer_audience tool "
            "is not registered."
        )

    result = tool("Young Professionals")

    return {
        **state,
        "customer_context": result,
    }


# ============================================================
# 3. COLLECT MARKETING GUIDELINES
# ============================================================

def get_marketing_context(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    tool = get_tool(
        "search_marketing_guidelines"
    )

    if tool is None:
        raise ValueError(
            "search_marketing_guidelines tool "
            "is not registered."
        )

    result = tool(
        "Rules and guidelines for creating "
        "marketing campaigns"
    )

    return {
        **state,
        "marketing_context": result,
    }


# ============================================================
# 4. COMBINE ALL TOOL RESULTS
# ============================================================

def combine_context(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    combined_context = f"""
================ PRODUCT INFORMATION ================

{state["product_context"]}


================ CUSTOMER INFORMATION ================

{state["customer_context"]}


================ MARKETING GUIDELINES ================

{state["marketing_context"]}
"""

    return {
        **state,
        "combined_context": combined_context,
    }


# ============================================================
# 5. GENERATE CAMPAIGN
# ============================================================

def generate_campaign_node(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    campaign = generate_campaign(
        user_request=state["message"],
        context=state["combined_context"],
    )

    return {
        **state,
        "campaign": campaign,
    }


# ============================================================
# 6. VALIDATE CAMPAIGN
# ============================================================

def validate_campaign(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

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
# 7. VALIDATION ROUTER
# ============================================================

def route_validation(
    state: MultiToolAgentState,
) -> str:

    if state["validation_status"] == "passed":
        return "finish"

    if state["retry_count"] < 1:
        return "retry"

    return "failed"


# ============================================================
# 8. RETRY CAMPAIGN
# ============================================================

def retry_campaign(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    retry_count = state["retry_count"] + 1

    retry_context = f"""
{state["combined_context"]}

IMPORTANT VALIDATION FEEDBACK:

{state["validation_message"]}

Regenerate the campaign and make sure
all required sections are included.
"""

    campaign = generate_campaign(
        user_request=state["message"],
        context=retry_context,
    )

    return {
        **state,
        "campaign": campaign,
        "retry_count": retry_count,
    }


# ============================================================
# 9. FINISH
# ============================================================

def finish(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    return state


# ============================================================
# 10. FAILED
# ============================================================

def failed(
    state: MultiToolAgentState,
) -> MultiToolAgentState:

    return {
        **state,
        "campaign": (
            "Campaign generation failed after "
            "validation retry."
        ),
    }


# ============================================================
# BUILD LANGGRAPH
# ============================================================

graph_builder = StateGraph(
    MultiToolAgentState
)


# ============================================================
# ADD NODES
# ============================================================

graph_builder.add_node(
    "get_product_context",
    get_product_context,
)

graph_builder.add_node(
    "get_customer_context",
    get_customer_context,
)

graph_builder.add_node(
    "get_marketing_context",
    get_marketing_context,
)

graph_builder.add_node(
    "combine_context",
    combine_context,
)

graph_builder.add_node(
    "generate_campaign",
    generate_campaign_node,
)

graph_builder.add_node(
    "validate_campaign",
    validate_campaign,
)

graph_builder.add_node(
    "retry_campaign",
    retry_campaign,
)

graph_builder.add_node(
    "finish",
    finish,
)

graph_builder.add_node(
    "failed",
    failed,
)


# ============================================================
# GRAPH FLOW
# ============================================================

graph_builder.add_edge(
    START,
    "get_product_context",
)

graph_builder.add_edge(
    "get_product_context",
    "get_customer_context",
)

graph_builder.add_edge(
    "get_customer_context",
    "get_marketing_context",
)

graph_builder.add_edge(
    "get_marketing_context",
    "combine_context",
)

graph_builder.add_edge(
    "combine_context",
    "generate_campaign",
)

graph_builder.add_edge(
    "generate_campaign",
    "validate_campaign",
)


# ============================================================
# VALIDATION ROUTING
# ============================================================

graph_builder.add_conditional_edges(
    "validate_campaign",
    route_validation,
    {
        "finish": "finish",
        "retry": "retry_campaign",
        "failed": "failed",
    },
)


graph_builder.add_edge(
    "retry_campaign",
    "validate_campaign",
)

graph_builder.add_edge(
    "finish",
    END,
)

graph_builder.add_edge(
    "failed",
    END,
)


# ============================================================
# COMPILE
# ============================================================

graph = graph_builder.compile()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    request = (
        "Create a marketing campaign for "
        "wireless headphones targeting "
        "young professionals."
    )

    result = graph.invoke(
        {
            "message": request,

            "product_context": "",

            "customer_context": "",

            "marketing_context": "",

            "combined_context": "",

            "campaign": "",

            "validation_status": "",

            "validation_message": "",

            "retry_count": 0,
        }
    )

    print("\n" + "=" * 70)
    print("MULTI-TOOL MARKETING AGENT")
    print("=" * 70)

    print("\nUSER REQUEST")
    print("-" * 70)
    print(result["message"])

    print("\nPRODUCT CONTEXT")
    print("-" * 70)
    print(result["product_context"])

    print("\nCUSTOMER CONTEXT")
    print("-" * 70)
    print(result["customer_context"])

    print("\nMARKETING GUIDELINES")
    print("-" * 70)
    print(result["marketing_context"])

    print("\nVALIDATION")
    print("-" * 70)
    print(result["validation_status"])
    print(result["validation_message"])

    print("\nRETRY COUNT")
    print("-" * 70)
    print(result["retry_count"])

    print("\nFINAL CAMPAIGN")
    print("=" * 70)
    print(result["campaign"])

    print("\n" + "=" * 70)
    print("MULTI-TOOL AGENT TEST COMPLETED")
    print("=" * 70)