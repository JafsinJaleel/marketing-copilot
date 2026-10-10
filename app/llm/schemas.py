from pydantic import BaseModel


class MarketingCampaign(BaseModel):
    campaign_title: str
    target_audience: str
    headline: str
    body: str
    call_to_action: str