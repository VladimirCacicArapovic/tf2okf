# tf2okf

`tf2okf` generates deterministic Open Knowledge Format v0.2 Markdown from Terraform-family repositories.

## Install and run

Requires Python 3.10 or newer.

### Install from this repository (local source)

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m pip install .
tf2okf --help
```

### Install for use in other repositories

Install once, then run `tf2okf` from any Terraform/Terragrunt project.

If published on PyPI:

```bash
python3 -m pip install tf2okf
```

If not published on PyPI, install directly from Git:

```bash
python3 -m pip install "git+https://github.com/<owner>/tf2okf.git"
```

For isolated global CLI usage across projects (`pipx`):

```bash
pipx install "git+https://github.com/<owner>/tf2okf.git"
```

Common commands:

```bash
tf2okf frameworks
tf2okf discover .
tf2okf init .
tf2okf generate .
tf2okf check .
tf2okf diff .
```

Generation profiles and optional AI summaries:

```bash
# Smaller machine output (fewer heavy files, compact interfaces)
tf2okf generate . --profile compact

# Full output (default)
tf2okf generate . --profile full

# Optional AI summary generation
tf2okf generate . --include-ai --ai-provider ollama --ai-model llama3.1:8b
tf2okf generate . --include-ai --ai-provider claude --ai-model claude-3-5-haiku-latest
tf2okf generate . --include-ai --ai-provider openai --ai-model gpt-4.1-mini
```

Authentication:

- `ollama` - no API key; local server, default `http://127.0.0.1:11434`
- `claude` - set `ANTHROPIC_API_KEY`
- `openai` - set `OPENAI_API_KEY`

## Framework selection

```bash
tf2okf frameworks
tf2okf discover .
tf2okf init . --framework auto
tf2okf init . --framework tfscaffold
tf2okf init . --framework terragrunt
tf2okf init . --framework plain-terraform
```

Configuration:

```yaml
version: '2'
framework:
  type: auto
generation:
  profile: full   # full | compact
ai:
  enabled: false
  provider: ollama
  output_dir: generated/ai
  ollama:
    base_url: http://127.0.0.1:11434
    model: llama3.1:8b
    timeout_seconds: 30
  claude:
    base_url: https://api.anthropic.com
    model: claude-3-5-haiku-latest
    api_key_env: ANTHROPIC_API_KEY
    timeout_seconds: 60
  openai:
    base_url: https://api.openai.com/v1
    model: gpt-4.1-mini
    api_key_env: OPENAI_API_KEY
    timeout_seconds: 60
```

`auto` detects known framework signatures. Explicit selection always wins.

### tfscaffold adapter

Discovers independent `components/`, reusable `modules/`, and `etc/*.tfvars` environment metadata.
Each generated component page includes a preserved `Component description` block between `tf2okf:manual-description-start` and `tf2okf:manual-description-end`; edit only that block to keep your explanation through regeneration.

### Terragrunt adapter

Discovers each `terragrunt.hcl` unit, static `terraform.source`, `include`, `dependency.config_path`, shared HCL and `terragrunt.stack.hcl` files. `.terragrunt-cache` and generated `.terragrunt-stack` content are ignored.

### Plain Terraform adapter

Parses Terraform source directly from the configured root.

## Curated knowledge examples

The generated bundle keeps human-written context under `.okf/knowledge/`. Typical starting points:

**`architecture.md`**

```md
---
type: Architecture Knowledge
title: Architecture
description: Human-curated architecture and design intent.
tags:
  - architecture
  - manual
---

# Architecture

## System purpose

This repository provisions the shared network, security, and application runtime for the platform.

## Main building blocks

- `components/network` creates the VPC and shared subnets.
- `components/security` creates ALB and application security groups.
- `components/app` deploys the ECS service behind the ALB.

## Important boundaries

- Each `components/` directory is an independent state boundary.
- Shared modules under `modules/` must stay reusable and environment-agnostic.

## Design rules

- Network outputs are consumed by security and application layers.
- Security outputs are consumed by application components.
- Manual architectural decisions belong here, not in generated files.
```

**`security.md`**

```md
---
type: Security Knowledge
title: Security
description: Human-curated security constraints and rationale.
tags:
  - security
  - manual
---

# Security

## Security goals

- Prevent public access to private workloads.
- Keep secrets out of generated OKF and committed source.
- Make network exposure explicit at component boundaries.

## Required controls

- Only ALB-facing security groups may allow internet ingress.
- Application tasks must run in private subnets.
- Sensitive Terraform inputs and outputs must be redacted in generated docs.

## Operational expectations

- Review `.okf/generated/topology.md` after infrastructure changes.
- Regenerate OKF after changing inputs, outputs, dependencies, or module composition.
- Treat Terraform source as the implementation source of truth when curated knowledge and generated knowledge diverge.
```

## Commands

- `init` — create configuration, detect/select framework, create initial OKF and Copilot instructions
- `discover` — show detected framework and reasons without changing files
- `generate` — regenerate machine-owned OKF
- `generate --include-ai --ai-provider ...` — add optional AI summaries using Ollama, Claude, or OpenAI
- `check` — fail when committed generated OKF has drifted
- `diff` — show generated knowledge diff
- `frameworks` — list supported adapters

No LLM is required for deterministic OKF generation. AI summaries are optional and only used when `--include-ai` or `ai.enabled: true` is set.

## Security defaults

`tf2okf` is intentionally source-only: it does not read Terraform state, plans, cloud credentials, or execute Terraform. Repository-relative configuration paths are containment-checked; symlinked Terraform files are ignored; source files over 2 MiB are skipped; likely secret-bearing attributes are redacted; and optional `terraform-docs` execution has a timeout and captured-output limit. See `SECURITY.md` for the threat model.

## Open-source release checklist

Before publishing: enable GitHub private vulnerability reporting, branch protection/rulesets, required CI/CodeQL/dependency review checks, Dependabot security updates, secret scanning/push protection where available, and PyPI trusted publishing for the `pypi` environment. Run `python -m build && python -m twine check dist/*` locally or in CI. See `docs/pypi-release.md` for the workflow and setup details.
