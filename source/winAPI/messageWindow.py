# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
A submodule for NVDA's message window, used for handling Window Messages.

Message windows can be used to handle communications from other processes, new NVDA instances and Windows.
"""

from enum import IntEnum
from typing import (
	Optional,
)

import wx

from . import (
	_displayTracking,
	_powerTracking,
	sessionTracking,
)
from .types import HWNDValT
import extensionPoints
import gui
import windowUtils


pre_handleWindowMessage = extensionPoints.Action()
"""
Notifies when a window message has been received by NVDA.
This allows components to perform an action when several system events occur,
such as power, screen orientation and hardware changes.

Handlers are called with three arguments.
@param msg: The window message.
@type msg: int
@param wParam: Additional message information.
@type wParam: int
@param lParam: Additional message information.
@type lParam: int
"""


class WindowMessage(IntEnum):
	DISPLAY_CHANGE = 0x7e
	"""
	WM_DISPLAYCHANGE

	https://docs.microsoft.com/en-us/windows/win32/gdi/wm-displaychange
	"""
	POWER_BROADCAST = 0x0218
	"""
	WM_POWERBROADCAST

	An application should process this event by calling the GetSystemPowerStatus function
	to retrieve the current power status of the computer.
	In particular, the application should check the
	ACLineStatus, BatteryFlag, BatteryLifeTime, and BatteryLifePercent members
	of the SYSTEM_POWER_STATUS structure for any changes.

	This event can occur when battery life drops to less than 5 minutes,
	or when the percentage of battery life drops below 10 percent,
	or if the battery life changes by 3 percent.

	https://docs.microsoft.com/en-us/windows/win32/power/pbt-apmpowerstatuschange
	"""

	WTS_SESSION_CHANGE = 0x02B1
	"""
	WM_WTSSESSION_CHANGE

	Windows Message for when a Session State Changes.
	Receiving these messages is registered by sessionTracking.register.
	handleSessionChange handles these messages.

	https://docs.microsoft.com/en-us/windows/win32/api/wtsapi32/nf-wtsapi32-wtsregistersessionnotification
	"""


class _MessageWindow(windowUtils.CustomWindow):
	className = "wxWindowClassNR"
	"""
	#3763: In wxPython 3, the class name of frame windows changed from wxWindowClassNR to wxWindowNR.
	NVDA uses the main frame to check for and quit another instance of NVDA.
	To remain compatible with older versions of NVDA, create our own wxWindowClassNR.
	We don't need to do anything else because wx handles WM_QUIT for all windows.
	"""

	def __init__(self, windowName: Optional[str] = None):
		super().__init__(windowName)
		_displayTracking.initialize()
		_powerTracking.initialize()

		# Call must be paired with a call to sessionTracking.unregister
		self._isSessionTrackingRegistered = sessionTracking.register(self.handle)

	def warnIfSessionTrackingNotRegistered(self) -> None:
		if self._isSessionTrackingRegistered:
			return
		failedToRegisterMsg = _(
			# Translators: This is a warning to users, shown if NVDA cannot determine if
			# Windows is locked.
			"NVDA failed to register session tracking. "
			"While this instance of NVDA is running, "
			"your desktop will not be secure when Windows is locked. "
			"Restart NVDA? "
		)
		if wx.YES == gui.messageBox(
			failedToRegisterMsg,
			# Translators: This is a warning to users, shown if NVDA cannot determine if
			# Windows is locked.
			caption=_("NVDA could not start securely."),
			style=wx.ICON_ERROR | wx.YES_NO,
		):
			import core
			core.restart()

	def destroy(self):
		"""
		NVDA must unregister session tracking before destroying the message window.

		Windows API states that every registration of session tracking must be paired with
		de-registering session tracking.
		We cannot deregister session tracking after the message window has been destroyed.
		"""
		if self._isSessionTrackingRegistered:
			# Requires an active message window and a handle to unregister.
			sessionTracking.unregister(self.handle)
		super().destroy()

	def windowProc(self, hwnd: HWNDValT, msg: int, wParam: int, lParam: int) -> None:
		"""
		@param hwnd
		@param msg: The window message.
		@param wParam: Additional message information.
		@param lParam: Additional message information.
		"""
		pre_handleWindowMessage.notify(msg=msg, wParam=wParam, lParam=lParam)
		self.handleWindowMessage(msg, wParam, lParam)

	def handleWindowMessage(self, msg: int, wParam: int, lParam: int) -> None:
		"""
		@param msg: The window message.
		@param wParam: Additional message information.
		@param lParam: Additional message information.
		"""
		if msg == WindowMessage.POWER_BROADCAST:
			if wParam == _powerTracking.PowerBroadcast.APM_POWER_STATUS_CHANGE:
				_powerTracking.reportCurrentBatteryStatus(_powerTracking.ReportContext.AC_STATUS_CHANGE)
		elif msg == WindowMessage.DISPLAY_CHANGE:
			_displayTracking.reportScreenOrientationChange(lParam)
		elif msg == WindowMessage.WTS_SESSION_CHANGE:
			# If we are receiving WTS_SESSION_CHANGE events, _isSessionTrackingRegistered should be True
			sessionTracking.handleSessionChange(sessionTracking.WindowsTrackedSession(wParam), lParam)
