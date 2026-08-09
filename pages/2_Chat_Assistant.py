"""Chat Assistant page: natural-language Q&A over the loaded logs.

Uses the current `QAEngine.answer(question, report, entries, history)` API,
which returns a `QAParseResult` (not a plain string). `report`/`entries`
come from the Dashboard page's pipeline run, stored in `st.session_state`.
"""

import streamlit as st

from app.logging_config import configure_logging
from app.models.schemas import ChatMessage
from app.services.pipeline import LogAnalysisPipeline

configure_logging()

st.set_page_config(page_title="Chat Assistant - Log Analysis Assistant", page_icon="💬", layout="wide")
st.title("💬 Chat Assistant")
st.caption("Ask questions like: \"What are the most critical errors?\" or \"Show all PostgreSQL-related errors.\"")
st.caption(
    "Each question makes a real local Ollama call (no caching) -- expect a few minutes per "
    "answer on CPU-only inference; a spinner will show while it's working."
)

if "pipeline" not in st.session_state:
    st.session_state.pipeline = LogAnalysisPipeline()
if "chat_history" not in st.session_state:
    st.session_state.chat_history: list[ChatMessage] = []
for key in ("report", "entries"):
    if key not in st.session_state:
        st.session_state[key] = None

report = st.session_state.report
entries = st.session_state.entries

if report is None or entries is None:
    st.warning("No analysis data loaded yet -- run the pipeline on the **Dashboard** page first.")

for msg in st.session_state.chat_history:
    with st.chat_message(msg.role):
        st.write(msg.content)

question = st.chat_input("Ask a question about your logs...")
if question:
    st.session_state.chat_history.append(ChatMessage(role="user", content=question))
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner(
            "Thinking... (local CPU inference -- has taken 2-6+ minutes per question, sometimes "
            "longer on a cold-started model, in earlier testing on this machine)"
        ):
            result = st.session_state.pipeline.qa_engine.answer(
                question,
                report=report,
                entries=entries,
                history=st.session_state.chat_history[:-1],
            )

        if result.success and result.answer is not None:
            answer = result.answer
            st.write(answer.answer)

            if answer.current_log_evidence:
                with st.expander("Current log evidence"):
                    for item in answer.current_log_evidence:
                        st.write(f"- {item}")

            if answer.historical_incidents:
                with st.expander("Historical incidents cited"):
                    for ref in answer.historical_incidents:
                        st.write(f"- {ref.incident_id}: {ref.title} -- {ref.relevance_explanation}")

            if answer.recommendations:
                with st.expander("Recommendations"):
                    for rec in answer.recommendations:
                        st.write(f"- {rec}")

            st.caption(
                f"Confidence: {answer.confidence_level.value}"
                + ("" if answer.evidence_sufficient else " -- evidence judged insufficient")
            )
            display_text = answer.answer
        else:
            st.error(f"Could not answer: {result.error}")
            display_text = f"(error: {result.error})"

        st.session_state.chat_history.append(ChatMessage(role="assistant", content=display_text))
