# Release Process

This document provides rough guidelines for the process of developing NVDA releases. All current and potential developers and translators should read and follow this document. These guidelines may be broken under special circumstances. Any concerns should be discussed via [GitHub Discussion](https://github.com/nvaccess/nvda/discussions).
 
## Release Workflow
This is the general release workflow. Information for specific community groups is provided in later sections. The production of a release consists of the following:
1. Development Phase
   - Development is done in parallel to the release process for the prior version. E.G. NVDA 2020.2 is in development while NVDA 2020.1 is going through the Release Phase
1. Release Phase
   - Final testing, and translations work prior to release.

### Development phase
* Contributions are made according to the [For Developers](#for-developers) section 
* Once a pull request has been reviewed and approved by at least one NVDA Collaborator and all build checks have passed, a lead developer will make a final commit to the pull request which updates `changes.t2t`, and then will squash merge the pull request into master.
* If the merging of a pull request to `master` causes any build checks on `master` to fail, the pull request is reverted without question. This is however unlikely to be an issue as build checks on the pull request itself must have already passed.
* If a merged pull request has been identified as causing a regression, new bug, or does not work as originally reported, the pull request may be reverted at the discretion of the lead developers. Reasons in favor of not reverting the pull request may be: 
  * The pull request was submitted by an active collaborator who is likely to follow up with a suitable pull request to address the issues.
  * The bug is trivial enough to be fixed by a collaborator.
*  Automatic 'alpha snapshots' are made available to the public for very early testing. See [For Testers](#for-testers)

### Release phase
The release phase is intended to refine the release, with testing from wider audiences, and incorporated translations.
When no blocking issues are encountered it is expected to take 5 weeks:
- Beta builds: 2 weeks to receive any required fixes
  - Subsequent betas may take another week or two at discretion of lead developers
- 2 weeks for translation freeze (starting 3 weeks before release) 
- RC: 1 week.
  - When issues are encountered, subsequent RC's may take another week at the discretion of lead developers.

#### Beta builds
* A commit without any known serious issues, will be selected from the 'master' branch and merged into 'beta', this draws the line for features included in the release.
  - This commit will have been on `master` and thus, in 'alpha builds' for at least 2 weeks and can now be considered beta quality.
* A tagged 'beta release' will be created for wider testing. 
* New pull requests may be now considered for squash merging straight to beta.
  - If addressing regression introduced in this release.
  - If addressing a bug in a "must have" feature for this release.
  - If addressing a critical Operating System change out of our control.
* As appropriate new tagged beta releases will be published. 
* As necessary `beta` will be merged back into master.
  - For critical pull requests or translation merges.
* If a merged pull request that reached beta has been identified as causing a regression, new bug, or does not work as originally reported:
  - The pull request may be reverted at the discretion of the lead developers.
  - It may be fixed by a collaborator if the bug is trivial enough.
  - Once a PR is reverted from `beta`, a replacement PR is very unlikely to get into the current release.

### Translatable String Freeze
- The beta branch will enter a translatable string freeze.
- No changes to text strings that affect translations are allowed. Minor spelling or grammatical fixes may be made to documentation files, but `gettext` strings in the code should not be changed at all.
* Only critical bug fixes and translation updates should be committed to the beta branch at this stage. Otherwise the translation period will need to be extended by an appropriate amount of time.

### Release Candidate
* After the translatable string freeze, the "rc" branch will be created based on the beta branch.
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

### Maintenance Release
* Under rare circumstances, a maintenance release (e.g. 2013.1.1) may be made.
* A maintenance release may only include fixes for crashes and major security issues.
* Maintenance releases are made from the `rc` branch.

## For Developers
* GitHub issues should be created for most issues and discussed prior to starting work or submitting a pull request. This is to give lead developers and the community a chance to give feedback on the approach and prevent disappointment or wasted effort for contributors. However, some trivial changes might not require an issue first. See [[Contributing]] for details.
* Work should be done in topic branches. Including for external contributors.
  - A PR attempting to merge in the master branch of a contributors fork may not get automatic Pull Request builds.
* Any relevant documentation should be included in the topic branch.
* The topic branch should be submitted for inclusion using a pull request.
* New commands, drivers, settings, dialogs, etc. must be documented in the User Guide as appropriate.
* All Pull Requests must follow the Pull Request template provided.
* Pull requests must be based on NVDA's master branch.
  - A lead developer may specifically requested the pull request be made against `beta` or `rc` in the case of addressing bugs introduced in the current release cycle.
* Submitted pull requests should not contain edits to `changes.t2t.
  - Instead, change log entries should be placed in the pull request description, under the appropriate section in the template.
* All pull requests submitted must have their "Allow edits from maintainers" checkbox ticked. This is the GitHub default for new pull requests.

## For Translators
* All translation should be based on the `beta` branch.
* Translators should ensure their translation is up to date a day before the translatable string freeze ends in order for it to be included in the upcoming final release. The lead developers will announce the deadline when the freeze begins, if in doubt check the [NVDA-Translations message board](https://groups.io/g/nvda-translations/) for the "language freeze" announcement. Work submitted after this time will not be included in the upcoming release.

## For Testers
* Pre-release builds for testing (known as "snapshot builds") can be downloaded from the snapshots page at https://www.nvaccess.org/files/nvda/snapshots/.
  - It lists 'alpha snapshots', 'beta releases', and 'release candidates'. 
* The `alpha` builds are bleeding edge. It includes code that is being tested for possible inclusion in upcoming releases, but it may not yet be tested much (if at all) and there may be major bugs. Alpha snapshots are created directly from the `master` branch each time it changes (I.E. when a pull request is merged). Although the automated tests pass, these builds have likely had no user testing.
* 'beta releases' are 'beta' quality. They include all features for the upcoming release that have proved stable in the alpha builds. A feature is considered stable if it has been in 'alpha builds' for at least a week.
* 'rc releases' in most cases will be identical to the final release.
