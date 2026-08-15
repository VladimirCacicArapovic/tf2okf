---
okf_version: "0.2"
---

# tfscaffold Knowledge Bundle

This repository uses tfscaffold. Start with the generated component index, then read only the component or shared module relevant to the task.

## Generated knowledge

* [tfscaffold generated knowledge](generated/) - Components, shared modules, environment metadata and Terraform facts.

## Curated knowledge

* [Architecture](knowledge/architecture.md)
* [Security](knowledge/security.md)

## Source of truth

Terraform under `components/` and `modules/` remains the implementation source of truth. Environment/version values under `etc/` are indexed as configuration inputs.
