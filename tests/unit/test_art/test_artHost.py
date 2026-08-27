# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the ART host entry point, root services, and host controllers."""

import unittest

from rpyc.core.stream import PipeStream

from _art.exceptions import CapabilityDeniedError, CapabilityUnavailableError, PermissionNotGrantedError
from _art.host.rootService import HostRootService
from _art.session.hostController import (
	HostController,
)
from _art.session.rootService import CoreRootService
from _art.transport import Connection
from .threadHostController import ThreadHostController


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

	def test_satisfiesTheProtocol(self):
		"""The implementation is recognisable as a ``HostController``."""
		self.assertIsInstance(self.controller, HostController)

	def test_pingRoundTrip(self):
		"""A host started by this controller answers a ping."""
		conn = self.startHost()
		self.assertEqual(conn.remoteService.ping(), "pong")

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
		self.controller.wait(10)
		self.assertIsNotNone(self.controller.poll())

	def test_terminateIsSafeOnAStoppedHost(self):
		"""Terminating twice is not an error."""
		self.startHost()
		self.controller.terminate()
		self.controller.wait(10)
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
