"""Shared pytest fixtures."""

import itertools
from datetime import datetime, timezone

import pytest

from app.models.schemas import CorrelatedEvent, CorrelationEvidence, LogEntry, LogSeverity

_line_counter = itertools.count(1)


@pytest.fixture
def make_entry():
    """Factory fixture for building a LogEntry with sensible defaults,
    overriding only the fields a test cares about."""

    def _make(**overrides) -> LogEntry:
        # Mirror LogParser's real behavior: component always tracks service
        # unless the caller explicitly overrides component too.
        if "service" in overrides and "component" not in overrides:
            overrides = {**overrides, "component": overrides["service"]}

        defaults = dict(
            timestamp=datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc),
            severity=LogSeverity.INFO,
            message="Test message",
            source="application",
            source_file="test.log",
            line_number=next(_line_counter),
            service="api-gateway",
            component="api-gateway",
            host="wilston-prod-01",
            raw_line="raw",
        )
        defaults.update(overrides)
        return LogEntry(**defaults)

    return _make


@pytest.fixture
def make_correlated_event():
    """Factory fixture for building a CorrelatedEvent with a minimal but
    valid `structured_evidence`, overriding only what a test cares about."""

    def _make(**overrides) -> CorrelatedEvent:
        related_events = overrides.get("related_events", [])
        defaults = dict(
            correlation_id="corr-test",
            start_time=related_events[0].timestamp if related_events else None,
            end_time=related_events[-1].timestamp if related_events else None,
            involved_components=sorted({e.component for e in related_events}),
            involved_hosts=sorted({e.host for e in related_events}),
            related_events=related_events,
            probable_trigger=related_events[0] if related_events else None,
            confidence_score=0.5,
            supporting_evidence=[],
            structured_evidence=CorrelationEvidence(
                cluster_size=len(related_events),
                time_span_seconds=0.0,
                involved_hosts_count=len({e.host for e in related_events}),
                involved_components_count=len({e.component for e in related_events}),
            ),
        )
        defaults.update(overrides)
        return CorrelatedEvent(**defaults)

    return _make


@pytest.fixture
def make_report():
    """Factory fixture that runs a list of LogEntry through the real
    LogAnalyzer, returning a genuine LogAnalysisReport -- avoids hand
    -constructing deeply nested pydantic objects in LLM-layer tests."""

    def _make(entries: list[LogEntry]):
        from app.analysis.log_analyzer import LogAnalyzer

        return LogAnalyzer().analyze(entries)

    return _make
