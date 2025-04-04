## Code/Docs contributions

If you are new to the project, or looking for some way to help take a look at:
- [label:"good first issue"](https://github.com/nvaccess/nvda/issues?q=label%3A%22good+first+issue%22)
- [label:component/documentation](https://github.com/nvaccess/nvda/issues?q=label%3Acomponent%2Fdocumentation)
- [label:closed/needs-new-author](https://github.com/nvaccess/nvda/issues?q=label%3Aclosed%2Fneeds-new-author)
- [label:Abandoned](https://github.com/nvaccess/nvda/issues?q=label%3AAbandoned)

### Guidelines:
- For anything other than minor bug fixes, please comment on an existing issue or create a new issue providing details about your proposed change.
- Unrelated changes should be addressed in separate issues.
- Include information about use cases, design, user experience, etc.
  - This allows us to discuss these aspects and any other concerns that might arise, thus potentially avoiding a great deal of wasted time.
- It is recommended to wait for acceptance of your proposal before you start coding.
  - A `triaged` label is an indicator that an issue is ready for a fix.
  - A triaged issue should have a priority, as a developer, consider focusing on higher priority issues (p1-p3) instead of lower priority issues (p4-p5).
  - Please understand that we very likely will not accept changes that are not discussed first.
  - Consider starting a [GitHub discussion](https://github.com/nvaccess/nvda/discussions) or [mailing list topic](https://groups.io/g/nvda-devel/topics) to see if there is interest.
- A minor/trivial change which definitely wouldn't require design, user experience or implementation discussion, you can just create a pull request rather than using an issue first.
  - e.g. a fix for a typo/obvious coding error or a simple synthesizer/braille display driver
  - This should be fairly rare.
- If in doubt, use an issue first. Use this issue to discuss the alternatives you have considered in regards to implementation, design, and user experience. Then give people time to offer feedback.
- Issues with translations should be reported to the [NVDA Translators list](https://groups.io/g/nvda-translations).


### Overview of contribution process:
1. [Setup your development environment](./createDevEnvironment.md).
    - Alternatively, you can use [AppVeyor](https://appveyor.com/) to build NVDA for you, without setting up a local development environment, by following [this how-to](./buildingNVDAOnAppVeyor.md).
1. Ensure the issue you plan to fix is [triaged](../issues/triage.md)
1. Create a branch for the contribution, to be used for a pull request.
	- Pull requests should be based on the latest commit in the official master branch.
	This helps reduce the chance of merge conflicts.
	- If you are adding a feature or changing something that will be noticeable to the user, you should update the [User Guide accordingly](./userGuideStandards.md).
	New commands, drivers, settings, dialogs, etc. must be documented.
1. [Build NVDA](./buildingNVDA.md) and run from source
1. [Manually test the change](../testing/readme.md)
1. [Run automated tests](../testing/automated.md)
	- Run `rununittests` (`rununittests.bat`) before you open your Pull Request, and make sure all the unit tests pass.
	- If possible for your PR, please consider creating a set of unit or system tests to test your changes.
	- The lint check ensures your changes comply with our code style expectations.
	Use `runlint.bat`.
	- Run `scons checkPot` to ensure translatable strings have comments for the translators
	- Run `runlicensecheck.bat` to check that you don't introduce any new python dependencies with incompatible licenses.
1. [Create a change log entry](#change-log-entry)
1. Create a Pull Request (PR)
	1. Filling out the template:
		- [Template guide](./githubPullRequestTemplateExplanationAndExamples.md)
		- Please fill out the Pull Request template, including the checklist of considerations.
		The checklist asks you to confirm that you have thought about each of the items, if any of the items are missing it is helpful to explain elsewhere in the PR why it has been left out.
	1. Submission process:
		- If you would like to publish unfinished work to seek early feedback or demonstrate an approach, open a draft pull request.
		When you would like a code review or response from NV Access, mark the PR as "ready for review".
		- All pull requests submitted must have their "Allow edits from maintainers" checkbox ticked.
		This is the GitHub default for new pull requests, except for organisation forks.
		Organisation forks must invite NV Access developers to collaborate directly.
		- Consider if the PR should be made against `beta` or `rc` in the case of addressing bugs introduced in the current release cycle.
	1. CI/CD testing:
		- Every time a PR has a commit pushed to it, CI/CD checks will be run
		- [pre-commit.ci](https://pre-commit.ci/) will apply linting fixes.
			- re-run pre-commit on a pull request by commenting `pre-commit.ci run`.
			- prevent pre-commit from pushing by putting `[skip ci]`, `[ci skip]`, `[skip pre-commit.ci]`, or `[pre-commit.ci skip]` in the commit message.
		- AppVeyor will build a copy of NVDA when changes are pushed to your PR.
		A build artifact will be created for a successful build to allow for testing the PR.
		- AppVeyor will run system tests and other tests.
		If these fail, please review them.
		Sometimes system tests fail unexpectedly.
		If you believe the failure is unrelated, feel free to ignore it unless it is raised by a reviewer.
		- Security checks will be run.
1. Participate in the code review process
	- This process requires core NVDA developers to understand the intent of the change, read the code changes, asking questions or suggesting changes.
	Please participate in this process, answering questions, and discussing the changes.
	- Being proactive will really help to speed up the process of code review.
	- When the PR is approved it will be merged, and the change will be active in the next alpha build.
	- If issues are raised with your PR, it may be marked as a draft.
	Please mark it as ready for review when you have addressed the review comments.
	- CodeRabbit AI can review your code.
	  - To request a review from CodeRabbit, comment `@coderabbitai review`
	  - CodeRabbit reviews may be automatically or manually requested by reviewers
	  - Please participate in the review process, the AI can respond to review comments, questions and feedback.
	  - Some comments may not be helpful due to the nature of AI, and some might be useful.
	  Please indicate comments which you intend to ignore and why.
	  For large numbers of unhelpful comments, please mark them as resolved or comment `@coderabbitai resolve` to resolve all comments.
1. Feedback from alpha users
	- After a PR is merged, watch for feedback from alpha users / testers.
	You may have to follow up to address bugs or missed use-cases.

#### Change log entry
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
