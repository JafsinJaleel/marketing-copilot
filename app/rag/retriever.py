import json
from pathlib import Path

import numpy as np

from app.rag.embeddings import create_embedding


VECTOR_STORE_PATH = Path("vector_store/chunks.json")


def load_vector_store() -> list[dict]:
    data = VECTOR_STORE_PATH.read_text(
        encoding="utf-8"
    )

    return json.loads(data)


def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:

    vector_a = np.array(vector_a)
    vector_b = np.array(vector_b)

    return float(
        np.dot(vector_a, vector_b)
        / (
            np.linalg.norm(vector_a)
            * np.linalg.norm(vector_b)
        )
    )


def retrieve(
    query: str,
    top_k: int = 3,
) -> list[dict]:

    vector_store = load_vector_store()

    query_embedding = create_embedding(query)

    results = []

    for chunk in vector_store:

        score = cosine_similarity(
            query_embedding,
            chunk["embedding"],
        )

        results.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "score": score,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]