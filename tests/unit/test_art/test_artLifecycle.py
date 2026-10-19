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


def startWithin(testCase: unittest.TestCase, session: AddonSession, timeout: float = _TIMEOUT) -> None:
	"""Start ``session``, failing the test rather than hanging if ``start`` does not return.

	Re-raises whatever ``start`` raised.
	"""
	# Used for mutability; should only ever have 0 or 1 elements.
	outcome: list[BaseException | None] = []

	def target():
		try:
			session.start()
		except BaseException as e:  # noqa: BLE001
			outcome.append(e)
		else:
			outcome.append(None)

	thread = threading.Thread(target=target, name="test session start", daemon=True)
	thread.start()
	thread.join(timeout)
	if not outcome:
		testCase.fail(f"AddonSession.start did not return within {timeout}s")
	if (exc := outcome[0]) is not None:
		raise exc


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
		self.service.ready()
		self.onReady.assert_called_once_with(None)

	def test_failureIsDelivered(self):
		"""A host reporting a failure has its reason passed on."""
		self.service.ready("component failed to load")
		self.onReady.assert_called_once_with("component failed to load")

	def test_onlyTheFirstSignalCounts(self):
		"""The add-on shares the host's process, so a later signal must not change the outcome."""
		self.service.ready()
		self.service.ready("late failure")
		self.onReady.assert_called_once_with(None)

	def test_malformedSignalIsRejectedAndDoesNotCount(self):
		"""A failure that is not a string is refused, and leaves the real signal to come."""
		with self.assertRaises(TypeError):
			self.service.ready(42)
		self.onReady.assert_not_called()
		self.service.ready()
		self.onReady.assert_called_once_with(None)

	def test_strSubclassIsRejected(self):
		"""Across the boundary a ``str`` subclass is a netref, not a string, so it is refused."""

		class NotQuiteStr(str):
			pass

		with self.assertRaises(TypeError):
			self.service.ready(NotQuiteStr("failure"))
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
			conn.remoteService.ready("late failure")
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
