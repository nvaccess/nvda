`appveyor.yml` specifies build settings which generally [override online UI driven settings](https://www.appveyor.com/docs/build-configuration/#appveyoryml-and-ui-coexistence). 

# Branch and tag filtering

Tags and branches that trigger a build are filtered by [whitelisting](https://www.appveyor.com/docs/branches/#white--and-blacklisting). Despite the option name, filtering via `branches: only` is applied to tag names too.

# Build pipeline

For ordering of `appveyor.yml` phases, see: [build pipeline docs](https://www.appveyor.com/docs/build-configuration/#build-pipeline).

Builds will fail if any command has a non-zero exit code. PowerShell scripts continue on non-terminating errors unless the file is prefixed with `$ErrorActionPreference = "Stop";`.

## Setup process

Before we begin the install process, AppVeyor clones our repository and checks out the commit of the build. 

### `install`

* Set environment variables about the build version
* Bump up the AppVeyor build number
* Decrypt files to be used for signing builds and deployment using secure environment variables
* Update git submodules

### `build_script`

Performs a build of NVDA and related artifacts for testing and deployment.

* Set the scons variables
* Call scons to build from source
* Build the symbol store and package it to an artifact with 7zip

## Testing

Unlike the rest of the build, tests do not exit early if they fail or raise an error. If any test fails, `testFailExitCode` is set to 1. The `after_test` build phase will exit the build if any tests fail so that all test failures can be recorded where possible. 

Before testing we:

* Create directories for test output
* Set `testFailExitCode` to 0
* Install NVDA for system tests

The tests we perform are:

* check translation comments
* unit tests
* lint check
* system tests

## Artifacts

Artifacts are added to the build throughout the process. 

Artifacts in `output\*` and `output\*\*` are automatically packaged after successful tests. If something fails before then, we manually push these artifacts in `on_failure`. Artifacts outside of `output` are pushed manually as they are created. 

At the end of the build, regardless of failure, we upload the list of successfully installed python packages in `pushPackagingInfo.ps1`. This is performed here in case scons (partially) fails.

## Deploying

The server side deploy code (`nvdaAppveyorHook`) is triggered from `deployScript.ps1`. The server-side deployment relies on our artifacts, so they must be uploaded first.
