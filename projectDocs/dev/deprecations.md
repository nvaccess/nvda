# Deprecations

## Background

The NVDA API must maintain compatibility with add-ons throughout yearly development cycles.
The first release of a year, i.e. `20XX.1`, is when the NVDA API can introduce breaking changes.

## Deprecating module attributes

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

## Deprecating extension points

Support for deprecations is included in the various extensionPoint classes.

For example:

```python
filter_something = extensionPoints.Filter[int](
	_deprecationMessage="filter_something is deprecated. Use filter_somethingElse instead.",
)
```

The deprecation message is logged at the warning level when calling `register` on a `HandlerRegistrar`.
When `NVDAState._allowDeprecatedAPI()` returns `False`, a `RuntimeError` is raised instead.

## Required API breaking changes

In order to improve the NVDA API, changes that will break future compatibility may be implemented, as long as they retain backwards compatibility until the `20XX.1` release.

This can be done by using a version check to automate deprecation.
For example, if you wish to replace usages of `deprecatedSymbolName` with `newSymbolName`.
When we begin work on `NEXT_YEAR`, we update `BACK_COMPAT_TO`, which introduces the add-on API breakage warning.
At this stage, `deprecatedSymbolName` will no longer be part of the NVDA API and all internal usages must be removed prior.

```python
from addonAPIVersion import BACK_COMPAT_TO
import NVDAState
if BACK_COMPAT_TO < (NEXT_YEAR, 1, 0) and NVDAState._allowDeprecatedAPI():
	deprecatedSymbolName = newSymbolName
```

## Limitations to retaining backwards compatibility

These snippets do not support re-assignment to `deprecatedSymbolName`.
As a result, it not possible to retain backwards compatibility for module level variables which are expected to support assignment.

For example, if there is a global variable named `currentState` in `exampleModule.py`, `currentState` cannot be deprecated.

This is because:

* `__getattr__` only fetches variables which are not defined on the module level.
As such, setting an attribute that is fetched via `__getattr__` will prevent `__getattr__` from fetching the attribute.
Any future gets will fetch the newly assigned value.
* Python does not have an equivalent module level `__setattr__` like the `__getattr__` example.
* Encapsulating a module level variable into another data structure changes the import behaviour.
  * e.g. if `exampleModule` became a class, so `exampleModule.currentState` was a class level variable with the same namespace as the deprecated symbol, `exampleModule` may not be importable in the same manner.

As a result, module level variables should be avoided.

## Testing backwards compatibility

To ensure a module retains the same symbol names being importable, check across versions what is imported using the NVDA python console.

```python
import controlTypes
dir(controlTypes)
```

Changes different to moving or renaming symbols need to be considered carefully with a different approach.

Any API breaking changes such as deprecations marked for removal should be commented with the year of intended removal, and notes on how to implement the API change as an add-on developer and NVDA developer.

## Announcements

Deprecations should be announced via the [NVDA API mailing list](https://groups.google.com/a/nvaccess.org/g/nvda-api/about).
