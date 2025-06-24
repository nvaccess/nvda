# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2023 NV Access Limited, Joseph Lee, Łukasz Golonka, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Framework to enable extensibility at specific points in the code.
This allows interested parties to register to be notified when some action occurs
or to modify a specific kind of data.
For example, you might wish to notify about a configuration profile switch
or allow modification of spoken messages before they are passed to the synthesizer.
See the L{Action}, L{Filter}, L{Decider} and L{AccumulatingDecider} classes.
"""

import inspect
import sys
from logHandler import log
from .util import HandlerRegistrar, callWithSupportedKwargs, BoundMethodWeakref  # noqa: F401
from typing import (
	Any,
	Callable,
	Generator,
	Generic,
	Iterable,
	Optional,
	Set,
	TypeVar,
	Union,
)


def _getExtensionPointName(obj) -> Optional[str]:
	"""Automatically determine extension point name from its location in code."""
	try:
		# Get the frame where the extension point was created
		frame = inspect.currentframe()
		while frame:
			frame = frame.f_back
			if frame is None:
				break
			
			# Look for the frame that's not in extensionPoints module
			module_name = frame.f_globals.get('__name__', '')
			if not module_name.startswith('extensionPoints'):
				# Found the calling module, now find the variable name
				for var_name, var_value in frame.f_locals.items():
					if var_value is obj:
						return f"{module_name}.{var_name}"
				
				# If not found in locals, check globals
				for var_name, var_value in frame.f_globals.items():
					if var_value is obj:
						return f"{module_name}.{var_name}"
				break
	except Exception:
		log.debugWarning("Failed to auto-detect extension point name", exc_info=True)
	
	return None


def _invokeART(
	extensionPointName: str, 
	epType: str, 
	*args: Any, 
	**kwargs: Any
) -> Any:
	"""Invoke ART handlers for an extension point."""
	try:
		# Import here to avoid circular imports
		from art.manager import getARTManager
		artManager = getARTManager()
		if artManager:
			extProxy = artManager.getExtensionPointProxy()
			if extProxy:
				return extProxy.invokeHandlers(
					extensionPointName,
					epType,
					*args,
					**kwargs
				)
	except Exception:
		log.debugWarning("Error invoking ART handlers", exc_info=True)
	
	# Return appropriate default for the extension point type
	if epType == "action":
		return None
	elif epType in ("decider", "accumulating_decider"):
		return True
	elif epType == "filter":
		return args[0] if args else None
	elif epType == "chain":
		return []
	return None


class _ExtensionPointBase:
	"""Base class for extension points that handles automatic naming."""
	
	def __init__(self):
		self._extensionPointName: Optional[str] = None
		# Try to auto-detect the name
		self._extensionPointName = _getExtensionPointName(self)
	
	def setName(self, name: str) -> None:
		"""Manually set the extension point name."""
		self._extensionPointName = name
	
	def getName(self) -> Optional[str]:
		"""Get the extension point name."""
		return self._extensionPointName


class Action(_ExtensionPointBase, HandlerRegistrar[Callable[..., None]]):
	"""Allows interested parties to register to be notified when some action occurs.
	For example, this might be used to notify that the configuration profile has been switched.

	First, an Action is created:

	>>> somethingHappened = extensionPoints.Action()

	Interested parties then register to be notified about this action, see
	L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def onSomethingHappened(someArg=None):
		... 	print(someArg)
	...
	>>> somethingHappened.register(onSomethingHappened)

	When the action is performed, register handlers are notified, see L{util.callWithSupportedKwargs}
	for how args passed to notify are mapped to the handler:

	>>> somethingHappened.notify(someArg=42)
	"""

	def __init__(self) -> None:
		_ExtensionPointBase.__init__(self)
		HandlerRegistrar.__init__(self)

	def notify(self, **kwargs: Any) -> None:
		"""Notify all registered handlers that the action has occurred.
		@param kwargs: Arguments to pass to the handlers.
		"""
		# Notify NVDA core handlers
		for handler in self.handlers:
			try:
				callWithSupportedKwargs(handler, **kwargs)
			except:  # noqa: E722
				log.exception("Error running handler %r for %r" % (handler, self))
		
		# Notify ART handlers
		if self._extensionPointName:
			_invokeART(self._extensionPointName, "action", **kwargs)

	def notifyOnce(self, **kwargs: Any) -> None:
		"""Notify all registered handlers that the action has occurred.
		Unregister handlers after calling.
		@param kwargs: Arguments to pass to the handlers.
		"""
		oldHandlers = list(self.handlers)
		for handler in oldHandlers:
			try:
				callWithSupportedKwargs(handler, **kwargs)
				self.unregister(handler)
			except Exception as e:
				log.exception(f"Error running handler {handler} for {self}. Exception {e}")
		
		# Notify ART handlers (don't unregister ART handlers - they're managed separately)
		if self._extensionPointName:
			_invokeART(self._extensionPointName, "action", **kwargs)


FilterValueT = TypeVar("FilterValueT")


class Filter(
	_ExtensionPointBase,
	HandlerRegistrar[Union[Callable[..., FilterValueT], Callable[[FilterValueT], FilterValueT]]],
	Generic[FilterValueT],
):
	"""Allows interested parties to register to modify a specific kind of data.
	For example, this might be used to allow modification of spoken messages before they are passed to the synthesizer.

	First, a Filter is created:

	>>> import extensionPoints
	>>> messageFilter = extensionPoints.Filter[str]()

	Interested parties then register to filter the data, see
	L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def filterMessage(message: str, someArg=None) -> str:
	... 	return message + " which has been filtered."
	...
	>>> messageFilter.register(filterMessage)

	When filtering is desired, all registered handlers are called to filter the data, see L{util.callWithSupportedKwargs}
	for how args passed to apply are mapped to the handler:

	>>> messageFilter.apply("This is a message", someArg=42)
	'This is a message which has been filtered'
	"""

	def __init__(self, **kwargs) -> None:
		_ExtensionPointBase.__init__(self)
		HandlerRegistrar.__init__(self, **kwargs)

	def apply(self, value: FilterValueT, **kwargs: Any) -> FilterValueT:
		"""Pass a value to be filtered through all registered handlers.
		The value is passed to the first handler
		and the return value from that handler is passed to the next handler.
		This process continues for all handlers until the final handler.
		The return value from the final handler is returned to the caller.
		@param value: The value to be filtered.
		@param kwargs: Arguments to pass to the handlers.
		@return: The filtered value.
		"""
		# Apply NVDA core filters
		for handler in self.handlers:
			try:
				value = callWithSupportedKwargs(handler, value, **kwargs)
			except:  # noqa: E722
				log.exception("Error running handler %r for %r" % (handler, self))
		
		# Apply ART filters
		if self._extensionPointName:
			artResult = _invokeART(self._extensionPointName, "filter", value, **kwargs)
			if artResult is not None:
				value = artResult
		
		return value


class Decider(_ExtensionPointBase, HandlerRegistrar[Callable[..., bool]]):
	"""Allows interested parties to participate in deciding whether something
	should be done.
	For example, input gestures are normally executed,
	but this might be used to prevent their execution
	under specific circumstances such as when controlling a remote system.

	First, a Decider is created:

	>>> doSomething = extensionPoints.Decider()

	Interested parties then register to participate in the decision, see
	L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def shouldDoSomething(someArg=None):
	... 	return False
	...
	>>> doSomething.register(shouldDoSomething)

	When the decision is to be made, registered handlers are called until
	a handler returns False, see L{util.callWithSupportedKwargs}
	for how args passed to decide are mapped to the handler:

	>>> doSomething.decide(someArg=42)
	False

	If there are no handlers or all handlers return True,
	the return value is True.
	"""

	def __init__(self) -> None:
		_ExtensionPointBase.__init__(self)
		HandlerRegistrar.__init__(self)

	def decide(self, **kwargs: Any) -> bool:
		"""Call handlers to make a decision.
		If a handler returns False, processing stops
		and False is returned.
		If there are no handlers or all handlers return True, True is returned.
		@param kwargs: Arguments to pass to the handlers.
		@return: The decision.
		@rtype: bool
		"""
		# Check NVDA core handlers first
		for handler in self.handlers:
			try:
				decision = callWithSupportedKwargs(handler, **kwargs)
			except:  # noqa: E722
				log.exception("Error running handler %r for %r" % (handler, self))
				continue
			if not decision:
				return False
		
		# Check ART handlers
		if self._extensionPointName:
			artDecision = _invokeART(self._extensionPointName, "decider", **kwargs)
			if not artDecision:
				return False
		
		return True


class AccumulatingDecider(_ExtensionPointBase, HandlerRegistrar[Callable[..., bool]]):
	"""Allows interested parties to participate in deciding whether something
	should be done.
	In contrast with L{Decider} all handlers are executed and then results are returned.
	For example, normally user should be warned about all command line parameters
	which are unknown to NVDA, but this extension point can be used to pass each unknown parameter
	to all add-ons since one of them may want to process some command line arguments.

	First, an AccumulatingDecider is created with a default decision  :

	>>> doSomething = AccumulatingDecider(defaultDecision=True)

	Interested parties then register to participate in the decision, see
	L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def shouldDoSomething(someArg=None):
	... 	return False
	...
	>>> doSomething.register(shouldDoSomething)

	When the decision is to be made registered handlers are called and their return values are collected,
	see L{util.callWithSupportedKwargs}
	for how args passed to decide are mapped to the handler:

	>>> doSomething.decide(someArg=42)
	False

	If there are no handlers or all handlers return defaultDecision,
	the return value is the value of the default decision.
	"""

	def __init__(self, defaultDecision: bool) -> None:
		_ExtensionPointBase.__init__(self)
		HandlerRegistrar.__init__(self)
		self.defaultDecision: bool = defaultDecision

	def decide(self, **kwargs: Any) -> bool:
		"""Call handlers to make a decision.
		Results returned from all handlers are collected
		and if at least one handler returns value different than the one specifed as default it is returned.
		If there are no handlers or all handlers return the default value, the default value is returned.
		@param kwargs: Arguments to pass to the handlers.
		@return: The decision.
		"""
		decisions: Set[bool] = set()
		
		# Collect decisions from NVDA core handlers
		for handler in self.handlers:
			try:
				decisions.add(callWithSupportedKwargs(handler, **kwargs))
			except Exception:
				log.exception("Error running handler %r for %r" % (handler, self))
				continue
		
		# Collect decision from ART handlers
		if self._extensionPointName:
			artDecision = _invokeART(self._extensionPointName, "accumulating_decider", **kwargs)
			if isinstance(artDecision, bool):
				decisions.add(artDecision)
		
		if (not self.defaultDecision) in decisions:
			return not self.defaultDecision
		return self.defaultDecision


ChainValueTypeT = TypeVar("ChainValueTypeT")


class Chain(_ExtensionPointBase, HandlerRegistrar[Callable[..., Iterable[ChainValueTypeT]]], Generic[ChainValueTypeT]):
	"""Allows creating a chain of registered handlers.
	The handlers should return an iterable, e.g. they are usually generator functions,
	but returning a list is also supported.

	First, a Chain is created:

	>>> chainOfNumbers = extensionPoints.Chain[int]()

	Interested parties then register to be iterated.
	See L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def yieldSomeNumbers(someArg=None) -> Generator[int, None, None]:
		... 	yield 1
		... 	yield 2
		... 	yield 3
	...
	>>> def yieldMoreNumbers(someArg=42) -> Generator[int, None, None]:
		... 	yield 4
		... 	yield 5
		... 	yield 6
	...
	>>> chainOfNumbers.register(yieldSomeNumbers)
	>>> chainOfNumbers.register(yieldMoreNumbers)

	When the chain is being iterated, it yields all entries generated by the registered handlers,
	see L{util.callWithSupportedKwargs} for how args passed to iter are mapped to the handler:

	>>> chainOfNumbers.iter(someArg=42)
	"""

	def __init__(self) -> None:
		_ExtensionPointBase.__init__(self)
		HandlerRegistrar.__init__(self)

	def iter(self, **kwargs: Any) -> Generator[ChainValueTypeT, None, None]:
		"""Returns a generator yielding all values generated by the registered handlers.
		@param kwargs: Arguments to pass to the handlers.
		"""
		# Yield from NVDA core handlers
		for handler in self.handlers:
			try:
				iterable = callWithSupportedKwargs(handler, **kwargs)
				if not isinstance(iterable, Iterable):
					log.exception(f"The handler {handler!r} on {self!r} didn't return an iterable")
					continue
				for value in iterable:
					yield value
			except Exception:
				log.exception(f"Error yielding value from handler {handler!r} for {self!r}")
		
		# Yield from ART handlers
		if self._extensionPointName:
			try:
				artResults = _invokeART(self._extensionPointName, "chain", **kwargs)
				if isinstance(artResults, Iterable):
					for value in artResults:
						yield value
			except Exception:
				log.exception(f"Error yielding values from ART handlers for {self!r}")


def registerExtensionPointsInModule(module_name: str) -> None:
	"""Register extension points in a module by scanning for them.
	This is a fallback for cases where automatic detection fails.
	"""
	try:
		if module_name not in sys.modules:
			return
		
		module = sys.modules[module_name]
		for attr_name in dir(module):
			attr_value = getattr(module, attr_name)
			if isinstance(attr_value, _ExtensionPointBase):
				if not attr_value.getName():
					attr_value.setName(f"{module_name}.{attr_name}")
					log.debug(f"Registered extension point: {module_name}.{attr_name}")
	except Exception:
		log.debugWarning(f"Failed to register extension points in module {module_name}", exc_info=True)


def registerAllExtensionPoints() -> None:
	"""Register all extension points in loaded modules.
	This should be called after NVDA modules are loaded.
	"""
	# Common modules that have extension points
	modules_to_scan = [
		'speech.speech',
		'braille',
		'inputCore',
		'config',
		'synthDriverHandler',
		'brailleDisplayDrivers',
		'eventHandler',
		'treeInterceptorHandler',
		'scriptHandler',
		'globalCommands',
		'gui.settingsDialogs',
		'addonHandler',
	]
	
	for module_name in modules_to_scan:
		registerExtensionPointsInModule(module_name)
	
	# Also scan any modules that start with common prefixes
	for module_name in list(sys.modules.keys()):
		if (module_name.startswith('appModules.') or 
		    module_name.startswith('globalPlugins.') or
		    module_name.startswith('synthDrivers.') or
		    module_name.startswith('brailleDisplayDrivers.')):
			registerExtensionPointsInModule(module_name)
