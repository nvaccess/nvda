# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited.
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt


import threading
import itertools
import time
import heapq
from logHandler import log


class _WorkItem:
	def __init__(self, time: float, ID: int, callable, args, kwargs):
		self.time = time
		self.ID = ID
		self.callable = callable
		self.args = args
		self.kwargs = kwargs

	def __lt__(self, other):
		if self.time != other.time:
			return self.time < other.time
		return self.ID < other.ID


class Core:
	_workIDFactory: itertools.count
	_workItems: list[_WorkItem]
	_workItemsLock: threading.Lock
	_wake: threading.Event
	_stopped: bool = False

	def __init__(self):
		self._workIDFactory = itertools.count()
		self._workItems = []
		self._workItemsLock = threading.Lock()
		self._wake = threading.Event()

	def stop(self):
		self._stopped = True
		self._wake.set()

	def schedule(self, delay: float, callable, *args, **kwargs):
		runAt = time.time() + delay
		workID = next(self._workIDFactory)
		workItem = _WorkItem(runAt, workID, callable, args, kwargs)
		log.debug(f"Scheduling work item {workItem} to run at {runAt}")
		with self._workItemsLock:
			heapq.heappush(self._workItems, workItem)
		self._wake.set()

	def run(self):
		log.debug("Entering Core run loop")
		while not self._stopped:
			log.debug("Core woke up, checking for work items")
			now = time.time()
			nextWorkItem: _WorkItem | None = None
			with self._workItemsLock:
				if self._workItems and self._workItems[0].time <= now:
					nextWorkItem = heapq.heappop(self._workItems)
			if nextWorkItem:
				log.debug(f"Running work item {nextWorkItem}")
				try:
					nextWorkItem.callable(*nextWorkItem.args, **nextWorkItem.kwargs)
				except Exception:
					log.error(f"Error running scheduled work item {nextWorkItem}", exc_info=True)
				continue
			# No work item ready to run; wait until the next one is due or a new one is scheduled.
			waitTime: float | None = None
			with self._workItemsLock:
				if self._workItems:
					nextRunAt = self._workItems[0].time
					waitTime = max(0, nextRunAt - time.time())
			log.debug(f"No work item ready; sleeping for up to {waitTime} seconds")
			self._wake.wait(timeout=waitTime)
			self._wake.clear()
		log.debug("Core stopped")


_core: Core | None = None


def callLater(delay, callable, *args, **kwargs):
	if _core is None:
		raise RuntimeError("Core not initialized")
	log.debug(f"Scheduling callLater: {callable} to run in {delay} seconds")
	_core.schedule(delay / 1000, callable, *args, **kwargs)


def requestStop():
	if _core is None:
		raise RuntimeError("Core not initialized")
	log.debug("Requesting Core stop")
	_core.stop()


def _runSynthDriverHost():
	log.debug("Starting synthDriverHost runtime thread")
	try:
		import comtypes

		comtypes.CoInitialize()
		import synthDriverHost

		synthDriverHost.main()
	except Exception:
		log.exception("Unhandled exception in synthDriverHost runtime thread")
	finally:
		requestStop()
	log.debug("synthDriverHost runtime thread exiting")


def main():
	global _core
	log.debug("Initializing core")
	_core = Core()
	threading.Thread(target=_runSynthDriverHost, daemon=True).start()
	_core.run()
