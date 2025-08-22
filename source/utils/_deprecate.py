from importlib import import_module
from types import ModuleType
import NVDAState
from collections.abc import Callable
from typing import Any
from logHandler import log
import inspect
import sys
from abc import ABC, abstractmethod, abstractproperty


class DeprecatedSymbol(ABC):
	name: str

	def __init__(self, name: str):
		self.name = name

	@abstractmethod
	def logMessage(self, moduleName: str) -> str: ...

	@abstractproperty
	def value(self) -> Any: ...


class MovedSymbol(DeprecatedSymbol):
	newModule: str
	newPath: tuple[str, ...]

	def __init__(self, name: str, newModule: str, *newPath: str):
		super().__init__(name)
		self.newModule = newModule
		self.newPath = newPath if newPath else (name,)

	def logMessage(self, moduleName: str) -> str:
		return (
			f"{moduleName}.{self.name} is deprecated. Use {self.newModule}.{'.'.join(self.newPath)} instead."
		)

	@property
	def value(self):
		value = import_module(self.newModule)
		for segment in self.newPath:
			value = getattr(value, segment)
		return value


class RemovedSymbol(DeprecatedSymbol):
	def __init__(self, name: str, value: Any, *, message: str = "No public replacement is planned."):
		super().__init__(name)
		self._value = value
		self._extraMessage = message

	@property
	def value(self) -> Any:
		return self._value

	def logMessage(self, moduleName: str) -> str:
		return f"{moduleName}.{self.name} is deprecated. {self._extraMessage}"


def _getCallerModule(level: int = 0) -> ModuleType:
	return inspect.getmodule(inspect.stack()[level + 1].frame) or sys.modules["__main__"]


def handleDeprecations(
	*deprecated: DeprecatedSymbol,
) -> Callable[[str], Any]:
	modName = _getCallerModule(1).__name__
	deprecatedSymbols = {symbol.name: symbol for symbol in deprecated}

	def module_getattr(attrName: str) -> Any:
		if NVDAState._allowDeprecatedAPI():
			# Symbols that have simply been moved elsewhere
			if attrName in deprecatedSymbols:
				deprecatedSymbol = deprecatedSymbols[attrName]
				log.warning(
					deprecatedSymbol.logMessage(modName),
					stack_info=True,
				)
				return deprecatedSymbol.value
		raise AttributeError(f"module {modName!r} has no attribute {attrName!r}")

	return module_getattr
