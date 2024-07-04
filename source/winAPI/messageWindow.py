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


from . import (
	_displayTracking,
	_powerTracking,
)
from .types import HWNDValT
import extensionPoints
import windowUtils


pre_handleWindowMessage = extensionPoints.Action()
"""
Notifies when a window message has been received by NVDA.
This allows components to perform an action when certain system events occur,
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
	DISPLAY_CHANGE = 0x7E
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
				_powerTracking.reportACStateChange()
		elif msg == WindowMessage.DISPLAY_CHANGE:
			_displayTracking.reportScreenOrientationChange(lParam)
