# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from datetime import datetime
from enum import Enum, auto
import threading
import time
from typing import Callable

import schedule

from logHandler import log
import NVDAState

scheduleThread: "ScheduleThread | None" = None


class ThreadTarget(Enum):
	"""
	When running a task, specify the thread to run the task on.
	ScheduleThread blocks until the scheduled task is complete.
	To avoid blocking the ScheduleThread, all tasks should be run on a separate thread.
	Using GUI or DAEMON thread targets ensures that the ScheduleThread is not blocked.
	CUSTOM thread target is used for tasks where the supplier of the task is responsible
	for running the task on a separate thread.
	"""

	GUI = auto()
	"""
	Uses wx.CallAfter to run the job on the GUI thread.
	This is encouraged for tasks that interact with the GUI, such as dialogs.
	"""

	DAEMON = auto()
	"""
	Uses threading.Thread(daemon=True) to run the job in the background.
	"""

	CUSTOM = auto()
	"""
	No thread target.
	Runs directly and blocks `scheduleThread`.
	Authors of tasks are responsible for running the task on a
	separate thread to ensure that `scheduleThread` is not blocked.
	"""


class JobClashError(Exception):
	"""Raised when a job time clashes with an existing job."""

	pass


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

	DAILY_JOB_MINUTE_OFFSET = 3
	"""
	Offset in minutes to schedule daily jobs.
	Daily scheduled jobs occur offset by X minutes to avoid overlapping jobs.
	"""

	def __init__(self, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)
		self.scheduledDailyJobCount = 0

	@classmethod
	def run(cls):
		while not cls.KILL.is_set():
			schedule.run_pending()
			time.sleep(cls.SLEEP_INTERVAL_SECS)

	def _calculateDailyTimeOffset(self) -> str:
		startTime = datetime.fromtimestamp(NVDAState.getStartTime())
		# Schedule jobs so that they occur offset by a regular period to avoid overlapping jobs.
		# Start with a delay to give time for NVDA to start up.
		startTimeMinuteOffset = (
			startTime.minute + (self.scheduledDailyJobCount + 1) * self.DAILY_JOB_MINUTE_OFFSET
		)
		# Handle the case where the minute offset is greater than 60.
		startTimeHourOffset = startTime.hour + (startTimeMinuteOffset // 60)
		startTimeMinuteOffset = startTimeMinuteOffset % 60
		# Handle the case where the hour offset is greater than 24.
		startTimeHourOffset = startTimeHourOffset % 24
		return f"{startTimeHourOffset:02d}:{startTimeMinuteOffset:02d}"

	def scheduleDailyJobAtStartUp(
		self,
		task: Callable,
		queueToThread: ThreadTarget,
		*args,
		**kwargs,
	) -> schedule.Job:
		"""
		Schedule a daily job to run at startup.
		Designed to handle clashes in a smart way to offset jobs.
		:param task: The task to run.
		:param queueToThread: The thread to run the task on.
		:param args: Arguments to pass to the task.
		:param kwargs: Keyword arguments to pass to the task.
		:return: The scheduled job.
		"""
		try:
			job = self.scheduleDailyJob(
				task,
				self._calculateDailyTimeOffset(),
				queueToThread,
				*args,
				**kwargs,
			)
		except JobClashError as e:
			log.warning(f"Failed to schedule daily job due to clash: {e}")
			self.scheduledDailyJobCount += 1
			log.debugWarning(f"Attempting to reschedule daily job {self.DAILY_JOB_MINUTE_OFFSET} min later")
			return self.scheduleDailyJobAtStartUp(task, queueToThread, *args, **kwargs)
		else:
			self.scheduledDailyJobCount += 1
			return job

	def scheduleDailyJob(
		self,
		task: Callable,
		cronTime: str,
		queueToThread: ThreadTarget,
		*args,
		**kwargs,
	) -> schedule.Job:
		"""
		Schedule a daily job to run at specific times.
		:param task: The task to run.
		:param cronTime: The time to run the job using a valid cron string.
		It is recommended to use minute level precision at most.
		https://schedule.readthedocs.io/en/stable/examples.html#run-a-job-every-x-minute
		:param queueToThread: The thread to run the task on.
		:param args: Arguments to pass to the task.
		:param kwargs: Keyword arguments to pass to the task.
		:return: The scheduled job.
		:raises JobClashError: If the job's next run clashes with an existing job's next run.
		"""
		scheduledJob = schedule.every().day.at(cronTime)
		return self.scheduleJob(task, scheduledJob, queueToThread, *args, **kwargs)

	def scheduleJob(
		self,
		task: Callable,
		jobSchedule: schedule.Job,
		queueToThread: ThreadTarget,
		*args,
		**kwargs,
	) -> schedule.Job:
		"""
		Schedule a job to run at specific times.
		:param task: The task to run.
		:param jobSchedule: The schedule to run the task on.
		Constructed using schedule e.g. `schedule.every().day.at("**:15")`.
		:param cronTime: The time to run the job at using a valid cron string.
		https://schedule.readthedocs.io/en/stable/examples.html#run-a-job-every-x-minute
		:param queueToThread: The thread to run the task on.
		:param args: Arguments to pass to the task.
		:param kwargs: Keyword arguments to pass to the task.
		:return: The scheduled job.
		:raises JobClashError: If the job's next run clashes with an existing job's next run.
		"""
		match queueToThread:
			case ThreadTarget.GUI:

				def callJobOnThread(*args, **kwargs):
					import wx

					log.debug(f"Starting thread for job: {task.__name__} on GUI thread")
					wx.CallAfter(task, *args, **kwargs)
			case ThreadTarget.DAEMON:

				def callJobOnThread(*args, **kwargs):
					t = threading.Thread(
						target=task,
						args=args,
						kwargs=kwargs,
						daemon=True,
						name=f"{task.__name__}",
					)
					log.debug(f"Starting thread for job: {task.__name__} on thread {t.ident}")
					t.start()
			case ThreadTarget.CUSTOM:

				def callJobOnThread(*args, **kwargs):
					log.debug(f"Starting thread for job: {task.__name__} on custom thread")
					task(*args, **kwargs)
			case _:
				raise ValueError(f"Invalid queueToThread value: {queueToThread}")

		# Check if scheduled job time clashes with existing jobs.
		for existingJob in schedule.jobs:
			if (jobSchedule.at_time is not None and existingJob.at_time == jobSchedule.at_time) or (
				jobSchedule.next_run is not None and existingJob.next_run == jobSchedule.next_run
			):
				# raise warning that job time clashes with existing job
				raise JobClashError(
					f"Job time {jobSchedule.at_time} clashes with existing job: "
					f"{existingJob.job_func} and {task.__name__}",
				)
		return jobSchedule.do(callJobOnThread, *args, **kwargs)


def initialize():
	global scheduleThread
	scheduleThread = ScheduleThread(daemon=True)
	scheduleThread.start()


def terminate():
	global scheduleThread
	if scheduleThread is not None:
		schedule.clear()
		scheduleThread.KILL.set()
		scheduleThread.join()
		scheduleThread = None
