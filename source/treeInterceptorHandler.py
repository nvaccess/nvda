#treeInterceptorHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from logHandler import log
import baseObject
import api
import braille

runningTable=set()

def getTreeInterceptor(obj):
	for ti in runningTable:
		if obj in ti:
			return ti

def update(obj):
	#If this object already has a treeInterceptor, just return that and don't bother trying to create one
	ti=obj.treeInterceptor
	if ti:
		return ti
	try:
		newClass=obj.treeInterceptorClass
	except NotImplementedError:
		return None
	treeInterceptorObject=newClass(obj)
	if not treeInterceptorObject.isAlive:
		return None
	runningTable.add(treeInterceptorObject)
	log.debug("Adding new treeInterceptor to runningTable: %s"%treeInterceptorObject)
	return treeInterceptorObject

def cleanup():
	"""Kills off any treeInterceptors that are no longer alive."""
	for ti in list(runningTable):
		if not ti.isTransitioning and not ti.isAlive:
			killTreeInterceptor(ti)

def killTreeInterceptor(treeInterceptorObject):
	try:
		runningTable.remove(treeInterceptorObject)
	except KeyError:
		return
	treeInterceptorObject.terminate()

def terminate():
	"""Kills any currently running treeInterceptors"""
	for ti in list(runningTable):
		killTreeInterceptor(ti)

class TreeInterceptor(baseObject.ScriptableObject):
	"""Intercepts events and scripts for a tree of NVDAObjects.
	When an NVDAObject is encompassed by this interceptor (i.e. it is beneath the root object or it is the root object itself),
	events will first be executed on this interceptor if implemented.
	Similarly, scripts on this interceptor take precedence over those of encompassed objects.
	"""

	def __init__(self, rootNVDAObject):
		super(TreeInterceptor, self).__init__()
		self._passThrough = False
		#: The root object of the tree wherein events and scripts are intercepted.
		#: @type: L{NVDAObjects.NVDAObject}
		self.rootNVDAObject = rootNVDAObject
		#: Indicates that this interceptor is in a state of transition and should not be killed even if L{isAlive} is C{False}.
		#: @type: bool
		self.isTransitioning = False

	def terminate(self):
		"""Terminate this interceptor.
		This is called to perform any clean up when this interceptor is being destroyed.
		"""

	def _get_isAlive(self):
		"""Whether this interceptor is alive.
		If it is not alive, it will be removed.
		"""
		raise NotImplementedError

	def __contains__(self, obj):
		"""Determine whether an object is encompassed by this interceptor.
		@param obj: The object in question.
		@type obj: L{NVDAObjects.NVDAObject}
		@return: C{True} if the object is encompassed by this interceptor.
		@rtype: bool
		"""
		raise NotImplementedError

	def _get_passThrough(self):
		"""Whether most scripts should temporarily pass through this interceptor without being intercepted.
		"""
		return self._passThrough

	def _set_passThrough(self, state):
		if self._passThrough == state:
			return
		self._passThrough = state
		if state:
			braille.handler.handleGainFocus(api.getFocusObject())
		else:
			braille.handler.handleGainFocus(self)
