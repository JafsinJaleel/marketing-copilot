from app.llm.rag_service import prepare_campaign_request


user_request = """
Create a marketing campaign for a product suitable
for fitness-focused users.
"""


prompt = prepare_campaign_request(
    user_request=user_request,
    top_k=2,
)


print("\nRAG → LLM Request")
print("-----------------")

print(prompt)