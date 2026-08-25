# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
The seam at which ART's dependency on a real process is injected.

A :class:`HostController` starts a host, manufactures its wire ends, reports on its liveness, and
tears it down.
It controls the host process, not the add-on running inside it.
"""

from __future__ import annotations

from typing import Protocol

from rpyc.core.stream import Stream


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
