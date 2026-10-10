from app.rag.retriever import retrieve


def search_marketing_guidelines(query: str) -> str:
    """
    Search the knowledge base for approved marketing guidelines.
    """

    results = retrieve(
        query=query,
        top_k=2,
    )

    if not results:
        return "No relevant marketing guidelines found."

    guideline_results = []

    for result in results:
        guideline_results.append(
            f"""
SOURCE: {result["source"]}
SIMILARITY: {result["score"]:.4f}

{result["text"]}
"""
        )

    return "\n---\n".join(guideline_results)


if __name__ == "__main__":

    result = search_marketing_guidelines(
        "What rules should I follow when creating marketing content?"
    )

    print("\nMarketing Guidelines Tool Result")
    print("--------------------------------")
    print(result)