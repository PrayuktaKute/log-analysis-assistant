"""Thin wrapper around the local Ollama LLM: sync + async chat, model
resolution with fallback, retry-with-backoff, and timeout handling.

Every other module that needs LLM generation should go through this client
rather than importing `ollama` directly, so model/host/timeout/retry
behavior stay centrally configurable (see `Settings.ollama_*`).
"""

import asyncio
import time
from typing import Any, Optional, Union

import httpx
import ollama
from loguru import logger

from app.config import settings

# Only network/transport-level failures are worth retrying -- a timeout or
# dropped connection might succeed on the next attempt. `ollama.ResponseError`
# means the server responded and said something is wrong (bad model name,
# bad request); retrying an unchanged request won't fix that, so it is
# deliberately NOT in this set and propagates on the first attempt.
_RETRYABLE_EXCEPTIONS = (httpx.HTTPError, ConnectionError, TimeoutError)


class OllamaUnavailableError(RuntimeError):
    """Raised when Ollama could not be reached after all retry attempts."""


class OllamaClient:
    """Wraps chat calls to a local Ollama server, with model resolution,
    retries, and timeout handling."""

    def __init__(
        self,
        base_url: str = settings.ollama_base_url,
        model: str = settings.ollama_model,
        fallback_models: str = settings.ollama_fallback_models,
        timeout_seconds: int = settings.ollama_timeout_seconds,
        max_retries: int = settings.ollama_max_retries,
        retry_backoff_seconds: float = settings.ollama_retry_backoff_seconds,
        temperature: float = settings.ollama_temperature,
    ):
        self.base_url = base_url
        self.requested_model = model
        self.fallback_models = [m.strip() for m in fallback_models.split(",") if m.strip()]
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.retry_backoff_seconds = retry_backoff_seconds
        self.temperature = temperature

        self._client = ollama.Client(host=base_url, timeout=timeout_seconds)
        self._async_client = ollama.AsyncClient(host=base_url, timeout=timeout_seconds)
        self._resolved_model: Optional[str] = None

    def resolve_model(self) -> str:
        """Return the model name to actually use: the configured model if
        it's available on the server, else the first available entry in
        `fallback_models`, else the configured model unchanged (letting a
        real call fail with a clear server-side error rather than guessing
        further). Cached per client instance after the first resolution.
        """
        if self._resolved_model is not None:
            return self._resolved_model

        candidates = [self.requested_model, *self.fallback_models]
        try:
            available = {m.model for m in self._client.list().models if m.model}
        except _RETRYABLE_EXCEPTIONS as exc:
            logger.warning(
                "Could not list Ollama models ({}); using configured model '{}' unchecked", exc, self.requested_model
            )
            self._resolved_model = self.requested_model
            return self._resolved_model

        for candidate in candidates:
            if self._model_available(candidate, available):
                if candidate != self.requested_model:
                    logger.warning(
                        "Configured model '{}' not available on Ollama server; falling back to '{}'",
                        self.requested_model,
                        candidate,
                    )
                self._resolved_model = candidate
                return candidate

        logger.warning(
            "None of the configured/fallback models {} are available on the Ollama server (has: {}); "
            "using '{}' unchecked",
            candidates,
            sorted(available),
            self.requested_model,
        )
        self._resolved_model = self.requested_model
        return self._resolved_model

    @staticmethod
    def _model_available(candidate: str, available: set[str]) -> bool:
        if candidate in available:
            return True
        # "llama3.1" (no tag) should match an installed "llama3.1:latest".
        return any(name.split(":")[0] == candidate for name in available)

    def chat(self, messages: list[dict[str, str]], format: Union[str, dict, None] = None) -> str:
        """Synchronous multi-turn chat completion. Returns the assistant's
        raw text content."""
        model = self.resolve_model()

        def _call() -> str:
            response = self._client.chat(
                model=model,
                messages=messages,
                format=format,
                options={"temperature": self.temperature},
            )
            return response.message.content or ""

        return self._with_retry(_call, description=f"chat(model={model})")

    async def achat(self, messages: list[dict[str, str]], format: Union[str, dict, None] = None) -> str:
        """Async multi-turn chat completion. Returns the assistant's raw
        text content."""
        model = self.resolve_model()

        async def _call() -> str:
            response = await self._async_client.chat(
                model=model,
                messages=messages,
                format=format,
                options={"temperature": self.temperature},
            )
            return response.message.content or ""

        return await self._awith_retry(_call, description=f"achat(model={model})")

    def _with_retry(self, fn: Any, description: str) -> str:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return fn()
            except _RETRYABLE_EXCEPTIONS as exc:
                last_exc = exc
                logger.warning(
                    "Ollama call failed ({}), attempt {}/{}: {}", description, attempt, self.max_retries, exc
                )
                if attempt < self.max_retries:
                    time.sleep(self.retry_backoff_seconds * attempt)
        raise OllamaUnavailableError(
            f"Ollama call failed after {self.max_retries} attempt(s): {last_exc}"
        ) from last_exc

    async def _awith_retry(self, fn: Any, description: str) -> str:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self.max_retries + 1):
            try:
                return await fn()
            except _RETRYABLE_EXCEPTIONS as exc:
                last_exc = exc
                logger.warning(
                    "Ollama call failed ({}), attempt {}/{}: {}", description, attempt, self.max_retries, exc
                )
                if attempt < self.max_retries:
                    await asyncio.sleep(self.retry_backoff_seconds * attempt)
        raise OllamaUnavailableError(
            f"Ollama call failed after {self.max_retries} attempt(s): {last_exc}"
        ) from last_exc
