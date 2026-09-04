# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
The seam at which ART's dependency on a real process is injected.

A :class:`HostController` starts a host, manufactures its wire ends, reports on its liveness, and
tears it down.
It controls the host process, not the add-on running inside it.

The abstraction is provided primarily to facilitate testing;
a live copy of NVDA should use :class:`SubprocessHostController`.

A thread-backed version for testing is provided at ``tests/unit/test_art/threadHostController.py``.
"""

from __future__ import annotations

import contextlib
import io
import msvcrt
import subprocess
import sys
import threading
from ctypes import WinError, byref
from ctypes.wintypes import HANDLE
from typing import Final, Protocol

import globalVars
import NVDAState
import winKernel
from logHandler import log
from rpyc.core.stream import PipeStream, Stream
from winBindings.kernel32 import CloseHandle, CreatePipe, OpenProcess

from ..winHandles import duplicateHandleForSelf, duplicateHandleIntoProcess

#: The module run to boot a host process.
_HOST_ENTRYPOINT_MODULE: Final[str] = "_art.host.entrypoint"

#: Buffer size for pipes backing dependent connections, matching rpyc's own default.
_PIPE_BUFFER_SIZE: Final[int] = 130000


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
		:raises RuntimeError: If the host has not been started.
		"""
		...

	def wait(self, timeout: float | None = None) -> int | None:
		"""Wait for the host to finish.

		:param timeout: Seconds to wait, or ``None`` to wait indefinitely.
		:returns: The exit status, or ``None`` if the host was still running when ``timeout`` elapsed.
		:raises RuntimeError: If the host has not been started.
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

	The control connection is carried on the child's standard input and output,
	and its standard error is drained into NVDA's log.

	Selecting a pre-built host executable and sandboxing the host are future steps.
	For now, this runs the host via the interpreter,
	which requires NVDA to be running from source.
	"""

	def __init__(self) -> None:
		"""Initializer."""
		self._process: subprocess.Popen | None = None
		self._stderrThread: threading.Thread | None = None

	def start(self) -> Stream:
		"""Launch the host process and return core's end of the control connection.

		:raises RuntimeError: If NVDA is not running from source, since there is no host executable to use yet.
		"""
		if self._process is not None:
			raise RuntimeError("Host has already been started")
		if not NVDAState.isRunningAsSource():
			raise RuntimeError("The ART host can only be launched on the interpreter path")
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

		With standard error piped to a buffered pipe,
		the host will deadlock as soon as it fills the pipe buffer.

		Also currently the only way host diagnostics are visible at all.
		Without this, unhandled exceptions simply disappear.
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
			for line in stderr:
				text = line.decode("utf-8", errors="replace").rstrip()
				if text:
					log.warning(f"ART host: {text}")
		except Exception:
			log.exception("Error draining ART host stderr")
		finally:
			# We must close our end of the pipe, as an open but undrained pipe will hang the host if it fills the buffer.
			# After this, the host attempting to write to the pipe will fail, but not block.
			with contextlib.suppress(Exception):
				stderr.close()

	def poll(self) -> int | None:
		"""Check whether the host process has exited, without blocking.

		:returns: The exit code of the process, or ``None`` if it is still alive.
		:raises RuntimeError: If the host has not been started.
		"""
		if self._process is None:
			raise RuntimeError("Cannot poll a host that has not been started")
		return self._process.poll()

	def wait(self, timeout: float | None = None) -> int | None:
		"""Wait for the host process to exit.

		:param timeout: How long to wait, in seconds.
		:returns: The exit code of the process, or ``None`` if it was still alive after ``timeout`` had elapsed.
		:raises RuntimeError: If the host has not been started.
		"""
		if self._process is None:
			raise RuntimeError("Cannot wait on a host that has not been started")
		try:
			return self._process.wait(timeout)
		except subprocess.TimeoutExpired:
			return None

	def terminate(self) -> None:
		"""Stop the host process.

		.. note::
			This currently hard-kills the host immediately.
			It can only become a cooperative shutdown once the host has a protocol for one.
		"""
		if self._process is None or self._process.poll() is not None:
			return
		log.debug("Terminating ART host process")
		self._process.terminate()
		self._process.wait()

	def createPipePair(self) -> tuple[Stream, tuple[int, int]]:
		"""Manufacture a pipe pair for a dependent connection.

		Core keeps a stream over its own ends; the host's ends are duplicated into the host
		process, and their values handed over for it to rebuild a stream from.

		:returns: A 2-tuple:
			The first member is core's end of the connection;
			The second member is a (read, write) tuple of file handles valid in the host process.
		:raises RuntimeError: If the host process is not running.
		:raises OSError: If pipe creation or handle duplication fails.
		"""
		if self._process is None:
			raise RuntimeError("Cannot create a pipe pair before the host has started")
		targetProcess = OpenProcess(winKernel.PROCESS_DUP_HANDLE, False, self._process.pid)
		if not targetProcess:
			raise WinError()
		try:
			# One pipe per direction, since an anonymous pipe is one-way.
			hostReadLocal, coreWrite, coreRead, hostWriteLocal = HANDLE(), HANDLE(), HANDLE(), HANDLE()
			openHandles: list[HANDLE] = []
			try:
				if not CreatePipe(byref(hostReadLocal), byref(coreWrite), None, _PIPE_BUFFER_SIZE):
					raise WinError()
				openHandles += hostReadLocal, coreWrite
				if not CreatePipe(byref(coreRead), byref(hostWriteLocal), None, _PIPE_BUFFER_SIZE):
					raise WinError()
				openHandles += coreRead, hostWriteLocal
				# The host's read and write handles are not valid in this process,
				# so we can't close them on failure.
				# If the second duplication fails after the first succeeded,
				# the handle already placed in the host is orphaned there.
				# Failure to duplicate `hostWriteLocal` into the host process most likely means that the host process died,
				# in which case `hostRead` will have been freed by the kernel.
				hostRead = duplicateHandleIntoProcess(hostReadLocal, winKernel.GENERIC_READ, targetProcess)
				hostWrite = duplicateHandleIntoProcess(hostWriteLocal, winKernel.GENERIC_WRITE, targetProcess)
			except Exception:
				for handle in openHandles:
					CloseHandle(handle)
				raise
			# The host has its own copies now; ours would otherwise hold the pipes open,
			# so the host would never see end-of-file when core goes away.
			CloseHandle(hostReadLocal)
			CloseHandle(hostWriteLocal)
			return (
				# PipeStream takes ownership of the handles it's constructed with,
				# so closing them when done is its responsibility.
				PipeStream(coreRead.value, coreWrite.value),
				(hostRead.value, hostWrite.value),
			)
		finally:
			CloseHandle(targetProcess)


def claimProcessControlStream(process: subprocess.Popen) -> Stream:
	"""Take sole ownership of a child's standard input and output as a control stream.

	Using ``PipeStream(process.stdout, process.stdin)`` sets up a double free:
	When closed, the file objects and the ``PipeStream`` both close the underlying handles, but neither is aware of the other's actions.
	Since handles are reused, this may result in an entirely unrelated handle being closed.
	Duplicating the handles for the stream and closing the file objects immediately leaves one owner of each.

	:param process: The child process whose standard streams carry the control connection.
	:returns: A stream over the child's standard input and output.
	:raises RuntimeError: If ``process`` was created without one or both of stdin or stdout piped.
	:raises OSError: If pipe handle duplication fails.
	"""
	stdout = process.stdout
	stdin = process.stdin
	if stdout is None or stdin is None:
		raise RuntimeError("The host process was not created with its standard streams piped")
	readHandle = duplicateHandleForSelf(msvcrt.get_osfhandle(stdout.fileno()))
	writeHandle = duplicateHandleForSelf(msvcrt.get_osfhandle(stdin.fileno()))
	stdout.close()
	stdin.close()
	return PipeStream(readHandle, writeHandle)
