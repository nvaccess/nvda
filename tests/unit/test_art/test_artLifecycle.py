# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the ART add-on session lifecycle.

Lifecycle behaviour is tested over the thread-backed host controller.
Only facts that need a real process run against :class:`SubprocessHostController`.
"""

import pathlib
import threading
import unittest
from collections.abc import Callable
from functools import partial
from typing import Any
from unittest.mock import MagicMock, patch

import rpyc
from _art.host import entrypoint
from _art.host.rootService import HostRootService
from _art.session.addonSession import AddonSession, HostLaunchError, SessionState
from _art.session.hostController import SubprocessHostController, interpreterCommand
from _art.session.rootService import CoreRootService
from _art.transport import Connection
from rpyc.core.stream import Stream

from .threadHostController import ThreadHostController

#: Bound on anything involving a real process or a background thread, in seconds.
_TIMEOUT: float = 10.0
#: Grace given to a host to exit once its control connection closes, in tests that expect it not to.
_SHORT_GRACE: float = 0.2


def fakeHostCommand(fakeHost: str, behaviour: str, *arguments: str) -> list[str]:
	"""The command line that runs the fake host with ``behaviour``.

	See ``fakeHosts/fakeHost.py`` for the behaviours available.
	"""
	script = pathlib.Path(__file__).parent / "fakeHosts" / fakeHost
	return interpreterCommand(str(script), behaviour, *arguments)


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


def makeHostRun(body: Callable[[Connection], None], serve: bool = True) -> Callable[[Stream], None]:
	"""Build a host half that runs ``body`` in place of the real entry point's readiness signal.

	``body`` receives the host's end of the control connection.

	:param serve: Whether to run the event loop once ``body`` returns.
		If ``False``, the host finishes when ``body`` does, as though it had exited.
	"""

	def run(stream: Stream) -> None:
		print("makeHostRun: Constructing connection...")
		conn = Connection(stream, HostRootService(), name=entrypoint.CONTROL_CONNECTION_NAME)
		try:
			print("makeHostRun: calling body...")
			body(conn)
			print("makeHostRun: Returned from body")
			if serve:
				print("makeHostRun: serving control connection...")
				conn.eventLoop()
		except Exception as e:
			print(f"makeHostRun: caught exception {e}")
			raise
		finally:
			print("makeHostRun: closing connection...")
			conn.close()

	return run


def waitForState(session: AddonSession, *states: SessionState, timeout: float | None = _TIMEOUT) -> bool:
	"""Block until the session is in one of ``states``.

	A state the session passes through quickly, such as ``STOPPING``, can be over before a waiter wakes.
	The lifecycle only moves forward, so wait for the state you need together with every state that can follow it.

	:param states: The states to wait for.
	:param timeout: How long to wait, in seconds, or ``None`` to wait indefinitely.
	:returns: Whether the session was in one of ``states`` before ``timeout`` elapsed.
	"""
	with session._stateChanged:
		return session._stateChanged.wait_for(lambda: session._state in states, timeout)


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
		self.addCleanup(session.stop)
		return session

	def test_invalidExitConfirmGraceIsRejected(self):
		"""Passing a non-positive or infinite value to ``AddonSession()`` fails."""
		controller = MagicMock()
		for exitConfirmGrace in (0, -1.23, float("inf"), float("-inf"), float("nan")):
			with self.subTest(exitConfirmGrace=exitConfirmGrace), self.assertRaises(ValueError):
				AddonSession(controller, exitConfirmGrace=exitConfirmGrace)

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

	def test_stopStopsTheHost(self):
		"""Closing a ready session stops its host."""
		session = self.makeSession()
		startWithin(self, session)
		session.stop()
		self.assertIs(session.state, SessionState.STOPPED)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))
		with self.assertRaises(RuntimeError):
			_ = session.hostRoot

	def test_stopPassesThroughStopping(self):
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
		session.stop()
		# It is safe to call ``terminate`` on a terminated host,
		# but the terminating call must occur when the session is ``STOPPING``.
		# Thus, we only care about the session's state at the time of the first ``terminate``.
		self.assertEqual(statesWhenTerminated[0], SessionState.STOPPING)
		self.assertIs(session.state, SessionState.STOPPED)

	def test_stopIsIdempotent(self):
		"""Stopping twice, or stopping a session that was never started, is not an error."""
		session = self.makeSession()
		session.stop()
		session.stop()
		self.assertIs(session.state, SessionState.STOPPED)

	def test_stopKeepsAFailedSessionFailed(self):
		"""Stopping after a failure does not hide the failure."""
		session = self.makeSession(
			ThreadHostController(run=makeHostRun(lambda conn: entrypoint._signalReadiness(conn, "boom"))),
		)
		with self.assertRaises(HostLaunchError):
			startWithin(self, session)
		self.assertIs(session.state, SessionState.FAILED)
		session.stop()
		self.assertIs(session.state, SessionState.FAILED)


class TestLifecycleProcessConformance(unittest.TestCase):
	"""Lifecycle facts checked against a real host process."""

	def test_realHostBecomesReady(self):
		"""A freshly booted host process signals readiness, and is stopped by closing the session."""
		controller = SubprocessHostController()
		session = AddonSession(controller)
		self.addCleanup(session.stop)
		startWithin(self, session)
		self.assertIs(session.state, SessionState.READY)
		self.assertEqual(session.hostRoot.ping(), "pong")
		session.stop()
		self.assertIsNotNone(controller.wait(_TIMEOUT))


class TestStartupTimeout(unittest.TestCase):
	"""Startup deadlines against hosts that are slow to signal readiness or service the control connection."""

	def makeSession(self, run: Callable[[Stream], None], timeout: float = 0.2) -> AddonSession:
		self.controller = ThreadHostController(run=run)
		session = AddonSession(self.controller)
		session.start = partial(session.start, timeout=timeout)
		realTerminate = self.controller.terminate

		def terminate():
			print("Custom terminate: setting release...")
			self.release.set()
			print("Custom terminate: calling original terminate...")
			realTerminate()
			print("Custom terminate: Joining thread...")
			self.controller._thread.join(timeout=_TIMEOUT)
			self.assertFalse(self.controller._thread.is_alive(), "host thread did not end in time.")
			print("Custom terminate: done!")

		self.controller.terminate = terminate
		self.addCleanup(session.stop)
		return session

	def makeBody(self, signalReadiness: bool, timeout: float = _TIMEOUT) -> Callable[[Stream], None]:
		self.release = threading.Event()
		self.addCleanup(self.release.set)

		def body(conn: Connection) -> None:
			if signalReadiness:
				print("waitReadyWait->body: signalling readiness...")
				entrypoint._signalReadiness(conn)
			print("waitReadyWait->body: waiting to return...")
			self.release.wait(timeout)
			print("waitReadyWait->body: done!")

		return makeHostRun(body, serve=False)

	def assertTimedOut(self, session: AddonSession) -> None:
		print("assertTimedOut: called")
		with self.assertRaisesRegex(HostLaunchError, "startup timed out") as raised:
			print("assertTimedOut: asserting startsWithin raises HostLaunchError")
			startWithin(self, session)
		self.assertIsInstance(raised.exception.__cause__, TimeoutError)
		print("assertTimedOut: asserting session is FAILED")
		self.assertIs(session.state, SessionState.FAILED)
		print("assertTimedOut: asserting failure was due to timeout")
		self.assertIn("startup timed out", session.failureReason)
		print("assertTimedOut: asserting host is no-longer running")
		self.assertIsNotNone(self.controller.poll(), "Timed-out host was left running")
		print("assertTimedOut: asserting connection is gone")
		self.assertIsNone(session._conn)
		with self.assertRaises(RuntimeError):
			print("assertTimedOut: asserting hostRoot is inaccessible")
			_ = session.hostRoot

	def test_invalidTimeoutIsRejectedBeforeLaunch(self):
		"""Nonpositive and infinite timeouts are rejected."""
		controller = MagicMock()
		session = AddonSession(controller)
		for timeout in (0, -1, float("inf"), float("-inf"), float("nan")):
			with self.subTest(timeout=timeout):
				with self.assertRaises(ValueError):
					session.start(timeout=timeout)
				controller.start.assert_not_called()
				self.assertIs(session.state, SessionState.NEW)

	def test_hostThatNeverReportsReadinessIsKilled(self):
		"""A host that fails to report readiness is killed promptly."""
		self.assertTimedOut(self.makeSession(self.makeBody(signalReadiness=False)))

	def test_readyHostThatNeverServesRootIsKilled(self):
		"""A host that reports readiness but fails to serve the control connection is killed promptly."""
		session = self.makeSession(self.makeBody(signalReadiness=True))
		self.assertTimedOut(session)
		self.assertTrue(session._readinessReported)

	def test_blockedLaunchTimesOutAndDisposesOfLateResources(self):
		"""Timeout releases callers; a launch that finishes later must clean up its resources.

		Block either controller.start() or Connection construction. After timeout, let that
		operation either succeed or raise. Repeat with a concurrent stop() waiting for startup.
		"""
		for stage, failAfterRelease in (
			("controller", False),
			("controller", True),
			("connection", False),
			("connection", True),
		):
			for stopDuringLaunch in (False, True):
				with self.subTest(
					stage=stage,
					failAfterRelease=failAfterRelease,
					stopDuringLaunch=stopDuringLaunch,
				):
					self.checkBlockedLaunch(
						stage=stage,
						failAfterRelease=failAfterRelease,
						stopDuringLaunch=stopDuringLaunch,
					)

	@staticmethod
	def doBlockedOperation(blockedOperationStarted, release, failAfterRelease, blockedOperation):
		def inner(*args, **kwargs):
			blockedOperationStarted.set()
			release.wait(_TIMEOUT)
			if failAfterRelease:
				raise OSError("late launch failure")
			return blockedOperation.return_value

		return inner

	def checkBlockedLaunch(self, *, stage: str, failAfterRelease: bool, stopDuringLaunch: bool) -> None:
		"""Hold a launch operation open until start() (and optionally stop()) has returned.

		``stage`` is "controller" for controller.start(), or "connection" for Connection(...).
		``failAfterRelease`` makes that operation raise instead of returning its resource.
		The session must time out first, then dispose of whatever the late operation produced.
		"""
		blockedOperationStarted = threading.Event()
		release = threading.Event()
		hostTerminated = threading.Event()
		controller = MagicMock(name="controller")
		stream = MagicMock(name="control stream")
		conn = MagicMock(name="control connection")
		controller.start.return_value = stream
		controller.terminate.side_effect = hostTerminated.set
		session = AddonSession(controller)
		session.start = partial(session.start, timeout=0.2)

		with patch("_art.session.addonSession.Connection", return_value=conn) as connectionFactory:
			blockedOperation = controller.start if stage == "controller" else connectionFactory
			blockedOperation.side_effect = self.doBlockedOperation(
				blockedOperationStarted,
				release,
				failAfterRelease,
				blockedOperation,
			)

			try:
				if stopDuringLaunch:
					stopper = threading.Thread(
						target=lambda: session.stop() if blockedOperationStarted.wait(_TIMEOUT) else None,
						daemon=True,
					)
					stopper.start()
				# Neither caller may wait for the blocked operation to finish.
				with self.assertRaisesRegex(HostLaunchError, "startup timed out") as raised:
					startWithin(self, session, timeout=2.0)
				self.assertIsInstance(raised.exception.__cause__, TimeoutError)
				self.assertTrue(blockedOperationStarted.is_set())
				self.assertIs(session.state, SessionState.FAILED)
				self.assertIsNone(session._conn)
				# Terminating a controller while it is creating resources would race launch.
				controller.terminate.assert_not_called()
				if stopDuringLaunch:
					stopper.join(2.0)
					self.assertFalse(stopper.is_alive(), "Stop waited for the blocked launch")
			finally:
				# Release even if an assertion fails, so the worker can clean up.
				release.set()
				self.assertTrue(hostTerminated.wait(_TIMEOUT), "Late host was not stopped")

		# Success produces a connection; failed construction leaves only the raw stream.
		# If controller.start() raised, it never handed a resource to the session.
		if not failAfterRelease:
			conn.close.assert_called_once()
		elif stage == "connection":
			stream.close.assert_called_once()
		# A late result or exception must not replace the timeout or revive the session.
		self.assertIsNone(session._conn)
		self.assertIs(session.state, SessionState.FAILED)
		self.assertIn("startup timed out", session.failureReason)

	def test_stopDuringStartupCannotWaitForever(self):
		"""Stopping a starting session does not block indefinitely."""
		session = self.makeSession(self.makeBody(signalReadiness=False))

		def stop() -> None:
			if waitForState(session, SessionState.STARTING, SessionState.FAILED):
				session.stop()

		stopper = threading.Thread(target=stop, daemon=True)
		stopper.start()
		self.assertTimedOut(session)
		stopper.join(_TIMEOUT)
		self.assertFalse(stopper.is_alive(), "Stop did not return after startup timed out")

	def test_stopDuringRootLookupCannotWaitForever(self):
		"""A stop while fetching the root shares the startup timeout and its exception cause."""
		session = self.makeSession(self.makeBody(signalReadiness=True))
		fetch = session._fetchHostRoot
		fetching = threading.Event()

		def fetchRoot(deadline: float):
			fetching.set()
			return fetch(deadline)

		def stop() -> None:
			if fetching.wait(_TIMEOUT):
				session.stop()

		stopper = threading.Thread(target=stop, daemon=True)
		with patch.object(session, "_fetchHostRoot", side_effect=fetchRoot):
			stopper.start()
			self.assertTimedOut(session)
		stopper.join(_TIMEOUT)
		self.assertFalse(stopper.is_alive(), "Stop did not return after root lookup timed out")

	def test_startupWaitUsesRemainingTime(self):
		"""At t=107, a startup deadline of t=110 allows only three more seconds."""
		session = AddonSession(MagicMock())
		ready = MagicMock(return_value=False)
		with (
			patch("_art.session.addonSession.time.monotonic", return_value=107.0),
			patch.object(session._stateChanged, "wait_for", return_value=False) as wait,
			session._stateChanged,
		):
			with self.assertRaises(TimeoutError):
				session._waitForStartupStep(ready, deadline=110.0)
			wait.assert_called_once_with(ready, 3.0)


class TestChildExitDetection(unittest.TestCase):
	"""Noticing a host that goes away without being asked to, over the thread-backed controller."""

	def setUp(self):
		# Released at cleanup, so that no test leaves a host thread blocked.
		self.release = threading.Event()
		self.addCleanup(self.release.set)

	def makeSession(self, run: Callable[[Stream], None], **kwargs) -> AddonSession:
		self.controller = ThreadHostController(run=run)
		session = AddonSession(self.controller, **kwargs)
		self.addCleanup(session.stop)
		return session

	def exitAfterReady(
		self,
		exitWith: BaseException | None = None,
		serve: bool = True,
	) -> Callable[[Stream], None]:
		"""A host half that signals readiness, then finishes once :attr:`release` is set.

		:param exitWith: Raised to finish, or ``None`` to return normally.
		:param serve: Whether to serve the control connection after signalling readiness.
		"""

		def body(conn: Connection) -> None:
			print("exitAfterReady->body: Signalling readiness...")
			entrypoint._signalReadiness(conn)
			if serve:
				print("exitAfterReady->body: serving control connection...")
				threading.Thread(target=conn.eventLoop, daemon=True).start()
			print("exitAfterReady->body: Waiting for event before exiting...")
			self.release.wait(_TIMEOUT)
			print("exitAfterReady->body: Release set or timed out!")
			if exitWith is not None:
				print("exitAfterReady->body: raising {exitWith}")
				raise exitWith
			print("exitAfterReady->body: Returning")

		return makeHostRun(body, serve=False)

	def test_hostExitingAfterReadyFailsTheSession(self):
		"""A host that finishes of its own accord, even cleanly, has failed."""
		print("Test: making session...")
		session = self.makeSession(self.exitAfterReady())
		print("Test: Starting session...")
		startWithin(self, session)
		print("Test: setting release event...")
		self.release.set()
		print("Test: waiting for state to be FAILED...")
		self.assertTrue(waitForState(session, SessionState.FAILED))
		self.assertIs(session.state, SessionState.FAILED)
		self.assertIn("status 0", session.failureReason)
		self.assertEqual(session.exitStatus, 0)

	def test_hostCrashingAfterReadyFailsTheSession(self):
		"""A host that dies of an exception has failed, with a failure status."""
		session = self.makeSession(self.exitAfterReady(RuntimeError("host crashed")))
		startWithin(self, session)
		self.release.set()
		self.assertTrue(waitForState(session, SessionState.FAILED))
		self.assertIs(session.state, SessionState.FAILED)
		self.assertEqual(session.exitStatus, 1)

	def test_hostExitingDuringLaunchFailsItPromptly(self):
		"""A host that finishes before signalling readiness ends launch, rather than leaving ``start`` waiting."""
		session = self.makeSession(makeHostRun(lambda conn: None, serve=False))
		with self.assertRaises(HostLaunchError) as cm:
			startWithin(self, session)
		self.assertIn("exited unexpectedly", str(cm.exception))
		self.assertIs(session.state, SessionState.FAILED)

	def test_hostExitingBetweenReadyAndServingFailsPromptly(self):
		"""Test that a host that exits after signalling readiness but never starts serving the control connection fails, rather than leaving start waiting."""
		session = self.makeSession(self.exitAfterReady(serve=False))

		def setRelease():
			with session._stateChanged:
				session._stateChanged.wait_for(
					lambda: session._readinessReported or session._state.isFinal,
					timeout=_TIMEOUT,
				)
			self.release.set()

		threading.Thread(target=setRelease, daemon=True).start()
		with self.assertRaises(HostLaunchError) as cm:
			startWithin(self, session)
		self.assertIn("exited unexpectedly", str(cm.exception))
		self.assertIs(session.state, SessionState.FAILED)

	def test_closedConnectionIsNotTakenAsProofOfExit(self):
		"""A host that drops the connection but keeps running is stopped, and the session failed."""

		def body(conn: Connection) -> None:
			entrypoint._signalReadiness(conn)
			conn.bgEventLoop(daemon=True)
			self.release.wait(_TIMEOUT)
			conn.close()
			# A thread cannot be killed, so lingering here stands in for a process that will not exit.
			self.lingerDone.wait(_TIMEOUT)

		self.lingerDone = threading.Event()
		self.addCleanup(self.lingerDone.set)
		terminated = threading.Event()
		session = self.makeSession(makeHostRun(body, serve=False), exitConfirmGrace=_SHORT_GRACE)
		realTerminate = self.controller.terminate

		def terminate() -> None:
			terminated.set()
			realTerminate()

		self.controller.terminate = terminate
		startWithin(self, session)
		self.release.set()
		self.assertTrue(waitForState(session, SessionState.FAILED))
		self.assertIn("did not exit", session.failureReason)
		self.assertTrue(terminated.wait(_SHORT_GRACE))
		self.assertIsNone(session.exitStatus)

	def test_closingIsNotAFailure(self):
		"""The host going away because core closed the session is expected."""
		session = self.makeSession(entrypoint.run)
		startWithin(self, session)
		session.stop()
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))
		self.assertIs(session.state, SessionState.STOPPED)
		self.assertIsNone(session.failureReason)

	def test_stoppingDuringLaunchEndsLaunch(self):
		"""Closing a session that is still waiting for readiness makes ``start`` give up, without a failure."""
		session = self.makeSession(makeHostRun(entrypoint._signalReadiness))
		startError: list[BaseException] = []

		def start() -> None:
			try:
				session.start()
			except BaseException as e:  # noqa: BLE001
				startError.append(e)

		starter = threading.Thread(target=start, daemon=True)
		starter.start()
		# Anything other than ``NEW`` means launch has begun.
		self.assertTrue(
			waitForState(session, *(set(SessionState) - {SessionState.NEW})),
		)
		session.stop()
		starter.join(_TIMEOUT)
		self.assertFalse(starter.is_alive(), "start did not return after the session was closed")
		self.assertIsInstance(startError[0], HostLaunchError)
		self.assertIs(session.state, SessionState.STOPPED)
		self.assertIsNone(session.failureReason)

	def test_exitStatusIsNoneBeforeStart(self):
		"""There is no exit status for a host that was never started."""
		session = self.makeSession(entrypoint.run)
		self.assertIsNone(session.exitStatus)

	def test_connectionLossAfterCallingStopBeforeReadinessDoesNotBlock(self):
		self.started = threading.Event()
		self.addCleanup(self.started.set)

		def body(conn: Connection) -> None:
			self.started.set()
			self.release.wait(_TIMEOUT)

		session = self.makeSession(makeHostRun(body, serve=False), exitConfirmGrace=_SHORT_GRACE)

		def stopper() -> None:
			self.started.wait(_TIMEOUT)
			session.stop()

		def releaser() -> None:
			waitForState(session, SessionState.STOPPING)
			self.release.set()

		stopperThread = threading.Thread(target=stopper, daemon=True)
		releaserThread = threading.Thread(target=releaser, daemon=True)
		stopperThread.start()
		releaserThread.start()
		with self.assertRaises(HostLaunchError) as cm:
			startWithin(self, session)
		self.assertIn("exited unexpectedly", str(cm.exception))
		self.assertIs(session.state, SessionState.FAILED)
		stopperThread.join(_TIMEOUT)
		releaserThread.join(_TIMEOUT)
		self.assertFalse(stopperThread.is_alive())
		self.assertFalse(releaserThread.is_alive())


class TestChildExitDetectionProcessConformance(unittest.TestCase):
	"""Exit detection against real host processes, which can die in ways a thread cannot."""

	def makeSession(self, *command: str, **kwargs) -> AddonSession:
		self.controller = SubprocessHostController(command=fakeHostCommand("exitDetection.py", *command))
		session = AddonSession(self.controller, **kwargs)
		self.addCleanup(session.stop)
		return session

	def test_hostDyingAfterReadyIsDetected(self):
		"""A host process that dies abruptly closes its pipe, and core records how it died."""
		session = self.makeSession("instrumented")
		startWithin(self, session)
		rpyc.async_(session.hostRoot._crash)(3)
		self.assertTrue(waitForState(session, SessionState.FAILED))
		self.assertIs(session.state, SessionState.FAILED)
		self.assertEqual(session.exitStatus, 3)
		self.assertIn("status 3", session.failureReason)

	def test_hostIsADirectChildOfCore(self):
		"""The process the controller holds is the host itself, not a launcher standing between them.

		A launcher would hold its own copies of the host's pipes, hiding a host that closes its end,
		and would be the process that handles for dependent connections are duplicated into.
		"""
		session = self.makeSession("instrumented")
		startWithin(self, session)
		self.assertEqual(session.hostRoot._getPid(), self.controller._process.pid)

	def test_hostDyingDuringLaunchFailsItPromptly(self):
		"""A host process that dies before signalling readiness ends launch straight away."""
		session = self.makeSession("exitBeforeReady", "4")
		with self.assertRaises(HostLaunchError):
			startWithin(self, session)
		self.assertIs(session.state, SessionState.FAILED)
		self.assertEqual(session.exitStatus, 4)

	def test_hostDyingBeforeServingFailsLaunch(self):
		"""A host process that dies between signalling readiness and serving the controll connection ends launch."""
		session = self.makeSession("exitBeforeServe", "5")
		session._onReady = MagicMock(wraps=session._onReady)
		with self.assertRaises(HostLaunchError):
			startWithin(self, session)
		session._onReady.assert_called_once_with(None)
		self.assertIs(session.state, SessionState.FAILED)
		self.assertEqual(session.exitStatus, 5)

	def test_lingeringHostIsStopped(self):
		"""A host process that closes its pipe but keeps running is stopped, rather than left behind."""
		session = self.makeSession("closeAndLinger", exitConfirmGrace=_SHORT_GRACE)
		with self.assertRaises(HostLaunchError):
			startWithin(self, session)
		self.assertIn("did not exit", session.failureReason)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))


class TestHeartbeat(unittest.TestCase):
	"""Noticing when a host has frozen."""

	def test_invalidHeartbeatIntervalIsRejected(self):
		"""Passing a non-positive or infinite value of ``heartbeatInterval`` to ``AddonSession()`` fails."""
		controller = MagicMock()
		for heartbeatInterval in (0, -42, float("inf"), float("-inf"), float("nan")):
			with self.subTest(heartbeatInterval=heartbeatInterval), self.assertRaises(ValueError):
				AddonSession(controller, heartbeatInterval=heartbeatInterval)

	def test_invalidConsecutiveHeartbeatMissLimitIsRejected(self):
		"""Passing a non-positive or non-integer value of ``consecutiveHeartbeatMissLimit`` to ``AddonSession()`` fails."""
		controller = MagicMock()
		for consecutiveHeartbeatMissLimit in (0, -42):
			with (
				self.subTest(consecutiveHeartbeatMissLimit=consecutiveHeartbeatMissLimit),
				self.assertRaises(ValueError),
			):
				AddonSession(controller, consecutiveHeartbeatMissLimit=consecutiveHeartbeatMissLimit)
		for consecutiveHeartbeatMissLimit in (3.14, float("inf"), float("-inf"), float("nan")):
			with (
				self.subTest(consecutiveHeartbeatMissLimit=consecutiveHeartbeatMissLimit),
				self.assertRaises(TypeError),
			):
				AddonSession(controller, consecutiveHeartbeatMissLimit=consecutiveHeartbeatMissLimit)

	def test_stateTransitionsNotifyHeartbeadCond(self) -> None:
		"""Moving from ``READY`` to another state should notify the heartbeat condition."""
		session = AddonSession(MagicMock())
		session._heartbeatCond = MagicMock(wraps=session._heartbeatCond)
		for old, new, notify in (
			(SessionState.NEW, SessionState.STARTING, False),
			(SessionState.NEW, SessionState.STOPPED, False),
			(SessionState.STARTING, SessionState.READY, False),
			(SessionState.STARTING, SessionState.FAILED, False),
			(SessionState.READY, SessionState.STOPPING, True),
			(SessionState.READY, SessionState.FAILED, True),
			(SessionState.STOPPING, SessionState.STOPPED, False),
			(SessionState.STOPPING, SessionState.FAILED, False),
		):
			session._state = old
			with self.subTest(old=old, new=new):
				with session._stateChanged:
					session._setState(new)
				if notify:
					session._heartbeatCond.notify_all.assert_called_once()
				else:
					session._heartbeatCond.notify_all.assert_not_called()
			session._heartbeatCond.reset_mock()

	@staticmethod
	def sideEffectFactory[**FP, **RP, RR](
		factory: Callable[FP, Callable[RP, RR]],
		sideEffect: Callable[[], Any],
	) -> Callable[FP, Callable[RP, RR]]:
		def outer(*args: FP.args, **kwargs: FP.kwargs) -> Callable[RP, RR]:
			orig = factory(*args, **kwargs)

			def inner(*args: RP.args, **kwargs: RP.kwargs) -> RR:
				res = orig(*args, **kwargs)
				sideEffect()
				return res

			return inner

		return outer

	@staticmethod
	def ignorePings[T](after: int = 0) -> Callable[[rpyc.core.protocol.Connection, T], T | None]:
		pingNum = 0

		def handlePing[T](self: rpyc.core.protocol.Connection, data: T) -> T | None:
			nonlocal pingNum
			if pingNum < after:
				pingNum += 1
				return data
			return None

		return handlePing

	def makeBody[T](
		self,
		pingHandler: Callable[[rpyc.core.protocol.Connection, T], Any],
	) -> Callable[[Connection], None]:
		self.release = threading.Event()
		self.addCleanup(self.release.set)

		def body(conn: Connection) -> None:
			conn._conn._HANDLERS[rpyc.core.consts.HANDLE_PING] = pingHandler
			entrypoint._signalReadiness(conn)
			conn.bgEventLoop(daemon=True)
			self.release.wait(timeout=_TIMEOUT)

		return body

	def test_heartbeatMissesFailSession(self):
		session = AddonSession(
			ThreadHostController(run=makeHostRun(self.makeBody(self.ignorePings(after=1)), serve=False)),
			heartbeatInterval=1,
			consecutiveHeartbeatMissLimit=2,
		)
		heartbeatCondNotifyAll = session._heartbeatCond.notify_all
		heartbeatCallbackFactory = session._heartbeatCallbackFactory
		with (
			patch.object(session._heartbeatCond, "notify_all"),
			patch("time.monotonic", return_value=0) as mockMonotonic,
			patch("threading._time", new=mockMonotonic),
			patch.object(session, "_heartbeatCallbackFactory") as mockCallbackFactory,
		):

			def incAndNotify() -> None:
				mockMonotonic.return_value += 1
				with session._heartbeatCond:
					heartbeatCondNotifyAll()

			mockCallbackFactory.side_effect = self.sideEffectFactory(heartbeatCallbackFactory, incAndNotify)
			startWithin(self, session)
			print(", ".join(t.name for t in threading.enumerate()))
			self.assertTrue(waitForState(session, SessionState.FAILED))
		self.assertIn("stopped responding", session.failureReason)
		self.assertEqual(mockCallbackFactory.call_count, 3)
		print(", ".join(t.name for t in threading.enumerate()))
