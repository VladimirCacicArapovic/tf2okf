from __future__ import annotations

import json
import os
from urllib import error, request
from urllib.parse import urlparse


def _validated_url(url: str, label: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise RuntimeError(f"{label} must use http or https.")
    return url


def _post_json(url: str, payload: dict, headers: dict[str, str], timeout_seconds: int) -> dict:
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(  # noqa: S310 - URL scheme validated before request construction.
        _validated_url(url, "AI endpoint URL"),
        data=data,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=timeout_seconds) as resp:  # noqa: S310 - URL scheme validated above.
            body = resp.read().decode("utf-8")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"AI provider HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Failed to reach AI provider at {url}: {exc.reason}") from exc

    try:
        result = json.loads(body)
    except json.JSONDecodeError as exc:
        raise RuntimeError("AI provider returned invalid JSON.") from exc
    if not isinstance(result, dict):
        raise RuntimeError("AI provider returned an unexpected response shape.")
    return result


def _required_env(env_name: str) -> str:
    value = os.environ.get(env_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {env_name}")
    return value


def _ollama_summary(prompt: str, settings: dict) -> tuple[str, str]:
    base_url = str(settings.get("base_url", "http://127.0.0.1:11434")).rstrip("/")
    model = str(settings.get("model", "llama3.1:8b"))
    timeout = int(settings.get("timeout_seconds", 30))
    payload = {"model": model, "prompt": prompt, "stream": False}
    result = _post_json(f"{base_url}/api/generate", payload, {}, timeout)
    text = result.get("response")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("Ollama response did not include a usable 'response' field.")
    return model, text.strip()


def _claude_summary(prompt: str, settings: dict) -> tuple[str, str]:
    base_url = str(settings.get("base_url", "https://api.anthropic.com")).rstrip("/")
    model = str(settings.get("model", "claude-3-5-haiku-latest"))
    timeout = int(settings.get("timeout_seconds", 60))
    api_key_env = str(settings.get("api_key_env", "ANTHROPIC_API_KEY"))
    api_key = _required_env(api_key_env)
    payload = {
        "model": model,
        "max_tokens": int(settings.get("max_tokens", 400)),
        "temperature": float(settings.get("temperature", 0.2)),
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {"x-api-key": api_key, "anthropic-version": str(settings.get("api_version", "2023-06-01"))}
    result = _post_json(f"{base_url}/v1/messages", payload, headers, timeout)
    content = result.get("content")
    if not isinstance(content, list):
        raise RuntimeError("Claude response did not include a usable 'content' list.")
    parts = [item.get("text", "") for item in content if isinstance(item, dict) and item.get("type") == "text"]
    text = "\n".join(part.strip() for part in parts if part.strip())
    if not text:
        raise RuntimeError("Claude response did not include any text content.")
    return model, text


def _openai_summary(prompt: str, settings: dict) -> tuple[str, str]:
    base_url = str(settings.get("base_url", "https://api.openai.com/v1")).rstrip("/")
    model = str(settings.get("model", "gpt-4.1-mini"))
    timeout = int(settings.get("timeout_seconds", 60))
    api_key_env = str(settings.get("api_key_env", "OPENAI_API_KEY"))
    api_key = _required_env(api_key_env)
    payload = {
        "model": model,
        "temperature": float(settings.get("temperature", 0.2)),
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {"Authorization": f"Bearer {api_key}"}
    result = _post_json(f"{base_url}/chat/completions", payload, headers, timeout)
    choices = result.get("choices")
    if not isinstance(choices, list) or not choices:
        raise RuntimeError("OpenAI response did not include any choices.")
    message = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
    text = message.get("content")
    if not isinstance(text, str) or not text.strip():
        raise RuntimeError("OpenAI response did not include usable message content.")
    return model, text.strip()


def generate_summary(prompt: str, config: dict) -> tuple[str, str, str]:
    ai_cfg = config.get("ai", {})
    provider = str(ai_cfg.get("provider", "ollama"))
    if provider == "ollama":
        model, text = _ollama_summary(prompt, ai_cfg.get("ollama", {}))
    elif provider == "claude":
        model, text = _claude_summary(prompt, ai_cfg.get("claude", {}))
    elif provider == "openai":
        model, text = _openai_summary(prompt, ai_cfg.get("openai", {}))
    else:
        raise ValueError(f"Unsupported ai.provider: {provider}")
    return provider, model, text
