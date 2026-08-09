# AI-Powered Log Analysis Assistant

A local-first assistant that ingests production log files, correlates events
across sources, detects repeated failures, retrieves similar historical
incidents via RAG, and answers natural-language questions about your logs —
all backed by a local LLM (Ollama) and a local FAISS vector index, with a
Streamlit UI.

> **Status: feature-complete.** Ingestion, deterministic log analysis,
> RAG retrieval, LLM integration, Markdown report generation, and the full
> pipeline wiring (including the Streamlit UI) are all implemented end to
> end — see [Ingestion parser](#ingestion-parser),
> [Deterministic log analysis](#deterministic-log-analysis),
> [RAG retrieval](#rag-retrieval), and [LLM integration](#llm-integration)
> below. `LogAnalysisPipeline` (`app/services/pipeline.py`) runs the whole
> flow — read → parse → normalize → analyze → correlate → retrieve →
> investigate → report — and is the only entrypoint the Streamlit pages
> call into. Sample generated reports are in [`reports/`](reports/).

## Tech stack

- Python 3.10+
- [Ollama](https://ollama.com) for the local LLM
- FAISS (`faiss-cpu`) for vector similarity search
- `sentence-transformers` for local embeddings
- Streamlit for the frontend
- Jinja2 for Markdown report templating
- `pydantic-settings` for configuration, `loguru` for logging

## Architecture

```
streamlit_app.py          Streamlit entrypoint (landing page)
pages/                    Multipage Streamlit UI
  1_Dashboard.py             Run the pipeline, view detected incidents
  2_Chat_Assistant.py        Natural-language Q&A over loaded logs
  3_Incident_Reports.py      Browse / download generated Markdown reports

app/
  config.py               Central settings (env-var backed), single source of truth
  logging_config.py       loguru setup (console + rotating file sink)

  models/
    schemas.py             Data contracts: LogEntry, CorrelatedEvent, FailurePattern,
                            HistoricalIncident, RetrievedIncident, Incident,
                            IncidentReport, ChatMessage

  ingestion/                 Requirement 1-2: read + parse + normalize logs (IMPLEMENTED)
    log_reader.py             Discover log files, stream (line_number, raw_line) pairs
    log_parser.py             Raw line -> LogEntry via regex + severity/timestamp handling
    normalizer.py             UTC timestamps, whitespace cleanup, chronological sort

  analysis/                  Deterministic analysis -- no LLM/embeddings (IMPLEMENTED)
    message_catalog.py         Static message -> failure-category map + keyword fallback
    error_grouping.py          ErrorGrouper: group non-INFO entries by message signature
    severity_analysis.py       SeverityAnalyzer: counts, distribution, worst events
    component_analysis.py      ComponentAnalyzer: rank components, health status
    timeline.py                TimelineGenerator: curated chronological incident timeline
    statistics.py              StatisticsGenerator: structured LogStatistics summary
    log_analyzer.py            LogAnalyzer: orchestrates all of the above into one report

  correlation/               Requirement 3-4: correlate + detect repeated failures (IMPLEMENTED)
    event_correlator.py       Deterministic EventCorrelator: time-window + attribute-overlap
                               graph clustering (see "Deterministic log analysis" below)
    failure_detector.py       FailureDetector: repeated-failure + sliding-window burst detection

  embeddings/
    embedder.py               Text -> vector via sentence-transformers (IMPLEMENTED;
                               Ollama embedding provider deferred to LLM integration)

  vectorstore/
    faiss_store.py            FAISS IndexFlatIP build/add/search/save/load (IMPLEMENTED)

  rag/                        Requirement 5: RAG retrieval (IMPLEMENTED)
    knowledge_base.py           Loads HistoricalIncident records from JSON
    retriever.py                FailurePattern/CorrelatedEvent/query -> similar HistoricalIncidents

  llm/                        Requirement 7 + LLM integration (IMPLEMENTED)
    ollama_client.py            Sync+async Ollama chat, model resolution w/ fallback,
                                 retry+backoff, timeout handling
    prompt_builder.py           Builds prompts that separate CURRENT LOG EVIDENCE /
                                 HISTORICAL INCIDENTS / instructions, with a strict
                                 JSON output schema
    response_parser.py          Parses raw LLM text into structured pydantic models;
                                 never raises on malformed output
    qa_engine.py                 QAEngine: investigate() (full structured investigation)
                                 and answer()/aanswer() (grounded Q&A pipeline)

  reporting/                  Requirement 6: Markdown incident reports
    report_generator.py        Renders Incident -> Markdown via Jinja2, writes to disk
    templates/incident_report.md.j2

  services/
    pipeline.py                Orchestrates the full pipeline; the only entrypoint
                                the Streamlit UI calls into

  utils/
    file_utils.py               Generic, non-domain helpers (e.g. ensure_dir)

data/
  logs/                      Drop input log files here (LOG_INPUT_DIR)
  knowledge_base/            Historical incident records for the RAG corpus
                              (incidents.json, 10 seeded example incidents)
  faiss_index/               Persisted FAISS index files

reports/                    Generated Markdown incident reports
logs/                       Application log file (app.log)
tests/                      pytest skeleton, one file per module group
```

### Data flow

```
data/logs/*  ->  LogReader  ->  LogParser  ->  LogNormalizer  ->  list[LogEntry]
                                                                        |
                                                                        v
                                                                  LogAnalyzer
                                              (ErrorGrouper, SeverityAnalyzer, ComponentAnalyzer,
                                               FailureDetector, EventCorrelator, TimelineGenerator,
                                               StatisticsGenerator -- all deterministic, no LLM)
                                                                        |
                                                                        v
                                                            LogAnalysisReport
                                                                        |
                                                                        v
                                          IncidentRetriever <- FaissVectorStore <- Embedder
                                                        |         (historical incidents,
                                                        v          data/knowledge_base/)
                                                    Incident
                                                        |
                                                        v
                                              ReportGenerator -> reports/*.md

                                    (separately) QAEngine(question) -> IncidentRetriever + OllamaClient
```

`app/services/pipeline.py:LogAnalysisPipeline` wires every stage together and
is the only class the Streamlit pages import for pipeline execution.

## Setup

1. **Install [Ollama](https://ollama.com)** and pull a model:
   ```bash
   ollama pull llama3.1
   ```
2. **Create a virtual environment and install dependencies:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure environment variables:**
   ```bash
   copy .env.example .env
   ```
   Adjust `OLLAMA_MODEL`, `EMBEDDING_MODEL_NAME`, thresholds, etc. as needed.
4. **Add log files** to `data/logs/` (any number of files, multiple sources).

## Running

```bash
streamlit run streamlit_app.py
```

Run tests:

```bash
pytest
```

## Ingestion parser

The wilston logs (`application`/`docker`/`plc`) all share one line grammar:

```
<timestamp> [<SEVERITY>] source=<src> service=<svc> host=<host> traceId=<id> [orderId=<id>] <message>
```

`LogParser` (app/ingestion/log_parser.py) matches this with a single
compiled regex and builds a `LogEntry` per line, handling two known
real-world quirks in the sample data:

- **Timestamps** appear as either `...T09:00:00.704000Z` (with 6-digit
  fractional seconds) or `...T09:00:04Z` (whole seconds only, ~0.1% of
  lines). `_parse_timestamp` tries the fractional format first and falls
  back to the whole-second format.
- **`orderId`** is present on ~3% of lines; when absent, the line has an
  extra space before the message. The regex's optional named group plus a
  `+` on the whitespace before the message handles both cases without
  special-casing.

Severity tokens (`INFO`/`WARN`/`ERROR`/`FATAL`) are mapped onto the
canonical `LogSeverity` enum (`WARN`→`WARNING`, `FATAL`→`CRITICAL`); an
unrecognized token doesn't drop the line, it's kept with
`severity=UNKNOWN` and a warning is logged.

**Malformed lines never raise.** `parse_line` returns `None` for blank
lines and for lines that don't match the grammar at all; the latter also
logs a warning with `source_file:line_number` and a snippet of the
offending content, so bad lines are visible without stopping ingestion of
the rest of the file. `parse_lines` (batch entrypoint) collects both the
successfully parsed `entries` and the `skipped_line_numbers` for the file,
via the `ParsedFileResult` dataclass — useful for a future "N lines could
not be parsed" summary in the UI. Across all three real sample files
(10,000 lines each), every line matches the grammar; only the timestamp
fallback path is actually exercised in practice.

`LogNormalizer` then makes every `LogEntry` timezone-aware UTC, collapses
incidental whitespace in `message`, and sorts the batch chronologically —
preparing a unified timeline for the correlation step, without doing any
cross-source grouping itself.

Cross-source correlation is intentionally **not implemented yet**: analysis
of the sample data showed `trace_id` is not a trustworthy cross-source join
key (each source generates it independently over the same ~900k-value
random range, so cross-file matches are statistical coincidence). Ingestion
now exposes all the fields correlation will need — `source`, `source_file`,
`line_number`, `service`, `component`, `host`, `trace_id`, `order_id` — as
first-class `LogEntry` fields, ready for `EventCorrelator` to consume once
its time-window-based strategy is implemented.

## Deterministic log analysis

`app/analysis/` and `app/correlation/` implement seven capabilities over
`list[LogEntry]`, entirely without an LLM, embeddings, or FAISS:

1. **Error grouping** (`ErrorGrouper`) — non-INFO entries grouped by exact
   `message` text (the wilston catalog is a fixed set of templates, so no
   fuzzy matching is needed), tracking count, first/last seen, and affected
   services/hosts/sources per group.
2. **Severity analysis** (`SeverityAnalyzer`) — counts, percentage
   distribution, and the worst events ranked by severity then recency.
3. **Component analysis** (`ComponentAnalyzer`) — components ranked by
   ERROR+CRITICAL count, with a `healthy`/`degraded`/`critical` status from
   a configurable error-rate threshold.
4. **Failure pattern detection** (`FailureDetector`) — every message
   signature occurring `>= repeated_failure_threshold` times becomes a
   `FailurePattern`; a two-pointer sliding-window scan additionally flags
   *bursts* (dense clustering within `repeated_failure_window_minutes`).
5. **Event correlation** (`EventCorrelator`) — candidates (WARNING/ERROR/
   CRITICAL) are linked if they fall within `correlation_window_seconds`
   AND agree on >= 2 of {host, service, failure category}, then merged via
   a **span-bounded** Union-Find (a cluster's total time span is capped at
   the window -- plain adjacent-pair union-find chains indefinitely and
   collapsed 89% of real events into one meaningless 80-minute cluster
   during testing). `trace_id` is deliberately not used -- see
   `event_correlator.py`'s docstring for the empirical reason.
6. **Timeline generation** (`TimelineGenerator`) — composes the outputs
   above into a curated, deduplicated chronological timeline: first
   critical error, bursts, per-component service failures, one entry per
   distinct fatal signature, and best-effort recovery events (only for
   confident/sizeable clusters, requiring every involved component/host
   pair to show renewed activity).
7. **Statistics** (`StatisticsGenerator`) — a single structured
   `LogStatistics` summary (totals, affected hosts/services, top recurring
   messages, top failing components).

`app/analysis/log_analyzer.py:LogAnalyzer` runs all seven and returns one
composed `LogAnalysisReport`. See each module's docstring for the full
rationale behind its heuristics.

**Configurability / reusability.** Every threshold used above (grouped
severities, component health cutoffs, correlation window/matching-dimension
count/confidence-formula weights, burst threshold/window, recovery
gating, top-N sizes) is read from `Settings` (`app/config.py`) --
overridable via `.env` / environment variables, not hardcoded. The
message -> failure-category mapping used for the "related error patterns"
correlation signal is external, editable JSON
(`config/message_categories.json`, path also configurable via
`MESSAGE_CATEGORY_CONFIG_PATH`) with a generic keyword-based fallback for
any message not explicitly listed -- so pointing this project at a
different log source mostly means replacing that one file and adjusting
`.env`, not editing analysis code. Each `CorrelatedEvent` also carries a
`structured_evidence` object (`shared_host`, `shared_service`,
`shared_category`, `cluster_size`, `time_span_seconds`, ...) alongside the
human-readable `supporting_evidence` strings, for later RAG/LLM stages to
consume programmatically.

## RAG retrieval

`Embedder` (app/embeddings/embedder.py) wraps a local `sentence-transformers`
model (`BAAI/bge-small-en-v1.5` by default), returning L2-normalized
384-dim vectors. `FaissVectorStore` (app/vectorstore/faiss_store.py) holds
them in an exact `IndexFlatIP` index -- inner product over normalized
vectors is exact cosine similarity, and exact search is appropriate at the
scale of a historical-incident knowledge base (hundreds to low thousands
of entries; an approximate index would be premature optimization). The
index and its id -> `HistoricalIncident` sidecar map persist to
`data/faiss_index/` via `save()`/`load()`.

`KnowledgeBaseLoader` (app/rag/knowledge_base.py) reads
`data/knowledge_base/incidents.json` -- 10 seeded example incidents
covering the failure categories seen in the wilston data (Postgres
deadlocks, Redis outages, Kafka publish failures, PLC timeouts, Docker
OOM-kills, JWT rotation issues, payment-gateway resets, Mongo failover,
schema-break exceptions, memory leaks). Replace this file for a different
deployment's real incident history.

`IncidentRetriever` (app/rag/retriever.py) builds a search query from
either a `FailurePattern`, a `CorrelatedEvent` (using its
`structured_evidence`), or free text, and returns ranked
`RetrievedIncident`s. Verified against real data: retrieving for the
`FailurePattern` for `"PLC communication timeout"` correctly surfaces the
seeded PLC incident at 0.85 cosine similarity, ahead of unrelated
incidents at 0.6-0.65.

No LLM calls are involved in retrieval itself -- `Embedder` and
`FaissVectorStore` only need the local embedding model, not Ollama.
`LogAnalyzer` is not yet wired to call `IncidentRetriever` automatically;
that composition, plus the Streamlit UI hookup, is part of the pipeline
wiring roadmap item below.

## LLM integration

`app/llm/` combines current log evidence (from `LogAnalysisReport`),
retrieved historical incidents (from `IncidentRetriever`), and a local
Ollama model into structured, source-attributed output. No cloud calls;
everything runs against a local Ollama server.

- **`OllamaClient`** (ollama_client.py) — sync (`chat`) and async (`achat`)
  chat completion. `resolve_model()` checks the server's available models
  and picks, in order: the configured `ollama_model` (default `llama3.1`),
  then each of `ollama_fallback_models` (default `qwen2.5,llama3,mistral`),
  else the configured model unchanged (so a real call fails with a clear
  server-side error rather than the client guessing further). Retries
  (`ollama_max_retries`, default 3, linear backoff via
  `ollama_retry_backoff_seconds`) apply only to transient transport
  failures (`httpx.HTTPError`, connection/timeout) -- an `ollama.ResponseError`
  (e.g. bad model, bad request) fails fast since retrying an unchanged
  request can't fix it. `ollama_timeout_seconds` defaults to 180s: CPU
  inference of an 8B model measured over 90s on the development machine
  used to build this, so a shorter default would flag ordinary slow-but-
  successful calls as failures.
- **`PromptBuilder`** (prompt_builder.py) — see [prompt engineering](#prompt-engineering-strategy) below.
- **`ResponseParser`** (response_parser.py) — see [hallucination prevention](#hallucination-prevention) below.
- **`QAEngine`** (qa_engine.py) — `investigate(report)` produces a full
  structured incident investigation; `answer(question, report, entries)` /
  `aanswer(...)` runs the Q&A pipeline (deterministic relevant-context
  selection -> historical retrieval -> prompt -> Ollama -> structured
  answer). Both gracefully return `success=False` (no LLM call attempted)
  if `report`/`entries` aren't supplied yet, and gracefully catch
  `OllamaUnavailableError`/`ollama.ResponseError` around the LLM call
  itself -- nothing in this module raises out to a caller under normal
  failure modes.

Verified end-to-end against the real wilston data and a real local Ollama
server (`llama3.2:3b`): asking "Show PostgreSQL errors." correctly cited
the exact matching log line as `current_log_evidence`, retrieved a
relevant historical incident, and returned `confidence_level: high` --
including one real run where the first attempt timed out and the retry
succeeded.

Constructing `QAEngine` doesn't require Ollama to be running (the client
only connects when a method is actually called); `resolve_model()` and
`chat()`/`achat()` do.

## Implementation status

All core requirements are implemented:

1. ~~`LogReader` / `LogParser` / `LogNormalizer`~~ — **implemented**, see [Ingestion parser](#ingestion-parser) above.
2. ~~`EventCorrelator` / `FailureDetector` / analysis suite~~ — **implemented**, see [Deterministic log analysis](#deterministic-log-analysis) above.
3. ~~`Embedder` / `FaissVectorStore` / `IncidentRetriever`~~ — **implemented**, see [RAG retrieval](#rag-retrieval) above.
4. ~~`OllamaClient` / `PromptBuilder` / `ResponseParser` / `QAEngine`~~ — **implemented**, see [LLM integration](#llm-integration) above.
5. ~~`ReportGenerator`~~ — **implemented**: renders `Incident` (including `QAEngine.investigate()` output) to Markdown via the Jinja2 template at `app/reporting/templates/incident_report.md.j2`. Sample output is in [`reports/`](reports/).
6. ~~`LogAnalysisPipeline.run()` / `.generate_reports()`~~ — **implemented**: wires `LogAnalyzer` + `IncidentRetriever` + `QAEngine` + `ReportGenerator` into the end-to-end flow; the Streamlit pages (`pages/1_Dashboard.py`, `pages/2_Chat_Assistant.py`, `pages/3_Incident_Reports.py`) call into it directly.

`regenerate_reports_overnight.py` drives a full, resumable batch run of the
pipeline over `data/logs/` for long/offline regeneration of every report in
`reports/`.
