from app.rag.search import semantic_search


query = "Which product has long battery life?"


results = semantic_search(query, top_k=2)


print("\nSemantic Search Results")
print("-----------------------")

for result in results:
    print(f"\nSource: {result['source']}")
    print(f"Similarity: {result['score']:.4f}")
    print("Content:")
    print(result["text"][:300])