from app.rag.retriever import retrieve


query = "Which product is suitable for fitness-focused users?"


results = retrieve(
    query=query,
    top_k=3,
)


print("\nRetrieval Results")
print("-----------------")

print("Query:", query)


for result in results:

    print("\nChunk ID:", result["chunk_id"])
    print("Source:", result["source"])
    print("Similarity:", f"{result['score']:.4f}")
    print("Text:")
    print(result["text"])