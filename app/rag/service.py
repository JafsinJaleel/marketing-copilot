from app.rag.retriever import retrieve


def build_context(
    query: str,
    top_k: int = 3,
) -> str:

    results = retrieve(
        query=query,
        top_k=top_k,
    )

    context_parts = []

    for result in results:

        context_parts.append(
            f"""
SOURCE: {result["source"]}
SIMILARITY: {result["score"]:.4f}

{result["text"]}
"""
        )

    return "\n---\n".join(context_parts)