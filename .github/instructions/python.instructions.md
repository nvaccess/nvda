---
applyTo: **/*.py, **/*.pyw
description: This file describes the Python code style for the project.
---

# Python code guidelines for NVDA

## Code Style

In general, Python contributions to NVDA should follow the PEP 8 style guide, except where it contradicts the specific guidance below.

## Indentation

Indentation must be done with tabs (one per level), not spaces.

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

* All strings that could be presented to the user should be translatable via one of the gettext functions
  * i.e. `_()`, `pgettext()`, `ngettext()` or `npgettext()`.
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
  * As a result, removing unused imports may break compatibility, and should be done in compatibility breaking releases.
* Unused imports will give a lint warning.
  These can be handled the following ways:
  * If these imports are intended to be imported from other modules, they can be included in a definition for `__all__`.
  This will override and define the symbols imported when performing a star import, e.g. `from module import *`.
  * Otherwise, with a comment like `# noqa: <explanation>`.

## Considering future backwards compatibility

When writing new code, consider how the code can be moved in future while retaining backwards compatibility.

In summary:

* Avoid module level global variables.
Any module level variables should be prefixed with an underscore and be encapsulated, e.g. via getters and setters.
* Avoid code which executes at import time.
Instead use initializer functions.

### Deprecating module attributes

Where possible, ensure the NVDA API maintains backwards compatibility.
To assist with a uniform approach, the `utils._deprecate` module provides a factory function, `handleDeprecations`, which returns a function suitable for use as a module's `__getattr__`.
Call `handleDeprecations` with any number of concrete `DeprecatedSymbol` objects to handle the logic for emitting a deprecation warning and returning the deprecated symbol.
The following `DeprecatedSymbol` subclasses are currently available:

* `MovedSymbol(name: str, newModule: str, *newPath: str)`: A symbol that has been moved to a different module, possibly under a different name or as part of a nested data structure.
If no `newPath` is given, it is assumed to be the same as the old path (i.e. the symbol was moved, but not renamed).
* `RemovedSymbol(name: str, value: Any, *, message: str)`: A symbol that has been removed (altogether or just from the public API).
Can optionally be provided with a message to direct API users to its (incompatible) replacement.

Consider the following example: module `foo` defines symbols `egg`, `sausage` and `spam`, but the following changes are to be made to its API:

* `foo.eggs` is to be moved to module `bar`, but keep its name.
* `foo.sausage` is to be moved to module `bar`, but as part of the `breakfastMeats` data structure.
* `foo.spam` is to be removed altogether.

The following code in `foo.py` would be used:

```python
from utils._deprecate import handleDeprecations, MovedSymbol, RemovedSymbol

__getattr__ = handleDeprecations(
	# `newPath` is not needed as it's the same
	MovedSymbol("eggs", "bar"),
	# `newPath` is needed, as it's `breakfastMeats.sausage`, not just `sausage`.
	MovedSymbol("sausage", "bar", "breakfastMeats", "sausage"),
	# Symbol marked internal (renamed to `foo._spam`) pending removal at end of deprecation grace period
	RemovedSymbol("spam", _spam),
)
"""Module level `__getattr__` used to preserve backward compatibility."""
```

### Deprecating extension points

Support for deprecations is included in the various extensionPoint classes.

For example:

```python
filter_something = extensionPoints.Filter[int](
	_deprecationMessage="filter_something is deprecated. Use filter_somethingElse instead.",
)
```

The deprecation message is logged at the warning level when calling `register` on a `HandlerRegistrar`.
When `NVDAState._allowDeprecatedAPI()` returns `False`, a `RuntimeError` is raised instead.

## Docstrings

Docstrings should use Sphinx format without types, and follow PEP 257 conventions.

* All public functions, classes, and methods should have docstrings.
  Most internal functions, classes and methods should have docstrings, except where their purpose is clear from their name or code.
  * A function of more than a few lines of code is most likely not self-explanatory.
* Providing type information in docstrings is discouraged, instead use python's type annotations.
* Class-level and module-level docstrings should contain a high-level overview of the class/module, optionally with usage examples and references to commonly used methods/functions and attributes.
* Document class constructors in `__init__`, not at the top of the class.
* Document class attributes and non-obvious public variables in a docstring immediately below the attribute being described.

NVDA formerly used epytext syntax for docstrings, which means there is inconsistent syntax used in the NVDA code base.
When updating docstrings, ensure the changed docstring uses Sphinx.

## Type hints

All new code contributions to NVDA should use PEP 484-style type hints.
Type hints make reasoning about code much easier, and allow static analysis tools to catch common errors.

* All variables, attributes, properties, and function/method arguments and returns should have type hints.
  * There is no need to provide type hints for the `self` or `cls` arguments to object/class methods.
* Prefer union shorthand (`X | Y`) over explicitly using `typing.Union`.
  * Corollary: prefer `T | None` over `typing.Optional[T]`.

## Calling non-python code

When using parts of the Windows API, or parts of NVDA implemented in C++, it is necessary to use the ctypes library.

* When providing ctypes type information for foreign functions, structures and data types, prefer to use the same name as used in the external library.
  * E.g. `GetModuleFileName` not `getModuleFileName`, even though the latter is a more Pythonic function name.
  * Pythonic names should be reserved for wrappers that provide more pythonic access to functions.
* All Windows API functions, types and data structures should be defined in the `winBindings` package, in modules named according to the DLL which exports the function.
  * E.g. `winBindings.kernel32`.
* Ctypes code for nvdaHelper should be defined in the `NVDAHelper.localLib` module.

## Language choices

The NVDA community is large and diverse, and we have a responsibility to make everyone feel welcome in it.
As our contributor code of conduct says:

> Communities mirror the societies in which they exist and positive action is essential to counteract the many forms of inequality and abuses of power that exist in society.

The wording choices we make have power, and as a part of our responsibility to be welcoming and inclusive, it is up to us to make sure the way we communicate, including in code, does not negatively impact others.
Consequently, authors should avoid metaphors, euphemisms or other language with layers of meaning or negative history; avoid generalisations about people, cultures or countries; avoid ableist language; and use gender-inclusive terminology.
For example:

* Instead of master/slave, prefer leader/follower, primary/replica, or other terms as appropriate.
* Instead of blacklist and whitelist, prefer blocklist and allowlist.
* Instead of sanity check, prefer confidence check.
* Instead of dummy (value), prefer placeholder.
* When referring to a person of unknown gender (such as in docstrings), use they/them/theirs pronouns.

## Security-specific review checks

NVDA operates with `UIAccess` privileges, injects code into other processes and handles untrusted data.
Scrutinize code for privilege escalation and data leaks.

* Secure mode, lock screens & installer limitations:
  * Check lock-screen object handling safeguards (e.g., secure object filtering).
  * Ensure `globalVars.appArgs.secure` is respected and blocked actions fail gracefully.
  * Check `NVDAState.shouldWriteToDisk`; do not write to disk/config if running securely or from the launcher.
  * Ensure no system or personal information is unintentionally exposed in secure screens or the lock screen.
* Subprocesses & file execution:
  * Flag any use of `subprocess`, `os.system`, or `os.startfile`.
  Because NVDA has UIAccess, these must use strictly sanitized arguments and absolute paths to prevent path/binary hijacking.
* Sensitive Data Logging:
  * Ensure new logging statements that are INFO level or higher do not capture sensitive user data, particularly from `protected` or password text fields, API keys, or secure desktop states.
  DEBUG level logging may include sensitive information such as the speech passed to a synthesizer.
* Untrusted input & web parsing:
  * Validate that parsing of external structures (HTML, ARIA attributes, UIA/IA2 properties) handles malformed, excessively long or deeply nested inputs safely without causing infinite loops or memory crashes.
  * Check for XSS e.g. from translators via translatable strings
* Network / Updates:
  * Any new HTTP/network requests must enforce secure connections (HTTPS) and validate server certificates except when updating certificates.

## Architecture / performance checks

* Verify thread safety.
GUI changes, core state mutations and most COM/UI interactions must happen on the main thread.
Ensure `wx.CallLater`, `wx.CallAfter`, `utils.schedule`, `core.callLater` or `queueHandler` are used when passing execution from background threads.
* Flag expensive operations (such as heavy computations, blocking I/O, complex loops) inside performance-critical hot paths like focus changes, key presses, or text iteration.
Watch for excessive COM calls (e.g. fetching properties individually inside a large loop instead of caching) and deep UIA tree walks on the main thread.
* For `ctypes` and COM interactions, ensure memory buffers, handles, and variants are safely freed to prevent memory leaks (e.g. using `ole32.CoTaskMemFree` or `kernel32.CloseHandle`).
