# Code Style

In general, Python contributions to NVDA should follow the [PEP 8 style guide](https://peps.python.org/pep-0008/), except where it contradicts the specific guidance below.

Python code style is enforced with the Ruff linter, see [linting](../testing/automated.md#linting-your-changes) for more information.

Authors should do their best to adhere to these standards in order to have the best chance of their contribution being accepted into NVDA.
In limited circumstances, NV Access may accept contributions that do not follow these coding standards.
If there is a reason you are unable to follow these standards in a contribution to NVDA, please make note of this when opening your PR.

## Encoding

* Python files should be encoded in UTF-8.
* Text files should be committed with `LF` line endings.
Files can be checked out locally using CRLF if needed for Windows development using [git](https://git-scm.com/book/en/v2/Customizing-Git-Git-Configuration#_core_autocrlf).

## Indentation

* Indentation must be done with tabs (one per level), not spaces.
* When splitting a single statement over multiple lines, just indent one or more additional levels.
  Don't use vertical alignment; i.e. lining up with the bracket on the previous line.
  * Be aware that this requires a new-line after an opening parenthesis/bracket/brace if you intend
    to split the statement over multiple lines.

## Identifier Names

* Use descriptive names
  * name constants to avoid "magic numbers" and hint at intent or origin of the value.
    Consider, what does this represent?
* Functions, variables, properties, etc. should use mixed case to separate words, starting with a lower case letter;
  * E.g. `speakText`.
* Boolean functions or variables
  * Use the positive form of the language.
    Avoid double negatives like `shouldNotDoSomething = False`
  * Start with a "question word" to hint at their boolean nature.
  * E.g. `shouldX`, `isX`, `hasX`
* Classes should use mixed case to separate words, starting with an upper case letter;
  * E.g. `BrailleHandler`.
* Constants should be all upper case, separating words with underscores;
  * E.g. `LANGS_WITH_CONJUNCT_CHARS`.
* Scripts (the targets of gestures) are prefixed with "script_", with subsequent words in camel case.
  * E.g. `script_cycleAudioDuckingMode`.
* Event handlers are prefixed with "event_", with subsequent words in camel case.
  Note, `object` and `action` are separated by underscores.
  * E.g.: `event_action` or `event_object_action`.
  * `object` refers to the class type that the `action` refers to.
  * Examples: `event_caret`, `event_appModule_gainFocus`
* Extension points:
  * `Action`
    * Prefixed with `pre_` or `post_` to specify that handlers are being notified before / after the
      action has taken place.
  * `Decider`
    * Prefixed with `should_` to turn them into a question, e.g. `should_doSomething`
  * `Filter`
    * Prefixed with `filter_`, e.g. `filter_displaySize_preRefresh`
    * Should describe the filtering action and the data being returned
    * Should communicate if the filtering happens before or after some action
* Enums should be formatted using the expected mix of the above, e.g.:

  ```python
  class ExampleGroupOfData(Enum):
      CONSTANT_VALUE_MEMBER = auto()
      @property
      def _formatMember(self): pass
  ```

## Translatable Strings

* All strings that could be presented to the user should be marked as translatable using the `_()` function
  * e.g. `_("Text review")`.
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

## Imports

* Unused imports should be removed where possible.
  * Anything imported into a (sub)module can also be imported from that submodule.
  * As a result, removing unused imports may break compatibility, and should be done in compatibility breaking releases (see `deprecations.md`).
* Unused imports will give a lint warning.
  These can be handled the following ways:
  * If these imports are intended to be imported from other modules, they can be included in a definition for `__all__`.
  This will override and define the symbols imported when performing a star import, e.g. `from module import *`.
  * Otherwise, with a comment like `# noqa: <explanation>`.

## Considering future backwards compatibility

When writing new code, consider how the code can be moved in future while retaining backwards compatibility.
Refer to the [limitations to retaining backwards compatibility](./deprecations.md#limitations-to-retaining-backwards-compatibility).

In summary:

* Avoid module level global variables.
Any module level variables should be prefixed with an underscore and be encapsulated, e.g. via getters and setters.
* Avoid code which executes at import time.
Instead use initializer functions.

## Docstrings

Docstrings should use [Sphinx format without types](https://sphinx-rtd-tutorial.readthedocs.io/en/latest/docstrings.html), and follow [PEP 257 conventions](https://peps.python.org/pep-0257/).

* All public functions, classes, and methods should have docstrings.
  Most internal functions, classes and methods should have docstrings, except where their purpose is clear from their name or code.
  * A function of more than a few lines of code is most likely not self-explanatory.
* Providing type information in docstrings is discouraged, instead use python's [type annotations](#type-hints).
* Class-level and module-level docstrings should contain a high-level overview of the class/module, optionally with usage examples and references to commonly used methods/functions and attributes.
* Document class constructors in `__init__`, not at the top of the class.
* Document class attributes and non-obvious public variables in a docstring immediately below the attribute being described.

NVDA formerly used [epytext](https://epydoc.sourceforge.net/manual-epytext.html) syntax for docstrings, which means there is inconsistent syntax used in the NVDA code base.
[#12971](https://github.com/nvaccess/nvda/issues/12971) exists to track converting epytext docstrings to Sphinx.

To learn more about reStructuredText, Sphinx and Python, check out the following links:

* [reStructuredText Primer from the Sphinx docs](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
* [reStructuredText markup from the Python Developer's Guide](https://devguide.python.org/documentation/markup/)
* [Sphynx' custom reStructuredText Directives](https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html)
* [Sphynx' Python Domain](https://www.sphinx-doc.org/en/master/usage/domains/python.html)

## Type hints

All new code contributions to NVDA should use [PEP 484-style type hints](https://peps.python.org/pep-0484/).
Type hints make reasoning about code much easier, and allow static analysis tools to catch common errors.

* All variables, attributes, properties, and function/method arguments and returns should have type hints.
  * There is no need to provide type hints for the `self` or `cls` arguments to object/class methods.
* Prefer union shorthand (`X | Y`) over explicitly using `typing.Union`.
  * Corollary: prefer `T | None` over `typing.Optional[T]`.

## Calling non-python code

When using parts of the Windows API, or parts of NVDA implemented in C++, it is necessary to use the [ctypes](https://docs.python.org/3/library/ctypes.html) library.

* When providing ctypes type information for foreign functions, structures and data types, prefer to use the same name as used in the external library.
  * E.g. `GetModuleFileName` not `getModuleFileName`, even though the latter is a more Pythonic function name.
  * Pythonic names should be reserved for wrappers that provide more pythonic access to functions.
* All Windows API functions, types and data structures should be defined in the `winBindings` package, in modules named according to the DLL which exports the function.
  * E.g. `winBindings.kernel32`.
* Ctypes code for nvdaHelper should be defined in the `NVDAHelper.localLib` module.

## Language choices

The NVDA community is large and diverse, and we have a responsibility to make everyone feel welcome in it.
As our [contributor code of conduct](../../CODE_OF_CONDUCT.md) says:

> Communities mirror the societies in which they exist and positive action is essential to counteract the many forms of inequality and abuses of power that exist in society.

The wording choices we make have power, and as a part of our responsibility to be welcoming and inclusive, it is up to us to make sure the way we communicate, including in code, does not negatively impact others.
Consequently, authors should avoid metaphors, euphemisms or other language with layers of meaning or negative history; avoid generalisations about people, cultures or countries; avoid ableist language; and use gender-inclusive terminology.
For example:

* Instead of master/slave, prefer leader/follower, primary/replica, or other terms as appropriate.
* Instead of blacklist and whitelist, prefer blocklist and allowlist.
* Instead of sanity check, prefer confidence check.
* Instead of dummy (value), prefer placeholder.
* When referring to a person of unknown gender (such as in docstrings), use they/them/theirs pronouns.
