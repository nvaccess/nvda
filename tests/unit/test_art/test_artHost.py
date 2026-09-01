# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the ART host entry point, root services, and host controllers."""

import io
import msvcrt
import os
import pathlib
import subprocess
import sys
import threading
import unittest
from unittest.mock import MagicMock, patch

import globalVars
from _art.exceptions import CapabilityDeniedError, CapabilityUnavailableError, PermissionNotGrantedError
from _art.host.entrypoint import CONTROL_CONNECTION_NAME
from _art.host.rootService import HostRootService
from _art.session.hostController import (
	HostController,
	SubprocessHostController,
	claimProcessControlStream,
)
from _art.session.rootService import CoreRootService
from _art.transport import Connection
from _art.winHandles import claimHandleFromDescriptor
from rpyc.core.stream import PipeStream

from .threadHostController import ThreadHostController

#: Bound on anything involving a real process, in seconds.
_PROCESS_TIMEOUT: float = 30.0


def getProbePath(filename: str) -> str:
	return str(pathlib.Path(__file__).parent / "probes" / filename)


class TestRootServices(unittest.TestCase):
	"""Exercise both root services over an in-process pipe pair.

	The transport is identical whether or not a process is involved, so the contracts themselves
	are cheapest to test without one.
	"""

	def setUp(self):
		coreStream, hostStream = PipeStream.create_pair()
		self.coreService = CoreRootService()
		self.hostService = HostRootService()
		self.coreConn = Connection(coreStream, self.coreService, name="test core")
		self.hostConn = Connection(hostStream, self.hostService, name="test host")
		self.coreConn.bgEventLoop(daemon=True)
		self.hostConn.bgEventLoop(daemon=True)

	def tearDown(self):
		self.hostConn.close()
		self.coreConn.close()

	def test_corePingsHost(self):
		"""Core can confirm the host is serving."""
		self.assertEqual(self.coreConn.remoteService.ping(), "pong")

	def test_hostPingsCore(self):
		"""The host can confirm core is serving, over the same connection."""
		self.assertEqual(self.hostConn.remoteService.ping(), "pong")

	def test_hostReachesCoreThroughItsRootService(self):
		"""Host-side code reaches core via ``HostRootService.coreRoot``.

		This is the route every capability request will take, so it is worth proving that the
		connection captured in ``on_connect`` resolves to core's root.
		"""
		self.assertEqual(self.hostService.coreRoot.ping(), "pong")

	def test_coreRootIsNotExposedAcrossTheBoundary(self):
		"""``coreRoot`` is for host-side code only; core must not reach it back over the wire."""
		with self.assertRaises(AttributeError):
			_ = self.coreConn.remoteService.coreRoot

	def test_loadComponentIsNotImplementedYet(self):
		"""Component loading refuses clearly until there is a manifest to drive it."""
		with self.assertRaises(NotImplementedError):
			self.coreConn.remoteService.loadComponent("someFeature")

	def test_requestCapabilityIsDeniedByDefault(self):
		"""Nothing is granted until there is a broker; denial is the safe default."""
		with self.assertRaises(PermissionNotGrantedError):
			self.hostConn.remoteService.requestCapability("audio")

	def test_capabilityErrorsKeepTheirTypeAcrossTheBoundary(self):
		"""An add-on can catch a denial by its base class, not just its exact type.

		The failure taxonomy exists to be caught across the boundary, which only works while
		``instantiate_custom_exceptions`` is set. Without it rpyc rebuilds remote exceptions as
		opaque stand-ins that keep the name and nothing else, and every ``except`` clause below
		stops matching while the tests that assert on exact types keep passing.

		This runs in-process, so the taxonomy is already resident and rpyc can always find the real classes.
		:class:`TestExceptionTaxonomyAcrossProcess` ensures that the taxonomy is imported by the host entry point.
		"""
		with self.assertRaises(CapabilityDeniedError):
			self.hostConn.remoteService.requestCapability("audio")
		with self.assertRaises(CapabilityUnavailableError):
			self.hostConn.remoteService.requestCapability("audio")


class HostControllerConformanceMixin:
	"""Behaviour every :class:`HostController` implementation must exhibit.

	Written once and run against both implementations, because conformance to a single protocol is
	the entire point of the seam.
	Not a ``TestCase`` itself, so it is not collected on its own.
	"""

	def makeController(self) -> HostController:
		"""Build the controller under test."""
		raise NotImplementedError

	def setUp(self):
		self.controller = self.makeController()
		self.addCleanup(self.controller.terminate)
		self.conn: Connection | None = None

	def startHost(self) -> Connection:
		"""Start the host and return core's control connection."""
		stream = self.controller.start()
		self.conn = Connection(stream, CoreRootService(), name="test core control")
		self.addCleanup(self.conn.close)
		self.conn.bgEventLoop(daemon=True)
		return self.conn

	def test_pingRoundTrip(self):
		"""A host started by this controller answers a ping."""
		conn = self.startHost()
		self.assertEqual(conn.remoteService.ping(), "pong")

	def test_pollBeforeStartIsRefused(self):
		"""Polling a host that was never started is an error, not a silent ``None``."""
		with self.assertRaises(RuntimeError):
			self.controller.poll()

	def test_waitBeforeStartIsRefused(self):
		"""Waiting on a host that was never started is an error, not a silent ``None``."""
		with self.assertRaises(RuntimeError):
			self.controller.wait(_PROCESS_TIMEOUT)

	def test_pollIsNoneWhileTheHostRuns(self):
		"""A running host has no exit status yet."""
		conn = self.startHost()
		# Ping first, so we know the host is genuinely up rather than merely not yet started.
		self.assertEqual(conn.remoteService.ping(), "pong")
		self.assertIsNone(self.controller.poll())

	def test_terminateStopsTheHost(self):
		"""After ``terminate``, the host finishes and reports an exit status."""
		conn = self.startHost()
		self.assertEqual(conn.remoteService.ping(), "pong")
		self.controller.terminate()
		self.assertIsNotNone(self.controller.wait(_PROCESS_TIMEOUT))
		self.assertIsNotNone(self.controller.poll())

	def test_terminateIsSafeOnAStoppedHost(self):
		"""Terminating twice is not an error."""
		self.startHost()
		self.controller.terminate()
		self.controller.wait(_PROCESS_TIMEOUT)
		self.controller.terminate()

	def test_startingTwiceIsRefused(self):
		"""A controller drives one host, not a series of them."""
		self.startHost()
		with self.assertRaises(RuntimeError):
			self.controller.start()


class TestThreadHostController(HostControllerConformanceMixin, unittest.TestCase):
	"""The thread-backed fake, which is the default substrate for tests."""

	def makeController(self) -> HostController:
		return ThreadHostController()

	def test_createPipePairGivesTwoUsableEnds(self):
		"""A dependent connection can be built over the pair, in this process."""
		self.startHost()
		coreEnd, hostEnd = self.controller.createPipePair()
		self.assertIsNotNone(coreEnd)
		self.assertIsNotNone(hostEnd)
		coreEnd.close()
		hostEnd.close()


class TestSubprocessHostController(HostControllerConformanceMixin, unittest.TestCase):
	"""The real implementation, driving a genuine child process.

	These are the tests a thread cannot stand in for.
	"""

	def makeController(self) -> HostController:
		return SubprocessHostController()

	def test_hostRunsInADifferentProcess(self):
		"""The ping is answered by another process, not this one."""
		self.startHost()
		self.assertIsNotNone(self.controller._process)
		self.assertNotEqual(self.controller._process.pid, os.getpid())

	def test_createPipePairRequiresARunningHost(self):
		"""There is nothing to duplicate handles into before the host starts."""
		with self.assertRaises(RuntimeError):
			self.controller.createPipePair()

	def test_createPipePairDuplicatesHandlesIntoTheHost(self):
		"""Core gets a stream, and the host gets two handle values valid in its own process.

		The host does not consume these until dependent connections exist, so this checks only
		that the ends are manufactured, not that traffic flows over them.
		"""
		self.startHost()
		coreEnd, hostEnd = self.controller.createPipePair()
		readHandle, writeHandle = hostEnd
		self.assertIsInstance(readHandle, int)
		self.assertIsInstance(writeHandle, int)
		self.assertNotEqual(readHandle, 0)
		self.assertNotEqual(writeHandle, 0)
		coreEnd.close()

	def test_stderrIsForwardedToTheLog(self):
		"""Whatever the host writes to standard error is surfaced in NVDA's log.

		Leaving the host's standard error unconnected is what makes an unhandled traceback vanish
		in the 32-bit synth driver host; this is the drain that stops that happening here.
		"""
		stderr = io.BytesIO(b"Traceback (most recent call last):\nValueError: boom\n")
		with patch("_art.session.hostController.log", new=MagicMock()) as mockLog:
			SubprocessHostController._drainStderr(stderr)
		logged = " ".join(str(call) for call in mockLog.warning.call_args_list)
		self.assertIn("ValueError: boom", logged)
		self.assertIn("Traceback", logged)

	def test_drainSurvivesUndecodableOutput(self):
		"""A host writing non-UTF-8 bytes must not kill the drain thread."""
		stderr = io.BytesIO(b"\xff\xfe not valid utf-8\n")
		with patch("_art.session.hostController.log", new=MagicMock()) as mockLog:
			SubprocessHostController._drainStderr(stderr)
		self.assertTrue(mockLog.warning.called)


class TestHostStandardStreams(unittest.TestCase):
	"""The entry point's defence of the control connection, and its diagnostic channel."""

	def test_strayStdoutDoesNotCorruptTheControlStream(self):
		"""Output written to standard output after boot must not reach the wire.

		The control connection is carried on the host's standard output, so a stray ``print`` is
		enough to desynchronise rpyc's framing. The entry point folds standard output into
		standard error to prevent exactly this, and this is the test that says so.
		"""
		script = (
			"import _art.host.entrypoint as entrypoint\n"
			"stream = entrypoint._claimControlStream()\n"
			"print('stray stdout that would otherwise corrupt the wire')\n"
			"entrypoint.run(stream)\n"
		)
		process = subprocess.Popen(
			[sys.executable, "-c", script],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.DEVNULL,  # We don't care, and a pipe buffer could fill and block
			cwd=globalVars.appDir,
			creationflags=subprocess.CREATE_NO_WINDOW,
		)
		self.addCleanup(process.wait)
		self.addCleanup(process.kill)
		conn = Connection(
			claimProcessControlStream(process),
			CoreRootService(),
			name=f"test {CONTROL_CONNECTION_NAME}",
		)
		self.addCleanup(conn.close)
		conn.bgEventLoop(daemon=True)
		# If the print had reached the wire, this would fail to deserialize rather than answer.
		self.assertEqual(conn.remoteService.ping(), "pong")


class TestControlStreamHandleOwnership(unittest.TestCase):
	"""Exactly one owner of each handle carrying the control connection.

	``PipeStream`` closes the handles it is built from.
	Anything that owns them as well -- a C runtime descriptor, or a Python file object over one --
	closes them a second time.
	Since Windows recycles handle values, that second close may land on an unrelated object rather
	than failing, so these tests assert on ownership rather than on an error.
	"""

	def test_claimingADescriptorLeavesOneOwner(self):
		"""The descriptor is released, and its handle survives for the caller to use."""
		readFd, writeFd = os.pipe()
		self.addCleanup(os.close, writeFd)
		handle = claimHandleFromDescriptor(readFd)
		with self.assertRaises(OSError):
			# The descriptor is gone, so it cannot close the handle a second time.
			os.fstat(readFd)
		# Ownership moved, rather than the object dying with the descriptor.
		message = b"still open"
		os.write(writeFd, message)
		claimed = msvcrt.open_osfhandle(handle, os.O_RDONLY)
		self.addCleanup(os.close, claimed)
		self.assertEqual(os.read(claimed, len(message)), message)

	def test_bootReleasesTheDescriptorsItDuplicates(self):
		"""``_claimControlStream`` gives its descriptors to the stream and keeps none back.

		Reading a handle out of a descriptor does not transfer ownership.
		A descriptor left behind holds a second claim, which the system closes at process
		teardown, long after the stream has closed the handle.

		The check runs in a child process, since ``_claimControlStream`` takes over the standard
		streams of whichever process calls it.
		"""
		process = subprocess.Popen(
			[sys.executable, getProbePath("controlStream.py")],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			cwd=globalVars.appDir,
			creationflags=subprocess.CREATE_NO_WINDOW,
		)
		self.addCleanup(process.kill)
		_stdout, stderr = process.communicate(timeout=_PROCESS_TIMEOUT)
		self.assertEqual(
			process.returncode,
			0,
			f"Host boot kept a claim on its control descriptors: {stderr.decode(errors='replace')}",
		)


class TestExceptionTaxonomyAcrossProcess(unittest.TestCase):
	"""An ART exception keeps its type when it crosses into a real, freshly booted host.

	``rpyc`` rebuilds a remote exception as its real class
	only when that class's module is resident in the receiving process.
	A host process does not import :mod:`_art.exceptions` just by booting,
	so unless the transport makes the taxonomy resident, a denial raised by core arrives at the host as a ``GenericException`` subclass.
	The check runs in a child process that deliberately avoids importing the taxonomy before the boundary call.
	"""

	def test_deniedCapabilityArrivesAsItsRealClass(self):
		"""A denial raised by core is catchable by its taxonomy classes in a fresh host."""
		process = subprocess.Popen(
			[sys.executable, getProbePath("exceptionTaxonomy.py")],
			stdin=subprocess.PIPE,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			cwd=globalVars.appDir,
			creationflags=subprocess.CREATE_NO_WINDOW,
		)
		self.addCleanup(process.stderr.close)
		self.addCleanup(process.kill)
		conn = Connection(
			claimProcessControlStream(process),
			CoreRootService(),
			name=f"test {CONTROL_CONNECTION_NAME}",
		)
		self.addCleanup(conn.close)
		conn.bgEventLoop(daemon=True)
		try:
			process.wait(timeout=_PROCESS_TIMEOUT)
		except subprocess.TimeoutExpired:
			process.kill()
			raise
		# The probe writes a short diagnostic and never fills the pipe, so reading after it exits
		# cannot deadlock.
		diagnostic = process.stderr.read().decode(errors="replace")
		self.assertEqual(
			process.returncode,
			0,
			f"A denial raised by core reached the host as the wrong type: {diagnostic}",
		)


class TestHostLoggingIsolation(unittest.TestCase):
	"""The host process logs without importing NVDA core.

	Shared transport code logs through :mod:`_art._log`, which resolves to NVDA's ``log`` in core
	but to a stdlib logger in the host, so the host never imports ``logHandler`` (and core with it).
	The choice is made once, at import time, from the host marker,
	so it can only be observed in a process that boots as the host does.
	"""

	def test_hostDoesNotImportLogHandler(self):
		"""A host process reaches the transport without ``logHandler`` becoming resident."""
		process = subprocess.run(
			[sys.executable, getProbePath("logIsolation.py")],
			cwd=globalVars.appDir,
			creationflags=subprocess.CREATE_NO_WINDOW,
			capture_output=True,
			timeout=_PROCESS_TIMEOUT,
			check=False,
		)
		diagnostic = process.stderr.decode(errors="replace")
		self.assertEqual(
			process.returncode,
			0,
			f"The host did not stay isolated from core: {diagnostic}",
		)


class TestHostRootServiceDisconnect(unittest.TestCase):
	"""The host root service cleans up when core drops the control connection."""

	def test_onDisconnectClearsConnectionAndTerminates(self):
		"""After ``on_disconnect``, ``coreRoot`` is unavailable again and the service is terminated."""
		service = HostRootService()
		conn = MagicMock()
		service.on_connect(conn)
		# Sanity: while connected, coreRoot reaches core through the connection.
		self.assertIs(service.coreRoot, conn.root)

		service.on_disconnect(conn)

		self.assertTrue(service.terminated)
		with self.assertRaises(RuntimeError):
			_ = service.coreRoot


class TestThreadHostControllerFailureReporting(unittest.TestCase):
	"""The thread-backed controller must not report a crashed host thread as a clean exit."""

	def test_finishedThreadWithoutAStatusIsAFailure(self):
		"""A finished host thread that recorded no status died abnormally; poll reports failure, not 0."""
		controller = ThreadHostController()
		finished = threading.Thread(target=lambda: None)
		finished.start()
		finished.join()
		# Stand in for ``_run`` dying from a ``BaseException`` its ``except Exception`` did not catch:
		# the thread is finished, but no exit status was recorded.
		controller._thread = finished
		controller._exitStatus = None

		self.assertIsNotNone(controller.poll())
		self.assertNotEqual(controller.poll(), 0)
