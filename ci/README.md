# Continuous Integration with GitHub Actions

## Background

GitHub Actions builds the following types of NVDA installers through a CI/CD pipeline:

* Pull Request builds: Generated from the pull requests.
Pull requests initiated from `nvaccess/nvda` rather than a fork have extra permissions than standard PRs.
* Snapshot builds: Generated from pushes to master/beta/rc or branch names prefixed with `try-`.
These are signed and deployed to the NV Access server.
* Tagged builds: Generated from pushes to tags prefixed with `release-`.
Official beta, rc and stable releases.
These are signed and deployed to the NV Access server.

## Builds

### Build process

The build process is non-linear.
Some of these steps run concurrently.

* Prepare source code and cache:
  * Checkout NVDA repository with submodules.
  * Install dependencies (or use cache).
  * Set version and scons variables.
  * Build NVDA source.
* Build and test:
  * Run static tests
  * Build launcher
  * Install NVDA
  * Run systems tests
* Deploy:
  * On tagged/snapshot builds, upload symbols to Mozilla
  * On beta branch builds, upload translation to Crowdin.
  * On snapshot builds, deploy to the server.
  * On release builds, publish the release on GitHub and deploy to the server.
* Clean up build cache.

### Build behaviours

Builds will fail if any command has a non-zero exit code.
PowerShell scripts continue on non-terminating errors unless the file is prefixed with `$ErrorActionPreference = "Stop";`.

## Setup requirements

Builds from PRs and pushes to master/beta/rc should work out of the box for forks.
You just need to enable GitHub Actions on your fork.

The following configuration is required only for more advanced development such as:

* signed builds
* Crowdin synchronisation
* publishing releases to a server

### Publisher name

Our releases are packaged with a publisher name.
To customise this, set:

* `PUBLISHER_NAME` as a variable.
It currently defaults to the repository owner (e.g. `nvaccess`).

### Build number offset

To offset from our previous build system, we start the sequential build count at a higher number than 0.
This means our first build will be numbered something like 100,001 not 1.

To offset build numbers, set;

* `BUILD_NUMBER_OFFSET` as a variable.
It currently defaults to 0.

### Crowdin

NVDA translations are synced with Crowdin on the beta branch.

To enable, set:

* `CROWDIN_PROJECT_ID` as a variable.
* `CROWDIN_AUTH_TOKEN` as a secret.

### Code signing

NV Access signs snapshot/tagged builds with SignPath.

To enable, set:

* `API_SIGNING_TOKEN` as a secret with your SignPath token.

### Uploading symbols

NVDA uploads its build symbols to Mozilla to help them with debugging on snapshot/tagged builds.

To enable, set:

* `MOZILLA_SYMS_TOKEN` as a secret.
* `feature_uploadSymbolsToMozilla` as a variable with any non-empty string.

Generating this requires direct co-ordination with Mozilla.

### GitHub Environments

GitHub Environments are used to protect deployments of snapshot/tagged builds.

Create two GitHub Environments, one called `production`, the other `snapshot`.

#### production

Used for tagged releases of NVDA.
It's recommended to enable deployment protection rules so that a human can confirm the deployment of a built tagged release staged for deployment.
This is so any desired testing can get manually confirmed, and communications for the release can be prepared.

Configuration:

* Name: `production`
* Enable required reviewers: this ensures a human must confirm deployment of a staged release
* Under "Deployment branches and tags", create a tag rule: `release-*`

#### snapshot

Configuration:

* Name: `snapshot`
* Do not enable required reviewers: this is not needed for snapshots.
* Under "Deployment branches and tags", create these branch rules:
  * `master`
  * `beta`
  * `rc`
  * `try-**`

### Deployment webhook

Create a GitHub webhook to subscribe to snapshot/tagged builds of NVDA, and use it to deploy to a server.

Under events, only subscribe to the Deployments event.

Ensure a secret is set and SSL is enabled.

### VirusTotal scanning

NV Access scans tagged builds with VirusTotal.

To ensure this step of tagged builds succeed, set:

* `VT_API_KEY` as a secret.

### GitHub Discussions category

This is only used when building tagged builds.
GitHub Discussions created for stable releases must go into a "Releases" category.
Discussions must be enabled in the repository.
Create a new discussion category with an "Announcement" type, and a category name of "Releases".
