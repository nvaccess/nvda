## Code Style

Python code style is enforced with the flake8 linter, see
[`tests/lint/readme.md`](https://github.com/nvaccess/nvda/tree/master/tests/lint)
for more information.

### Encoding
* Where Python files contain non-ASCII characters, they should be encoded in UTF-8.
    * There should be no Unicode BOM at the start of the file, as this unfortunately breaks one of
      the translation tools we use (`xgettext`).
      Instead, include this as the first line of the file (only if the file contains non-ASCII
      characters):
        ```
        # -*- coding: UTF-8 -*-
        ```
    * This coding comment must also be included if strings in the code (even strings that aren't
      translatable) contain escape sequences that produce non-ASCII characters; e.g. `"\xff"`.
      This is particularly relevant for braille display drivers.
      This is due to a `gettext` bug; see
      https://github.com/nvaccess/nvda/issues/2592#issuecomment-155299911.
* Most files should contain `CRLF` line endings, as this is a Windows project and can't be used on
  Unix-like operating systems.

### Indentation
* Indentation must be done with tabs (one per level), not spaces.
* When splitting a single statement over multiple lines, just indent one or more additional levels.
  Don't use vertical alignment; e.g. lining up with the bracket on the previous line.
  - Be aware that this requires a new-line after an opening parenthesis/bracket/brace if you intend
    to split the statement over multiple lines.
  - For the parameter list of function definitions, double indent, this differentiates the
    parameters and the body of the function.

### Identifier Names
* Use descriptive names
  - name constants to avoid "magic numbers" and hint at intent or origin of the value.
    Consider, what does this represent?
* Functions, variables, properties, etc. use mixed case to separate words, starting with a lower
  case letter; e.g. `speakText`.
* Boolean functions or variables
  - Prefer positive form of the language.
    Avoid double negatives like `shouldNotDoSomething = False`
  - Start with a "question word" to hint at their boolean nature. EG `shouldX`, `isX`, `hasX`
* Classes should use mixed case to separate words, starting with an upper case letter;
  - E.G. `BrailleHandler`.
* Constants should be all upper case, separating words with underscores;
  - E.G. `LANGS_WITH_CONJUNCT_CHARS`.
  - Avoid unnecesary shared prefixes in constants. Instead, use an enum for related constants.
* Event handlers are prefixed with "event_", subsequent words in camel case.
  Note, `object` and `action` are separated by underscores.
  - E.G.: `event_action` or `event_object_action`.
  - `object` refers to the class type that the `action` refers to.
  - Examples: `event_caret`, `event_appModule_gainFocus`
* Extension points:
  * `Action`
    - Prefixed with `pre_` or `post_` to specify that handlers are being notified before / after the
      action has taken place.
  * `Decider`
    - Prefixed with `should_` to turn them into a question eg `should_doSomething`
  * `Filter`
    - TBD. Ideally follows a similar style the others, and communicates if the filtering happens
      before or after some action.
    - It would also be nice to have a naming scheme that differentiates it from the others.
* Enums should be formatted using the expected mix of above eg:
  ```python
  class ExampleGroupOfData(Enum):
      CONSTANT_VALUE_MEMBER = auto()
      @property
      def _formatMember(self): pass
  ```

### Translatable Strings
* All strings that could be presented to the user should be marked as translatable using the `_()`
  function; e.g. `_("Text review")`.
* All translatable strings should have a preceding translators comment describing the purpose of the
  string for translators. For example:
```
# Translators: The name of a category of NVDA commands.
SCRCAT_TEXTREVIEW = _("Text review")
```
* Lengthy translatable strings can be split across multiple lines, taking advantage of Python's
  implicit line joining inside parentheses.
  Translators comment can span multiple lines as well.
  For example:
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

### Imports
* Unused imports should be removed where possible.
  - Anything imported into a (sub)module can also be imported from that submodule.
  - As a result, removing unused imports may break compatibility, and should be done in compatibility breaking releases (see `deprecations.md`).
* Unused imports will give a lint warning. These can be handled the following ways: 
  - If these imports are inteded to be imported from other modules, they can be done included in a definition for `__all__`. This will override and define the symbols imported when performing a star import, eg `from module import *`.
  - Otherwise, with a comment like `# noqa: <explanation>`.
