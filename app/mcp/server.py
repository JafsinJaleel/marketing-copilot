from mcp.server.mcpserver import MCPServer

from app.tools.product_tool import search_product
from app.tools.customer_tool import (
    create_database,
    search_customer_audience,
)
from app.tools.marketing_tool import search_marketing_guidelines


mcp = MCPServer("Marketing Copilot")


@mcp.tool()
def product_search(query: str) -> str:
    """Search the product knowledge base for product information and features."""
    return search_product(query)


@mcp.tool()
def customer_search(segment: str = "Young Professionals") -> str:
    """Search customer data for a target audience or customer segment."""
    create_database()
    return search_customer_audience(segment)


@mcp.tool()
def marketing_guidelines_search(query: str) -> str:
    """Search the approved marketing guidelines and content rules."""
    return search_marketing_guidelines(query)


if __name__ == "__main__":
    mcp.run(transport="stdio")