"""Tests for app.llm.qa_engine: deterministic relevance selection (pure, no
LLM), and the full prepare -> call -> parse pipeline against a fake LLM
client (dependency injection, no real Ollama needed for most tests). A
single live smoke test at the bottom exercises the real pipeline
end-to-end and skips gracefully if Ollama isn't reachable.
"""

import asyncio
import json
from datetime import datetime, timedelta, timezone

import httpx
import pytest

from app.config import settings
from app.llm.ollama_client import OllamaClient, OllamaUnavailableError
from app.llm.qa_engine import QAEngine, _select_relevant_context
from app.models.schemas import LogSeverity
from app.rag.knowledge_base import KnowledgeBaseLoader
from app.rag.retriever import IncidentRetriever
from app.vectorstore.faiss_store import FaissVectorStore

BASE = datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc)


def t(seconds: float) -> datetime:
    return BASE + timedelta(seconds=seconds)


class _FakeRetriever:
    def retrieve_for_query(self, query, top_k=5):
        return []

    def retrieve_for_pattern(self, pattern, top_k=5):
        return []

    def retrieve_for_correlated_event(self, event, top_k=5):
        return []


class _FakeLLMClient:
    """Duck-types OllamaClient's chat()/achat() surface with a canned response."""

    def __init__(self, response: str):
        self.response = response
        self.calls: list[list[dict]] = []

    def chat(self, messages, format=None):
        self.calls.append(messages)
        return self.response

    async def achat(self, messages, format=None):
        self.calls.append(messages)
        return self.response


class _FailingLLMClient:
    def __init__(self, exc: Exception):
        self.exc = exc

    def chat(self, messages, format=None):
        raise self.exc

    async def achat(self, messages, format=None):
        raise self.exc


VALID_QA_RESPONSE = json.dumps(
    {
        "answer": "api-gateway generated the most errors.",
        "current_log_evidence": ["- api-gateway had the highest failure_count"],
        "historical_incidents": [],
        "ai_reasoning": "Ranked components by failure_count.",
        "recommendations": [],
        "confidence_level": "medium",
        "evidence_sufficient": True,
    }
)

VALID_INVESTIGATION_RESPONSE = json.dumps(
    {
        "executive_summary": "summary",
        "incident_summary": "details",
        "possible_root_causes": [],
        "supporting_evidence": [],
        "similar_historical_incidents": [],
        "recommended_actions": [],
        "confidence_level": "low",
        "open_questions": [],
        "evidence_sufficient": True,
    }
)


# ---- _select_relevant_context (deterministic, no LLM) ----


def test_select_relevant_context_filters_by_category(make_entry, make_report):
    pg_entries = [
        make_entry(timestamp=t(i), severity=LogSeverity.ERROR, message="PostgreSQL error: deadlock detected")
        for i in range(3)
    ]
    other_entries = [
        make_entry(timestamp=t(10 + i), severity=LogSeverity.ERROR, message="Kafka publish failed") for i in range(3)
    ]
    report = make_report(pg_entries + other_entries)

    context = _select_relevant_context("Show PostgreSQL errors.", report, pg_entries + other_entries, top_n=10)

    assert all(g.message == "PostgreSQL error: deadlock detected" for g in context.relevant_error_groups)
    assert all(e.message == "PostgreSQL error: deadlock detected" for e in context.relevant_entries)


def test_select_relevant_context_filters_by_component(make_entry, make_report):
    entries = [
        make_entry(
            timestamp=t(0), severity=LogSeverity.ERROR, message="boom", service="payment-service", host="wilston-prod-01"
        ),
        make_entry(
            timestamp=t(1), severity=LogSeverity.ERROR, message="boom", service="auth-service", host="wilston-prod-02"
        ),
    ]
    report = make_report(entries)

    context = _select_relevant_context("What's wrong with payment-service?", report, entries, top_n=10)

    assert {c.component for c in context.component_summary} == {"payment-service"}


def test_select_relevant_context_falls_back_to_top_n_when_no_match(make_entry, make_report):
    entries = [make_entry(timestamp=t(i), severity=LogSeverity.ERROR, message="boom") for i in range(3)]
    report = make_report(entries)

    context = _select_relevant_context("What are the most critical failures?", report, entries, top_n=10)

    assert context.relevant_error_groups == report.error_groups[:10]
    assert context.component_summary == report.component_analysis.components[:10]


# ---- QAEngine.answer / investigate with a fake LLM client ----


def test_answer_returns_graceful_result_when_no_report_loaded():
    engine = QAEngine(llm_client=_FakeLLMClient(VALID_QA_RESPONSE), retriever=_FakeRetriever())

    result = engine.answer("What happened?")

    assert result.success is False
    assert "no log analysis data" in result.error.lower()


def test_answer_full_pipeline_with_fake_llm(make_entry, make_report):
    entries = [make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)
    fake_llm = _FakeLLMClient(VALID_QA_RESPONSE)
    engine = QAEngine(llm_client=fake_llm, retriever=_FakeRetriever())

    result = engine.answer("Which service generated the most errors?", report=report, entries=entries)

    assert result.success is True
    assert result.answer.question == "Which service generated the most errors?"
    assert len(fake_llm.calls) == 1
    combined = " ".join(m["content"] for m in fake_llm.calls[0])
    assert "CURRENT LOG EVIDENCE" in combined
    assert "HISTORICAL INCIDENTS" in combined


def test_answer_handles_ollama_unavailable_gracefully(make_entry, make_report):
    entries = [make_entry()]
    report = make_report(entries)
    engine = QAEngine(
        llm_client=_FailingLLMClient(OllamaUnavailableError("server down")), retriever=_FakeRetriever()
    )

    result = engine.answer("What happened?", report=report, entries=entries)

    assert result.success is False
    assert "server down" in result.error


def test_investigate_full_pipeline_with_fake_llm(make_entry, make_report):
    entries = [make_entry(severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)
    fake_llm = _FakeLLMClient(VALID_INVESTIGATION_RESPONSE)
    engine = QAEngine(llm_client=fake_llm, retriever=_FakeRetriever())

    result = engine.investigate(report)

    assert result.success is True
    assert result.investigation.executive_summary == "summary"


def test_investigate_rejects_bare_field_name_evidence(make_entry, make_report):
    # Regression test for a real failure mode observed from a weaker local
    # model: schema-valid JSON where an evidence item is just the name of a
    # CURRENT LOG EVIDENCE section/field instead of an actual fact.
    entries = [make_entry(severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)
    bad_response = json.loads(VALID_INVESTIGATION_RESPONSE)
    bad_response["supporting_evidence"] = ["top_recurring_messages"]
    fake_llm = _FakeLLMClient(json.dumps(bad_response))
    engine = QAEngine(llm_client=fake_llm, retriever=_FakeRetriever())

    result = engine.investigate(report)

    assert result.success is False
    assert result.investigation is None
    assert "field-name" in result.error


def test_investigate_rejects_high_confidence_with_insufficient_evidence(make_entry, make_report):
    # Regression test for a real failure mode: the model reported
    # confidence_level="high" while also flagging evidence_sufficient=False
    # -- an internally contradictory response.
    entries = [make_entry(severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)
    bad_response = json.loads(VALID_INVESTIGATION_RESPONSE)
    bad_response["confidence_level"] = "high"
    bad_response["evidence_sufficient"] = False
    fake_llm = _FakeLLMClient(json.dumps(bad_response))
    engine = QAEngine(llm_client=fake_llm, retriever=_FakeRetriever())

    result = engine.investigate(report)

    assert result.success is False
    assert result.investigation is None
    assert "contradictory" in result.error


# ---- async variants ----


def test_aanswer_full_pipeline_with_fake_llm(make_entry, make_report):
    entries = [make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)
    fake_llm = _FakeLLMClient(VALID_QA_RESPONSE)
    engine = QAEngine(llm_client=fake_llm, retriever=_FakeRetriever())

    result = asyncio.run(engine.aanswer("Which service generated the most errors?", report=report, entries=entries))

    assert result.success is True


def test_ainvestigate_full_pipeline_with_fake_llm(make_entry, make_report):
    entries = [make_entry(severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)
    fake_llm = _FakeLLMClient(VALID_INVESTIGATION_RESPONSE)
    engine = QAEngine(llm_client=fake_llm, retriever=_FakeRetriever())

    result = asyncio.run(engine.ainvestigate(report))

    assert result.success is True


# ---- live smoke test (skips gracefully if Ollama isn't reachable) ----


def _ollama_reachable() -> bool:
    try:
        httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2)
        return True
    except httpx.HTTPError:
        return False


@pytest.mark.skipif(not _ollama_reachable(), reason="Ollama server not reachable at settings.ollama_base_url")
def test_live_qa_engine_answer_end_to_end(make_entry, make_report, tmp_path):
    entries = [
        make_entry(
            timestamp=t(0),
            severity=LogSeverity.ERROR,
            message="PostgreSQL error: deadlock detected",
            service="payment-service",
        )
    ]
    report = make_report(entries)

    store = FaissVectorStore(index_path=tmp_path / "live_qa_test.index")
    store.build_index(KnowledgeBaseLoader().load())
    retriever = IncidentRetriever(store)
    llm = OllamaClient(model="llama3.2:3b", fallback_models="llama3.1,mistral", timeout_seconds=90, max_retries=2)
    engine = QAEngine(llm_client=llm, retriever=retriever)

    result = engine.answer("Show PostgreSQL errors.", report=report, entries=entries)

    assert result.success is True
    assert result.answer.confidence_level is not None
