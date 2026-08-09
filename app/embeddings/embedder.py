"""Embed text (incident summaries, failure-pattern descriptions, user
questions) into vectors for storage in / querying against the FAISS index.

Only the "sentence-transformers" provider (local, no external server) is
implemented here. An "ollama" embedding provider is intentionally left
unimplemented: it requires a running Ollama server, which this project
treats as part of "LLM integration" -- a separate, later phase from the
RAG retrieval plumbing built here.
"""

from functools import lru_cache

from loguru import logger

from app.config import settings


@lru_cache(maxsize=4)
def _load_sentence_transformer(model_name: str):
    """Lazily import and load a SentenceTransformer model, cached per model
    name so repeated Embedder instances don't reload the (slow-to-load)
    model from disk."""
    from sentence_transformers import SentenceTransformer

    logger.info("Loading sentence-transformers model '{}'", model_name)
    return SentenceTransformer(model_name)


class Embedder:
    """Produces embedding vectors for a given embedding provider."""

    def __init__(
        self,
        provider: str = settings.embedding_provider,
        model_name: str = settings.embedding_model_name,
    ):
        self.provider = provider
        self.model_name = model_name

    def embed_text(self, text: str) -> list[float]:
        """Embed a single string."""
        return self.embed_batch([text])[0]

    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """Embed a batch of strings. Vectors are L2-normalized so a FAISS
        inner-product index over them computes exact cosine similarity."""
        if self.provider != "sentence-transformers":
            raise NotImplementedError(
                f"Embedding provider '{self.provider}' is not implemented yet -- only "
                "'sentence-transformers' is supported until LLM integration (which will "
                "add the Ollama embedding provider)."
            )

        model = _load_sentence_transformer(self.model_name)
        vectors = model.encode(list(texts), convert_to_numpy=True, normalize_embeddings=True)
        return vectors.tolist()
