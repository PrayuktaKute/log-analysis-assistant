"""Tests for app.llm.response_parser (pure parsing, no LLM call)."""

import json

from app.llm.response_parser import ResponseParser

VALID_QA_JSON = json.dumps(
    {
        "answer": "The database service failed due to deadlocks.",
        "current_log_evidence": ["- ERROR PostgreSQL deadlock detected"],
        "historical_incidents": [
            {"incident_id": "inc-001", "title": "Deadlocks", "similarity_score": 0.9, "relevance_explanation": "similar"}
        ],
        "ai_reasoning": "The pattern matches a known deadlock signature.",
        "recommendations": ["Add retry logic"],
        "confidence_level": "high",
        "evidence_sufficient": True,
    }
)

VALID_INVESTIGATION_JSON = json.dumps(
    {
        "executive_summary": "Database issues caused order failures.",
        "incident_summary": "Repeated PostgreSQL deadlocks.",
        "possible_root_causes": [
            {"description": "Long transactions", "likelihood": "high", "supporting_evidence": ["evidence 1"]}
        ],
        "supporting_evidence": ["evidence 1"],
        "similar_historical_incidents": [
            {"incident_id": "inc-001", "title": "Deadlocks", "similarity_score": 0.9, "relevance_explanation": "similar"}
        ],
        "recommended_actions": ["Reduce transaction scope"],
        "confidence_level": "medium",
        "open_questions": [],
        "evidence_sufficient": True,
    }
)


# ---- QA parsing ----


def test_parse_qa_answer_valid_json():
    result = ResponseParser().parse_qa_answer(VALID_QA_JSON, "What caused it?")

    assert result.success is True
    assert result.error is None
    assert result.answer.question == "What caused it?"
    assert result.answer.confidence_level.value == "high"
    assert result.answer.historical_incidents[0].incident_id == "inc-001"


def test_parse_qa_answer_json_wrapped_in_markdown_fence():
    fenced = f"Here is the answer:\n```json\n{VALID_QA_JSON}\n```"

    result = ResponseParser().parse_qa_answer(fenced, "Q")

    assert result.success is True
    assert result.answer.answer.startswith("The database")


def test_parse_qa_answer_json_with_surrounding_prose():
    noisy = f"Sure, I can help with that! {VALID_QA_JSON} Let me know if you need more."

    result = ResponseParser().parse_qa_answer(noisy, "Q")

    assert result.success is True


def test_parse_qa_answer_completely_malformed_never_raises():
    result = ResponseParser().parse_qa_answer("I'm not able to comply with that request.", "Q")

    assert result.success is False
    assert result.answer is None
    assert result.error is not None
    assert result.raw_response == "I'm not able to comply with that request."


def test_parse_qa_answer_valid_json_wrong_schema():
    result = ResponseParser().parse_qa_answer('{"unexpected": "shape"}', "Q")

    assert result.success is False
    assert "schema" in result.error.lower()


def test_parse_qa_answer_empty_string():
    result = ResponseParser().parse_qa_answer("", "Q")

    assert result.success is False


# ---- Investigation parsing ----


def test_parse_investigation_valid_json():
    result = ResponseParser().parse_investigation(VALID_INVESTIGATION_JSON)

    assert result.success is True
    assert result.investigation.confidence_level.value == "medium"
    assert result.investigation.possible_root_causes[0].likelihood.value == "high"
    assert result.investigation.similar_historical_incidents[0].incident_id == "inc-001"


def test_parse_investigation_malformed_never_raises():
    result = ResponseParser().parse_investigation("not json at all")

    assert result.success is False
    assert result.investigation is None
    assert result.raw_response == "not json at all"
