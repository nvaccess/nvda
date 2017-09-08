#extensionPoints.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Framework to enable extensibility at specific points in the code.
This allows interested parties to register to be notified when some action occurs
or to modify a specific kind of data.
For example, you might wish to notify about a configuration profile switch
or allow modification of spoken messages before they are passed to the synthesizer.
See the L{Action} and L{Filter} classes.
"""

import weakref
import collections
import inspect
from logHandler import log

class AnnotatableWeakref(weakref.ref):
	"""A weakref.ref which allows annotation with custom attributes.
	"""

class BoundMethodWeakref(object):
	"""Weakly references a bound instance method.
	Instance methods are bound dynamically each time they are fetched.
	weakref.ref on a bound instance method doesn't work because
	as soon as you drop the reference, the method object dies.
	Instead, this class holds weak references to both the instance and the function,
	which can then be used to bind an instance method.
	To get the actual method, you call an instance as you would a weakref.ref.
	"""

	def __init__(self, target, onDelete):
		def onRefDelete(weak):
			"""Calls onDelete for our BoundMethodWeakref when one of the individual weakrefs (instance or function) dies.
			"""
			onDelete(self)
		inst = target.__self__
		func = target.__func__
		self.weakInst = weakref.ref(inst, onRefDelete)
		self.weakFunc = weakref.ref(func, onRefDelete)

	def __call__(self):
		inst = self.weakInst()
		if not inst:
			return
		func = self.weakFunc()
		assert func, "inst is alive but func is dead"
		# Get an instancemethod by binding func to inst.
		return func.__get__(inst)

def _getHandlerKey(handler):
	"""Get a key which identifies a handler function.
	This is needed because we store weak references, not the actual functions.
	We store the key on the weak reference.
	When the handler dies, we can use the key on the weak reference to remove the handler.
	"""
	inst = getattr(handler, "__self__", None)
	if inst:
		return (id(inst), id(handler.__func__))
	return id(handler)

class HandlerRegistrar(object):
	"""Base class to Facilitate registration and unregistration of handler functions.
	The handlers are stored using weak references and are automatically unregistered
	if the handler dies.
	Both normal functions and instance methods are supported.
	The handlers are maintained in the order they were registered
	so that they can be called in a deterministic order across runs.
	This class doesn't provide any functionality to actually call the handlers.
	If you want to implement an extension point,
	you probably want the L{Action} or L{Filter} subclasses instead.
	"""

	def __init__(self):
		#: Registered handler functions.
		#: This is an OrderedDict where the keys are unique identifiers (as returned by _getHandlerKey)
		#: and the values are weak references.
		self._handlers = collections.OrderedDict()

	def register(self, handler):
		if hasattr(handler, "__self__"):
			weak = BoundMethodWeakref(handler, self.unregister)
		else:
			weak = AnnotatableWeakref(handler, self.unregister)
		key = _getHandlerKey(handler)
		# Store the key on the weakref so we can remove the handler when it dies.
		weak.handlerKey = key
		self._handlers[key] = weak

	def unregister(self, handler):
		if isinstance(handler, (AnnotatableWeakref, BoundMethodWeakref)):
			key = handler.handlerKey
		else:
			key = _getHandlerKey(handler)
		try:
			del self._handlers[key]
		except KeyError:
			return False
		return True

	@property
	def handlers(self):
		"""Generator of registered handler functions.
		This should be used when you want to call the handlers.
		"""
		for weak in self._handlers.values():
			handler = weak()
			if not handler:
				continue # Died.
			yield handler

def callWithSupportedKwargs(func, *args, **kwargs):
	"""Call a function with only the keyword arguments it supports.
	For example, if myFunc is defined as:
		def myFunc(a=None, b=None):
	and you call:
		callWithSupportedKwargs(myFunc, a=1, b=2, c=3)
	Instead of raising a TypeError, myFunc will simply be called like this:
		myFunc(a=1, b=2)
	"""
	spec = inspect.getargspec(func)
	if spec.keywords:
		# func has a catch-all for kwargs (**kwargs).
		return func(*args, **kwargs)
	# spec.defaults lists all arguments with defaults (keyword arguments).
	numKwargs = len(spec.defaults) if spec.defaults else 0
	# spec.args lists all arguments, first positional, then keyword.
	firstKwarg = len(spec.args) - numKwargs
	supportedKwargs = set(spec.args[firstKwarg:])
	for kwarg in kwargs.keys():
		if kwarg not in supportedKwargs:
			del kwargs[kwarg]
	return func(*args, **kwargs)

class Action(HandlerRegistrar):
	"""Allows interested parties to register to be notified when some action occurs.
	For example, this might be used to notify that the configuration profile has been switched.

	First, an Action is created:

	>>> somethingHappened = extensionPoints.Action()

	Interested parties then register to be notified about this action:

	>>> def onSomethingHappened(someArg=None):
		... 	print(someArg)
	...
	>>> somethingHappened.register(onSomethingHappened)

	When the action is performed, register handlers are notified:

	>>> somethingHappened.notify(someArg=42)
	"""

	def notify(self, **kwargs):
		"""Notify all registered handlers that the action has occurred.
		@param kwargs: Arguments to pass to the handlers.
		"""
		for handler in self.handlers:
			try:
				callWithSupportedKwargs(handler, **kwargs)
			except:
				log.exception("Error running handler %r for %r" % (handler, self))

class Filter(HandlerRegistrar):
	"""Allows interested parties to register to modify a specific kind of data.
	For example, this might be used to allow modification of spoken messages before they are passed to the synthesizer.

	First, a Filter is created:

	>>> messageFilter = extensionPoints.Filter()

	Interested parties then register to filter the data:

	>>> def filterMessage(message, someArg=None):
	... 	return message + " which has been filtered."
	...
	>>> messageFilter.register(filterMessage)

	When filtering is desired, all registered handlers are called to filter the data:

	>>> messageFilter.apply("This is a message", someArg=42)
	'This is a message which has been filtered'
	"""

	def apply(self, value, **kwargs):
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
			except:
				log.exception("Error running handler %r for %r" % (handler, self))
		return value

class Decider(HandlerRegistrar):
	"""Allows interested parties to participate in deciding whether something
	should be done.
	For example, input gestures are normally executed,
	but this might be used to prevent their execution
	under specific circumstances such as when controlling a remote system.

	First, a Decider is created:

	>>> doSomething = extensionPoints.Decider()

	Interested parties then register to participate in the decision:

	>>> def shouldDoSomething(someArg=None):
	... 	return False
	...
	>>> doSomething.register(shouldDoSomething)

	When the decision is to be made, registered handlers are called until
	a handler returns False:

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
			except:
				log.exception("Error running handler %r for %r" % (handler, self))
				continue
			if not decision:
				return False
		return True
