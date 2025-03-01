# Continuous Integration with GitHub Actions

[Documentation about GitHub Actions](https://docs.github.com/en/actions)

## Builds

Builds will fail if any command has a non-zero exit code. PowerShell scripts continue on non-terminating errors unless the file is prefixed with `$ErrorActionPreference = "Stop";`.

### Build process
1. Checkout NVDA repository.
1. Set version and scons variables.
1. Prepare source code.
1. Build launcher.
1. Install NVDA.
1. Prepare for tests.

## Testing

Unlike the rest of the build, tests do not exit early if they fail or raise an error. If any test fails, `testFailExitCode` is set to 1. The `after_test` build phase will exit the build if any tests fail so that all test failures can be recorded where possible.

Before testing we:

* Create directories to store results.
* Install NVDA for system tests

The tests we perform are:

* check translation comments
* unit tests
* system tests

## Artifacts
- NVDA launcher.
* Tests results.
- If tests fail, the job summary of GitHub Actions.
