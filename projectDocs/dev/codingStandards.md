## Code Style

Python code style is enforced with the Ruff linter, see [linting](../testing/automated.md#linting-your-changes) for more information.

### Encoding

* Where Python files contain non-ASCII characters, they should be encoded in UTF-8.
  * There should be no Unicode BOM at the start of the file, as this unfortunately breaks one of the translation tools we use (`xgettext`).
  Instead, include this as the first line of the file, only if the file contains non-ASCII characters:

  ```py
  # -*- coding: UTF-8 -*-
  ```

  * This coding comment must also be included if strings in the code (even strings that aren't translatable) contain escape sequences that produce non-ASCII characters; e.g. `"\xff"`.
    This is particularly relevant for braille display drivers.
    This is due to a `gettext` bug; see [comment on #2592](https://github.com/nvaccess/nvda/issues/2592#issuecomment-155299911).
* Text files should be committed with `LF` line endings.
Files can be checked out locally using CRLF if needed for Windows development using [git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration#_core_autocrlf).

### Indentation
* Indentation must be done with tabs (one per level), not spaces.
* When splitting a single statement over multiple lines, just indent one or more additional levels.
  Don't use vertical alignment; i.e. lining up with the bracket on the previous line.
  - Be aware that this requires a new-line after an opening parenthesis/bracket/brace if you intend
    to split the statement over multiple lines.

### Identifier Names
* Use descriptive names
  - name constants to avoid "magic numbers" and hint at intent or origin of the value.
    Consider, what does this represent?
* Functions, variables, properties, etc. should use mixed case to separate words, starting with a lower case letter;
  - E.g. `speakText`.
* Boolean functions or variables
  - Use the positive form of the language.
    Avoid double negatives like `shouldNotDoSomething = False`
  - Start with a "question word" to hint at their boolean nature.
  - E.g. `shouldX`, `isX`, `hasX`
* Classes should use mixed case to separate words, starting with an upper case letter;
  - E.g. `BrailleHandler`.
* Constants should be all upper case, separating words with underscores;
  - E.g. `LANGS_WITH_CONJUNCT_CHARS`.
* Scripts (the targets of gestures) are prefixed with "script_", with subsequent words in camel case.
  - E.g. `script_cycleAudioDuckingMode`.
* Event handlers are prefixed with "event_", with subsequent words in camel case.
  Note, `object` and `action` are separated by underscores.
  - E.g.: `event_action` or `event_object_action`.
  - `object` refers to the class type that the `action` refers to.
  - Examples: `event_caret`, `event_appModule_gainFocus`
* Extension points:
  * `Action`
    - Prefixed with `pre_` or `post_` to specify that handlers are being notified before / after the
      action has taken place.
  * `Decider`
    - Prefixed with `should_` to turn them into a question, e.g. `should_doSomething`
  * `Filter`
    - Prefixed with `filter_`, e.g. `filter_displaySize_preRefresh`
    - Should describe the filtering action and the data being returned
    - Should communicate if the filtering happens before or after some action
* Enums should be formatted using the expected mix of the above, e.g.:
  ```python
  class ExampleGroupOfData(Enum):
      CONSTANT_VALUE_MEMBER = auto()
      @property
      def _formatMember(self): pass
  ```

### Translatable Strings
* All strings that could be presented to the user should be marked as translatable using the `_()` function
  - e.g. `_("Text review")`.
* All translatable strings should have a preceding translators comment describing the purpose of the string for translators.
For example:
```py
# Translators: The name of a category of NVDA commands.
SCRCAT_TEXTREVIEW = _("Text review")
```
* Lengthy translatable strings can be split across multiple lines, taking advantage of Python's implicit line joining inside parentheses.
Translators comment can span multiple lines as well.
For example:
```py
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

### Imports
* Unused imports should be removed where possible.
  - Anything imported into a (sub)module can also be imported from that submodule.
  - As a result, removing unused imports may break compatibility, and should be done in compatibility breaking releases (see `deprecations.md`).
* Unused imports will give a lint warning. These can be handled the following ways:
  - If these imports are intended to be imported from other modules, they can be included in a definition for `__all__`. This will override and define the symbols imported when performing a star import, e.g. `from module import *`.
  - Otherwise, with a comment like `# noqa: <explanation>`.

### Considering future backwards compatibility

When writing new code, consider how the code can be moved in future while retaining backwards compatibility.
Refer to the [limitations to retaining backwards compatibility](./deprecations.md#limitations-to-retaining-backwards-compatibility).

In summary:
- Avoid module level global variables.
Any module level variables should be prefixed with an underscore and be encapsulated, e.g. via getters and setters.
- Avoid code which executes at import time.
Instead use initializer functions.

### Docstrings

Docstrings should use [Sphinx format](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html).
Providing type information in docstrings is discouraged, instead use python's type annotations.

NVDA formerly used [epytext](https://epydoc.sourceforge.net/manual-epytext.html) syntax for docstrings, which means there is inconsistent syntax used in the NVDA code base.
[#12971](https://github.com/nvaccess/nvda/issues/12971) exists to track converting epytext docstrings to Sphinx.
