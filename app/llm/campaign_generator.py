from app.llm.ollama_service import generate_text


def generate_campaign(
    user_request: str,
    context: str,
) -> str:

    system_prompt = """
You are an AI Marketing Copilot.

Your job is to create a professional marketing campaign
using ONLY the approved knowledge provided by the user.

Rules:
1. Do not invent product specifications.
2. Do not invent product features.
3. Do not make unsupported medical or technical claims.
4. Match the campaign to the target audience.
5. Focus on genuine customer benefits.
6. Include a clear call to action.
7. Return ONLY the campaign.
8. Do not explain your reasoning.
9. Do not add notes about why the campaign works.

Use exactly this structure:

Campaign Title:
Target Audience:
Headline:
Body:
Call To Action:
"""

    user_prompt = f"""
Create a marketing campaign for this request:

{user_request}

Approved Knowledge:
{context}
"""

    return generate_text(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )