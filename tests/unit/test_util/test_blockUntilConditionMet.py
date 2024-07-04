# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule."""

from typing import (
	Any,
	Callable,
	Type,
)
import unittest
from unittest.mock import patch

from utils.blockUntilConditionMet import blockUntilConditionMet


class _FakeTimer:
	"""
	Used to simulate the passage of time.
	Patches sleeping and getting the current time,
	so that the module under test is not dependent on real world time.
	"""

	POLL_INTERVAL = 0.1

	def __init__(self) -> None:
		self._fakeTime: float = 0.0

	def sleep(self, secs: float) -> None:
		"""Patch for utils.blockUntilConditionMet.sleep"""
		self._fakeTime += secs

	def time(self) -> float:
		"""Patch for utils.blockUntilConditionMet.timer"""
		return self._fakeTime

	def getValue(self) -> float:
		"""Used to test the getValue parameter of utils.blockUntilConditionMet.blockUntilConditionMet"""
		return self.time()

	def createShouldStopEvaluator(self, succeedAfterSeconds: float) -> Callable[[Any], bool]:
		"""Used to test the shouldStopEvaluator parameter of utils.blockUntilConditionMet.blockUntilConditionMet"""

		def _shouldStopEvaluator(_value: Any) -> bool:
			return self._fakeTime >= succeedAfterSeconds

		return _shouldStopEvaluator


class _Timer_SlowSleep(_FakeTimer):
	"""
	Adds an extra amount of sleep when sleep is called to simulate
	the device taking longer than expected.
	"""

	def sleep(self, secs: float) -> None:
		return super().sleep(secs + 2 * self.POLL_INTERVAL)


class _Timer_SlowGetValue(_FakeTimer):
	"""
	Adds an extra amount of sleep when getValue is called to simulate
	the function taking a significant amount of time.
	"""

	def getValue(self) -> float:
		self._fakeTime += 2 * self.POLL_INTERVAL
		return super().getValue()


class _Timer_SlowShouldStop(_FakeTimer):
	"""
	Adds an extra amount of sleep when shouldStopEvaluator is called to simulate
	the function taking a significant amount of time.
	"""

	def createShouldStopEvaluator(self, succeedAfterSeconds: float) -> Callable[[Any], bool]:
		"""Used to test the shouldStopEvaluator parameter of utils.blockUntilConditionMet.blockUntilConditionMet"""

		def _shouldStopEvaluator(_value: Any):
			self._fakeTime += 2 * self.POLL_INTERVAL
			return self._fakeTime >= succeedAfterSeconds

		return _shouldStopEvaluator


class Test_blockUntilConditionMet_Timer(unittest.TestCase):
	"""
	Tests blockUntilConditionMet against a timer, which simulates the passage of time.
	Ensures that blockUntilConditionMet succeeds just before timeout, and fails just after timeout.
	"""

	_TimerClass: Type[_FakeTimer] = _FakeTimer
	"""Test suites which inherit from Test_blockUntilConditionMet_Timer will override the TimerClass"""

	def setUp(self) -> None:
		self._timer = self._TimerClass()
		self._sleepPatch = patch("utils.blockUntilConditionMet.sleep", new_callable=lambda: self._timer.sleep)
		self._sleepPatch.start()
		self._timerPatch = patch("utils.blockUntilConditionMet.timer", new_callable=lambda: self._timer.time)
		self._timerPatch.start()

	def tearDown(self) -> None:
		self._sleepPatch.stop()
		self._timerPatch.stop()

	def test_condition_succeeds_before_timeout(self):
		giveUpAfterSeconds = 5
		success, _endTimeOrNone = blockUntilConditionMet(
			getValue=self._timer.getValue,
			giveUpAfterSeconds=giveUpAfterSeconds,
			shouldStopEvaluator=self._timer.createShouldStopEvaluator(
				succeedAfterSeconds=giveUpAfterSeconds - _FakeTimer.POLL_INTERVAL,
			),
			intervalBetweenSeconds=_FakeTimer.POLL_INTERVAL,
		)

		timeElapsed = self._timer.time()
		self.assertTrue(
			success,
			msg=f"Test condition failed unexpectedly due to timeout. Elapsed time: {timeElapsed:.2f}s",
		)
		self.assertGreater(giveUpAfterSeconds, timeElapsed)

	def test_condition_fails_on_timeout(self):
		giveUpAfterSeconds = 5
		success, _endTimeOrNone = blockUntilConditionMet(
			getValue=self._timer.getValue,
			giveUpAfterSeconds=giveUpAfterSeconds,
			shouldStopEvaluator=self._timer.createShouldStopEvaluator(
				succeedAfterSeconds=giveUpAfterSeconds + _FakeTimer.POLL_INTERVAL,
			),
			intervalBetweenSeconds=_FakeTimer.POLL_INTERVAL,
		)
		timeElapsed = self._timer.time()
		self.assertFalse(
			success,
			msg=f"Test condition succeeded unexpectedly before timeout. Elapsed time: {timeElapsed:.2f}s",
		)
		self.assertGreaterEqual(timeElapsed, giveUpAfterSeconds)


class Test_blockUntilConditionMet_Timer_SlowShouldStop(Test_blockUntilConditionMet_Timer):
	TimerClass = _Timer_SlowShouldStop


class Test_blockUntilConditionMet_Timer_SlowGetValue(Test_blockUntilConditionMet_Timer):
	TimerClass = _Timer_SlowGetValue


class Test_blockUntilConditionMet_Timer_SlowSleep(Test_blockUntilConditionMet_Timer):
	TimerClass = _Timer_SlowSleep


class Test_blockUntilConditionMet_general(unittest.TestCase):
	def test_lowPollRate_Raises(self):
		with self.assertRaises(AssertionError):
			blockUntilConditionMet(
				getValue=lambda: None,
				giveUpAfterSeconds=1,
				intervalBetweenSeconds=1 / 1000,
			)
