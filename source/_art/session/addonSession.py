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
#: How long to give a host before killing it when the control connection is lost.
_EXIT_CONFIRM_GRACE: Final[int] = 1.0


class SessionState(enum.Enum):
	"""Where an add-on session is in its lifecycle."""

	NEW = enum.auto()
	"""Constructed, but not yet started."""
	LAUNCHING = enum.auto()
	"""The host has been started, but has not yet signalled readiness."""
	READY = enum.auto()
	"""The host signalled that it launched successfully."""
	STOPPING = enum.auto()
	"""Close has been called on the session, but it has not yet finished shutting down."""
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
		self._stateLock = threading.RLock()
		self._state = SessionState.NEW
		self._failureReason: str | None = None
		self._exitStatus: int | None = None
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
	def exitStatus(self) -> int | None:
		"""The host's exit status, or ``None`` if it has not yet exited."""
		return self._exitStatus

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

	def _serveControlConnection(self) -> None:
		"""Serve the control connection in the calling thread."""
		self._conn.eventLoop()
		self._onControlConnectionLost()

	def _onControlConnectionLost(self) -> None:
		"""Respond to control connection exhaustion.

		Ensures the host is dead, moves the session's state to ``STOPPED`` or ``FAILED`` as appropriate,
		ensures ``start`` isn't blocked, and cleans up.

		Must be called after the host has started.
		"""
		# Loss of the control connection most likely means the host has died, but we wish to ensure it really has.
		exitStatus = self._controller.wait(_EXIT_CONFIRM_GRACE)
		if exitStatus is None:
			# The host is still alive, even after giving it extra time to finish.
			# Forcefully terminate it.
			self._controller.terminate()
			exitStatus = self._controller.poll()
		self._exitStatus = exitStatus
		with self._stateLock:
			if self._state == SessionState.STOPPING:
				# Termination was expected.
				self._state = SessionState.STOPPED
			else:
				# This is an unexpected termination.
				self._fail(f"Host exited prematurely with status {exitStatus}")
		# If the host exited prematurely while launching, start may still be waiting on the ready signal.
		if not self._readinessReported.is_set():
			self._readinessReported.set()
		self._stopHost()

	def close(self) -> None:
		"""Close the session, stopping the host.

		Safe to call more than once, and on a session that failed or was never started.
		A failed session stays ``FAILED``; any other session becomes ``STOPPED``.
		"""
		with self._stateLock:
			if self._state is SessionState.STOPPED:
				return
			if self._state is not SessionState.FAILED:
				self._state = SessionState.STOPPING
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
