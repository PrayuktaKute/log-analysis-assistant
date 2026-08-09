"""Build a chronological timeline of the notable moments in a batch of logs.

Responsible for requirement 6, "Timeline Generation". Composes the outputs
of the other deterministic analysis/correlation stages rather than
re-deriving them:

- first critical error: earliest ERROR/CRITICAL entry system-wide.
- bursts of failures: one entry per `FailurePattern` flagged `is_burst`
  (from `FailureDetector`), anchored at its densest window.
- service failures: one entry per component `ComponentAnalyzer` rated
  "critical", anchored at that component's first ERROR/CRITICAL.
- fatal events: one entry per *distinct message* that ever reached
  CRITICAL severity, at its first occurrence -- curated (one per failure
  signature), not a dump of every individual FATAL line.
- recovery events: for each `CorrelatedEvent` cluster that looks like a
  genuine incident (confidence_score >= `min_recovery_confidence` and at
  least `min_recovery_cluster_size` events -- filtering out the low-signal
  "busy window" clusters that dominate this dataset), check whether *every*
  (component, host) pair involved in the cluster produced a subsequent
  INFO-severity entry within `recovery_window_seconds`. If so, the whole
  incident is considered resolved at the latest of those per-pair recovery
  timestamps. If any involved pair never shows a follow-up INFO entry in
  time, no recovery event is emitted for that cluster -- hence "(if any)".
  (One INFO log alone is weak evidence of "recovery" -- see the
  architecture explanation for why this heuristic is necessarily
  best-effort without semantic understanding of the messages.)
"""

import bisect
from datetime import datetime, timedelta
from typing import Optional

from app.config import settings
from app.models.schemas import (
    ComponentAnalysisResult,
    CorrelatedEvent,
    FailurePattern,
    LogEntry,
    LogSeverity,
    TimelineEvent,
    TimelineEventType,
)

_CRITICAL_LEVELS = frozenset({LogSeverity.ERROR, LogSeverity.CRITICAL})


class TimelineGenerator:
    """Builds a chronologically sorted list of curated TimelineEvents."""

    def __init__(
        self,
        recovery_window_seconds: int = settings.recovery_window_seconds,
        min_recovery_confidence: float = settings.timeline_min_recovery_confidence,
        min_recovery_cluster_size: int = settings.timeline_min_recovery_cluster_size,
        recovery_severity: LogSeverity = settings.timeline_recovery_severity_enum,
    ):
        self.recovery_window = timedelta(seconds=recovery_window_seconds)
        self.min_recovery_confidence = min_recovery_confidence
        self.min_recovery_cluster_size = min_recovery_cluster_size
        self.recovery_severity = recovery_severity

    def generate(
        self,
        entries: list[LogEntry],
        failure_patterns: list[FailurePattern],
        correlated_events: list[CorrelatedEvent],
        component_analysis: ComponentAnalysisResult,
    ) -> list[TimelineEvent]:
        events: list[TimelineEvent] = []
        events.extend(self._first_critical_error(entries))
        events.extend(self._bursts(failure_patterns))
        events.extend(self._service_failures(entries, component_analysis))
        events.extend(self._fatal_events(entries))
        events.extend(self._recovery_events(entries, correlated_events))

        events.sort(key=lambda e: e.timestamp)
        return events

    def _first_critical_error(self, entries: list[LogEntry]) -> list[TimelineEvent]:
        critical_entries = [e for e in entries if e.severity in _CRITICAL_LEVELS]
        if not critical_entries:
            return []
        first = min(critical_entries, key=lambda e: e.timestamp)
        return [
            TimelineEvent(
                event_type=TimelineEventType.FIRST_CRITICAL_ERROR,
                timestamp=first.timestamp,
                title="First critical error",
                description=f"First ERROR/CRITICAL event: '{first.message}' on {first.component}@{first.host}",
                component=first.component,
                host=first.host,
                related_entries=[first],
            )
        ]

    def _bursts(self, failure_patterns: list[FailurePattern]) -> list[TimelineEvent]:
        events = []
        for pattern in failure_patterns:
            if not pattern.is_burst or pattern.peak_window_start is None:
                continue
            events.append(
                TimelineEvent(
                    event_type=TimelineEventType.BURST_OF_FAILURES,
                    timestamp=pattern.peak_window_start,
                    title=f"Burst of '{pattern.message}'",
                    description=(
                        f"{pattern.peak_window_count} occurrences of '{pattern.message}' clustered tightly, "
                        f"affecting {', '.join(pattern.affected_services)}"
                    ),
                    related_entries=pattern.sample_events,
                )
            )
        return events

    def _service_failures(
        self, entries: list[LogEntry], component_analysis: ComponentAnalysisResult
    ) -> list[TimelineEvent]:
        critical_components = {c.component for c in component_analysis.components if c.health_status == "critical"}
        if not critical_components:
            return []

        first_failure: dict[str, LogEntry] = {}
        for entry in entries:
            if entry.component in critical_components and entry.severity in _CRITICAL_LEVELS:
                existing = first_failure.get(entry.component)
                if existing is None or entry.timestamp < existing.timestamp:
                    first_failure[entry.component] = entry

        return [
            TimelineEvent(
                event_type=TimelineEventType.SERVICE_FAILURE,
                timestamp=entry.timestamp,
                title=f"{component} entered a critical failure state",
                description=(
                    f"'{component}' crossed the critical error-rate threshold, starting with '{entry.message}'"
                ),
                component=component,
                host=entry.host,
                related_entries=[entry],
            )
            for component, entry in first_failure.items()
        ]

    def _fatal_events(self, entries: list[LogEntry]) -> list[TimelineEvent]:
        first_fatal_by_message: dict[str, LogEntry] = {}
        for entry in entries:
            if entry.severity != LogSeverity.CRITICAL:
                continue
            existing = first_fatal_by_message.get(entry.message)
            if existing is None or entry.timestamp < existing.timestamp:
                first_fatal_by_message[entry.message] = entry

        return [
            TimelineEvent(
                event_type=TimelineEventType.FATAL_EVENT,
                timestamp=entry.timestamp,
                title=f"Fatal: {entry.message}",
                description=f"First FATAL occurrence of '{entry.message}' on {entry.component}@{entry.host}",
                component=entry.component,
                host=entry.host,
                related_entries=[entry],
            )
            for entry in first_fatal_by_message.values()
        ]

    def _recovery_events(
        self, entries: list[LogEntry], correlated_events: list[CorrelatedEvent]
    ) -> list[TimelineEvent]:
        if not correlated_events:
            return []

        info_index: dict[tuple[str, str], list[LogEntry]] = {}
        for entry in entries:
            if entry.severity == self.recovery_severity:
                info_index.setdefault((entry.component, entry.host), []).append(entry)
        for group_entries in info_index.values():
            group_entries.sort(key=lambda e: e.timestamp)

        events: list[TimelineEvent] = []
        for cluster in correlated_events:
            if (
                cluster.confidence_score < self.min_recovery_confidence
                or len(cluster.related_events) < self.min_recovery_cluster_size
            ):
                continue  # low-signal "busy window" cluster -- not a real incident to track recovery for

            involved_pairs = sorted({(e.component, e.host) for e in cluster.related_events})
            recoveries: list[LogEntry] = []
            for component, host in involved_pairs:
                candidates = info_index.get((component, host))
                recovery = self._first_after(candidates, cluster.end_time, self.recovery_window) if candidates else None
                if recovery is None:
                    recoveries = []
                    break  # every involved pair must recover for the incident to count as resolved
                recoveries.append(recovery)

            if not recoveries:
                continue

            last_recovery = max(recoveries, key=lambda e: e.timestamp)
            events.append(
                TimelineEvent(
                    event_type=TimelineEventType.RECOVERY,
                    timestamp=last_recovery.timestamp,
                    title=f"Incident {cluster.correlation_id} resolved",
                    description=(
                        f"All {len(involved_pairs)} component/host pair(s) involved in incident "
                        f"{cluster.correlation_id} showed normal activity again by this point"
                    ),
                    component=last_recovery.component,
                    host=last_recovery.host,
                    related_entries=recoveries,
                )
            )
        return events

    @staticmethod
    def _first_after(sorted_entries: list[LogEntry], after: datetime, window: timedelta) -> Optional[LogEntry]:
        timestamps = [e.timestamp for e in sorted_entries]
        idx = bisect.bisect_right(timestamps, after)
        if idx >= len(sorted_entries):
            return None
        candidate = sorted_entries[idx]
        if candidate.timestamp - after > window:
            return None
        return candidate
