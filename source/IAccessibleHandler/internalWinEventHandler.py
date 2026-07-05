# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020-2026 NV Access Limited, Bill Dengler
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Provides Windows event hooks and processing using either the in-process limiter
or the optional external limiter DLL.
"""

from ctypes import ArgumentError, CDLL, c_int, wintypes
import threading

from typing import Any, Callable, Dict

import config
import core
from NVDAHelper import winEventLimiter as winEventLimiterLib
from winBindings.user32 import WINEVENTPROC
import winUser
from .utils import getWinEventLogInfo, isMSAADebugLoggingEnabled

from comInterfaces import IAccessible2Lib as IA2


from .orderedWinEventLimiter import OrderedWinEventLimiter, MENU_EVENTIDS
from logHandler import log

# The win event limiter for all winEvents
winEventLimiter = OrderedWinEventLimiter()

# The loaded winEventLimiter dll, only set while initialized in external mode.
_externalWinEventLimiterDll: CDLL | None = None

# UIA initializes first and may explicitly add an event from a callback thread.
# Hold those calls until initialize has published the selected limiter.
_limiterSelectionComplete: threading.Event = threading.Event()

# #3831: Stuff related to deferring of events for foreground changes.
# See pumpAll for details.
MAX_FOREGROUND_DEFERS = 2
_deferUntilForegroundWindow = None
_foregroundDefers = 0

winEventIDsToNVDAEventNames = {
	winUser.EVENT_SYSTEM_DESKTOPSWITCH: "desktopSwitch",
	winUser.EVENT_SYSTEM_FOREGROUND: "gainFocus",
	winUser.EVENT_SYSTEM_ALERT: "alert",
	winUser.EVENT_SYSTEM_MENUSTART: "menuStart",
	winUser.EVENT_SYSTEM_MENUEND: "menuEnd",
	winUser.EVENT_SYSTEM_MENUPOPUPSTART: "menuStart",
	winUser.EVENT_SYSTEM_MENUPOPUPEND: "menuEnd",
	winUser.EVENT_SYSTEM_SCROLLINGSTART: "scrollingStart",
	# We don't need switchStart.
	winUser.EVENT_SYSTEM_SWITCHEND: "switchEnd",
	winUser.EVENT_OBJECT_FOCUS: "gainFocus",
	winUser.EVENT_OBJECT_SHOW: "show",
	winUser.EVENT_OBJECT_HIDE: "hide",
	winUser.EVENT_OBJECT_DESTROY: "destroy",
	winUser.EVENT_OBJECT_DESCRIPTIONCHANGE: "descriptionChange",
	winUser.EVENT_OBJECT_LOCATIONCHANGE: "locationChange",
	winUser.EVENT_OBJECT_NAMECHANGE: "nameChange",
	winUser.EVENT_OBJECT_SELECTION: "selection",
	winUser.EVENT_OBJECT_SELECTIONADD: "selectionAdd",
	winUser.EVENT_OBJECT_SELECTIONREMOVE: "selectionRemove",
	winUser.EVENT_OBJECT_SELECTIONWITHIN: "selectionWithIn",
	winUser.EVENT_OBJECT_STATECHANGE: "stateChange",
	winUser.EVENT_OBJECT_VALUECHANGE: "valueChange",
	winUser.EVENT_OBJECT_LIVEREGIONCHANGED: "liveRegionChange",
	IA2.IA2_EVENT_TEXT_CARET_MOVED: "caret",
	IA2.IA2_EVENT_DOCUMENT_LOAD_COMPLETE: "documentLoadComplete",
	IA2.IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED: "IA2AttributeChange",
	IA2.IA2_EVENT_PAGE_CHANGED: "pageChange",
}

_processDestroyWinEvent = None


def processDestroyWinEvent(window: int, objectID: int, childID: int) -> None:
	"""Call the destroy handler registered by L{initialize}, if still active."""
	handler = _processDestroyWinEvent
	if handler is None:
		return
	handler(window, objectID, childID)


# C901: winEventCallback is too complex
def winEventCallback(
	handle: int | None,
	eventID: int,
	window: int | None,
	objectID: int,
	childID: int,
	threadID: int,
	timestamp: int,
) -> None:  # noqa: C901
	# Keep this logic aligned with MessagePumpThread::_handleWinEvent
	# and EventLimiterThread::_preprocessEvent in the external limiter.
	if window is None:
		window = 0
	if isMSAADebugLoggingEnabled():
		log.debug(
			f"Hook received winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
		)
	try:
		# Ignore all object IDs from alert onwards (sound, nativeom etc) as we don't support them
		if objectID <= winUser.OBJID_ALERT:
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"objectID not supported. "
					f"Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
			return
		# Ignore all locationChange events except ones for the caret
		if eventID == winUser.EVENT_OBJECT_LOCATIONCHANGE and objectID != winUser.OBJID_CARET:
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"locationChange for something other than the caret. "
					f"Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
			return
		if eventID == winUser.EVENT_OBJECT_DESTROY:
			processDestroyWinEvent(window, objectID, childID)
			return
		# Change window objIDs to client objIDs for better reporting of objects
		if (objectID == 0) and (childID == 0):
			objectID = winUser.OBJID_CLIENT
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"Changing OBJID_WINDOW to OBJID_CLIENT "
					f"for winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
		# Ignore events with invalid window handles
		isWindow = winUser.isWindow(window) if window else 0
		if window == 0 or (
			not isWindow
			and eventID
			in (
				winUser.EVENT_SYSTEM_SWITCHSTART,
				winUser.EVENT_SYSTEM_SWITCHEND,
				winUser.EVENT_SYSTEM_MENUEND,
				winUser.EVENT_SYSTEM_MENUPOPUPEND,
			)
		):
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"Changing NULL or invalid window to desktop window "
					f"for winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
			window = winUser.getDesktopWindow()
		elif not isWindow:
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"Invalid window. "
					f"Dropping winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
			return

		windowClassName = winUser.getClassName(window)
		# Excel produces UI automation events
		# Which are proxied by Windows into MSAA winEvents.
		# However in certain builds of Excel 2016
		# calling UIAHasServerSideProvider on the EXCEL7 window in responce to these events
		# causes a freeze of several seconds.
		# As we don't need these MSAA events for our Excel support, just ignore them early.
		if windowClassName == "EXCEL7" and objectID > 0:
			log.debug(
				f"Dropping UIA proxied event for Excel7 window. "
				f"WinEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
			)
			return
		if windowClassName == "ConsoleWindowClass":
			# #10113: we need to use winEvents to track the real thread for console windows.
			consoleWindowsToThreadIDs[window] = threadID

		# Modern IME candidate list windows fire menu events which confuse us
		# and can't be used properly in conjunction with input composition support.
		if windowClassName == "Microsoft.IME.UIManager.CandidateWindow.Host" and eventID in MENU_EVENTIDS:
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"Dropping menu event for IME window. "
					f"WinEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
			return
		if eventID == winUser.EVENT_SYSTEM_FOREGROUND:
			# We never want to see foreground events for the Program Manager or Shell (task bar)
			if windowClassName in ("Progman", "Shell_TrayWnd"):
				if isMSAADebugLoggingEnabled():
					log.debug(
						f"Progman or shell_trayWnd window. "
						f"Dropping winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
					)
				return
			# #3831: Event handling can be deferred if Windows takes a while to change the foreground window.
			# See pumpAll for details.
			global _deferUntilForegroundWindow, _foregroundDefers
			_deferUntilForegroundWindow = window
			_foregroundDefers = 0
			if isMSAADebugLoggingEnabled():
				log.debug(
					f"Recording foreground defer "
					f"for WinEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
				)
		if windowClassName == "MSNHiddenWindowClass":
			# HACK: Events get fired by this window in Windows Live Messenger 2009 when it starts. If we send a
			# WM_NULL to this window at this point (which happens in accessibleObjectFromEvent), Messenger will
			# silently exit (#677). Therefore, completely ignore these events, which is useless to us anyway.
			return
		if isMSAADebugLoggingEnabled():
			log.debug(
				f"Adding winEvent to limiter: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
			)
		if winEventLimiter.addEvent(eventID, window, objectID, childID, threadID):
			core.requestPump(immediate=eventID == winUser.EVENT_OBJECT_FOCUS)
	except Exception:
		log.error("winEventCallback", exc_info=True)


# Register internal object event with IAccessible
cWinEventCallback = WINEVENTPROC(winEventCallback)
# A list to store handles received from setWinEventHook, for use with unHookWinEvent
winEventHookIDs = []


@winEventLimiterLib.NotifyCallback
def _newEventsCallback(hasFocusEvent: int):
	# #14928: focus events are pumped immediately rather than after a delay.
	core.requestPump(immediate=bool(hasFocusEvent))


def addEvent(
	eventID: int,
	window: int,
	objectID: int,
	childID: int,
	threadID: int,
) -> bool:
	"""Add a winEvent to whichever limiter is active.

	Events explicitly added while the external limiter is active must enter the DLL's
	input buffer. This preserves their chronology relative to hooked winEvents before
	limiting and focus selection.

	Returns Whether the event was accepted by the active limiter.
	"""
	_limiterSelectionComplete.wait()
	dll = _externalWinEventLimiterDll
	if dll is not None:
		return (
			dll.winEventLimiter_addEvent(
				eventID,
				window,
				objectID,
				childID,
				threadID,
			)
			== 0
		)
	return winEventLimiter.addEvent(
		eventID,
		window,
		objectID,
		childID,
		threadID,
	)


def _initializeExternal() -> CDLL | None:
	"""Load the external winEventLimiter dll and start receiving winEvents from it.

	Returns the started dll, or None if it could not be loaded or failed to start.
	"""
	try:
		dll = winEventLimiterLib.getWinEventLimiterDll()
		eventIds = sorted(winEventIDsToNVDAEventNames)
		eventIdsArg = (wintypes.DWORD * len(eventIds))(*eventIds)
		res = dll.winEventLimiter_start(
			_newEventsCallback,
			eventIdsArg,
			len(eventIds),
		)
	except (OSError, AttributeError, ArgumentError):
		log.error("Could not load or start the winEventLimiter dll", exc_info=True)
		return None
	if res != 0:
		log.error(f"Could not start the winEventLimiter dll, error code {res}")
		return None
	return dll


def _registerInternalHooks():
	"""Hook winEvents on NVDA's main thread, processing them with the in-process limiter."""
	for eventType in winEventIDsToNVDAEventNames:
		hookID = winUser.setWinEventHook(eventType, eventType, 0, cWinEventCallback, 0, 0, 0)
		if hookID:
			winEventHookIDs.append(hookID)
		else:
			log.error(
				f"initialize: could not register callback for"
				f" event {eventType} ({winEventIDsToNVDAEventNames[eventType]})",
			)


def initialize(
	processDestroyWinEventFunc: Callable[
		[
			c_int,  # window
			c_int,  # objectID
			c_int,  # childID
		],
		None,
	],
):
	global _externalWinEventLimiterDll, _processDestroyWinEvent
	_limiterSelectionComplete.clear()
	try:
		_processDestroyWinEvent = processDestroyWinEventFunc
		# Read once at initialization: changing the flag requires an NVDA restart.
		shouldUseExternal = bool(config.conf["IAccessible"]["externalWinEventLimiter"])
		dll: CDLL | None = _initializeExternal() if shouldUseExternal else None
		if dll is None:
			# Either the external limiter is disabled,
			# or it failed to load or start;
			# fall back to hooking winEvents on NVDA's main thread.
			_registerInternalHooks()
		_externalWinEventLimiterDll = dll
	finally:
		# UIA callbacks must never remain blocked if initialization raises.
		_limiterSelectionComplete.set()


def terminate():
	global _externalWinEventLimiterDll
	global _processDestroyWinEvent, _deferUntilForegroundWindow, _foregroundDefers
	dll = _externalWinEventLimiterDll
	_externalWinEventLimiterDll = None
	# UIA terminates after IAccessible, so its shutdown callbacks must not block
	# waiting for a limiter that will never be initialized again.
	_limiterSelectionComplete.set()
	if dll is not None:
		dll.winEventLimiter_stop()
	for handle in winEventHookIDs:
		winUser.unhookWinEvent(handle)
	winEventHookIDs.clear()
	# Reset the state that initialize() and event processing established, so a stale
	# destroy handler or foreground defer can never leak into a later initialize
	# (or from one unit test into another).
	_processDestroyWinEvent = None
	_deferUntilForegroundWindow = None
	_foregroundDefers = 0
	winEventLimiter.clear()
	consoleWindowsToThreadIDs.clear()


def _fetchExternalEventData(
	flush: Callable[[], int | None],
	getCount: Callable[[], int],
	getEvents: Callable[[int, int, Any], int],
) -> tuple[bool, list[tuple[int, int, int, int, int]]]:
	"""Flush and fetch one of the external limiter's event queues."""
	# Only the regular flush returns 1 for a defer; the destroy flush returns
	# None.
	if flush() == 1:
		return True, []
	eventCount = getCount()
	data = (winEventLimiterLib.EventData * eventCount)()
	countFetched = getEvents(0, eventCount, data)
	return False, [
		(
			int(e.idEvent),
			int(e.hwnd) if e.hwnd else 0,
			int(e.idObject),
			int(e.idChild),
			int(e.dwEventThread),
		)
		for e in data[:countFetched]
	]


def _fetchExternalDestroyEvents() -> tuple[bool, list[tuple[int, int, int]]]:
	"""Fetch the destroy events collected by the external winEventLimiter dll since the last
	core pump.

	Destroys are snapshotted independently of the regular flush so pumpAll can process them
	before it captures this cycle's focus: processing a destroy may correct the focus
	(#2695), and the in-process implementation handles destroys at hook-callback time,
	which is always before pumpAll runs. They are never held back by a foreground defer,
	for the same reason.

	Returns a (destroysLost, destroys) tuple.
		destroysLost is True when the dll could not preserve per-window destroy handling,
		either because events were discarded under a sustained flood or a pending destroy
		reached the regular-event defer cap. The caller must then treat every cached object
		as potentially destroyed.
		destroys are raw (window, objectID, childID) tuples for destroyed objects.
	"""
	dll = _externalWinEventLimiterDll
	if dll is None:
		return False, []
	_deferred, destroyEvents = _fetchExternalEventData(
		dll.winEventLimiter_flushDestroyEvents,
		dll.winEventLimiter_getDestroyEventCount,
		dll.winEventLimiter_getDestroyEvents,
	)
	destroysLost = takeLostDestroyEvents()
	if destroyEvents and isMSAADebugLoggingEnabled():
		log.debug(
			f"Number of destroy events fetched from the winEventLimiter dll: {len(destroyEvents)}",
		)
	return destroysLost, [
		(window, objectID, childID) for _eventID, window, objectID, childID, _threadID in destroyEvents
	]


def takeLostDestroyEvents() -> bool:
	"""Report and consume the external limiter's pending destroy-recovery flag."""
	dll = _externalWinEventLimiterDll
	if dll is None:
		return False
	destroysLost = bool(dll.winEventLimiter_takeLostDestroys())
	if destroysLost:
		log.warning(
			"The winEventLimiter dll could not preserve per-window destroy "
			"handling; treating every cached object as potentially destroyed",
		)
	return destroysLost


def fetchDestroyEvents() -> tuple[bool, list[tuple[int, int, int]]]:
	"""Fetch pending destroys.

	Returns a (destroysLost, destroys) tuple (see L{_fetchExternalDestroyEvents}).
	Both are falsy when the internal limiter is active: it processes destroys at
	hook-callback time and never sheds them.
	"""
	return _fetchExternalDestroyEvents()


def _fetchExternalEvents(
	alwaysAllowedObject: tuple[int, int, int] | None = None,
) -> tuple[bool, list[tuple[int, int, int, int]]]:
	"""Fetch the winEvents collected by the external winEventLimiter dll since the last core pump.

	Per-event decisions made inside the dll (dropping, remapping and limiting) are not
	logged; only the events that survive limiting are visible here.

	alwaysAllowedObject is a (window, objectID, childID) tuple of the object whose events
		must never be dropped by the dll's per-thread limit, i.e. the focused object (#11520),
		or None to clear the exemption.
	Returns a (deferred, winEvents) tuple.
		deferred is True when the dll deferred the flush because a foreground
		change is still settling (#3831), or a destroy arrived after this cycle's
		destroy snapshot. Nothing was flushed, the dll has already requested another
		pump, and the caller should hold its whole cycle.
		winEvents are (eventID, window, objectID, childID) tuples in
		chronological order.
	"""
	dll = _externalWinEventLimiterDll
	if dll is None:
		return False, []
	normalizedAlwaysAllowedObject = alwaysAllowedObject or (0, 0, 0)
	dll.winEventLimiter_setAlwaysAllowedObject(*normalizedAlwaysAllowedObject)
	deferred, fetchedEvents = _fetchExternalEventData(
		dll.winEventLimiter_flushEvents,
		dll.winEventLimiter_getEventCount,
		dll.winEventLimiter_getEvents,
	)
	if deferred:
		if isMSAADebugLoggingEnabled():
			log.debug(
				"The winEventLimiter dll deferred this flush for a pending "
				"foreground change or destroy event",
			)
		return True, []
	debugLogging = isMSAADebugLoggingEnabled()
	if debugLogging:
		log.debug(
			f"Number of events fetched from the winEventLimiter dll: {len(fetchedEvents)}",
		)
	winEvents = []
	for eventID, window, objectID, childID, threadID in fetchedEvents:
		if debugLogging:
			log.debug(
				f"Emitting winEvent {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
			)
		winEvents.append((eventID, window, objectID, childID))
	return False, winEvents


def flushEvents(
	alwaysAllowedObject: tuple[int, int, int] | None = None,
) -> tuple[bool, list[tuple[int, int, int, int]]]:
	"""Flush the active limiter and report whether this cycle was deferred."""
	dll = _externalWinEventLimiterDll
	if dll is not None:
		return _fetchExternalEvents(alwaysAllowedObject)
	if not _shouldGetEvents():
		return True, []
	allowedObjects: list[tuple[int, int, int]] = []
	if alwaysAllowedObject is not None:
		allowedObjects.append(alwaysAllowedObject)
	return False, winEventLimiter.flushEvents(allowedObjects)


def _shouldGetEvents():
	global _deferUntilForegroundWindow, _foregroundDefers
	if _deferUntilForegroundWindow:
		# #3831: Sometimes, a foreground event is fired,
		# but GetForegroundWindow() takes a short while to return this new foreground.
		curForegroundWindow = winUser.getForegroundWindow()
		curForegroundClassName = winUser.getClassName(curForegroundWindow)
		futureForegroundClassName = winUser.getClassName(_deferUntilForegroundWindow)
		if _foregroundDefers < MAX_FOREGROUND_DEFERS and curForegroundWindow != _deferUntilForegroundWindow:
			# Wait a core cycle before handling events to give the foreground window time to update.
			core.requestPump()
			_foregroundDefers += 1
			if isMSAADebugLoggingEnabled():
				log.debugWarning(
					f"Foreground still {curForegroundWindow} ({curForegroundClassName}). "
					f"Deferring until foreground is {_deferUntilForegroundWindow} ({futureForegroundClassName}), "
					f"defer count {_foregroundDefers}",
				)
			return False
		else:
			# Either the foreground window is now correct
			# or we've already had the maximum number of defers.
			# (Sometimes, foreground events are fired even when the foreground hasn't actually changed.)
			if curForegroundWindow != _deferUntilForegroundWindow:
				log.debugWarning(
					"Foreground took too long to change. "
					f"Foreground still {curForegroundWindow} ({curForegroundClassName}). "
					f"Should be {_deferUntilForegroundWindow} ({futureForegroundClassName})",
				)
			_deferUntilForegroundWindow = None
	return True


#: Maps from console windows (ConsoleWindowClass) to thread IDs
# Windows hacks GetWindowThreadProcessId to return the input thread of the first attached process in a console
# But NVDA really requires to know the actual thread the window was created in,
# I.e. inside conhost,
# In order to handle speaking of typed characters etc.
# winEventCallback adds these whenever it sees an event for ConsoleWindowClass windows,
# As winEvents always contain the true thread ID.
# Only populated in internal mode; use L{getConsoleWindowThreadID} to also cover
# external mode, where the winEventLimiter dll records the mapping instead.
consoleWindowsToThreadIDs: Dict[int, int] = {}


def getConsoleWindowThreadID(window: int) -> int:
	"""The thread a console (ConsoleWindowClass) window was really created in (#10113, #10554),
	whichever winEvent source is active, or 0 if unknown.
	"""
	dll = _externalWinEventLimiterDll
	if dll is not None:
		return dll.winEventLimiter_getConsoleThreadID(window)
	return consoleWindowsToThreadIDs.get(window, 0)
