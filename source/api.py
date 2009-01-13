#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""General functions for NVDA"""

import textHandler
import globalVars
from logHandler import log
import speech
import sayAllHandler
import virtualBufferHandler
import NVDAObjects
import NVDAObjects.IAccessible
import winUser
import controlTypes
import win32clipboard
import win32con

#User functions

def findObjectWithFocus():
	"""Walks the object hyerarchy starting at the desktop Window (root object) and follows the activeChild property of each object until it can not go any further - this will be the object with focus.
@returns: object with focus
@rtype: L{NVDAObjects.NVDAObject}
"""
	obj=getDesktopObject()
	prevObj=None
	while obj and obj!=prevObj:
		prevObj=obj
		obj=obj.activeChild
	return prevObj

def getFocusObject():
	"""
Gets the current object with focus.
@returns: the object with focus
@rtype: L{NVDAObjects.NVDAObject}
"""
	return globalVars.focusObject

def getForegroundObject():
	"""Gets the current foreground object.
@returns: the current foreground object
@rtype: L{NVDAObjects.NVDAObject}
"""
	numAncestors=len(globalVars.focusAncestors)
	if numAncestors<=1:
		return globalVars.focusObject
	elif globalVars.focusAncestors[1].role==controlTypes.ROLE_WINDOW:
		if numAncestors==2:
			return globalVars.focusObject
		return globalVars.focusAncestors[2]
	else:
		return globalVars.focusAncestors[1]

def setForegroundObject(obj):
	"""Stores the given object as the current foreground object. (Note: it does not physically change the operating system foreground window, but only allows NVDA to keep track of what it is).
@param obj: the object that will be stored as the current foreground object
@type obj: NVDAObjects.NVDAObject
"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	globalVars.foregroundObject=obj
	if log.isEnabledFor(log.DEBUG):
		log.debug("%s %s %s %s"%(obj.name or "",controlTypes.speechRoleLabels[obj.role],obj.value or "",obj.description or ""))
	return True

def setFocusObject(obj):
	"""Stores an object as the current focus object. (Note: this does not physically change the window with focus in the operating system, but allows NVDA to keep track of the correct object).
Before overriding the last object, this function calls event_loseFocus on the object to notify it that it is loosing focus. 
@param obj: the object that will be stored as the focus object
@type obj: NVDAObjects.NVDAObject
"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_loseFocus"):
		try:
			globalVars.focusObject.event_loseFocus()
		except:
			log.error("event_loseFocus in focusObject", exc_info=True)
	oldFocusLine=globalVars.focusAncestors
	#add the old focus to the old focus ancestors, but only if its not None (is none at NVDA initialization)
	if globalVars.focusObject: 
		oldFocusLine.append(globalVars.focusObject)
	oldAppModuleSet=set(o.appModule for o in oldFocusLine if o and o.appModule)
	ancestors=[]
	tempObj=obj
	matchedOld=False
	focusDifferenceLevel=0
	oldFocusLineLength=len(oldFocusLine)
	# Starting from the focus, move up the ancestor chain.
	while tempObj:
		# Scan backwards through the old ancestors looking for a match.
		for index in xrange(oldFocusLineLength-1,-1,-1):
			if tempObj==oldFocusLine[index]:
				# Match! The old and new focus ancestors converge at this point.
				# Copy the old ancestors up to and including this object.
				origAncestors=oldFocusLine[0:index+1]
				#make sure to cache the last old ancestor as a parent on the first new ancestor so as not to leave a broken parent cache
				if ancestors and origAncestors:
					ancestors[0].parent=origAncestors[-1]
				origAncestors.extend(ancestors)
				ancestors=origAncestors
				focusDifferenceLevel=index+1
				# We don't need to process any more in either this loop or the outer loop; we have all of the ancestors.
				matchedOld=True
				break
		if matchedOld:
			break
		# We're moving backwards along the ancestor chain, so add this to the start of the list.
		ancestors.insert(0,tempObj)
		parent=tempObj.parent
		tempObj.parent=parent # Cache the parent.
		tempObj=parent
	#Remove the final new ancestor as this will be the new focus object
	del ancestors[-1]
	newAppModuleSet=set(o.appModule for o in ancestors+[obj] if o and o.appModule)
	for removedMod in oldAppModuleSet-newAppModuleSet:
		if hasattr(removedMod,'event_appLoseFocus'):
			removedMod.event_appLoseFocus()
  	for addedMod in newAppModuleSet-oldAppModuleSet:
		if hasattr(addedMod,'event_appGainFocus'):
			addedMod.event_appGainFocus()
	if not obj.virtualBuffer or not obj.virtualBuffer.isAlive():
		virtualBufferObject=None
		for o in ancestors[focusDifferenceLevel:]+[obj]:
			virtualBufferObject=virtualBufferHandler.update(o)
			if virtualBufferObject:
				break
		obj.virtualBuffer=virtualBufferObject
		if virtualBufferObject and hasattr(virtualBufferObject,"event_virtualBuffer_firstGainFocus"):
			virtualBufferObject.event_virtualBuffer_firstGainFocus()
	oldVirtualBuffer=globalVars.focusObject.virtualBuffer if globalVars.focusObject else None
	# Set global focus variables before calling event_virtualBuffer_gainFocus.
	globalVars.focusDifferenceLevel=focusDifferenceLevel
	globalVars.focusObject=obj
	globalVars.focusAncestors=ancestors
	if globalVars.focusMovesNavigatorObject:
		setNavigatorObject(obj)
	if obj.virtualBuffer is not oldVirtualBuffer:
		if hasattr(oldVirtualBuffer,"event_virtualBuffer_loseFocus"):
			oldVirtualBuffer.event_virtualBuffer_loseFocus()
		if hasattr(obj.virtualBuffer,"event_virtualBuffer_gainFocus"):
			obj.virtualBuffer.event_virtualBuffer_gainFocus()
	if log.isEnabledFor(log.DEBUG):
		log.debug("%s %s %s %s"%(obj.name or "",controlTypes.speechRoleLabels[obj.role],obj.value or "",obj.description or ""))
	return True

def getFocusDifferenceLevel():
	return globalVars.focusDifferenceLevel

def getFocusAncestors():
	return globalVars.focusAncestors

def getMouseObject():
	"""Returns the object that is directly under the mouse"""
	return globalVars.mouseObject

def setMouseObject(obj):
	"""Tells NVDA to remember the given object as the object that is directly under the mouse"""
	if log.isEnabledFor(log.DEBUG):
		log.debug("%s %s %s %s"%(obj.name or "",controlTypes.speechRoleLabels[obj.role],obj.value or "",obj.description or ""))
	globalVars.mouseObject=obj

def getDesktopObject():
	"""Get the desktop object"""
	return globalVars.desktopObject

def setDesktopObject(obj):
	"""Tells NVDA to remember the given object as the desktop object"""
	if log.isEnabledFor(log.DEBUG):
		log.debug("%s %s %s %s"%(obj.name or "",controlTypes.speechRoleLabels[obj.role],obj.value or "",obj.description or ""))
	globalVars.desktopObject=obj

def getReviewPosition():
	"""Retreaves the current TextInfo instance representing the user's review position. If it is not set, it uses the user's set navigator object and creates a TextInfo from that.
	"""
	if globalVars.reviewPosition: 
		return globalVars.reviewPosition
	else:
		try:
			globalVars.reviewPosition=globalVars.navigatorObject.virtualBuffer.makeTextInfo(globalVars.navigatorObject)
			return globalVars.reviewPosition
		except:
			pass
		try:
			globalVars.reviewPosition=globalVars.navigatorObject.makeTextInfo(textHandler.POSITION_CARET)
			return globalVars.reviewPosition
		except:
			globalVars.reviewPosition=globalVars.navigatorObject.makeTextInfo(textHandler.POSITION_FIRST)
			return globalVars.reviewPosition

def setReviewPosition(reviewPosition):
	"""Sets a TextInfo instance as the review position. It sets the current navigator object to None so that the next time the navigator object is asked for it fetches it from the review position.
	"""
	globalVars.reviewPosition=reviewPosition
	globalVars.navigatorObject=None
	import braille
	braille.handler.handleReviewMove()

def getNavigatorObject():
	"""Gets the current navigator object. Navigator objects can be used to navigate around the operating system (with the number pad) with out moving the focus. If the navigator object is not set, it fetches it from the review position. 
@returns: the current navigator object
@rtype: L{NVDAObjects.NVDAObject}
"""
	if globalVars.navigatorObject:
		return globalVars.navigatorObject
	else:
		globalVars.navigatorObject=globalVars.reviewPosition.NVDAObjectAtStart
		return globalVars.navigatorObject

def setNavigatorObject(obj):
	"""Sets an object to be the current navigator object. Navigator objects can be used to navigate around the operating system (with the number pad) with out moving the focus. It also sets the current review position to None so that next time the review position is asked for, it is created from the navigator object.  
@param obj: the object that will be set as the current navigator object
@type obj: NVDAObjects.NVDAObject  
"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	if log.isEnabledFor(log.DEBUG):
		log.debug("%s %s %s %s"%(obj.name or "",controlTypes.speechRoleLabels[obj.role],obj.value or "",obj.description or ""))
	globalVars.navigatorObject=obj
	globalVars.reviewPosition=None
	import braille
	braille.handler.handleReviewMove()

def isTypingProtected():
	"""Checks to see if key echo should be suppressed because the focus is currently on an object that has its protected state set.
@returns: True if it should be suppressed, False otherwise.
@rtype: boolean
"""
	focusObject=getFocusObject()
	if focusObject and (controlTypes.STATE_PROTECTED in focusObject.states or focusObject.role==controlTypes.ROLE_PASSWORDEDIT):
		return True
	else:
		return False

def createStateList(states):
	"""Breaks down the given integer in to a list of numbers that are 2 to the power of their position.""" 
	return [x for x in [1<<y for y in xrange(32)] if x&states]


def moveMouseToNVDAObject(obj):
	"""Moves the mouse to the given NVDA object's position""" 
	location=obj.location
	if location and (len(location)==4):
		(left,top,width,height)=location
		x=(left+left+width)/2
		y=(top+top+height)/2
		winUser.setCursorPos(x,y)

def processPendingEvents(processEventQueue=True):
	# Import late to avoid circular import.
	import IAccessibleHandler
	import JABHandler
	import wx
	import queueHandler
	wx.Yield()
	JABHandler.pumpAll()
	IAccessibleHandler.pumpAll()
	if processEventQueue:
		queueHandler.flushQueue(queueHandler.eventQueue)

def copyToClip(text):
	"""Copies the given text to the windows clipboard.
@returns: True if it succeeds, False otherwise.
@rtype: boolean
@param text: the text which will be copied to the clipboard
@type text: string
"""
	if isinstance(text,basestring) and len(text)>0 and not text.isspace():
		win32clipboard.OpenClipboard()
		try:
			win32clipboard.EmptyClipboard()
			win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
		finally:
			win32clipboard.CloseClipboard()
		win32clipboard.OpenClipboard() # there seems to be a bug so to retrieve unicode text we have to reopen the clipboard
		try:
			got = 	win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
		finally:
			win32clipboard.CloseClipboard()
		if got == text:
			return True
	return False

def getClipData():
	"""Receives text from the windows clipboard.
@returns: Clipboard text
@rtype: string
"""
	text = ""
	win32clipboard.OpenClipboard()
	try:
		text = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
	finally:
		win32clipboard.CloseClipboard()
	return text

def getStatusBar():
	"""Obtain the status bar for the current foreground object.
	@return: The status bar object or C{None} if no status bar was found.
	@rtype: L{NVDAObjects.NVDAObject}
	"""
	# The status bar is usually at the bottom of the screen.
	# Therefore, get the object at the bottom left of the foreground object using screen coordinates.
	foreground = getForegroundObject()
	location=foreground.location
	if not location:
		return None
	left, top, width, height = location
	bottom = top + height - 1
	obj = NVDAObjects.IAccessible.getNVDAObjectFromPoint(left, bottom)

	# We may have landed in a child of the status bar, so search the ancestry for a status bar.
	while obj and not obj.role == controlTypes.ROLE_STATUSBAR:
		obj = obj.parent

	return obj

def getStatusBarText(obj):
	"""Get the text from a status bar.
	This includes the name of the status bar and the names and values of all of its children.
	@param obj: The status bar.
	@type obj: L{NVDAObjects.NVDAObject}
	@return: The status bar text.
	@rtype: str
	"""
	text = obj.name
	if text is None:
		text = ""
	return text + " ".join(chunk for child in obj.children for chunk in (child.name, child.value) if chunk and isinstance(chunk, basestring) and not chunk.isspace())

def filterFileName(name):
	"""Replaces invalid characters in a given string to make a windows compatible file name.
	@param name: The file name to filter.
	@type name: str
	@returns: The filtered file name.
	@rtype: str
	"""
	invalidChars=':?*\|<>/"'
	for c in invalidChars:
		name=name.replace(c,'_')
	return name
