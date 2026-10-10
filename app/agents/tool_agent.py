from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.tools.registry import get_tool
from app.llm.campaign_generator import (
    generate_campaign as generate_campaign_llm,
)


# ============================================================
# AGENT STATE
# ============================================================

class ToolAgentState(TypedDict):
    message: str
    product_query: str
    product_context: str
    campaign: str


# ============================================================
# 1. ANALYZE USER REQUEST
# ============================================================

def analyze_request(state: ToolAgentState) -> ToolAgentState:

    message = state["message"]

    return {
        **state,
        "product_query": message,
    }


# ============================================================
# 2. SELECT PRODUCT TOOL
# ============================================================

def select_product_tool(state: ToolAgentState) -> ToolAgentState:

    tool = get_tool("search_product")

    if tool is None:
        raise ValueError("search_product tool is not registered.")

    product_context = tool(
        state["product_query"]
    )

    return {
        **state,
        "product_context": product_context,
    }


# ============================================================
# 3. GENERATE CAMPAIGN
# ============================================================

def generate_campaign(state: ToolAgentState) -> ToolAgentState:

    campaign = generate_campaign_llm(
        user_request=state["message"],
        context=state["product_context"],
    )

    return {
        **state,
        "campaign": campaign,
    }


# ============================================================
# LANGGRAPH
# ============================================================

graph_builder = StateGraph(ToolAgentState)


# ------------------------------------------------------------
# Nodes
# ------------------------------------------------------------

graph_builder.add_node(
    "analyze_request",
    analyze_request,
)

graph_builder.add_node(
    "select_product_tool",
    select_product_tool,
)

graph_builder.add_node(
    "generate_campaign",
    generate_campaign,
)


# ------------------------------------------------------------
# Graph flow
# ------------------------------------------------------------

graph_builder.add_edge(
    START,
    "analyze_request",
)

graph_builder.add_edge(
    "analyze_request",
    "select_product_tool",
)

graph_builder.add_edge(
    "select_product_tool",
    "generate_campaign",
)

graph_builder.add_edge(
    "generate_campaign",
    END,
)


# ------------------------------------------------------------
# Compile
# ------------------------------------------------------------

graph = graph_builder.compile()


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    result = graph.invoke(
        {
            "message": (
                "Create a marketing campaign for young professionals "
                "who want comfortable wireless audio with long battery life."
            ),
            "product_query": "",
            "product_context": "",
            "campaign": "",
        }
    )

    print("\n" + "=" * 60)
    print("LANGGRAPH TOOL AGENT")
    print("=" * 60)

    print("\nUser Request:")
    print(result["message"])

    print("\nProduct Query:")
    print(result["product_query"])

    print("\nProduct Tool Result:")
    print("-" * 60)
    print(result["product_context"])

    print("\nGenerated Campaign:")
    print("-" * 60)
    print(result["campaign"])

    print("\n" + "=" * 60)