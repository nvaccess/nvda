# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
The seam at which ART's dependency on a real process is injected.

A :class:`HostController` starts a host, manufactures its wire ends, reports on its liveness, and
tears it down.
It controls the host process, not the add-on running inside it.

Two implementations are provided, and a session is given one at construction time:

* :class:`ThreadHostController` runs the host entry point in a thread of this process.
	Deterministic and fast, so it is the default substrate for tests.
* :class:`SubprocessHostController` runs the host entry point in a real child process.
	Used at runtime, and for the tests that need behaviour a thread cannot imitate.

Some things genuinely have no in-process analogue: a thread cannot close a pipe by dying, cannot
be timed for cold start, and cannot demonstrate handle inheritance.
That is the whole reason the real implementation exists this early, rather than the seam being
designed against a fake alone.
"""

from __future__ import annotations

from rpyc.core.stream import Stream
import io
import msvcrt
import subprocess
import sys
import threading
from ctypes import WinError, byref
from ctypes.wintypes import HANDLE
from typing import Final, Protocol, runtime_checkable

import win32con
import win32pipe
from rpyc.core.stream import PipeStream

import globalVars
import NVDAState
from logHandler import log
from winBindings.kernel32 import DuplicateHandle, GetCurrentProcess


#: The module run to boot a host process.
_HOST_ENTRYPOINT_MODULE: Final[str] = "_art.host.entrypoint"

#: How long :meth:`SubprocessHostController.terminate` waits for a polite exit before killing.
_TERMINATE_GRACE_SECONDS: Final[float] = 5.0

#: Buffer size for pipes backing dependent connections, matching rpyc's own default.
_PIPE_BUFFER_SIZE: Final[int] = 130000

#: ``DUPLICATE_SAME_ACCESS``, which makes ``DuplicateHandle`` ignore the requested access mask.
_DUPLICATE_SAME_ACCESS: Final[int] = 0x00000002


@runtime_checkable
class HostController[HostPipeEnd](Protocol):
	"""Starts a host, watches it, and stops it."""

	def start(self) -> Stream:
		"""Start the host and return core's end of the control connection.

		:returns: Core's end of the control connection, ready to be wrapped in a
			:class:`~_art.transport.Connection`.
		"""
		...

	def poll(self) -> int | None:
		"""Check whether the host has finished, without blocking.

		:returns: The exit status, or ``None`` if the host is still running.
		"""
		...

	def wait(self, timeout: float | None = None) -> int | None:
		"""Wait for the host to finish.

		:param timeout: Seconds to wait, or ``None`` to wait indefinitely.
		:returns: The exit status, or ``None`` if the host was still running when ``timeout`` elapsed.
		"""
		...

	def terminate(self) -> None:
		"""Stop the host.

		Safe to call on a host that has already finished.
		"""
		...

	def createPipePair(self) -> tuple[Stream, HostPipeEnd]:
		"""Manufacture a pipe pair for a dependent connection.

		:returns: Core's end as a stream, and the host's end in whatever form this host consumes.
		:raises RuntimeError: If the host is not running.
		"""
		...


class SubprocessHostController:
	"""Runs the host entry point in a real child process.

	The control connection is carried on the child's standard input and output, and its standard
	error is drained into NVDA's log.

	Not yet sandboxed: swapping :class:`subprocess.Popen` for ``secureProcess.SecurePopen``, and
	choosing a host executable by architecture, belong to later stages.
	Until then this runs the host on the interpreter path, which requires NVDA to be running from
	source.
	"""

	def __init__(self) -> None:
		self._process: subprocess.Popen | None = None
		self._stderrThread: threading.Thread | None = None

	def start(self) -> Stream:
		"""Launch the host process and return core's end of the control connection.

		:raises RuntimeError: If NVDA is not running from source, since there is no host executable to fall back on yet.
		"""
		if self._process is not None:
			raise RuntimeError("Host has already been started")
		if not NVDAState.isRunningAsSource():
			raise RuntimeError(
				"The ART host can only be launched on the interpreter path; "
				"host executables are not built yet",
			)
		log.debug(f"Launching ART host: {sys.executable} -m {_HOST_ENTRYPOINT_MODULE}")
		self._process = subprocess.Popen(
			[sys.executable, "-m", _HOST_ENTRYPOINT_MODULE],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			# Running with the source directory as the working directory puts the _art package on
			# the host's import path, which is what makes ``-m`` resolve.
			cwd=globalVars.appDir,
			creationflags=subprocess.CREATE_NO_WINDOW,
		)
		self._startStderrDrain()
		return claimProcessControlStream(self._process)

	def _startStderrDrain(self) -> None:
		"""Forward the host's standard error into NVDA's log.

		Not optional: with standard error piped and nothing reading it, the host deadlocks as soon
		as it fills the pipe buffer.

		It is also the only way host diagnostics are visible at all.
		Leaving the host's standard error unconnected has caused real trouble in the 32-bit synth
		driver host, where an unhandled traceback goes nowhere.
		"""
		assert self._process is not None
		self._stderrThread = threading.Thread(
			target=self._drainStderr,
			args=(self._process.stderr,),
			name="ART host stderr drain",
			daemon=True,
		)
		self._stderrThread.start()

	@staticmethod
	def _drainStderr(stderr: io.BufferedReader) -> None:
		try:
			for line in iter(stderr.readline, b""):
				text = line.decode("utf-8", errors="replace").rstrip()
				if text:
					# Anything reaching here is unexpected by construction: the host logs at
					# warning and above, and its standard output is folded in here precisely
					# because writing to it is a bug. Revisit if the host is ever given a
					# configurable log level.
					log.warning(f"ART host: {text}")
		except Exception:
			log.debugWarning("Error draining ART host stderr", exc_info=True)
		finally:
			# Reaching here means end-of-file, so the host is gone and this is the last reference.
			try:
				stderr.close()
			except Exception:
				pass

	def poll(self) -> int | None:
		"""Check whether the host process has exited, without blocking."""
		if self._process is None:
			return None
		return self._process.poll()

	def wait(self, timeout: float | None = None) -> int | None:
		"""Wait for the host process to exit."""
		if self._process is None:
			return None
		try:
			return self._process.wait(timeout)
		except subprocess.TimeoutExpired:
			return None

	def terminate(self) -> None:
		"""Stop the host process, killing it if it does not go quietly."""
		if self._process is None or self._process.poll() is not None:
			return
		log.debug("Terminating ART host process")
		self._process.terminate()
		if self.wait(_TERMINATE_GRACE_SECONDS) is None:
			log.debugWarning("ART host did not exit after terminate; killing it")
			self._process.kill()
			self._process.wait()

	def createPipePair(self) -> tuple[Stream, tuple[int, int]]:
		"""Manufacture a pipe pair for a dependent connection.

		Core keeps a stream over its own ends; the host's ends are duplicated into the host
		process, and their values handed over for it to rebuild a stream from.

		:raises RuntimeError: If the host process is not running.
		"""
		if self._process is None:
			raise RuntimeError("Cannot create a pipe pair before the host has started")
		targetProcess = self._process._handle
		# One pipe per direction, since an anonymous pipe is one-way.
		hostReadEnd, coreWriteEnd = win32pipe.CreatePipe(None, _PIPE_BUFFER_SIZE)
		coreReadEnd, hostWriteEnd = win32pipe.CreatePipe(None, _PIPE_BUFFER_SIZE)
		try:
			hostRead = _duplicateHandleIntoProcess(hostReadEnd, win32con.GENERIC_READ, targetProcess)
			hostWrite = _duplicateHandleIntoProcess(hostWriteEnd, win32con.GENERIC_WRITE, targetProcess)
		finally:
			# The host has its own copies now; ours would otherwise hold the pipes open, so the
			# host would never see end-of-file when core goes away.
			hostReadEnd.Close()
			hostWriteEnd.Close()
		# Detached, so the stream is the sole owner of core's ends.
		# Closing a stream closes the underlying handle without marking the ``PyHANDLE`` wrapper
		# closed, so leaving these wrapped would close each handle a second time on garbage
		# collection, by which point Windows may have reissued the value to someone else.
		return (
			PipeStream(coreReadEnd.Detach(), coreWriteEnd.Detach()),
			(hostRead.value, hostWrite.value),
		)


def claimProcessControlStream(process: subprocess.Popen) -> Stream:
	"""Take sole ownership of a child's standard input and output as a control stream.

	The obvious ``PipeStream(process.stdout, process.stdin)`` sets up a double free: the stream
	closes the underlying handles, while the file objects still believe they own the descriptors
	and close them again when collected.
	The second close lands on whatever Windows has since reissued the value to, so the damage
	surfaces as an unrelated pipe failing later, arbitrarily far from the cause.

	Duplicating the handles for the stream and closing the file objects immediately leaves exactly
	one owner of each.

	:param process: The child process whose standard streams carry the control connection.
	:returns: A stream over the child's standard input and output.
	"""
	stdout = process.stdout
	stdin = process.stdin
	if stdout is None or stdin is None:
		raise RuntimeError("The host process was not created with its standard streams piped")
	readHandle = _duplicateHandleForSelf(msvcrt.get_osfhandle(stdout.fileno()))
	writeHandle = _duplicateHandleForSelf(msvcrt.get_osfhandle(stdin.fileno()))
	stdout.close()
	stdin.close()
	return PipeStream(readHandle, writeHandle)


def _duplicateHandleForSelf(handle: int) -> int:
	"""Duplicate a handle within this process, with the same access as the original.

	Used to take ownership of a handle away from a Python file object, so that a stream can be the
	only thing that closes it.

	:param handle: Handle to duplicate.
	:returns: The value of an independent handle to the same object.
	:raises RuntimeError: If duplication fails.
	"""
	duplicate = HANDLE()
	currentProcess = GetCurrentProcess()
	if not DuplicateHandle(
		currentProcess,
		HANDLE(int(handle)),
		currentProcess,
		byref(duplicate),
		0,
		False,
		_DUPLICATE_SAME_ACCESS,
	):
		raise RuntimeError(f"Failed to duplicate handle, {WinError()}")
	return duplicate.value


def _duplicateHandleIntoProcess(handle: int, accessMask: int, targetProcess: int) -> HANDLE:
	"""Duplicate a handle so it is valid in another process.

	The target process is a parameter rather than state on the caller, so that wire ends stay
	manufacturable without a controller having to own the process it duplicates into.

	:param handle: Handle to duplicate.
	:param accessMask: Desired access for the duplicate.
	:param targetProcess: Handle of the process to duplicate into.
	:returns: A handle valid in ``targetProcess``.
	:raises RuntimeError: If duplication fails.
	"""
	duplicate = HANDLE()
	if not DuplicateHandle(
		GetCurrentProcess(),
		HANDLE(int(handle)),
		targetProcess,
		byref(duplicate),
		accessMask,
		False,
		0,
	):
		raise RuntimeError(f"Failed to duplicate handle into host process, {WinError()}")
	return duplicate
