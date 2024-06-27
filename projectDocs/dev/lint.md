# Linting

## Lint overview

Our linting process involves running [Ruff](https://docs.astral.sh/ruff) to pick up linting issues and auto-apply fixes where possible.

## Lint integration

For faster lint results, or greater integration with your tools you may want to set up Ruff with your IDE.

## Pre-commit hooks

[Pre-commit hooks](https://pre-commit.com/) can be used to automatically run linting on files staged for commit.
From a shell, perform:

1. `venvUtils\ensureAndActivate.bat`
1. `pre-commit install`

Future commits will automatically apply linting.
