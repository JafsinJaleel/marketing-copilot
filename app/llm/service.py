from app.llm.client import client
from app.llm.schemas import MarketingCampaign


def generate_campaign(
    product_name: str,
    target_audience: str,
    product_information: str,
) -> MarketingCampaign:

    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions="""
You are an AI Marketing Copilot.

Create concise and professional marketing campaigns.

Rules:
1. Use only the product information provided.
2. Do not invent product specifications.
3. Focus on customer benefits.
4. Use a professional marketing tone.
5. Return the campaign using the required structure.
""",
        input=f"""
Create a marketing campaign.

Product:
{product_name}

Target audience:
{target_audience}

Product information:
{product_information}
""",
        text_format=MarketingCampaign,
    )

    return response.output_parsed