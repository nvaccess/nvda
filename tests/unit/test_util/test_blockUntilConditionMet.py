# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule.
"""

import unittest
from unittest.mock import patch

from utils import blockUntilConditionMet as _moduleUnderTest


class _FakeTimer():
	"""
	Simulate sleeping and getting the current time,
	so that the module under test is not dependent on real world time.
	"""
	def __init__(self) -> None:
		self._fakeTime: float = 0.0

	def sleep(self, secs: float) -> None:
		self._fakeTime += secs

	def time(self):
		return self._fakeTime


class Test_blockUntilConditionMet(unittest.TestCase):
	def setUp(self) -> None:
		self._timer = _FakeTimer()

	def test_condition_succeeds_before_timeout(self):
		giveUpAfterSecs = 5
		pollInterval = 1
		startTime = self._timer.time()

		def succeedJustBeforeTimeOut(currentTime: float):
			return (currentTime - startTime) > (giveUpAfterSecs - pollInterval)

		with patch("time.sleep", new_callable=lambda: self._timer.sleep):
			with patch("time.perf_counter", new_callable=lambda: self._timer.time):
				success, endTimeOrNone = _moduleUnderTest.blockUntilConditionMet(
					getValue=self._timer.time,
					giveUpAfterSeconds=giveUpAfterSecs,
					shouldStopEvaluator=succeedJustBeforeTimeOut,
					intervalBetweenSeconds=pollInterval,
				)
		timeElapsed = self._timer.time() - startTime
		self.assertTrue(
			success,
			msg=f"Test condition failed unexpectedly due to timeout. Elapsed time: {timeElapsed:.2f}s"
		)
		self.assertGreater(giveUpAfterSecs, timeElapsed)

	def test_condition_fails_on_timeout(self):
		giveUpAfterSecs = 5
		pollInterval = 1
		startTime = self._timer.time()

		def succeedJustAfterTimeOut(currentTime: float):
			return (currentTime - startTime) > (giveUpAfterSecs + pollInterval)

		with patch("time.sleep", new_callable=lambda: self._timer.sleep):
			with patch("time.perf_counter", new_callable=lambda: self._timer.time):
				success, endTimeOrNone = _moduleUnderTest.blockUntilConditionMet(
					getValue=self._timer.time,
					giveUpAfterSeconds=giveUpAfterSecs,
					shouldStopEvaluator=succeedJustAfterTimeOut,
					intervalBetweenSeconds=pollInterval,
				)
		timeElapsed = self._timer.time() - startTime
		self.assertFalse(
			success,
			msg=f"Test condition succeeded unexpectedly before timeout. Elapsed time: {timeElapsed:.2f}s"
		)
		self.assertGreater(timeElapsed, giveUpAfterSecs)
