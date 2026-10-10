from app.llm.service import generate_campaign


campaign = generate_campaign(
    product_name="Wireless Headphones",
    target_audience="Young professionals aged 22–35",
    product_information="""
    Comfortable over-ear design
    Bluetooth connectivity
    30-hour battery life
    Available in black
    """,
)


print("Campaign Title:", campaign.campaign_title)
print("Target Audience:", campaign.target_audience)
print("Headline:", campaign.headline)
print("Body:", campaign.body)
print("Call To Action:", campaign.call_to_action)