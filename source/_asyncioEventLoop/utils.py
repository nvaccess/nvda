# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Utility functions for scheduling coroutines on the asyncio event loop.
"""

import asyncio
from collections.abc import Coroutine

from . import _state


def runCoroutine(coro: Coroutine) -> asyncio.Future:
	"""Schedule a coroutine to be run on the asyncio event loop.

	:param coro: The coroutine to run.
	"""
	if _state.asyncioThread is None or not _state.asyncioThread.is_alive():
		raise RuntimeError("Asyncio event loop thread is not running")
	return asyncio.run_coroutine_threadsafe(coro, _state.eventLoop)


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
		return future.result(timeout)
	except asyncio.TimeoutError as e:
		future.cancel()
		raise TimeoutError(f"Coroutine execution timed out after {timeout} seconds") from e
