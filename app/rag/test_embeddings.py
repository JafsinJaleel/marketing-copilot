from app.rag.embeddings import create_embedding
import numpy as np


texts = {
    "A": "Wireless headphones with 30-hour battery life.",
    "B": "Bluetooth headset with extended battery backup.",
    "C": "Chocolate cake recipe with vanilla frosting.",
}


embeddings = {
    name: create_embedding(text)
    for name, text in texts.items()
}


def cosine_similarity(vector_a, vector_b):
    return np.dot(vector_a, vector_b) / (
        np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    )


similarity_ab = cosine_similarity(
    embeddings["A"],
    embeddings["B"],
)

similarity_ac = cosine_similarity(
    embeddings["A"],
    embeddings["C"],
)

similarity_bc = cosine_similarity(
    embeddings["B"],
    embeddings["C"],
)


print("\nSemantic Similarity Results")
print("---------------------------")

print(f"A ↔ B: {similarity_ab:.4f}")
print(f"A ↔ C: {similarity_ac:.4f}")
print(f"B ↔ C: {similarity_bc:.4f}")