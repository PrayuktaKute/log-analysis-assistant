"""Deterministic log analysis: grouping, severity/component analytics,
failure-pattern and correlation support data, timeline, and statistics.

Nothing in this package calls an LLM, uses embeddings, or does retrieval --
it operates purely on the structured `LogEntry` objects produced by
`app.ingestion`.
"""
