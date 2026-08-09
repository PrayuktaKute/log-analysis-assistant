"""Orchestrates the full deterministic analysis pipeline over a batch of
LogEntries: error grouping, severity/component analytics, failure-pattern
detection, event correlation, timeline generation, and statistics.

No LLM calls, no embeddings, no FAISS, no RAG -- see the individual
modules under app/analysis and app/correlation for each stage.
"""

from loguru import logger

from app.analysis.component_analysis import ComponentAnalyzer
from app.analysis.error_grouping import ErrorGrouper
from app.analysis.severity_analysis import SeverityAnalyzer
from app.analysis.statistics import StatisticsGenerator
from app.analysis.timeline import TimelineGenerator
from app.correlation.event_correlator import EventCorrelator
from app.correlation.failure_detector import FailureDetector
from app.models.schemas import LogAnalysisReport, LogEntry


class LogAnalyzer:
    """Single entrypoint that runs every deterministic analysis stage and
    returns one composed `LogAnalysisReport`."""

    def __init__(
        self,
        error_grouper: ErrorGrouper | None = None,
        severity_analyzer: SeverityAnalyzer | None = None,
        component_analyzer: ComponentAnalyzer | None = None,
        failure_detector: FailureDetector | None = None,
        event_correlator: EventCorrelator | None = None,
        timeline_generator: TimelineGenerator | None = None,
        statistics_generator: StatisticsGenerator | None = None,
    ):
        self.error_grouper = error_grouper or ErrorGrouper()
        self.severity_analyzer = severity_analyzer or SeverityAnalyzer()
        self.component_analyzer = component_analyzer or ComponentAnalyzer()
        self.failure_detector = failure_detector or FailureDetector(grouper=self.error_grouper)
        self.event_correlator = event_correlator or EventCorrelator()
        self.timeline_generator = timeline_generator or TimelineGenerator()
        self.statistics_generator = statistics_generator or StatisticsGenerator()

    def analyze(self, entries: list[LogEntry]) -> LogAnalysisReport:
        logger.info("Running deterministic log analysis over {} entries", len(entries))

        error_groups = self.error_grouper.group(entries)
        severity_analysis = self.severity_analyzer.analyze(entries)
        component_analysis = self.component_analyzer.analyze(entries)
        failure_patterns = self.failure_detector.detect_repeated_failures(entries)
        correlated_events = self.event_correlator.correlate(entries)
        timeline = self.timeline_generator.generate(
            entries=entries,
            failure_patterns=failure_patterns,
            correlated_events=correlated_events,
            component_analysis=component_analysis,
        )
        statistics = self.statistics_generator.generate(entries, component_analysis)

        return LogAnalysisReport(
            error_groups=error_groups,
            severity_analysis=severity_analysis,
            component_analysis=component_analysis,
            failure_patterns=failure_patterns,
            correlated_events=correlated_events,
            timeline=timeline,
            statistics=statistics,
        )
