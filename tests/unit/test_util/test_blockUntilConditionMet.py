# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the blockUntilConditionMet submodule.
"""

from time import perf_counter as timer
import unittest

from utils.blockUntilConditionMet import blockUntilConditionMet

class Test_blockUntilConditionMet(unittest.TestCase):
	def test_condition_succeeds_before_timeout(self):
		giveUpAfterSecs = 0.5
		pollInterval = 0.1
		startTime = timer()
		succeedJustBeforeTimeOut = lambda value: (value - startTime) > (giveUpAfterSecs - pollInterval)
		success, endTimeOrNone = blockUntilConditionMet(
			getValue=timer,
			giveUpAfterSeconds=giveUpAfterSecs,
			shouldStopEvaluator=succeedJustBeforeTimeOut,
			intervalBetweenSeconds=pollInterval,
		)
		timeElapsed = timer() - startTime
		self.assertTrue(
			success,
			msg=f"Test condition failed unexpectedly due to timeout. Elapsed time: {timeElapsed:.2f}s"
		)
		self.assertGreater(giveUpAfterSecs, timeElapsed)

	def test_condition_fails_on_timeout(self):
		giveUpAfterSecs = 0.5
		pollInterval = 0.1
		startTime = timer()
		succeedJustAfterTimeOut = lambda value: (value - startTime) > (giveUpAfterSecs + pollInterval)
		success, endTimeOrNone = blockUntilConditionMet(
			getValue=timer,
			giveUpAfterSeconds=giveUpAfterSecs,
			shouldStopEvaluator=succeedJustAfterTimeOut,
			intervalBetweenSeconds=pollInterval,
		)
		timeElapsed = timer() - startTime
		self.assertFalse(
			success,
			msg=f"Test condition succeeded unexpectedly before timeout. Elapsed time: {timeElapsed:.2f}s"
		)
		self.assertGreater(timeElapsed, giveUpAfterSecs)
