from __future__ import annotations

import copy
from pathlib import Path

import yaml

from .security import safe_repo_path

DEFAULT = {
    "version": "2",
    "framework": {"type": "auto"},
    "terraform": {"root": ".", "recursive_modules": True},
    "tfscaffold": {
        "components_dir": "components",
        "modules_dir": "modules",
        "variables_dir": "etc",
        "include_components": ["*"],
        "include_modules": True,
    },
    "terragrunt": {"ignore_dirs": [".git", ".terraform", ".terragrunt-cache", ".terragrunt-stack", ".okf"]},
    "sources": {"terraform": True, "terraform_docs": True, "readme": True},
    "output": {"directory": ".okf"},
    "generation": {
        "profile": "full",
        "resources": True,
        "modules": True,
        "dependencies": True,
        "inputs": True,
        "outputs": True,
        "providers": True,
    },
    "knowledge": {"preserve_manual_files": True},
    "copilot": {"generate_instructions": True},
    "ai": {
        "enabled": False,
        "provider": "ollama",
        "output_dir": "generated/ai",
        "ollama": {"base_url": "http://127.0.0.1:11434", "model": "llama3.1:8b", "timeout_seconds": 30},
        "claude": {
            "base_url": "https://api.anthropic.com",
            "model": "claude-3-5-haiku-latest",
            "api_key_env": "ANTHROPIC_API_KEY",
            "api_version": "2023-06-01",
            "timeout_seconds": 60,
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4.1-mini",
            "api_key_env": "OPENAI_API_KEY",
            "timeout_seconds": 60,
        },
    },
    "security": {"redact_sensitive_attributes": True},
}


def _merge(base: dict, raw: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in raw.items():
        out[k] = _merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def validate(repo: Path, cfg: dict) -> dict:
    framework = (cfg.get("framework") or {}).get("type", "auto")
    if framework not in {"auto", "plain-terraform", "tfscaffold", "terragrunt"}:
        raise ValueError(f"Unsupported framework: {framework}")
    profile = (cfg.get("generation") or {}).get("profile", "full")
    if profile not in {"full", "compact"}:
        raise ValueError("generation.profile must be one of: full, compact")
    provider = (cfg.get("ai") or {}).get("provider", "ollama")
    if provider not in {"ollama", "claude", "openai"}:
        raise ValueError("ai.provider must be one of: ollama, claude, openai")
    safe_repo_path(repo, str((cfg.get("output") or {}).get("directory", ".okf")), label="output.directory")
    safe_repo_path(repo, str((cfg.get("terraform") or {}).get("root", ".")), label="terraform.root")
    ai_out = str((cfg.get("ai") or {}).get("output_dir", "generated/ai"))
    safe_repo_path(repo, ai_out, label="ai.output_dir")
    for key in ("components_dir", "modules_dir", "variables_dir"):
        value = str((cfg.get("tfscaffold") or {}).get(key, ""))
        if value:
            safe_repo_path(repo, value, label=f"tfscaffold.{key}")
    return cfg


def load(repo: Path) -> dict:
    path = repo / ".tf2okf.yml"
    if not path.exists():
        return validate(repo, copy.deepcopy(DEFAULT))
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError(".tf2okf.yml must contain a YAML mapping")
    mode = (raw.get("layout") or {}).get("mode")
    if mode and "framework" not in raw:
        raw["framework"] = {"type": {"terraform": "plain-terraform"}.get(mode, mode)}
    return validate(repo, _merge(DEFAULT, raw))


def write_default(repo: Path, framework: str = "auto") -> None:
    cfg = copy.deepcopy(DEFAULT)
    cfg["framework"]["type"] = framework
    (repo / ".tf2okf.yml").write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
