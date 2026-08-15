# tf2okf

`tf2okf` generates deterministic Open Knowledge Format v0.2 Markdown from Terraform-family repositories.

## Install and run

Requires Python 3.10 or newer.

```bash
python3.15 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install .
tf2okf --help
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
```

`auto` detects known framework signatures. Explicit selection always wins.

### tfscaffold adapter

Discovers independent `components/`, reusable `modules/`, and `etc/*.tfvars` environment metadata.

### Terragrunt adapter

Discovers each `terragrunt.hcl` unit, static `terraform.source`, `include`, `dependency.config_path`, shared HCL and `terragrunt.stack.hcl` files. `.terragrunt-cache` and generated `.terragrunt-stack` content are ignored.

### Plain Terraform adapter

Parses Terraform source directly from the configured root.

## Commands

- `init` — create configuration, detect/select framework, create initial OKF and Copilot instructions
- `discover` — show detected framework and reasons without changing files
- `generate` — regenerate machine-owned OKF
- `check` — fail when committed generated OKF has drifted
- `diff` — show generated knowledge diff
- `frameworks` — list supported adapters

No LLM is needed for generation.

## Security defaults

`tf2okf` is intentionally source-only: it does not read Terraform state, plans, cloud credentials, or execute Terraform. Repository-relative configuration paths are containment-checked; symlinked Terraform files are ignored; source files over 2 MiB are skipped; likely secret-bearing attributes are redacted; and optional `terraform-docs` execution has a timeout and captured-output limit. See `SECURITY.md` for the threat model.

## Open-source release checklist

Before publishing: enable GitHub private vulnerability reporting, branch protection/rulesets, required CI/CodeQL/dependency review checks, Dependabot security updates, secret scanning/push protection where available, and PyPI trusted publishing for the `pypi` environment. Run `python -m build && python -m twine check dist/*` locally or in CI.
