import json
from typing import Literal, TypedDict

from app.llm.ollama_service import generate_text


class IntentResult(TypedDict):
    intent: Literal["information", "campaign"]


def classify_intent(user_request: str) -> IntentResult:
    """
    Classify the user's request into one of two intents:

    information:
        The user wants information, facts, product details,
        customer information, or marketing guidelines.

    campaign:
        The user wants us to create or generate marketing
        content or a marketing campaign.
    """

    system_prompt = """
You are an intent-classification agent for an AI Marketing Copilot.

Classify the user's request into exactly one of these intents:

1. "information"
   Use this when the user wants to know something, retrieve
   information, inspect product details, find customer data,
   or understand marketing guidelines.

2. "campaign"
   Use this when the user explicitly wants you to create,
   generate, write, or produce a marketing campaign or
   marketing content.

Return ONLY valid JSON.

Use exactly this structure:

{
  "intent": "information"
}

or:

{
  "intent": "campaign"
}

Do not add explanations.
"""

    user_prompt = f"""
User request:

{user_request}

Classify this request.
"""

    response = generate_text(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    try:
        result = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid intent JSON returned by Qwen3: {response}"
        ) from exc

    intent = result.get("intent")

    if intent not in {"information", "campaign"}:
        raise ValueError(
            f"Invalid intent: {intent}"
        )

    return {
        "intent": intent
    }


if __name__ == "__main__":

    test_requests = [
        "What are the features of the wireless headphones?",

        "What customers are in the young professionals segment?",

        "What marketing guidelines should I follow?",

        "Create a marketing campaign for wireless headphones.",

        "Write a campaign for the SmartFit Watch.",
    ]

    for request in test_requests:

        print("\n" + "=" * 70)
        print("REQUEST")
        print("=" * 70)
        print(request)

        result = classify_intent(request)

        print("\nINTENT")
        print("-" * 70)
        print(result["intent"])