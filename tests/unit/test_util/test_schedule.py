# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited.

from datetime import datetime
import unittest
from unittest.mock import MagicMock

import schedule

import NVDAState
from utils.schedule import (
	JobClashError,
	ScheduleThread,
	ThreadTarget,
	initialize,
	terminate,
)


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

		ScheduleThread.scheduleDailyJobAtStartUp(incrementA, ThreadTarget.CUSTOM, scheduledVals)
		ScheduleThread.scheduleDailyJobAtStartUp(incrementB, ThreadTarget.CUSTOM, scheduledVals)
		ScheduleThread.scheduleDailyJobAtStartUp(incrementC, ThreadTarget.CUSTOM, scheduledVals)
		# Sanity checks (have failed in development)
		self.assertEqual(len(ScheduleThread.scheduledJobs), 3)
		self.assertEqual(ScheduleThread.scheduledDailyJobCount, 3)

		expectedResult = [0, 0, 0]
		self.assertEqual(scheduledVals, expectedResult)
		for jobIndex in range(3):
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
				f"Job {jobIndex} was not scheduled as expected. Job: {currentJob}"
			)
			self.assertGreaterEqual(
				actualSecsOffset,
				expectedSecsOffsetMin,
				f"Job {jobIndex} was not scheduled as expected. Job: {currentJob}"
			)

			# Ensure the job runs as expected
			currentJob.run()
			expectedResult[jobIndex] += 1
			self.assertEqual(
				scheduledVals,
				expectedResult,
				f"Job {jobIndex} did not run as expected. Scheduled jobs: {ScheduleThread.scheduledJobs}"
			)

	def test_scheduleJob(self):
		def jobFunc():
			# Job function implementation
			pass

		cronTime = "12:00"  # Example cron time
		jobSchedule = schedule.every().day.at(cronTime)

		# Call the scheduleJob method
		ScheduleThread.scheduleJob(jobFunc, jobSchedule, ThreadTarget.GUI)

		# Assert that the job is scheduled correctly
		self.assertEqual(len(ScheduleThread.scheduledJobs), 1)
		scheduledJob = ScheduleThread.scheduledJobs[0]
		self.assertEqual(f"{scheduledJob.at_time.hour:02d}:{scheduledJob.at_time.minute:02d}", cronTime)

	def test_scheduleJob_jobClash(self):
		def jobFunc():
			# Job function implementation
			pass

		cronTime = "12:00"  # Example cron time
		jobSchedule = schedule.every().day.at(cronTime)

		# Call the scheduleJob method
		ScheduleThread.scheduleJob(jobFunc, jobSchedule, ThreadTarget.GUI)

		with self.assertRaises(JobClashError):
			# Call the scheduleJob method with the same cron time
			ScheduleThread.scheduleJob(jobFunc, jobSchedule, ThreadTarget.GUI)

	def test_calculateDailyTimeOffset(self):
		todayAtMidnight = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
		NVDAState.getStartTime = MagicMock(return_value=todayAtMidnight.timestamp())
		# Call the _calculateDailyTimeOffset method
		offset = ScheduleThread._calculateDailyTimeOffset()
		# Assert that the offset is calculated correctly
		self.assertEqual(offset, f"00:{ScheduleThread.DAILY_JOB_MINUTE_OFFSET:02d}")
		
		ScheduleThread.scheduledDailyJobCount = 1
		offset = ScheduleThread._calculateDailyTimeOffset()
		self.assertEqual(offset, f"00:{ScheduleThread.DAILY_JOB_MINUTE_OFFSET * 2:02d}")

		# Test the case where the start time is 11:59 to ensure the hour offset is calculated correctly
		NVDAState.getStartTime = MagicMock(return_value=todayAtMidnight.replace(hour=11, minute=59).timestamp())
		ScheduleThread.scheduledDailyJobCount = 0
		offset = ScheduleThread._calculateDailyTimeOffset()
		expectedMinOffset = (ScheduleThread.DAILY_JOB_MINUTE_OFFSET + 59) % 60
		self.assertEqual(offset, f"12:{expectedMinOffset:02d}")

		# Test the case where the start time is 23:59 to ensure the day and hour offset is calculated correctly
		NVDAState.getStartTime = MagicMock(return_value=todayAtMidnight.replace(hour=23, minute=59).timestamp())
		ScheduleThread.scheduledDailyJobCount = 0
		offset = ScheduleThread._calculateDailyTimeOffset()
		expectedMinOffset = (ScheduleThread.DAILY_JOB_MINUTE_OFFSET + 59) % 60
		self.assertEqual(offset, f"00:{expectedMinOffset:02d}")
