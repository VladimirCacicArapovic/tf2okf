# Architecture

tf2okf has four layers:
1. **framework detection/discovery**: selects plain Terraform, tfscaffold, or Terragrunt and builds an in-memory model;
2. **source parsing**: extracts deterministic infrastructure facts without evaluating Terraform or reading state;
3. **OKF generation**: writes machine-owned `.okf/generated/` and preserves `.okf/knowledge/`;
4. **consumer guidance**: optionally creates GitHub Copilot repository instructions pointing agents at the OKF index.

Framework support is adapter-oriented: framework discovery should be kept separate from OKF serialization so new frameworks do not fork the output contract.
