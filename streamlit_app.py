"""Streamlit entrypoint: AI-Powered Log Analysis Assistant.

Run with:
    streamlit run streamlit_app.py

This is the landing page. Additional pages live in `pages/` and are
auto-discovered by Streamlit's multipage app support.
"""

import streamlit as st

from app.config import settings
from app.logging_config import configure_logging

configure_logging()

st.set_page_config(
    page_title="Log Analysis Assistant",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 AI-Powered Log Analysis Assistant")
st.caption("Local-first log correlation, failure detection, and RAG-powered incident analysis.")

st.markdown(
    """
    Use the sidebar to navigate:

    - **Dashboard** — load log files, run the analysis pipeline, and review detected failures.
    - **Chat Assistant** — ask natural-language questions about the currently loaded logs.
    - **Incident Reports** — browse and download generated Markdown incident reports.
    """
)

with st.expander("Current configuration", expanded=False):
    st.json(
        {
            "ollama_base_url": settings.ollama_base_url,
            "ollama_model": settings.ollama_model,
            "embedding_provider": settings.embedding_provider,
            "embedding_model_name": settings.embedding_model_name,
            "log_input_dir": str(settings.log_input_dir),
            "faiss_index_path": str(settings.faiss_index_path),
            "reports_output_dir": str(settings.reports_output_dir),
        }
    )

st.info(
    "Start on the **Dashboard** page and click *Run analysis pipeline* to ingest the "
    "log files, run correlation/failure detection, retrieve similar historical "
    "incidents, and generate Markdown incident reports."
)
