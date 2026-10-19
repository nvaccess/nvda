# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
A single add-on session, and its lifecycle.

An add-on session is the full live unit:
host process, loaded add-on, granted capabilities, and the control connection between them.
"""

from __future__ import annotations

import enum
import threading
from typing import TYPE_CHECKING, Final

from logHandler import log

from ..transport import Connection
from .hostController import HostController
from .rootService import CoreRootService

if TYPE_CHECKING:
	from ..host.rootService import HostRootService

#: Name of core's end of the control connection, used in logging.
CONTROL_CONNECTION_NAME: Final[str] = "ART core control"


class SessionState(enum.Enum):
	"""Where an add-on session is in its lifecycle."""

	NEW = enum.auto()
	"""Constructed, but not yet started."""
	LAUNCHING = enum.auto()
	"""The host has been started, but has not yet signalled readiness."""
	READY = enum.auto()
	"""The host signalled that it launched successfully."""
	STOPPED = enum.auto()
	"""The session was closed. Final."""
	FAILED = enum.auto()
	"""The session failed, and the host has been stopped. Final."""


class HostLaunchError(RuntimeError):
	"""The host could not be brought to readiness."""


class AddonSession:
	"""A single add-on session.

	Owns the host (through a :class:`HostController`), the control connection to it,
	and the lifecycle that takes it from launch to readiness and back down again.
	"""

	def __init__(self, controller: HostController) -> None:
		"""Initializer.

		:param controller: Starts, watches and stops the host.
			Owned by the session from here on.
		"""
		self._controller = controller
		self._stateLock = threading.Lock()
		self._state = SessionState.NEW
		self._failureReason: str | None = None
		self._conn: Connection[CoreRootService, HostRootService] | None = None
		self._readinessReported = threading.Event()
		self._readinessFailure: str | None = None

	@property
	def state(self) -> SessionState:
		"""Where this session is in its lifecycle."""
		return self._state

	@property
	def failureReason(self) -> str | None:
		"""Why the session failed, or ``None`` if it has not."""
		return self._failureReason

	@property
	def hostRoot(self) -> HostRootService:
		"""The host's root service, through which core reaches the add-on's feature components.

		:raises RuntimeError: If the session is not ready.
		"""
		if self._state is not SessionState.READY or self._conn is None:
			raise RuntimeError(f"Add-on session is not ready (state: {self._state.name})")
		return self._conn.remoteService

	def start(self) -> None:
		"""Launch the host and wait for it to signal readiness.

		Blocks until the host's readiness signal arrives.

		:raises RuntimeError: If the session has already been started.
		:raises HostLaunchError: If the host could not be started, or reported a failed launch.
			The session is ``FAILED``, and the host has been stopped.
		"""
		with self._stateLock:
			if self._state is not SessionState.NEW:
				raise RuntimeError(f"Add-on session has already been started (state: {self._state.name})")
			self._state = SessionState.LAUNCHING
		try:
			stream = self._controller.start()
		except Exception as e:
			self._fail(f"Host could not be started: {e}")
			raise HostLaunchError("Host could not be started") from e
		self._conn = Connection(
			stream,
			CoreRootService(onReady=self._onReady),
			name=CONTROL_CONNECTION_NAME,
		)
		self._conn.bgEventLoop(daemon=True)
		self._readinessReported.wait()
		if (failure := self._readinessFailure) is not None:
			self._fail(f"Host reported a failed launch: {failure}")
			raise HostLaunchError(f"Host reported a failed launch: {failure}")
		with self._stateLock:
			if self._state is SessionState.LAUNCHING:
				self._state = SessionState.READY
		log.debug("ART add-on session is ready")

	def _onReady(self, failure: str | None) -> None:
		"""Receive the outcome of the host's readiness signal.

		Runs on the control connection's serving thread, so only records the outcome.
		"""
		self._readinessFailure = failure
		self._readinessReported.set()

	def close(self) -> None:
		"""Close the session, stopping the host.

		Safe to call more than once, and on a session that failed or was never started.
		A failed session stays ``FAILED``; any other session becomes ``STOPPED``.
		"""
		with self._stateLock:
			if self._state is SessionState.STOPPED:
				return
			if self._state is not SessionState.FAILED:
				self._state = SessionState.STOPPED
		self._stopHost()

	def _fail(self, reason: str) -> None:
		"""Mark the session as failed, and stop the host.

		Only the first failure is recorded.

		:param reason: Why the session failed.
		"""
		with self._stateLock:
			if self._state in (SessionState.FAILED, SessionState.STOPPED):
				return
			self._state = SessionState.FAILED
			self._failureReason = reason
		log.warning(f"ART add-on session failed: {reason}")
		self._stopHost()

	def _stopHost(self) -> None:
		"""Close the control connection, then stop the host.

		Closing the connection first lets a healthy host see end-of-file and exit by itself.
		"""
		conn = self._conn
		self._conn = None
		if conn is not None:
			conn.close()
		self._controller.terminate()
