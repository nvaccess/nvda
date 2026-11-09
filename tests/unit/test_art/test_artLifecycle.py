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
from unittest.mock import MagicMock

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
_TIMEOUT: float = 30.0
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


class TestChildExitDetectionProcessConformance(unittest.TestCase):
	"""Exit detection against real host processes, which can die in ways a thread cannot."""

	def makeSession(self, *command: str, **kwargs) -> AddonSession:
		self.controller = SubprocessHostController(command=fakeHostCommand("exitDetection.py", *command))
		session = AddonSession(self.controller, **kwargs)
		self.addCleanup(session.stop)
		return session

	@unittest.expectedFailure
	def test_hostDyingAfterReadyIsDetected(self):
		"""A host process that dies abruptly closes its pipe, and core records how it died."""
		session = self.makeSession("instrumented")
		startWithin(self, session)
		rpyc.async_(session.hostRoot._crash)(3)
		self.assertTrue(session.waitForState(SessionState.FAILED, timeout=_TIMEOUT))
		self.assertIs(session.state, SessionState.FAILED)
		self.assertEqual(session.exitStatus, 3)
		self.assertIn("status 3", session.failureReason)

	@unittest.expectedFailure
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

	def test_lingeringHostIsStopped(self):
		"""A host process that closes its pipe but keeps running is stopped, rather than left behind."""
		session = self.makeSession("closeAndLinger", exitConfirmGrace=_SHORT_GRACE)
		with self.assertRaises(HostLaunchError):
			startWithin(self, session)
		self.assertIn("did not exit", session.failureReason)
		self.assertIsNotNone(self.controller.wait(_TIMEOUT))
