# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from typing import cast
import unittest
from unittest.mock import MagicMock

from winAPI._powerTracking import (
	BATTERY_LIFE_TIME_UNKNOWN,
	BatteryFlag,
	PowerState,
	_ReportContext,
	SystemPowerStatus,
	_getSpeechForBatteryStatus,
)


class Test_GetSpeechForBatteryStatus(unittest.TestCase):
	def setUp(self) -> None:
		self.testPowerStatus = cast(
			SystemPowerStatus,
			MagicMock(SystemPowerStatus())
		)

	def test_fetch_status_fetchFailed(self):
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=None,
			context=_ReportContext.FETCH_STATUS,
			oldPowerState=PowerState.UNKNOWN,
		)
		self.assertEqual(
			["Unknown power status"],
			actualSpeech,
		)

	def test_fetch_status_fetchSuccessful_unknownPowerStatus(self):
		self.testPowerStatus.BatteryFlag = BatteryFlag.UNKNOWN
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.FETCH_STATUS,
			oldPowerState=PowerState.UNKNOWN,
		)
		self.assertEqual(
			["Unknown power status"],
			actualSpeech,
		)

	def test_fetch_status_fetchSuccessful_noSystemBattery(self):
		self.testPowerStatus.BatteryFlag = 0 ^ BatteryFlag.NO_SYSTEM_BATTERY
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.FETCH_STATUS,
			oldPowerState=PowerState.UNKNOWN,
		)
		self.assertEqual(
			["No system battery"],
			actualSpeech,
		)

	def test_fetch_status_full_report(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = 3660
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.FETCH_STATUS,
			oldPowerState=PowerState.AC_OFFLINE,
		)
		self.assertEqual(
			['1 percent', '1 hour and 1 minute remaining', "Unplugged"],
			actualSpeech,
		)

	def test_ac_status_change_statusUnchanged_ignore(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.AC_STATUS_CHANGE,
			oldPowerState=PowerState.AC_OFFLINE,
		)
		self.assertEqual(
			[],
			actualSpeech,
		)

	def test_ac_status_change_statusChanged_connected(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_ONLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = 3660
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.AC_STATUS_CHANGE,
			oldPowerState=PowerState.AC_OFFLINE,
		)
		self.assertEqual(
			["Plugged in", '1 percent', '1 hour and 1 minute remaining'],
			actualSpeech,
		)

	def test_ac_status_change_statusChanged_disconnected(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = 3660
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.AC_STATUS_CHANGE,
			oldPowerState=PowerState.AC_ONLINE,
		)
		self.assertEqual(
			["Unplugged", '1 percent', '1 hour and 1 minute remaining'],
			actualSpeech,
		)

	def test_ac_status_change_batteryLifetimeUnknown(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = BATTERY_LIFE_TIME_UNKNOWN
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.AC_STATUS_CHANGE,
			oldPowerState=PowerState.AC_ONLINE,
		)
		self.assertEqual(
			["Unplugged", '1 percent'],
			actualSpeech,
		)

	def test_ac_status_change_batteryLifePercent(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifePercent = 7
		self.testPowerStatus.BatteryLifeTime = BATTERY_LIFE_TIME_UNKNOWN
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			context=_ReportContext.AC_STATUS_CHANGE,
			oldPowerState=PowerState.AC_ONLINE,
		)
		self.assertEqual(
			["Unplugged", '7 percent'],
			actualSpeech,
		)
