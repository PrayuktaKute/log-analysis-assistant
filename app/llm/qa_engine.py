"""Combines current log evidence, deterministic analysis results, and
retrieved historical incidents into LLM-generated structured output --
either a full incident investigation or an answer to a free-text question.

Pipeline for `answer()`/`aanswer()`:

    question -> relevant current logs & analysis results (deterministic,
    no LLM -- see `_select_relevant_context`) -> historical incident
    retrieval (`IncidentRetriever`) -> prompt (`PromptBuilder`) -> Ollama
    (`OllamaClient`) -> structured answer (`ResponseParser`)

See `app.llm.prompt_builder` for the evidence-separation rules enforced in
every prompt, and `app.llm.response_parser` for how malformed LLM output
is handled without ever raising to the caller.
"""

import re
from typing import Optional

import ollama
from loguru import logger

from app.analysis.message_catalog import categories_mentioned_in, categorize
from app.config import settings
from app.llm.ollama_client import OllamaClient, OllamaUnavailableError
from app.llm.prompt_builder import PromptBuilder, QAContext
from app.llm.response_parser import ResponseParser
from app.models.schemas import (
    ChatMessage,
    ConfidenceLevel,
    IncidentInvestigation,
    LLMParseResult,
    LogAnalysisReport,
    LogEntry,
    LogSeverity,
    QAParseResult,
)
from app.rag.retriever import IncidentRetriever

_LLM_FAILURE_EXCEPTIONS = (OllamaUnavailableError, ollama.ResponseError)

# Post-validation for investigate()/ainvestigate() (see prompt_builder.py
# system prompt rules 6-7): catches syntactically-valid-but-semantically-
# broken output from weaker local models, which schema validation alone
# can't catch.
_BARE_FIELD_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:_[a-z0-9]+)+$")

_KNOWN_EVIDENCE_FIELD_NAMES = {
    "top_recurring_messages",
    "top_failing_components",
    "affected_hosts",
    "affected_services",
    "affected_sources",
    "failure_patterns",
    "error_groups",
    "correlated_events",
    "component_health",
    "timeline",
    "statistics",
    "distinct_messages",
    "supporting_evidence",
    "structured_evidence",
    "total_logs",
    "error_count",
    "warning_count",
    "fatal_count",
    "failure_count",
    "error_rate",
    "top_failure_message",
    "occurrences",
    "first_seen",
    "last_seen",
    "health_status",
}


def _looks_like_bare_field_name(evidence_item: str) -> bool:
    """True if `evidence_item` is just a schema/field-name-shaped token
    (e.g. "top_recurring_messages") rather than an actual fact -- a failure
    mode observed from weaker local models, which sometimes echo a CURRENT
    LOG EVIDENCE section label instead of the values inside it."""
    token = evidence_item.strip().strip("'\"").strip()
    if not token:
        return False
    if token in _KNOWN_EVIDENCE_FIELD_NAMES:
        return True
    return bool(_BARE_FIELD_NAME_PATTERN.fullmatch(token))


def _investigation_validation_error(investigation: IncidentInvestigation) -> Optional[str]:
    """Lightweight semantic check beyond schema conformance. Returns an
    error message if `investigation` should be treated as invalid, else
    None. Two checks, matching prompt_builder.py's rules 6-7:

    1. Any supporting-evidence string (top-level or inside a root cause)
       that's just a bare field-name-shaped token rather than a real fact.
    2. confidence_level of 'high' while evidence_sufficient is False --
       an internally contradictory response.
    """
    all_evidence = list(investigation.supporting_evidence)
    for cause in investigation.possible_root_causes:
        all_evidence.extend(cause.supporting_evidence)

    bad_items = [item for item in all_evidence if _looks_like_bare_field_name(item)]
    if bad_items:
        return f"supporting_evidence contained bare field-name-like value(s), not real evidence: {bad_items!r}"

    if investigation.confidence_level == ConfidenceLevel.HIGH and not investigation.evidence_sufficient:
        return "confidence_level is 'high' but evidence_sufficient is False -- contradictory response"

    return None


def _select_relevant_context(
    question: str, report: LogAnalysisReport, entries: list[LogEntry], top_n: int
) -> QAContext:
    """Deterministically narrow the full analysis report + raw entries down
    to what's relevant to `question`, with no LLM call:

    - If the question mentions a known failure category (or a keyword that
      maps to one, e.g. "postgresql" -> "database") via
      `categories_mentioned_in`, filter error groups / failure patterns /
      non-INFO entries to that category. Otherwise fall back to the
      top-N items by the report's own ranking (count / severity / failure
      count), which already surface the most notable things.
    - If the question names a known component/service, filter correlated
      events and component health to those; otherwise use the top-N
      (components are already ranked by failure count).

    This directly supports questions like "Show PostgreSQL errors" or
    "Which service generated the most errors?" without needing the LLM to
    do retrieval itself.
    """
    category_matches = categories_mentioned_in(question)
    lowered_question = question.lower()
    component_names = {c.component for c in report.component_analysis.components}
    component_matches = {name for name in component_names if name.lower() in lowered_question}

    if category_matches:
        relevant_error_groups = [g for g in report.error_groups if g.category in category_matches][:top_n]
        relevant_failure_patterns = [
            p for p in report.failure_patterns if categorize(p.message) in category_matches
        ][:top_n]
        category_entries = [
            e for e in entries if e.severity != LogSeverity.INFO and categorize(e.message) in category_matches
        ]
        relevant_entries = sorted(category_entries, key=lambda e: e.timestamp, reverse=True)[:top_n]
    else:
        relevant_error_groups = report.error_groups[:top_n]
        relevant_failure_patterns = report.failure_patterns[:top_n]
        relevant_entries = report.severity_analysis.most_critical_events[:top_n]

    if component_matches:
        relevant_correlated_events = [
            e for e in report.correlated_events if set(e.involved_components) & component_matches
        ][:top_n]
        component_summary = [c for c in report.component_analysis.components if c.component in component_matches]
    else:
        relevant_correlated_events = report.correlated_events[:top_n]
        component_summary = report.component_analysis.components[:top_n]

    return QAContext(
        relevant_entries=relevant_entries,
        relevant_error_groups=relevant_error_groups,
        relevant_failure_patterns=relevant_failure_patterns,
        relevant_correlated_events=relevant_correlated_events,
        component_summary=component_summary,
        statistics=report.statistics,
    )


def _investigation_query(report: LogAnalysisReport, top_n: int) -> str:
    """Build a retrieval query representative of the whole incident, from
    the most prominent failure patterns and correlated-event triggers."""
    parts = [p.message for p in report.failure_patterns[:top_n]]
    parts += [e.probable_trigger.message for e in report.correlated_events[:top_n] if e.probable_trigger]
    if not parts:
        return "No significant failures detected"
    return "; ".join(dict.fromkeys(parts))  # de-duplicate, preserve order


class QAEngine:
    """Answers natural-language questions and generates structured incident
    investigations, grounded in current log evidence + retrieved history."""

    def __init__(
        self,
        llm_client: OllamaClient,
        retriever: IncidentRetriever,
        prompt_builder: Optional[PromptBuilder] = None,
        response_parser: Optional[ResponseParser] = None,
        top_n: int = settings.llm_prompt_max_items_per_section,
    ):
        self.llm_client = llm_client
        self.retriever = retriever
        self.prompt_builder = prompt_builder or PromptBuilder()
        self.response_parser = response_parser or ResponseParser()
        self.top_n = top_n

    # ---- Incident investigation ----

    def investigate(self, report: LogAnalysisReport) -> LLMParseResult:
        """Generate a full structured investigation of the given report."""
        messages = self._prepare_investigation(report)
        try:
            raw = self.llm_client.chat(messages, format="json")
        except _LLM_FAILURE_EXCEPTIONS as exc:
            logger.error("Investigation LLM call failed: {}", exc)
            return LLMParseResult(success=False, raw_response="", error=str(exc))
        return self._validate_investigation_result(self.response_parser.parse_investigation(raw))

    async def ainvestigate(self, report: LogAnalysisReport) -> LLMParseResult:
        """Async counterpart of `investigate`."""
        messages = self._prepare_investigation(report)
        try:
            raw = await self.llm_client.achat(messages, format="json")
        except _LLM_FAILURE_EXCEPTIONS as exc:
            logger.error("Investigation LLM call failed: {}", exc)
            return LLMParseResult(success=False, raw_response="", error=str(exc))
        return self._validate_investigation_result(self.response_parser.parse_investigation(raw))

    @staticmethod
    def _validate_investigation_result(result: LLMParseResult) -> LLMParseResult:
        """Run `_investigation_validation_error` on a successfully-parsed
        result, downgrading it to `success=False` if it fails -- so a
        schema-valid-but-semantically-broken response degrades exactly like
        an LLM failure (callers, e.g. `LogAnalysisPipeline._investigate_incident`,
        already fall back to `investigation=None` for `success=False`)."""
        if not result.success or result.investigation is None:
            return result
        error = _investigation_validation_error(result.investigation)
        if error is None:
            return result
        logger.warning("Discarding LLM investigation that failed post-validation: {}", error)
        return LLMParseResult(success=False, investigation=None, raw_response=result.raw_response, error=error)

    def _prepare_investigation(self, report: LogAnalysisReport) -> list[dict[str, str]]:
        query = _investigation_query(report, self.top_n)
        retrieved = self.retriever.retrieve_for_query(query, top_k=settings.rag_top_k)
        return self.prompt_builder.build_investigation_prompt(report, retrieved)

    # ---- Question answering ----

    def answer(
        self,
        question: str,
        report: Optional[LogAnalysisReport] = None,
        entries: Optional[list[LogEntry]] = None,
        history: Optional[list[ChatMessage]] = None,
    ) -> QAParseResult:
        """Answer a natural-language question, grounded in `report`/`entries`.

        Returns a graceful `success=False` result (no LLM call made) if no
        analysis data has been loaded yet, rather than raising.
        """
        prepared = self._prepare_qa(question, report, entries, history)
        if isinstance(prepared, QAParseResult):
            return prepared
        messages = prepared

        try:
            raw = self.llm_client.chat(messages, format="json")
        except _LLM_FAILURE_EXCEPTIONS as exc:
            logger.error("QA LLM call failed: {}", exc)
            return QAParseResult(success=False, raw_response="", error=str(exc))

        return self.response_parser.parse_qa_answer(raw, question)

    async def aanswer(
        self,
        question: str,
        report: Optional[LogAnalysisReport] = None,
        entries: Optional[list[LogEntry]] = None,
        history: Optional[list[ChatMessage]] = None,
    ) -> QAParseResult:
        """Async counterpart of `answer`."""
        prepared = self._prepare_qa(question, report, entries, history)
        if isinstance(prepared, QAParseResult):
            return prepared
        messages = prepared

        try:
            raw = await self.llm_client.achat(messages, format="json")
        except _LLM_FAILURE_EXCEPTIONS as exc:
            logger.error("QA LLM call failed: {}", exc)
            return QAParseResult(success=False, raw_response="", error=str(exc))

        return self.response_parser.parse_qa_answer(raw, question)

    def _prepare_qa(
        self,
        question: str,
        report: Optional[LogAnalysisReport],
        entries: Optional[list[LogEntry]],
        history: Optional[list[ChatMessage]],
    ):
        if report is None or entries is None:
            return QAParseResult(
                success=False,
                raw_response="",
                error="No log analysis data loaded yet -- run the analysis pipeline before asking questions.",
            )

        context = _select_relevant_context(question, report, entries, self.top_n)
        context.retrieved_incidents = self.retriever.retrieve_for_query(question, top_k=settings.rag_top_k)
        return self.prompt_builder.build_qa_prompt(question, context, history=history)
