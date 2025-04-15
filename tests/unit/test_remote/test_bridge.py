# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import unittest
from _remoteClient.bridge import BridgeTransport
from _remoteClient.transport import Transport, RemoteMessageType


# A fake transport that implements minimal Transport interface for testing BridgeTransport.
class FakeTransport(Transport):
	def __init__(self):
		class DummySerializer:
			def serialize(self, *, type, **kwargs):
				return b"dummy"

			def deserialize(self, data):
				return {}

		super().__init__(DummySerializer())
		# Override inboundHandlers to be a dict mapping RemoteMessageType -> list of handlers.
		self.inboundHandlers = {}
		# List to collect sent messages.
		self.sentMessages = []

	def registerInbound(self, messageType, handler):
		if messageType in self.inboundHandlers:
			self.inboundHandlers[messageType].append(handler)
		else:
			self.inboundHandlers[messageType] = [handler]

	def unregisterInbound(self, messageType, handler):
		if messageType in self.inboundHandlers:
			self.inboundHandlers[messageType].remove(handler)
			if not self.inboundHandlers[messageType]:
				del self.inboundHandlers[messageType]

	def send(self, type, **kwargs):
		self.sentMessages.append((type, kwargs))

	def parse(self, line: bytes):
		pass  # Not used in these tests.

	def run(self):
		pass


# Tests for BridgeTransport.
class TestBridgeTransport(unittest.TestCase):
	def setUp(self):
		self.transport1 = FakeTransport()
		self.transport2 = FakeTransport()
		# Create a bridge between the two fake transports.
		self.bridge = BridgeTransport(self.transport1, self.transport2)

	def test_inboundRegistrationOnInit(self):
		# On initialization, both transports should have inbound handlers registered for every RemoteMessageType.
		for messageType in list(RemoteMessageType):
			self.assertIn(
				messageType,
				self.transport1.inboundHandlers,
				f"{messageType} not registered in transport1",
			)
			self.assertIn(
				messageType,
				self.transport2.inboundHandlers,
				f"{messageType} not registered in transport2",
			)

	def test_forwardingMessage(self):
		# Choose a message type that is not excluded.
		nonExcluded = None
		for m in list(RemoteMessageType):
			if m not in BridgeTransport.excluded:
				nonExcluded = m
				break
		self.assertIsNotNone(nonExcluded, "There must be at least one non-excluded message type")
		# Simulate an inbound message on transport1.
		callbacks = self.transport1.inboundHandlers[nonExcluded]
		for callback in callbacks:
			callback(a=10, b=20)
		# Expect that transport2's send() was called with the same message type and payload.
		self.assertTrue(len(self.transport2.sentMessages) > 0, "No message was forwarded to transport2")
		for typeSent, payload in self.transport2.sentMessages:
			self.assertEqual(typeSent, nonExcluded)
			self.assertEqual(payload, {"a": 10, "b": 20})

	def test_excludedMessageNotForwarded(self):
		# Choose a message type that is excluded.
		excludedMessage = None
		for m in list(RemoteMessageType):
			if m in BridgeTransport.excluded:
				excludedMessage = m
				break
		self.assertIsNotNone(excludedMessage, "There must be at least one excluded message type")
		# Clear any previous sent messages.
		self.transport2.sentMessages.clear()
		# Simulate an inbound message on transport1 for the excluded type.
		callbacks = self.transport1.inboundHandlers[excludedMessage]
		for callback in callbacks:
			callback(a=99)
		# Expect that transport2's send() is not called.
		self.assertEqual(len(self.transport2.sentMessages), 0, "Excluded message was forwarded")

	def test_disconnectUnregistersHandlers(self):
		# Count initial number of registered handlers.
		countT1 = sum(len(handlers) for handlers in self.transport1.inboundHandlers.values())
		countT2 = sum(len(handlers) for handlers in self.transport2.inboundHandlers.values())
		self.assertGreater(countT1, 0)
		self.assertGreater(countT2, 0)
		# Disconnect the bridge.
		self.bridge.disconnect()
		# After disconnection, there should be no inbound handlers remaining.
		totalT1 = sum(len(handlers) for handlers in self.transport1.inboundHandlers.values())
		totalT2 = sum(len(handlers) for handlers in self.transport2.inboundHandlers.values())
		self.assertEqual(totalT1, 0, "Still registered handlers in transport1 after disconnect")
		self.assertEqual(totalT2, 0, "Still registered handlers in transport2 after disconnect")


if __name__ == "__main__":
	unittest.main()
