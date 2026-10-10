from app.rag.retriever import retrieve


def search_product(product_query: str) -> str:
    """
    Search the product knowledge base and return
    the most relevant product information.
    """

    results = retrieve(
        query=product_query,
        top_k=2,
    )

    if not results:
        return "No relevant product information found."

    product_results = []

    for result in results:
        product_results.append(
            f"""
SOURCE: {result["source"]}
SIMILARITY: {result["score"]:.4f}

{result["text"]}
"""
        )

    return "\n---\n".join(product_results)


if __name__ == "__main__":

    result = search_product(
        "wireless headphones with long battery life"
    )

    print("\nProduct Tool Result")
    print("-------------------")
    print(result)