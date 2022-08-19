
# Deprecations

## Background
The NVDA API must maintain compatibility with add-ons throughout yearly development cycles.
The first release of a year, i.e. `20XX.1`, is when the NVDA API can introduce breaking changes.

## Deprecations
Where possible, ensure the NVDA API maintains backwards compatibility.
If no removal is required or proposed, backwards compatibility can be maintained via the following snippet:

```py
import globalVars
def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "deprecatedSymbolName" and globalVars._allowDeprecatedAPI:
		# Note: this should only log in situations where it will not be excessively noisy.
		log.warning(
			"Importing deprecatedSymbolName from here is deprecated. "
			"Import X instead and do Y. "
		)
		# Ensure the API of deprecatedSymbolNameReplacement is the same as the deprecated symbol.
		return deprecatedSymbolNameReplacement
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
```


## Required API breaking changes
In order to improve the NVDA API, changes that will break future compatibility may be implemented, as long they retain backwards compatibility until the `20XX.1` release.

This can be done by using a version check to automate deprecation. For example, if you wish to replace usages of `foo` with `bar`. When we begin work on `NEXT_YEAR`, `foo` will no longer be part of the NVDA API and all internal usages must be removed prior. 
```python
from buildVersion import version_year
import globalVars
if version_year < NEXT_YEAR and globalVars._allowDeprecatedAPI:
	foo = bar
```

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

