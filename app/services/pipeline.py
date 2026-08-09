"""End-to-end orchestration: read -> parse -> normalize -> correlate ->
detect failures -> retrieve similar incidents -> generate report.

This is the single entrypoint the Streamlit frontend calls into. It wires
together every module from `app/*` but contains no analysis logic itself.
"""

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from loguru import logger

from app.analysis.log_analyzer import LogAnalyzer
from app.config import settings
from app.correlation.event_correlator import EventCorrelator
from app.correlation.failure_detector import FailureDetector
from app.embeddings.embedder import Embedder
from app.ingestion.log_parser import LogParser
from app.ingestion.log_reader import LogReader
from app.ingestion.normalizer import LogNormalizer
from app.llm.ollama_client import OllamaClient
from app.llm.qa_engine import QAEngine
from app.models.schemas import (
    ComponentAnalysisResult,
    CorrelatedEvent,
    FailurePattern,
    Incident,
    IncidentInvestigation,
    IncidentReport,
    LogAnalysisReport,
    LogEntry,
    LogSeverity,
    RetrievedIncident,
    TimelineEvent,
)
from app.rag.knowledge_base import KnowledgeBaseLoader
from app.rag.retriever import IncidentRetriever
from app.reporting.report_generator import ReportGenerator
from app.vectorstore.faiss_store import FaissVectorStore

_SEVERITY_RANK: dict[LogSeverity, int] = {
    LogSeverity.DEBUG: 0,
    LogSeverity.INFO: 1,
    LogSeverity.UNKNOWN: 1,
    LogSeverity.WARNING: 2,
    LogSeverity.ERROR: 3,
    LogSeverity.CRITICAL: 4,
}


class LogAnalysisPipeline:
    """Coordinates all modules to turn raw log files into incident reports
    and a queryable Q&A engine."""

    def __init__(self, log_dir: Path = settings.log_input_dir):
        self.reader = LogReader(log_dir=log_dir)
        self.parser = LogParser()
        self.normalizer = LogNormalizer()
        self.correlator = EventCorrelator()
        self.failure_detector = FailureDetector()
        self.analyzer = LogAnalyzer()

        self.embedder = Embedder()
        self.vector_store = FaissVectorStore()
        self.retriever = IncidentRetriever(vector_store=self.vector_store)
        self.knowledge_base_loader = KnowledgeBaseLoader()

        self.llm_client = OllamaClient()
        self.qa_engine = QAEngine(llm_client=self.llm_client, retriever=self.retriever)
        self.report_generator = ReportGenerator()

    def run(self, investigate: bool = True) -> list[Incident]:
        """Execute the full pipeline over `self.reader.log_dir` and return
        the resulting Incidents.

        Flow: discover_log_files -> read_lines -> parse_line -> normalize ->
        LogAnalyzer (error grouping, correlation, failure detection, ...) ->
        RAG retrieval -> per-incident QAEngine.investigate() -> assembled
        Incidents.

        Only correlated-event incidents at or above
        `settings.investigation_min_confidence` get an individual LLM
        investigation (see `_assemble_incidents`) -- so this makes at most
        one Ollama call per qualifying incident, not one per incident
        detected. That's still up to dozens of multi-minute Ollama calls
        (observed: ~150-370s each on CPU-only local inference), so pass
        `investigate=False` for a fast, LLM-free call (e.g. an interactive
        UI's default "show me the stats" action) -- every Incident is
        still built, just with `investigation=None`. Callers that do want
        the full investigation for a long/offline/overnight run should
        pass `investigate=True` (the default) or use
        `regenerate_reports_overnight.py`, which adds per-incident progress
        logging, resumability, and a dedicated per-call timeout on top of
        this.

        Never raises for ordinary failure modes (empty/missing log dir, a
        single bad file, an unreachable Ollama/embedding backend) -- each of
        those degrades gracefully and is logged, so one bad stage doesn't
        take down the rest of the pipeline.
        """
        logger.info("Starting log analysis pipeline over log_dir={} (investigate={})", self.reader.log_dir, investigate)

        entries = self._ingest()
        if not entries:
            logger.warning("No log entries parsed from {} -- returning no incidents", self.reader.log_dir)
            return []

        report = self.analyzer.analyze(entries)
        logger.info(
            "Analysis complete: {} error group(s), {} correlated event(s), {} failure pattern(s)",
            len(report.error_groups),
            len(report.correlated_events),
            len(report.failure_patterns),
        )

        self._ensure_knowledge_base_loaded()

        incidents = self._assemble_incidents(report, investigate=investigate)
        logger.info("Pipeline produced {} incident(s)", len(incidents))
        return incidents

    def _ingest(self) -> list[LogEntry]:
        """Discover, read, and parse every log file under `self.reader.log_dir`,
        then normalize the combined batch. A single unreadable file is
        logged and skipped rather than aborting ingestion of the rest."""
        files = self.reader.discover_log_files()
        if not files:
            logger.warning("No log files found under {}", self.reader.log_dir)
            return []

        entries: list[LogEntry] = []
        for file_path in files:
            try:
                lines = self.reader.read_lines(file_path)
                result = self.parser.parse_lines(lines, source_file=file_path.name)
            except OSError as exc:
                logger.error("Failed to read log file {}: {}", file_path, exc)
                continue

            logger.info(
                "Parsed {} entries from {} ({} line(s) skipped)",
                len(result.entries),
                file_path.name,
                len(result.skipped_line_numbers),
            )
            entries.extend(result.entries)

        return self.normalizer.normalize(entries)

    def _ensure_knowledge_base_loaded(self) -> None:
        """Make sure `self.vector_store` has an index to search: load a
        previously persisted one if present, else build one from the
        knowledge base JSON and persist it for next time. Any failure here
        (e.g. the embedding model can't be loaded) degrades to an empty,
        searchable-but-empty vector store rather than crashing the pipeline.
        """
        if self.vector_store.index is not None:
            return

        try:
            self.vector_store.load()
        except FileNotFoundError:
            try:
                incidents = self.knowledge_base_loader.load()
                self.vector_store.build_index(incidents)
                if incidents:
                    self.vector_store.save()
            except Exception as exc:  # noqa: BLE001 - never let RAG setup crash the pipeline
                logger.error("Failed to build FAISS index from knowledge base: {}", exc)
        except Exception as exc:  # noqa: BLE001 - a corrupt/incompatible index shouldn't crash the pipeline
            logger.error("Failed to load existing FAISS index: {}", exc)

    def _assemble_incidents(self, report: LogAnalysisReport, investigate: bool = True) -> list[Incident]:
        """Build one Incident per correlated-event cluster (enriched with any
        failure patterns sharing its messages and with retrieved historical
        incidents), plus one Incident per failure pattern not covered by any
        correlated event.

        Only correlated-event incidents whose `confidence_score` is at least
        `settings.investigation_min_confidence` are even candidates for an
        individual LLM investigation (see `_investigate_incident`) --
        pattern-only incidents and low-confidence correlated events are
        still returned (so `generate_reports` can summarize them in the
        appendix) but never trigger an Ollama call themselves.

        Two things additionally gate the actual LLM call for a qualifying
        incident, on top of `investigate`:
        - `investigate=False` skips it entirely (fast, LLM-free run --
          `investigation` stays None on every Incident).
        - a report already on disk for that incident_id skips it too, so a
          repeat call (e.g. clicking "run" again in the Streamlit Dashboard)
          doesn't silently redo dozens of multi-minute Ollama calls for
          incidents already investigated by a previous run -- see
          `generate_reports(..., skip_existing=True)`, which is what keeps
          those existing report files from then being overwritten with a
          now-investigation-less version.
        """
        incidents: list[Incident] = []
        matched_pattern_ids: set[str] = set()

        for event in report.correlated_events:
            related_patterns = [
                p for p in report.failure_patterns if p.message in event.structured_evidence.distinct_messages
            ]
            matched_pattern_ids.update(p.pattern_id for p in related_patterns)

            incident_id = f"incident-{event.correlation_id}"
            investigation: Optional[IncidentInvestigation] = None
            timeline: list[TimelineEvent] = []
            if event.confidence_score >= settings.investigation_min_confidence:
                incident_view = self._build_incident_report_view(report, event, related_patterns)
                timeline = incident_view.timeline
                if investigate and self._has_existing_report(incident_id):
                    logger.debug("Skipping LLM investigation for {} -- report already exists on disk", incident_id)
                elif investigate:
                    investigation = self._investigate_incident(incident_view)

            incidents.append(
                Incident(
                    incident_id=incident_id,
                    title=self._event_title(event),
                    severity=event.probable_trigger.severity if event.probable_trigger else LogSeverity.UNKNOWN,
                    correlated_events=[event],
                    failure_patterns=related_patterns,
                    similar_incidents=self._retrieve_similar(event=event),
                    timeline=timeline,
                    investigation=investigation,
                )
            )

        for pattern in report.failure_patterns:
            if pattern.pattern_id in matched_pattern_ids:
                continue

            incidents.append(
                Incident(
                    incident_id=f"incident-{pattern.pattern_id}",
                    title=pattern.description,
                    severity=self._pattern_severity(pattern),
                    correlated_events=[],
                    failure_patterns=[pattern],
                    similar_incidents=self._retrieve_similar(pattern=pattern),
                )
            )

        return incidents

    @staticmethod
    def _build_incident_report_view(
        report: LogAnalysisReport, event: CorrelatedEvent, patterns: list[FailurePattern]
    ) -> LogAnalysisReport:
        """Narrow the full `LogAnalysisReport` down to what's relevant to one
        correlated-event incident, for a focused (and shorter/cheaper)
        investigation prompt: error groups/timeline/component health scoped
        to this event's messages/components, statistics kept global for
        overall context."""
        relevant_messages = set(event.structured_evidence.distinct_messages) | {p.message for p in patterns}
        involved_components = set(event.involved_components)

        error_groups = [g for g in report.error_groups if g.message in relevant_messages]
        components = [c for c in report.component_analysis.components if c.component in involved_components]
        timeline = [
            te
            for te in report.timeline
            if event.start_time <= te.timestamp <= event.end_time or te.component in involved_components
        ]

        return LogAnalysisReport(
            error_groups=error_groups,
            severity_analysis=report.severity_analysis,
            component_analysis=ComponentAnalysisResult(
                components=components,
                most_failing_component=components[0].component if components else None,
            ),
            failure_patterns=patterns,
            correlated_events=[event],
            timeline=timeline,
            statistics=report.statistics,
        )

    def _investigate_incident(self, incident_view: LogAnalysisReport) -> Optional[IncidentInvestigation]:
        """Run one LLM investigation scoped to a single incident. Any
        failure (Ollama unreachable, malformed response) is logged and
        degrades to `None` -- the incident/report still gets generated,
        just without the AI-generated sections."""
        result = self.qa_engine.investigate(incident_view)
        if result.success and result.investigation is not None:
            return result.investigation
        logger.warning("Per-incident LLM investigation unavailable: {}", result.error)
        return None

    def _has_existing_report(self, incident_id: str) -> bool:
        return (self.report_generator.output_dir / f"{incident_id}.md").exists()

    @staticmethod
    def is_minor_incident(incident: Incident) -> bool:
        """True for incidents that never qualify for an individual
        investigation/report: pattern-only incidents (no correlated event)
        and correlated events below `settings.investigation_min_confidence`.
        Used by `generate_reports` to route these into one batched appendix
        instead of a full report each."""
        if not incident.correlated_events:
            return True
        return incident.correlated_events[0].confidence_score < settings.investigation_min_confidence

    def _retrieve_similar(
        self,
        event: CorrelatedEvent | None = None,
        pattern: FailurePattern | None = None,
    ) -> list[RetrievedIncident]:
        """Retrieve similar historical incidents for one correlated event or
        failure pattern. Any RAG failure (e.g. embedding backend down)
        degrades to no retrieved incidents rather than crashing the pipeline.
        """
        try:
            if event is not None:
                return self.retriever.retrieve_for_correlated_event(event)
            if pattern is not None:
                return self.retriever.retrieve_for_pattern(pattern)
            return []
        except Exception as exc:  # noqa: BLE001 - RAG retrieval must never take down the pipeline
            logger.error("RAG retrieval failed: {}", exc)
            return []

    @staticmethod
    def _event_title(event: CorrelatedEvent) -> str:
        if event.probable_trigger is not None:
            return event.probable_trigger.message
        return event.structured_evidence.distinct_messages[0] if event.structured_evidence.distinct_messages else (
            f"Correlated event {event.correlation_id}"
        )

    @staticmethod
    def _pattern_severity(pattern: FailurePattern) -> LogSeverity:
        if not pattern.sample_events:
            return LogSeverity.UNKNOWN
        return max((e.severity for e in pattern.sample_events), key=lambda s: _SEVERITY_RANK.get(s, 0))

    def generate_reports(self, incidents: list[Incident], skip_existing: bool = False) -> list[IncidentReport]:
        """Generate and persist Markdown reports via `self.report_generator`,
        writing to `settings.reports_output_dir`.

        Incidents that qualified for an individual investigation (see
        `is_minor_incident`) each get a full report; the rest (pattern-only
        incidents, low-confidence correlated events) are summarized together
        in a single appendix report instead of one file each.

        `skip_existing=True` leaves a primary incident's report file
        untouched if it already exists on disk AND this run didn't attach a
        fresh investigation to it (i.e. `_assemble_incidents` was called
        with `investigate=False`, or skipped the LLM call because a report
        already existed) -- otherwise a fast, LLM-free run would overwrite a
        good previously-investigated report with a version that has no
        investigation. The existing file's content is still read back and
        returned as an IncidentReport for a consistent return value.

        A single incident failing to render (e.g. a filesystem error) is
        logged and skipped rather than aborting the rest of the batch.
        """
        primary = [i for i in incidents if not self.is_minor_incident(i)]
        minor = [i for i in incidents if self.is_minor_incident(i)]

        reports: list[IncidentReport] = []
        for incident in primary:
            report_path = self.report_generator.output_dir / f"{incident.incident_id}.md"
            if skip_existing and incident.investigation is None and report_path.exists():
                reports.append(
                    IncidentReport(
                        incident_id=incident.incident_id,
                        markdown_content=report_path.read_text(encoding="utf-8"),
                        file_path=str(report_path),
                        generated_at=datetime.fromtimestamp(report_path.stat().st_mtime, tz=timezone.utc),
                    )
                )
                continue
            try:
                reports.append(self.report_generator.generate(incident))
            except OSError as exc:
                logger.error("Failed to generate report for {}: {}", incident.incident_id, exc)

        if minor:
            try:
                reports.append(self.report_generator.generate_appendix(minor))
            except OSError as exc:
                logger.error("Failed to generate appendix report for {} minor incident(s): {}", len(minor), exc)

        logger.info(
            "Generated {} report(s) for {} incident(s) ({} primary, {} in appendix)",
            len(reports),
            len(incidents),
            len(primary),
            len(minor),
        )
        return reports
