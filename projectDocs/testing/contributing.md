# Testing

## Builds

Testing alpha / beta / and release candidates (RC) help to ensure the quality of the NVDA project.
Download the [latest alpha builds](https://download.nvaccess.org/snapshots/alpha) or [beta/RC builds](https://download.nvaccess.org/snapshots/beta/).

* The alpha builds are bleeding edge.
It includes code that is being tested for possible inclusion in upcoming releases, but it may not yet be tested much (if at all) and there may be major bugs.
Alpha snapshots are created directly from the `master` branch each time it changes (i.e. when a pull request is merged).
Although the automated tests pass, these builds have likely had no user testing.
* 'beta releases' are 'beta' quality. They include all features for the upcoming release that have proved stable in the alpha builds.
* 'RC releases' in most cases will be identical to the final release.
The latest final release will be identical to the final RC release of the release cycle.

## Manual testing
User / community testing is particularly important for languages other than English.

NVDA includes [manual test plans](../../tests/manual/README.md) to guide testers in smoke testing features of NVDA.

There are several approaches you may take for testing:
- Unfocused usage: Just use NVDA as you normally would, and try to complete everyday tasks.
- Recent change focused testing: By following the changes that are being made to NVDA and purposefully testing these changes and looking for edge-cases.
- Regression testing: Testing older features and behavior to look for unintended regressions in behavior that don't seem related to recent changes.
- Pull request testing.
Testing pull requests can be done
	1. Go to the pull request page.
	1. Navigate to the linked "Details of continuous integration", this is towards the end of the PR, as part of the checks and approval status.
	1. Go to the "Artifacts" tab
	1. Download the NVDA installer, named something like `output\nvda_snapshot_pr15335-28962,a2970e3f.exe`
	1. The pull request should contain some information on how to test this change.
- Confirming bugs.
By following the [issue triage process](../issues/triage.md) you can help confirm bugs and debug issues.

Forming a group can help you to get good coverage, brainstorm on what should be tested, and perhaps learn new ways to use NVDA.

## Automated testing

NVDA performs automated testing as part of CI/CD.
This includes linting checks, unit tests and system tests.
Refer to our [automated testing](./automated.md) document.
