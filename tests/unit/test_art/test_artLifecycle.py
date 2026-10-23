# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the ART add-on session lifecycle.

Lifecycle behaviour is tested over the thread-backed host controller.
Only facts that need a real process run against :class:`SubprocessHostController`.
"""

import threading
import unittest
from collections.abc import Callable
from unittest.mock import MagicMock

from _art.host import entrypoint
from _art.host.rootService import HostRootService
from _art.session.addonSession import AddonSession, HostLaunchError, SessionState
from _art.session.hostController import SubprocessHostController
from _art.session.rootService import CoreRootService
from _art.transport import Connection
from rpyc.core.stream import Stream

from .threadHostController import ThreadHostController

#: Bound on anything involving a real process or a background thread, in seconds.
_TIMEOUT: float = 30.0


class BackgroundCall:
	"""Runs a call on a daemon thread, so a test can bound how long it waits for it."""

	def __init__(self, func: Callable[[], None], name: str) -> None:
		# Used for mutability; should only ever have 0 or 1 elements.
		self._outcome: list[BaseException | None] = []
		self._name = name
		self._thread = threading.Thread(target=self._run, args=(func,), name=name, daemon=True)
		self._thread.start()

	def _run(self, func: Callable[[], None]) -> None:
		try:
			func()
		except BaseException as e:  # noqa: BLE001
			self._outcome.append(e)
		else:
			self._outcome.append(None)

	def result(self, testCase: unittest.TestCase, timeout: float = _TIMEOUT) -> None:
		"""Wait for the call, failing the test rather than hanging if it does not return.

		Re-raises whatever the call raised.
		"""
		self._thread.join(timeout)
		if not self._outcome:
			testCase.fail(f"{self._name} did not return within {timeout}s")
		if (exc := self._outcome[0]) is not None:
			raise exc


def startWithin(testCase: unittest.TestCase, session: AddonSession, timeout: float = _TIMEOUT) -> None:
	"""Start ``session``, failing the test rather than hanging if ``start`` does not return.

	Re-raises whatever ``start`` raised.
	"""
	BackgroundCall(session.start, "AddonSession.start").result(testCase, timeout)


def waitForState(session: AddonSession, state: SessionState, timeout: float = _TIMEOUT) -> bool:
	"""Wait for ``session`` to reach ``state``, returning whether it did within ``timeout``."""
	with session._stateChanged:
		return session._stateChanged.wait_for(lambda: session.state is state, timeout)


def recordStates(session: AddonSession) -> list[SessionState]:
	"""Record every state ``session`` moves to from here on."""
	states: list[SessionState] = []
	realSetState = session._setState

	def setState(state: SessionState) -> None:
		states.append(state)
		realSetState(state)

	session._setState = setState
	return states


def makeHostRun(body: Callable[[Connection], None]) -> Callable[[Stream], None]:
	"""Build a host half that runs ``body`` in place of the real entry point's readiness signal.

	``body`` receives the host's end of the control connection, and the event loop runs once it returns.
	"""

	def run(stream: Stream) -> None:
		conn = Connection(stream, HostRootService(), name=entrypoint.CONTROL_CONNECTION_NAME)
		try:
			body(conn)
			conn.eventLoop()
		finally:
			conn.close()

	return run


class TestReadinessSignalReceipt(unittest.TestCase):
	"""Core's handling of the readiness signal, independent of any connection."""

	def setUp(self):
		self.onReady = MagicMock()
		self.service = CoreRootService(onReady=self.onReady)

	def test_successIsDelivered(self):
		"""A host reporting no failure is reported as ready."""
		self.service._ready()
		self.onReady.assert_called_once_with(None)

	def test_failureIsDelivered(self):
		"""A host reporting a failure has its reason passed on."""
		self.service._ready("component failed to load")
		self.onReady.assert_called_once_with("component failed to load")

	def test_onlyTheFirstSignalCounts(self):
		"""The add-on shares the host's process, so a later signal must not change the outcome."""
		self.service._ready()
		self.service._ready("late failure")
		self.onReady.assert_called_once_with(None)

	def test_malformedSignalIsRejectedAndDoesNotCount(self):
		"""A failure that is not a string is refused, and leaves the real signal to come."""
		with self.assertRaises(TypeError):
			self.service._ready(42)
		self.onReady.assert_not_called()
		self.service._ready()
		self.onReady.assert_called_once_with(None)

	def test_strSubclassIsRejected(self):
		"""Across the boundary a ``str`` subclass is a netref, not a string, so it is refused."""

		class NotQuiteStr(str):
			pass

		with self.assertRaises(TypeError):
			self.service._ready(NotQuiteStr("failure"))
		self.onReady.assert_not_called()


class TestAddonSessionLaunch(unittest.TestCase):
	"""Launching a session and waiting for readiness, over the thread-backed controller."""

	def makeSession(self, controller: ThreadHostController | None = None) -> AddonSession:
		self.controller = controller if controller is not None else ThreadHostController()
		session = AddonSession(self.controller)
		self.addCleanup(session.close)
		return session

	def test_newSessionIsNotReady(self):
		"""Nothing is reachable before the session has been started."""
		session = self.makeSession()
		self.assertIs(session.state, SessionState.NEW)
		with self.assertRaises(RuntimeError):
			_ = session.hostRoot

	def test_sessionBecomesReady(self):
		"""A host that signals readiness takes the session to ``READY``, and can be reached."""
		session = self.makeSession()
		startWithin(self, session)
		self.assertIs(session.state, SessionState.READY)
		self.assertIsNone(session.failureReason)
		self.assertEqual(session.hostRoot.ping(), "pong")

	def test_reportedFailureAbortsLaunch(self):
		"""A host that reports a failed launch fails the session, and is stopped."""
		FAILURE_REASON = "component failed to load"
		session = self.makeSession(
			ThreadHostController(
				run=makeHostRun(lambda conn: entrypoint._signalReadiness(conn, FAILURE_REASON)),
			),
		)
		with self.assertRaises(HostLaunchError) as cm:
			startWithin(self, session)
		self.assertIn(FAILURE_REASON, str(cm.exception))
		self.assertIs(session.state, SessionState.FAILED)
		self.assertIn(FAILURE_REASON, session.failureReason)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))
		with self.assertRaises(RuntimeError):
			_ = session.hostRoot

	def test_laterSignalDoesNotChangeTheOutcome(self):
		"""A failure reported after a successful launch is ignored."""
		lateSignalSent = threading.Event()

		def body(conn: Connection) -> None:
			entrypoint._signalReadiness(conn)
			# Synchronous, so that core has handled it before the test looks.
			conn.remoteService._ready("late failure")
			lateSignalSent.set()

		session = self.makeSession(ThreadHostController(run=makeHostRun(body)))
		startWithin(self, session)
		self.assertTrue(lateSignalSent.wait(_TIMEOUT))
		self.assertIs(session.state, SessionState.READY)
		self.assertIsNone(session.failureReason)

	def test_controllerFailureAbortsLaunch(self):
		"""A host that cannot be started at all fails the session."""
		FAILURE_REASON = "no host for you"
		controller = MagicMock()
		controller.start.side_effect = OSError(FAILURE_REASON)
		session = AddonSession(controller)
		with self.assertRaises(HostLaunchError):
			session.start()
		self.assertIs(session.state, SessionState.FAILED)
		self.assertIn(FAILURE_REASON, session.failureReason)
		controller.terminate.assert_called()

	def test_startingTwiceIsRefused(self):
		"""A session launches one host, once."""
		session = self.makeSession()
		startWithin(self, session)
		with self.assertRaises(RuntimeError):
			session.start()

	def test_closeStopsTheHost(self):
		"""Closing a ready session stops its host."""
		session = self.makeSession()
		startWithin(self, session)
		session.close()
		self.assertIs(session.state, SessionState.STOPPED)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))
		with self.assertRaises(RuntimeError):
			_ = session.hostRoot

	def test_closePassesThroughStopping(self):
		"""The host is stopped while the session is ``STOPPING``, so its exit is expected rather than a failure."""
		statesWhenTerminated: list[SessionState] = []
		controller = ThreadHostController()
		realTerminate = controller.terminate

		def terminate() -> None:
			# In the case of a healthy session, the session must move its state to ``STOPPING`` before terminating the host,
			# so this test is a valid check of the state we're interested in.
			statesWhenTerminated.append(session.state)
			realTerminate()

		controller.terminate = terminate
		session = self.makeSession(controller)
		startWithin(self, session)
		session.close()
		# It is safe to call ``terminate`` on a terminated host,
		# but the terminating call must occur when the session is ``STOPPING``.
		# Thus, we only care about the session's state at the time of the first ``terminate``.
		self.assertEqual(statesWhenTerminated[0], SessionState.STOPPING)
		self.assertIs(session.state, SessionState.STOPPED)

	def makeHeldLaunchSession(self, failure: str | None = None) -> tuple[AddonSession, threading.Event]:
		"""Make a session whose host holds off signalling readiness until released.

		:param failure: The failure the host reports once released, or ``None`` for a successful launch.
		:returns: The session, and the event that releases the host.
		"""
		release = threading.Event()

		def body(conn: Connection) -> None:
			release.wait(_TIMEOUT)
			entrypoint._signalReadiness(conn, failure)

		return self.makeSession(ThreadHostController(run=makeHostRun(body))), release

	def test_closeDuringLaunchWaitsForReadiness(self):
		"""A session closed during launch lets the host finish launching, then stops it without ever being ready."""
		session, release = self.makeHeldLaunchSession()
		states = recordStates(session)
		start = BackgroundCall(session.start, "AddonSession.start")
		self.assertTrue(waitForState(session, SessionState.LAUNCHING))
		close = BackgroundCall(session.close, "AddonSession.close")
		self.assertTrue(waitForState(session, SessionState.STOPPING))
		# The host has not yet signalled readiness, so the session must hold off on terminating it.
		self.assertIsNone(self.controller.poll())
		release.set()
		close.result(self)
		with self.assertRaises(HostLaunchError):
			start.result(self)
		self.assertEqual(
			states,
			[SessionState.LAUNCHING, SessionState.STOPPING, SessionState.STOPPED],
		)
		self.assertIsNone(session.failureReason)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))

	def test_closeDuringFailedLaunchLeavesSessionFailed(self):
		"""A host that reports a failed launch after the session was closed still fails the session."""
		FAILURE_REASON = "component failed to load"
		session, release = self.makeHeldLaunchSession(FAILURE_REASON)
		start = BackgroundCall(session.start, "AddonSession.start")
		self.assertTrue(waitForState(session, SessionState.LAUNCHING))
		close = BackgroundCall(session.close, "AddonSession.close")
		self.assertTrue(waitForState(session, SessionState.STOPPING))
		release.set()
		close.result(self)
		with self.assertRaises(HostLaunchError):
			start.result(self)
		self.assertIs(session.state, SessionState.FAILED)
		self.assertIn(FAILURE_REASON, session.failureReason)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))

	def test_closeIsIdempotent(self):
		"""Closing twice, or closing a session that was never started, is not an error."""
		session = self.makeSession()
		session.close()
		session.close()
		self.assertIs(session.state, SessionState.STOPPED)

	def test_closeKeepsAFailedSessionFailed(self):
		"""Closing after a failure does not hide the failure."""
		session = self.makeSession(
			ThreadHostController(run=makeHostRun(lambda conn: entrypoint._signalReadiness(conn, "boom"))),
		)
		with self.assertRaises(HostLaunchError):
			startWithin(self, session)
		self.assertIs(session.state, SessionState.FAILED)
		session.close()
		self.assertIs(session.state, SessionState.FAILED)


class TestLifecycleProcessConformance(unittest.TestCase):
	"""Lifecycle facts checked against a real host process."""

	def test_realHostBecomesReady(self):
		"""A freshly booted host process signals readiness, and is stopped by closing the session."""
		controller = SubprocessHostController()
		session = AddonSession(controller)
		self.addCleanup(session.close)
		startWithin(self, session)
		self.assertIs(session.state, SessionState.READY)
		self.assertEqual(session.hostRoot.ping(), "pong")
		session.close()
		self.assertIsNotNone(controller.wait(_TIMEOUT))
