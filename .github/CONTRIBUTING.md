# Contributing to NVDA
There are several ways in which you can contribute to the NVDA project:
- By testing NVDA
- Issue triage and investigation
- Code or documentation contributions

## Testing

Testing alpha / beta / and release candidates help to ensure the quality of the NVDA.
User / community testing is particularly important for languages other than English.
There are several approaches you may take for this:
- Unfocused usage: Just use NVDA as you normally would, and try to complete everyday tasks.
- Recent change focused testing: By following the changes that are being made to NVDA and purposefully testing these changes and looking for edge-cases.
- Regression testing: Testing older features and behavior to look for unintended regressions in behavior that don't seem related to recent changes.

Forming a group can help you to get good coverage, brainstorm on what should be tested, and perhaps learn new ways to use NVDA.

## Issue triage and investigation:
You can also make non-code contributions by helping process incoming GitHub issues. For information on this please see the [triage process](https://github.com/nvaccess/nvda/wiki/Triage-process) and [issue triage help](https://github.com/nvaccess/nvda/wiki/Issue-triage-help) on the wiki.

## Code/Docs contributions

If you are new to the project, or looking for some way to help take a look at:
- [label:"good first issue" ](https://github.com/nvaccess/nvda/issues?q=label%3A%22good+first+issue%22)
- [label:closed/needs-new-author ](https://github.com/nvaccess/nvda/issues?q=label%3Aclosed%2Fneeds-new-author)
- [label:Abandoned ](https://github.com/nvaccess/nvda/issues?q=label%3AAbandoned)

### Guidelines:
- For anything other than minor bug fixes, please comment on an existing issue or create a new issue providing details about your proposed change.
- Unrelated changes should be addressed in separate issues.
- Include information about use cases, design, user experience, etc.
  - This allows us to discuss these aspects and any other concerns that might arise, thus potentially avoiding a great deal of wasted time.
- It is recommended to wait for acceptance of your proposal before you start coding.
  - Please understand that we very likely will not accept changes that are not discussed first.
  - Consider starting a discussion on mailing lists (EG NVDA developers) to see if there is interest.
- A minor/trivial change which definitely wouldn't require design, user experience or implementation discussion, you can just create a pull request rather than using an issue first.
  - E.G. a fix for a typo/obvious coding error or a simple synthesizer/braille display driver
  - This should be fairly rare.
- If in doubt, use an issue first. Use this issue to discuss the alternatives you have considered in regards to implementation, design, and user experience. Then give people time to offer feedback.


### GitHub process:
#### 1. "fork" the NVDA repository on GitHub
   When you fork the repository, GitHub will create a copy of the master branch.
   However, this branch will not be updated when the official master branch is updated.
   To ensure your work is always based on the latest commit in the official master branch, it is recommended that your master branch be linked to the official master branch, rather than the master branch in your GitHub fork.
   If you have cloned your GitHub fork, you can do this from the command line as follows:
   ```
   # Add a remote for the NV Access repository.
   git remote add nvaccess https://github.com/nvaccess/nvda.git
   # Fetch the nvaccess branches.
   git fetch nvaccess
   # Switch to the local master branch.
   git checkout master
   # Set the local master to use the nvaccess master as its upstream.
   git branch -u nvaccess/master
   # Update the local master.
   git pull
   ```

#### 2. Use a separate "topic" branch for each contribution
   All code should usually be based on the latest commit in the official master branch at the time you start the work unless the code is entirely dependent on the code for another issue.
   If you are adding a feature or changing something that will be noticeable to the user, you should update the User Guide accordingly.

#### 3. Run unit tests and lint check
   - Run `rununittests` (`rununittests.bat`) before you open your Pull Request, and make sure all the unit tests pass.
   - If possible for your PR, please consider creating a set of unit tests to test your changes.
   - The lint check ensures your changes comply with our code style expectations. Use `runlint nvaccess/master` (`runlint.bat`)

#### 4. Create a Pull Request (PR)
   When you think a contribution is ready, or you would like feedback, open a draft pull request.
   Please fill out the Pull Request Template, including the checklist of considerations.
   The checklist asks you to confirm that you have thought about each of the items, if any of the items are missing it is helpful to explain elsewhere in the PR why it has been left out.
   When you would like a review, mark the PR as "ready for review".

#### 5. Participate in the code review process
   This process requires core NVDA developers to understand the intent of the change, read the code changes, asking questions or suggesting changes.
   Please participate in this process, answering questions, and discussing the changes.
   Being proactive will really help to speed up the process of code review.
   When the PR is approved it will be merged, and the change will be active in the next Alpha build.

#### 6. Feedback from Alpha users
   After a PR is merged, watch for feedback from Alpha users / testers.
   You may have to follow up to address bugs or missed use-cases.

## Code Style

Code style is enforced with the flake8 linter, see [`tests/lint/readme.md`](https://github.com/nvaccess/nvda/tree/master/tests/lint) for more information.

### Encoding
* Where Python files contain non-ASCII characters, they should be encoded in UTF-8.
    * There should be no Unicode BOM at the start of the file, as this unfortunately breaks one of the translation tools we use (`xgettext`). Instead, include this as the first line of the file (only if the file contains non-ASCII characters):
        ```
        # -*- coding: UTF-8 -*-
        ```
    * This coding comment must also be included if strings in the code (even strings that aren't translatable) contain escape sequences that produce non-ASCII characters; e.g. `"\xff"`. This is particularly relevant for braille display drivers. This is due to a `gettext` bug; see https://github.com/nvaccess/nvda/issues/2592#issuecomment-155299911.
* Most files should contain `CRLF` line endings, as this is a Windows project and can't be used on Unix-like operating systems.

### Indentation
* Indentation must be done with tabs (one per level), not spaces.
* When splitting a single statement over multiple lines, just indent one or more additional levels. Don't use vertical alignment; e.g. lining up with the bracket on the previous line.
  - Be aware that this requires a new-line after an opening parenthesis/bracket/brace if you intend to split the statement over multiple lines.
  - For the parameter list of function definitions, double indent, this differentiates the parameters and the body of the function.

### Identifier Names
* Use descriptive names
  - name constants to avoid "magic numbers" and hint at intent or origin of the value. Consider, what does this represent?
* Functions, variables, properties, etc. should use mixed case to separate words, starting with a lower case letter; e.g. `speakText`.
* Boolean functions or variables
  - should try to use the positive form of the language (to avoid double negatives like `shouldNotDoSomething = False`)
  - start with a "question word" to hint at their boolean nature. EG `shouldX`, `isX`, `hasX`
* Classes should use mixed case to separate words, starting with an upper case letter; e.g. `BrailleHandler`.
* Constants should be all upper case, separating words with underscores; e.g. `LANGS_WITH_CONJUNCT_CHARS`.
* Event handlers are prefixed with "event_", and are often in the form "event_ACTION" or "event_OBJECT_ACTION". Where OBJECT refers to the class type that the ACTION refers to.
* Extension points:
  * `Action`: Prefixed with `pre_` or `post_` to specify that handlers are being notified before / after the action has taken place.
  * `Decider`: Prefixed with `should_` to turn them into a question eg `should_doSomething`
  * `Filter`: TBD. Ideally follows a similar style the others, and communicates if the filtering happens before or after some action. It would also be nice to have a naming scheme that differentiates it from the others.

### Translatable Strings
* All strings that could be presented to the user should be marked as translatable using the `_()` function; e.g. `_("Text review")`.
* All translatable strings should have a preceding translators comment describing the purpose of the string for translators. For example:
```
# Translators: The name of a category of NVDA commands.
SCRCAT_TEXTREVIEW = _("Text review")
```
* Lengthy translatable strings can be split across multiple lines, taking advantage of Python's implicit line joining inside parentheses. Translators comment can span multiple lines as well. For example:
```
self.copySettingsButton = wx.Button(
	self,
	label=_(
		# Translators: The label for a button in general settings to copy
		# current user settings to system settings (to allow current
		# settings to be used in secure screens such as User Account
		# Control (UAC) dialog).
		"Use currently saved settings during sign-in and on secure screens"
		" (requires administrator privileges)"
	)
)
```
