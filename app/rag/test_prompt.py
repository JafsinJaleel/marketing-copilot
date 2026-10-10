from app.rag.service import build_context
from app.rag.prompt import build_rag_prompt


user_request = """
Create a marketing campaign for a product suitable
for fitness-focused users.
"""


context = build_context(
    query=user_request,
    top_k=2,
)


prompt = build_rag_prompt(
    user_request=user_request,
    context=context,
)


print("\nGenerated RAG Prompt")
print("--------------------")

print(prompt)