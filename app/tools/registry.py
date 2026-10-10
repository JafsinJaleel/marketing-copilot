from app.tools.product_tool import search_product
from app.tools.marketing_tool import search_marketing_guidelines
from app.tools.customer_tool import (
    create_database,
    search_customer_audience,
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

create_database()


# ============================================================
# TOOL REGISTRY
# ============================================================

TOOLS = {
    "search_product": search_product,
    "search_marketing_guidelines": search_marketing_guidelines,
    "search_customer_audience": search_customer_audience,
}


# ============================================================
# GET TOOL
# ============================================================

def get_tool(tool_name: str):
    """
    Return a registered tool by name.
    """

    return TOOLS.get(tool_name)


# ============================================================
# LIST TOOLS
# ============================================================

def list_tools() -> list[str]:
    """
    Return all registered tool names.
    """

    return list(TOOLS.keys())


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("\nRegistered Tools")
    print("----------------")

    for tool_name in list_tools():
        print("-", tool_name)