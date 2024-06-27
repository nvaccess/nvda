# Linting

## Lint overview

Our linting process involves running [Ruff](https://docs.astral.sh/ruff) to pick up linting issues and auto-apply fixes where possible.

## Lint integration

For faster lint results, or greater integration with your tools you may want to set up Ruff with your IDE.

## Pre-commit hooks

[Pre-commit hooks](https://pre-commit.com/) can be used to automatically run linting on files staged for commit.
This will automatically apply lint fixes where possible, otherwise cancelling the commit on lint issues.

From a shell, set up pre-commit scripts for your NVDA python environment:

1. `venvUtils\ensureAndActivate.bat`
1. `pre-commit install`

Alternatively, set up pre-commit scripts globally:

1. `pip install pre-commit`
1. `pre-commit install --allow-missing-config`
