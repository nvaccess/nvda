
# Deprecations

## Background
The NVDA API must maintain compatibility with add-ons throughout yearly development cycles.
The first release of a year, i.e. `20XX.1`, is when the NVDA API can introduce breaking changes.

## Deprecations
Where possible, ensure the NVDA API maintains backwards compatibility.
If no removal is required or proposed, backwards compatibility can be maintained via the following snippet:

```py
import NVDAState
def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "deprecatedSymbolName" and NVDAState._allowDeprecatedAPI():
		# Note: this should only log in situations where it will not be excessively noisy.
		log.warning(
			"Importing deprecatedSymbolName from here is deprecated. "
			"Import X instead and do Y. ",
			# Include stack info so testers can report warning to add-on author.
			stack_info=True,
		)
		# Ensure the API of deprecatedSymbolNameReplacement is the same as the deprecated symbol.
		return deprecatedSymbolNameReplacement
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
```

## Required API breaking changes
In order to improve the NVDA API, changes that will break future compatibility may be implemented, as long they retain backwards compatibility until the `20XX.1` release.

This can be done by using a version check to automate deprecation.
For example, if you wish to replace usages of `deprecatedSymbolName` with `newSymbolName`.
When we begin work on `NEXT_YEAR`, `deprecatedSymbolName` will no longer be part of the NVDA API and all internal usages must be removed prior. 

```python
from buildVersion import version_year
import NVDAState
if version_year < NEXT_YEAR and NVDAState._allowDeprecatedAPI():
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
	- e.g. if `exampleModule` became a class, so `exampleModule.currentState` was a class level variable with the same namespace as the deprecated symbol, `exampleModule` may not be importable in the same manner.

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
