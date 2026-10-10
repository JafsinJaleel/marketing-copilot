from app.rag.service import build_context


query = "Which product is suitable for fitness-focused users?"


context = build_context(
    query=query,
    top_k=2,
)


print("\nRAG Context")
print("-----------")

print(context)