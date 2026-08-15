.PHONY: test lint typecheck security build check

test:
	pytest --cov=tf2okf --cov-report=term-missing
lint:
	ruff check src tests

typecheck:
	mypy src
security:
	bandit -q -r src
	pip-audit
build:
	python -m build
	python -m twine check dist/*
check: lint typecheck security test build
