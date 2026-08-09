"""Tests for app.reporting.report_generator -- rendering Incidents (with and
without an attached LLM investigation) to Markdown, and the batched
"minor incidents" appendix."""

from datetime import datetime, timezone

from app.models.schemas import (
    ConfidenceLevel,
    FailurePattern,
    Incident,
    IncidentInvestigation,
    LogSeverity,
    RootCauseHypothesis,
)
from app.reporting.report_generator import ReportGenerator


def _make_pattern(**overrides) -> FailurePattern:
    defaults = dict(
        pattern_id="pattern-test",
        description="'Something broke' recurred 5 time(s)",
        message="Something broke",
        occurrences=5,
        first_seen=datetime(2026, 8, 1, 9, 0, tzinfo=timezone.utc),
        last_seen=datetime(2026, 8, 1, 9, 5, tzinfo=timezone.utc),
        affected_sources=["application"],
        affected_services=["api-gateway"],
        affected_hosts=["wilston-prod-01"],
        sample_events=[],
    )
    defaults.update(overrides)
    return FailurePattern(**defaults)


def test_report_generator_loads_template(tmp_path):
    generator = ReportGenerator(output_dir=tmp_path)
    assert generator.template is not None
    assert generator.appendix_template is not None


def test_generate_without_investigation_renders_deterministic_fallbacks(tmp_path, make_entry, make_correlated_event):
    entries = [make_entry(severity=LogSeverity.ERROR, message="Something broke")]
    event = make_correlated_event(related_events=entries, confidence_score=0.3)
    incident = Incident(
        incident_id="incident-corr-test",
        title="Something broke",
        severity=LogSeverity.ERROR,
        correlated_events=[event],
        failure_patterns=[_make_pattern()],
        investigation=None,
    )

    generator = ReportGenerator(output_dir=tmp_path)
    report = generator.generate(incident)

    assert report.file_path is not None
    on_disk = (tmp_path / f"{incident.incident_id}.md").read_text(encoding="utf-8")
    assert on_disk == report.markdown_content

    for heading in [
        "## Executive Summary",
        "## Incident Summary",
        "## Major Issues Detected",
        "## Timeline of Important Events",
        "## Root Cause Analysis",
        "## Supporting Evidence",
        "## Similar Historical Incidents",
        "## Recommended Fixes",
        "## Confidence Level",
    ]:
        assert heading in report.markdown_content

    assert "No AI-generated executive summary is available" in report.markdown_content
    assert "No AI-generated root cause analysis is available" in report.markdown_content
    assert "Not assessed by the LLM" in report.markdown_content
    assert "Something broke" in report.markdown_content


def test_generate_with_investigation_renders_llm_sections(tmp_path, make_entry, make_correlated_event):
    entries = [make_entry(severity=LogSeverity.CRITICAL, message="Database connection pool exhausted")]
    event = make_correlated_event(related_events=entries, confidence_score=0.8)
    investigation = IncidentInvestigation(
        executive_summary="The database connection pool was exhausted under load.",
        incident_summary="Repeated pool-exhaustion errors on api-gateway.",
        possible_root_causes=[
            RootCauseHypothesis(
                description="Connection leak in the order service",
                likelihood=ConfidenceLevel.HIGH,
                supporting_evidence=["Pool exhaustion errors correlate with order-service deploys"],
            )
        ],
        supporting_evidence=["5 pool-exhaustion errors within 2 minutes on wilston-prod-01"],
        recommended_actions=["Add connection pool monitoring", "Audit order-service for unclosed connections"],
        confidence_level=ConfidenceLevel.HIGH,
        ai_reasoning="Concluded from the tight time clustering of errors on a single host/service pair.",
        evidence_sufficient=True,
    )
    incident = Incident(
        incident_id="incident-corr-test-2",
        title="Database connection pool exhausted",
        severity=LogSeverity.CRITICAL,
        correlated_events=[event],
        failure_patterns=[],
        investigation=investigation,
    )

    generator = ReportGenerator(output_dir=tmp_path)
    report = generator.generate(incident)

    assert "The database connection pool was exhausted under load." in report.markdown_content
    assert "Connection leak in the order service" in report.markdown_content
    assert "Add connection pool monitoring" in report.markdown_content
    assert "Concluded from the tight time clustering" in report.markdown_content
    assert "**high**" in report.markdown_content

    on_disk = (tmp_path / f"{incident.incident_id}.md").read_text(encoding="utf-8")
    assert on_disk == report.markdown_content


def test_generate_appendix_summarizes_minor_incidents(tmp_path, make_entry, make_correlated_event):
    low_confidence_event = make_correlated_event(
        related_events=[make_entry(severity=LogSeverity.WARNING, message="Slow response detected")],
        confidence_score=0.3,
    )
    event_incident = Incident(
        incident_id="incident-corr-minor",
        title="Slow response detected",
        severity=LogSeverity.WARNING,
        correlated_events=[low_confidence_event],
        failure_patterns=[],
    )
    pattern_incident = Incident(
        incident_id="incident-pattern-minor",
        title="'Something broke' recurred 5 time(s)",
        severity=LogSeverity.ERROR,
        correlated_events=[],
        failure_patterns=[_make_pattern()],
    )

    generator = ReportGenerator(output_dir=tmp_path)
    report = generator.generate_appendix([event_incident, pattern_incident])

    assert report.incident_id == "appendix-minor-incidents"
    assert report.file_path is not None
    on_disk = (tmp_path / "appendix-minor-incidents.md").read_text(encoding="utf-8")
    assert on_disk == report.markdown_content

    assert "incident-corr-minor" in report.markdown_content
    assert "incident-pattern-minor" in report.markdown_content
    assert "0.30" in report.markdown_content
    assert "Something broke" in report.markdown_content
