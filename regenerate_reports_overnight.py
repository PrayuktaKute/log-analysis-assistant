"""Resilient, resumable regeneration of every incident report -- meant for
an unattended overnight run against a local Ollama server.

Not part of the pytest suite -- run directly:

    python regenerate_reports_overnight.py

Differs from `verify_generate_reports.py` (which just calls
`pipeline.run()` + `pipeline.generate_reports()` in one shot) in three ways
needed for a long unattended run:

1. Progress (incident ID, outcome, elapsed seconds) is appended to
   `logs/regeneration_run.log` after every single incident, not just at
   the end -- so you can tail the log overnight and know exactly how far
   it got even if the process never finishes.
2. Each qualifying incident's investigation is wrapped in its own
   try/except: an Ollama timeout/error/unexpected exception on one
   incident is logged and the run moves on to the next one, rather than
   the whole batch aborting.
3. Resumable: before investigating a qualifying incident, its report file
   is checked on disk first -- if `reports/<incident_id>.md` already
   exists, it's skipped. Re-running this script after an interruption
   (crash, machine sleep, Ctrl-C) only processes what's left.

Minor/low-confidence incidents (pattern-only, or a correlated event below
`settings.investigation_min_confidence`) never call the LLM -- they're
always regenerated fresh into the single appendix report at the end, which
takes seconds.
"""

import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from loguru import logger

from app.config import settings
from app.llm.ollama_client import OllamaClient
from app.logging_config import configure_logging
from app.models.schemas import Incident, LogSeverity
from app.services.pipeline import LogAnalysisPipeline

PROGRESS_LOG_PATH = Path(__file__).resolve().parent / "logs" / "regeneration_run.log"

# Generous single-attempt timeout dedicated to this unattended run -- long
# enough that a real-but-slow generation isn't mistaken for a hang, short
# enough that one stuck call can't stall the whole overnight run
# indefinitely. No retries: a fresh attempt on the next incident is more
# useful than re-trying the same slow call twice in a row.
PER_CALL_TIMEOUT_SECONDS = 600
PER_CALL_MAX_RETRIES = 1


def _log_progress(line: str) -> None:
    PROGRESS_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with PROGRESS_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {line}\n")


def _process_qualifying_incident(pipeline: LogAnalysisPipeline, report, event, related_patterns) -> str:
    """Build, investigate, and render one correlated-event incident that
    met the confidence bar. Returns an outcome string for the progress log.
    Never raises -- any exception is caught by the caller."""
    incident_view = pipeline._build_incident_report_view(report, event, related_patterns)
    investigation = pipeline._investigate_incident(incident_view)

    incident = Incident(
        incident_id=f"incident-{event.correlation_id}",
        title=pipeline._event_title(event),
        severity=event.probable_trigger.severity if event.probable_trigger else LogSeverity.UNKNOWN,
        correlated_events=[event],
        failure_patterns=related_patterns,
        similar_incidents=pipeline._retrieve_similar(event=event),
        timeline=incident_view.timeline,
        investigation=investigation,
    )
    pipeline.report_generator.generate(incident)
    return "SUCCESS" if investigation is not None else "FALLBACK (no valid investigation; deterministic report written)"


def main() -> int:
    configure_logging()
    _log_progress(
        f"=== Run started | model={settings.ollama_model} | "
        f"per_call_timeout={PER_CALL_TIMEOUT_SECONDS}s | "
        f"investigation_min_confidence={settings.investigation_min_confidence} ==="
    )

    pipeline = LogAnalysisPipeline()
    # Override the shared LLM client with this run's dedicated timeout/retry
    # settings -- QAEngine (used internally by _investigate_incident) reads
    # whatever client object is assigned here.
    pipeline.llm_client = OllamaClient(timeout_seconds=PER_CALL_TIMEOUT_SECONDS, max_retries=PER_CALL_MAX_RETRIES)
    pipeline.qa_engine.llm_client = pipeline.llm_client

    entries = pipeline._ingest()
    if not entries:
        _log_progress("No log entries parsed -- aborting.")
        return 1

    report = pipeline.analyzer.analyze(entries)
    pipeline._ensure_knowledge_base_loaded()

    qualifying_count = sum(
        1 for e in report.correlated_events if e.confidence_score >= settings.investigation_min_confidence
    )
    _log_progress(
        f"{len(report.correlated_events)} correlated event(s), {qualifying_count} qualify for "
        f"individual investigation, {len(report.failure_patterns)} failure pattern(s) total"
    )

    matched_pattern_ids: set[str] = set()
    minor_incidents: list[Incident] = []
    completed = skipped = failed = 0

    for event in report.correlated_events:
        incident_id = f"incident-{event.correlation_id}"
        related_patterns = [
            p for p in report.failure_patterns if p.message in event.structured_evidence.distinct_messages
        ]
        matched_pattern_ids.update(p.pattern_id for p in related_patterns)

        if event.confidence_score < settings.investigation_min_confidence:
            minor_incidents.append(
                Incident(
                    incident_id=incident_id,
                    title=pipeline._event_title(event),
                    severity=event.probable_trigger.severity if event.probable_trigger else LogSeverity.UNKNOWN,
                    correlated_events=[event],
                    failure_patterns=related_patterns,
                    similar_incidents=pipeline._retrieve_similar(event=event),
                )
            )
            continue

        report_path = pipeline.report_generator.output_dir / f"{incident_id}.md"
        if report_path.exists():
            skipped += 1
            _log_progress(f"{incident_id} | SKIPPED (report already exists)")
            continue

        start = time.perf_counter()
        try:
            outcome = _process_qualifying_incident(pipeline, report, event, related_patterns)
            elapsed = time.perf_counter() - start
            _log_progress(f"{incident_id} | {outcome} | {elapsed:.1f}s")
            completed += 1
        except Exception as exc:  # noqa: BLE001 - one bad incident must never abort the overnight run
            elapsed = time.perf_counter() - start
            logger.exception("Unexpected error processing {}", incident_id)
            _log_progress(f"{incident_id} | ERROR | {elapsed:.1f}s | {exc!r}")
            failed += 1
            continue

    for pattern in report.failure_patterns:
        if pattern.pattern_id in matched_pattern_ids:
            continue
        minor_incidents.append(
            Incident(
                incident_id=f"incident-{pattern.pattern_id}",
                title=pattern.description,
                severity=pipeline._pattern_severity(pattern),
                correlated_events=[],
                failure_patterns=[pattern],
                similar_incidents=pipeline._retrieve_similar(pattern=pattern),
            )
        )

    try:
        pipeline.report_generator.generate_appendix(minor_incidents)
        _log_progress(f"appendix | SUCCESS | {len(minor_incidents)} minor incident(s) summarized")
    except OSError as exc:
        _log_progress(f"appendix | ERROR | {exc!r}")

    _log_progress(
        f"=== Run finished | completed={completed} skipped={skipped} failed={failed} "
        f"(of {qualifying_count} qualifying incident(s)) ==="
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
