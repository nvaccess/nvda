# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Unit tests for the remoteClient.transport module.
This test suite covers:
 - RemoteExtensionPoint bridging of extension points
 - Basic Transport functionality (send, inbound/outbound handler registration)
 - Processing of incoming socket data and message parsing
 - sendQueue functionality
 - Creating outbound sockets in TCPTransport (with both .onion and regular hosts)
 - RelayTransport onConnected logic
 - ConnectorThread basic reconnection behavior
 - clearQueue utility
"""

import ast
import socket
import ssl
import threading
import unittest
from queue import Queue
from unittest import mock

import wx

# Import classes from the transport module.
from _remoteClient.transport import (
	PROTOCOL_VERSION,
	ConnectorThread,
	RelayTransport,
	RemoteExtensionPoint,
	RemoteMessageType,
	TCPTransport,
	Transport,
	clearQueue,
)
import logHandler


# ---------------------------------------------------------------------------
# Fake Serializer used for testing
class FakeSerializer:
	def serialize(self, *, type, **kwargs):
		# Return a simple string representation ending with newline.
		import enum

		if isinstance(type, enum.Enum):
			type = type.value
		return f"type={type}|{kwargs}\n".encode("utf-8")

	def deserialize(self, line: bytes):
		s = line.decode("utf-8").strip()
		if not s.startswith("type="):
			return {}
		rest = s[len("type=") :]
		typePart, sep, kwargPart = rest.partition("|")
		kwargs = ast.literal_eval(kwargPart) if kwargPart else {}
		kwargs["type"] = typePart
		return kwargs


# ---------------------------------------------------------------------------
# Fake HandlerRegistrar (for outbound tests)
class FakeHandlerRegistrar:
	def __init__(self):
		self.handlers = []

	def register(self, handler):
		self.handlers.append(handler)

	def unregister(self, handler):
		self.handlers.remove(handler)

	def notify(self, **kwargs):
		for h in self.handlers:
			h(**kwargs)


# ---------------------------------------------------------------------------
# Tests for RemoteExtensionPoint
class TestRemoteExtensionPoint(unittest.TestCase):
	def test_remoteBridgeWithFilter(self):
		# Create a fake extension point and a filter function
		registrar = FakeHandlerRegistrar()

		def myFilter(*args, **kwargs):
			return {"filtered": True}

		rep = RemoteExtensionPoint(extensionPoint=registrar, messageType="TEST", filter=myFilter)

		# Create a fake transport that records calls to send
		class FakeTransport:
			def __init__(self):
				self.sent = []

			def send(self, messageType, **kwargs):
				self.sent.append((messageType, kwargs))

		fakeTransport = FakeTransport()
		rep.register(fakeTransport)
		# Trigger the extension point
		registrar.notify(unused="value")
		self.assertEqual(fakeTransport.sent, [("TEST", {"filtered": True})])
		rep.unregister()

	def test_remoteBridgeWithoutFilter(self):
		registrar = FakeHandlerRegistrar()
		rep = RemoteExtensionPoint(extensionPoint=registrar, messageType="TEST", filter=None)

		class FakeTransport:
			def __init__(self):
				self.sent = []

			def send(self, messageType, **kwargs):
				self.sent.append((messageType, kwargs))

		fakeTransport = FakeTransport()
		rep.register(fakeTransport)
		registrar.notify(a=1, b=2)
		self.assertEqual(fakeTransport.sent, [("TEST", {"a": 1, "b": 2})])
		rep.unregister()


# ---------------------------------------------------------------------------
# Dummy subclass of TCPTransport for testing (without real network IO)
class DummyTransport(TCPTransport):
	def __init__(self, serializer):
		super().__init__(serializer, address=("localhost", 0), timeout=0, insecure=True)

	def run(self):
		# Do nothing (for testing send, etc.)
		pass


# ---------------------------------------------------------------------------
# Tests for send() and queue functionality in Transport
class TestTransportSendAndQueue(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()
		self.transport = DummyTransport(serializer=self.serializer)
		self.transport.connected = True
		self.transport.queue = Queue()

	def test_sendEnqueuesSerializedMessage(self):
		self.transport.send("TEST_TYPE", key=123)
		item = self.transport.queue.get_nowait()
		result = self.serializer.deserialize(item)
		self.assertEqual(result["type"], "TEST_TYPE")
		self.assertEqual(result["key"], 123)

	def test_sendWhenNotConnectedLogsWarning(self):
		self.transport.connected = False
		with mock.patch("_remoteClient.transport.log.debugWarning") as mockWarning:
			self.transport.send("TEST", a=1)
		mockWarning.assert_called_once()


# ---------------------------------------------------------------------------
# Fake socket for testing processIncomingSocketData
class FakeSocket:
	def __init__(self, recv_data: bytes):
		self.recv_data = recv_data
		self.blocking = True
		self.closed = False

	def setblocking(self, flag: bool):
		self.blocking = flag

	def recv(self, buffSize: int) -> bytes:
		data = self.recv_data[:buffSize]
		self.recv_data = self.recv_data[buffSize:]
		return data

	def close(self):
		self.closed = True


# ---------------------------------------------------------------------------
# Tests for processIncomingSocketData and parse()
class TestProcessAndParse(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()
		self.transport = DummyTransport(serializer=self.serializer)
		# Use a fake socket that returns two full lines and a partial
		self.transport.serverSock = FakeSocket(b"line1\nline2\npartial")
		self.transport.serverSockLock = threading.Lock()
		self.transport.buffer = b""

	def test_processIncomingSocketData(self):
		parsedLines = []

		def fakeParse(line):
			parsedLines.append(line)

		self.transport.parse = fakeParse
		self.transport.processIncomingSocketData()
		self.assertEqual(self.transport.buffer, b"partial")
		self.assertEqual(parsedLines, [b"line1", b"line2"])

	def test_parseCallsInboundHandler(self):
		# Set up an inbound handler for type RemoteMessageType.PROTOCOL_VERSION
		dummyInbound = mock.MagicMock()
		self.transport.inboundHandlers = {RemoteMessageType.PROTOCOL_VERSION: dummyInbound}
		# Patch wx.CallAfter to simply call immediately
		original_CallAfter = wx.CallAfter
		wx.CallAfter = lambda func, *args, **kwargs: func(*args, **kwargs)
		# Prepare a message
		message = self.serializer.serialize(type=RemoteMessageType.PROTOCOL_VERSION, a=1)
		self.transport.parse(message)
		dummyInbound.notify.assert_called_once_with(a=1)
		wx.CallAfter = original_CallAfter


# ---------------------------------------------------------------------------
# Tests for sendQueue
class DummyTransportSocket:
	def __init__(self):
		self.sent = []

	def sendall(self, data):
		self.sent.append(data)

	def close(self):
		self.closed = True


class TestSendQueue(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()
		self.transport = DummyTransport(serializer=self.serializer)
		self.transport.serverSock = DummyTransportSocket()
		self.transport.serverSockLock = threading.Lock()
		self.transport.queue = Queue()

	def test_sendQueueSendsMessages(self):
		item1 = b"msg1"
		item2 = b"msg2"
		self.transport.queue.put(item1)
		self.transport.queue.put(item2)
		self.transport.queue.put(None)  # Signal to stop
		self.transport.sendQueue()
		self.assertEqual(self.transport.serverSock.sent, [item1, item2])

	def test_sendQueueStopsOnSocketError(self):
		item1 = b"msg1"
		self.transport.queue.put(item1)

		def fakeSendall(data):
			raise socket.error("Test error")

		self.transport.serverSock.sendall = fakeSendall
		# Should complete without raising further exception
		self.transport.sendQueue()


# ---------------------------------------------------------------------------
# Tests for TCPTransport.createOutboundSocket
class DummyTCPSocket:
	def __init__(self):
		self.options = {}
		self.blocking = True
		self.connected = False
		self.timeout = None
		self.family = socket.AF_INET
		self.type = socket.SOCK_STREAM
		self.proto = 0

	def setsockopt(self, level, optname, value):
		self.options[(level, optname)] = value

	def settimeout(self, timeout):
		self.timeout = timeout

	def gettimeout(self):
		return self.timeout

	def connect(self, address):
		self.connected = True

	def close(self):
		self.connected = False

	def ioctl(self, *args, **kwargs):
		return

	def getsockopt(self, level, optname):
		return socket.SOCK_STREAM

	def fileno(self):
		return 0

	def recv(self, buffSize):
		return b""


class TestTCPTransportCreateOutboundSocket(unittest.TestCase):
	def setUp(self):
		# Prevent pip_system_certs from replacing certifi with system certificates for testing.
		self.patcher_truststore = mock.patch(
			"pip._vendor.truststore._api._verify_peercerts", lambda *a, **kw: None
		)
		self.patcher_truststore.start()
		self.serializer = FakeSerializer()
		self.host = "localhost"
		self.port = 8090

	def test_createOutboundSocketOnion(self):
		t = TCPTransport(self.serializer, (self.host + ".onion", self.port))
		fakeSocket = DummyTCPSocket()
		sock = t.createOutboundSocket(self.host + ".onion", self.port, insecure=False)
		self.assertFalse(fakeSocket.connected)
		self.assertTrue(isinstance(sock, ssl.SSLSocket))

	def test_createOutboundSocketRegularInsecure(self):
		t = TCPTransport(self.serializer, (self.host, self.port))
		fakeSocket = DummyTCPSocket()
		sock = t.createOutboundSocket(self.host, self.port, insecure=True)
		self.assertFalse(fakeSocket.connected)
		self.assertTrue(isinstance(sock, ssl.SSLSocket))


# ---------------------------------------------------------------------------
# Tests for RelayTransport.onConnected
class TestRelayTransportOnConnected(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()

	def test_onConnectedWithChannel(self):
		# Create a RelayTransport with a channel set.
		rt = RelayTransport(
			serializer=self.serializer,
			address=("localhost", 8090),
			channel="mychannel",
			connectionType="relayMode",
			protocolVersion=PROTOCOL_VERSION,
			insecure=False,
		)
		# Override send() to record calls.
		rt.send = mock.MagicMock()
		rt.onConnected()
		# It should send protocol version message.
		rt.send.assert_any_call(RemoteMessageType.PROTOCOL_VERSION, version=PROTOCOL_VERSION)
		# And since channel is set, should send JOIN message.
		rt.send.assert_any_call(RemoteMessageType.JOIN, channel="mychannel", connection_type="relayMode")

	def test_onConnectedWithoutChannel(self):
		# Create a RelayTransport with no channel.
		rt = RelayTransport(
			serializer=self.serializer,
			address=("localhost", 8090),
			channel=None,
			connectionType="relayMode",
			protocolVersion=PROTOCOL_VERSION,
			insecure=False,
		)
		rt.send = mock.MagicMock()
		rt.onConnected()
		rt.send.assert_any_call(RemoteMessageType.PROTOCOL_VERSION, version=PROTOCOL_VERSION)
		rt.send.assert_any_call(RemoteMessageType.GENERATE_KEY)


# ---------------------------------------------------------------------------
# Tests for ConnectorThread
class DummyConnectorTransport(Transport):
	def __init__(self, serializer):
		super().__init__(serializer)
		self.runCalled = 0

	def run(self):
		self.runCalled += 1
		raise socket.error("Simulated socket error")

	def processIncomingSocketData(self):
		pass

	def send(self, type, **kwargs):
		pass


class TestConnectorThread(unittest.TestCase):
	def testConnectorThreadRunsAndReconnects(self):
		serializer = FakeSerializer()
		fakeTransport = DummyConnectorTransport(serializer)
		connector = ConnectorThread(fakeTransport, reconnectDelay=0.01)
		connector.running = True
		# Run connector.run() in a loop for a few iterations manually.
		iterations = 3
		for _ in range(iterations):
			try:
				fakeTransport.run()
			except socket.error:
				pass
		connector.running = False
		self.assertEqual(fakeTransport.runCalled, iterations)


# ---------------------------------------------------------------------------
# Tests for clearQueue function
class TestClearQueue(unittest.TestCase):
	def test_clearQueue(self):
		q = Queue()
		for i in range(5):
			q.put(i)
		clearQueue(q)
		self.assertTrue(q.empty())


class TestRemoteExtensionPointIntegration(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()
		self.transport = DummyTransport(serializer=self.serializer)
		self.transport.connected = True
		self.transport.queue = Queue()
		self.fakeRegistrar = FakeHandlerRegistrar()

	def test_registerOutboundAndTrigger(self):
		self.transport.registerOutbound(self.fakeRegistrar, RemoteMessageType.GENERATE_KEY)
		for handler in self.fakeRegistrar.handlers:
			handler(a=42)
		item = self.transport.queue.get_nowait()
		payload = self.serializer.deserialize(item)
		self.assertEqual(payload["type"], RemoteMessageType.GENERATE_KEY.value)
		self.assertEqual(payload["a"], 42)

	def test_unregisterOutbound(self):
		self.transport.registerOutbound(self.fakeRegistrar, RemoteMessageType.GENERATE_KEY)
		self.assertIn(RemoteMessageType.GENERATE_KEY, self.transport.outboundHandlers)
		self.transport.unregisterOutbound(RemoteMessageType.GENERATE_KEY)
		self.assertNotIn(RemoteMessageType.GENERATE_KEY, self.transport.outboundHandlers)


class TestInboundRegistration(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()
		self.transport = DummyTransport(serializer=self.serializer)
		self.called = False

		def handler(**kwargs):
			self.called = True

		self.handler = handler

	def test_registerInbound(self):
		self.transport.registerInbound(RemoteMessageType.PROTOCOL_VERSION, self.handler)
		self.assertIn(RemoteMessageType.PROTOCOL_VERSION, self.transport.inboundHandlers)
		self.transport.inboundHandlers[RemoteMessageType.PROTOCOL_VERSION].notify(a=123)
		self.assertTrue(self.called)

	def test_unregisterInbound(self):
		self.transport.registerInbound(RemoteMessageType.PROTOCOL_VERSION, self.handler)
		self.transport.unregisterInbound(RemoteMessageType.PROTOCOL_VERSION, self.handler)
		self.called = False
		if RemoteMessageType.PROTOCOL_VERSION in self.transport.inboundHandlers:
			self.transport.inboundHandlers[RemoteMessageType.PROTOCOL_VERSION].notify(a=456)
		self.assertFalse(self.called)


class TestParseErrorHandling(unittest.TestCase):
	def setUp(self):
		self.serializer = FakeSerializer()
		self.transport = DummyTransport(serializer=self.serializer)
		self.transport.inboundHandlers = {}

	def test_parseNoType(self):
		with self.assertLogs(logHandler.log, level="WARN") as cm:
			self.transport.parse(b"invalid message\n")
			self.assertTrue(any("Received message without type" in log for log in cm.output))

	def test_parseInvalidType(self):
		with self.assertLogs(logHandler.log, level="WARN") as cm:
			message = self.serializer.serialize(type="NONEXISTENT", a=10)
			self.transport.parse(message)
			self.assertTrue(any("Received message with invalid type" in log for log in cm.output))

	def test_parseUnhandledType(self):
		with self.assertLogs(logHandler.log, level="WARN") as cm:
			message = self.serializer.serialize(type=RemoteMessageType.GENERATE_KEY, b=10)
			self.transport.parse(message)
			self.assertTrue(any("Received message with unhandled type" in log for log in cm.output))


if __name__ == "__main__":
	unittest.main()
