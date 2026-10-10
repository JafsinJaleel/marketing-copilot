from app.llm.client import client
from app.llm.schemas import MarketingCampaign
from app.llm.rag_service import prepare_campaign_request


def generate_campaign_with_rag(
    user_request: str,
    top_k: int = 2,
) -> MarketingCampaign:

    prompt = prepare_campaign_request(
        user_request=user_request,
        top_k=top_k,
    )

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
You are an AI Marketing Copilot.

Return the campaign using the required
MarketingCampaign structure.

Use ONLY the approved knowledge provided
in the user prompt.

Do not invent product specifications,
features, or unsupported claims.
""",
        input=prompt,
        text_format=MarketingCampaign,
    )

    return response.output_parsed