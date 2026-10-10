from app.rag.service import build_context
from app.rag.prompt import build_rag_prompt
from app.llm.schemas import MarketingCampaign


def prepare_campaign_request(
    user_request: str,
    top_k: int = 2,
) -> str:

    context = build_context(
        query=user_request,
        top_k=top_k,
    )

    prompt = build_rag_prompt(
        user_request=user_request,
        context=context,
    )

    return prompt