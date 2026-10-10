from pathlib import Path


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


def chunk_text(text: str) -> list[str]:

    sections = [
        section.strip()
        for section in text.split("\n---\n")
        if section.strip()
    ]

    return sections


def create_chunks() -> list[dict]:

    chunks = []

    for document in load_documents():

        document_chunks = chunk_text(
            document["text"]
        )

        for index, chunk in enumerate(document_chunks):

            chunks.append(
                {
                    "chunk_id": f"{document['source']}_{index}",
                    "source": document["source"],
                    "text": chunk,
                }
            )

    return chunks