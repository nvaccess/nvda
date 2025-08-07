# Release Process

This document provides rough guidelines for the process of developing NVDA releases.
All current and potential developers, add-on developers and translators should read and follow this document.
These guidelines may be broken under special circumstances.
Any concerns should be discussed via [GitHub Discussion](https://github.com/nvaccess/nvda/discussions), issue or pull request.

## Release Workflow
This is the general release workflow.
Information for specific community groups is provided in later sections.
The production of a release consists of the following:
1. [Alpha Phase](#alpha-phase) (~7 weeks)
    - Development is done in parallel to the release process for the prior version once beta phase begins.
    - e.g. NVDA 2020.2 is in alpha while NVDA 2020.1 is going from beta to the final release.
    - The add-on API for the release is unstable.
    Add-ons targeting this release should use "dev" channel.
1. [Beta phase](#beta-phase) (~4 weeks)
    - Beta1 is released 1 week after the most recent final release.
    There is an exception for `20XX.1` releases.
    The first `20XX.1` beta release will occur when all planned API breaking changes have been made.
    - A new beta is released weekly as required
    - Translations should be relatively stable.
    Translators may wish to start working on the release, however further changes to translation strings will occur.
    - The add-on API should be relatively stable.
    Add-on authors may wish to start testing the new API, however further changes to the API may occur.
    Add-ons targeting this release should use "dev" or "beta" channel.
1. [Release candidate phase](#Release-Candidate-phase) (~3 weeks)
    - Once a beta has been stable for one week (no issues reported), the 2 week [translation freeze begins](#translatable-string-freeze).
    There should be no further translatable string changes, unless, if required, another freeze will be announced.
    - Once the translation freeze ends, [a release candidate (RC)](#release-candidate) is created.
    - A new RC is released weekly as required.
    The final RC should be identical to the final release.
    - The add-on API for RC should be stable.
    Add-ons targeting this release can use "stable" channel.
1. Final release
    - When an RC has been stable for one week (no issues reported), the final release is created
    - If required, a [follow up patch release](#patch-release) may occur.

### Alpha phase
* Contributions are made following the [dev contributing guide](../dev/contributing.md).
* Once a pull request has been reviewed and approved by at least one NV Access employee and all relevant build checks have passed, NV Access will squash merge the pull request into master.
* If the merging of a pull request to `master` causes any build checks on `master` to fail, the pull request is reverted without question.
This is however unlikely to be an issue as build checks on the pull request itself must have already passed.
* If a merged pull request has been identified as causing a regression, new bug, or does not work as originally reported, the pull request may be reverted at the discretion of the lead developers. Reasons in favor of not reverting the pull request may be:
  * The pull request was submitted by an active collaborator who is likely to follow up with a suitable pull request to address the issues.
  * The bug is trivial enough to be fixed by a collaborator.
  * Use the [PR revert template](../../.github/PULL_REQUEST_TEMPLATE/revert.md) when reverting.
* Automatic 'alpha snapshots' are made available to the public for very early testing. See [testing guide](../testing/contributing.md).

### Beta phase
* A commit without any known serious issues, will be selected from the 'master' branch and merged into 'beta', this draws the line for features included in the release.
* Documentation changes will be reviewed. A release summary will be added to the change log for the beta.
* A tagged 'beta release' will be created for wider testing.
* New pull requests may be now considered for squash merging straight to beta.
  - If addressing regression introduced in this release.
  - If addressing a bug in a "must have" feature for this release.
  - If addressing a critical Operating System change out of our control.
* As appropriate new tagged beta releases will be published once a week.
* As necessary `beta` will be merged back into master.
  - For critical pull requests or translation merges.
* If a merged pull request that reached beta has been identified as causing a regression, new bug, or does not work as originally reported:
  - The pull request may be reverted at the discretion of the lead developers.
  - It may be fixed by a collaborator if the bug is trivial enough.
  - Once a PR is reverted from `beta`, a replacement PR is very unlikely to be accepted into the current release.
  - Use the [PR revert template](../../.github/PULL_REQUEST_TEMPLATE/revert.md) when reverting.

### Release Candidate phase

#### Translatable String Freeze
- The beta branch will enter a 2 week translatable string freeze.
- Translators should ensure their translation is up to date a day before the translatable string freeze ends in order for it to be included in the upcoming final release.
The lead developers will announce the deadline when the freeze begins, if in doubt check the [NVDA-Translations message board](https://groups.io/g/nvda-translations/) for the "language freeze" announcement.
Work submitted after this time will not be included in the upcoming release.
- No changes to text strings that affect translations are allowed during the freeze. Minor spelling or grammatical fixes may be made to documentation files, but `gettext` strings in the code should not be changed at all.
- Only critical bug fixes and translation updates should be committed to the beta branch at this stage.
In this case the translation period will need to be extended by an appropriate amount of time.

#### Release Candidate
* After the translatable string freeze, the `rc` branch will be created based on the beta branch.
* The first release candidate will immediately be released from the `rc` branch.
* After this, only critical bug fixes should be committed to the `rc` branch.
* Subsequent release candidates may be released.
* The final release can only be made if there have been no significant changes and at least 1 week since the last release candidate.

### Representation on GitHub
* For most items, an issue will be filed and discussed before a pull request is submitted.
* If priority should be given to an issue for inclusion in a specific release, its milestone should be set to the appropriate release milestone (e.g. 2014.4).
* Once a pull request is squash merged to the master branch, the milestone for the issue (if any) and pull request should be set to the next release milestone (e.g. 2013.2) and it should be closed as fixed.
* Issues/pull requests for bug fixes for an rc should have their milestone set to the relevant release (e.g. 2013.2).

### Scheduled Releases
* In the past NVDA has been released 4 times per year. This is not expected to change drastically. The exact date for each release will be determined by the lead developers.

### Patch Release
* Under rare circumstances, a patch release (e.g. 2013.1.1) may be made.
* A patch release may only include fixes for crashes and major security issues.
* Patch releases are made from the `rc` branch.
