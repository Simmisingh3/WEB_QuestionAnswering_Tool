from retriever import chunk_text


def test_chunk_text_returns_content_for_short_input():
    assert chunk_text("hello world", chunk_size=200, overlap=20) == ["hello world"]


def test_chunk_text_splits_long_text_with_overlap():
    text = " ".join(f"word{i}" for i in range(200))
    chunks = chunk_text(text, chunk_size=180, overlap=30)
    assert len(chunks) > 1
    assert all(chunks)
    assert all(len(chunk) <= 180 for chunk in chunks)
    assert set(chunks[0].split()) & set(chunks[1].split())


def test_chunk_text_normalizes_whitespace():
    assert chunk_text("  alpha\n\n beta   gamma ", chunk_size=200) == ["alpha beta gamma"]
