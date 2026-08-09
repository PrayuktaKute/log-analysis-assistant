"""Thin wrapper around a FAISS index for storing and querying incident
embeddings.

Backs requirement 5: "Retrieve similar historical incidents using RAG."
Uses an exact `IndexFlatIP` (inner product) over L2-normalized embeddings
-- i.e. exact cosine similarity search. A knowledge base of historical
incidents is expected to be small/medium in size (hundreds to low
thousands of entries, not millions), so an approximate index (IVF/HNSW)
would be premature optimization; exact search is simpler, deterministic,
and fast enough at this scale.
"""

import json
from pathlib import Path
from typing import Optional

import faiss
import numpy as np
from loguru import logger

from app.config import settings
from app.embeddings.embedder import Embedder
from app.models.schemas import HistoricalIncident, RetrievedIncident


def _incident_text(incident: HistoricalIncident) -> str:
    """Build the text representation of an incident that gets embedded."""
    parts = [incident.title, incident.summary]
    if incident.root_cause:
        parts.append(incident.root_cause)
    if incident.tags:
        parts.append(", ".join(incident.tags))
    return ". ".join(part for part in parts if part)


class FaissVectorStore:
    """Manages a FAISS index of embedded HistoricalIncidents."""

    def __init__(
        self,
        index_path: Path = settings.faiss_index_path,
        dimension: int = settings.embedding_dimension,
        embedder: Optional[Embedder] = None,
    ):
        self.index_path = Path(index_path)
        self.dimension = dimension
        self.embedder = embedder or Embedder()
        self.index: Optional[faiss.Index] = None
        self._incidents: dict[int, HistoricalIncident] = {}  # FAISS row id -> incident

    @property
    def _meta_path(self) -> Path:
        return self.index_path.with_suffix(self.index_path.suffix + ".meta.json")

    def build_index(self, incidents: list[HistoricalIncident]) -> None:
        """Embed and add a batch of incidents, building the index from scratch."""
        self.index = faiss.IndexFlatIP(self.dimension)
        self._incidents = {}
        self.add(incidents)

    def add(self, incidents: list[HistoricalIncident]) -> None:
        """Embed and add incidents to the index, creating one if none exists yet."""
        if self.index is None:
            self.index = faiss.IndexFlatIP(self.dimension)
        if not incidents:
            return

        texts = [_incident_text(incident) for incident in incidents]
        vectors = np.array(self.embedder.embed_batch(texts), dtype="float32")

        start_id = self.index.ntotal
        self.index.add(vectors)
        for offset, incident in enumerate(incidents):
            self._incidents[start_id + offset] = incident

        logger.info("Added {} incident(s) to FAISS index (total={})", len(incidents), self.index.ntotal)

    def search(self, query: str, top_k: int = settings.rag_top_k) -> list[RetrievedIncident]:
        """Return the top_k most similar historical incidents to `query`."""
        if self.index is None or self.index.ntotal == 0:
            return []

        query_vector = np.array([self.embedder.embed_text(query)], dtype="float32")
        k = min(top_k, self.index.ntotal)
        scores, ids = self.index.search(query_vector, k)

        results: list[RetrievedIncident] = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue
            incident = self._incidents.get(int(idx))
            if incident is None:
                continue
            results.append(RetrievedIncident(incident=incident, similarity_score=float(score)))
        return results

    def save(self) -> None:
        """Persist the index and id-map to `self.index_path`."""
        if self.index is None:
            raise ValueError("No index to save -- call build_index() or add() first")

        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(self.index_path))

        meta = {str(idx): incident.model_dump(mode="json") for idx, incident in self._incidents.items()}
        self._meta_path.write_text(json.dumps(meta), encoding="utf-8")
        logger.info("Saved FAISS index ({} vectors) to {}", self.index.ntotal, self.index_path)

    def load(self) -> None:
        """Load a previously persisted index from `self.index_path`."""
        if not self.index_path.exists():
            raise FileNotFoundError(f"No FAISS index found at {self.index_path}")

        self.index = faiss.read_index(str(self.index_path))
        raw_meta = json.loads(self._meta_path.read_text(encoding="utf-8")) if self._meta_path.exists() else {}
        self._incidents = {int(idx): HistoricalIncident(**data) for idx, data in raw_meta.items()}
        logger.info("Loaded FAISS index ({} vectors) from {}", self.index.ntotal, self.index_path)
