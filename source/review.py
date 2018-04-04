#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 Michael Curran <mick@nvaccess.org>

from collections import OrderedDict
import api
import winUser
from logHandler import log
from NVDAObjects import NVDAObject, NVDAObjectTextInfo
from NVDAObjects.window import Window
from treeInterceptorHandler import DocumentTreeInterceptor
from displayModel import DisplayModelTextInfo
import textInfos
import config

def getObjectPosition(obj):
	"""
	Fetches a TextInfo instance suitable for reviewing the text in  the given object.
	@param obj: the NVDAObject to review
	@type obj: L{NVDAObject}
	@return: the TextInfo instance and the Scriptable object the TextInfo instance is referencing, or None on error. 
	@rtype: (L{TextInfo},L{ScriptableObject})
	"""
	try:
		pos=obj.makeTextInfo(textInfos.POSITION_CARET)
	except (NotImplementedError, RuntimeError):
		# No caret supported, try first position instead
		try:
			pos=obj.makeTextInfo(textInfos.POSITION_FIRST)
		except (NotImplementedError, RuntimeError):
			log.debugWarning("%s does not support POSITION_FIRST, falling back to NVDAObjectTextInfo"%obj.TextInfo)
			# First position not supported either, return first position from a generic NVDAObjectTextInfo 
			return NVDAObjectTextInfo(obj,textInfos.POSITION_FIRST),obj
	return pos,pos.obj

def getDocumentPosition(obj):
	"""
	Fetches a TextInfo instance suitable for reviewing the text in  the given object's L{TreeInterceptor}, positioned at the object.
	@param obj: the NVDAObject to review
	@type obj: L{NVDAObject}
	@return: the TextInfo instance and the Scriptable object the TextInfo instance is referencing, or None on error. 
	@rtype: (L{TextInfo},L{ScriptableObject})
	"""
	if not isinstance(obj.treeInterceptor,DocumentTreeInterceptor):
		return None
	try:
		pos=obj.treeInterceptor.makeTextInfo(obj)
	except LookupError:
		return None
	return pos,pos.obj

def getScreenPosition(obj):
	"""
	Fetches a TextInfo instance suitable for reviewing the screen, positioned at the given object's coordinates. 
	@param obj: the NVDAObject to review
	@type obj: L{NVDAObject}
	@return: the TextInfo instance and the Scriptable object the TextInfo instance is referencing, or None on error. 
	@rtype: (L{TextInfo},L{ScriptableObject})
	"""
	focus=api.getFocusObject()
	while focus and not isinstance(focus,Window):
		focus=focus.parent
	if not focus: return None
	w=winUser.getAncestor(focus.windowHandle,winUser.GA_ROOT) or focus.windowHandle
	s=Window(windowHandle=w)
	if s:
		s.redraw()
		try:
			pos=DisplayModelTextInfo(s,obj)
		except LookupError:
			pos=DisplayModelTextInfo(s,textInfos.POSITION_FIRST)
		return pos,pos.obj

modes=[
	# Translators: One of the review modes.
	('object',_("Object review"),getObjectPosition),
	# Translators: One of the review modes.
	('document',_("Document review"),getDocumentPosition),
	# Translators: One of the review modes.
	('screen',_("Screen review"),getScreenPosition),
]

_currentMode=0

def getPositionForCurrentMode(obj):
	"""
	Fetches a TextInfo instance suitable for reviewing the text in or around the given object, according to the current review mode. 
	@param obj: the NVDAObject to review
	@type obj: L{NVDAObject}
	@return: the TextInfo instance and the Scriptable object the TextInfo instance is referencing, or None on error. 
	@rtype: (L{TextInfo},L{ScriptableObject})
	"""
	mode=_currentMode
	while mode>=0:
		pos=modes[mode][2](obj)
		if pos:
			return pos
		mode-=1

def getCurrentMode():
	"""Fetches the ID of the current mode"""
	return modes[_currentMode][0]

def setCurrentMode(mode,updateReviewPosition=True):
	"""
	Sets the current review mode to the given mode ID or index and updates the review position.
	@param mode: either a 0-based index into the modes list, or one of the mode IDs (first item of a tuple in the modes list).
	@type mode: int or string
	@return: a presentable label for the new current mode (suitable for speaking or brailleing)
	@rtype: string
	"""
	global _currentMode
	if isinstance(mode,int):
		ID,label,func=modes[mode]
	else:
		for index,(ID,label,func) in enumerate(modes):
			if mode==ID:
				mode=index
				break
		else:
			raise LookupError("mode %s not found"%mode)
	obj=api.getNavigatorObject()
	pos=func(obj)
	if pos:
		_currentMode=mode
		if updateReviewPosition: api.setReviewPosition(pos[0],clearNavigatorObject=False)
		return label

def nextMode(prev=False,startMode=None):
	"""
	Sets the current review mode to the next available  mode and updates the review position. 
	@param prev: if true then switch to the previous mode. If false, switch to the next mode.
	@type prev: bool
	@return: a presentable label for the new current mode (suitable for speaking or brailleing)
	@rtype: string
	"""
	if startMode is None:
		startMode=_currentMode
	newMode=startMode+(1 if not prev else -1)
	if newMode<0 or newMode>=len(modes):
		return None
	label=setCurrentMode(newMode)
	return label or nextMode(prev=prev,startMode=newMode)

def handleCaretMove(pos):
	"""
	Instructs the review position to be updated due to caret movement.
	@param pos: Either a TextInfo instance at the caret position, or an NVDAObject or TeeInterceptor who's caret position should be retreaved.
	@type pos: L{textInfos.TextInfo} or L{NVDAObject} or L{TreeInterceptor}
	"""
	if not config.conf["reviewCursor"]["followCaret"]:
		return
	if isinstance(pos,textInfos.TextInfo):
		info=pos
		obj=pos.obj
	else:
		info=None
		obj=pos
	mode=getCurrentMode()
	if isinstance(obj,NVDAObject):
		if not mode=='object' or obj!=api.getNavigatorObject():
			return
	elif isinstance(obj,DocumentTreeInterceptor):
		if mode not in ('object','document'):
			return
		if mode!='document':
			if obj.passThrough:
				#if trying to set with a position in a treeInterceptor but passThrough is turned on, ignore it completely
				return
			setCurrentMode('document',updateReviewPosition=False)
	if not info:
		try:
			info=obj.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError,RuntimeError):
			return
	api.setReviewPosition(info, isCaret=True)
