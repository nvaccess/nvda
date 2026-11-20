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
import itertools
import queue
import threading
import time
from collections.abc import Callable
from typing import TYPE_CHECKING, Final

import rpyc
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
#: Maximum time from launch to a usable host root service, in seconds.
_STARTUP_TIMEOUT: Final[float] = 30.0
#: How frequently to send a heartbeat request to the host, in seconds.
_HEARTBEAT_INTERVAL: Final[float] = 5.0
#: Limit on how many heartbeat requests a host may fail to acknowledge in a timely manner before being considered unresponsive.
_CONSECUTIVE_HEARTBEAT_MISS_LIMIT: Final[int] = 3


def dbg(msg: str) -> None:
	import datetime
	import inspect

	now = datetime.datetime.now()  # noqa: DTZ005
	print(f"{inspect.stack()[1].function} {now.second}.{now.microsecond // 1000:03d}: {msg}")


class SessionState(enum.Enum):
	"""Where an add-on session is in its lifecycle.

	A healthy session moves through ``NEW``, ``STARTING``, ``READY``, ``STOPPING`` and ``STOPPED`` in order.
	A session stopped while starting moves straight from ``STARTING`` to ``STOPPING``, and is never ``READY``.
	A session stopped before it was started moves straight from ``NEW`` to ``STOPPED``.
	In case of an issue with the host, a started session may move from any state other than ``STOPPED`` straight to ``FAILED``.

	``STOPPED`` and ``FAILED`` are final.
	"""

	NEW = enum.auto()
	"""Constructed, but not yet started."""
	STARTING = enum.auto()
	"""``start`` has been called, but the host has not yet signalled readiness."""
	READY = enum.auto()
	"""The host signalled that it launched successfully."""
	STOPPING = enum.auto()
	"""Stop has been called on the session, but it has not yet finished shutting down."""
	STOPPED = enum.auto()
	"""The session was stopped. Final."""
	FAILED = enum.auto()
	"""The session failed. Final. A blocked launch is cleaned up when it returns."""

	@property
	def isFinal(self) -> bool:
		"""Whether the session can no longer change state."""
		return self is SessionState.STOPPED or self is SessionState.FAILED


class HostLaunchError(RuntimeError):
	"""The host could not be brought to readiness."""


class AddonSession:
	"""A single add-on session.

	Owns the host (through a :class:`HostController`), the control connection to it,
	and the lifecycle that takes it from launch to readiness and back down again.
	"""

	def __init__(
		self,
		controller: HostController,
		*,
		exitConfirmGrace: float = _EXIT_CONFIRM_GRACE,
		heartbeatInterval: float = _HEARTBEAT_INTERVAL,
		consecutiveHeartbeatMissLimit: int = _CONSECUTIVE_HEARTBEAT_MISS_LIMIT,
	) -> None:
		"""Initializer.

		:param controller: Starts, watches and stops the host.
			Owned by the session from here on.
		:param exitConfirmGrace: How long to give the host before killing it when the control connection is lost.
			Defaults to :const:`_EXIT_CONFIRM_GRACE`.
		:param heartbeatInterval: How frequently to send heartbeat requests to the host, in seconds.
			Defaults to :const:`_HEARTBEAT_INTERVAL`.
		:param consecutiveHeartbeatMissLimit: The number of heartbeat requests the host may fail to acknowledge on time before being considered unresponsive.
			Defaults to :const:`_CONSECUTIVE_HEARTBEAT_MISS_LIMIT`.
		:raises ValueError: If ``exitConfirmGrace`` is nonpositive or infinite.
		:raises ValueError: If ``heartbeatInterval`` is nonpositive or infinite.
		:raises ValueError: if ``consecutiveHeartbeatMissLimit`` is nonpositive.
		:raises TypeError: If ``consecutiveHeartbeatMissLimit`` is not an integer.
		"""
		if not 0 < exitConfirmGrace < float("inf"):
			raise ValueError("exitConfirmGrace must be finite and positive")
		if not 0 < heartbeatInterval < float("inf"):
			raise ValueError("heartbeatInterval must be finite and positive")
		if not isinstance(consecutiveHeartbeatMissLimit, int):
			raise TypeError("consecutiveHeartbeatMissLimit must be integral.")
		if not 0 < consecutiveHeartbeatMissLimit:
			raise ValueError("consecutiveHeartbeatMissLimit must be positive.")
		self._controller = controller
		self._exitConfirmGrace = exitConfirmGrace
		self._heartbeatInterval = heartbeatInterval
		self._consecutiveHeartbeatMissLimit = consecutiveHeartbeatMissLimit
		# stateChanged and heartbeatCond guard some of the same resources, and have overlapping interests.
		# Make them share the same underlying reentrant lock.
		rLock = threading.RLock()
		self._stateChanged = threading.Condition(rLock)
		self._heartbeatCond = threading.Condition(rLock)
		self._state = SessionState.NEW
		self._failureReason: str | None = None
		self._conn: Connection[CoreRootService, HostRootService] | None = None
		self._hostRoot: HostRootService | None = None
		# Guarded by ``_stateChanged``, so that ``start`` can wait for readiness and failure together.
		self._readinessReported = False
		self._readinessFailure: str | None = None
		self._heartbeatAckId = None
		self._heartbeatSender: threading.Thread | None = None
		self._heartbeatWatcher: threading.Thread | None = None

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
		"""The host's exit status, or ``None`` if it has not been started or is still running."""
		if not self._controller.started:
			return None
		return self._controller.poll()

	@property
	def hostRoot(self) -> HostRootService:
		"""The host's root service, through which core reaches the add-on's feature components.

		:raises RuntimeError: If the session is not ready.
		"""
		# ``_hostRoot`` is set before the session is ``READY``, and only cleared after it leaves ``READY``,
		# so reading the state first makes this snapshot consistent without holding ``_stateChanged``.
		if (state := self._state) is not SessionState.READY or (hostRoot := self._hostRoot) is None:
			raise RuntimeError(f"Add-on session is not ready (state: {state.name})")
		return hostRoot

	@staticmethod
	def _isTransitionValid(old: SessionState, new: SessionState) -> bool:
		"""Whether the lifecycle allows the session to move from ``old`` to ``new``.

		See :class:`SessionState` for the allowed transitions.
		"""
		match old, new:
			case (_, SessionState.FAILED):
				return old is not SessionState.NEW and old is not SessionState.STOPPED
			case (
				(SessionState.NEW, SessionState.STARTING | SessionState.STOPPED)
				| (SessionState.STARTING, SessionState.READY | SessionState.STOPPING)
				| (SessionState.READY, SessionState.STOPPING)
				| (SessionState.STOPPING, SessionState.STOPPED)
			):
				return True
			case _:
				return False

	def _setState(self, state: SessionState) -> None:
		"""Move the session to ``state``, and wake everything waiting on a state change.

		Every state transition goes through here.
		Must be called with :attr:`_stateChanged` held.
		"""
		if state is self._state:
			return
		assert self._isTransitionValid(self._state, state), (
			f"Cannot transition from {self._state.name} to {state.name}"
		)
		wasReady = self._state is SessionState.READY
		self._state = state
		self._stateChanged.notify_all()
		if wasReady:
			self._heartbeatCond.notify_all()

	def _waitForStartupStep(self, predicate: Callable[[], bool], deadline: float) -> None:
		"""Wait for a startup step using the shared deadline, with ``_stateChanged`` held."""
		if not self._stateChanged.wait_for(predicate, max(0.0, deadline - time.monotonic())):
			raise TimeoutError("Host startup timed out")

	def start(self, *, timeout: float = _STARTUP_TIMEOUT) -> None:
		"""Launch the host and wait for it to signal readiness.

		Blocks until the host is ready and its root service is available, or the session fails.
		Startup is bounded by ``timeout``, including when stopped while starting.
		If the session is stopped in the meantime, the host is allowed to finish launching and then stopped.
		A controller still blocked at the deadline is cleaned up when it returns.

		:param timeout: Seconds allowed for launch, readiness and fetching the host's root service.
			Defaults to :const:`_STARTUP_TIMEOUT`.
		:raises ValueError: If ``timeout`` is nonpositive or infinite.
		:raises RuntimeError: If the session has already been started.
		:raises HostLaunchError: If the host could not be started, reported a failed launch,
			did not expose its root service, startup timed out, or the session was stopped while starting.
			The session is ``FAILED`` or ``STOPPED`` respectively; a blocked launch is cleaned up later.
			Startup timeouts have a :class:`TimeoutError` as their cause.
		"""
		if not 0 < timeout < float("inf"):
			raise ValueError("startupTimeout must be finite and positive")
		print(f"start: called with {timeout=}")
		with self._stateChanged:
			if self._state is not SessionState.NEW:
				raise RuntimeError(f"Add-on session has already been started (state: {self._state.name})")
			self._setState(SessionState.STARTING)
		deadline = time.monotonic() + timeout
		try:
			self._conn = self._connectHost(deadline)
			print("start: Starting control connection service thread...")
			threading.Thread(
				target=self._serveControlConnection,
				name=f"ART connection event loop: {CONTROL_CONNECTION_NAME}",
				daemon=True,
			).start()
			self._waitForReady(deadline)
		except HostLaunchError:
			raise
		except Exception as e:
			self._fail(str(e) if isinstance(e, TimeoutError) else f"Host could not be started: {e}")
			raise HostLaunchError(f"Host did not launch: {self._failureReason}") from e

	def _connectHost(self, deadline: float) -> Connection:
		"""Bound controller startup and connection construction; dispose of a connection that arrives late."""
		outcome: list[Connection | Exception] = []

		def connect() -> None:
			stream = None
			try:
				stream = self._controller.start()
				result = Connection(
					stream,
					CoreRootService(onReady=self._onReady),
					name=CONTROL_CONNECTION_NAME,
				)
			except Exception as e:  # noqa: BLE001 -- pass launch errors back to the starting thread.
				result = e
				if stream is not None:
					stream.close()
			with self._stateChanged:
				if self._state in (SessionState.STARTING, SessionState.STOPPING):
					outcome.append(result)
					self._stateChanged.notify_all()
					return
			# Timeout won the race. Never publish these resources or terminate a controller
			# concurrently with its start call.
			try:
				if not isinstance(result, Exception):
					result.close()
			finally:
				self._controller.terminate()

		with self._stateChanged:
			threading.Thread(target=connect, name="ART host launch", daemon=True).start()
			try:
				self._waitForStartupStep(lambda: bool(outcome), deadline)
			except TimeoutError as e:
				self._fail(str(e), stopHost=False)
				raise
		result = outcome[0]
		if isinstance(result, Exception):
			raise result
		return result

	def _fetchHostRoot(self, deadline: float) -> HostRootService:
		"""Fetch the root off-thread so an unresponsive host cannot hold up startup."""
		outcome: list[HostRootService | Exception] = []
		conn = self._conn
		assert conn is not None

		def fetch() -> None:
			try:
				result = conn.remoteService
			except Exception as e:  # noqa: BLE001 -- pass RPC errors back to the starting thread.
				result = e
			with self._stateChanged:
				outcome.append(result)
				self._stateChanged.notify_all()

		with self._stateChanged:
			threading.Thread(target=fetch, name="ART host root lookup", daemon=True).start()
			self._waitForStartupStep(lambda: bool(outcome) or self._state is SessionState.FAILED, deadline)
			if self._state is SessionState.FAILED:
				raise HostLaunchError(f"Host did not launch: {self._failureReason}")
		result = outcome[0]
		if isinstance(result, Exception):
			raise result
		return result

	def _waitForReady(self, deadline: float) -> None:
		"""Wait for readiness and fetch the root service within the startup deadline."""
		print("start: Waiting for a status update...")
		with self._stateChanged:
			# Not woken by a stop: the host must be left to finish launching before it is stopped.
			self._waitForStartupStep(
				lambda: self._readinessReported or self._state is SessionState.FAILED,
				deadline,
			)
			state = self._state
			failure = self._readinessFailure
			print(f"start: Got {state=} and {failure=}")
		if state is SessionState.STARTING and failure is None:
			# A host that cannot expose its root service has failed to launch,
			# and fetching it here means ``hostRoot`` never makes a round trip to the host.
			# It is a round trip, so happens without ``_stateChanged`` held.
			print("start: Fetching host root service...")
			try:
				hostRoot = self._fetchHostRoot(deadline)
			except (TimeoutError, HostLaunchError):
				raise
			except Exception as e:
				# If readiness was reported but the host died before serving the control conection,
				# the connection will be closed, but _onControlConnectionLost may not have finished marking the session as failed.
				# Wait for the session to be marked as FAILED before raising,
				# so the top-most exception explains that this is due to the control connection dying.
				if (conn := self._conn) is None or conn.closed:
					with self._stateChanged:
						self._waitForStartupStep(lambda: self._state.isFinal, deadline)
				else:
					self._fail(f"Could not fetch the host's root service: {e}")
				raise HostLaunchError(f"Host did not launch: {self._failureReason}") from e
			print("start: Got host root service")
			with self._stateChanged:
				# The session may have been stopped, or failed, during the round trip.
				if (state := self._state) is SessionState.STARTING:
					print("start: Started successfully")
					self._hostRoot = hostRoot
					self._setState(SessionState.READY)
					self._startWatchdog()
					log.debug("ART add-on session is ready")
					return
		# Stopping the host blocks this thread,
		# but we are interested in state changes in the meantime,
		# such as if a failure is detected during shutdown.
		# Thus, we act on a request to stop without ``_stateChanged`` held.
		if state is SessionState.FAILED:
			raise HostLaunchError(f"Host did not launch: {self._failureReason}")
		if failure is not None:
			self._fail(f"Host reported a failed launch: {failure}")
			raise HostLaunchError(f"Host reported a failed launch: {failure}")
		# The session was stopped while starting, and ``stop`` is waiting for this thread to stop the host.
		self._finishStopping()
		raise HostLaunchError("Add-on session was stopped while starting")

	def _onReady(self, failure: str | None) -> None:
		"""Receive the outcome of the host's readiness signal.

		Runs on the control connection's serving thread, so only records the outcome.
		"""
		with self._stateChanged:
			print(f"onReady: _onReady({failure=})")
			self._readinessFailure = failure
			self._readinessReported = True
			self._stateChanged.notify_all()

	def _serveControlConnection(self) -> None:
		try:
			print("serveControlConnection: Serving control connection...")
			self._conn.eventLoop()
		finally:
			print("serveControlConnection: Control connection exhausted")
			self._onControlConnectionLost()

	def _onControlConnectionLost(self) -> None:
		"""Work out why the control connection closed, and fail the session if core did not close it."""
		print("_onControlConnectionLost: determining reason...")
		with self._stateChanged:
			if self._conn is None or self._state.isFinal:
				# Core closed the connection itself, so the host stopping is expected.
				print(
					f"_onControlConnectionLost: expected loss of control connection ({self._state=}, {self._readinessReported=})",
				)
				return
		exitStatus = self._controller.wait(self._exitConfirmGrace)
		if exitStatus is None:
			self._fail("Host closed the control connection, but did not exit")
		else:
			self._fail(f"Host exited unexpectedly with status {exitStatus}")

	def _startWatchdog(self) -> None:
		dbg("Creating request queue...")
		send = queue.Queue(maxsize=self._consecutiveHeartbeatMissLimit)
		dbg("Creating heartbeat watcher and server...")
		self._heartbeatWatcher = watcher = threading.Thread(
			target=self._watchHeartbeats,
			args=(send,),
			daemon=True,
			name="ART heartbeat watchdog",
		)
		self._heartbeatSender = sender = threading.Thread(
			target=self._sendHeartbeats,
			args=(send,),
			daemon=True,
			name="ART heartbeat sender",
		)
		dbg("Starting watchdog threads...")
		watcher.start()
		sender.start()

	def _watchHeartbeats(self, send: queue.Queue[tuple[int, float]]) -> None:
		dbg("Entering")
		idGen = itertools.count()
		missed = 0
		fail = False
		try:
			with self._heartbeatCond:
				if self._state is not SessionState.READY:
					dbg(f"Exiting early as state is {self._state.name}")
					return
				while True:
					id = next(idGen)
					deadline = time.monotonic() + self._heartbeatInterval
					dbg(f"Sending heartbead request with {id=} and {deadline=}")
					try:
						send.put_nowait((id, deadline))
					except queue.Full:
						dbg("Queue full, failing")
						fail = True
						break
					now = time.monotonic()
					timeout = max(0, deadline - now)
					dbg(f"Waiting for {timeout} ({now=})")
					self._heartbeatCond.wait_for(
						lambda id=id: self._heartbeatAckId == id or self._state is not SessionState.READY,
						timeout=timeout,
					)
					dbg(f"Woke at {time.monotonic()}")
					if self._state is not SessionState.READY:
						dbg(f"exiting as state is {self._state.name}")
						break
					if self._heartbeatAckId != id:
						dbg(f"want {id}, got {self._heartbeatAckId}. Incrementing missed from {missed}")
						missed += 1
						if missed >= self._consecutiveHeartbeatMissLimit:
							dbg(f"{missed=} >= {self._consecutiveHeartbeatMissLimit=}, failing")
							fail = True
							break
					else:
						dbg("resetting missed to 0")
						missed = 0
					now = time.monotonic()
					timeout = max(0, deadline - now)
					dbg(f"Waiting for {timeout} ({now=})")
					if self._heartbeatCond.wait_for(
						lambda: self._state is not SessionState.READY,
						timeout=timeout,
					):
						dbg(f"exiting as state is {self._state.name}")
						break
		finally:
			dbg("Shutting down send queue")
			send.shutdown(immediate=True)
			if fail:
				dbg("Failing session")
				self._fail("Add-on stopped responding.")
				dbg("done")

	def _sendHeartbeats(self, send: queue.Queue[tuple[int, float]]) -> None:
		dbg("entering")
		while True:
			dbg("Waiting for request")
			try:
				id, deadline = send.get()
			except queue.ShutDown:
				dbg("Queue shutdown, exiting")
				break
			dbg(f"got request with {id=} and {deadline=}")
			if deadline <= (now := time.monotonic()):
				dbg(f"{deadline=} <= {now=}, dropping")
				continue
			dbg("Creating and sending ping")
			req = self._conn._conn.async_request(rpyc.core.consts.HANDLE_PING, id)
			req.add_callback(self._heartbeatCallbackFactory(id, deadline))
		dbg("done")

	def _heartbeatCallbackFactory(
		self,
		id: int,
		deadline: float,
	) -> Callable[[rpyc.core.async_.AsyncResult], None]:
		def callback(res: rpyc.core.async_.AsyncResult) -> None:
			dbg("entering")
			with self._heartbeatCond:
				dbg(f"Checking prereqs ({id=}, {deadline=}, {res=}")
				if not (
					self._state is SessionState.READY
					and time.monotonic() < deadline
					and res.ready
					and not res.error
					and res.value == id
				):
					dbg("Prerequisites not satisfied, dropping")
					return
				dbg("prereqs met, setting heartbeatAckId and notifying heartbeatCond")
				self._heartbeatAckId = id
				self._heartbeatCond.notify_all()
			dbg("done")

		return callback

	def stop(self) -> None:
		"""Stop the session and its host.

		Blocks until the session is ``STOPPED`` or ``FAILED``.
		A session that is still starting has its host left to finish launching before it is stopped,
		so this must not be called on the control connection's serving thread.

		Safe to call more than once, and on a session that failed or was never started.
		A failed session stays ``FAILED``; any other session becomes ``STOPPED``,
		unless it fails while shutting down.
		"""
		with self._stateChanged:
			match self._state:
				case SessionState.NEW:
					self._setState(SessionState.STOPPED)
					return
				case SessionState.STOPPED | SessionState.FAILED:
					return
				case SessionState.STARTING | SessionState.STOPPING:
					# ``start`` stops the host if ``state`` is ``STOPPING`` when launch has finished.
					self._setState(SessionState.STOPPING)
					self._stateChanged.wait_for(lambda: self._state.isFinal)
					return
				case SessionState.READY:
					self._setState(SessionState.STOPPING)
		self._finishStopping()

	def _finishStopping(self) -> None:
		"""Stop the host of a ``STOPPING`` session, and mark the session ``STOPPED``.

		Must be called by exactly one thread per session, without :attr:`_stateChanged` held.
		"""
		self._stopHost()
		with self._stateChanged:
			# The session may have failed while the host was being stopped.
			if self._state is SessionState.STOPPING:
				self._setState(SessionState.STOPPED)

	def _fail(self, reason: str, *, stopHost: bool = True) -> None:
		"""Mark the session as failed, and stop the host.

		Only the first failure is recorded.

		:param reason: Why the session failed.
		:param stopHost: False when a blocked launch must clean up its own resources later.
		"""
		with self._stateChanged:
			if self._state.isFinal:
				return
			log.warning(f"ART add-on session failed: {reason}")
			self._failureReason = reason
			try:
				if stopHost:
					self._stopHost()
			finally:
				self._setState(SessionState.FAILED)

	def _stopHost(self) -> None:
		"""Close the control connection, then stop the host.

		Closing the connection first lets a healthy host see end-of-file and exit by itself.
		"""
		self._hostRoot = None
		with self._stateChanged:
			conn = self._conn
			self._conn = None
		if conn is not None:
			conn.close()
		self._controller.terminate()
