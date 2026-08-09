"""Data contracts shared across the ingestion, correlation, RAG, and
reporting layers.

These are pure data models (pydantic) with no behavior. Keeping them in one
place means every module agrees on the same shape for a "log event", an
"incident", etc.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class LogSeverity(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    UNKNOWN = "UNKNOWN"


class LogEntry(BaseModel):
    """A single, structured log line parsed from a source file.

    Carries both parsing provenance (`source_file`, `line_number` -- for
    debugging and error reporting) and the normalized analytics fields
    (`service`, `component`, `host`, `trace_id`, `order_id`) that later
    correlation, failure-detection, and reporting stages will key off of.
    """

    timestamp: datetime
    severity: LogSeverity = LogSeverity.UNKNOWN
    message: str

    source: str = Field(..., description="Originating system as declared in the log line, e.g. 'application', 'docker', 'plc'")
    source_file: str = Field(..., description="Name of the file this entry was parsed from")
    line_number: int = Field(..., description="1-indexed line number within source_file")

    service: str = Field(..., description="Originating service name, e.g. 'api-gateway'")
    component: str = Field(..., description="Logical component; currently derived 1:1 from `service`")
    host: str = Field(..., description="Host/node the event originated from")
    trace_id: Optional[str] = Field(default=None, description="Request/correlation trace ID if present")
    order_id: Optional[str] = Field(default=None, description="Business order ID, present on a subset of entries")

    raw_line: str = Field(..., description="The original, unparsed line, kept for debugging/audit")
    fields: dict[str, Any] = Field(
        default_factory=dict,
        description="Any additional key=value fields not yet promoted to first-class attributes",
    )


class CorrelationEvidence(BaseModel):
    """Machine-readable evidence backing a CorrelatedEvent's confidence
    score -- the structured counterpart to `supporting_evidence`, meant to
    be consumed programmatically by later RAG/LLM stages rather than
    displayed as-is."""

    shared_host: Optional[str] = Field(default=None, description="Set if every event in the cluster shares one host")
    shared_service: Optional[str] = Field(default=None, description="Set if every event in the cluster shares one service")
    shared_category: Optional[str] = Field(
        default=None, description="Set if every event in the cluster shares one failure category"
    )
    cluster_size: int
    time_span_seconds: float
    involved_hosts_count: int
    involved_components_count: int
    severity_counts: dict[str, int] = Field(default_factory=dict)
    distinct_messages: list[str] = Field(default_factory=list)


class CorrelatedEvent(BaseModel):
    """A cluster of LogEntries a deterministic heuristic judged to be related --
    e.g. an incident that produced symptoms across several services/hosts
    within a short time window."""

    correlation_id: str
    start_time: datetime
    end_time: datetime
    involved_components: list[str]
    involved_hosts: list[str]
    related_events: list[LogEntry]
    probable_trigger: Optional[LogEntry] = Field(
        default=None, description="The earliest occurrence of the cluster's worst severity -- the likely root symptom"
    )
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    supporting_evidence: list[str] = Field(
        default_factory=list, description="Human-readable reasons this cluster was formed"
    )
    structured_evidence: CorrelationEvidence = Field(
        ..., description="Machine-readable counterpart to supporting_evidence, for RAG/LLM consumption"
    )


class FailurePattern(BaseModel):
    """A repeated-failure signature detected across one or more sources."""

    pattern_id: str
    description: str
    message: str = Field(..., description="The exact recurring message text this pattern groups on")
    occurrences: int
    first_seen: datetime
    last_seen: datetime
    affected_sources: list[str]
    affected_services: list[str]
    affected_hosts: list[str]
    sample_events: list[LogEntry]

    is_burst: bool = Field(default=False, description="Whether occurrences clustered densely within a single time window")
    peak_window_start: Optional[datetime] = Field(
        default=None, description="Start of the densest occurrence window found, if is_burst"
    )
    peak_window_count: int = Field(default=0, description="Occurrences within the densest window found")


class ErrorGroup(BaseModel):
    """All non-INFO entries sharing the same message text, i.e. the same
    failure signature -- the basic unit of "similar log messages grouped
    together" (deterministic, since the message catalog is a fixed set of
    templates with no embedded dynamic data)."""

    group_id: str
    message: str
    category: str = Field(..., description="Static failure category, e.g. 'database', 'network' (see message_catalog.py)")

    count: int
    severity_counts: dict[str, int] = Field(default_factory=dict, description="Occurrences per LogSeverity value")
    dominant_severity: LogSeverity

    first_seen: datetime
    last_seen: datetime

    affected_services: list[str]
    affected_hosts: list[str]
    affected_sources: list[str]

    sample_entries: list[LogEntry] = Field(default_factory=list, description="A few representative occurrences")


class SeverityAnalysisResult(BaseModel):
    """Counts and distribution of log severities, plus the worst entries."""

    total_logs: int
    counts: dict[str, int]
    distribution_pct: dict[str, float]
    most_critical_events: list[LogEntry]


class ComponentHealth(BaseModel):
    """Deterministic health summary for one service/component."""

    component: str
    total_logs: int
    severity_counts: dict[str, int]
    failure_count: int = Field(..., description="ERROR + CRITICAL count for this component")
    error_rate: float = Field(..., description="failure_count / total_logs")
    top_failure_message: Optional[str] = None
    health_status: str = Field(..., description="'healthy' | 'degraded' | 'critical'")


class ComponentAnalysisResult(BaseModel):
    """Components ranked by failure count, worst first."""

    components: list[ComponentHealth]
    most_failing_component: Optional[str] = None


class TimelineEventType(str, Enum):
    FIRST_CRITICAL_ERROR = "first_critical_error"
    BURST_OF_FAILURES = "burst_of_failures"
    SERVICE_FAILURE = "service_failure"
    FATAL_EVENT = "fatal_event"
    RECOVERY = "recovery_event"


class TimelineEvent(BaseModel):
    """One notable, curated moment on the incident timeline."""

    event_type: TimelineEventType
    timestamp: datetime
    title: str
    description: str
    component: Optional[str] = None
    host: Optional[str] = None
    related_entries: list[LogEntry] = Field(default_factory=list)


class MessageFrequency(BaseModel):
    message: str
    count: int


class ComponentFailureSummary(BaseModel):
    component: str
    failure_count: int
    error_rate: float


class LogStatistics(BaseModel):
    """Structured summary statistics over an ingested batch of LogEntries."""

    total_logs: int
    error_count: int
    warning_count: int
    fatal_count: int

    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None

    affected_hosts: list[str]
    affected_services: list[str]
    affected_sources: list[str]

    top_recurring_messages: list[MessageFrequency]
    top_failing_components: list[ComponentFailureSummary]


class LogAnalysisReport(BaseModel):
    """The complete output of the deterministic analysis pipeline
    (app.analysis.log_analyzer.LogAnalyzer) over one batch of LogEntries."""

    error_groups: list[ErrorGroup]
    severity_analysis: SeverityAnalysisResult
    component_analysis: ComponentAnalysisResult
    failure_patterns: list[FailurePattern]
    correlated_events: list[CorrelatedEvent]
    timeline: list[TimelineEvent]
    statistics: LogStatistics


class HistoricalIncident(BaseModel):
    """An entry in the RAG knowledge base of past incidents."""

    incident_id: str
    title: str
    summary: str
    root_cause: Optional[str] = None
    resolution: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


class RetrievedIncident(BaseModel):
    """A historical incident returned by similarity search, with its score."""

    incident: HistoricalIncident
    similarity_score: float


class Incident(BaseModel):
    """A synthesized incident, built from correlated events + failure patterns,
    optionally enriched with similar historical incidents and an LLM-generated
    investigation."""

    incident_id: str
    title: str
    severity: LogSeverity
    correlated_events: list[CorrelatedEvent]
    failure_patterns: list[FailurePattern]
    similar_incidents: list[RetrievedIncident] = Field(default_factory=list)
    timeline: list["TimelineEvent"] = Field(
        default_factory=list, description="Curated timeline events scoped to this incident's time window/components"
    )
    investigation: Optional["IncidentInvestigation"] = Field(
        default=None,
        description="LLM-generated investigation (executive summary, root causes, recommendations, "
        "confidence level). None if this incident didn't meet the confidence bar for an individual "
        "investigation, or if the LLM call failed.",
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class IncidentReport(BaseModel):
    """The final Markdown report produced for an Incident."""

    incident_id: str
    markdown_content: str
    file_path: Optional[str] = None
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ChatMessage(BaseModel):
    """A single turn in the natural-language Q&A chat interface."""

    role: str = Field(..., description="'user' or 'assistant'")
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ==== LLM integration (app.llm.*) ====
#
# The LLM is only ever asked to return JSON matching one of the models
# below (see app.llm.prompt_builder); app.llm.response_parser validates the
# response against that model and never lets a malformed response reach
# the caller as an exception -- every parse path returns one of the
# `*ParseResult` wrappers, which callers must check via `success` before
# trusting the parsed payload.


class ConfidenceLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RootCauseHypothesis(BaseModel):
    """One candidate explanation for the incident. `supporting_evidence`
    must point only to CURRENT LOG EVIDENCE -- never to historical
    incidents (those are cited separately, see IncidentInvestigation)."""

    description: str
    likelihood: ConfidenceLevel
    supporting_evidence: list[str] = Field(default_factory=list)


class SimilarIncidentRef(BaseModel):
    """A historical incident cited in an LLM response, kept structurally
    distinct from current-log evidence so it can never be silently
    presented as a fact about the current incident."""

    incident_id: str
    title: str
    similarity_score: Optional[float] = None
    relevance_explanation: str


class IncidentInvestigation(BaseModel):
    """Structured LLM output for a full incident investigation, combining
    current log evidence, deterministic analysis results, and retrieved
    historical incidents."""

    executive_summary: str
    incident_summary: str
    possible_root_causes: list[RootCauseHypothesis] = Field(default_factory=list)
    supporting_evidence: list[str] = Field(
        default_factory=list, description="Facts drawn from CURRENT LOG EVIDENCE only"
    )
    similar_historical_incidents: list[SimilarIncidentRef] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW
    ai_reasoning: str = Field(
        default="",
        description="Explanation of how the conclusions above were reached, drawn only from CURRENT LOG "
        "EVIDENCE and HISTORICAL INCIDENTS -- satisfies 'clearly explain how conclusions were reached'",
    )
    open_questions: list[str] = Field(
        default_factory=list, description="Questions CURRENT LOG EVIDENCE could not answer"
    )
    evidence_sufficient: bool = Field(
        default=True, description="False if the model judged current evidence too thin for a confident conclusion"
    )


class LLMParseResult(BaseModel):
    """Wraps a parsed IncidentInvestigation, or -- if the raw response
    wasn't valid JSON matching that schema -- the raw text and an error
    description. Callers must check `success` before using `investigation`."""

    success: bool
    investigation: Optional[IncidentInvestigation] = None
    raw_response: str
    error: Optional[str] = None


class QAAnswer(BaseModel):
    """Structured LLM output for one natural-language Q&A turn. `question`
    is filled in by QAEngine after parsing, not requested from the LLM."""

    question: str = ""
    answer: str
    current_log_evidence: list[str] = Field(default_factory=list)
    historical_incidents: list[SimilarIncidentRef] = Field(default_factory=list)
    ai_reasoning: str = ""
    recommendations: list[str] = Field(default_factory=list)
    confidence_level: ConfidenceLevel = ConfidenceLevel.LOW
    evidence_sufficient: bool = True


class QAParseResult(BaseModel):
    """Wraps a parsed QAAnswer, or -- if parsing failed -- the raw text and
    an error description. Callers must check `success` before using `answer`."""

    success: bool
    answer: Optional[QAAnswer] = None
    raw_response: str
    error: Optional[str] = None
