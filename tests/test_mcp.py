from app.mcp.client import call_mcp_tool


def test_product_mcp_tool():
    result = call_mcp_tool(
        "product_search",
        {"query": "wireless headphones"}
    )

    assert "Wireless Headphones" in result


def test_customer_mcp_tool():
    result = call_mcp_tool(
        "customer_search",
        {"segment": "Young Professionals"}
    )

    assert "Arjun" in result


def test_marketing_mcp_tool():
    result = call_mcp_tool(
        "marketing_guidelines_search",
        {"query": "marketing campaign guidelines"}
    )

    assert "marketing" in result.lower()