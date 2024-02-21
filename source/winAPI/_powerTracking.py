# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rui Batista, Cyrille Bougot
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
	Enum,
	IntEnum,
	IntFlag,
	auto,
	unique,
)
from typing import (
	List,
	Optional,
)

from logHandler import log
import ui
import winKernel


BATTERY_LIFE_TIME_UNKNOWN = 0xffffffff


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


_powerState: PowerState = PowerState.UNKNOWN


def initialize():
	"""
	The NVDA message window only handles changes of state.
	As such, to correctly ignore an initial power change event,
	which does not change the power state (e.g. a battery level drop),
	we fetch the initial power state manually.
	"""
	global _powerState
	systemPowerStatus = SystemPowerStatus()
	if (
		not winKernel.GetSystemPowerStatus(systemPowerStatus)
		or systemPowerStatus.BatteryFlag == BatteryFlag.UNKNOWN
	):
		log.error("Error retrieving system power status")
		return

	if systemPowerStatus.BatteryFlag & BatteryFlag.NO_SYSTEM_BATTERY:
		return

	_powerState = systemPowerStatus.ACLineStatus
	return


@unique
class _ReportContext(Enum):
	"""
	Used to determine the order of information, based on relevance to the user,
	when announcing power status information
	"""

	AC_STATUS_CHANGE = auto()
	"""e.g. a charger is connected/disconnected"""
	FETCH_STATUS = auto()
	"""e.g. when a user presses nvda+shift+b to fetch the current battery status"""


def reportACStateChange() -> None:
	_reportPowerStatus(_ReportContext.AC_STATUS_CHANGE)


def reportCurrentBatteryStatus() -> None:
	_reportPowerStatus(_ReportContext.FETCH_STATUS)


def _reportPowerStatus(context: _ReportContext) -> None:
	"""
	@param context: the context is used to order the announcement.
	When the context is AC_STATUS_CHANGE, this reports the current AC status first.
	When the context is FETCH_STATUS, this reports the remaining battery life first.
	"""
	global _powerState
	systemPowerStatus = _getPowerStatus()
	speechSequence = _getSpeechForBatteryStatus(systemPowerStatus, context, _powerState)
	if speechSequence:
		ui.message(" ".join(speechSequence))
	if systemPowerStatus is not None:
		_powerState = systemPowerStatus.ACLineStatus


def _getPowerStatus() -> Optional[SystemPowerStatus]:
	sps = SystemPowerStatus()
	systemPowerStatusUpdateResult = winKernel.GetSystemPowerStatus(sps)
	if not systemPowerStatusUpdateResult:
		log.error(f"Error retrieving power status: {ctypes.GetLastError()}")
		return None
	return sps


def _getSpeechForBatteryStatus(
		systemPowerStatus: Optional[SystemPowerStatus],
		context: _ReportContext,
		oldPowerState: PowerState,
) -> List[str]:
	if not systemPowerStatus or systemPowerStatus.BatteryFlag == BatteryFlag.UNKNOWN:
		# Translators: This is presented when there is an error retrieving the battery status.
		return [_("Unknown power status")]

	if systemPowerStatus.BatteryFlag & BatteryFlag.NO_SYSTEM_BATTERY:
		# Translators: This is presented when there is no battery such as desktop computers
		# and laptops with battery pack removed.
		return [_("No system battery")]

	if (
		context == _ReportContext.AC_STATUS_CHANGE
		and systemPowerStatus.ACLineStatus == oldPowerState
	):
		# Sometimes, the power change event double fires.
		# The power change event also fires when the battery level decreases by 3%.
		return []

	text: List[str] = []

	if context == _ReportContext.AC_STATUS_CHANGE:
		# When the AC status changes, users want to be alerted to the new AC status first.
		text.append(_getACStatusText(systemPowerStatus))
		text.extend(_getBatteryInformation(systemPowerStatus))
	elif context == _ReportContext.FETCH_STATUS:
		# When fetching the current battery status,
		# users want to know the current battery status first,
		# rather than the AC status which should be unchanged.
		text.extend(_getBatteryInformation(systemPowerStatus))
		text.append(_getACStatusText(systemPowerStatus))
	else:
		raise NotImplementedError(f"Unexpected _ReportContext: {context}")

	return text


def _getACStatusText(systemPowerStatus: SystemPowerStatus) -> str:
	# Translators: This is presented to inform the user of the current battery percentage.
	if systemPowerStatus.ACLineStatus & PowerState.AC_ONLINE:
		# Translators: Reported when the battery is plugged in, and now is charging.
		return _("Plugged in")
	else:
		# Translators: Reported when the battery is no longer plugged in, and now is not charging.
		return _("Unplugged")


def _getBatteryInformation(systemPowerStatus: SystemPowerStatus) -> List[str]:
	text: List[str] = []
	# Translators: This is presented to inform the user of the current battery percentage.
	text.append(_("%d percent") % systemPowerStatus.BatteryLifePercent)
	SECONDS_PER_HOUR = 3600
	SECONDS_PER_MIN = 60
	if systemPowerStatus.BatteryLifeTime != BATTERY_LIFE_TIME_UNKNOWN:
		nHours = systemPowerStatus.BatteryLifeTime // SECONDS_PER_HOUR
		hourText = ngettext(
			# Translators: This is the hour string part of the estimated remaining runtime of the laptop battery.
			# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "1 hour".
			"{hours:d} hour",
			"{hours:d} hours",
			nHours,
		).format(hours=nHours)
		nMinutes = (systemPowerStatus.BatteryLifeTime % SECONDS_PER_HOUR) // SECONDS_PER_MIN
		minuteText = ngettext(
			# Translators: This is the minute string part of the estimated remaining runtime of the laptop battery.
			# E.g. if the full string is "1 hour and 34 minutes remaining", this string is "34 minutes".
			"{minutes:d} minute",
			"{minutes:d} minutes",
			nMinutes,
		).format(minutes=nMinutes)
		# Translators: This is the main string for the estimated remaining runtime of the laptop battery.
		# E.g. hourText is replaced by "1 hour" and minuteText by "34 minutes".
		text.append(_("{hourText} and {minuteText} remaining").format(hourText=hourText, minuteText=minuteText))
	return text
