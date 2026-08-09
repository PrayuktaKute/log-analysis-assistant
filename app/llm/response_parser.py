"""Parse raw Ollama text responses into structured pydantic models.

Ollama calls are made with `format="json"` (see `app.llm.qa_engine`), which
constrains the model to emit syntactically valid JSON -- but "valid JSON"
doesn't guarantee it matches our schema (missing fields, wrong types, or
occasionally prose/a markdown fence despite the instruction not to). This
module never lets a malformed response propagate as an exception: every
parse path returns a `*ParseResult` wrapper with `success: bool`, so a bad
LLM response degrades to a visible "parsing failed" state (with the raw
text preserved for debugging) instead of crashing the caller or silently
fabricating a plausible-looking empty report.
"""

import json
import re
from typing import Optional, TypeVar

from loguru import logger
from pydantic import BaseModel, ValidationError

from app.models.schemas import IncidentInvestigation, LLMParseResult, QAAnswer, QAParseResult

_JSON_FENCE_PATTERN = re.compile(r"```(?:json)?\s*(\{.*\})\s*```", re.DOTALL)
_JSON_OBJECT_PATTERN = re.compile(r"\{.*\}", re.DOTALL)

T = TypeVar("T", bound=BaseModel)


def _extract_json(raw_text: str) -> Optional[str]:
    """Best-effort extraction of a JSON object from raw LLM text: try the
    text as-is, then a ```json fenced block, then the largest {...} span
    in the text. Returns the first candidate that's syntactically valid
    JSON, or None if nothing in the text parses."""
    candidates = [raw_text.strip()]

    fence_match = _JSON_FENCE_PATTERN.search(raw_text)
    if fence_match:
        candidates.append(fence_match.group(1))

    object_match = _JSON_OBJECT_PATTERN.search(raw_text)
    if object_match:
        candidates.append(object_match.group(0))

    for candidate in candidates:
        try:
            json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            continue
    return None


def _parse_as(model_cls: type[T], raw_text: str) -> tuple[Optional[T], Optional[str]]:
    json_str = _extract_json(raw_text)
    if json_str is None:
        return None, "Response did not contain valid JSON"
    try:
        return model_cls.model_validate_json(json_str), None
    except ValidationError as exc:
        return None, f"JSON did not match the expected schema: {exc}"


class ResponseParser:
    """Parses raw Ollama responses into structured pydantic models."""

    def parse_investigation(self, raw_response: str) -> LLMParseResult:
        investigation, error = _parse_as(IncidentInvestigation, raw_response)
        if investigation is None:
            logger.warning("Failed to parse LLM investigation response: {}", error)
            return LLMParseResult(success=False, raw_response=raw_response, error=error)
        return LLMParseResult(success=True, investigation=investigation, raw_response=raw_response)

    def parse_qa_answer(self, raw_response: str, question: str) -> QAParseResult:
        answer, error = _parse_as(QAAnswer, raw_response)
        if answer is None:
            logger.warning("Failed to parse LLM QA response: {}", error)
            return QAParseResult(success=False, raw_response=raw_response, error=error)
        answer = answer.model_copy(update={"question": question})
        return QAParseResult(success=True, answer=answer, raw_response=raw_response)
