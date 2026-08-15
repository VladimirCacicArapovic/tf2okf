from pathlib import Path

BASE='''# Repository knowledge instructions

This repository stores project knowledge in Open Knowledge Format (OKF) v0.2 under `.okf/`.

Before analysing or modifying infrastructure:

1. Read `.okf/index.md` and then the generated framework index.
2. Read only the OKF concepts relevant to the task; do not load the entire bundle by default.
3. Use `.okf/generated/` for deterministic facts extracted from infrastructure source.
4. Use `.okf/knowledge/` for human-curated architecture, security, decisions and operations.
5. Treat infrastructure source as the implementation source of truth.
6. If source conflicts with OKF, report the discrepancy and regenerate OKF with `tf2okf generate`.
'''

EXTRA={
'plain-terraform': '''\nFor plain Terraform, inspect the relevant Terraform root/module after reading OKF.\n''',
'tfscaffold': '''\nThis repository uses **tfscaffold**. Treat each `components/` child as an independent root module/state boundary. Use `.okf/generated/components/<component>/` first, then relevant shared-module knowledge. Environment/version tfvars are indexed separately.\n''',
'terragrunt': '''\nThis repository uses **Terragrunt**. Treat each directory containing `terragrunt.hcl` as an independently operable unit. Use `.okf/generated/units/` and the Terragrunt dependency graph first. Follow `terraform.source`, `include`, and `dependency.config_path` relationships only as needed. Ignore generated `.terragrunt-cache/` and `.terragrunt-stack/` content unless explicitly required.\n'''
}

def ensure(repo: Path, framework: str='plain-terraform', force: bool=False) -> bool:
    path=repo/'.github'/'copilot-instructions.md'
    if path.exists() and not force: return False
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(BASE+EXTRA.get(framework,''),encoding='utf-8')
    return True
