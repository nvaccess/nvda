# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from datetime import datetime
import threading
import time
from typing import Callable

import schedule

import NVDAState

scheduleThread: "ScheduleThread | None" = None


class ScheduleThread(threading.Thread):
	name = "ScheduleThread"

	KILL = threading.Event()
	"""Event which can be set to cease continuous run."""

	SLEEP_INTERVAL_SECS = 0.5
	"""
	Note that the behaviour of ScheduleThread is to not run missed jobs.
	For example, if you've registered a job that should run every minute and
	you set a continuous run interval of one hour then your job won't be run 60 times
	at each interval but only once.
	"""

	DAILY_JOB_MINUTE_OFFSET = 1
	"""
	Offset in minutes to schedule daily jobs.
	Daily scheduled jobs occur offset by X minutes to avoid overlapping jobs.
	"""

	scheduledJobs: list[schedule.Job] = []

	@classmethod
	def run(cls):
		while not cls.KILL.is_set():
			schedule.run_pending()
			time.sleep(cls.SLEEP_INTERVAL_SECS)

	@classmethod
	def scheduleDailyJobAtStartUp(cls, job: Callable, *args, **kwargs):
		"""Schedule a daily job to run at startup."""
		startTime = datetime.fromtimestamp(NVDAState.getStartTime())
		# Schedule jobs so that they occur offset by a regular period to avoid overlapping jobs.
		# Start with a delay to give time for NVDA to start up.
		startTimeMinuteOffset = startTime.minute + (len(cls.scheduledJobs) + 1) * cls.DAILY_JOB_MINUTE_OFFSET
		# Handle the case where the minute offset is greater than 60.
		startTimeHourOffset = startTime.hour + (startTimeMinuteOffset // 60)
		startTimeMinuteOffset = startTimeMinuteOffset % 60
		# Handle the case where the hour offset is greater than 24.
		startTimeHourOffset = startTimeHourOffset % 24
		scheduledTime = f"{startTimeHourOffset:02d}:{startTimeMinuteOffset:02d}"
		scheduledJob = schedule.every().day.at(scheduledTime).do(job, *args, **kwargs)
		cls.scheduledJobs.append(scheduledJob)


def initialize():
	global scheduleThread
	scheduleThread = ScheduleThread(daemon=True)
	scheduleThread.start()


def terminate():
	global scheduleThread
	if scheduleThread is not None:
		ScheduleThread.scheduledJobs.clear()
		schedule.clear()
		scheduleThread.KILL.set()
		scheduleThread.join()
		scheduleThread = None
