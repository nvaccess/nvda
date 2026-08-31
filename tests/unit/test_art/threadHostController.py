# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Thread-backed ``HostController`` for testing."""

import contextlib
import threading

from _art.host import entrypoint
from rpyc.core.stream import PipeStream, Stream


class ThreadHostController:
	"""Runs the host entry point in a thread of this process.

	The default test substrate: no process to schedule, no cold start to wait for, and failures
	surface as ordinary exceptions.

	Some things have no in-process analogue:
	a thread cannot close a pipe by dying, be timed for cold start, or demonstrate handle inheritance.
	Tests that rely on such behaviour should use :class:`_art.session.hostController.SubprocessHostController` instead.
	"""

	def __init__(self) -> None:
		self._thread: threading.Thread | None = None
		self._hostStream: Stream | None = None
		self._exitStatus: int | None = None

	def start(self) -> Stream:
		"""Start the host thread and return core's end of the control connection."""
		if self._thread is not None:
			msg = "Host has already been started"
			raise RuntimeError(msg)
		coreStream, hostStream = PipeStream.create_pair()
		self._hostStream = hostStream
		self._thread = threading.Thread(
			target=self._run,
			args=(hostStream,),
			name="ART host (thread-backed)",
			# A wedged host must not be able to keep the interpreter alive.
			daemon=True,
		)
		self._thread.start()
		return coreStream

	def _run(self, hostStream: Stream) -> None:
		try:
			entrypoint.run(hostStream)
		except Exception:  # noqa: BLE001
			self._exitStatus = 1
		else:
			self._exitStatus = 0

	def poll(self) -> int | None:
		"""Check whether the host thread has finished, without blocking."""
		if self._thread is None:
			raise RuntimeError("Cannot poll a host that has not been started")
		if self._thread.is_alive():
			return None
		# The thread may have been recorded as finished before _run assigned a status.
		return self._exitStatus if self._exitStatus is not None else 0

	def wait(self, timeout: float | None = None) -> int | None:
		"""Wait for the host thread to finish."""
		if self._thread is None:
			raise RuntimeError("Cannot wait on a host that has not been started")
		self._thread.join(timeout)
		return self.poll()

	def terminate(self) -> None:
		"""Stop the host by closing its end of the control connection.

		The host's event loop sees the connection close and returns, which is the same thing that
		happens to a real host when core goes away.
		"""
		if self._hostStream is None:
			return
		with contextlib.suppress(Exception):
			self._hostStream.close()

	def createPipePair(self) -> tuple[Stream, Stream]:
		"""Manufacture a pipe pair for a dependent connection.

		Both ends are streams: the host shares this process, so there are no handles to duplicate.
		"""
		coreStream, hostStream = PipeStream.create_pair()
		return coreStream, hostStream
