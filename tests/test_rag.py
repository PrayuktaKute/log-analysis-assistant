"""Tests for app.rag.knowledge_base and app.rag.retriever (real embeddings
+ real FAISS, no mocking)."""

from datetime import datetime, timezone

from app.config import settings
from app.models.schemas import (
    CorrelatedEvent,
    CorrelationEvidence,
    FailurePattern,
    HistoricalIncident,
)
from app.rag.knowledge_base import KnowledgeBaseLoader
from app.rag.retriever import IncidentRetriever
from app.vectorstore.faiss_store import FaissVectorStore

BASE = datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc)


# ---- KnowledgeBaseLoader ----


def test_knowledge_base_loader_loads_bundled_incidents():
    incidents = KnowledgeBaseLoader().load()
    assert len(incidents) >= 5
    assert all(isinstance(i, HistoricalIncident) for i in incidents)
    ids = {i.incident_id for i in incidents}
    assert "inc-004" in ids  # PLC incident, used by other tests


def test_knowledge_base_loader_missing_file_returns_empty(tmp_path):
    loader = KnowledgeBaseLoader(knowledge_base_dir=tmp_path)
    assert loader.load() == []


def test_knowledge_base_loader_custom_file(tmp_path):
    custom = tmp_path / "custom.json"
    custom.write_text(
        '[{"incident_id": "x", "title": "T", "summary": "S"}]', encoding="utf-8"
    )
    loader = KnowledgeBaseLoader(knowledge_base_dir=tmp_path)
    incidents = loader.load(filename="custom.json")
    assert len(incidents) == 1
    assert incidents[0].incident_id == "x"


# ---- IncidentRetriever ----


def _built_retriever() -> IncidentRetriever:
    store = FaissVectorStore(index_path=settings.faiss_index_dir / "test_retriever.index")
    store.build_index(KnowledgeBaseLoader().load())
    return IncidentRetriever(store)


def test_retrieve_for_query_finds_relevant_incident():
    retriever = _built_retriever()
    results = retriever.retrieve_for_query("PLC controller timing out", top_k=1)
    assert results[0].incident.incident_id == "inc-004"


def test_retrieve_for_pattern_finds_relevant_incident():
    retriever = _built_retriever()
    pattern = FailurePattern(
        pattern_id="pattern-test",
        description="'PLC communication timeout' recurred 5 time(s)",
        message="PLC communication timeout",
        occurrences=5,
        first_seen=BASE,
        last_seen=BASE,
        affected_sources=["application"],
        affected_services=["api-gateway"],
        affected_hosts=["wilston-prod-01"],
        sample_events=[],
    )

    results = retriever.retrieve_for_pattern(pattern, top_k=1)

    assert results[0].incident.incident_id == "inc-004"


def test_retrieve_for_correlated_event_finds_relevant_incident(make_entry, make_correlated_event):
    retriever = _built_retriever()
    trigger = make_entry(
        timestamp=BASE, severity="CRITICAL", message="PLC communication timeout", service="api-gateway", host="wilston-prod-01"
    )
    event = make_correlated_event(
        related_events=[trigger, trigger],
        structured_evidence=CorrelationEvidence(
            shared_host="wilston-prod-01",
            shared_service="api-gateway",
            shared_category="plc",
            cluster_size=2,
            time_span_seconds=5.0,
            involved_hosts_count=1,
            involved_components_count=1,
            distinct_messages=["PLC communication timeout"],
        ),
    )

    results = retriever.retrieve_for_correlated_event(event, top_k=1)

    assert results[0].incident.incident_id == "inc-004"
