#baseObject.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from new import instancemethod
from keyUtils import key

class autoPropertyObject(object):

	def __getattr__(self,name):
		if not name.startswith('_get_') and hasattr(self,'_get_%s'%name):
			return getattr(self,'_get_%s'%name)()
		else:
			raise AttributeError("object has no attribute '%s'"%name)
 

	def __setattr__(self,name,value):
		if not name.startswith('_set_') and hasattr(self,'_set_%s'%name):
			getattr(self,'_set_%s'%name)(value)
		else:
			super(autoPropertyObject,self).__setattr__(name,value)

class scriptableObject(autoPropertyObject):

	@classmethod
	def bindKey(cls,keyName,scriptName):
		scriptName="script_%s"%scriptName
		if not hasattr(cls,scriptName):
			raise ValueError("no script \"%s\" in %s"%(scriptName,cls))
		if not cls.__dict__.has_key('_keyMap'):
			cls._keyMap=getattr(cls,'_keyMap',{}).copy()
		cls._keyMap[key(keyName)]=getattr(cls,scriptName)

	_keyMap={}

	def getScript(self,keyPress):
		"""
Returns a script (instance method) if one is assigned to the keyPress given.
@param keyPress: The key you wish to retreave the script for
@type keyPress: key
""" 
		if self._keyMap.has_key(keyPress):
			return instancemethod(self._keyMap[keyPress],self,self.__class__)
