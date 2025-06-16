# Continuous Integration with GitHub Actions

[Documentation about GitHub Actions](https://docs.github.com/en/actions)

## Builds

Builds will fail if any command has a non-zero exit code.
PowerShell scripts continue on non-terminating errors unless the file is prefixed with `$ErrorActionPreference = "Stop";`.

### Build process

1. Checkout NVDA repository with submodules.
1. Install dependencies (or use cache).
1. Set version and scons variables.
1. Prepare source code.
1. Build launcher.
1. Install NVDA.
1. Prepare for tests.
1. Run tests.
1. Clean up build cache.
1. Release NVDA if this is a tagged release.

## Testing

Before testing we:

* Create directories to store results.
* Install NVDA for system tests

The tests we perform are:

* check translation comments
* license checks
* unit tests
* system tests
  * each test suite (i.e. .robot file) must be manually included by:
    * adding a tag to `Force Tags` in the suite
    * adding the tag to `systemTests.strategy.matrix.testSuite` in the [CI script](../.github/workflows/testAndPublish.yml)

## Artifacts

* NVDA launcher.
* Test results.
