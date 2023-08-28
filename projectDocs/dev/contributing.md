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
  - Please understand that we very likely will not accept changes that are not discussed first.
  - Consider starting a [GitHub discussion](https://github.com/nvaccess/nvda/discussions) or [mailing list topic](https://groups.io/g/nvda-devel/topics) to see if there is interest.
- A minor/trivial change which definitely wouldn't require design, user experience or implementation discussion, you can just create a pull request rather than using an issue first.
  - e.g. a fix for a typo/obvious coding error or a simple synthesizer/braille display driver
  - This should be fairly rare.
- If in doubt, use an issue first. Use this issue to discuss the alternatives you have considered in regards to implementation, design, and user experience. Then give people time to offer feedback.


### Overview of contribution process:
1. [Setup your development environment](./createDevEnvironment.md).
1. Ensure the issue you plan to fix is [triaged](../issues/triage.md)
1. Create a branch for the contribution.
	- Pull requests should be based on the latest commit in the official master branch.
	This helps reduce the chance of merge conflicts.
	- If you are adding a feature or changing something that will be noticeable to the user, you should update the User Guide accordingly.
1. [Build NVDA](./buildingNVDA.md) and run from source
1. [Manually test the change](../testing/readme.md)
1. [Run automated tests](../testing/automated.md)
	- Run `rununittests` (`rununittests.bat`) before you open your Pull Request, and make sure all the unit tests pass.
	- If possible for your PR, please consider creating a set of unit or system tests to test your changes.
	- The lint check ensures your changes comply with our code style expectations. Use `runlint nvaccess/master` (`runlint.bat`)
	- Run `scons checkPot` to ensure translatable strings have comments for the translators
1. [Create a Pull Request (PR)](./githubPullRequestTemplateExplanationAndExamples.md)
	- When you think a contribution is ready, or you would like feedback, open a draft pull request.
	When you would like a review, mark the PR as "ready for review".
	- Please fill out the Pull Request Template, including the checklist of considerations.
	The checklist asks you to confirm that you have thought about each of the items, if any of the items are missing it is helpful to explain elsewhere in the PR why it has been left out.
1. Participate in the code review process
	- This process requires core NVDA developers to understand the intent of the change, read the code changes, asking questions or suggesting changes.
	Please participate in this process, answering questions, and discussing the changes.
	- Being proactive will really help to speed up the process of code review.
	- When the PR is approved it will be merged, and the change will be active in the next alpha build.
	- If issues are raised with your PR, it may be marked as a draft.
	Please mark it as ready for review when you have addressed the review comments.
1. Feedback from alpha users
	- After a PR is merged, watch for feedback from alpha users / testers.
	You may have to follow up to address bugs or missed use-cases.

## Code Style
Please ensure you follow [our coding standards document](../projectDocs/dev/codingStandards.md).

## Technical design
Please checkout our [technical design overview](../design/technicalDesignOverview.md).
