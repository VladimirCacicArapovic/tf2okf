from pathlib import Path

BASE = """# Repository knowledge instructions

This repository stores project knowledge in Open Knowledge Format (OKF) v0.2 under `.okf/`.

Before analysing or modifying infrastructure:

1. Read `.okf/index.md` and then the generated framework index.
2. Read only the OKF concepts relevant to the task; do not load the entire bundle by default.
3. Use `.okf/generated/` for deterministic facts extracted from infrastructure source.
4. Use `.okf/knowledge/` for human-curated architecture, security, decisions and operations.
5. Answer from OKF first. Do not read Terraform/Terragrunt source for routine questions when OKF already contains the needed facts.
6. Treat infrastructure source as the implementation source of truth, and read it only to resolve missing, ambiguous, or conflicting OKF details.
7. If source conflicts with OKF, report the discrepancy and regenerate OKF with `tf2okf generate`.
8. Minimize file reads: start with the smallest OKF set that can answer the question.
9. Avoid duplicate exploration across equivalent OKF and source files unless you are resolving a specific gap.
10. In answers, name the owning unit/module/component first and include concrete file paths for the likely edit points.
11. Prefer generated indexes to identify where to look; only drill into source after identifying the most relevant unit or module.
12. For change requests, explain both the likely Terraform/Terragrunt files to edit and the OKF files that justify that conclusion.
13. Ignore `.terraform/`, `.terragrunt-cache/`, `.terragrunt-stack/`, build outputs, and benchmark artifacts unless the task is explicitly about generated or cached content.
14. Treat generated OKF pages as discovery and routing aids; validate nuanced behavioral changes against source before proposing edits.
"""

EXTRA = {
    "plain-terraform": """
This repository uses **plain Terraform**.

For Terraform tasks:
- Start with `.okf/generated/index.md`, then read only the relevant generated pages.
- For variable questions, read `.okf/generated/inputs.md` first.
- For output or integration questions, read `.okf/generated/outputs.md` first.
- For provider or platform questions, read `.okf/generated/providers.md` first.
- For dependency or ownership questions, read `.okf/generated/dependencies.md`, then the relevant module or resource pages.
- After routing with OKF, inspect the owning Terraform root/module source only if details are missing or a code change is required.
""",
    "tfscaffold": """
This repository uses **tfscaffold**. Treat each `components/` child as an independent root module/state boundary. Use `.okf/generated/components/<component>/` first, then relevant shared-module knowledge. Environment/version tfvars are indexed separately.

For tfscaffold tasks:
- Identify the owning component in `.okf/generated/index.md` before reading source.
- For shared behavior, read `.okf/generated/shared-modules/<module>/` after the component summary.
- For IAM or access questions, prefer generated `iam-access.md` pages and curated knowledge such as `knowledge/iam-permissions.md`.
- For environment-specific questions, check generated environment/version inputs before reading `etc/` files.
""",
    "terragrunt": """
This repository uses **Terragrunt**. Treat each directory containing `terragrunt.hcl` as an independently operable unit. Use `.okf/generated/units/` and the Terragrunt dependency graph first. Follow `terraform.source`, `include`, and `dependency.config_path` relationships only as needed. Ignore generated `.terragrunt-cache/` and `.terragrunt-stack/` content unless explicitly required.

For Terragrunt tasks:
- Start with `.okf/generated/dependencies.md` to understand unit relationships.
- Read the relevant `.okf/generated/units/<unit>/index.md` page before opening `terragrunt.hcl`.
- For variable or output questions, prefer the generated local Terraform facts linked from the owning unit when available.
- For change requests, separate Terragrunt-layer edits (`terragrunt.hcl`, includes, dependency wiring) from Terraform-module edits (`terraform.source` targets).
""",
}


def ensure(repo: Path, framework: str = "plain-terraform", force: bool = False) -> bool:
    path = repo / ".github" / "copilot-instructions.md"
    if path.exists() and not force:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(BASE + EXTRA.get(framework, ""), encoding="utf-8")
    return True
