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

	scheduledJobs: list[Callable[[], None]] = []

	@classmethod
	def run(cls):
		while not cls.KILL.is_set():
			schedule.run_pending()
			time.sleep(cls.SLEEP_INTERVAL_SECS)

	@classmethod
	def scheduleDailyJobAtStartUp(cls, job: Callable, *args, **kwargs):
		"""Schedule a daily job to run at startup."""
		startTime = datetime.fromtimestamp(NVDAState.getStartTime())
		# We add the length of the scheduled jobs to the minute offset to avoid overlapping jobs.
		startTimeMinuteOffset = startTime.minute + len(cls.scheduledJobs) + 1
		scheduledJob = schedule.every().day.at(f"{startTime.hour}:{startTimeMinuteOffset}").do(job, *args, **kwargs)
		cls.scheduledJobs.append(scheduledJob)


def initialize():
	global scheduleThread
	scheduleThread = ScheduleThread()
	scheduleThread.start()


def terminate():
	global scheduleThread
	if scheduleThread is not None:
		schedule.clear()
		scheduleThread.KILL.set()
		scheduleThread.join()
		scheduleThread = None
