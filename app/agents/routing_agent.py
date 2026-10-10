from typing import Literal, TypedDict

from langgraph.graph import StateGraph, START, END

from app.tools.registry import get_tool


# ============================================================
# AGENT STATE
# ============================================================

class RoutingAgentState(TypedDict):
    message: str
    intent: str
    tool_name: str
    tool_result: str


# ============================================================
# 1. ANALYZE REQUEST
# ============================================================

def analyze_request(
    state: RoutingAgentState,
) -> RoutingAgentState:

    message = state["message"].lower()

    # --------------------------------------------------------
    # Product-related keywords
    # --------------------------------------------------------

    product_keywords = [
        "product",
        "headphone",
        "headphones",
        "watch",
        "feature",
        "features",
        "battery",
        "bluetooth",
        "wearable",
        "audio",
    ]

    # --------------------------------------------------------
    # Marketing-guideline keywords
    # --------------------------------------------------------

    guideline_keywords = [
        "guideline",
        "guidelines",
        "rules",
        "marketing rules",
        "marketing guidelines",
        "marketing policy",
        "what should i follow",
        "what can i claim",
        "marketing requirements",
    ]

    # --------------------------------------------------------
    # Customer-related keywords
    # --------------------------------------------------------

    customer_keywords = [
        "customer",
        "customers",
        "audience",
        "target audience",
        "young professionals",
        "customer segment",
        "customer profile",
        "customer data",
        "customer information",
        "user segment",
    ]

    # --------------------------------------------------------
    # Determine intent
    # --------------------------------------------------------

    if any(
        keyword in message
        for keyword in guideline_keywords
    ):
        intent = "marketing_guidelines"

    elif any(
        keyword in message
        for keyword in customer_keywords
    ):
        intent = "customer"

    elif any(
        keyword in message
        for keyword in product_keywords
    ):
        intent = "product"

    else:
        intent = "unknown"

    return {
        **state,
        "intent": intent,
    }


# ============================================================
# 2. ROUTE REQUEST TO TOOL
# ============================================================

def route_tool(
    state: RoutingAgentState,
) -> Literal[
    "product_tool",
    "marketing_tool",
    "customer_tool",
    "unknown",
]:

    if state["intent"] == "product":
        return "product_tool"

    if state["intent"] == "marketing_guidelines":
        return "marketing_tool"

    if state["intent"] == "customer":
        return "customer_tool"

    return "unknown"


# ============================================================
# 3. PRODUCT TOOL
# ============================================================

def product_tool(
    state: RoutingAgentState,
) -> RoutingAgentState:

    tool = get_tool("search_product")

    if tool is None:
        raise ValueError(
            "search_product tool is not registered."
        )

    result = tool(
        state["message"]
    )

    return {
        **state,
        "tool_name": "search_product",
        "tool_result": result,
    }


# ============================================================
# 4. MARKETING GUIDELINES TOOL
# ============================================================

def marketing_tool(
    state: RoutingAgentState,
) -> RoutingAgentState:

    tool = get_tool(
        "search_marketing_guidelines"
    )

    if tool is None:
        raise ValueError(
            "search_marketing_guidelines tool "
            "is not registered."
        )

    result = tool(
        state["message"]
    )

    return {
        **state,
        "tool_name": "search_marketing_guidelines",
        "tool_result": result,
    }


# ============================================================
# 5. CUSTOMER TOOL
# ============================================================

def customer_tool(
    state: RoutingAgentState,
) -> RoutingAgentState:

    tool = get_tool(
        "search_customer_audience"
    )

    if tool is None:
        raise ValueError(
            "search_customer_audience tool "
            "is not registered."
        )

    # For now we use the Young Professionals
    # segment because that is the customer segment
    # currently available in our database.

    result = tool(
        "Young Professionals"
    )

    return {
        **state,
        "tool_name": "search_customer_audience",
        "tool_result": result,
    }


# ============================================================
# 6. UNKNOWN REQUEST
# ============================================================

def unknown_request(
    state: RoutingAgentState,
) -> RoutingAgentState:

    return {
        **state,
        "tool_name": "none",
        "tool_result": (
            "I could not determine which tool "
            "should handle this request."
        ),
    }


# ============================================================
# 7. FINISH
# ============================================================

def finish(
    state: RoutingAgentState,
) -> RoutingAgentState:

    return state


# ============================================================
# BUILD LANGGRAPH
# ============================================================

graph_builder = StateGraph(
    RoutingAgentState
)


# ============================================================
# ADD NODES
# ============================================================

graph_builder.add_node(
    "analyze_request",
    analyze_request,
)

graph_builder.add_node(
    "product_tool",
    product_tool,
)

graph_builder.add_node(
    "marketing_tool",
    marketing_tool,
)

graph_builder.add_node(
    "customer_tool",
    customer_tool,
)

graph_builder.add_node(
    "unknown",
    unknown_request,
)

graph_builder.add_node(
    "finish",
    finish,
)


# ============================================================
# GRAPH START
# ============================================================

graph_builder.add_edge(
    START,
    "analyze_request",
)


# ============================================================
# CONDITIONAL ROUTING
# ============================================================

graph_builder.add_conditional_edges(
    "analyze_request",
    route_tool,
    {
        "product_tool": "product_tool",
        "marketing_tool": "marketing_tool",
        "customer_tool": "customer_tool",
        "unknown": "unknown",
    },
)


# ============================================================
# TOOL → FINISH
# ============================================================

graph_builder.add_edge(
    "product_tool",
    "finish",
)

graph_builder.add_edge(
    "marketing_tool",
    "finish",
)

graph_builder.add_edge(
    "customer_tool",
    "finish",
)

graph_builder.add_edge(
    "unknown",
    "finish",
)


# ============================================================
# FINISH → END
# ============================================================

graph_builder.add_edge(
    "finish",
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

    test_requests = [

        # Product tool
        "What are the features of the wireless headphones?",

        # Marketing guidelines tool
        "What marketing guidelines should I follow?",

        # Marketing guidelines tool
        "What are the rules for creating marketing content?",

        # Product tool
        "Tell me about the SmartFit Watch.",

        # Customer tool
        "What customers are in the young professionals segment?",
    ]

    for request in test_requests:

        result = graph.invoke(
            {
                "message": request,
                "intent": "",
                "tool_name": "",
                "tool_result": "",
            }
        )

        print("\n" + "=" * 60)
        print("REQUEST")
        print("=" * 60)

        print(result["message"])

        print("\nDetected Intent:")
        print(result["intent"])

        print("\nSelected Tool:")
        print(result["tool_name"])

        print("\nTool Result:")
        print("-" * 60)

        print(result["tool_result"])

    print("\n" + "=" * 60)
    print("ROUTING TEST COMPLETED")
    print("=" * 60)