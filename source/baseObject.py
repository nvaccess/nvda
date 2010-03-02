#baseObject.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Contains the base classes that many of NVDA's classes such as NVDAObjects, virtualBuffers, appModules, synthDrivers inherit from. These base classes provide such things as auto properties, and methods and properties for scripting and key binding.
"""

import weakref
from new import instancemethod
from keyUtils import key

class Getter(object):

	def __init__(self,fget):
		self.fget=fget

	def __get__(self,instance,owner):
		return self.fget(instance)

	def setter(self,func):
		return property(fget=self._func,fset=func)

	def deleter(self,func):
		return property(fget=self._func,fdel=func)

class CachingGetter(Getter):

	def __get__(self, instance, owner):
		return instance._getPropertyViaCache(self.fget)

class AutoPropertyType(type):

	def __init__(self,name,bases,dict):
		super(AutoPropertyType,self).__init__(name,bases,dict)
		try:
			useCache=any(issubclass(base,AutoPropertyCacheObject) for base in bases)
		except NameError:
			# AutoPropertyCacheObject hasn't been defined yet. This will occur when this metaclass is applied to AutoPropertyObject.
			useCache=False
		propSet=(x[5:] for x in dict.keys() if x[0:5] in ('_get_','_set_','_del_'))
		for x in propSet:
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
			if g and not s and not d:
				setattr(self,x,(CachingGetter if useCache else Getter)(g))
			else:
				setattr(self,x,property(fget=g,fset=s,fdel=d))

class AutoPropertyObject(object):

	"""A class that dynamicly supports properties, by looking up _get_* and _set_* methods at runtime.
 _get_x will make property x with a getter (you can get its value).
_set_x will make a property x with a setter (you can set its value).
If there is a _get_x but no _set_x then setting x will override the property completely.
"""
	__metaclass__=AutoPropertyType

class ScriptableObject(AutoPropertyObject):

	"""A class that implements NVDA's scripting interface. This allows the binding of keys to scripts (specially named methods that take a keyPress and a possible next script).
@ivar _keyMap: a dictionary of key strings to script name mappings
@type _keyMap: dict
"""

	@classmethod
	def bindKey(cls,keyName,scriptName):
		"""A class method that binds a key to a script (method starting with 'script_' in this class).
Note that the binding is performed on the class so that all future instances will have the binding. For runtime binding  on one particular instance use L{bindKey_runtime}.
@param keyName: the name of the key press you want to bind the script to (e.g. 'control+n')
@type keyName: string
 @param scriptName: the name of the script you want to bind the key press to (the name of the method with out the 'script_')
@type scriptName: string
"""
 		scriptName="script_%s"%scriptName
		if not hasattr(cls,scriptName):
			raise ValueError("no script \"%s\" in %s"%(scriptName,cls))
		if not cls.__dict__.has_key('_keyMap'):
			cls._keyMap=getattr(cls,'_keyMap',{}).copy()
		cls._keyMap[key(keyName)]=getattr(cls,scriptName)

	def bindKey_runtime(self,keyName,scriptName):
		"""Binds  a key to a script (method starting with 'script_' in this instance).
Note that the binding is performed on the instance, not the class. To bind on the class to affect all instances, use L{bindKey}.
 @param keyName: the name of the key press you want to bind the script to (e.g. 'control+n')
@type keyName: string
 @param scriptName: the name of the script you want to bind the key press to (the name of the method with out the 'script_')
@type scriptName: string
"""
		scriptName="script_%s"%scriptName
    		func=getattr(self.__class__,scriptName,None)
		if func:
            			self.bindKeyToFunc_runtime(keyName,func)
      		else:
			raise ValueError("no script \"%s\" in %s"%(scriptName,self))

	def bindKeyToFunc_runtime(self,keyName,func):
		"""Binds a key press for this instance to any arbitrary function.
Note that the binding is performed on this instance, not the instance's class.
@param keyName: the name of the key press you want to bind the function to (e.g. 'Control+n')
@type keyName: string
@param func: the function you wish to bind the key press to
@type func: function
"""
		if not self.__dict__.has_key('_keyMap'):
			self._keyMap=getattr(self.__class__,'_keyMap',{}).copy()
		self._keyMap[key(keyName)]=func

	_keyMap={}

	def getScript(self,keyPress):
		"""
Returns a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to retreave the script for
@type keyPress: key
""" 
		if keyPress in self._keyMap:
			func=self._keyMap[keyPress]
      			if func.im_self:
            				return func
      			else:
				return instancemethod(func,self,self.__class__)

class AutoPropertyCacheObject(AutoPropertyObject):
	#: Tracks the instances of this class; used by L{invalidateCaches}.
	#: @type: weakref.WeakKeyDictionary
	__instances=weakref.WeakKeyDictionary()

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
