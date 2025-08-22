from importlib import import_module
from types import ModuleType
import NVDAState
from collections.abc import Callable
from typing import Any
from logHandler import log
import inspect
import sys


def _getCallerModule(level: int = 0) -> ModuleType:
	return inspect.getmodule(inspect.stack()[level + 1].frame) or sys.modules["__main__"]


def handleMovedSymbols(
	moved: dict[str, tuple[str, ...]] | None,
) -> Callable[[str], Any]:
	modName = _getCallerModule(1).__name__

	def module_getattr(attrName: str) -> Any:
		if NVDAState._allowDeprecatedAPI():
			# Symbols that have simply been moved elsewhere
			if moved is not None and attrName in moved:
				newModule, *newPath = moved[attrName]
				newPath = newPath or [attrName]
				log.warning(
					f"{modName}.{attrName} is deprecated. Use {newModule}.{'.'.join(newPath)} instead.",
					stack_info=True,
				)
				value = import_module(newModule)
				for segment in newPath:
					value = getattr(value, segment)
				return value

			# Other symbols
			match attrName:
				case "INVALID_HANDLE_VALUE":
					log.warning(f"hwPortUtils.{attrName} is deprecated.", stack_info=True)
					return 0
				case _:
					pass
		raise AttributeError(f"module {__name__!r} has no attribute {attrName!r}")

	return module_getattr
