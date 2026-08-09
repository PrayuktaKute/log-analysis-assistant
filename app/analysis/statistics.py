"""Generate structured summary statistics over a batch of LogEntries.

Responsible for requirement 7, "Statistics".
"""

from collections import Counter

from app.config import settings
from app.models.schemas import (
    ComponentAnalysisResult,
    ComponentFailureSummary,
    LogEntry,
    LogSeverity,
    LogStatistics,
    MessageFrequency,
)


class StatisticsGenerator:
    """Aggregates entries + component analysis into a single LogStatistics."""

    def generate(
        self,
        entries: list[LogEntry],
        component_analysis: ComponentAnalysisResult,
        top_n: int = settings.statistics_top_n,
    ) -> LogStatistics:
        severity_counts = Counter(e.severity for e in entries)
        message_counts = Counter(e.message for e in entries)

        timestamps = [e.timestamp for e in entries]

        top_messages = [
            MessageFrequency(message=message, count=count)
            for message, count in message_counts.most_common(top_n)
        ]
        top_components = [
            ComponentFailureSummary(
                component=c.component, failure_count=c.failure_count, error_rate=c.error_rate
            )
            for c in component_analysis.components[:top_n]
            if c.failure_count > 0
        ]

        return LogStatistics(
            total_logs=len(entries),
            error_count=severity_counts.get(LogSeverity.ERROR, 0),
            warning_count=severity_counts.get(LogSeverity.WARNING, 0),
            fatal_count=severity_counts.get(LogSeverity.CRITICAL, 0),
            time_range_start=min(timestamps) if timestamps else None,
            time_range_end=max(timestamps) if timestamps else None,
            affected_hosts=sorted({e.host for e in entries}),
            affected_services=sorted({e.service for e in entries}),
            affected_sources=sorted({e.source for e in entries}),
            top_recurring_messages=top_messages,
            top_failing_components=top_components,
        )
