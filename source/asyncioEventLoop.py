# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Provide an asyncio event loop
"""

import asyncio
from collections.abc import Coroutine
from threading import Thread

from logHandler import log

TERMINATE_TIMEOUT_SECONDS = 5
"Time to wait for tasks to finish while terminating the event loop."

eventLoop: asyncio.BaseEventLoop
"The asyncio event loop used by NVDA."
asyncioThread: Thread
"Thread running the asyncio event loop."


def initialize():
	"""Initialize and start the asyncio event loop."""
	global eventLoop, asyncioThread
	log.info("Initializing asyncio event loop")
	eventLoop = asyncio.new_event_loop()
	asyncio.set_event_loop(eventLoop)
	asyncioThread = Thread(target=eventLoop.run_forever, daemon=True)
	asyncioThread.start()


def terminate():
	global eventLoop, asyncioThread
	log.info("Terminating asyncio event loop")

	async def cancelAllTasks():
		tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
		[task.cancel() for task in tasks]
		await asyncio.gather(*tasks, return_exceptions=True)
		eventLoop.stop()

	f = asyncio.run_coroutine_threadsafe(cancelAllTasks(), eventLoop)
	try:
		f.result(TERMINATE_TIMEOUT_SECONDS)
	except asyncio.TimeoutError:
		pass

	eventLoop.close()
	asyncioThread.stop()
	asyncioThread = None


def runCoroutine(coro: Coroutine) -> asyncio.Future:
	"""Schedule a coroutine to be run on the asyncio event loop.

	:param coro: The coroutine to run.
	"""
	if not asyncioThread.is_alive():
		raise RuntimeError("Asyncio event loop thread is not running")
	return asyncio.run_coroutine_threadsafe(coro, eventLoop)
