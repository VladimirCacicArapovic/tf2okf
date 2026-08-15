# Threat model

## Assets
- repository source code and developer workstation files;
- generated OKF committed to version control;
- CI credentials and repository write permissions.

## Untrusted inputs
- repository paths and configuration;
- Terraform/HCL text;
- filenames and symlinks;
- optional `terraform-docs` output.

## Primary threats and mitigations
- **Path traversal / arbitrary overwrite:** all configured roots/output directories must resolve inside the repository.
- **Symlink escape:** symlinked Terraform source is ignored.
- **Secret propagation:** likely secret-bearing attributes are redacted; state/plans are never read; tfvars contents are not copied.
- **Resource exhaustion:** source file size limits and `terraform-docs` timeout/output caps are enforced.
- **Command injection:** external tools are executed with argument arrays and `shell=False` semantics.
- **CI token abuse:** sample workflows use least-privilege permissions and disable credential persistence where practical.
- **Generated-content overwrite:** only `.okf/generated/` is machine-owned; curated knowledge is preserved.

## Residual risks
Static secret detection is heuristic. A secret hard-coded under an innocuous attribute name can still appear in generated output. Repositories should use secret scanning and avoid hard-coded credentials. The lightweight HCL parser is not a Terraform evaluator and may miss complex expressions.
