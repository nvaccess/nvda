# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, James Teh, Michael Curran, Peter Vagner, Derek Riemer,
# Davy Kager, Babbage B.V., Leonard de Ruijter, Joseph Lee, Accessolutions, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""General functions for NVDA
Functions should mostly refer to getting an object (NVDAObject) or a position (TextInfo).
"""
import typing

import config
import textInfos
import review
import globalVars
from logHandler import log
import ui
import treeInterceptorHandler
import NVDAObjects
import winUser
import controlTypes
import eventHandler
import braille
import vision
import watchdog
import exceptions
import appModuleHandler
import cursorManager
from typing import Any, Optional

if typing.TYPE_CHECKING:
	import documentBase


def _isLockAppAndAlive(appModule: "appModuleHandler.AppModule"):
	return appModule.appName == "lockapp" and appModule.isAlive


def _isSecureObjectWhileLockScreenActivated(obj: NVDAObjects.NVDAObject) -> bool:
	"""
	While Windows is locked, Windows 10 and 11 allow for object navigation outside of the lockscreen.
	@return: C{True} if the Windows 10/11 lockscreen is active and C{obj} is outside of the lockscreen.

	According to MS docs, "There is no function you can call to determine whether the workstation is locked."
	https://docs.microsoft.com/en-gb/windows/win32/api/winuser/nf-winuser-lockworkstation
	"""
	runningAppModules = appModuleHandler.runningTable.values()
	lockAppModule = next(filter(_isLockAppAndAlive, runningAppModules), None)
	if lockAppModule is None:
		return False

	# The LockApp process might be kept alive
	# So determine if it is active, check the foreground window
	foregroundHWND = winUser.getForegroundWindow()
	foregroundProcessId, _threadId = winUser.getWindowThreadProcessID(foregroundHWND)

	isLockAppForeground = foregroundProcessId == lockAppModule.processID
	isObjectOutsideLockApp = obj.appModule.processID != foregroundProcessId

	if isLockAppForeground and isObjectOutsideLockApp:
		if log.isEnabledFor(log.DEBUG):
			devInfo = '\n'.join(obj.devInfo)
			log.debug(f"Attempt at navigating to a secure object: {devInfo}")
		return True
	return False

#User functions

def getFocusObject() -> NVDAObjects.NVDAObject:
	"""
	Gets the current object with focus.
	@returns: the object with focus
	"""
	return globalVars.focusObject


def getForegroundObject() -> NVDAObjects.NVDAObject:
	"""Gets the current foreground object.
	This (cached) object is the (effective) top-level "window" (hwnd).
	EG a Dialog rather than the focused control within the dialog.
	The cache is updated as queued events are processed, as such there will be a delay between the winEvent
	and this function matching. However, within NVDA this should be used in order to be in sync with other
	functions such as "getFocusAncestors".
	@returns: the current foreground object
	"""
	return globalVars.foregroundObject


def setForegroundObject(obj: NVDAObjects.NVDAObject) -> bool:
	"""Stores the given object as the current foreground object.
	Note: does not cause the operating system to change the foreground window,
		but simply allows NVDA to keep track of what the foreground window is.
		Alternative names for this function may have been:
		- setLastForegroundWindow
		- setLastForegroundEventObject
	@param obj: the object that will be stored as the current foreground object
	"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	if _isSecureObjectWhileLockScreenActivated(obj):
		return False
	globalVars.foregroundObject=obj
	return True


# C901 'setFocusObject' is too complex
# Note: when working on setFocusObject, look for opportunities to simplify
# and move logic out into smaller helper functions.
def setFocusObject(obj: NVDAObjects.NVDAObject) -> bool:  # noqa: C901
	"""Stores an object as the current focus object.
	Note: this does not physically change the window with focus in the operating system,
	but allows NVDA to keep track of the correct object.
	Before overriding the last object,
	this function calls event_loseFocus on the object to notify it that it is losing focus.
	@param obj: the object that will be stored as the focus object
	"""
	if not isinstance(obj,NVDAObjects.NVDAObject):
		return False
	if _isSecureObjectWhileLockScreenActivated(obj):
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
				log.error(
					"Never ending focus ancestry:"
					f" last object: {tempObj.name}, {controlTypes.Role(tempObj.role).displayString},"
					f" window class {tempObj.windowClassName}, application name {tempObj.appModule.appName}"
				)
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
	except exceptions.CallCancelled:
		pass
	treeInterceptorObject=None
	o=None
	watchdog.alive()
	for o in ancestors[focusDifferenceLevel:]+[obj]:
		try:
			treeInterceptorObject=treeInterceptorHandler.update(o)
		except:
			log.error("Error updating tree interceptor", exc_info=True)
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


def setMouseObject(obj: NVDAObjects.NVDAObject) -> None:
	"""Tells NVDA to remember the given object as the object that is directly under the mouse"""
	if _isSecureObjectWhileLockScreenActivated(obj):
		return
	globalVars.mouseObject=obj


def getDesktopObject() -> NVDAObjects.NVDAObject:
	"""Get the desktop object"""
	return globalVars.desktopObject


def setDesktopObject(obj: NVDAObjects.NVDAObject) -> None:
	"""Tells NVDA to remember the given object as the desktop object.
	We cannot prevent setting this when _isSecureObjectWhileLockScreenActivated is True,
	as NVDA needs to set the desktopObject on start, and NVDA may start from the lockscreen.
	"""
	globalVars.desktopObject=obj


def getReviewPosition() -> textInfos.TextInfo:
	"""Retrieves the current TextInfo instance representing the user's review position.
	If it is not set, it uses navigator object to create a TextInfo.
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


def getNavigatorObject() -> NVDAObjects.NVDAObject:
	"""Gets the current navigator object.
	Navigator objects can be used to navigate around the operating system (with the numpad),
	without moving the focus.
	If the navigator object is not set, it fetches and sets it from the review position.
	@returns: the current navigator object
	"""
	if globalVars.navigatorObject:
		return globalVars.navigatorObject
	elif review.getCurrentMode() == 'object':
		obj = globalVars.reviewPosition.obj
	else:
		try:
			obj = globalVars.reviewPosition.NVDAObjectAtStart
		except (NotImplementedError, LookupError):
			obj = globalVars.reviewPosition.obj
	nextObj = getattr(obj, 'rootNVDAObject', None) or obj
	if _isSecureObjectWhileLockScreenActivated(nextObj):
		return globalVars.navigatorObject
	globalVars.navigatorObject = nextObj
	return globalVars.navigatorObject


def setNavigatorObject(obj: NVDAObjects.NVDAObject, isFocus: bool = False) -> Optional[bool]:
	"""Sets an object to be the current navigator object.
	Navigator objects can be used to navigate around the operating system (with the numpad),
	without moving the focus.
	It also sets the current review position to None so that next time the review position is asked for,
	it is created from the navigator object.
	@param obj: the object that will be set as the current navigator object
	@param isFocus: true if the navigator object was set due to a focus change.
	"""

	if not isinstance(obj, NVDAObjects.NVDAObject):
		return False
	if _isSecureObjectWhileLockScreenActivated(obj):
		return False
	globalVars.navigatorObject=obj
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


def copyToClip(text: str, notify: Optional[bool] = False) -> bool:
	"""Copies the given text to the windows clipboard.
	@returns: True if it succeeds, False otherwise.
	@param text: the text which will be copied to the clipboard
	@param notify: whether to emit a confirmation message
	"""
	if not isinstance(text, str) or len(text) == 0:
		return False
	import gui
	try:
		with winUser.openClipboard(gui.mainFrame.Handle):
			winUser.emptyClipboard()
			winUser.setClipboardData(winUser.CF_UNICODETEXT, text)
		got = getClipData()
	except OSError:
		if notify:
			ui.reportTextCopiedToClipboard()  # No argument reports a failure.
		return False
	if got == text:
		if notify:
			ui.reportTextCopiedToClipboard(text)
		return True
	if notify:
		ui.reportTextCopiedToClipboard()  # No argument reports a failure.
	return False


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
	while obj and not obj.role == controlTypes.Role.STATUSBAR:
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
	try:
		return obj.appModule.getStatusBarText(obj)
	except NotImplementedError:
		pass
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
	invalidChars = r':?*\|<>/"'
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


def getCaretPosition() -> "textInfos.TextInfo":
	"""Gets a text info at the position of the caret.
	"""
	textContainerObj = getCaretObject()
	if not textContainerObj:
		raise RuntimeError("No Caret Object available, this is expected while NVDA is still starting up.")
	return textContainerObj.makeTextInfo("caret")


def getCaretObject() -> "documentBase.TextContainerObject":
	"""Gets the object which contains the caret.
	This is normally the NVDAObject with focus, unless it has a browse mode tree interceptor to return instead.
	@return: The object containing the caret.
	@note: Note: this may not be the NVDA Object closest to the caret, EG an edit text box may have focus,
	and contain multiple NVDAObjects closer to the caret position, consider instead:
		ti = getCaretPosition()
		ti.expand(textInfos.UNIT_CHARACTER)
		closestObj = ti.NVDAObjectAtStart
	"""
	obj = getFocusObject()
	ti = obj.treeInterceptor
	if isinstance(ti,treeInterceptorHandler.DocumentTreeInterceptor) and ti.isReady and not ti.passThrough:
		return ti
	return obj
