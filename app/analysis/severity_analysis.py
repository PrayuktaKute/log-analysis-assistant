"""Severity-level counts, distribution, and the most critical events.

Responsible for requirement 2, "Severity Analysis".
"""

from collections import Counter

from app.config import settings
from app.models.schemas import LogEntry, LogSeverity, SeverityAnalysisResult

_SEVERITY_RANK: dict[LogSeverity, int] = {
    LogSeverity.DEBUG: 0,
    LogSeverity.INFO: 1,
    LogSeverity.UNKNOWN: 1,
    LogSeverity.WARNING: 2,
    LogSeverity.ERROR: 3,
    LogSeverity.CRITICAL: 4,
}


class SeverityAnalyzer:
    """Computes severity counts/distribution and ranks the worst events."""

    def analyze(self, entries: list[LogEntry], top_n: int = settings.severity_top_n) -> SeverityAnalysisResult:
        total = len(entries)
        counts = Counter(e.severity.value for e in entries)

        distribution = {
            severity: round((count / total) * 100, 2) if total else 0.0 for severity, count in counts.items()
        }

        most_critical = sorted(
            entries,
            key=lambda e: (-_SEVERITY_RANK.get(e.severity, 0), e.timestamp),
        )[:top_n]

        return SeverityAnalysisResult(
            total_logs=total,
            counts=dict(counts),
            distribution_pct=distribution,
            most_critical_events=most_critical,
        )
