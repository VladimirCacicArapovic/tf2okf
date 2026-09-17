# Changelog

## 0.6.0
- Added extracted IAM facts for `aws_iam_policy_document` and inline `aws_iam_policy` `jsonencode(...)` policies, including statement `Sid`, effects, actions, resources, principals, and direct group/role/user attachment hints.
- Added generated IAM access summary pages for plain Terraform and tfscaffold outputs, plus curated OKF scaffolding for task routing, IAM permissions, and AWS advisories.
- Added `examples/tfscaffold/components/iam-access` to exercise IAM-aware OKF generation and expanded conformance coverage for IAM extraction.

## 0.4.0
- Added security hardening for repository/output path containment.
- Added symlink and oversized-source protections.
- Added `terraform-docs` timeout/output limits.
- Added redaction of likely secret-bearing Terraform attributes.
- Added publication-grade CI, security, coverage, packaging, and malicious-input tests.
- Retained adapters for plain Terraform, tfscaffold, and Terragrunt.
