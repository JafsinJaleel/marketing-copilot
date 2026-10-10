from app.agents.agentic_campaign import agent


def create_state(message: str):
    return {
        "message": message,
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


def test_product_information_agent():
    state = create_state(
        "What are the features of the wireless headphones?"
    )

    result = agent.invoke(state)

    assert result["intent"] == "information"
    assert result["product_executed"] is True
    assert result["response"] != ""


def test_working_professionals_segment():
    state = create_state(
        "What customers are in the working professionals segment?"
    )

    result = agent.invoke(state)

    assert result["intent"] == "information"
    assert result["use_customer_tool"] is True
    assert result["customer_segment"] == "Working Professionals"
    assert result["customer_executed"] is True
    assert "Sneha" in result["customer_context"]