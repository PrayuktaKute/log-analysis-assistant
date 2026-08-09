"""Standalone verification script for `LogAnalysisPipeline.run()`.

Not part of the pytest suite -- run directly:

    python verify_pipeline.py

Executes the full pipeline against the sample wilston logs in `data/logs/`,
prints the requested counts, sanity-checks that the returned `Incident`
objects are fully populated, and reports any pre-existing issues observed
along the way.
"""

import sys
import time

from app.logging_config import configure_logging
from app.services.pipeline import LogAnalysisPipeline


def main() -> int:
    configure_logging()

    pipeline = LogAnalysisPipeline()

    # Ingestion is cheap and side-effect-free, so it's safe to run once here
    # (purely to report the raw parsed-entry count) and again inside run().
    entries = pipeline._ingest()
    print(f"Parsed log entries: {len(entries)}")

    start = time.perf_counter()
    incidents = pipeline.run()
    elapsed = time.perf_counter() - start

    correlated_event_count = sum(len(i.correlated_events) for i in incidents)
    failure_pattern_count = sum(len(i.failure_patterns) for i in incidents)
    retrieved_incident_count = sum(len(i.similar_incidents) for i in incidents)

    print(f"Correlated events: {correlated_event_count}")
    print(f"Failure patterns: {failure_pattern_count}")
    print(f"Retrieved historical incidents: {retrieved_incident_count}")
    print(f"Incidents assembled: {len(incidents)}")
    print(f"Pipeline run() took {elapsed:.1f}s")

    issues: list[str] = []

    if not incidents:
        issues.append("Pipeline returned zero incidents -- nothing further to verify.")
    else:
        print("\nIncidents:")
        for incident in incidents:
            print(f"  - {incident.incident_id}: {incident.title!r} (severity={incident.severity.value})")

        primary = incidents[0]
        print(f"\nGenerated Incident ID (first): {primary.incident_id}")

        required_fields = ["incident_id", "title", "severity", "correlated_events", "failure_patterns", "created_at"]
        for incident in incidents:
            for field in required_fields:
                value = getattr(incident, field)
                if value in (None, "", []):
                    issues.append(f"{incident.incident_id}: field '{field}' is empty/unset.")
            if not incident.correlated_events and not incident.failure_patterns:
                issues.append(f"{incident.incident_id}: has neither correlated_events nor failure_patterns.")
            if incident.created_at is None:
                issues.append(f"{incident.incident_id}: missing created_at timestamp.")

    print("\n--- Pre-existing issues discovered during verification ---")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("None found.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
