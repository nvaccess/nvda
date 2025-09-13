# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Utilities for handling deprecations in NVDA's public API."""

import inspect
import sys
from abc import ABC, abstractmethod, abstractproperty
from collections.abc import Callable
from importlib import import_module
from types import ModuleType
from typing import Any

import NVDAState


class DeprecatedSymbol(ABC):
	"""A deprecated symbol (variable, constant, function, class, etc).

	Concrete subclasses:

	:class:`MovedSymbol`
		A symbol that has been moved (renamed, moved to a different module, etc) in the public API.

	:class:`RemovedSymbol`
		A symbol that has been removed from the API (including symbols that have been made internal).
	"""

	name: str
	"""Name of the symbol.

	This should be a valid Python name.
	"""

	def __init__(self, name: str):
		"""Initialiser.

		:param name: Old name of the deprecated symbol.
		"""
		self.name = name

	@abstractmethod
	def getLogMessage(self, moduleName: str) -> str:
		"""
		Get the message to be output to the log when attempting to access this symbol.

		:param moduleName: Fully qualified module name from which the symbol is being accessed.
		:return: String to be output to the log.
		"""
		...

	@abstractproperty
	def value(self) -> Any:
		"""Value to be returned as the value of the deprecated symbol."""
		...


class MovedSymbol(DeprecatedSymbol):
	"""A symbol which has been moved (renamed or relocated) in the public API."""

	newModule: str
	"""Fully qualified module name from which the symbol should now be accessed."""

	newPath: tuple[str, ...]
	"""
	Path to access the new symbol from the new module.

	Each element of the path is an attribute of the last.
	The first element is an attribute of :attr:`newModule`.
	"""

	def __init__(self, name: str, newModule: str, *newPath: str):
		"""Initialiser.

		:param name: Old name of the symbol.
		:param newModule: Fully qualified name of the module from which the symbol should now be accessed.
		:param *newPath: Path by which the new symbol is accessed from the new module.
			If the new symbol is an attribute of the new module, this should just be the name of the new symbol.
			If the new symbol is part of a nested data structure (e.g. an enumeration),
			The first element should be an attribute of the new module,
			and each subsequent element should be an element of the previous element.
			If no path segments are provided, ``name`` is used.
		"""
		super().__init__(name)
		self.newModule = newModule
		self.newPath = newPath if newPath else (name,)

	def getLogMessage(self, moduleName: str) -> str:
		return (
			f"{moduleName}.{self.name} is deprecated. Use {self.newModule}.{'.'.join(self.newPath)} instead."
		)

	@property
	def value(self):
		# Get the new module in which the symbol is defined.
		value = import_module(self.newModule)
		# And iteratively drill down to get the actual symbol.
		for segment in self.newPath:
			value = getattr(value, segment)
		return value


class RemovedSymbol(DeprecatedSymbol):
	"""A symbol which has been removed from the public API."""

	def __init__(self, name: str, value: Any, *, message: str = "No public replacement is planned."):
		"""Initialiser.

		:param name: Old name of the symbol.
		:param value: Old value of the symbol.
		:param message: _description_, defaults to "No public replacement is planned."
		"""
		super().__init__(name)
		self._value = value
		self._extraMessage = message

	@property
	def value(self) -> Any:
		return self._value

	def getLogMessage(self, moduleName: str) -> str:
		return f"{moduleName}.{self.name} is deprecated. {self._extraMessage}"


def _getCallerModule(level: int = 0) -> ModuleType:
	"""Get the module from which this was called.

	..note::
		This function will not work on stackless python implementations,
		and may not work on implementations other than cpython.

	:param level: Number of stack frames to skip, defaults to ``0``.
		This can be used if calling from a helper function to skip the stack frame created by the helper.
	:return: The module from which this function was called.
	"""
	moduleName = inspect.stack()[level + 1].frame.f_globals["__name__"]
	return sys.modules[moduleName]


def handleDeprecations(
	*deprecated: DeprecatedSymbol,
) -> Callable[[str], Any]:
	"""Get a function that can be used as a module's ``__getattr__`` for handling deprecated symbols in the public API.

	:param *deprecated: Symbols deprecated in the calling module's namespace.
	:return: A function which can be used as a module's ``__getattr__``.
	"""
	# Get the name of the calling module.
	modName = _getCallerModule(1).__name__
	# Place the symbols into an indexable data structure for more efficient access.
	deprecatedSymbols = {symbol.name: symbol for symbol in deprecated}

	def module_getattr(attrName: str) -> Any:
		if NVDAState._allowDeprecatedAPI():
			if attrName in deprecatedSymbols:
				# Import late to avoid circular import
				from logHandler import log

				deprecatedSymbol = deprecatedSymbols[attrName]
				# TODO: #17783: switch to using warnings.warn when NVDA's support for it matures.
				log.warning(
					deprecatedSymbol.getLogMessage(modName),
					stack_info=True,
					# TODO: #18785: add stacklevel parameter so the stack trace is less noisy
				)
				return deprecatedSymbol.value
		raise AttributeError(f"module {modName!r} has no attribute {attrName!r}")

	return module_getattr
