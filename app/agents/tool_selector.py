import json
from typing import TypedDict

from app.llm.ollama_service import generate_text


class ToolSelection(TypedDict):
    use_product_tool: bool
    use_customer_tool: bool
    use_marketing_tool: bool
    customer_segment: str


def select_tools(user_request: str) -> ToolSelection:
    """
    Use the local Qwen3 model to determine which tools are required
    and extract the target customer segment when applicable.
    """

    system_prompt = """
You are the tool-selection agent for an AI Marketing Copilot.

You have access to exactly three tools.

============================================================
1. PRODUCT TOOL
============================================================

Use the Product Tool when the request requires:

- Product information
- Product features
- Product specifications
- Product benefits
- Product details

============================================================
2. CUSTOMER TOOL
============================================================

Use the Customer Tool when the request requires:

- Customer information
- Customer segments
- Target audience information
- Customer demographics
- Audience profiles

If a target audience or customer segment is mentioned,
extract the segment exactly as understood from the request.

Examples:

"targeting young professionals"
→ "Young Professionals"

"for working professionals"
→ "Working Professionals"

"aimed at fitness-focused users"
→ "Fitness-focused Users"

If no customer segment is mentioned:
→ ""

============================================================
3. MARKETING GUIDELINES TOOL
============================================================

Use the Marketing Guidelines Tool when the request requires:

- Marketing rules
- Marketing guidelines
- Content requirements
- Messaging rules
- Marketing claims
- Campaign-writing rules

============================================================
IMPORTANT CAMPAIGN RULE
============================================================

When the user asks you to CREATE, WRITE, GENERATE,
or PRODUCE a marketing campaign:

- ALWAYS use the Marketing Guidelines Tool.

- Use the Product Tool if a specific product is mentioned
  or product information is needed.

- Use the Customer Tool if a target audience, customer segment,
  demographic group, or audience is mentioned.

============================================================
EXAMPLES
============================================================

Request:
"Create a marketing campaign for wireless headphones."

Required tools:
Product = true
Customer = false
Marketing = true
Customer Segment = ""


Request:
"Create a marketing campaign for wireless headphones
targeting young professionals."

Required tools:
Product = true
Customer = true
Marketing = true
Customer Segment = "Young Professionals"


Request:
"Create a campaign for SmartFit Watch targeting
working professionals."

Required tools:
Product = true
Customer = true
Marketing = true
Customer Segment = "Working Professionals"


Request:
"What are the features of the wireless headphones?"

Required tools:
Product = true
Customer = false
Marketing = false
Customer Segment = ""


Request:
"What customers are in the young professionals segment?"

Required tools:
Product = false
Customer = true
Marketing = false
Customer Segment = "Young Professionals"


Request:
"What marketing guidelines should I follow?"

Required tools:
Product = false
Customer = false
Marketing = true
Customer Segment = ""

============================================================
OUTPUT FORMAT
============================================================

Return ONLY valid JSON.

Use exactly these four fields:

{
  "use_product_tool": true,
  "use_customer_tool": true,
  "use_marketing_tool": true,
  "customer_segment": "Young Professionals"
}

Rules:

- use_product_tool must be true or false.
- use_customer_tool must be true or false.
- use_marketing_tool must be true or false.
- customer_segment must be a string.
- Use an empty string when no customer segment is mentioned.
- Do not add explanations.
- Do not use Markdown.
- Do not add any other fields.
"""

    user_prompt = f"""
User request:

{user_request}

Determine exactly which tools are required
and extract the target customer segment if present.
"""

    response = generate_text(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    print("\nRAW TOOL SELECTION RESPONSE")
    print("-" * 60)
    print(response)

    try:
        selection = json.loads(response)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Qwen3 returned invalid JSON: {response}"
        ) from exc

    customer_segment = selection.get(
        "customer_segment",
        "",
    )

    if customer_segment is None:
        customer_segment = ""

    return {
        "use_product_tool": bool(
            selection.get("use_product_tool", False)
        ),
        "use_customer_tool": bool(
            selection.get("use_customer_tool", False)
        ),
        "use_marketing_tool": bool(
            selection.get("use_marketing_tool", False)
        ),
        "customer_segment": str(customer_segment).strip(),
    }


if __name__ == "__main__":

    test_requests = [

        "What are the features of the wireless headphones?",

        "What customers are in the young professionals segment?",

        "What marketing guidelines should I follow?",

        "Create a marketing campaign for wireless headphones.",

        (
            "Create a marketing campaign for wireless "
            "headphones targeting young professionals."
        ),

        (
            "Create a marketing campaign for SmartFit Watch "
            "targeting working professionals."
        ),

        "Write a campaign for the SmartFit Watch.",
    ]

    for request in test_requests:

        print("\n" + "=" * 70)
        print("REQUEST")
        print("=" * 70)

        print(request)

        result = select_tools(request)

        print("\nSELECTED TOOLS")
        print("-" * 60)

        print(
            "Product Tool:",
            result["use_product_tool"],
        )

        print(
            "Customer Tool:",
            result["use_customer_tool"],
        )

        print(
            "Marketing Tool:",
            result["use_marketing_tool"],
        )

        print(
            "Customer Segment:",
            result["customer_segment"],
        )