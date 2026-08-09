"""Central application configuration.

All runtime configuration is sourced from environment variables (optionally
loaded from a local `.env` file). Every other module should import the
shared `settings` singleton from here rather than reading `os.environ`
directly.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.models.schemas import LogSeverity

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_severities(value: str) -> frozenset[LogSeverity]:
    """Parse a comma-separated env var (e.g. "WARNING,ERROR,CRITICAL") into
    a frozenset of LogSeverity. Unknown tokens are ignored rather than
    raising, so a typo in an env var degrades gracefully instead of
    crashing the app at import time."""
    result = set()
    for token in value.split(","):
        token = token.strip().upper()
        if not token:
            continue
        try:
            result.add(LogSeverity(token))
        except ValueError:
            continue
    return frozenset(result)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # ==== LLM (Ollama) ====
    ollama_base_url: str = "http://localhost:11434"
    # Smallest model measured on this hardware -- CPU-only inference (no GPU
    # offload available), so the 8B models (llama3.1/llama3) and mistral
    # (7B) took 4-6+ minutes per investigation call vs. this one being
    # markedly faster once warm. Chosen for practical unattended batch runs.
    ollama_model: str = "llama3.2:3b"
    # Tried in order if `ollama_model` isn't pulled on the server.
    ollama_fallback_models: str = "llama3.1,mistral,llama3"
    # CPU-only inference of a full investigation/QA prompt (~2000-2500
    # tokens in, structured JSON out) was observed taking 150-370s on this
    # hardware even with the small 3B model -- 180s guaranteed a timeout on
    # every attempt (retrying at the same too-short timeout doesn't help;
    # it just repeats the same failure). 450s covers the observed worst
    # case with margin.
    ollama_timeout_seconds: int = 450
    # Retrying mainly helps genuine transient failures (dropped connection,
    # brief server hiccup) -- it can't fix a call that's simply too slow
    # for the timeout, so keep this low: 2 attempts means a worst case of
    # ~2*450s=900s instead of 3*450s=1350s if something really is stuck.
    ollama_max_retries: int = 2
    ollama_retry_backoff_seconds: float = 2.0
    # Low temperature: this assistant should read evidence back
    # consistently, not creatively.
    ollama_temperature: float = 0.2

    # ==== LLM prompt construction (app.llm.prompt_builder) ====
    llm_prompt_max_items_per_section: int = 10

    # ==== Embeddings ====
    embedding_provider: str = "sentence-transformers"
    embedding_model_name: str = "BAAI/bge-small-en-v1.5"
    embedding_dimension: int = 384

    # ==== FAISS vector store ====
    faiss_index_dir: Path = PROJECT_ROOT / "data" / "faiss_index"
    faiss_index_name: str = "incidents.index"

    # ==== Data paths ====
    log_input_dir: Path = PROJECT_ROOT / "data" / "logs"
    knowledge_base_dir: Path = PROJECT_ROOT / "data" / "knowledge_base"
    reports_output_dir: Path = PROJECT_ROOT / "reports"

    # ==== Message categorization (app.analysis.message_catalog) ====
    # JSON file mapping messages/keywords to failure categories. Replace this
    # file (or point the path elsewhere) to adapt category inference to a
    # different log source without touching code.
    message_category_config_path: Path = PROJECT_ROOT / "config" / "message_categories.json"

    # ==== Error grouping (app.analysis.error_grouping) ====
    error_grouping_severities: str = "WARNING,ERROR,CRITICAL"
    error_grouping_sample_size: int = 3
    # Collapse embedded numeric content (IDs, counts, ...) before grouping
    # by message, so structurally-identical messages with different dynamic
    # values still group together. No-op on datasets (like wilston) whose
    # message templates contain no digits.
    error_grouping_normalize_dynamic_content: bool = True

    # ==== Component analysis (app.analysis.component_analysis) ====
    component_failure_severities: str = "ERROR,CRITICAL"
    component_degraded_threshold: float = 0.05
    component_critical_threshold: float = 0.15

    # ==== Severity analysis (app.analysis.severity_analysis) ====
    severity_top_n: int = 10

    # ==== Correlation / failure detection ====
    correlation_window_seconds: int = 30
    correlation_candidate_severities: str = "WARNING,ERROR,CRITICAL"
    correlation_min_matching_dimensions: int = 2
    # confidence = base + per_dimension * (dims matched) + corroboration bonus, capped at 1.0
    correlation_confidence_base: float = 0.3
    correlation_confidence_per_dimension: float = 0.2
    correlation_confidence_corroboration_bonus_max: float = 0.1
    correlation_confidence_corroboration_per_event: float = 0.02

    repeated_failure_threshold: int = 3
    repeated_failure_window_minutes: int = 15

    # ==== Timeline (app.analysis.timeline) ====
    recovery_window_seconds: int = 120
    timeline_recovery_severity: str = "INFO"
    timeline_min_recovery_confidence: float = 0.5
    timeline_min_recovery_cluster_size: int = 3

    # ==== Statistics (app.analysis.statistics) ====
    statistics_top_n: int = 5

    # ==== RAG ====
    rag_top_k: int = 5

    # ==== Per-incident LLM investigation (app.services.pipeline) ====
    # Only correlated-event incidents at or above this confidence get an
    # individual QAEngine.investigate() call + full report; everything else
    # (single-pattern incidents, low-confidence correlated events) is batched
    # into one appendix report instead, so LLM calls stay practical even when
    # hundreds of incidents are detected.
    investigation_min_confidence: float = 0.5

    # ==== Logging ====
    log_level: str = "INFO"
    log_file: Path = PROJECT_ROOT / "logs" / "app.log"

    @property
    def faiss_index_path(self) -> Path:
        return self.faiss_index_dir / self.faiss_index_name

    @property
    def error_grouping_severities_set(self) -> frozenset[LogSeverity]:
        return parse_severities(self.error_grouping_severities)

    @property
    def component_failure_severities_set(self) -> frozenset[LogSeverity]:
        return parse_severities(self.component_failure_severities)

    @property
    def correlation_candidate_severities_set(self) -> frozenset[LogSeverity]:
        return parse_severities(self.correlation_candidate_severities)

    @property
    def timeline_recovery_severity_enum(self) -> LogSeverity:
        try:
            return LogSeverity(self.timeline_recovery_severity.strip().upper())
        except ValueError:
            return LogSeverity.INFO


settings = Settings()
