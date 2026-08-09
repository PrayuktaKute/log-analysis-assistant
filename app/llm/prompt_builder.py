"""Builds chat-message prompts for incident investigation and Q&A that
clearly separate three kinds of content:

1. CURRENT LOG EVIDENCE -- deterministic facts about the incident being
   investigated right now (error groups, failure patterns, correlated
   events, statistics, component health, timeline), produced by
   `app.analysis`/`app.correlation`, never by the LLM.
2. HISTORICAL INCIDENTS -- unrelated past incidents retrieved by
   similarity search (`app.rag.retriever`). Explicitly labeled as NOT part
   of the current incident.
3. Instructions to the LLM, including a strict rule against presenting
   historical-incident content as current fact, and the exact JSON schema
   the response must match (parsed by `app.llm.response_parser`).

Every section is length-capped (`max_items_per_section`) with an explicit
"N more not shown" note when truncated, so the model never mistakes a
partial evidence dump for a complete one.
"""

from dataclasses import dataclass, field
from typing import Optional

from app.config import settings
from app.models.schemas import (
    ChatMessage,
    ComponentHealth,
    CorrelatedEvent,
    ErrorGroup,
    FailurePattern,
    LogAnalysisReport,
    LogEntry,
    LogStatistics,
    RetrievedIncident,
    TimelineEvent,
)

_SYSTEM_PROMPT = """You are an incident investigation assistant for a production log analysis system.

You will be given information under clearly labeled headings. Follow these rules strictly:

1. "CURRENT LOG EVIDENCE" contains facts deterministically extracted from the logs being investigated right now (error groups, failure patterns, correlated events, statistics, component health, timeline). Treat everything in this section as ground truth about the CURRENT incident, and ONLY this section.

2. "HISTORICAL INCIDENTS" contains past, separate incidents retrieved by similarity search from a knowledge base. They are NOT part of the current incident. You may cite them as precedent, but you must ALWAYS attribute their content explicitly (e.g. "a similar historical incident (inc-004) was caused by X") and NEVER state their details as if they are facts about what is happening now.

3. Everything else you produce is your own reasoning, drawn only from the sections above. Do not invent services, hosts, error messages, timestamps, or counts that are not present in CURRENT LOG EVIDENCE. Do not invent historical incidents beyond those listed in HISTORICAL INCIDENTS.

4. If CURRENT LOG EVIDENCE is insufficient to answer confidently, say so explicitly (use the open_questions / evidence_sufficient fields) and lower your confidence_level -- do not guess and present a guess as settled fact.

5. Respond with ONLY a single JSON object matching the schema given at the end of the user message. No prose before or after it, no markdown code fences.

6. Every evidence item you write (supporting_evidence, current_log_evidence, or evidence inside a root cause) MUST be a concrete fact, quote, count, or value taken from CURRENT LOG EVIDENCE -- for example "391 occurrences of 'Unhandled exception in order processing' on order-service". NEVER write the bare name of a field, key, or section heading from CURRENT LOG EVIDENCE as if it were an evidence item (e.g. do NOT write "top_recurring_messages" or "affected_hosts" -- write out the actual messages/hosts/numbers those sections contain instead).

7. Before finalizing your answer, check that confidence_level is consistent with evidence_sufficient and the amount of concrete evidence you cited: if evidence_sufficient is false, or you have fewer than two independent, concrete pieces of supporting evidence, confidence_level must be "low" or "medium" -- never "high".
"""

_INVESTIGATION_SCHEMA = """Respond with a JSON object with exactly these fields:
{
  "executive_summary": string,
  "incident_summary": string,
  "possible_root_causes": [
    {"description": string, "likelihood": "low"|"medium"|"high", "supporting_evidence": [string, ...]}
  ],
  "supporting_evidence": [string, ...],
  "similar_historical_incidents": [
    {"incident_id": string, "title": string, "similarity_score": number|null, "relevance_explanation": string}
  ],
  "recommended_actions": [string, ...],
  "confidence_level": "low"|"medium"|"high",
  "ai_reasoning": string,
  "open_questions": [string, ...],
  "evidence_sufficient": true|false
}"""

_QA_SCHEMA = """Respond with a JSON object with exactly these fields:
{
  "answer": string,
  "current_log_evidence": [string, ...],
  "historical_incidents": [
    {"incident_id": string, "title": string, "similarity_score": number|null, "relevance_explanation": string}
  ],
  "ai_reasoning": string,
  "recommendations": [string, ...],
  "confidence_level": "low"|"medium"|"high",
  "evidence_sufficient": true|false
}"""


@dataclass
class QAContext:
    """Deterministically-selected subset of the current LogAnalysisReport +
    raw entries judged relevant to a specific question (see
    `app.llm.qa_engine._select_relevant_context`), plus retrieved
    historical incidents. This is the shape `build_qa_prompt` expects."""

    relevant_entries: list[LogEntry]
    relevant_error_groups: list[ErrorGroup]
    relevant_failure_patterns: list[FailurePattern]
    relevant_correlated_events: list[CorrelatedEvent]
    component_summary: list[ComponentHealth]
    statistics: LogStatistics
    retrieved_incidents: list[RetrievedIncident] = field(default_factory=list)


def _truncate(items: list, max_items: int) -> tuple[list, int]:
    if len(items) <= max_items:
        return items, 0
    return items[:max_items], len(items) - max_items


def _format_statistics(stats: LogStatistics) -> str:
    return (
        f"- total_logs={stats.total_logs}, errors={stats.error_count}, warnings={stats.warning_count}, "
        f"fatals={stats.fatal_count}\n"
        f"- affected_hosts={stats.affected_hosts}\n"
        f"- affected_services={stats.affected_services}\n"
        f"- top_recurring_messages={[(m.message, m.count) for m in stats.top_recurring_messages]}\n"
        f"- top_failing_components={[(c.component, c.failure_count) for c in stats.top_failing_components]}"
    )


def _format_component_health(components: list[ComponentHealth], max_items: int) -> str:
    shown, omitted = _truncate(components, max_items)
    if not shown:
        return "(none)"
    lines = [
        f"- {c.component}: status={c.health_status}, failure_count={c.failure_count}, "
        f"error_rate={c.error_rate}, top_failure_message={c.top_failure_message!r}"
        for c in shown
    ]
    if omitted:
        lines.append(f"... ({omitted} more component(s) not shown)")
    return "\n".join(lines)


def _format_error_groups(groups: list[ErrorGroup], max_items: int) -> str:
    shown, omitted = _truncate(groups, max_items)
    if not shown:
        return "(none)"
    lines = [
        f"- [{g.category}] \"{g.message}\" -- count={g.count}, dominant_severity={g.dominant_severity.value}, "
        f"first_seen={g.first_seen.isoformat()}, last_seen={g.last_seen.isoformat()}, "
        f"services={g.affected_services}, hosts={g.affected_hosts}"
        for g in shown
    ]
    if omitted:
        lines.append(f"... ({omitted} more error group(s) not shown)")
    return "\n".join(lines)


def _format_failure_patterns(patterns: list[FailurePattern], max_items: int) -> str:
    shown, omitted = _truncate(patterns, max_items)
    if not shown:
        return "(none)"
    lines = []
    for p in shown:
        burst_note = (
            f", BURST: {p.peak_window_count} occurrences in one window starting "
            f"{p.peak_window_start.isoformat() if p.peak_window_start else '?'}"
            if p.is_burst
            else ""
        )
        lines.append(
            f"- \"{p.message}\" -- occurrences={p.occurrences}, first_seen={p.first_seen.isoformat()}, "
            f"last_seen={p.last_seen.isoformat()}, services={p.affected_services}, hosts={p.affected_hosts}{burst_note}"
        )
    if omitted:
        lines.append(f"... ({omitted} more failure pattern(s) not shown)")
    return "\n".join(lines)


def _format_correlated_events(events: list[CorrelatedEvent], max_items: int) -> str:
    shown, omitted = _truncate(events, max_items)
    if not shown:
        return "(none)"
    lines = []
    for e in shown:
        trigger = e.probable_trigger.message if e.probable_trigger else "(none)"
        lines.append(
            f"- {e.correlation_id}: confidence={e.confidence_score}, window={e.start_time.isoformat()} -> "
            f"{e.end_time.isoformat()}, components={e.involved_components}, hosts={e.involved_hosts}, "
            f"probable_trigger=\"{trigger}\""
        )
    if omitted:
        lines.append(f"... ({omitted} more correlated event(s) not shown)")
    return "\n".join(lines)


def _format_timeline(events: list[TimelineEvent], max_items: int) -> str:
    shown, omitted = _truncate(events, max_items)
    if not shown:
        return "(none)"
    lines = [f"- {e.timestamp.isoformat()} [{e.event_type.value}] {e.title}: {e.description}" for e in shown]
    if omitted:
        lines.append(f"... ({omitted} more timeline event(s) not shown)")
    return "\n".join(lines)


def _format_log_entries(entries: list[LogEntry], max_items: int) -> str:
    shown, omitted = _truncate(entries, max_items)
    if not shown:
        return "(none)"
    lines = [
        f"- {e.timestamp.isoformat()} [{e.severity.value}] {e.service}@{e.host}: {e.message}" for e in shown
    ]
    if omitted:
        lines.append(f"... ({omitted} more log entries not shown)")
    return "\n".join(lines)


def _format_historical_incidents(incidents: list[RetrievedIncident], max_items: int) -> str:
    shown, omitted = _truncate(incidents, max_items)
    if not shown:
        return "(none retrieved)"
    lines = [
        f"- {r.incident.incident_id} (similarity={r.similarity_score:.3f}): \"{r.incident.title}\" -- "
        f"{r.incident.summary} root_cause={r.incident.root_cause!r} resolution={r.incident.resolution!r} "
        f"tags={r.incident.tags}"
        for r in shown
    ]
    if omitted:
        lines.append(f"... ({omitted} more historical incident(s) not shown)")
    return "\n".join(lines)


class PromptBuilder:
    """Builds chat-message prompts that clearly separate current log
    evidence, retrieved historical incidents, and instructions."""

    def __init__(self, max_items_per_section: int = settings.llm_prompt_max_items_per_section):
        self.max_items_per_section = max_items_per_section

    def build_investigation_prompt(
        self, report: LogAnalysisReport, retrieved_incidents: list[RetrievedIncident]
    ) -> list[dict[str, str]]:
        n = self.max_items_per_section
        user_content = f"""=== CURRENT LOG EVIDENCE ===

Statistics:
{_format_statistics(report.statistics)}

Component health:
{_format_component_health(report.component_analysis.components, n)}

Error groups (recurring message signatures):
{_format_error_groups(report.error_groups, n)}

Failure patterns (repeated/bursting failures):
{_format_failure_patterns(report.failure_patterns, n)}

Correlated events (clusters of related failures):
{_format_correlated_events(report.correlated_events, n)}

Timeline (curated notable moments, chronological):
{_format_timeline(report.timeline, n)}

=== HISTORICAL INCIDENTS (retrieved by similarity search -- NOT part of the current incident) ===

{_format_historical_incidents(retrieved_incidents, n)}

=== TASK ===

Investigate the current incident using ONLY the CURRENT LOG EVIDENCE above. Use HISTORICAL INCIDENTS
only as attributed precedent, never as current fact.

{_INVESTIGATION_SCHEMA}"""

        return [
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ]

    def build_qa_prompt(
        self, question: str, context: QAContext, history: Optional[list[ChatMessage]] = None
    ) -> list[dict[str, str]]:
        n = self.max_items_per_section
        user_content = f"""=== CURRENT LOG EVIDENCE (relevant to the question below) ===

Statistics:
{_format_statistics(context.statistics)}

Component health:
{_format_component_health(context.component_summary, n)}

Relevant error groups:
{_format_error_groups(context.relevant_error_groups, n)}

Relevant failure patterns:
{_format_failure_patterns(context.relevant_failure_patterns, n)}

Relevant correlated events:
{_format_correlated_events(context.relevant_correlated_events, n)}

Relevant raw log entries (sample):
{_format_log_entries(context.relevant_entries, n)}

=== HISTORICAL INCIDENTS (retrieved by similarity search -- NOT part of the current incident) ===

{_format_historical_incidents(context.retrieved_incidents, n)}

=== QUESTION ===

{question}

=== TASK ===

Answer the question using ONLY the CURRENT LOG EVIDENCE above for facts about the current system.
Use HISTORICAL INCIDENTS only as attributed precedent, never as current fact.

{_QA_SCHEMA}"""

        messages: list[dict[str, str]] = [{"role": "system", "content": _SYSTEM_PROMPT}]
        for turn in history or []:
            role = "user" if turn.role == "user" else "assistant"
            messages.append({"role": role, "content": turn.content})
        messages.append({"role": "user", "content": user_content})
        return messages
