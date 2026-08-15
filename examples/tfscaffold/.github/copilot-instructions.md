# Repository knowledge instructions

This repository stores project knowledge in Open Knowledge Format (OKF) v0.2 under `.okf/`.

Before analysing or modifying infrastructure:

1. Read `.okf/index.md` and then the generated framework index.
2. Read only the OKF concepts relevant to the task; do not load the entire bundle by default.
3. Use `.okf/generated/` for deterministic facts extracted from infrastructure source.
4. Use `.okf/knowledge/` for human-curated architecture, security, decisions and operations.
5. Treat infrastructure source as the implementation source of truth.
6. If source conflicts with OKF, report the discrepancy and regenerate OKF with `tf2okf generate`.
7. Minimize file reads: start with the smallest OKF set that can answer the question.
8. Only read Terraform/Terragrunt source after OKF when details are missing, ambiguous, or conflicting.
9. Avoid duplicate exploration across equivalent OKF and source files unless you are resolving a specific gap.

This repository uses **tfscaffold**. Treat each `components/` child as an independent root module/state boundary. Use `.okf/generated/components/<component>/` first, then relevant shared-module knowledge. Environment/version tfvars are indexed separately.
