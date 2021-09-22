# Creating PR's on the NVDA project

This page is meant to serve as an explanation for how to fill out
[our Github pull request template](https://github.com/nvaccess/nvda/blob/master/.github/PULL_REQUEST_TEMPLATE.md)

## The template
At the start of the template there is a HTML comment block (starting with `<!--`),
which points to this wiki page, it can be left in place and will not appear once the issue is saved.
Feel free to delete it, i.e. all text up to and including `-->`.

### Link to issue number:
Please include the issue number here, including information on how this pull request is related to 
it.
This helps us to keep the information linked together.
If this is a minor/trivial change an issue does not need to be created.
If in doubt, please create one.
Note that Github 
[allows you to automatically close issues using keywords](https://help.github.com/en/articles/closing-issues-using-keywords).
For example, when writing `closes #7777` or `fixes #4242` in the body of the description,
the mentioned issue will automatically be closed when the pull request is merged into the master
branch.
If your pull request is filed against another branch, such as beta, the particular issue will have
to be close manually after merging the pull request.

### Summary of the issue:
A quick summary of the problem you are trying to solve.

### Description of how this pull request fixes the issue:
Please include a quick discussion of how this change addresses the issue.
Please also include any links or external information you may have used in order to address the
issue.
This helps others to have the same background as you and learn from this work.

### Testing strategy:
Outline the steps you took to test the change.
This should allow someone else to reproduce your testing.

More broadly, try to answer the following questions:
- How have you tested to ensure that your change works as intended?
- Have you ensured testing coverage across all supported operating systems?
- Have you considered possible regressions (related features or behaviours that may break)?

Please use this section as an opportunity to try to convince us (and yourself) that your proposed 
change should be merged. 

Often in face to face development it's useful to demonstrate a change, quite often bugs are noticed
at this point when the new person asks for some variation in testing approach.
Since we unlikely to be able to demonstrate a feature in an interactive way, an easy-to-follow list
of steps for a "demo" allows others check themselves without having to work out all the details.
It also serves as a starting point for members of the community who are testing the changes that go
into NVDA.

Example:
> In NVDA settings ensure that:
> - Keyboard category
>   - "speak typed characters" is unchecked
>   - "speak typed words" is checked
>
> 1. Open notepad
> 2. Type "hello"
> 3. Press space
>
> Expect "hello" to be announced.

- If many NVDA settings are required, consider attaching a sample `nvda.ini` file to the PR.
- If a complicated document is required to test with a 3rd party application, consider attaching it
  to the PR for others to test with.

### Known issues with pull request:
Are there any known issues or downsides of this approach.
For instance: _Will not work with python 3_

### Change log entries:
An entry intended to explain changes in NVDA to end users.
Your proposed entry will be added to the `changes.t2t` file which is converted to html and used as a
what's changed / change log document.
See 
[`user_docs/en/changes.t2t`](https://github.com/nvaccess/nvda/blob/master/user_docs/en/changes.t2t)

Because the `changes.t2t` file is prone to conflicts, we ask contributors not to edit the file directly, but instead add the entry to the bottom of the PR description.
A lead developer will update file when merging the pull request.

For instance:
```
*New features*
`Added a command to announce useful thing. (#WXYZ, #ABCD)`

*Changes*
`Old command, now also uses new useful command. (#WXYZ)`
```

These descriptions should be in the format: `"{Description of change}. (#{issue number})"`

You may suggest descriptions for multiple sections.
The usual sections are:
 
* New features
* Changes
* Bug fixes

Multiple issue numbers can be included, separated by comma.
If there is no issue number, you can use the PR number.

For examples see the
[changes.t2t file](https://github.com/nvaccess/nvda/blob/master/user_docs/en/changes.t2t)

## Code Review Checklist

Code must be reviewed (via a Pull Request on GitHub) before it can be accepted into the project.
The Pull Request template (``.github/PULL_REQUEST_TEMPLATE.md``) asks authors (and reviewers) to
consider several aspects of the change.

The aim of this checklist is to ensure each item has been considered by both the author and the
reviewer.
Hopefully it helps to prevent items being forgotten.
After reviewing the checklist the reviewer and author need to use their best judgement on whether
they think further changes need to be made.
Reviewers are invited to start a conversation about items in the list, to provide guidance on how to
improve the PR.
Not all items will be applicable for all situations, in this case checking the item lets reviewers
know it's been considered.
If the reviewer reaches the same conclusion as the author, no further work is necessary.
Most items in the checklist have a section in the PR template where you can add your thoughts, doing
so may preempt questions from the reviewer ensuring you are on the same page, and speed up the
review process.

### Pull Request description:
- description is up to date.
  Authors must keep the PR description up to date.
  - Even if changes to the approach are described in the comments for the PR.
  - Future developers need a concise explanation of a change.
  After each modification, check that the PR description is still accurate.
- change log entries
  Has an appropriate change log entry been supplied?
  As a reviewer, please review it.

### Testing:
Discuss under "testing strategy" heading:
- Unit tests
  - Describe the coverage of automated unit tests?
  - Is the changed code already, or can it be covered by automated unit tests?
- System tests
  - Describe the coverage of automated system tests?
  - Is the changed code already, or can it be covered by automated system tests?
- Manual tests
  - How did you manually test the change?
  - Be clear on steps another user can take to replicate your testing.
  - Is the described manual testing appropriate for the change?
  - Clearly describing this helps alpha testers, and future developers.
  - As a reviewer, please use this description to replicate the testing (if possible).

### API is compatible with existing add-ons.
- If this is not a `.1` breaking release, ensure that all API changes are backwards compatible with existing add-ons.
- Ensure proposed API changes are included in the change log (Changes for Developers).
- See [Deprecations](./deprecations.md) for more information.

### Documentation
- User Documentation
  Does the user documentation need updating?
- Context sensitive help for GUI changes.
  New GUI options require context sensitive help assignment.
- Developer / Technical Documentation
  Does the developer or technical documentation need updating?

### UX of all users considered
- Users of NVDA are diverse, and rely on different parts of NVDA.
  Ensure the change caters to users of the following:
  - Speech
  - Braille
  - Low Vision
  - Different web browsers (Firefox, Chrome, Edge)
  - Localization in other languages / culture than English
- When one of these can not be supported with this change,
  highlight it under the "Known issues" heading
