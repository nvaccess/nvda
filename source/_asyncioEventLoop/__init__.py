# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Provide an asyncio event loop running on a background thread for use by NVDA components.
"""

import asyncio
from threading import Thread

from logHandler import log

from .utils import runCoroutineSync

from . import _state

TERMINATE_TIMEOUT_SECONDS = _state.TERMINATE_TIMEOUT_SECONDS


def initialize():
	"""Initialize and start the asyncio event loop."""
	log.info("Initializing asyncio event loop")
	_state.eventLoop = asyncio.new_event_loop()
	asyncio.set_event_loop(_state.eventLoop)
	_state.asyncioThread = Thread(target=_state.eventLoop.run_forever, daemon=True)
	_state.asyncioThread.start()


def terminate():
	"""Terminate the asyncio event loop and cancel all running tasks."""
	log.info("Terminating asyncio event loop")

	async def cancelAllTasks():
		tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
		log.debug(f"Stopping {len(tasks)} tasks")
		[task.cancel() for task in tasks]
		await asyncio.gather(*tasks, return_exceptions=True)
		log.debug("Done stopping tasks")

	try:
		runCoroutineSync(cancelAllTasks(), TERMINATE_TIMEOUT_SECONDS)
	except TimeoutError:
		log.debugWarning("Timeout while stopping async tasks")
	finally:
		_state.eventLoop.call_soon_threadsafe(_state.eventLoop.stop)

	_state.asyncioThread.join()
	_state.asyncioThread = None
	_state.eventLoop.close()
