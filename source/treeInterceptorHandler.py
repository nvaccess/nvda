#treeInterceptorHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from logHandler import log
import baseObject

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

	def __init__(self, rootNVDAObject):
		super(TreeInterceptor, self).__init__()
		self._passThrough = False
		self.rootNVDAObject = rootNVDAObject
		self.isTransitioning = False

	def terminate(self):
		pass

	def _get_isAlive(self):
		return False

	def __contains__(self, obj):
		return False

	def _get_passThrough(self):
		return self._passThrough

	def _set_passThrough(self, state):
		if self._passThrough == state:
			return
		self._passThrough = state
		import braille
		if state:
			braille.handler.handleGainFocus(api.getFocusObject())
		else:
			braille.handler.handleGainFocus(self)
