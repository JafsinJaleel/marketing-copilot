from app.llm.campaign_generator import generate_campaign


context = """
PRODUCT: SmartFit Watch

Category: Wearables

Description:
A smart wearable designed to help users monitor daily activity
and maintain an active lifestyle.

Features:
- Activity tracking
- Step tracking
- Daily fitness monitoring
- Lightweight design

Target Audience:
Fitness-focused users and active professionals.

Marketing Notes:
Focus on activity tracking, convenience, and everyday fitness.
Do not claim medical-grade monitoring.

MARKETING GUIDELINES:

1. Marketing content must be clear, concise, and professional.
2. Do not invent product specifications.
3. Do not make unsupported medical, performance, or technical claims.
4. Focus on genuine customer benefits.
5. Include a clear call to action.
"""


campaign = generate_campaign(
    user_request="Create a marketing campaign for fitness-focused users.",
    context=context,
)


print("\nCampaign Generator Test")
print("-----------------------")
print(campaign)