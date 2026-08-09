"""Retrieve similar historical incidents for a given query, failure
pattern, or correlated event cluster.

Backs requirement 5: "Retrieve similar historical incidents using RAG."
Sits between the deterministic analysis/correlation outputs
(`FailurePattern`, `CorrelatedEvent`) and the (future) LLM-assisted
report/answer generation -- this module only does retrieval, no generation.
"""

from app.config import settings
from app.models.schemas import CorrelatedEvent, FailurePattern, RetrievedIncident
from app.vectorstore.faiss_store import FaissVectorStore


class IncidentRetriever:
    """Finds historical incidents similar to a current failure, correlated
    event cluster, or free-text query."""

    def __init__(self, vector_store: FaissVectorStore):
        self.vector_store = vector_store

    def retrieve_for_pattern(
        self, pattern: FailurePattern, top_k: int = settings.rag_top_k
    ) -> list[RetrievedIncident]:
        """Build a search query from a FailurePattern and return similar
        historical incidents."""
        return self.vector_store.search(self._pattern_query(pattern), top_k=top_k)

    def retrieve_for_correlated_event(
        self, event: CorrelatedEvent, top_k: int = settings.rag_top_k
    ) -> list[RetrievedIncident]:
        """Build a search query from a CorrelatedEvent (using its
        structured_evidence) and return similar historical incidents."""
        return self.vector_store.search(self._correlated_event_query(event), top_k=top_k)

    def retrieve_for_query(self, query: str, top_k: int = settings.rag_top_k) -> list[RetrievedIncident]:
        """Return similar historical incidents for a free-text query."""
        return self.vector_store.search(query, top_k=top_k)

    @staticmethod
    def _pattern_query(pattern: FailurePattern) -> str:
        services = ", ".join(pattern.affected_services)
        return f"{pattern.message}. Affected services: {services}. {pattern.description}"

    @staticmethod
    def _correlated_event_query(event: CorrelatedEvent) -> str:
        components = ", ".join(event.involved_components)
        messages = ", ".join(event.structured_evidence.distinct_messages)
        trigger = event.probable_trigger.message if event.probable_trigger else ""
        return f"Incident triggered by '{trigger}'. Involved components: {components}. Related messages: {messages}"
