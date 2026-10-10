from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END

from app.rag.service import build_context
from app.llm.campaign_generator import (
    generate_campaign as generate_campaign_llm,
)


# ============================================================
# AGENT STATE
# ============================================================

class AgentState(TypedDict):
    message: str
    task: str
    request_type: str
    context: str
    campaign: str
    validation_status: str
    validation_message: str
    retry_count: int


# ============================================================
# 1. ANALYZE REQUEST
# ============================================================

def analyze_request(state: AgentState) -> AgentState:

    message = state["message"].lower()

    if "marketing" in message or "campaign" in message:
        request_type = "marketing"
    else:
        request_type = "unknown"

    return {
        **state,
        "request_type": request_type,
    }


# ============================================================
# 2. ROUTE REQUEST
# ============================================================

def route_request(
    state: AgentState,
) -> Literal["retrieve_knowledge", "reject_request"]:

    if state["request_type"] == "marketing":
        return "retrieve_knowledge"

    return "reject_request"


# ============================================================
# 3. RETRIEVE KNOWLEDGE
# ============================================================

def retrieve_knowledge(state: AgentState) -> AgentState:

    context = build_context(
        query=state["message"],
        top_k=2,
    )

    return {
        **state,
        "context": context,
    }


# ============================================================
# 4. PREPARE TASK
# ============================================================

def prepare_task(state: AgentState) -> AgentState:

    return {
        **state,
        "task": "Marketing task prepared: " + state["message"],
    }


# ============================================================
# 5. GENERATE CAMPAIGN
# ============================================================

def generate_campaign(state: AgentState) -> AgentState:

    campaign = generate_campaign_llm(
        user_request=state["message"],
        context=state["context"],
    )

    return {
        **state,
        "campaign": campaign,
    }


# ============================================================
# 6. VALIDATE CAMPAIGN
# ============================================================

def validate_campaign(state: AgentState) -> AgentState:

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

    # --------------------------------------------------------
    # Validation failed
    # --------------------------------------------------------

    if missing_sections:

        return {
            **state,
            "validation_status": "failed",
            "validation_message": (
                "Missing sections: "
                + ", ".join(missing_sections)
            ),
        }

    # --------------------------------------------------------
    # Validation passed
    # --------------------------------------------------------

    return {
        **state,
        "validation_status": "passed",
        "validation_message": "Campaign passed validation.",
    }


# ============================================================
# 7. DECIDE WHETHER TO RETRY
# ============================================================

def route_validation(
    state: AgentState,
) -> Literal["finish", "retry", "failed"]:

    # Campaign is valid
    if state["validation_status"] == "passed":
        return "finish"

    # Allow only one retry
    if state["retry_count"] < 1:
        return "retry"

    # Retry already used
    return "failed"


# ============================================================
# 8. RETRY CAMPAIGN
# ============================================================

def retry_campaign(state: AgentState) -> AgentState:

    new_retry_count = state["retry_count"] + 1

    retry_context = (
        state["context"]
        + "\n\n"
        + "Previous validation feedback:\n"
        + state["validation_message"]
        + "\n\n"
        + "Please correct the campaign according to the validation feedback."
    )

    campaign = generate_campaign_llm(
        user_request=state["message"],
        context=retry_context,
    )

    return {
        **state,
        "campaign": campaign,
        "retry_count": new_retry_count,
        "validation_message": "",
    }


# ============================================================
# 9. REJECT UNSUPPORTED REQUEST
# ============================================================

def reject_request(state: AgentState) -> AgentState:

    return {
        **state,
        "task": "Request is not a supported marketing task.",
        "campaign": "",
        "validation_status": "not_required",
        "validation_message": "",
    }


# ============================================================
# 10. FINISH SUCCESSFULLY
# ============================================================

def finish(state: AgentState) -> AgentState:

    return state


# ============================================================
# 11. FINAL FAILURE AFTER MAX RETRIES
# ============================================================

def failed(state: AgentState) -> AgentState:

    return {
        **state,
        "validation_status": "failed",
        "validation_message": (
            "Campaign failed validation after maximum retry attempts."
        ),
    }


# ============================================================
# LANGGRAPH
# ============================================================

graph_builder = StateGraph(AgentState)


# ------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------

graph_builder.add_node(
    "analyze_request",
    analyze_request,
)

graph_builder.add_node(
    "retrieve_knowledge",
    retrieve_knowledge,
)

graph_builder.add_node(
    "prepare_task",
    prepare_task,
)

graph_builder.add_node(
    "generate_campaign",
    generate_campaign,
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
    "reject_request",
    reject_request,
)

graph_builder.add_node(
    "failed",
    failed,
)


# ============================================================
# GRAPH FLOW
# ============================================================

# START
graph_builder.add_edge(
    START,
    "analyze_request",
)


# ------------------------------------------------------------
# Analyze → Request Router
# ------------------------------------------------------------

graph_builder.add_conditional_edges(
    "analyze_request",
    route_request,
    {
        "retrieve_knowledge": "retrieve_knowledge",
        "reject_request": "reject_request",
    },
)


# ------------------------------------------------------------
# Knowledge → Task → Generation
# ------------------------------------------------------------

graph_builder.add_edge(
    "retrieve_knowledge",
    "prepare_task",
)

graph_builder.add_edge(
    "prepare_task",
    "generate_campaign",
)

graph_builder.add_edge(
    "generate_campaign",
    "validate_campaign",
)


# ------------------------------------------------------------
# Validation → Finish / Retry / Failed
# ------------------------------------------------------------

graph_builder.add_conditional_edges(
    "validate_campaign",
    route_validation,
    {
        "finish": "finish",
        "retry": "retry_campaign",
        "failed": "failed",
    },
)


# ------------------------------------------------------------
# Retry → Validation
# ------------------------------------------------------------

graph_builder.add_edge(
    "retry_campaign",
    "validate_campaign",
)


# ------------------------------------------------------------
# END nodes
# ------------------------------------------------------------

graph_builder.add_edge(
    "finish",
    END,
)

graph_builder.add_edge(
    "reject_request",
    END,
)

graph_builder.add_edge(
    "failed",
    END,
)


# ============================================================
# COMPILE GRAPH
# ============================================================

graph = graph_builder.compile()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = graph.invoke(
        {
            "message": (
                "Create a marketing campaign for young professionals "
                "who want comfortable wireless audio with long battery life"
            ),
            "task": "",
            "request_type": "",
            "context": "",
            "campaign": "",
            "validation_status": "",
            "validation_message": "",
            "retry_count": 0,
        }
    )

    print("\n" + "=" * 60)
    print("LANGGRAPH MARKETING COPILOT")
    print("=" * 60)

    print("\nRequest:")
    print(result["message"])

    print("\nRequest Type:")
    print(result["request_type"])

    print("\nRetrieved Context:")
    print("-" * 60)
    print(result["context"])

    print("\nTask:")
    print(result["task"])

    print("\nGenerated Campaign:")
    print("-" * 60)
    print(result["campaign"])

    print("\nValidation:")
    print("-" * 60)
    print("Status:", result["validation_status"])
    print("Message:", result["validation_message"])

    print("\nRetry Count:")
    print(result["retry_count"])

    print("\n" + "=" * 60)