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

from logHandler import log
from .util import HandlerRegistrar, callWithSupportedKwargs, BoundMethodWeakref  # noqa: F401
from typing import (
	Callable,
	Generator,
	Generic,
	Iterable,
	Set,
	TypeVar,
	Union,
)


class Action(HandlerRegistrar[Callable[..., None]]):
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

	def notify(self, **kwargs):
		"""Notify all registered handlers that the action has occurred.
		@param kwargs: Arguments to pass to the handlers.
		"""
		for handler in self.handlers:
			try:
				callWithSupportedKwargs(handler, **kwargs)
			except:  # noqa: E722
				log.exception("Error running handler %r for %r" % (handler, self))

	def notifyOnce(self, **kwargs):
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


FilterValueT = TypeVar("FilterValueT")


class Filter(
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

	def apply(self, value: FilterValueT, **kwargs) -> FilterValueT:
		"""Pass a value to be filtered through all registered handlers.
		The value is passed to the first handler
		and the return value from that handler is passed to the next handler.
		This process continues for all handlers until the final handler.
		The return value from the final handler is returned to the caller.
		@param value: The value to be filtered.
		@param kwargs: Arguments to pass to the handlers.
		@return: The filtered value.
		"""
		for handler in self.handlers:
			try:
				value = callWithSupportedKwargs(handler, value, **kwargs)
			except:  # noqa: E722
				log.exception("Error running handler %r for %r" % (handler, self))
		return value


class Decider(HandlerRegistrar[Callable[..., bool]]):
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

	def decide(self, **kwargs):
		"""Call handlers to make a decision.
		If a handler returns False, processing stops
		and False is returned.
		If there are no handlers or all handlers return True, True is returned.
		@param kwargs: Arguments to pass to the handlers.
		@return: The decision.
		@rtype: bool
		"""
		for handler in self.handlers:
			try:
				decision = callWithSupportedKwargs(handler, **kwargs)
			except:  # noqa: E722
				log.exception("Error running handler %r for %r" % (handler, self))
				continue
			if not decision:
				return False
		return True


class AccumulatingDecider(HandlerRegistrar[Callable[..., bool]]):
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
		super().__init__()
		self.defaultDecision: bool = defaultDecision

	def decide(self, **kwargs) -> bool:
		"""Call handlers to make a decision.
		Results returned from all handlers are collected
		and if at least one handler returns value different than the one specifed as default it is returned.
		If there are no handlers or all handlers return the default value, the default value is returned.
		@param kwargs: Arguments to pass to the handlers.
		@return: The decision.
		"""
		decisions: Set[bool] = set()
		for handler in self.handlers:
			try:
				decisions.add(callWithSupportedKwargs(handler, **kwargs))
			except Exception:
				log.exception("Error running handler %r for %r" % (handler, self))
				continue
		if (not self.defaultDecision) in decisions:
			return not self.defaultDecision
		return self.defaultDecision


ChainValueTypeT = TypeVar("ChainValueTypeT")


class Chain(HandlerRegistrar[Callable[..., Iterable[ChainValueTypeT]]], Generic[ChainValueTypeT]):
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

	def iter(self, **kwargs) -> Generator[ChainValueTypeT, None, None]:
		"""Returns a generator yielding all values generated by the registered handlers.
		@param kwargs: Arguments to pass to the handlers.
		"""
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
