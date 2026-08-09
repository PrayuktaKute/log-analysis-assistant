"""Tests for app.llm.ollama_client.

Model resolution and retry/backoff logic are tested with the underlying
`ollama.Client`/`AsyncClient` methods mocked out (fast, deterministic, no
server required). A single live smoke test at the bottom exercises the
real local Ollama server and skips gracefully if it isn't reachable.
"""

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import httpx
import ollama
import pytest

from app.config import settings
from app.llm.ollama_client import OllamaClient, OllamaUnavailableError


def _client(**kwargs) -> OllamaClient:
    defaults = dict(base_url="http://localhost:11434", timeout_seconds=5, max_retries=3, retry_backoff_seconds=0)
    defaults.update(kwargs)
    return OllamaClient(**defaults)


def _fake_models(*names: str):
    return SimpleNamespace(models=[SimpleNamespace(model=n) for n in names])


# ---- resolve_model ----


def test_resolve_model_uses_configured_model_when_available():
    client = _client(model="llama3.1")
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest", "mistral:latest"))

    assert client.resolve_model() == "llama3.1"


def test_resolve_model_falls_back_when_configured_unavailable():
    client = _client(model="not-installed", fallback_models="qwen2.5,mistral")
    client._client.list = MagicMock(return_value=_fake_models("mistral:latest"))

    assert client.resolve_model() == "mistral"


def test_resolve_model_falls_back_to_configured_when_nothing_available():
    client = _client(model="not-installed", fallback_models="also-not-installed")
    client._client.list = MagicMock(return_value=_fake_models("something-else:latest"))

    assert client.resolve_model() == "not-installed"


def test_resolve_model_is_cached_after_first_call():
    client = _client(model="llama3.1")
    mock_list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._client.list = mock_list

    client.resolve_model()
    client.resolve_model()

    assert mock_list.call_count == 1


def test_resolve_model_degrades_gracefully_when_list_fails():
    client = _client(model="llama3.1")
    client._client.list = MagicMock(side_effect=httpx.ConnectError("refused"))

    assert client.resolve_model() == "llama3.1"


# ---- chat / retry (sync) ----


def test_chat_returns_content_on_success():
    client = _client(model="llama3.1")
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._client.chat = MagicMock(return_value=SimpleNamespace(message=SimpleNamespace(content="hello")))

    assert client.chat([{"role": "user", "content": "hi"}]) == "hello"


def test_chat_retries_on_transient_failure_then_succeeds():
    client = _client(model="llama3.1", max_retries=3, retry_backoff_seconds=0)
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._client.chat = MagicMock(
        side_effect=[httpx.ReadTimeout("timed out"), SimpleNamespace(message=SimpleNamespace(content="ok"))]
    )

    result = client.chat([{"role": "user", "content": "hi"}])

    assert result == "ok"
    assert client._client.chat.call_count == 2


def test_chat_raises_ollama_unavailable_after_exhausting_retries():
    client = _client(model="llama3.1", max_retries=2, retry_backoff_seconds=0)
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._client.chat = MagicMock(side_effect=httpx.ConnectError("refused"))

    with pytest.raises(OllamaUnavailableError):
        client.chat([{"role": "user", "content": "hi"}])

    assert client._client.chat.call_count == 2


def test_chat_does_not_retry_on_response_error():
    client = _client(model="llama3.1", max_retries=3, retry_backoff_seconds=0)
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._client.chat = MagicMock(side_effect=ollama.ResponseError("model not found"))

    with pytest.raises(ollama.ResponseError):
        client.chat([{"role": "user", "content": "hi"}])

    assert client._client.chat.call_count == 1  # a real API error isn't retried


# ---- achat / retry (async) ----


def test_achat_returns_content_on_success():
    client = _client(model="llama3.1")
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._async_client.chat = AsyncMock(return_value=SimpleNamespace(message=SimpleNamespace(content="hello")))

    result = asyncio.run(client.achat([{"role": "user", "content": "hi"}]))

    assert result == "hello"


def test_achat_retries_on_transient_failure_then_succeeds():
    client = _client(model="llama3.1", max_retries=3, retry_backoff_seconds=0)
    client._client.list = MagicMock(return_value=_fake_models("llama3.1:latest"))
    client._async_client.chat = AsyncMock(
        side_effect=[httpx.ReadTimeout("timed out"), SimpleNamespace(message=SimpleNamespace(content="ok"))]
    )

    result = asyncio.run(client.achat([{"role": "user", "content": "hi"}]))

    assert result == "ok"
    assert client._async_client.chat.call_count == 2


# ---- live smoke test (skips gracefully if Ollama isn't reachable) ----


def _ollama_reachable() -> bool:
    try:
        httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2)
        return True
    except httpx.HTTPError:
        return False


@pytest.mark.skipif(not _ollama_reachable(), reason="Ollama server not reachable at settings.ollama_base_url")
def test_live_chat_against_real_ollama_server():
    client = OllamaClient(model="llama3.2:3b", fallback_models="llama3.1,mistral", timeout_seconds=90, max_retries=2)

    reply = client.chat([{"role": "user", "content": "Reply with exactly the word: PONG"}])

    assert "PONG" in reply.upper()
