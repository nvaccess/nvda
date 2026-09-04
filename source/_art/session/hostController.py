# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
The seam at which ART's dependency on a real process is injected.

A :class:`HostController` starts a host, manufactures its wire ends, reports on its liveness, and
tears it down.
It controls the host process, not the add-on running inside it.

The abstraction is provided primarily to facilitate testing.

A thread-backed version for testing is provided at ``tests/unit/test_art/threadHostController.py``.
"""

from __future__ import annotations

import msvcrt
import subprocess
from typing import Protocol

from rpyc.core.stream import PipeStream, Stream

from ..winHandles import duplicateHandleForSelf


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
