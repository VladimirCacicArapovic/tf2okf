import json

import pytest

from tf2okf.ai import generate_summary
from tf2okf.config import load


class _FakeResponse:
    def __init__(self, payload: dict):
        self._payload = payload

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_load_accepts_claude_provider(tmp_path):
    (tmp_path / ".tf2okf.yml").write_text("ai:\n  provider: claude\n")
    cfg = load(tmp_path)
    assert cfg["ai"]["provider"] == "claude"


def test_load_accepts_openai_provider(tmp_path):
    (tmp_path / ".tf2okf.yml").write_text("ai:\n  provider: openai\n")
    cfg = load(tmp_path)
    assert cfg["ai"]["provider"] == "openai"


def test_generate_summary_uses_ollama(monkeypatch):
    def fake_urlopen(req, timeout):
        assert req.full_url == "http://127.0.0.1:11434/api/generate"
        return _FakeResponse({"response": "ollama result"})

    monkeypatch.setattr("tf2okf.ai.request.urlopen", fake_urlopen)
    provider, model, text = generate_summary(
        "hello", {"ai": {"provider": "ollama", "ollama": {"model": "llama3.1:8b"}}}
    )
    assert provider == "ollama"
    assert model == "llama3.1:8b"
    assert text == "ollama result"


def test_generate_summary_uses_claude(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    def fake_urlopen(req, timeout):
        assert req.full_url == "https://api.anthropic.com/v1/messages"
        assert req.headers["X-api-key"] == "test-key"
        return _FakeResponse({"content": [{"type": "text", "text": "claude result"}]})

    monkeypatch.setattr("tf2okf.ai.request.urlopen", fake_urlopen)
    provider, model, text = generate_summary(
        "hello", {"ai": {"provider": "claude", "claude": {"model": "claude-3-5-haiku-latest"}}}
    )
    assert provider == "claude"
    assert model == "claude-3-5-haiku-latest"
    assert text == "claude result"


def test_generate_summary_uses_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_urlopen(req, timeout):
        assert req.full_url == "https://api.openai.com/v1/chat/completions"
        assert req.headers["Authorization"] == "Bearer test-key"
        return _FakeResponse({"choices": [{"message": {"content": "openai result"}}]})

    monkeypatch.setattr("tf2okf.ai.request.urlopen", fake_urlopen)
    provider, model, text = generate_summary(
        "hello", {"ai": {"provider": "openai", "openai": {"model": "gpt-4.1-mini"}}}
    )
    assert provider == "openai"
    assert model == "gpt-4.1-mini"
    assert text == "openai result"


def test_generate_summary_requires_api_key_env(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        generate_summary("hello", {"ai": {"provider": "openai", "openai": {}}})
