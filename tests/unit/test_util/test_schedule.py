# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited.

from datetime import datetime
import unittest
from unittest.mock import MagicMock

import NVDAState
from utils.schedule import ScheduleThread, initialize, terminate


class ScheduleThreadTests(unittest.TestCase):
	def setUp(self):
		self.oldNVDAStateGetStartTime = NVDAState.getStartTime
		NVDAState.getStartTime = MagicMock(return_value=datetime.now().timestamp())
		initialize()

	def tearDown(self):
		terminate()
		NVDAState.getStartTime = self.oldNVDAStateGetStartTime

	def test_scheduleDailyJobAtStartUp(self):
		scheduledVals = [0, 0, 0]

		def incrementA(scheduledVals: list):
			scheduledVals[0] += 1

		def incrementB(scheduledVals: list):
			scheduledVals[1] += 1

		def incrementC(scheduledVals: list):
			scheduledVals[2] += 1

		ScheduleThread.scheduleDailyJobAtStartUp(incrementA, scheduledVals)
		ScheduleThread.scheduleDailyJobAtStartUp(incrementB, scheduledVals)
		ScheduleThread.scheduleDailyJobAtStartUp(incrementC, scheduledVals)

		expectedResult = [0, 0, 0]
		self.assertEqual(scheduledVals, expectedResult)
		for jobIndex in range(3):
			# Simulate a forced job run
			startTime = NVDAState.getStartTime()
			currentJob = ScheduleThread.scheduledJobs[jobIndex]

			# Ensure that the job is scheduled to run at the expected time
			expectedSecsOffsetMin = jobIndex * ScheduleThread.DAILY_JOB_MINUTE_OFFSET * 60
			expectedSecsOffsetMax = (jobIndex + 1) * ScheduleThread.DAILY_JOB_MINUTE_OFFSET * 60
			nextRun = currentJob.next_run.timestamp()
			actualSecsOffset = nextRun - startTime
			self.assertLessEqual(
				actualSecsOffset,
				expectedSecsOffsetMax,
				f"Job {jobIndex} did not scheduled as expected. Job: {currentJob}"
			)
			self.assertGreaterEqual(
				actualSecsOffset,
				expectedSecsOffsetMin,
				f"Job {jobIndex} did not scheduled as expected. Job: {currentJob}"
			)

			# Ensure the job runs as expected
			currentJob.run()
			expectedResult[jobIndex] += 1
			self.assertEqual(
				scheduledVals,
				expectedResult,
				f"Job {jobIndex} did not run as expected. Scheduled jobs: {ScheduleThread.scheduledJobs}"
			)
