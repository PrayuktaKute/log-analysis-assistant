"""Rank services/components by failure count and summarize their health.

Responsible for requirement 3, "Component Analysis".
"""

from collections import Counter, defaultdict

from app.config import settings
from app.models.schemas import ComponentAnalysisResult, ComponentHealth, LogEntry, LogSeverity


class ComponentAnalyzer:
    """Computes per-component health and ranks components by failure count."""

    def __init__(
        self,
        failure_severities: frozenset[LogSeverity] = settings.component_failure_severities_set,
        degraded_threshold: float = settings.component_degraded_threshold,
        critical_threshold: float = settings.component_critical_threshold,
    ):
        self.failure_severities = failure_severities
        self.degraded_threshold = degraded_threshold
        self.critical_threshold = critical_threshold

    def analyze(self, entries: list[LogEntry]) -> ComponentAnalysisResult:
        by_component: dict[str, list[LogEntry]] = defaultdict(list)
        for entry in entries:
            by_component[entry.component].append(entry)

        components = [self._build_health(component, group) for component, group in by_component.items()]
        components.sort(key=lambda c: (-c.failure_count, -c.error_rate, c.component))

        most_failing = components[0].component if components and components[0].failure_count > 0 else None

        return ComponentAnalysisResult(components=components, most_failing_component=most_failing)

    def _build_health(self, component: str, group: list[LogEntry]) -> ComponentHealth:
        total = len(group)
        severity_counts = Counter(e.severity.value for e in group)
        failure_count = sum(1 for e in group if e.severity in self.failure_severities)
        error_rate = failure_count / total if total else 0.0

        failure_messages = Counter(e.message for e in group if e.severity in self.failure_severities)
        top_failure_message = failure_messages.most_common(1)[0][0] if failure_messages else None

        return ComponentHealth(
            component=component,
            total_logs=total,
            severity_counts=dict(severity_counts),
            failure_count=failure_count,
            error_rate=round(error_rate, 4),
            top_failure_message=top_failure_message,
            health_status=self._health_status(error_rate),
        )

    def _health_status(self, error_rate: float) -> str:
        if error_rate >= self.critical_threshold:
            return "critical"
        if error_rate >= self.degraded_threshold:
            return "degraded"
        return "healthy"
