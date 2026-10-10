from app.agents.intent_classifier import classify_intent


def test_campaign_intent():
    result = classify_intent(
        "Create a marketing campaign for wireless headphones."
    )

    assert result["intent"] == "campaign"


def test_information_intent():
    result = classify_intent(
        "What are the features of the wireless headphones?"
    )

    assert result["intent"] == "information"