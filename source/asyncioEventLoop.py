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
		log.debug(f"Stopping {len(tasks)} tasks")
		[task.cancel() for task in tasks]
		await asyncio.gather(*tasks, return_exceptions=True)
		log.debug("Done stopping tasks")

	try:
		runCoroutineSync(cancelAllTasks(), TERMINATE_TIMEOUT_SECONDS)
	except TimeoutError:
		log.debugWarning("Timeout while stopping async tasks")
	finally:
		eventLoop.call_soon_threadsafe(eventLoop.stop)

	asyncioThread.join()
	asyncioThread = None
	eventLoop.close()


def runCoroutine(coro: Coroutine) -> asyncio.Future:
	"""Schedule a coroutine to be run on the asyncio event loop.

	:param coro: The coroutine to run.
	"""
	if asyncioThread is None or not asyncioThread.is_alive():
		raise RuntimeError("Asyncio event loop thread is not running")
	return asyncio.run_coroutine_threadsafe(coro, eventLoop)


def runCoroutineSync(coro: Coroutine, timeout: float | None = None):
	"""Schedule a coroutine to be run on the asyncio event loop and wait for the result.

	This is a synchronous wrapper around runCoroutine() that blocks until the coroutine
	completes and returns the result directly, or raises any exception that occurred.

	:param coro: The coroutine to run.
	:param timeout: Optional timeout in seconds. If None, waits indefinitely.
	:return: The result of the coroutine.
	:raises: Any exception raised by the coroutine.
	:raises TimeoutError: If the timeout is exceeded.
	:raises RuntimeError: If the asyncio event loop thread is not running.
	"""
	future = runCoroutine(coro)
	try:
		# Wait for the future to complete and get the result
		# This will raise any exception that occurred in the coroutine
		return future.result(timeout)
	except asyncio.TimeoutError as e:
		# Cancel the coroutine since it timed out
		future.cancel()
		raise TimeoutError(f"Coroutine execution timed out after {timeout} seconds") from e
