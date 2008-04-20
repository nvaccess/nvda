#baseObject.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Contains the base classes that many of NVDA's classes such as NVDAObjects, virtualBuffers, appModules, synthDrivers inherit from. These base classes provide such things as auto properties, and methods and properties for scripting and key binding.
"""

from new import instancemethod
from keyUtils import key

class AutoPropertyObject(object):

	"""A class that dynamicly supports properties, by looking up _get_* and _set_* methods at runtime.
 _get_x will make property x with a getter (you can get its value).
_set_x will make a property x with a setter (you can set its value).
If there is a _get_x but no _set_x then setting x will override the property completely.
"""

	def __getattr__(self,name):
		if not name.startswith('_get_') and hasattr(self,'_get_%s'%name):
			return getattr(self,'_get_%s'%name)()
		else:
			raise AttributeError("object has no attribute '%s'"%name)
 
	def __setattr__(self,name,value):
		if not name.startswith('_set_') and hasattr(self,'_set_%s'%name):
			getattr(self,'_set_%s'%name)(value)
		else:
			super(AutoPropertyObject,self).__setattr__(name,value)

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
    		func=getattr(self,scriptName,None)
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
