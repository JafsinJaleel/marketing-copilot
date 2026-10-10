from app.agents.tool_selector import select_tools


def test_product_tool_selection():
    result = select_tools(
        "What are the features of the wireless headphones?"
    )

    assert result["use_product_tool"] is True
    assert result["use_customer_tool"] is False
    assert result["use_marketing_tool"] is False


def test_customer_tool_selection():
    result = select_tools(
        "What customers are in the young professionals segment?"
    )

    assert result["use_product_tool"] is False
    assert result["use_customer_tool"] is True
    assert result["use_marketing_tool"] is False


def test_marketing_tool_selection():
    result = select_tools(
        "What marketing guidelines should I follow?"
    )

    assert result["use_product_tool"] is False
    assert result["use_customer_tool"] is False
    assert result["use_marketing_tool"] is True


def test_campaign_tool_selection():
    result = select_tools(
        "Create a marketing campaign for wireless headphones "
        "targeting young professionals."
    )

    assert result["use_product_tool"] is True
    assert result["use_customer_tool"] is True
    assert result["use_marketing_tool"] is True