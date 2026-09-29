from __future__ import annotations

import copy
import difflib
import tempfile
from pathlib import Path

import typer

from . import __version__
from .config import load, write_default
from .copilot import ensure as ensure_copilot
from .frameworks import SUPPORTED, detect, discover
from .generator import generate_bundle
from .scaffold_generator import generate_tfscaffold_bundle
from .terragrunt_generator import generate_terragrunt_bundle

app = typer.Typer(help="Generate OKF v0.2 knowledge bundles from Terraform-family repositories.", no_args_is_help=True)


def _repo(path: Path) -> Path:
    return path.resolve()


def _generate(repo: Path, cfg: dict, out: Path):
    d, model = discover(repo, cfg)
    if d.framework == "tfscaffold":
        generate_tfscaffold_bundle(model, out, cfg)
    elif d.framework == "terragrunt":
        generate_terragrunt_bundle(model, out, cfg)
    else:
        generate_bundle(model, out, cfg)
    return d, model


def _apply_generate_overrides(
    cfg: dict,
    profile: str | None = None,
    include_ai: bool | None = None,
    ai_provider: str | None = None,
    ai_model: str | None = None,
    ai_base_url: str | None = None,
    ai_timeout_seconds: int | None = None,
) -> dict:
    out = copy.deepcopy(cfg)
    if profile:
        out["generation"]["profile"] = profile
    if include_ai is not None:
        out["ai"]["enabled"] = include_ai
    if ai_provider:
        out["ai"]["provider"] = ai_provider
    provider = out["ai"].get("provider", "ollama")
    if ai_model:
        out["ai"][provider]["model"] = ai_model
    if ai_base_url:
        out["ai"][provider]["base_url"] = ai_base_url
    if ai_timeout_seconds is not None:
        out["ai"][provider]["timeout_seconds"] = ai_timeout_seconds
    return out


@app.command()
def frameworks():
    """List supported repository frameworks."""
    typer.echo("Supported frameworks:")
    for f in SUPPORTED:
        typer.echo(f"  - {f}")


def discover_cmd(
    path: Path = typer.Argument(Path("."), exists=True, file_okay=False),
    framework: str = typer.Option("auto", "--framework", "-f"),
):
    """Detect the repository framework without changing files."""
    if framework not in SUPPORTED:
        raise typer.BadParameter(f"Choose one of: {', '.join(SUPPORTED)}")
    repo = _repo(path)
    cfg = load(repo)
    cfg["framework"]["type"] = framework
    d = detect(repo, cfg)
    typer.echo(f"Framework: {d.framework}")
    typer.echo(f"Confidence: {d.confidence}%")
    for r in d.reasons:
        typer.echo(f"  - {r}")


# command name should be discover rather than discover-cmd
app.command(name="discover")(discover_cmd)


@app.command()
def init(
    path: Path = typer.Argument(Path("."), exists=True, file_okay=False),
    framework: str = typer.Option("auto", "--framework", "-f"),
    force: bool = typer.Option(False, "--force"),
):
    """Initialise config, automatically detect/select framework, then create OKF and Copilot instructions."""
    if framework not in SUPPORTED:
        raise typer.BadParameter(f"Choose one of: {', '.join(SUPPORTED)}")
    repo = _repo(path)
    cfg_path = repo / ".tf2okf.yml"
    if cfg_path.exists() and not force:
        typer.echo(".tf2okf.yml already exists; preserving it (use --force to replace).")
    else:
        write_default(repo, framework)
        typer.echo(f"Created .tf2okf.yml (framework: {framework})")
    cfg = load(repo)
    # CLI selection overrides existing config for this init and is persisted when explicit.
    if framework != "auto":
        cfg["framework"]["type"] = framework
        import yaml

        cfg_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    out = repo / cfg["output"].get("directory", ".okf")
    d, model = _generate(repo, cfg, out)
    if cfg.get("copilot", {}).get("generate_instructions", True):
        ensure_copilot(repo, d.framework, force=force)
    typer.echo(f"Detected framework: {d.framework} ({d.confidence}% confidence)")
    for r in d.reasons:
        typer.echo(f"  - {r}")
    typer.echo(f"Generated OKF v0.2 bundle at {out.relative_to(repo)}")


@app.command()
def generate(
    path: Path = typer.Argument(Path("."), exists=True, file_okay=False),
    framework: str | None = typer.Option(None, "--framework", "-f"),
    profile: str | None = typer.Option(None, "--profile", help="Generation profile: full or compact"),
    include_ai: bool | None = typer.Option(
        None, "--include-ai/--no-include-ai", help="Include AI summaries in generated output."
    ),
    ai_provider: str | None = typer.Option(None, "--ai-provider", help="AI provider: ollama, claude, or openai."),
    ai_model: str | None = typer.Option(None, "--ai-model", help="AI model name for the selected provider."),
    ai_base_url: str | None = typer.Option(None, "--ai-base-url", help="Base URL for the selected AI provider."),
    ai_timeout_seconds: int | None = typer.Option(
        None, "--ai-timeout-seconds", min=1, help="AI request timeout in seconds."
    ),
):
    """Regenerate machine-owned OKF. --framework can override config for this run."""
    if profile and profile not in {"full", "compact"}:
        raise typer.BadParameter("Choose one of: full, compact")
    if ai_provider and ai_provider not in {"ollama", "claude", "openai"}:
        raise typer.BadParameter("Choose one of: ollama, claude, openai")
    repo = _repo(path)
    cfg = load(repo)
    if framework:
        if framework not in SUPPORTED:
            raise typer.BadParameter(f"Choose one of: {', '.join(SUPPORTED)}")
        cfg["framework"]["type"] = framework
    cfg = _apply_generate_overrides(
        cfg,
        profile,
        include_ai,
        ai_provider,
        ai_model,
        ai_base_url,
        ai_timeout_seconds,
    )
    out = repo / cfg["output"].get("directory", ".okf")
    d, model = _generate(repo, cfg, out)
    if cfg.get("copilot", {}).get("generate_instructions", True):
        ensure_copilot(repo, d.framework)
    summary = f"Generated {d.framework} OKF knowledge ({d.confidence}% detection confidence)."
    summary += f" Profile: {cfg.get('generation', {}).get('profile', 'full')}."
    if cfg.get("ai", {}).get("enabled", False):
        summary += f" AI summaries: enabled ({cfg.get('ai', {}).get('provider', 'ollama')})."
    typer.echo(summary)


@app.command()
def check(path: Path = typer.Argument(Path("."), exists=True, file_okay=False)):
    repo = _repo(path)
    cfg = load(repo)
    cfg = _apply_generate_overrides(cfg, include_ai=False)
    out = repo / cfg["output"].get("directory", ".okf")
    if not out.exists():
        typer.echo("OKF bundle is missing. Run tf2okf generate.", err=True)
        raise typer.Exit(1)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / ".okf"
        d, _ = _generate(repo, cfg, tmp)
        current = _snapshot(out / "generated")
        expected = _snapshot(tmp / "generated")
    if current != expected:
        typer.echo(f"{d.framework} knowledge drift detected. Run: tf2okf generate", err=True)
        for k in sorted(expected.keys() - current.keys()):
            typer.echo(f"  + {k}", err=True)
        for k in sorted(current.keys() - expected.keys()):
            typer.echo(f"  - {k}", err=True)
        for k in sorted(k for k in current.keys() & expected.keys() if current[k] != expected[k]):
            typer.echo(f"  ~ {k}", err=True)
        raise typer.Exit(1)
    typer.echo(f"OK: generated OKF matches {d.framework} sources.")


@app.command(name="diff")
def diff_cmd(path: Path = typer.Argument(Path("."), exists=True, file_okay=False)):
    repo = _repo(path)
    cfg = load(repo)
    cfg = _apply_generate_overrides(cfg, include_ai=False)
    out = repo / cfg["output"].get("directory", ".okf")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td) / ".okf"
        _generate(repo, cfg, tmp)
        keys = sorted(set(_files(out / "generated")) | set(_files(tmp / "generated")))
        any_diff = False
        for k in keys:
            a = out / "generated" / k
            b = tmp / "generated" / k
            at = _normalised_lines(a) if a.exists() else []
            bt = _normalised_lines(b) if b.exists() else []
            if at != bt:
                any_diff = True
                typer.echo("".join(difflib.unified_diff(at, bt, fromfile=f"a/{k}", tofile=f"b/{k}")), nl=False)
        if not any_diff:
            typer.echo("No generated OKF changes.")


@app.command()
def version():
    typer.echo(__version__)


def _files(root: Path):
    if not root.exists():
        return []
    return [
        p.relative_to(root).as_posix()
        for p in root.rglob("*.md")
        if not p.relative_to(root).as_posix().startswith("ai/")
    ]


def _normalised_lines(path: Path):
    import re

    text = path.read_text(encoding="utf-8")
    text = re.sub(r"(?m)^\s*at: ['\"]?[^\n'\"]+['\"]?\s*$", "  at: <timestamp>", text)
    return text.splitlines(keepends=True)


def _snapshot(root: Path):
    return {k: "".join(_normalised_lines(root / k)) for k in _files(root)}


if __name__ == "__main__":
    app()
