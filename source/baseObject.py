#baseObject.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Contains the base classes that many of NVDA's classes such as NVDAObjects, virtualBuffers, appModules, synthDrivers inherit from. These base classes provide such things as auto properties, and methods and properties for scripting and key binding.
"""

import weakref
from logHandler import log

class Getter(object):

	def __init__(self,fget):
		self.fget=fget

	def __get__(self,instance,owner):
		if not instance:
			return self
		return self.fget(instance)

	def setter(self,func):
		return property(fget=self._func,fset=func)

	def deleter(self,func):
		return property(fget=self._func,fdel=func)

class CachingGetter(Getter):

	def __get__(self, instance, owner):
		if not instance:
			return self
		return instance._getPropertyViaCache(self.fget)

class AutoPropertyType(type):

	def __init__(self,name,bases,dict):
		super(AutoPropertyType,self).__init__(name,bases,dict)

		cacheByDefault=False
		try:
			cacheByDefault=dict["cachePropertiesByDefault"]
		except KeyError:
			cacheByDefault=any(getattr(base, "cachePropertiesByDefault", False) for base in bases)

		props=(x[5:] for x in dict.keys() if x[0:5] in ('_get_','_set_','_del_'))
		for x in props:
			g=dict.get('_get_%s'%x,None)
			s=dict.get('_set_%s'%x,None)
			d=dict.get('_del_%s'%x,None)
			if x in dict:
				methodsString=",".join([str(i) for i in g,s,d if i])
				raise TypeError("%s is already a class attribute, cannot create descriptor with methods %s"%(x,methodsString))
			if not g:
				# There's a setter or deleter, but no getter.
				# This means it could be in one of the base classes.
				for base in bases:
					g = getattr(base,'_get_%s'%x,None)
					if g:
						break

			cache=dict.get('_cache_%s'%x,None)
			if cache is None:
				# The cache setting hasn't been specified in this class, but it could be in one of the bases.
				for base in bases:
					cache = getattr(base,'_cache_%s'%x,None)
					if cache is not None:
						break
				else:
					cache=cacheByDefault

			if g and not s and not d:
				setattr(self,x,(CachingGetter if cache else Getter)(g))
			else:
				setattr(self,x,property(fget=g,fset=s,fdel=d))

class AutoPropertyObject(object):
	"""A class that dynamicly supports properties, by looking up _get_* and _set_* methods at runtime.
	_get_x will make property x with a getter (you can get its value).
	_set_x will make a property x with a setter (you can set its value).
	If there is a _get_x but no _set_x then setting x will override the property completely.
	Properties can also be cached for the duration of one core pump cycle.
	This is useful if the same property is likely to be fetched multiple times in one cycle. For example, several NVDAObject properties are fetched by both braille and speech.
	Setting _cache_x to C{True} specifies that x should be cached. Setting it to C{False} specifies that it should not be cached.
	If _cache_x is not set, L{cachePropertiesByDefault} is used.
	"""
	__metaclass__=AutoPropertyType

	#: Tracks the instances of this class; used by L{invalidateCaches}.
	#: @type: weakref.WeakKeyDictionary
	__instances=weakref.WeakKeyDictionary()
	#: Specifies whether properties are cached by default;
	#: can be overridden for individual properties by setting _cache_propertyName.
	#: @type: bool
	cachePropertiesByDefault = False

	def __init__(self):
		#: Maps properties to cached values.
		#: @type: dict
		self._propertyCache={}
		self.__instances[self]=None

	def _getPropertyViaCache(self,getterMethod=None):
		if not getterMethod:
			raise ValueError("getterMethod is None")
		try:
			val=self._propertyCache[getterMethod]
		except KeyError:
			val=getterMethod(self)
			self._propertyCache[getterMethod]=val
		return val

	def invalidateCache(self):
		self._propertyCache.clear()

	@classmethod
	def invalidateCaches(cls):
		"""Invalidate the caches for all current instances.
		"""
		# We use keys() here instead of iterkeys(), as invalidating the cache on an object may cause instances to disappear,
		# which would in turn cause an exception due to the dictionary changing size during iteration.
		for instance in cls.__instances.keys():
			instance.invalidateCache()

class ScriptableObject(AutoPropertyObject):
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
	@type scriptCategory: basestring
	"""

	def __init__(self):
		#: Maps input gestures to script functions.
		#: @type: dict
		self._gestureMap = {}
		# Bind gestures specified on the class.
		for cls in reversed(self.__class__.__mro__):
			try:
				self.bindGestures(getattr(cls, "_%s__gestures" % cls.__name__))
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
		# Don't store the instance method, as this causes a circular reference
		# and instance methods are meant to be generated on retrieval anyway.
		func = getattr(self.__class__, "script_%s" % scriptName, None)
		if not func:
			raise LookupError("No such script: %s" % func)
		# Import late to avoid circular import.
		import inputCore
		self._gestureMap[inputCore.normalizeGestureIdentifier(gestureIdentifier)] = func

	def removeGestureBinding(self,gestureIdentifier):
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
		"""Remove all input gesture bindings from this object.
		"""
		self._gestureMap.clear()

	def bindGestures(self, gestureMap):
		"""Bind or unbind multiple input gestures.
		This is a convenience method which simply calls L{bindGesture} for each gesture and script pair, logging any errors.
		For the case where script is None, L{removeGestureBinding} is called instead.
		@param gestureMap: A mapping of gesture identifiers to script names.
		@type gestureMap: dict of str to str
		"""
		for gestureIdentifier, scriptName in gestureMap.iteritems():
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

	def getScript(self,gesture):
		"""Retrieve the script bound to a given gesture.
		@param gesture: The input gesture in question.
		@type gesture: L{inputCore.InputGesture}
		@return: The script function or C{None} if none was found.
		@rtype: script function
		""" 
		for identifier in gesture.identifiers:
			try:
				# Convert to instance method.
				return self._gestureMap[identifier].__get__(self, self.__class__)
			except KeyError:
				continue
		else:
			return None

	#: A value for sleepMode which indicates that NVDA should fully sleep for this object;
	#: i.e. braille and speech via NVDA controller client is disabled and the user cannot disable sleep mode.
	SLEEP_FULL = "full"
