from __future__ import annotations

import re
from pathlib import Path

MAX_SOURCE_BYTES = 2 * 1024 * 1024
MAX_SUBPROCESS_OUTPUT = 10 * 1024 * 1024
SECRET_KEY_RE = re.compile(
    r"(?i)(password|passwd|secret|token|api[_-]?key|private[_-]?key|client[_-]?secret|access[_-]?key|credential)"
)


class SecurityError(ValueError):
    pass


def ensure_within(root: Path, candidate: Path, *, label: str = "path") -> Path:
    root = root.resolve()
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise SecurityError(f"Unsafe {label}: {candidate} resolves outside repository root") from exc
    return resolved


def safe_repo_path(repo: Path, value: str, *, label: str) -> Path:
    p = Path(value)
    if p.is_absolute():
        raise SecurityError(f"Unsafe {label}: absolute paths are not allowed")
    return ensure_within(repo, repo / p, label=label)


def should_read(path: Path, repo: Path) -> bool:
    if path.is_symlink():
        return False
    try:
        ensure_within(repo, path, label="source path")
        return path.is_file() and path.stat().st_size <= MAX_SOURCE_BYTES
    except (OSError, SecurityError):
        return False


def redact_attribute(key: str, value: str) -> str:
    if SECRET_KEY_RE.search(key):
        return "<redacted-sensitive-value>"
    return value
