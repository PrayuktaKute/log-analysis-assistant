"""Tests for app.embeddings.embedder (real sentence-transformers embeddings,
no mocking -- the model is small and already cached in this environment)."""

import pytest

from app.config import settings
from app.embeddings.embedder import Embedder


def test_embed_text_returns_correct_dimension():
    vector = Embedder().embed_text("Redis connection lost")
    assert len(vector) == settings.embedding_dimension
    assert all(isinstance(v, float) for v in vector)


def test_embed_batch_returns_one_vector_per_text():
    vectors = Embedder().embed_batch(["a", "b", "c"])
    assert len(vectors) == 3
    assert all(len(v) == settings.embedding_dimension for v in vectors)


def test_embed_is_deterministic():
    embedder = Embedder()
    assert embedder.embed_text("Kafka publish failed") == embedder.embed_text("Kafka publish failed")


def test_embed_different_texts_produce_different_vectors():
    embedder = Embedder()
    a = embedder.embed_text("Redis connection lost")
    b = embedder.embed_text("Completely unrelated sentence about weather")
    assert a != b


def test_embed_vectors_are_l2_normalized():
    vector = Embedder().embed_text("PLC communication timeout")
    norm = sum(v * v for v in vector) ** 0.5
    assert norm == pytest.approx(1.0, abs=1e-3)


def test_unsupported_provider_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        Embedder(provider="ollama").embed_text("hello")
