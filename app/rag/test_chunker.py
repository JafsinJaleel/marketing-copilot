from app.rag.chunker import create_chunks


chunks = create_chunks()


print("\nDocument Chunks")
print("----------------")

print("Total chunks:", len(chunks))


for chunk in chunks:
    print("\nChunk ID:", chunk["chunk_id"])
    print("Source:", chunk["source"])
    print("Text:", chunk["text"][:250])