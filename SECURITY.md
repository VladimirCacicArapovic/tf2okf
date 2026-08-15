# Security Policy

## Supported versions
Security fixes are provided for the latest released minor version.

## Reporting a vulnerability
Please do **not** open a public issue for a suspected vulnerability. Use GitHub's private vulnerability reporting for this repository, or contact the maintainers through the private security contact configured for the project.

Include reproduction steps, affected version, impact, and any proposed mitigation. Maintainers should acknowledge reports promptly and coordinate disclosure after a fix is available.

## Security model
`tf2okf` is a source-code documentation generator. It does not require Terraform state, cloud credentials, network access, or execution of Terraform configuration.

Security boundaries:
- repository-relative paths are validated and output cannot escape the repository;
- symlinked Terraform source is ignored by default;
- individual source files larger than 2 MiB are skipped;
- `terraform-docs` is optional, invoked without a shell, limited to 30 seconds, and its captured output is capped;
- likely secret-bearing Terraform attributes are redacted from generated Markdown;
- `.tfvars` files are indexed by path/name only; their values are not copied into OKF;
- generated content is written only under the configured OKF output directory;
- `.okf/knowledge/` is never overwritten by normal regeneration.

Do not treat generated OKF as a secret store. Never commit credentials, private keys, tokens, Terraform state, or sensitive plans to the repository.
