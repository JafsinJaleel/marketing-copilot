from app.rag.retriever import retrieve


def test_wireless_headphones_retrieval():
    results = retrieve(
        "wireless headphones with long battery life",
        top_k=2,
    )

    assert len(results) == 2

    top_result = results[0]

    assert "Wireless Headphones" in top_result["text"]
    assert top_result["score"] > 0


def test_smartfit_watch_retrieval():
    results = retrieve(
        "fitness watch for activity and step tracking",
        top_k=2,
    )

    assert len(results) == 2

    top_result = results[0]

    assert "SmartFit Watch" in top_result["text"]
    assert top_result["score"] > 0