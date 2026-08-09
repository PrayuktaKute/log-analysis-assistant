"""Dashboard page: load logs, run the pipeline, review detected failures.

Three explicit, opt-in stages, all hitting `LogAnalysisPipeline`'s public
API only:

1. "Run analysis pipeline" -> `pipeline.run(investigate=False)` +
   `pipeline.generate_reports(..., skip_existing=True)` -- fast (seconds),
   makes zero Ollama calls, and never overwrites a report that already has
   a real AI investigation on disk from a previous run.
2. "Regenerate full AI investigation reports" -> `pipeline.run(investigate=True)`
   -- one real Ollama call per qualifying correlated-event incident
   (confidence >= `settings.investigation_min_confidence`), each observed
   at 150-370s on local CPU inference. Easily hours for the full incident
   set, so it's gated behind an explicit confirmation checkbox. Incidents
   that already have a report are skipped automatically. For a genuinely
   long unattended run, `regenerate_reports_overnight.py` (run from a
   terminal) is a better fit -- it adds resumability and per-incident
   progress logging to a file.
3. "Generate AI investigation report" (whole-batch) -> `pipeline.qa_engine.investigate()`
   over the *entire* LogAnalysisReport at once (not per-incident) -- a
   single LLM call, kept separate so the fast deterministic results above
   aren't gated behind it.
"""

import pandas as pd
import streamlit as st

from app.config import settings
from app.logging_config import configure_logging
from app.services.pipeline import LogAnalysisPipeline

configure_logging()

st.set_page_config(page_title="Dashboard - Log Analysis Assistant", page_icon="📊", layout="wide")
st.title("📊 Dashboard")

st.write(f"Log input directory: `{settings.log_input_dir}`")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = LogAnalysisPipeline()
for key in ("entries", "report", "incidents", "incident_reports", "investigation"):
    if key not in st.session_state:
        st.session_state[key] = None

pipeline = st.session_state.pipeline

st.subheader("1. Run analysis pipeline")
st.caption(
    "Ingests every log file, runs deterministic analysis + RAG retrieval, and assembles "
    "Incidents via `LogAnalysisPipeline.run(investigate=False)` -- fast (seconds), makes "
    "**zero** Ollama calls. Any incident that already has a full AI-investigated report on "
    "disk (e.g. from an overnight run) is left untouched, not overwritten."
)
if st.button("Run analysis pipeline", type="primary"):
    with st.spinner("Running LogAnalysisPipeline.run(investigate=False) (ingest, analyze, correlate, retrieve, assemble)..."):
        entries = pipeline._ingest()
        report = pipeline.analyzer.analyze(entries) if entries else None
        incidents = pipeline.run(investigate=False)
    with st.spinner("Writing/refreshing Markdown incident reports (skipping ones already investigated)..."):
        incident_reports = pipeline.generate_reports(incidents, skip_existing=True)

    st.session_state.entries = entries
    st.session_state.report = report
    st.session_state.incidents = incidents
    st.session_state.incident_reports = incident_reports
    st.session_state.investigation = None
    st.success(
        f"Pipeline produced {len(incidents)} incident(s) and {len(incident_reports)} report(s) "
        "(fast pass -- no per-incident AI investigation performed)."
    )

entries = st.session_state.entries
report = st.session_state.report
incidents = st.session_state.incidents
incident_reports = st.session_state.incident_reports

if incidents is None:
    st.info("No results yet. Click **Run analysis pipeline** above.")
    st.stop()

st.divider()
st.subheader("2. Ingestion statistics")
if not entries:
    st.warning("No log entries were parsed -- check that log files exist under the log input directory.")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Parsed log entries", len(entries))
    c2.metric("Error groups", len(report.error_groups) if report else 0)
    c3.metric("Correlated events", len(report.correlated_events) if report else 0)
    c4.metric("Failure patterns", len(report.failure_patterns) if report else 0)

    severity_counts = pd.Series([e.severity.value for e in entries]).value_counts()
    source_counts = pd.Series([e.source for e in entries]).value_counts()
    col_a, col_b = st.columns(2)
    with col_a:
        st.write("By severity")
        st.dataframe(severity_counts.rename("count"), use_container_width=True)
    with col_b:
        st.write("By source")
        st.dataframe(source_counts.rename("count"), use_container_width=True)

st.divider()
st.subheader("3. Correlated events")
if report and report.correlated_events:
    events_df = pd.DataFrame(
        [
            {
                "correlation_id": e.correlation_id,
                "start_time": e.start_time,
                "confidence": e.confidence_score,
                "components": ", ".join(e.involved_components),
                "hosts": ", ".join(e.involved_hosts),
                "trigger": e.probable_trigger.message if e.probable_trigger else "",
                "trigger_severity": e.probable_trigger.severity.value if e.probable_trigger else "",
                "cluster_size": e.structured_evidence.cluster_size,
            }
            for e in report.correlated_events
        ]
    )
    st.dataframe(events_df, use_container_width=True, height=300)
else:
    st.write("No correlated events detected.")

st.divider()
st.subheader("4. Failure patterns")
if report and report.failure_patterns:
    patterns_df = pd.DataFrame(
        [
            {
                "pattern_id": p.pattern_id,
                "message": p.message,
                "occurrences": p.occurrences,
                "is_burst": p.is_burst,
                "peak_window_count": p.peak_window_count,
                "affected_services": ", ".join(p.affected_services),
            }
            for p in report.failure_patterns
        ]
    )
    st.dataframe(patterns_df, use_container_width=True, height=300)
else:
    st.write("No repeated failure patterns detected.")

st.divider()
st.subheader("5. Incident inspector (retrieved historical incidents, per incident)")
if incidents:
    severity_options = sorted({i.severity.value for i in incidents})
    selected_severities = st.multiselect("Filter by severity", severity_options, default=severity_options)
    filtered = [i for i in incidents if i.severity.value in selected_severities]
    st.caption(f"Showing {len(filtered)} of {len(incidents)} incident(s).")

    options = {f"{i.incident_id} -- {i.title} ({i.severity.value})": i for i in filtered[:500]}
    choice = st.selectbox("Select an incident to inspect", options=list(options.keys())) if options else None

    if choice:
        incident = options[choice]
        st.markdown(f"**{incident.title}**  \nSeverity: `{incident.severity.value}` | ID: `{incident.incident_id}`")

        if incident.correlated_events:
            st.write("Correlated events:")
            for e in incident.correlated_events:
                st.write(
                    f"- `{e.correlation_id}` confidence={e.confidence_score:.2f}, "
                    f"window {e.start_time} -> {e.end_time}, "
                    f"components={e.involved_components}, hosts={e.involved_hosts}"
                )

        if incident.failure_patterns:
            st.write("Attached failure patterns:")
            for p in incident.failure_patterns:
                st.write(f"- `{p.message}` -- {p.occurrences} occurrence(s), burst={p.is_burst}")

        st.write("Retrieved historical incidents (RAG):")
        if incident.similar_incidents:
            for r in incident.similar_incidents:
                st.write(
                    f"- **{r.incident.title}** (`{r.incident.incident_id}`, similarity={r.similarity_score:.3f}) "
                    f"-- {r.incident.summary}"
                )
        else:
            st.write("  (none retrieved)")
else:
    st.write("No incidents to inspect.")

st.divider()
st.subheader("5b. Regenerate full AI investigation reports (slow)")
st.caption(
    f"Calls `LogAnalysisPipeline.run(investigate=True)` -- one real Ollama call per "
    f"correlated-event incident at confidence >= {settings.investigation_min_confidence} "
    f"({sum(1 for e in report.correlated_events if e.confidence_score >= settings.investigation_min_confidence) if report else '?'} "
    "on the currently loaded data), each observed to take 150-370s on local CPU inference -- "
    "easily hours in total. Incidents that already have a report on disk are skipped "
    "automatically, so a repeat run only processes what's new. For a genuinely long "
    "unattended run, prefer running `python regenerate_reports_overnight.py` from a terminal "
    "instead -- it adds resumability and per-incident progress logging to a file, and won't "
    "tie up this page."
)
confirm_slow_run = st.checkbox("I understand this can take hours and will block this page until it finishes.")
if report is None:
    st.info("Run the pipeline first.")
elif st.button("Regenerate full AI investigation reports", disabled=not confirm_slow_run):
    with st.spinner("Running LogAnalysisPipeline.run(investigate=True) -- this can take a long time..."):
        incidents = pipeline.run(investigate=True)
    with st.spinner("Generating Markdown incident reports..."):
        incident_reports = pipeline.generate_reports(incidents, skip_existing=True)

    st.session_state.incidents = incidents
    st.session_state.incident_reports = incident_reports
    st.success(f"Produced {len(incidents)} incident(s) and {len(incident_reports)} report(s).")

incidents = st.session_state.incidents
incident_reports = st.session_state.incident_reports

st.divider()
st.subheader("6. AI investigation report (whole-batch)")
st.caption(
    "Calls `QAEngine.investigate(report)` directly over the *entire* current LogAnalysisReport "
    "in one shot -- a single LLM call, separate from the per-incident investigations in section "
    "5b above. Local CPU inference can take a couple of minutes."
)
if report is None:
    st.info("Run the pipeline first.")
elif st.button("Generate AI investigation report"):
    with st.spinner("Calling QAEngine.investigate() -- this can take a few minutes on local CPU inference..."):
        st.session_state.investigation = pipeline.qa_engine.investigate(report)

investigation = st.session_state.investigation
if investigation is not None:
    if investigation.success and investigation.investigation is not None:
        inv = investigation.investigation
        st.success(f"Confidence: {inv.confidence_level.value}")
        st.markdown(f"**Executive summary**\n\n{inv.executive_summary}")
        st.markdown(f"**Incident summary**\n\n{inv.incident_summary}")

        if inv.possible_root_causes:
            st.write("**Possible root causes**")
            for cause in inv.possible_root_causes:
                st.write(f"- ({cause.likelihood.value}) {cause.description}")
                for evidence in cause.supporting_evidence:
                    st.caption(f"  evidence: {evidence}")

        if inv.supporting_evidence:
            st.write("**Supporting evidence (current logs)**")
            for evidence in inv.supporting_evidence:
                st.write(f"- {evidence}")

        if inv.similar_historical_incidents:
            st.write("**Cited historical incidents**")
            for ref in inv.similar_historical_incidents:
                st.write(f"- {ref.incident_id}: {ref.title} -- {ref.relevance_explanation}")

        if inv.recommended_actions:
            st.write("**Recommended actions**")
            for action in inv.recommended_actions:
                st.write(f"- {action}")

        if not inv.evidence_sufficient:
            st.warning("The model judged current evidence insufficient for a fully confident conclusion.")
        if inv.open_questions:
            st.write("**Open questions**")
            for q in inv.open_questions:
                st.write(f"- {q}")
    else:
        st.warning(f"AI investigation unavailable: {investigation.error}")

st.divider()
st.subheader("7. Generated incident reports")
if incident_reports:
    st.write(f"{len(incident_reports)} Markdown report(s) written to `{settings.reports_output_dir}`.")
    st.page_link("pages/3_Incident_Reports.py", label="Browse & download reports", icon="📄")
else:
    st.write("No reports generated yet.")
