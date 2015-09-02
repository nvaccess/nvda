#api.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""General functions for NVDA"""

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
import win32clipboard
import win32con
import eventHandler
import braille
import watchdog
import appModuleHandler

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
		for index in xrange(oldFocusLineLength-1,-1,-1):
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
	newAppModules=[o.appModule for o in ancestors if o and o.appModule]
	#Remove the final new ancestor as this will be the new focus object
	del ancestors[-1]
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

def setReviewPosition(reviewPosition,clearNavigatorObject=True):
	"""Sets a TextInfo instance as the review position. if clearNavigatorObject is true, It sets the current navigator object to None so that the next time the navigator object is asked for it fetches it from the review position.
	"""
	globalVars.reviewPosition=reviewPosition.copy()
	globalVars.reviewPositionObj=reviewPosition.obj
	if clearNavigatorObject: globalVars.navigatorObject=None
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
	eventHandler.executeEvent("becomeNavigatorObject",obj)

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
	if isinstance(text,basestring) and len(text)>0 and not text.isspace():
		try:
			win32clipboard.OpenClipboard()
		except win32clipboard.error:
			return False
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
