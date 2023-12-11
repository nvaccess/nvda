# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2023 NV Access Limited, Babbage B.V., Joseph Lee

import threading
import typing
from typing import Optional
from comtypes import COMError

import garbageHandler
import queueHandler
import api
import speech
from speech.commands import _CancellableSpeechCommand
import treeInterceptorHandler
import controlTypes
from logHandler import log
import globalPluginHandler
import config
import winUser
import extensionPoints
import oleacc
from utils.security import objectBelowLockScreenAndWindowsIsLocked
import winVersion

if typing.TYPE_CHECKING:
	import NVDAObjects


#Some dicts to store event counts by name and or obj
_pendingEventCountsByName={}
_pendingEventCountsByObj={}
_pendingEventCountsByNameAndObj={}
# Needed to ensure updates are atomic, as these might be updated from multiple threads simultaneously.
_pendingEventCountsLock=threading.RLock()

#: the last object queued for a gainFocus event. Useful for code running outside NVDA's core queue 
lastQueuedFocusObject=None


# Handle virtual desktop switch announcements in Windows 10 and later
_virtualDesktopName: Optional[str] = None
_canAnnounceVirtualDesktopNames: bool = winVersion.getWinVer() >= winVersion.WIN10_1903


def queueEvent(eventName,obj,**kwargs):
	"""Queues an NVDA event to be executed.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@type eventName: string
	"""
	_trackFocusObject(eventName, obj)
	with _pendingEventCountsLock:
		_pendingEventCountsByName[eventName]=_pendingEventCountsByName.get(eventName,0)+1
		_pendingEventCountsByObj[obj]=_pendingEventCountsByObj.get(obj,0)+1
		_pendingEventCountsByNameAndObj[(eventName,obj)]=_pendingEventCountsByNameAndObj.get((eventName,obj),0)+1
	queueHandler.queueFunction(
		queueHandler.eventQueue,
		_queueEventCallback,
		eventName,
		obj,
		kwargs,
		_immediate=eventName == "gainFocus"
	)


def _queueEventCallback(eventName,obj,kwargs):
	with _pendingEventCountsLock:
		curCount=_pendingEventCountsByName.get(eventName,0)
		if curCount>1:
			_pendingEventCountsByName[eventName]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByName[eventName]
		curCount=_pendingEventCountsByObj.get(obj,0)
		if curCount>1:
			_pendingEventCountsByObj[obj]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByObj[obj]
		curCount=_pendingEventCountsByNameAndObj.get((eventName,obj),0)
		if curCount>1:
			_pendingEventCountsByNameAndObj[(eventName,obj)]=(curCount-1)
		elif curCount==1:
			del _pendingEventCountsByNameAndObj[(eventName,obj)]
	executeEvent(eventName,obj,**kwargs)

def isPendingEvents(eventName=None,obj=None):
	"""Are there currently any events queued?
	@param eventName: an optional name of an event type. If given then only if there are events of this type queued will it return True.
	@type eventName: string
	@param obj: the NVDAObject the event is for
	@type obj: L{NVDAObjects.NVDAObject}
	@returns: True if there are events queued, False otherwise.
	@rtype: boolean
	"""
	if not eventName and not obj:
		return bool(len(_pendingEventCountsByName))
	elif not eventName and obj:
		return obj in _pendingEventCountsByObj
	elif eventName and not obj:
		return eventName in _pendingEventCountsByName
	elif eventName and obj:
		return (eventName,obj) in _pendingEventCountsByNameAndObj


class _EventExecuter(garbageHandler.TrackedObject):
	"""Facilitates execution of a chain of event functions.
	L{gen} generates the event functions and positional arguments.
	L{next} calls the next function in the chain.
	"""

	def __init__(self, eventName, obj, kwargs):
		self.kwargs = kwargs
		self._gen = self.gen(eventName, obj)
		try:
			self.next()
		except StopIteration:
			pass
		finally:
			del self._gen

	def next(self):
		func, args = next(self._gen)
		try:
			return func(*args, **self.kwargs)
		except TypeError:
			log.warning("Could not execute function {func} defined in {module} module; kwargs: {kwargs}".format(
				func=func.__name__,
				module=func.__module__ or "unknown",
				kwargs=self.kwargs
			), exc_info=True)
			return extensionPoints.callWithSupportedKwargs(func, *args, **self.kwargs)

	def gen(self, eventName, obj):
		funcName = "event_%s" % eventName

		# Global plugin level.
		for plugin in globalPluginHandler.runningPlugins:
			func = getattr(plugin, funcName, None)
			if func:
				yield func, (obj, self.next)

		# App module level.
		app = obj.appModule
		if app:
			func = getattr(app, funcName, None)
			if func:
				yield func, (obj, self.next)

		# Tree interceptor level.
		treeInterceptor = obj.treeInterceptor
		if treeInterceptor:
			func = getattr(treeInterceptor, funcName, None)
			if func and (getattr(func,'ignoreIsReady',False) or treeInterceptor.isReady):
				yield func, (obj, self.next)

		# NVDAObject level.
		func = getattr(obj, funcName, None)
		if func:
			yield func, ()


WAS_GAIN_FOCUS_OBJ_ATTR_NAME = "wasGainFocusObj"


def _trackFocusObject(eventName: str, obj: "NVDAObjects.NVDAObject") -> None:
	""" Keeps track of lastQueuedFocusObject and sets wasGainFocusObj attr on objects.
	:param eventName: the event type, eg "gainFocus"
	:param obj: the object to track if focused
	"""
	global lastQueuedFocusObject

	if (
		eventName == "gainFocus"
		and not objectBelowLockScreenAndWindowsIsLocked(
			obj,
			shouldLog=config.conf["debugLog"]["events"],
		)
	):
		lastQueuedFocusObject = obj


class FocusLossCancellableSpeechCommand(_CancellableSpeechCommand):
	def __init__(self, obj, reportDevInfo: bool):
		from NVDAObjects import NVDAObject
		if not isinstance(obj, NVDAObject):
			log.warning("Unhandled object type. Expected all objects to be descendant from NVDAObject")
			raise TypeError(f"Unhandled object type: {obj!r}")
		self._obj = obj
		super(FocusLossCancellableSpeechCommand, self).__init__(reportDevInfo=reportDevInfo)

		if self.isLastFocusObj():
			# Objects may be re-used.
			# WAS_GAIN_FOCUS_OBJ_ATTR_NAME state should be cleared at some point?
			# perhaps instead keep a weak ref list of obj that had focus, clear on keypress?

			# Assumption: we only process one focus event at a time, so even if several focus events are queued,
			# all focused objects will still gain this tracking attribute. Otherwise, this may need to be set via
			# api.setFocusObject when api.getFocusObject is set.
			setattr(obj, WAS_GAIN_FOCUS_OBJ_ATTR_NAME, True)
		elif not hasattr(obj, WAS_GAIN_FOCUS_OBJ_ATTR_NAME):
			setattr(obj, WAS_GAIN_FOCUS_OBJ_ATTR_NAME, False)

	def _checkIfValid(self) -> bool:
		stillValid = (
			self.isLastFocusObj()
			or not self.previouslyHadFocus()
			or self.isAncestorOfCurrentFocus()
			# Ensure titles for dialogs gaining focus are reported, EG NVDA Find dialog
			or self.isForegroundObject()
			# Ensure menu items are reported when focus is gained to the menu start (see #12624).
			or self.isMenuItemOfCurrentFocus()
		)
		return stillValid

	def _getDevInfo(self) -> str:
		return (
			f"isLast: {self.isLastFocusObj()}"
			f", previouslyHad: {self.previouslyHadFocus()}"
			f", isAncestorOfCurrentFocus: {self.isAncestorOfCurrentFocus()}"
			f", is foreground obj {self.isForegroundObject()}"
			f", isMenuItemOfCurrentFocus: {self.isMenuItemOfCurrentFocus()}"
		)

	def isLastFocusObj(self):
		# Use '==' rather than 'is' because obj may have been created multiple times
		# pointing to the same underlying object.
		return self._obj == api.getFocusObject()

	def previouslyHadFocus(self):
		return getattr(self._obj, WAS_GAIN_FOCUS_OBJ_ATTR_NAME, False)

	def isAncestorOfCurrentFocus(self):
		return self._obj in api.getFocusAncestors()

	def isForegroundObject(self):
		foreground = api.getForegroundObject()
		return self._obj is foreground or self._obj == foreground

	def isMenuItemOfCurrentFocus(self) -> bool:
		"""
		Checks if the current object is a menu item of the current focus.
		The only known case where this returns True is the following (see #12624):
		
		When opening a submenu in certain applications (like Thunderbird 78.12),
		NVDA can process a menu start event after the first item in the menu is focused.
		The menu start event causes a focus event on the menu, taking NVDA's focus from the menu item.
		Additionally, the "menu" parent of the submenu item is not keyboard focusable, and is separate from
		the menu item which triggered the submenu.
		The object tree in this case (menu item > submenu (not keyboard focusable) > submenu item).
		The focus event order after activating the menu item's sub menu is (submenu item, submenu).
		"""
		from NVDAObjects import IAccessible
		lastFocus = api.getFocusObject()
		_isMenuItemOfCurrentFocus = (
			self._obj.parent
			and isinstance(self._obj, IAccessible.IAccessible)
			and isinstance(lastFocus, IAccessible.IAccessible)
			and self._obj.IAccessibleRole == oleacc.ROLE_SYSTEM_MENUITEM
			and lastFocus.IAccessibleRole == oleacc.ROLE_SYSTEM_MENUPOPUP
			and self._obj.parent == lastFocus
		)
		if _isMenuItemOfCurrentFocus:
			# Change this to log.error for easy debugging
			log.debugWarning(
				"This parent menu was not announced properly, "
				"and should have been focused before the submenu item.\n"
				f"Object info: {self._obj.devInfo}\n"
				f"Object parent info: {self._obj.parent.devInfo}\n"
			)
		return _isMenuItemOfCurrentFocus


def _getFocusLossCancellableSpeechCommand(
		obj,
		reason: controlTypes.OutputReason
) -> Optional[_CancellableSpeechCommand]:
	if reason != controlTypes.OutputReason.FOCUS or not speech.manager._shouldCancelExpiredFocusEvents():
		return None
	from NVDAObjects import NVDAObject
	if not isinstance(obj, NVDAObject):
		log.warning("Unhandled object type. Expected all objects to be descendant from NVDAObject")
		return None

	shouldReportDevInfo = speech.manager._shouldDoSpeechManagerLogging()
	return FocusLossCancellableSpeechCommand(obj, reportDevInfo=shouldReportDevInfo)


def executeEvent(
		eventName: str,
		obj: "NVDAObjects.NVDAObject",
		**kwargs,
) -> None:
	"""Executes an NVDA event.
	@param eventName: the name of the event type (e.g. 'gainFocus', 'nameChange')
	@param obj: the object the event is for
	@param kwargs: Additional event parameters as keyword arguments.
	"""
	if objectBelowLockScreenAndWindowsIsLocked(
		obj,
		shouldLog=config.conf["debugLog"]["events"],
	):
		return
	try:
		global _virtualDesktopName
		isGainFocus = eventName == "gainFocus"
		# Allow NVDAObjects to redirect focus events to another object of their choosing.
		if isGainFocus and obj.focusRedirect:
			obj = obj.focusRedirect
		sleepMode = obj.sleepMode
		# Handle possible virtual desktop name change event.
		# More effective in Windows 10 Version 1903 and later.
		from NVDAObjects.window import Window
		if (
			eventName == "nameChange"
			and isinstance(obj, Window)
			and obj.windowClassName == "#32769"
			and _canAnnounceVirtualDesktopNames
		):
			import core
			_virtualDesktopName = obj.name
			core.callLater(250, handlePossibleDesktopNameChange)
		if isGainFocus and not doPreGainFocus(obj, sleepMode=sleepMode):
			return
		elif not sleepMode and eventName == "documentLoadComplete" and not doPreDocumentLoadComplete(obj):
			return
		elif not sleepMode:
			_EventExecuter(eventName, obj, kwargs)
	except Exception:
		log.exception(f"error executing event: {eventName} on {obj} with extra args of {kwargs}")


def handlePossibleDesktopNameChange() -> None:
	"""
	Reports the new virtual desktop name if changed.
	On Windows versions lower than Windows 10, this function does nothing.
	"""
	global _virtualDesktopName
	# Virtual desktop switch announcement works more effectively in Version 1903 and later.
	if not _canAnnounceVirtualDesktopNames:
		return
	if _virtualDesktopName:
		import ui
		ui.message(_virtualDesktopName)
		_virtualDesktopName = None


def doPreGainFocus(obj: "NVDAObjects.NVDAObject", sleepMode: bool = False) -> bool:
	if objectBelowLockScreenAndWindowsIsLocked(
		obj,
		shouldLog=config.conf["debugLog"]["events"],
	):
		return False
	oldFocus = api.getFocusObject()
	oldTreeInterceptor = oldFocus.treeInterceptor if oldFocus else None
	if not api.setFocusObject(obj):
		return False
	if speech.manager._shouldCancelExpiredFocusEvents():
		log._speechManagerDebug("executeEvent: Removing cancelled speech commands.")
		# ask speechManager to check if any of it's queued utterances should be cancelled
		# Note: Removing cancelled speech commands should happen after all dependencies for the isValid check
		# have been updated:
		# - obj.WAS_GAIN_FOCUS_OBJ_ATTR_NAME
		# - api.setFocusObject()
		# - api.getFocusAncestors()
		# When these are updated:
		# - obj.WAS_GAIN_FOCUS_OBJ_ATTR_NAME
		#   - Set during creation of the _CancellableSpeechCommand.
		# - api.getFocusAncestors() via api.setFocusObject() called in doPreGainFocus
		speech._manager.removeCancelledSpeechCommands()

	if api.getFocusDifferenceLevel() <= 1:
		newForeground = api.getDesktopObject().objectInForeground()
		if not newForeground:
			log.debugWarning("Can not get real foreground, resorting to focus ancestors")
			ancestors = api.getFocusAncestors()
			if len(ancestors) > 1:
				newForeground = ancestors[1]
			else:
				newForeground = obj
		if not api.setForegroundObject(newForeground):
			return False
		executeEvent('foreground', newForeground)
	handlePossibleDesktopNameChange()
	if sleepMode:
		return True
	# Fire focus entered events for all new ancestors of the focus if this is a gainFocus event
	for parent in api.getFocusAncestors()[api.getFocusDifferenceLevel():]:
		executeEvent("focusEntered", parent)
	if obj.treeInterceptor is not oldTreeInterceptor:
		if hasattr(oldTreeInterceptor, "event_treeInterceptor_loseFocus"):
			oldTreeInterceptor.event_treeInterceptor_loseFocus()
		if (
			obj.treeInterceptor
			and obj.treeInterceptor.isReady
			and hasattr(obj.treeInterceptor, "event_treeInterceptor_gainFocus")
		):
			obj.treeInterceptor.event_treeInterceptor_gainFocus()
	return True

def doPreDocumentLoadComplete(obj):
	focusObject=api.getFocusObject()
	if (not obj.treeInterceptor or not obj.treeInterceptor.isAlive or obj.treeInterceptor.shouldPrepare) and (obj==focusObject or obj in api.getFocusAncestors()):
		ti=treeInterceptorHandler.update(obj)
		if ti:
			obj.treeInterceptor=ti
			#Focus may be in this new treeInterceptor, so force focus to look up its treeInterceptor
			focusObject.treeInterceptor=treeInterceptorHandler.getTreeInterceptor(focusObject)
	return True

#: set of (eventName, processId, windowClassName) of events to accept.
_acceptEvents = set()
#: Maps process IDs to sets of events so they can be cleaned up when the process exits.
_acceptEventsByProcess = {}

def requestEvents(eventName=None, processId=None, windowClassName=None):
	"""Request that particular events be accepted from a platform API.
	Normally, L{shouldAcceptEvent} rejects certain events, including
	most show events, events indicating changes in background processes, etc.
	This function allows plugins to override this for specific cases;
	e.g. to receive show events from a specific control or
	to receive certain events even when in the background.
	Note that NVDA may block some events at a lower level and doesn't listen for some event types at all.
	In these cases, you will not be able to override this.
	This should generally be called when a plugin is instantiated.
	All arguments must be provided.
	"""
	if not eventName or not processId or not windowClassName:
		raise ValueError("eventName, processId or windowClassName not specified")
	entry = (eventName, processId, windowClassName)
	procEvents = _acceptEventsByProcess.get(processId)
	if not procEvents:
		procEvents = _acceptEventsByProcess[processId] = set()
	procEvents.add(entry)
	_acceptEvents.add(entry)

def handleAppTerminate(appModule):
	global _acceptEvents
	events = _acceptEventsByProcess.pop(appModule.processID, None)
	if not events:
		return
	_acceptEvents -= events

def shouldAcceptEvent(eventName, windowHandle=None):
	"""Check whether an event should be accepted from a platform API.
	Creating NVDAObjects and executing events can be expensive
	and might block the main thread noticeably if the object is slow to respond.
	Therefore, this should be used before NVDAObject creation to filter out any unnecessary events.
	A platform API handler may do its own filtering before this.
	"""
	if not windowHandle:
		# We can't filter without a window handle.
		return True
	wClass = winUser.getClassName(windowHandle)
	key = (eventName,
		winUser.getWindowThreadProcessID(windowHandle)[0],
		wClass)
	if key in _acceptEvents:
		return True
	if eventName == "valueChange" and config.conf["presentation"]["progressBarUpdates"]["reportBackgroundProgressBars"]:
		return True
	if eventName == "hide":
		return False
	if eventName == "show":
		# Only accept 'show' events for specific cases, as otherwise we get flooded.
		return wClass in (
			"Frame Notification Bar", # notification bars
			"tooltips_class32", # tooltips
			"mscandui21.candidate", "mscandui40.candidate", "MSCandUIWindow_Candidate", # IMM candidates
			"TTrayAlert", # 5405: Skype
		)
	if eventName == "alert" and winUser.getClassName(winUser.getAncestor(windowHandle, winUser.GA_PARENT)) == "ToastChildWindowClass":
		# Toast notifications.
		return True
	if eventName in ("menuEnd", "switchEnd", "desktopSwitch"):
		# #5302, #5462: These events can be fired on the desktop window
		# or windows that would otherwise be blocked.
		# Platform API handlers will translate these events to focus events anyway,
		# so we must allow them here.
		return True
	if windowHandle == winUser.getDesktopWindow():
		# #5595: Events for the cursor get mapped to the desktop window.
		return True

	# #6713: Edge (and soon all UWP apps) will no longer have windows as descendants of the foreground window.
	# However, it does look like they are always  equal to or descendants of the "active" window of the input thread. 
	gi = winUser.getGUIThreadInfo(0)
	if wClass.startswith('Windows.UI.Core'):
		if winUser.isDescendantWindow(gi.hwndActive,windowHandle):
			return True

	fg = winUser.getForegroundWindow()
	# #5504, #14916, #15432 : Some windows, such as in the Office ribbon or Edge downloads window
	# aren't directly beneath the foreground window, so our foreground application checks fail.
	# However, they share the same root owner and events for them should be allowed.
	if (
		winUser.getAncestor(windowHandle, winUser.GA_ROOTOWNER)
		== winUser.getAncestor(fg, winUser.GA_ROOTOWNER)
	):
		return True
	if (winUser.isDescendantWindow(fg, windowHandle)
			# #3899, #3905: Covers cases such as the Firefox Page Bookmarked window and OpenOffice/LibreOffice context menus.
			or winUser.isDescendantWindow(fg, winUser.getAncestor(windowHandle, winUser.GA_ROOTOWNER))):
		# This is for the foreground application.
		return True
	if (winUser.user32.GetWindowLongW(windowHandle, winUser.GWL_EXSTYLE) & winUser.WS_EX_TOPMOST
			or winUser.user32.GetWindowLongW(winUser.getAncestor(windowHandle, winUser.GA_ROOT), winUser.GWL_EXSTYLE) & winUser.WS_EX_TOPMOST):
		# This window or its root is a topmost window.
		# This includes menus, combo box pop-ups and the task switching list.
		return True
	# This may be an event for a windowless embedded Chrome document
	# (E.g. Microsoft Loop component).
	if wClass == "Chrome_RenderWidgetHostHWND":
		# The event is for a Chromium document
		if winUser.getClassName(gi.hwndFocus) == "Chrome_WidgetWin_0":
			# The real win32 focus is on a Chrome embedding window.
			# See if we can get from the event's Chromium document to the Chrome embedding window
			# via ancestors in the UIA tree.
			rootWindowHandle = winUser.getAncestor(windowHandle, winUser.GA_ROOT)
			import UIAHandler
			try:
				rootElement = UIAHandler.handler.clientObject.elementFromHandle(rootWindowHandle)
			except COMError:
				log.debugWarning("Could not create UIA element for root of Chromium document", exc_info=True)
			else:
				condition = UIAHandler.handler.clientObject.CreatePropertyCondition(
					UIAHandler.UIA_NativeWindowHandlePropertyId, gi.hwndFocus
				)
				try:
					walker = UIAHandler.handler.clientObject.CreateTreeWalker(condition)
					ancestorElement = walker.NormalizeElement(rootElement)
				except COMError:
					log.debugWarning("Unable to normalize root Chromium element to focused ancestor", exc_info=True)
					ancestorElement = None
				if ancestorElement:
					# The real focused window is an ancestor of the Chromium document in the UIA tree.
					return True
	return False
