# Contributing

1. Fork the repository and create a focused branch.
2. Install development dependencies: `python -m pip install -e '.[dev]'`.
3. Run `ruff check .`, `mypy src`, `pytest --cov=tf2okf --cov-fail-under=85`, and `bandit -q -r src`.
4. Add tests for every behaviour change, including framework fixtures when relevant.
5. Keep generated OKF deterministic apart from `generated.at` timestamps.
6. Do not add network calls or cloud/state access to core generation without a security design discussion.

All contributions must pass CI and follow the Code of Conduct.
