# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rui Batista
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Tracking was introduced so that NVDA has a mechanism to announce changes to the power state.

When NVDA receives a power status change Window Message,
we notify the user of the power status.
The power status can also be reported using script_say_battery_status.
"""

import ctypes
from enum import (
	IntEnum,
	IntFlag,
)
from typing import (
	List,
)

from logHandler import log
import ui
import winKernel


class PowerBroadcast(IntEnum):
	# https://docs.microsoft.com/en-us/windows/win32/power/wm-powerbroadcast
	APM_POWER_STATUS_CHANGE = 0xA
	"""
	Notifies applications of a change in the power status of the computer,
	such as a switch from battery power to A/C.
	The system also broadcasts this event when remaining battery power
	slips below the threshold specified by the user
	or if the battery power changes by a specified percentage.
	A window receives this event through the WM_POWERBROADCAST message.
	https://docs.microsoft.com/en-us/windows/win32/power/pbt-apmpowerstatuschange
	"""
	APM_RESUME_AUTOMATIC = 0x12
	"""
	Operation is resuming automatically from a low-power state.
	This message is sent every time the system resumes.
	"""
	APM_RESUME_SUSPEND = 0x7
	"""
	Operation is resuming from a low-power state.
	This message is sent after APM_RESUME_AUTOMATIC if the resume is triggered by user input,
	such as pressing a key.
	"""
	APM_SUSPEND = 0x4
	"""
	System is suspending operation.
	"""
	POWER_SETTING_CHANGE = 0x8013
	"""
	A power setting change event has been received.
	"""


class BatteryFlag(IntFlag):
	# https://docs.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-system_power_status
	HIGH = 0x1
	"""More than 66%"""
	LOW = 0x2
	"""Less than 33%"""
	CRITICAL = 0x4
	"""Less than 5%"""
	NO_SYSTEM_BATTERY = 0x80
	UNKNOWN = 0xFF


class PowerState(IntFlag):
	# https://docs.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-system_power_status
	AC_OFFLINE = 0x0
	AC_ONLINE = 0x1
	UNKNOWN = 0xFF


class SystemPowerStatus(ctypes.Structure):
	# https://docs.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-system_power_status
	_fields_ = [
		("ACLineStatus", ctypes.c_byte),
		("BatteryFlag", ctypes.c_byte),
		("BatteryLifePercent", ctypes.c_byte),
		("Reserved1", ctypes.c_byte),
		("BatteryLifeTime", ctypes.wintypes.DWORD),
		("BatteryFullLiveTime", ctypes.wintypes.DWORD)
	]

	BatteryFlag: BatteryFlag
	ACLineStatus: PowerState
	BatteryLifePercent: int
	BatteryLifeTime: int


_batteryState: PowerState = 0


def initialize():
	global _batteryState
	sps = SystemPowerStatus()
	if not winKernel.GetSystemPowerStatus(sps) or sps.BatteryFlag == BatteryFlag.UNKNOWN:
		log.error("Error retrieving system power status")
		return

	if sps.BatteryFlag & BatteryFlag.NO_SYSTEM_BATTERY:
		return

	_batteryState = sps.ACLineStatus
	return


def reportCurrentBatteryStatus(onlyReportIfStatusChanged: bool = False) -> None:
	"""
	@param onlyReportIfStatusChanged: sometimes multiple events may fire for a power status change.
	Set this to True to only report if the power status changes.
	"""
	global _batteryState
	sps = SystemPowerStatus()
	systemPowerStatusUpdateResult = winKernel.GetSystemPowerStatus(sps)
	if not systemPowerStatusUpdateResult:
		log.error(f"Error retrieving power status: {ctypes.GetLastError()}")

	if not systemPowerStatusUpdateResult or sps.BatteryFlag == BatteryFlag.UNKNOWN:
		# Translators: This is presented when there is an error retrieving the battery status.
		ui.message(_("Unknown power status"))
		return

	if sps.BatteryFlag & BatteryFlag.NO_SYSTEM_BATTERY:
		# Translators: This is presented when there is no battery such as desktop computers
		# and laptops with battery pack removed.
		ui.message(_("No system battery"))
		return

	if onlyReportIfStatusChanged and sps.ACLineStatus == _batteryState:
		# Sometimes, the power change event double fires.
		# The power change event also fires when the battery level decreases by 3%.
		return

	_batteryState = sps.ACLineStatus
	text: List[str] = []
	# Translators: This is presented to inform the user of the current battery percentage.
	if sps.ACLineStatus & PowerState.AC_ONLINE:
		# Translators: Reported when the battery is plugged in, and now is charging.
		text.append(_("Charging battery"))
	else:
		# Translators: Reported when the battery is no longer plugged in, and now is not charging.
		text.append(_("AC disconnected"))

	# Translators: This is presented to inform the user of the current battery percentage.
	text.append(_("%d percent") % sps.BatteryLifePercent)
	BATTERY_LIFE_TIME_UNKNOWN = 0xffffffff
	if sps.BatteryLifeTime != BATTERY_LIFE_TIME_UNKNOWN:
		# Translators: This is the estimated remaining runtime of the laptop battery.
		text.append(_("{hours:d} hours and {minutes:d} minutes remaining").format(
			hours=sps.BatteryLifeTime // 3600,
			minutes=(sps.BatteryLifeTime % 3600) // 60)
		)
	ui.message(" ".join(text))
