#treeInterceptorHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2006-2010 Michael Curran <mick@kulgan.net>, James Teh <jamie@jantrid.net>

from logHandler import log
import baseObject
import api
import review
import textInfos
import config
import braille

runningTable=set()

def getTreeInterceptor(obj):
	for ti in runningTable:
		if obj in ti:
			return ti

def update(obj):
	# Don't create treeInterceptors for objects for which NVDA should sleep.
	if obj.sleepMode:
		return None
	#If this object already has a treeInterceptor, just return that and don't bother trying to create one
	ti=obj.treeInterceptor
	if not ti:
		if not obj.shouldCreateTreeInterceptor:
			return None
		try:
			newClass=obj.treeInterceptorClass
		except NotImplementedError:
			return None
		ti=newClass(obj)
		if not ti.isAlive:
			return None
		runningTable.add(ti)
		log.debug("Adding new treeInterceptor to runningTable: %s"%ti)
	if ti.shouldPrepare:
		ti.prepare()
	return ti

def cleanup():
	"""Kills off any treeInterceptors that are no longer alive."""
	for ti in list(runningTable):
		if not ti.isAlive:
			killTreeInterceptor(ti)

def killTreeInterceptor(treeInterceptorObject):
	try:
		runningTable.remove(treeInterceptorObject)
	except KeyError:
		return
	treeInterceptorObject.terminate()
	log.debug("Killed treeInterceptor: %s" % treeInterceptorObject)

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

	shouldTrapNonCommandGestures=False #: If true then gestures that do not have a script and are not a command gesture should be trapped from going through to Windows.

	def __init__(self, rootNVDAObject):
		super(TreeInterceptor, self).__init__()
		self._passThrough = False
		#: The root object of the tree wherein events and scripts are intercepted.
		#: @type: L{NVDAObjects.NVDAObject}
		self.rootNVDAObject = rootNVDAObject

	def terminate(self):
		"""Terminate this interceptor.
		This is called to perform any clean up when this interceptor is being destroyed.
		"""

	def _get_isAlive(self):
		"""Whether this interceptor is alive.
		If it is not alive, it will be removed.
		"""
		raise NotImplementedError

	#: Whether this interceptor is ready to be used; i.e. whether it should receive scripts and events.
	#: @type: bool
	isReady = True

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
			if config.conf['reviewCursor']['followFocus']:
				focusObj=api.getFocusObject()
				if self is focusObj.treeInterceptor:
					if review.getCurrentMode()=='document':
						# if focus is in this treeInterceptor and review mode is document, turning on passThrough should force object review
						review.setCurrentMode('object')
					api.setNavigatorObject(focusObj)
			braille.handler.handleGainFocus(api.getFocusObject())
		else:
			obj=api.getNavigatorObject()
			if config.conf['reviewCursor']['followCaret'] and self is obj.treeInterceptor: 
				if review.getCurrentMode()=='object':
					# if navigator object is in this treeInterceptor and the review mode is object, then turning off passThrough should force document review 
					review.setCurrentMode('document',True)
			braille.handler.handleGainFocus(self)

	_cache_shouldPrepare=True
	shouldPrepare=False #:True if this treeInterceptor's prepare method should be called in order to make it ready (e.g. load a virtualBuffer, or process the document in some way).

	def prepare(self):
		"""Prepares this treeInterceptor so that it becomes ready to accept event/script input."""
		raise NotImplementedError

class DocumentTreeInterceptor(TreeInterceptor):
	"""A TreeInterceptor that supports document review."""

	def _get_TextInfo(self):
		raise NotImplementedError

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

class RootProxyTextInfo(textInfos.TextInfo):

	def __init__(self,obj,position,_rangeObj=None):
		super(RootProxyTextInfo,self).__init__(obj,position)
		self.innerTextInfo=self.InnerTextInfoClass(obj.rootNVDAObject,position,_rangeObj=_rangeObj)

	def _get_InnerTextInfoClass(self):
		return self.obj.rootNVDAObject.TextInfo

	def copy(self):
		return self.__class__(self.obj,None,_rangeObj=self.innerTextInfo._rangeObj)

	def _get__rangeObj(self):
		return self.innerTextInfo._rangeObj

	def _set__rangeObj(self,r):
		self.innerTextInfo._rangeObj=r

	def find(self,text,caseSensitive=False,reverse=False):
		return self.innerTextInfo.find(text,caseSensitive,reverse)

	def activate(self):
		return self.innerTextInfo.activate()

	def compareEndPoints(self,other,which):
		return self.innerTextInfo.compareEndPoints(other.innerTextInfo,which)

	def setEndPoint(self,other,which):
		return self.innerTextInfo.setEndPoint(other.innerTextInfo,which)

	def _get_isCollapsed(self):
		return self.innerTextInfo.isCollapsed

	def collapse(self,end=False):
		return self.innerTextInfo.collapse(end=end)

	def move(self,unit,direction,endPoint=None):
		return self.innerTextInfo.move(unit,direction,endPoint=endPoint)

	def _get_bookmark(self):
		return self.innerTextInfo.bookmark

	def updateCaret(self):
		return self.innerTextInfo.updateCaret()

	def updateSelection(self):
		return self.innerTextInfo.updateSelection()

	def _get_text(self):
		return self.innerTextInfo.text

	def getTextWithFields(self,formatConfig=None):
		return self.innerTextInfo.getTextWithFields(formatConfig=formatConfig)

	def expand(self,unit):
		return self.innerTextInfo.expand(unit)

	def getMathMl(self, field):
		return self.innerTextInfo.getMathMl(field)

	def _get_NVDAObjectAtStart(self):
		return self.innerTextInfo.NVDAObjectAtStart

	def _get_focusableNVDAObjectAtStart(self):
		return self.innerTextInfo.focusableNVDAObjectAtStart
