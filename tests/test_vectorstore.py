"""Tests for app.vectorstore.faiss_store (real FAISS + real embeddings,
no mocking)."""

import pytest

from app.models.schemas import HistoricalIncident
from app.vectorstore.faiss_store import FaissVectorStore

INCIDENT_A = HistoricalIncident(
    incident_id="a",
    title="Redis cache outage",
    summary="Redis connection pool exhausted, causing cache misses across services.",
    tags=["cache", "redis"],
)
INCIDENT_B = HistoricalIncident(
    incident_id="b",
    title="PostgreSQL deadlocks during checkout",
    summary="Long-running transactions caused repeated deadlock errors under load.",
    tags=["database", "postgresql"],
)


def _store(tmp_path, dimension=384):
    return FaissVectorStore(index_path=tmp_path / "test.index", dimension=dimension)


def test_search_on_empty_index_returns_empty_list(tmp_path):
    store = _store(tmp_path)
    assert store.search("anything") == []


def test_build_index_and_search_returns_most_similar(tmp_path):
    store = _store(tmp_path)
    store.build_index([INCIDENT_A, INCIDENT_B])

    results = store.search("Redis connection failures", top_k=2)

    assert len(results) == 2
    assert results[0].incident.incident_id == "a"
    assert results[0].similarity_score > results[1].similarity_score
    assert -1.0 <= results[0].similarity_score <= 1.0


def test_search_top_k_is_capped_at_total_incidents(tmp_path):
    store = _store(tmp_path)
    store.build_index([INCIDENT_A])

    results = store.search("Redis", top_k=10)

    assert len(results) == 1


def test_add_incrementally(tmp_path):
    store = _store(tmp_path)
    store.build_index([INCIDENT_A])
    store.add([INCIDENT_B])

    results = store.search("deadlock in postgres", top_k=2)

    assert {r.incident.incident_id for r in results} == {"a", "b"}
    assert results[0].incident.incident_id == "b"


def test_save_and_load_roundtrip(tmp_path):
    store = _store(tmp_path)
    store.build_index([INCIDENT_A, INCIDENT_B])
    store.save()

    reloaded = FaissVectorStore(index_path=tmp_path / "test.index", dimension=384)
    reloaded.load()

    results = reloaded.search("Redis connection failures", top_k=1)
    assert results[0].incident.incident_id == "a"


def test_load_missing_index_raises_file_not_found(tmp_path):
    store = _store(tmp_path)
    with pytest.raises(FileNotFoundError):
        store.load()
