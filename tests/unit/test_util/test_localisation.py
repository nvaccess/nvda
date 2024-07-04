# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited.

"""Unit tests for the localisation submodule."""

from datetime import timedelta
import unittest

from utils.localisation import (
	TimeOutputFormat,
)


class Test_TimeOutputFormat(unittest.TestCase):
	def _test_time_format(
		self,
		exampleTimeDelta: timedelta,
		expectedTimeOutputFormat: TimeOutputFormat,
		expectedOutputStr: str,
	):
		"""Covers testing convertTimeDeltaToTimeOutputFormat, parseTimeDeltaToFormatted"""
		actualTimeOutputFormat = TimeOutputFormat.convertTimeDeltaToTimeOutputFormat(exampleTimeDelta)
		actualOutputStr = TimeOutputFormat.parseTimeDeltaToFormatted(exampleTimeDelta)
		self.assertIs(expectedTimeOutputFormat, actualTimeOutputFormat)
		self.assertEqual(expectedOutputStr, actualOutputStr)

	def test_32days(self):
		self._test_time_format(
			exampleTimeDelta=timedelta(days=32, hours=23, minutes=54, seconds=33),
			expectedTimeOutputFormat=TimeOutputFormat.DAYS,
			expectedOutputStr="32 days 23:54:33",
		)

	def test_2days(self):
		self._test_time_format(
			exampleTimeDelta=timedelta(days=2, hours=23, minutes=54, seconds=33),
			expectedTimeOutputFormat=TimeOutputFormat.DAYS,
			expectedOutputStr="2 days 23:54:33",
		)

	def test_1day(self):
		self._test_time_format(
			exampleTimeDelta=timedelta(days=1, hours=23, minutes=54, seconds=33),
			expectedTimeOutputFormat=TimeOutputFormat.DAY,
			expectedOutputStr="1 day 23:54:33",
		)

	def test_hours(self):
		self._test_time_format(
			exampleTimeDelta=timedelta(hours=23, minutes=54, seconds=33),
			expectedTimeOutputFormat=TimeOutputFormat.HOURS,
			expectedOutputStr="23:54:33",
		)

	def test_minutes(self):
		self._test_time_format(
			exampleTimeDelta=timedelta(minutes=54, seconds=33),
			expectedTimeOutputFormat=TimeOutputFormat.MINUTES,
			expectedOutputStr="54:33",
		)

	def test_seconds(self):
		self._test_time_format(
			exampleTimeDelta=timedelta(seconds=33),
			expectedTimeOutputFormat=TimeOutputFormat.SECONDS,
			expectedOutputStr="33",
		)
