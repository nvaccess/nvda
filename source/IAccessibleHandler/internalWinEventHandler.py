# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Provides a non-threaded (limited by GIL) Windows Event Hook and processing.
"""

from ctypes import WINFUNCTYPE, c_int

from typing import Dict, Callable

import core
import winUser

from comInterfaces.IAccessible2Lib import (
	IA2_EVENT_TEXT_CARET_MOVED,
	IA2_EVENT_DOCUMENT_LOAD_COMPLETE,
	IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED,
	IA2_EVENT_PAGE_CHANGED,
)

from .orderedWinEventLimiter import OrderedWinEventLimiter, MENU_EVENTIDS
from logHandler import log

# The win event limiter for all winEvents
winEventLimiter = OrderedWinEventLimiter()

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
	winUser.EVENT_OBJECT_REORDER: "reorder",
	winUser.EVENT_OBJECT_SELECTION: "selection",
	winUser.EVENT_OBJECT_SELECTIONADD: "selectionAdd",
	winUser.EVENT_OBJECT_SELECTIONREMOVE: "selectionRemove",
	winUser.EVENT_OBJECT_SELECTIONWITHIN: "selectionWithIn",
	winUser.EVENT_OBJECT_STATECHANGE: "stateChange",
	winUser.EVENT_OBJECT_VALUECHANGE: "valueChange",
	winUser.EVENT_OBJECT_LIVEREGIONCHANGED: "liveRegionChange",
	IA2_EVENT_TEXT_CARET_MOVED: "caret",
	IA2_EVENT_DOCUMENT_LOAD_COMPLETE: "documentLoadComplete",
	IA2_EVENT_OBJECT_ATTRIBUTE_CHANGED: "IA2AttributeChange",
	IA2_EVENT_PAGE_CHANGED: "pageChange",
}

_processDestroyWinEvent = None


# C901: winEventCallback is too complex
def winEventCallback(handle, eventID, window, objectID, childID, threadID, timestamp):  # noqa: C901
	try:
		# Ignore all object IDs from alert onwards (sound, nativeom etc) as we don't support them
		if objectID <= winUser.OBJID_ALERT:
			return
		# Ignore all locationChange events except ones for the caret
		if eventID == winUser.EVENT_OBJECT_LOCATIONCHANGE and objectID != winUser.OBJID_CARET:
			return
		if eventID == winUser.EVENT_OBJECT_DESTROY:
			_processDestroyWinEvent(window, objectID, childID)
			return
		# Change window objIDs to client objIDs for better reporting of objects
		if (objectID == 0) and (childID == 0):
			objectID = winUser.OBJID_CLIENT
		# Ignore events with invalid window handles
		isWindow = winUser.isWindow(window) if window else 0
		if window == 0 or (
			not isWindow and eventID in (
				winUser.EVENT_SYSTEM_SWITCHSTART,
				winUser.EVENT_SYSTEM_SWITCHEND,
				winUser.EVENT_SYSTEM_MENUEND,
				winUser.EVENT_SYSTEM_MENUPOPUPEND,
			)
		):
			window = winUser.getDesktopWindow()
		elif not isWindow:
			return

		if childID < 0:
			tempWindow = window
			while (
				tempWindow
				and not winUser.getWindowStyle(tempWindow) & winUser.WS_POPUP
				and winUser.getClassName(tempWindow) == "MozillaWindowClass"
			):
				tempWindow = winUser.getAncestor(tempWindow, winUser.GA_PARENT)
			if tempWindow and winUser.getClassName(tempWindow).startswith('Mozilla'):
				window = tempWindow

		windowClassName = winUser.getClassName(window)
		if windowClassName == "ConsoleWindowClass":
			# #10113: we need to use winEvents to track the real thread for console windows.
			consoleWindowsToThreadIDs[window] = threadID

		# Modern IME candidate list windows fire menu events which confuse us
		# and can't be used properly in conjunction with input composition support.
		if windowClassName == "Microsoft.IME.UIManager.CandidateWindow.Host" and eventID in MENU_EVENTIDS:
			return
		# At the moment we can't handle show, hide or reorder events on Mozilla Firefox Location bar,
		# as there are just too many of them Ignore show, hide and reorder on MozillaDropShadowWindowClass
		# windows.
		if (
			windowClassName.startswith('Mozilla')
			and eventID in (
				winUser.EVENT_OBJECT_SHOW,
				winUser.EVENT_OBJECT_HIDE,
				winUser.EVENT_OBJECT_REORDER
			) and childID < 0
		):
			# Mozilla Gecko can sometimes fire win events on a catch-all window which isn't really the real window
			# Move up the ancestry to find the real mozilla Window and use that
			if winUser.getClassName(window) == 'MozillaDropShadowWindowClass':
				return
		if eventID == winUser.EVENT_SYSTEM_FOREGROUND:
			# We never want to see foreground events for the Program Manager or Shell (task bar)
			if windowClassName in ("Progman", "Shell_TrayWnd"):
				return
			# #3831: Event handling can be deferred if Windows takes a while to change the foreground window.
			# See pumpAll for details.
			global _deferUntilForegroundWindow, _foregroundDefers
			_deferUntilForegroundWindow = window
			_foregroundDefers = 0
		if windowClassName == "MSNHiddenWindowClass":
			# HACK: Events get fired by this window in Windows Live Messenger 2009 when it starts. If we send a
			# WM_NULL to this window at this point (which happens in accessibleObjectFromEvent), Messenger will
			# silently exit (#677). Therefore, completely ignore these events, which is useless to us anyway.
			return
		if winEventLimiter.addEvent(eventID, window, objectID, childID, threadID):
			core.requestPump()
	except:  # noqa: E722 Bare except
		log.error("winEventCallback", exc_info=True)


# Register internal object event with IAccessible
cWinEventCallback = WINFUNCTYPE(None, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(winEventCallback)
# A list to store handles received from setWinEventHook, for use with unHookWinEvent
winEventHookIDs = []


def initialize(
		processDestroyWinEventFunc: Callable[[
			c_int,  # window
			c_int,  # objectID
			c_int,  # childID
		], None]
):
	global _processDestroyWinEvent
	_processDestroyWinEvent = processDestroyWinEventFunc
	for eventType in winEventIDsToNVDAEventNames:
		hookID = winUser.setWinEventHook(eventType, eventType, 0, cWinEventCallback, 0, 0, 0)
		if hookID:
			winEventHookIDs.append(hookID)
		else:
			log.error(
				f"initialize: could not register callback for"
				f" event {eventType} ({winEventIDsToNVDAEventNames[eventType]})"
			)


def terminate():
	for handle in winEventHookIDs:
		winUser.unhookWinEvent(handle)
	winEventHookIDs.clear()


def _shouldGetEvents():
	global _deferUntilForegroundWindow, _foregroundDefers
	if _deferUntilForegroundWindow:
		# #3831: Sometimes, a foreground event is fired,
		# but GetForegroundWindow() takes a short while to return this new foreground.
		if (
			_foregroundDefers < MAX_FOREGROUND_DEFERS
			and winUser.getForegroundWindow() != _deferUntilForegroundWindow
		):
			# Wait a core cycle before handling events to give the foreground window time to update.
			core.requestPump()
			_foregroundDefers += 1
			return False
		else:
			# Either the foreground window is now correct
			# or we've already had the maximum number of defers.
			# (Sometimes, foreground events are fired even when the foreground hasn't actually changed.)
			_deferUntilForegroundWindow = None
	return True


#: Maps from console windows (ConsoleWindowClass) to thread IDs
# Windows hacks GetWindowThreadProcessId to return the input thread of the first attached process in a console
# But NVDA really requires to know the actual thread the window was created in,
# I.e. inside conhost,
# In order to handle speaking of typed characters etc.
# winEventCallback adds these whenever it sees an event for ConsoleWindowClass windows,
# As winEvents always contain the true thread ID.
consoleWindowsToThreadIDs: Dict[int, int] = {}
