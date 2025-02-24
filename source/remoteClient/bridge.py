# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Bridge Transport Module.

Provides functionality to bridge two NVDA Remote transports together,
enabling bidirectional message passing with filtering and routing.

:param transport1: First transport instance to bridge
:param transport2: Second transport instance to bridge

The bridge acts as an intermediary layer that:
* Connects two transport instances
* Routes messages between them
* Filters out specific message types
* Manages message handler lifecycle

Example::

    transport1 = TCPTransport(serializer, addr1)
    transport2 = TCPTransport(serializer, addr2)
    bridge = BridgeTransport(transport1, transport2)
    # Messages will now flow between transport1 and transport2
    bridge.disconnect()  # Clean up when done
"""

from collections.abc import Callable
from .protocol import RemoteMessageType
from .transport import Transport

_CallbackT = Callable[..., None]


class BridgeTransport:
	"""A bridge between two NVDA Remote transport instances.

	Creates a bidirectional bridge between two Transport instances,
	allowing them to exchange messages while providing message filtering capabilities.
	Automatically sets up message handlers for all RemoteMessageTypes and manages
	their lifecycle.
	"""

	excluded: set[RemoteMessageType] = {
		RemoteMessageType.CLIENT_JOINED,
		RemoteMessageType.CLIENT_LEFT,
		RemoteMessageType.CHANNEL_JOINED,
		RemoteMessageType.SET_BRAILLE_INFO,
	}
	"""Message types that should not be forwarded between transports
	By default includes connection management messages that should remain local.
	"""

	t1: Transport
	"""First transport instance to bridge"""

	t2: Transport
	"""Second transport instance to bridge"""

	t1Callbacks: dict[RemoteMessageType, _CallbackT]
	"""Storage for t1's message handlers"""

	t2Callbacks: dict[RemoteMessageType, _CallbackT]
	"""Storage for t2's message handlers"""

	def __init__(self, t1: Transport, t2: Transport) -> None:
		"""Initialize the bridge between two transports.

		Sets up message routing between the two provided transport instances
		by registering handlers for all possible message types.

		:param t1: First transport instance to bridge
		:param t2: Second transport instance to bridge
		"""
		self.t1 = t1
		self.t2 = t2
		# Store callbacks for each message type
		self.t1Callbacks = {}
		self.t2Callbacks = {}

		for messageType in RemoteMessageType:
			# Create and store callbacks
			self.t1Callbacks[messageType] = self.makeCallback(self.t1, messageType)
			self.t2Callbacks[messageType] = self.makeCallback(self.t2, messageType)
			# Register with stored references
			t1.registerInbound(messageType, self.t2Callbacks[messageType])
			t2.registerInbound(messageType, self.t1Callbacks[messageType])

	def makeCallback(self, targetTransport: Transport, messageType: RemoteMessageType) -> _CallbackT:
		"""Create a callback function for handling a specific message type.

		:param targetTransport: Transport instance to forward messages to
		:param messageType: Type of message this callback will handle
		:return: A callback function that forwards messages to the target transport
		:note: Creates a closure that forwards messages unless the type is excluded
		"""

		def callback(*args, **kwargs) -> None:
			if messageType not in self.excluded:
				targetTransport.send(messageType, *args, **kwargs)

		return callback

	def disconnect(self):
		"""Disconnect the bridge and clean up all message handlers.

		:note: Unregisters all message handlers from both transports.
		    Should be called before disposal to prevent memory leaks.
		"""
		for messageType in RemoteMessageType:
			self.t1.unregisterInbound(messageType, self.t2Callbacks[messageType])
			self.t2.unregisterInbound(messageType, self.t1Callbacks[messageType])
