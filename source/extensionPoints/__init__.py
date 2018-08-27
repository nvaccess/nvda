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
See the L{Action}, L{Filter}, L{Decider} classes.
Actions can be grouped in a container using the L{ActionContainer} class.
"""
from logHandler import log
from .util import HandlerRegistrar, callWithSupportedKwargs, BoundMethodWeakref
from fnmatch import fnmatch
from collections import MutableMapping, OrderedDict


class Action(HandlerRegistrar):
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
			except:
				log.exception("Error running handler %r for %r" % (handler, self))

class ActionContainer(MutableMapping):
	"""Bundles a collection of actions together in a container,
	and allows interested parties to register to be notified when one or more actions occur.

	First, an ActionContainer is created:

	>>> actions= extensionPoints.ActionContainer()

	Interested parties then register to be notified about an action, see
	L{Action.register} docstring for details of the type of handlers that can be
	registered:

	>>> def onSomethingHappened(someArg=None):
		... 	print(someArg)
	...
	>>> actions.register('somethingHappened', onSomethingHappened)

	When the action is performed, register handlers are notified, see L{util.callWithSupportedKwargs}
	for how args passed to notify are mapped to the handler:

	>>> actions.notify('somethingHappened', someArg=42)

	Alternatively, you can use Unix filename pattern matching rules
	to create an action that will be notified for multiple action names.

	>>> actions.register('something*', onSomethingRandom)

	Then, Calling notify for 'somethingHappened' will trigger both 'somethingHappened' and 'something*'
	"""

	def __getitem__(self, key):
		return self._actions[key]

	def __contains__(self, key):
		return key in self._actions

	def __setitem__(self, key, val):
		if not isinstance(key, basestring):
			raise TypeError("Keys in an ActionContainer should be of type basestring")
		if not isinstance(val, Action):
			raise TypeError("You can only add items of type Action to an ActionContainer")
		self._actions[key] = val

	def __delitem__(self, key):
		del self._actions[key]
		if key in self._wildcards:
			self._wildcards.remove(actionName)

	def __iter__(self):
		return iter(self._actions)

	def __len__(self):
		return len(self._actions)

	def __init__(self):
		#: Registered actions.
		#: This is an OrderedDict where the keys are names
		#: and the values are instances of L{Action}.
		self._actions = OrderedDict()
		#: Actions that are registered as wildcard actions.
		self._wildcards = set()

	def addAction(self, actionName, isWildcard=False):
		"""Adds an action to this L{ActionContainer}.
		To delete an action, call "del self[actionName]"
		@param actionName: The name of the action to be created.
		@type actionName: str
		@param isWildcard: Whether the action name should be treated as a wildcard name.
			For example, when the actionName is 'msg_*',
			and L{notify} is called for the 'msg_notify' action,
			handlers for both 'msg_notify' and 'msg_*' will be notified.
		@type isWildcard: bool
		"""
		if actionName in self:
			raise ValueError("Action with name %s already exists" % actionName)
		self[actionName] = Action()
		if isWildcard:
			self._wildcards.add(actionName)

	def register(self, actionName, handler, createAction=True, isWildcard=False):
		"""Allows the registration of handlers for a specified action name.
		@param actionName: The name of the action for which a handler should be registered.
		@type actionName: str
		@param handler: The handler that should be registered with this action.
			Conditions should match those required by L{HandlerRegistrar.register}.
		@param createAction: Whether a new action should be automatically created
			if there isn't an action for the specified action name.
		@type createAction: bool
		@param isWildcard: Whether the action name should be treated as a wildcard name.
			For example, when the actionName is 'msg_*',
			and L{notify} is called for the 'msg_notify' action,
			handlers for both 'msg_notify' and 'msg_*' will be notified.
		@type isWildcard: bool
		"""
		if actionName not in self:
			if not createAction:
				raise ValueError("An action with name %s does not exist" % actionName)
			self.createAction(actionName, isWildcard=isWildcard)
		elif isWildcard and actionName not in self._wildcards:
			raise RuntimeError("Specified isWilrdcard for existing action %s that isn't a wildcard" % actionName)
		self[actionName].register(handler)

	def unregister(self, actionName, handler):
		if actionName not in self:
			raise ValueError("An action with name %s does not exist" % actionName)
		self[actionName].unregister(handler)

	def notify(self, actionName, **kwargs):
		"""Notify all registered handlers that the action has occurred.
		@param actionName: The name of the action for which the handlers should be notified.
			If there is a registered wildcard action which name matches L{actionName},
			the handlers for that action are notified as well.
		@type actionName: str
		@param kwargs: Arguments to pass to the handlers.
			The actionName is also provided when calling the handlers.
		"""
		try:
			actions = [self[actionName]]
		except KeyError:
			actions = []
		actions.extend(
			self[wildcardName] for wildcardName in self._wildcards if
			wildcardName != actionName and
			fnmatch(actionName, wildcardName)
		)
		if not actions:
			raise ValueError("No action registered matching name %s" % actionName)
		for action in actions:
			action.notify(actionName=actionName, **kwargs)

class Filter(HandlerRegistrar):
	"""Allows interested parties to register to modify a specific kind of data.
	For example, this might be used to allow modification of spoken messages before they are passed to the synthesizer.

	First, a Filter is created:

	>>> messageFilter = extensionPoints.Filter()

	Interested parties then register to filter the data, see
	L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def filterMessage(message, someArg=None):
	... 	return message + " which has been filtered."
	...
	>>> messageFilter.register(filterMessage)

	When filtering is desired, all registered handlers are called to filter the data, see L{util.callWithSupportedKwargs}
	for how args passed to notify are mapped to the handler:

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

	Interested parties then register to participate in the decision, see
	L{register} docstring for details of the type of handlers that can be
	registered:

	>>> def shouldDoSomething(someArg=None):
	... 	return False
	...
	>>> doSomething.register(shouldDoSomething)

	When the decision is to be made, registered handlers are called until
	a handler returns False, see L{util.callWithSupportedKwargs}
	for how args passed to notify are mapped to the handler:

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
