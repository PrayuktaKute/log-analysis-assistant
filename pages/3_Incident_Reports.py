"""Incident Reports page: browse and download generated Markdown reports."""

import streamlit as st

from app.config import settings
from app.logging_config import configure_logging

configure_logging()

st.set_page_config(page_title="Incident Reports - Log Analysis Assistant", page_icon="📄", layout="wide")
st.title("📄 Incident Reports")

reports_dir = settings.reports_output_dir
reports_dir.mkdir(parents=True, exist_ok=True)

report_files = sorted(reports_dir.glob("*.md"))

if not report_files:
    st.write(
        f"No reports found in `{reports_dir}` yet. Run the pipeline from the "
        "Dashboard page to generate incident reports."
    )
else:
    selected = st.selectbox("Select a report", options=report_files, format_func=lambda p: p.name)
    if selected:
        content = selected.read_text(encoding="utf-8")
        st.download_button("Download Markdown", data=content, file_name=selected.name)
        st.markdown(content)
