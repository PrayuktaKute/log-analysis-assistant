"""Tests for app.llm.prompt_builder (pure string construction, no LLM call)."""

from datetime import datetime, timedelta, timezone

from app.llm.prompt_builder import PromptBuilder, QAContext
from app.models.schemas import ChatMessage, HistoricalIncident, LogSeverity, RetrievedIncident

BASE = datetime(2026, 8, 1, 9, 0, 0, tzinfo=timezone.utc)


def t(seconds: float) -> datetime:
    return BASE + timedelta(seconds=seconds)


def _retrieved_incident(incident_id="inc-001", score=0.9):
    return RetrievedIncident(
        incident=HistoricalIncident(
            incident_id=incident_id,
            title="Some past incident",
            summary="A summary.",
            root_cause="Some cause.",
            resolution="Some fix.",
        ),
        similarity_score=score,
    )


# ---- Investigation prompt ----


def test_investigation_prompt_has_system_and_user_messages(make_entry, make_report):
    entries = [make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="boom")]
    report = make_report(entries)

    messages = PromptBuilder().build_investigation_prompt(report, [])

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"


def test_investigation_prompt_separates_current_evidence_and_history(make_entry, make_report):
    entries = [make_entry(timestamp=t(0), severity=LogSeverity.ERROR, message="Kafka publish failed")]
    report = make_report(entries)
    retrieved = [_retrieved_incident("inc-042")]

    messages = PromptBuilder().build_investigation_prompt(report, retrieved)
    user_content = messages[1]["content"]

    assert "=== CURRENT LOG EVIDENCE ===" in user_content
    assert "=== HISTORICAL INCIDENTS" in user_content
    assert "NOT part of the current incident" in user_content
    assert "Kafka publish failed" in user_content
    assert "inc-042" in user_content
    # historical incident content appears strictly after the historical marker,
    # not intermixed into the current-evidence section
    assert user_content.index("=== HISTORICAL INCIDENTS") > user_content.index("Kafka publish failed")


def test_investigation_prompt_system_message_states_hallucination_rules(make_report):
    report = make_report([])
    messages = PromptBuilder().build_investigation_prompt(report, [])

    system_content = messages[0]["content"]
    assert "NEVER" in system_content or "never" in system_content
    assert "historical" in system_content.lower()


def test_investigation_prompt_includes_json_schema_fields(make_entry, make_report):
    report = make_report([make_entry()])
    messages = PromptBuilder().build_investigation_prompt(report, [])
    user_content = messages[1]["content"]

    for field in [
        "executive_summary",
        "incident_summary",
        "possible_root_causes",
        "supporting_evidence",
        "similar_historical_incidents",
        "recommended_actions",
        "confidence_level",
        "open_questions",
        "evidence_sufficient",
    ]:
        assert field in user_content


def test_investigation_prompt_truncates_large_sections(make_entry, make_report):
    # Distinct, digit-free messages -- ErrorGrouper normalizes embedded
    # digits by default, which would collapse "error-0".."error-29" into a
    # single "error-<NUM>" group and defeat this test's premise.
    import string

    entries = [
        make_entry(timestamp=t(i), severity=LogSeverity.ERROR, message=f"failure-mode-{letter}")
        for i, letter in enumerate(string.ascii_lowercase)
    ]
    report = make_report(entries)

    messages = PromptBuilder(max_items_per_section=5).build_investigation_prompt(report, [])
    user_content = messages[1]["content"]

    assert "more error group(s) not shown" in user_content


# ---- QA prompt ----


def test_qa_prompt_includes_question_and_schema(make_report):
    report = make_report([])
    context = QAContext(
        relevant_entries=[],
        relevant_error_groups=[],
        relevant_failure_patterns=[],
        relevant_correlated_events=[],
        component_summary=[],
        statistics=report.statistics,
    )

    messages = PromptBuilder().build_qa_prompt("What caused the incident?", context)

    user_content = messages[-1]["content"]
    assert "What caused the incident?" in user_content
    assert '"answer"' in user_content
    assert '"current_log_evidence"' in user_content


def test_qa_prompt_includes_chat_history_in_order(make_report):
    report = make_report([])
    context = QAContext(
        relevant_entries=[],
        relevant_error_groups=[],
        relevant_failure_patterns=[],
        relevant_correlated_events=[],
        component_summary=[],
        statistics=report.statistics,
    )
    history = [
        ChatMessage(role="user", content="First question"),
        ChatMessage(role="assistant", content="First answer"),
    ]

    messages = PromptBuilder().build_qa_prompt("Second question", context, history=history)

    # system, then history (user, assistant), then the new user turn
    assert messages[0]["role"] == "system"
    assert messages[1] == {"role": "user", "content": "First question"}
    assert messages[2] == {"role": "assistant", "content": "First answer"}
    assert messages[3]["role"] == "user"
    assert "Second question" in messages[3]["content"]
