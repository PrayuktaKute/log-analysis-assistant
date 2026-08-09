"""Generate Markdown incident reports from an `Incident`.

Backs requirement #6: "Generate incident reports."
"""

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import settings
from app.models.schemas import Incident, IncidentReport
from app.utils.file_utils import ensure_dir

_TEMPLATE_DIR = Path(__file__).resolve().parent / "templates"

_jinja_env = Environment(
    loader=FileSystemLoader(str(_TEMPLATE_DIR)),
    autoescape=select_autoescape(disabled_extensions=("j2",)),
    trim_blocks=True,
    lstrip_blocks=True,
)


class ReportGenerator:
    """Renders Incidents into Markdown reports and writes them to disk."""

    def __init__(self, output_dir: Path = settings.reports_output_dir):
        self.output_dir = output_dir
        self.template = _jinja_env.get_template("incident_report.md.j2")
        self.appendix_template = _jinja_env.get_template("incident_report_appendix.md.j2")

    def generate(self, incident: Incident) -> IncidentReport:
        """Render `incident` to Markdown and persist it under `self.output_dir`."""
        generated_at = datetime.now(timezone.utc)
        markdown_content = self.template.render(incident=incident, generated_at=generated_at.isoformat())

        ensure_dir(self.output_dir)
        file_path = self.output_dir / f"{incident.incident_id}.md"
        file_path.write_text(markdown_content, encoding="utf-8")

        return IncidentReport(
            incident_id=incident.incident_id,
            markdown_content=markdown_content,
            file_path=str(file_path),
            generated_at=generated_at,
        )

    def generate_appendix(self, incidents: list[Incident]) -> IncidentReport:
        """Render a single summary report for incidents that didn't qualify
        for an individual LLM investigation (pattern-only incidents,
        low-confidence correlated events) -- see
        `LogAnalysisPipeline.is_minor_incident`."""
        generated_at = datetime.now(timezone.utc)
        markdown_content = self.appendix_template.render(incidents=incidents, generated_at=generated_at.isoformat())

        ensure_dir(self.output_dir)
        incident_id = "appendix-minor-incidents"
        file_path = self.output_dir / f"{incident_id}.md"
        file_path.write_text(markdown_content, encoding="utf-8")

        return IncidentReport(
            incident_id=incident_id,
            markdown_content=markdown_content,
            file_path=str(file_path),
            generated_at=generated_at,
        )
