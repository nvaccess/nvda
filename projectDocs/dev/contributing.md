# Code/Docs contributions

## Guidelines:

### First time contributors

When making your first PR, we encourage starting with one of the following issues.
This will help introduce you to the project.
To get used to the contribution process, please wait for feedback on your first PR before opening any other PRs.

* [label:"good first issue"](https://github.com/nvaccess/nvda/issues?q=label%3A%22good+first+issue%22)
* [label:component/documentation](https://github.com/nvaccess/nvda/issues?q=label%3Acomponent%2Fdocumentation)
* [label:closed/needs-new-author](https://github.com/nvaccess/nvda/issues?q=label%3Aclosed%2Fneeds-new-author)
* [label:Abandoned](https://github.com/nvaccess/nvda/issues?q=label%3AAbandoned)

### Trivial changes

A minor/trivial change which definitely wouldn't require design, user experience or implementation discussion, you can just create a pull request rather than using an issue first.

e.g. a fix for a typo/obvious coding error, or typing improvements.

Issues with the translations of the NVDA interface, Changes or User Guide should be reported to the [NVDA Translators list](https://groups.io/g/nvda-translations).

### Non-trivial changes

For anything other than minor bug fixes, ensure an issue has been filed and triaged.
Please understand that we very likely will not accept non-trivial changes that are not discussed first.

A `triaged` label is an indicator that an issue is ready for a fix.
A triaged issue should have a priority, as a developer, consider focusing on higher priority issues (p1-p3) instead of lower priority issues (p4-p5).

If the issue has an `ADR-required` label, this is a complex change.
Refer to ["Proposing Major Changes"](./proposingMajorChanges.md) before opening a PR.

Once triaged and ready please comment on the issue or ADR to confirm you plan to work on it.

### PR submission rules

Avoid having too many concurrent PRs (e.g. more than 3 ongoing).
NV Access is a small team and will try to respond to PRs within a couple of days.
Having multiple ongoing PRs increases the time to merge for each of them.

All PRs must be submitted by a human.
PRs which have not been reviewed and tested by the author will be closed.

### PR scope and size

Unrelated changes should be addressed in separate issues and PRs.

Avoid PRs where over 500 lines of code (LOC) is added.
PRs over 500 LOC may be rejected at the reviewers' discretion.

500-1000 line PRs can typically be broken into smaller changes such as automated tests, refactors, data-structures and core changes.
These can be merged as stacked PRs if they depend on each other (e.g. `branchX` targets `master`, `branchY` targets `branchX`).

Large refactors should instead target specific symbols/files/modules per PR to minimize mass changes.

Ongoing feature development that cannot be merged straight to `master` can occur on `try-` branches, done in pieces.
Ask NV Access on the corresponding ADR to create a `try-` branch.

## Overview of contribution process:

1. [Setup your development environment](./createDevEnvironment.md).
   * Alternatively, you can use GitHub Actions to build NVDA for you, without setting up a local development environment, by following [our CI/CD README](../../ci/README.md).
1. Ensure the issue you plan to fix is [triaged](../issues/triage.md)
1. If the issue has an `ADR-required` label, this is a complex change.
Refer to ["Proposing Major Changes"](./proposingMajorChanges.md) before opening a PR.
1. Create a branch for the contribution, to be used for a pull request.
	* Pull requests should be based on the latest commit in the official master branch.
	This helps reduce the chance of merge conflicts.
	* If you are adding a feature or changing something that will be noticeable to the user, you should update the [User Guide accordingly](./userGuideStandards.md).
	New commands, drivers, settings, dialogs, etc. must be documented.
1. [Build NVDA](./buildingNVDA.md) and run from source
1. [Manually test the change](../testing/readme.md)
1. [Run automated tests](../testing/automated.md)
	* Run `rununittests` (`rununittests.bat`) before you open your Pull Request, and make sure all the unit tests pass.
	* If possible for your PR, please consider creating a set of unit or system tests to test your changes.
	* The lint check ensures your changes comply with our code style expectations.
	Use `runlint.bat`.
	* Run `runcheckpot.bat` to ensure translatable strings have comments for the translators
	* Run `runlicensecheck.bat` to check that you don't introduce any new python dependencies with incompatible licenses.
1. [Create a change log entry](#change-log-entry)
1. Create a Pull Request (PR)
	1. Filling out the template:
		* [Template guide](./githubPullRequestTemplateExplanationAndExamples.md)
		* Please fill out the Pull Request template, including the checklist of considerations.
		The checklist asks you to confirm that you have thought about each of the items, if any of the items are missing it is helpful to explain elsewhere in the PR why it has been left out.
	1. Submission process:
		* If you would like to publish unfinished work to seek early feedback or demonstrate an approach, open a draft pull request.
		When you would like a code review or response from NV Access, mark the PR as "ready for review".
		* All pull requests submitted must have their "Allow edits from maintainers" checkbox ticked.
		This is the GitHub default for new pull requests, except for organisation forks.
		Organisation forks must invite NV Access developers to collaborate directly.
		* Consider if the PR should be made against `beta` or `rc` in the case of addressing bugs introduced in the current release cycle.
	1. CI/CD testing:
		* Every time a PR has a commit pushed to it, CI/CD checks will be run
		* [pre-commit.ci](https://pre-commit.ci/) will apply linting fixes.
			* re-run pre-commit on a pull request by commenting `pre-commit.ci run`.
			* prevent pre-commit from pushing by putting `[skip ci]`, `[ci skip]`, `[skip pre-commit.ci]`, or `[pre-commit.ci skip]` in the commit message.
		* GitHub Actions will build a copy of NVDA when changes are pushed to your PR.
		A build artifact will be created for a successful build to allow for testing the PR.
		* GitHub Actions will run system tests and other tests.
		If these fail, please review them.
		Sometimes system tests fail unexpectedly.
		If you believe the failure is unrelated, feel free to ignore it unless it is raised by a reviewer.
		* Security checks will be run.
		* If this is your first PR, GitHub will require manual approval from NV Access before running CI/CD.
		We encourage testing in your fork in this scenario (e.g. open a practice PR in your own fork).
1. Participate in the code review process
	* This process requires core NVDA developers to understand the intent of the change, read the code changes, asking questions or suggesting changes.
	Please participate in this process, answering questions, and discussing the changes.
	* Being proactive will really help to speed up the process of code review.
	* When the PR is approved it will be merged, and the change will be active in the next alpha build.
	* If issues are raised with your PR, it may be marked as a draft.
	Please mark it as ready for review when you have addressed the review comments.
	* CoPilot AI can review your code.
	  * CoPilot reviews may be automatically or manually requested by reviewers
	  * Please participate in the review process, the AI can respond to review comments, questions and feedback.
	  * Some comments may not be helpful due to the nature of AI, and some might be useful.
	  Please indicate comments which you intend to ignore and why.
1. Feedback from alpha users
	* After a PR is merged, watch for feedback from alpha users / testers.
	You may have to follow up to address bugs or missed use-cases.

### Change log entry

An entry intended to explain changes in NVDA to end users.
Your proposed entry should be added to the [`changes.md` file](../../user_docs/en/changes.md) which is converted to HTML.
Change log entries are not required for changes with no/minor user impact or no developer impact.

Because the `changes.md` file is prone to conflicts, NV Access will resolve any merge conflicts with the change log entry before merging.

These descriptions should be in the format: `"{Description of change}. (#{issue number})"`.
Multiple issue numbers can be included, separated by comma.
If there is no issue number, you can use the PR number.
Optionally, you may also include your GitHub username after the issue numbers: `"{Description of change}. (#{issue number}, @{GitHub username})"`.
Our processing will automatically link the issue number to the GitHub page, and your GitHub username to your contributions to NVDA.

For instance:

```md
### New Features

* Added a command to announce useful thing. (#1234, #4321, @myGitHub)

### Changes

* Old command now also uses new useful command. (#1234)
```

You may add descriptions for multiple sections.
The sections are:

* New features
* Changes
* Bug fixes
* Changes for developers

## Code Style

Please ensure you follow [our coding standards document](./codingStandards.md).

## Technical design

Please checkout our [technical design overview](../design/technicalDesignOverview.md).

## Copyright headers

Please refer to our guide on creating or updating [copyright headers](./copyrightHeaders.md)
