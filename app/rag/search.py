from pathlib import Path

import numpy as np

from app.rag.embeddings import create_embedding


KNOWLEDGE_DIR = Path("data/knowledge")


def load_documents() -> list[dict]:
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        documents.append(
            {
                "source": file_path.name,
                "text": text,
            }
        )

    return documents


def cosine_similarity(vector_a, vector_b) -> float:
    return float(
        np.dot(vector_a, vector_b)
        / (
            np.linalg.norm(vector_a)
            * np.linalg.norm(vector_b)
        )
    )


def semantic_search(
    query: str,
    top_k: int = 2,
) -> list[dict]:

    documents = load_documents()

    query_embedding = create_embedding(query)

    results = []

    for document in documents:
        document_embedding = create_embedding(document["text"])

        score = cosine_similarity(
            query_embedding,
            document_embedding,
        )

        results.append(
            {
                "source": document["source"],
                "text": document["text"],
                "score": score,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]