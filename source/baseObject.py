# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2022 NV Access Limited, Christopher Toth, Babbage B.V., Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Contains the base classes that many of NVDA's classes such as NVDAObjects, virtualBuffers, appModules, synthDrivers inherit from. These base classes provide such things as auto properties, and methods and properties for scripting and key binding."""

from typing import (
	Any,
	Callable,
	Optional,
	Set,
	Union,
)
import weakref
import garbageHandler
from logHandler import log
from abc import ABCMeta, abstractproperty

GetterReturnT = Any
GetterMethodT = Callable[["AutoPropertyObject"], GetterReturnT]


class Getter(object):
	def __init__(self, fget, abstract=False):
		self.fget = fget
		if abstract:
			self._abstract = self.__isabstractmethod__ = abstract

	def __get__(
		self,
		instance: Union[Any, None, "AutoPropertyObject"],
		owner,
	) -> Union[GetterReturnT, "Getter"]:
		if isinstance(self.fget, classmethod):
			return self.fget.__get__(instance, owner)()
		elif instance is None:
			return self
		return self.fget(instance)

	def setter(self, func):
		return (abstractproperty if self._abstract else property)(fget=self.fget, fset=func)

	def deleter(self, func):
		return (abstractproperty if self._abstract else property)(fget=self.fget, fdel=func)


class CachingGetter(Getter):
	def __get__(
		self,
		instance: Union[Any, None, "AutoPropertyObject"],
		owner,
	) -> Union[GetterReturnT, "CachingGetter"]:
		if isinstance(self.fget, classmethod):
			log.warning("Class properties do not support caching")
			return self.fget.__get__(instance, owner)()
		elif instance is None:
			return self
		return instance._getPropertyViaCache(self.fget)


class AutoPropertyType(ABCMeta):
	def __init__(self, name: str, bases: tuple[type, ...], namespace: dict[str, Any], /, **kwargs: Any):
		super().__init__(name, bases, namespace, **kwargs)

		cacheByDefault = False
		try:
			cacheByDefault = namespace["cachePropertiesByDefault"]
		except KeyError:
			cacheByDefault = any(getattr(base, "cachePropertiesByDefault", False) for base in bases)

		# Create a set containing properties that are marked as abstract.
		newAbstractProps = set()
		# Create a set containing properties that were, but are no longer abstract.
		oldAbstractProps = set()
		# given _get_myVal, _set_myVal, and _del_myVal: "myVal" would be output 3 times
		# use a set comprehension to ensure unique values, "myVal" only needs to occur once.
		props = {x[5:] for x in namespace.keys() if x[0:5] in ("_get_", "_set_", "_del_")}
		for x in props:
			g = namespace.get("_get_%s" % x, None)
			s = namespace.get("_set_%s" % x, None)
			d = namespace.get("_del_%s" % x, None)
			if x in namespace:
				methodsString = ",".join(str(i) for i in (g, s, d) if i)
				raise TypeError(
					"%s is already a class attribute, cannot create descriptor with methods %s"
					% (x, methodsString),
				)
			if not g:
				# There's a setter or deleter, but no getter.
				# This means it could be in one of the base classes.
				for base in bases:
					g = getattr(base, "_get_%s" % x, None)
					if g:
						break

			cache = namespace.get("_cache_%s" % x, None)
			if cache is None:
				# The cache setting hasn't been specified in this class, but it could be in one of the bases.
				for base in bases:
					cache = getattr(base, "_cache_%s" % x, None)
					if cache is not None:
						break
				else:
					cache = cacheByDefault if not isinstance(g, classmethod) else False

			abstract = namespace.get("_abstract_%s" % x, False)
			if g and not (s or d):
				attr = (CachingGetter if cache else Getter)(g, abstract)
			else:
				attr = (abstractproperty if abstract else property)(fget=g, fset=s, fdel=d)
			if abstract:
				newAbstractProps.add(x)
			elif x in self.__abstractmethods__:
				oldAbstractProps.add(x)
			setattr(self, x, attr)

		if newAbstractProps or oldAbstractProps:
			# The __abstractmethods__ set is frozen, therefore we ought to override it.
			self.__abstractmethods__ = (self.__abstractmethods__ | newAbstractProps) - oldAbstractProps


class AutoPropertyObject(garbageHandler.TrackedObject, metaclass=AutoPropertyType):
	"""A class that dynamically supports properties, by looking up _get_*, _set_*, and _del_* methods at runtime.
	_get_x will make property x with a getter (you can get its value).
	_set_x will make a property x with a setter (you can set its value).
	_del_x will make a property x with a deleter that is executed when deleting its value.
	If there is a _get_x but no _set_x then setting x will override the property completely.
	Properties can also be cached for the duration of one core pump cycle.
	This is useful if the same property is likely to be fetched multiple times in one cycle.
	For example, several NVDAObject properties are fetched by both braille and speech.
	Setting _cache_x to C{True} specifies that x should be cached.
	Setting it to C{False} specifies that it should not be cached.
	If _cache_x is not set, L{cachePropertiesByDefault} is used.
	Properties can also be made abstract.
	Setting _abstract_x to C{True} specifies that x should be abstract.
	Setting it to C{False} specifies that it should not be abstract.
	"""

	#: Tracks the instances of this class; used by L{invalidateCaches}.
	#: @type: weakref.WeakKeyDictionary
	__instances = weakref.WeakKeyDictionary()
	#: Specifies whether properties are cached by default;
	#: can be overridden for individual properties by setting _cache_propertyName.
	#: @type: bool
	cachePropertiesByDefault = False

	_propertyCache: Set[GetterMethodT]

	def __new__(cls, *args, **kwargs):
		self = super(AutoPropertyObject, cls).__new__(cls)
		#: Maps properties to cached values.
		#: @type: dict
		self._propertyCache = {}
		self.__instances[self] = None
		return self

	def _getPropertyViaCache(self, getterMethod: Optional[GetterMethodT] = None) -> GetterReturnT:
		if not getterMethod:
			raise ValueError("getterMethod is None")
		missing = False
		try:
			val = self._propertyCache[getterMethod]
		except KeyError:
			missing = True
		if missing:
			val = getterMethod(self)
			self._propertyCache[getterMethod] = val
		return val

	def invalidateCache(self):
		self._propertyCache.clear()

	@classmethod
	def invalidateCaches(cls):
		"""Invalidate the caches for all current instances."""
		# We use a list here, as invalidating the cache on an object may cause instances to disappear,
		# which would in turn cause an exception due to the dictionary changing size during iteration.
		for instance in list(cls.__instances):
			instance.invalidateCache()


class ScriptableType(AutoPropertyType):
	"""A metaclass used for collecting and caching gestures on a ScriptableObject"""

	def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any], /, **kwargs: Any):
		newCls = super().__new__(cls, name, bases, namespace, **kwargs)
		gesturesDictName = "_%s__gestures" % newCls.__name__
		# #8463: To avoid name mangling conflicts, create a copy of the __gestures dictionary.
		try:
			gestures = getattr(newCls, gesturesDictName).copy()
		except AttributeError:
			# This class currently has no gestures dictionary,
			# because no custom __gestures dictionary has been defined.
			gestures = {}
		for name, script in namespace.items():
			if not name.startswith("script_"):
				continue
			scriptName = name[len("script_") :]
			if hasattr(script, "gestures"):
				for gesture in script.gestures:
					gestures[gesture] = scriptName
		if gestures:
			setattr(newCls, gesturesDictName, gestures)
		return newCls


class ScriptableObject(AutoPropertyObject, metaclass=ScriptableType):
	"""A class that implements NVDA's scripting interface.
	Input gestures are bound to scripts such that the script will be executed when the appropriate input gesture is received.
	Scripts are methods named with a prefix of C{script_}; e.g. C{script_foo}.
	They accept an L{inputCore.InputGesture} as their single argument.
	Gesture bindings can be specified on the class by creating a C{__gestures} dict which maps gesture identifiers to script names.
	They can also be bound on an instance using the L{bindGesture} method.
	@cvar scriptCategory: If present, a translatable string displayed to the user
		as the category for scripts in this class;
		e.g. in the Input Gestures dialog.
		This can be overridden for individual scripts
		by setting a C{category} attribute on the script method.
	@type scriptCategory: str
	"""

	def __init__(self):
		#: Maps input gestures to script functions.
		#: @type: dict
		self._gestureMap = {}
		# Bind gestures specified on the class.
		# This includes gestures specified on decorated scripts.
		# This does not include the gestures that are added when creating a DynamicNVDAObjectType.
		for cls in reversed(self.__class__.__mro__):
			try:
				self.bindGestures(getattr(cls, "_%s__gestures" % cls.__name__))
			except AttributeError:
				pass
			try:
				self.bindGestures(cls._scriptDecoratorGestures)
			except AttributeError:
				pass
		super(ScriptableObject, self).__init__()

	def bindGesture(self, gestureIdentifier, scriptName):
		"""Bind an input gesture to a script.
		@param gestureIdentifier: The identifier of the input gesture.
		@type gestureIdentifier: str
		@param scriptName: The name of the script, which is the name of the method excluding the C{script_} prefix.
		@type scriptName: str
		@raise LookupError: If there is no script with the provided name.
		"""
		scriptAttrName = "script_%s" % scriptName
		# Don't store the instance method, as this causes a circular reference
		# and instance methods are meant to be generated on retrieval anyway.
		func = getattr(self.__class__, scriptAttrName, None)
		if not func:
			raise LookupError(
				"No such script on class {className}. Couldn't find attribute: {scriptAttrName}".format(
					className=self.__class__.__name__,
					scriptAttrName=scriptAttrName,
				),
			)
		# Import late to avoid circular import.
		import inputCore

		self._gestureMap[inputCore.normalizeGestureIdentifier(gestureIdentifier)] = func

	def removeGestureBinding(self, gestureIdentifier):
		"""
		Removes the binding for the given gesture identifier if a binding exists.
		@param gestureIdentifier: The identifier of the input gesture.
		@type gestureIdentifier: str
		@raise LookupError: If there is no binding for this gesture
		"""
		# Import late to avoid circular import.
		import inputCore

		del self._gestureMap[inputCore.normalizeGestureIdentifier(gestureIdentifier)]

	def clearGestureBindings(self):
		"""Remove all input gesture bindings from this object."""
		self._gestureMap.clear()

	def bindGestures(self, gestureMap):
		"""Bind or unbind multiple input gestures.
		This is a convenience method which simply calls L{bindGesture} for each gesture and script pair, logging any errors.
		For the case where script is None, L{removeGestureBinding} is called instead.
		@param gestureMap: A mapping of gesture identifiers to script names.
		@type gestureMap: dict of str to str
		"""
		for gestureIdentifier, scriptName in gestureMap.items():
			if scriptName:
				try:
					self.bindGesture(gestureIdentifier, scriptName)
				except LookupError:
					log.error("Error binding script %s in %r" % (scriptName, self))
			else:
				try:
					self.removeGestureBinding(gestureIdentifier)
				except LookupError:
					pass

	def getScript(self, gesture):
		"""Retrieve the script bound to a given gesture.
		@param gesture: The input gesture in question.
		@type gesture: L{inputCore.InputGesture}
		@return: The script function or C{None} if none was found.
		@rtype: script function
		"""
		for identifier in gesture.normalizedIdentifiers:
			try:
				# Convert to instance method.
				return self._gestureMap[identifier].__get__(self, self.__class__)
			except KeyError:
				continue
			except AttributeError:
				log.exception(
					(f"Base class may not have been initialized.\nMRO={self.__class__.__mro__}")
					if not hasattr(self, "_gestureMap")
					else None,
				)
				return None
		else:
			return None

	#: A value for sleepMode which indicates that NVDA should fully sleep for this object;
	#: i.e. braille and speech via NVDA controller client is disabled and the user cannot disable sleep mode.
	SLEEP_FULL = "full"
