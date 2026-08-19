# PyPI release workflow

This repository publishes to PyPI through GitHub Actions using PyPI Trusted Publishing.

## Workflow file

The release workflow lives at:

```bash
.github/workflows/publish.yml
```

It runs when:

- a GitHub Release is published
- the workflow is started manually with `workflow_dispatch`

## What the workflow does

1. checks out the repository
2. sets up Python 3.13
3. installs `build` and `twine`
4. builds source and wheel distributions with `python -m build`
5. validates metadata with `python -m twine check dist/*`
6. publishes to PyPI using `pypa/gh-action-pypi-publish`

## Required GitHub setup

Configure a GitHub Actions environment named:

```bash
pypi
```

The workflow already targets that environment.

## Required PyPI setup

In PyPI, configure Trusted Publishing for this repository.

Recommended settings:

- **Owner**: your GitHub org or user
- **Repository**: `tf2okf`
- **Workflow name**: `Publish to PyPI`
- **Environment name**: `pypi`

## Release flow

### Option 1: publish from a GitHub Release

1. bump the version in `pyproject.toml`
2. update `CHANGELOG.md`
3. merge to your release branch
4. create and publish a GitHub Release matching the version tag
5. GitHub Actions publishes the package to PyPI

### Option 2: manual publish from Actions

1. bump the version in `pyproject.toml`
2. push the changes
3. open the GitHub Actions tab
4. run `Publish to PyPI` manually

## Local preflight check

Before publishing, you can verify the package locally:

```bash
python3 -m pip install --upgrade pip build twine
python3 -m build
python3 -m twine check dist/*
```

## Notes

- This workflow uses OIDC Trusted Publishing, so no PyPI API token secret is required.
- The PyPI project URL in the workflow is set to `https://pypi.org/project/tf2okf/`.
- If the package name changes, update both the workflow URL and the PyPI project configuration.
