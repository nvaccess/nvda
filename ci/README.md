# Continuous Integration with GitHub Actions

Information in this file pertains both to NV Access, and to forks of NVDA that wish to enable automated builds.

## Background

GitHub Actions builds the following types of NVDA installers through a CI/CD pipeline:

* Pull Request builds: Generated from pull requests.
Pull requests initiated from `nvaccess/nvda` rather than a fork have greater permissions than standard PRs.
* Snapshot builds: Generated from pushes to master/beta/rc or branch names prefixed with `try-`.
These are signed and deployed to the NV Access server.
* Tagged builds: Generated from pushes to tags prefixed with `release-`.
Official beta, rc and stable releases, which are signed and deployed to the NV Access server.

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
  * Run system tests
* Deploy:
  * On tagged/snapshot builds, upload symbols to Mozilla
  * On snapshot builds, deploy to the server.
  * On beta branch builds, upload translation to Crowdin.
  * On release builds, publish the release on GitHub and deploy to the server.
* Clean up build cache.

### Build behaviours

Builds will fail if any command has a non-zero exit code.
PowerShell scripts continue on non-terminating errors unless the file is prefixed with `$ErrorActionPreference = "Stop";`.

## Fork setup requirements

Builds from PRs and pushes to master/beta/rc should work out of the box for forks.
However, you will need to enable GitHub Actions on your fork.
To do this, go to `https://github.com/YOUR_USER_NAME/YOUR_FORK_REPO/actions`.
Select "I understand my workflows, go ahead and enable them".

You should check which workflows are enabled, and which are disabled; they may not all be enabled by default when you perform the above step.
At least initially, the only workflows a fork is likely to want enabled for standard building of NVDA, are: `codeql.yml`, `clearCaches.yml`, and `testAndPublish.yml`.

If you are using the GitHub CLI, and you plan to use PRs to trigger NVDA to build instead of pushing to master/beta/rc, you may want those PRs to target your fork instead of nvaccess/nvda.
To do this by default, run the following:

```sh
gh repo set-default YOUR_USER_NAME/YOUR_FORK_REPO_NAME
```

## Advanced setup (optional for forks)

The following configuration is required only for more advanced development such as:

* signed builds
* Crowdin synchronisation
* publishing releases to a server
* email notifications
* auto-assigning milestones

### Publisher name

Our releases are packaged with a publisher name.
To customise this, set:

* `PUBLISHER_NAME` as a variable.
It currently defaults to the repository owner (e.g. `nvaccess`).

### Build number offset

To offset from our previous build system, we start the sequential build count at a higher number than 0.
This means our first build will be numbered something like 100,001 not 1.

To offset build numbers, set:

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

### Email notifications

You can send out email notifications to various email lists when certain changes are made.
Currently, notifications are only sent to a translators list, when localisation file changes occur or have syntax errors.

To enable, set:

* `EMAIL_USERNAME` as a secret.
* `EMAIL_PASSWORD` as a secret.
* `EMAIL_SERVER_ADDRESS` as a secret.
* `EMAIL_SERVER_PORT` optionally, as a secret, with 465 being the default if unset.

### Automatically assign milestone on PR merge

There is a workflow to assign a milestone to the PR, when a PR is merged.

To enable, set:

* `MILESTONE_ID` as a variable with the milestone number.
You can get this from the end of the URL when you visit the milestone.

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

To ensure this step of tagged builds succeeds, set:

* `VT_API_KEY` as a secret.

### GitHub Discussions category

This is only used when building tagged builds.
GitHub Discussions created for stable releases must go into a "Releases" category.
Discussions must be enabled in the repository.
Create a new discussion category with an "Announcement" type, and a category name of "Releases".
