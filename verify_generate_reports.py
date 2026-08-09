"""Standalone verification script for `LogAnalysisPipeline.generate_reports()`.

Not part of the pytest suite -- run directly:

    python verify_generate_reports.py

Executes the full pipeline, generates Markdown incident reports, and checks
that every returned `IncidentReport` corresponds to a real file on disk
whose contents match `IncidentReport.markdown_content` exactly.
"""

import sys
from pathlib import Path

from app.logging_config import configure_logging
from app.services.pipeline import LogAnalysisPipeline


def main() -> int:
    configure_logging()

    pipeline = LogAnalysisPipeline()

    incidents = pipeline.run()
    print(f"Pipeline produced {len(incidents)} incident(s).")

    reports = pipeline.generate_reports(incidents)
    print(f"generate_reports() produced {len(reports)} report(s).")

    issues: list[str] = []

    if len(reports) != len(incidents):
        issues.append(f"Expected one report per incident ({len(incidents)}), got {len(reports)}.")

    report_incident_ids = {r.incident_id for r in reports}
    incident_ids = {i.incident_id for i in incidents}
    if report_incident_ids != incident_ids:
        issues.append(
            "Report incident_ids do not match pipeline incident_ids. "
            f"Missing: {incident_ids - report_incident_ids}, extra: {report_incident_ids - incident_ids}"
        )

    print("\nPer-report checks:")
    for report in reports:
        if not report.file_path:
            issues.append(f"{report.incident_id}: IncidentReport.file_path is not set.")
            continue

        path = Path(report.file_path)
        if not path.exists():
            issues.append(f"{report.incident_id}: report file does not exist at {path}.")
            continue

        on_disk = path.read_text(encoding="utf-8")
        if on_disk != report.markdown_content:
            issues.append(
                f"{report.incident_id}: file contents at {path} do not match "
                f"IncidentReport.markdown_content ({len(on_disk)} vs {len(report.markdown_content)} chars)."
            )
        else:
            print(f"  OK  {report.incident_id} -> {path} ({len(on_disk)} chars, matches)")

    print("\n--- Issues found ---")
    if issues:
        for issue in issues:
            print(f"- {issue}")
    else:
        print("None. All reports exist on disk and match the returned IncidentReport content.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
