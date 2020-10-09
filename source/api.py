#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""General functions for NVDA"""

import ctypes
import config
import textInfos
import review
import globalVars
from logHandler import log
import ui
import treeInterceptorHandler
import virtualBuffers
import NVDAObjects
import NVDAObjects.IAccessible
import winUser
import controlTypes
import eventHandler
import braille
import vision
import watchdog
import appModuleHandler
import cursorManager
from typing import Any

#User functions

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
	return globalVars.foregroundObject

def setForegroundObject(obj):
	"""Stores the given object as the current foreground object. (Note: it does not physically change the operating system foreground window, but only allows NVDA to keep track of what it is).
@param obj: the object that will be stored as the current foreground object
@type obj: NVDAObjects.NVDAObject
"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	globalVars.foregroundObject=obj
	return True

def setFocusObject(obj):
	"""Stores an object as the current focus object. (Note: this does not physically change the window with focus in the operating system, but allows NVDA to keep track of the correct object).
Before overriding the last object, this function calls event_loseFocus on the object to notify it that it is loosing focus. 
@param obj: the object that will be stored as the focus object
@type obj: NVDAObjects.NVDAObject
"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	if globalVars.focusObject:
		eventHandler.executeEvent("loseFocus",globalVars.focusObject)
	oldFocusLine=globalVars.focusAncestors
	#add the old focus to the old focus ancestors, but only if its not None (is none at NVDA initialization)
	if globalVars.focusObject: 
		oldFocusLine.append(globalVars.focusObject)
	oldAppModules=[o.appModule for o in oldFocusLine if o and o.appModule]
	appModuleHandler.cleanup()
	ancestors=[]
	tempObj=obj
	matchedOld=False
	focusDifferenceLevel=0
	oldFocusLineLength=len(oldFocusLine)
	# Starting from the focus, move up the ancestor chain.
	safetyCount=0
	while tempObj:
		if safetyCount<100:
			safetyCount+=1
		else:
			try:
				log.error("Never ending focus ancestry: last object: %s, %s, window class %s, application name %s"%(tempObj.name,controlTypes.roleLabels[tempObj.role],tempObj.windowClassName,tempObj.appModule.appName))
			except:
				pass
			tempObj=getDesktopObject()
		# Scan backwards through the old ancestors looking for a match.
		for index in range(oldFocusLineLength-1,-1,-1):
			watchdog.alive()
			if tempObj==oldFocusLine[index]:
				# Match! The old and new focus ancestors converge at this point.
				# Copy the old ancestors up to and including this object.
				origAncestors=oldFocusLine[0:index+1]
				#make sure to cache the last old ancestor as a parent on the first new ancestor so as not to leave a broken parent cache
				if ancestors and origAncestors:
					ancestors[0].container=origAncestors[-1]
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
		container=tempObj.container
		tempObj.container=container # Cache the parent.
		tempObj=container
	#Remove the final new ancestor as this will be the new focus object
	del ancestors[-1]
	# #5467: Ensure that the appModule of the real focus is included in the newAppModule list for profile switching
	# Rather than an original focus ancestor which happened to match the new focus.
	newAppModules=[o.appModule for o in ancestors if o and o.appModule]
	if obj.appModule:
		newAppModules.append(obj.appModule)
	try:
		treeInterceptorHandler.cleanup()
	except watchdog.CallCancelled:
		pass
	treeInterceptorObject=None
	o=None
	watchdog.alive()
	for o in ancestors[focusDifferenceLevel:]+[obj]:
		try:
			treeInterceptorObject=treeInterceptorHandler.update(o)
		except:
			log.exception("Error updating tree interceptor")
	#Always make sure that the focus object's treeInterceptor is forced to either the found treeInterceptor (if its in it) or to None
	#This is to make sure that the treeInterceptor does not have to be looked up, which can cause problems for winInputHook
	if obj is o or obj in treeInterceptorObject:
		obj.treeInterceptor=treeInterceptorObject
	else:
		obj.treeInterceptor=None
	# #3804: handleAppSwitch should be called as late as possible,
	# as triggers must not be out of sync with global focus variables.
	# setFocusObject shouldn't fail earlier anyway, but it's best to be safe.
	appModuleHandler.handleAppSwitch(oldAppModules,newAppModules)
	# Set global focus variables.
	globalVars.focusDifferenceLevel=focusDifferenceLevel
	globalVars.focusObject=obj
	globalVars.focusAncestors=ancestors
	braille.invalidateCachedFocusAncestors(focusDifferenceLevel)
	if config.conf["reviewCursor"]["followFocus"]:
		setNavigatorObject(obj,isFocus=True)
	return True

def getFocusDifferenceLevel():
	return globalVars.focusDifferenceLevel

def getFocusAncestors():
	"""An array of NVDAObjects that are all parents of the object which currently has focus"""
	return globalVars.focusAncestors

def getMouseObject():
	"""Returns the object that is directly under the mouse"""
	return globalVars.mouseObject

def setMouseObject(obj):
	"""Tells NVDA to remember the given object as the object that is directly under the mouse"""
	globalVars.mouseObject=obj

def getDesktopObject():
	"""Get the desktop object"""
	return globalVars.desktopObject

def setDesktopObject(obj):
	"""Tells NVDA to remember the given object as the desktop object"""
	globalVars.desktopObject=obj

def getReviewPosition():
	"""Retreaves the current TextInfo instance representing the user's review position. If it is not set, it uses the user's set navigator object and creates a TextInfo from that.
	"""
	if globalVars.reviewPosition: 
		return globalVars.reviewPosition
	else:
		obj=globalVars.navigatorObject
		globalVars.reviewPosition,globalVars.reviewPositionObj=review.getPositionForCurrentMode(obj)
		return globalVars.reviewPosition


def setReviewPosition(
		reviewPosition,
		clearNavigatorObject=True,
		isCaret=False,
		isMouse=False
):
	"""Sets a TextInfo instance as the review position.
	@param clearNavigatorObject: if  true, It sets the current navigator object to C{None}.
		In that case, the next time the navigator object is asked for it fetches it from the review position.
	@type clearNavigatorObject: bool
	@param isCaret: Whether the review position is changed due to caret following.
	@type isCaret: bool
	@param isMouse: Whether the review position is changed due to mouse following.
	@type isMouse: bool
	"""
	globalVars.reviewPosition=reviewPosition.copy()
	globalVars.reviewPositionObj=reviewPosition.obj
	if clearNavigatorObject: globalVars.navigatorObject=None
	# When the review cursor follows the caret and braille is auto tethered to review,
	# we should not update braille with the new review position as a tether to focus is due.
	if not (braille.handler.shouldAutoTether and isCaret):
		braille.handler.handleReviewMove(shouldAutoTether=not isCaret)
	if isCaret:
		visionContext = vision.constants.Context.CARET
	elif isMouse:
		visionContext = vision.constants.Context.MOUSE
	else:
		visionContext = vision.constants.Context.REVIEW
	vision.handler.handleReviewMove(context=visionContext)

def getNavigatorObject():
	"""Gets the current navigator object. Navigator objects can be used to navigate around the operating system (with the number pad) with out moving the focus. If the navigator object is not set, it fetches it from the review position. 
@returns: the current navigator object
@rtype: L{NVDAObjects.NVDAObject}
"""
	if globalVars.navigatorObject:
		return globalVars.navigatorObject
	else:
		if review.getCurrentMode()=='object':
			obj=globalVars.reviewPosition.obj
		else:
			try:
				obj=globalVars.reviewPosition.NVDAObjectAtStart
			except (NotImplementedError,LookupError):
				obj=globalVars.reviewPosition.obj
		globalVars.navigatorObject=getattr(obj,'rootNVDAObject',None) or obj
		return globalVars.navigatorObject

def setNavigatorObject(obj,isFocus=False):
	"""Sets an object to be the current navigator object. Navigator objects can be used to navigate around the operating system (with the number pad) with out moving the focus. It also sets the current review position to None so that next time the review position is asked for, it is created from the navigator object.  
@param obj: the object that will be set as the current navigator object
@type obj: NVDAObjects.NVDAObject  
@param isFocus: true if the navigator object was set due to a focus change.
@type isFocus: bool
"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	globalVars.navigatorObject=obj
	oldPos=globalVars.reviewPosition
	oldPosObj=globalVars.reviewPositionObj
	globalVars.reviewPosition=None
	globalVars.reviewPositionObj=None
	reviewMode=review.getCurrentMode()
	# #3320: If in document review yet there is no document to review the mode should be forced to object. 
	if reviewMode=='document' and (not isinstance(obj.treeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor)  or not obj.treeInterceptor.isReady or obj.treeInterceptor.passThrough):
		review.setCurrentMode('object',False)
	elif isinstance(obj.treeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor) and obj.treeInterceptor.isReady and not obj.treeInterceptor.passThrough:
		if reviewMode=='object':
			review.setCurrentMode('document',False)
		if isFocus:
			globalVars.reviewPosition=obj.treeInterceptor.makeTextInfo(textInfos.POSITION_CARET)
			globalVars.reviewPositionObj=globalVars.reviewPosition
	eventHandler.executeEvent("becomeNavigatorObject",obj,isFocus=isFocus)

def isTypingProtected():
	"""Checks to see if key echo should be suppressed because the focus is currently on an object that has its protected state set.
@returns: True if it should be suppressed, False otherwise.
@rtype: boolean
"""
	focusObject=getFocusObject()
	if focusObject and focusObject.isProtected:
		return True
	else:
		return False

def createStateList(states):
	"""Breaks down the given integer in to a list of numbers that are 2 to the power of their position.""" 
	return [x for x in [1<<y for y in range(32)] if x&states]


def moveMouseToNVDAObject(obj):
	"""Moves the mouse to the given NVDA object's position""" 
	location=obj.location
	if location:
		winUser.setCursorPos(*location.center)

def processPendingEvents(processEventQueue=True):
	# Import late to avoid circular import.
	import IAccessibleHandler
	import JABHandler
	import wx
	import queueHandler
	watchdog.alive()
	wx.Yield()
	JABHandler.pumpAll()
	IAccessibleHandler.pumpAll()
	import baseObject
	baseObject.AutoPropertyObject.invalidateCaches()
	if processEventQueue:
		queueHandler.flushQueue(queueHandler.eventQueue)

def copyToClip(text):
	"""Copies the given text to the windows clipboard.
@returns: True if it succeeds, False otherwise.
@rtype: boolean
@param text: the text which will be copied to the clipboard
@type text: string
"""
	if not isinstance(text,str) or len(text)==0:
		return False
	import gui
	with winUser.openClipboard(gui.mainFrame.Handle):
		winUser.emptyClipboard()
		winUser.setClipboardData(winUser.CF_UNICODETEXT,text)
	got=getClipData()
	return got == text

def getClipData():
	"""Receives text from the windows clipboard.
@returns: Clipboard text
@rtype: string
"""
	import gui
	with winUser.openClipboard(gui.mainFrame.Handle):
		return winUser.getClipboardData(winUser.CF_UNICODETEXT) or u""

def getStatusBar():
	"""Obtain the status bar for the current foreground object.
	@return: The status bar object or C{None} if no status bar was found.
	@rtype: L{NVDAObjects.NVDAObject}
	"""
	foreground = getForegroundObject()
	try:
		return foreground.appModule.statusBar
	except NotImplementedError:
		pass
	# The status bar is usually at the bottom of the screen.
	# Therefore, get the object at the bottom left of the foreground object using screen coordinates.
	location=foreground.location
	if not location:
		return None
	left, top, width, height = location
	bottom = top + height - 1
	obj = getDesktopObject().objectFromPoint(left, bottom)

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
	text = obj.name or ""
	if text:
		text += " "
	return text + " ".join(chunk for child in obj.children for chunk in (child.name, child.value) if chunk and isinstance(chunk, str) and not chunk.isspace())

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


def isNVDAObject(obj: Any) -> bool:
	"""Returns whether the supplied object is a L{NVDAObjects.NVDAObject}"""
	return isinstance(obj, NVDAObjects.NVDAObject)


def isCursorManager(obj: Any) -> bool:
	"""Returns whether the supplied object is a L{cursorManager.CursorManager}"""
	return isinstance(obj, cursorManager.CursorManager)


def isTreeInterceptor(obj: Any) -> bool:
	"""Returns whether the supplied object is a L{treeInterceptorHandler.TreeInterceptor}"""
	return isinstance(obj, treeInterceptorHandler.TreeInterceptor)


def isObjectInActiveTreeInterceptor(obj: NVDAObjects.NVDAObject) -> bool:
	"""Returns whether the supplied L{NVDAObjects.NVDAObject} is
	in an active L{treeInterceptorHandler.TreeInterceptor},
	i.e. a tree interceptor that is not in pass through mode.
	"""
	return bool(
		isinstance(obj, NVDAObjects.NVDAObject)
		and obj.treeInterceptor
		and not obj.treeInterceptor.passThrough
	)


def getCaretObject():
	"""Gets the object which contains the caret.
	This is normally the focus object.
	However, if the focus object has a tree interceptor which is not in focus mode,
	the tree interceptor will be returned.
	@return: The object containing the caret.
	@rtype: L{baseObject.ScriptableObject}
	"""
	obj = getFocusObject()
	ti = obj.treeInterceptor
	if isinstance(ti,treeInterceptorHandler.DocumentTreeInterceptor) and ti.isReady and not ti.passThrough:
		return ti
	return obj
