# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

from typing import cast
import unittest
from unittest.mock import MagicMock

from winAPI.powerTracking import (
	BATTERY_LIFE_TIME_UNKNOWN,
	BatteryFlag,
	PowerState,
	SystemPowerStatus,
	_getSpeechForBatteryStatus,
)


class Test_GetSpeechForBatteryStatus(unittest.TestCase):
	def setUp(self) -> None:
		self.testPowerStatus = cast(
			SystemPowerStatus,
			MagicMock(SystemPowerStatus())
		)

	def test_unknownPowerStatus_failedFetch(self):
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=None,
			onlyReportIfStatusChanged=False,
			oldPowerState=PowerState.UNKNOWN,
		)
		self.assertEqual(
			["Unknown power status"],
			actualSpeech,
		)

	def test_unknownPowerStatus_fetchSuccessful(self):
		self.testPowerStatus.BatteryFlag = BatteryFlag.UNKNOWN
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=False,
			oldPowerState=PowerState.UNKNOWN,
		)
		self.assertEqual(
			["Unknown power status"],
			actualSpeech,
		)

	def test_noSystemBattery(self):
		self.testPowerStatus.BatteryFlag = 0 ^ BatteryFlag.NO_SYSTEM_BATTERY
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=False,
			oldPowerState=PowerState.UNKNOWN,
		)
		self.assertEqual(
			["No system battery"],
			actualSpeech,
		)

	def test_statusUnchanged_ignore(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=True,
			oldPowerState=PowerState.AC_OFFLINE,
		)
		self.assertEqual(
			[],
			actualSpeech,
		)

	def test_statusUnchanged_report(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = 3660
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=False,
			oldPowerState=PowerState.AC_OFFLINE,
		)
		self.assertEqual(
			["AC disconnected", '1 percent', '1 hours and 1 minutes remaining'],
			actualSpeech,
		)

	def test_statusChanged_connected(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_ONLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = 3660
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=True,
			oldPowerState=PowerState.AC_OFFLINE,
		)
		self.assertEqual(
			["Charging battery", '1 percent', '1 hours and 1 minutes remaining'],
			actualSpeech,
		)

	def test_statusChanged_disconnected(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = 3660
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=True,
			oldPowerState=PowerState.AC_ONLINE,
		)
		self.assertEqual(
			["AC disconnected", '1 percent', '1 hours and 1 minutes remaining'],
			actualSpeech,
		)

	def test_batteryLifetimeUnknown(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifeTime = BATTERY_LIFE_TIME_UNKNOWN
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=True,
			oldPowerState=PowerState.AC_ONLINE,
		)
		self.assertEqual(
			["AC disconnected", '1 percent'],
			actualSpeech,
		)

	def test_batteryLifePercent(self):
		self.testPowerStatus.ACLineStatus = PowerState.AC_OFFLINE
		self.testPowerStatus.BatteryFlag = BatteryFlag.HIGH
		self.testPowerStatus.BatteryLifePercent = 7
		self.testPowerStatus.BatteryLifeTime = BATTERY_LIFE_TIME_UNKNOWN
		actualSpeech = _getSpeechForBatteryStatus(
			systemPowerStatus=self.testPowerStatus,
			onlyReportIfStatusChanged=True,
			oldPowerState=PowerState.AC_ONLINE,
		)
		self.assertEqual(
			["AC disconnected", '7 percent'],
			actualSpeech,
		)
