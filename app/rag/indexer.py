import json
from pathlib import Path

from app.rag.chunker import create_chunks
from app.rag.embeddings import create_embedding


VECTOR_STORE_PATH = Path("vector_store/chunks.json")


def build_vector_store():

    chunks = create_chunks()

    vector_store = []

    for chunk in chunks:

        embedding = create_embedding(
            chunk["text"]
        )

        vector_store.append(
            {
                "chunk_id": chunk["chunk_id"],
                "source": chunk["source"],
                "text": chunk["text"],
                "embedding": embedding,
            }
        )

    VECTOR_STORE_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    VECTOR_STORE_PATH.write_text(
        json.dumps(vector_store),
        encoding="utf-8",
    )

    print(
        f"Vector store created with {len(vector_store)} chunks."
    )


if __name__ == "__main__":
    build_vector_store()