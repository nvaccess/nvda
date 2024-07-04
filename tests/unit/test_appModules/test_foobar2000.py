# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited.

"""Unit tests for the foobar appModule."""

from datetime import timedelta
import unittest

from appModules.foobar2000 import (
	TimeOutputFormat,
	_getTimeOutputFormat,
	_parseTimeStrToTimeDelta,
)


class Test_TimeParsing(unittest.TestCase):
	def _test_time_format(
		self,
		exampleTimeStr: str,
		expectedTimeInputFormat: TimeOutputFormat,
		expectedTimeDelta: timedelta,
	):
		"""Covers testing _getTimeOutputFormat, _parseTimeStrToTimeDelta"""
		actualTimeInputFormat = _getTimeOutputFormat(exampleTimeStr)
		actualTimeDelta = _parseTimeStrToTimeDelta(exampleTimeStr)
		self.assertEqual(expectedTimeDelta, actualTimeDelta)
		self.assertIs(expectedTimeInputFormat, actualTimeInputFormat)

	def test_32days(self):
		"""Note days > 31 is not fully supported"""
		self._test_time_format(
			exampleTimeStr="32d 23:54:33",
			expectedTimeInputFormat=TimeOutputFormat.DAYS,
			expectedTimeDelta=None,
		)

	def test_2days(self):
		self._test_time_format(
			exampleTimeStr="2d 23:54:33",
			expectedTimeInputFormat=TimeOutputFormat.DAYS,
			expectedTimeDelta=timedelta(days=2, hours=23, minutes=54, seconds=33),
		)

	def test_1day(self):
		self._test_time_format(
			exampleTimeStr="1d 23:54:33",
			expectedTimeInputFormat=TimeOutputFormat.DAY,
			expectedTimeDelta=timedelta(days=1, hours=23, minutes=54, seconds=33),
		)

	def test_hours(self):
		self._test_time_format(
			exampleTimeStr="23:54:33",
			expectedTimeInputFormat=TimeOutputFormat.HOURS,
			expectedTimeDelta=timedelta(hours=23, minutes=54, seconds=33),
		)

	def test_minutes(self):
		self._test_time_format(
			exampleTimeStr="54:33",
			expectedTimeInputFormat=TimeOutputFormat.MINUTES,
			expectedTimeDelta=timedelta(minutes=54, seconds=33),
		)

	def test_seconds(self):
		self._test_time_format(
			exampleTimeStr="33",
			expectedTimeInputFormat=TimeOutputFormat.SECONDS,
			expectedTimeDelta=timedelta(seconds=33),
		)

	def test_None(self):
		self._test_time_format(
			exampleTimeStr="foo",
			expectedTimeInputFormat=None,
			expectedTimeDelta=None,
		)
