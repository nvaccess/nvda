# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 NV Access Limited

"""Unit tests for the ``_art.transport`` package (the rpyc-over-pipes transport core)."""

import unittest

import rpyc
from rpyc.core.stream import PipeStream

from _art.transport import Connection, Service


@rpyc.service
class _ChildService(Service):
	@Service.exposed
	def ping(self):
		return "pong"


@rpyc.service
class _EchoService(Service):
	def __init__(self):
		super().__init__()
		self.children: list[_ChildService] = []
		self.notExposedValue = "secret"

	@Service.exposed
	def echo(self, value):
		return value

	@Service.exposed
	def applyCallback(self, callback, value):
		# The callback lives in the peer; invoking it round-trips back over the connection.
		return callback(value)

	@Service.exposed
	def makeChild(self):
		child = _ChildService()
		self.children.append(child)
		return child

	def notExposedMethod(self):
		return "should not be reachable"


class TestArtTransport(unittest.TestCase):
	"""Exercise the transport over an in-process duplex pipe pair."""

	def setUp(self):
		serverStream, clientStream = PipeStream.create_pair()
		self.serverService = _EchoService()
		self.serverConn = Connection(serverStream, self.serverService, name="test server")
		self.clientConn = Connection(clientStream, None, name="test client")
		self.serverConn.bgEventLoop(daemon=True)
		self.clientConn.bgEventLoop(daemon=True)
		self.remote = self.clientConn.remoteService

	def tearDown(self):
		self.clientConn.close()
		self.serverConn.close()

	def test_roundTrip(self):
		"""An exposed method called across the boundary returns its result."""
		self.assertEqual(self.remote.echo("hello"), "hello")
		self.assertEqual(self.remote.echo(42), 42)

	def test_bidirectionalCallback(self):
		"""A callable passed to the peer can be invoked back across the connection."""
		result = self.remote.applyCallback(lambda x: x * 2, 21)
		self.assertEqual(result, 42)

	def test_nonExposedAttributesAreBlocked(self):
		"""Only ``@Service.exposed`` members are reachable from the peer."""
		with self.assertRaises(AttributeError):
			self.remote.notExposedMethod()
		with self.assertRaises(AttributeError):
			_ = self.remote.notExposedValue

	def test_terminatedServiceRefusesCalls(self):
		"""Calls on a terminated service raise (and the exception deserializes)."""
		self.assertEqual(self.remote.echo("alive"), "alive")
		self.serverService.terminate()
		with self.assertRaises(Exception):
			self.remote.echo("dead")

	def test_dependantServiceSharesLifetime(self):
		"""A service returned over the boundary is terminated with its parent."""
		childRef = self.remote.makeChild()
		self.assertEqual(childRef.ping(), "pong")
		child = self.serverService.children[0]
		self.assertFalse(child.terminated)
		self.serverService.terminate()
		self.assertTrue(child.terminated)


if __name__ == "__main__":
	unittest.main()
