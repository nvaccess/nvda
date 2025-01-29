# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2025 NV Access Limited, Christopher Toth, Tyler Spivey, Babbage B.V., David Sexton and others.
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
Bridge Transport Module
======================

This module provides functionality to bridge two NVDA Remote transports together,
enabling bidirectional message passing between two transport instances while
handling message filtering and routing.

The bridge acts as an intermediary layer that:
- Connects two transport instances
- Routes messages between them
- Filters out specific message types that shouldn't be forwarded
- Manages the lifecycle of message handlers

Example:
	>>> transport1 = TCPTransport(serializer, addr1)
	>>> transport2 = TCPTransport(serializer, addr2)
	>>> bridge = BridgeTransport(transport1, transport2)
	# Messages will now flow between transport1 and transport2
	>>> bridge.disconnect()  # Clean up when done
"""

from typing import Dict, Set

from .protocol import RemoteMessageType
from .transport import Transport


class BridgeTransport:
	"""A bridge between two NVDA Remote transport instances.

	This class creates a bidirectional bridge between two Transport instances,
	allowing them to exchange messages while providing message filtering capabilities.
	It automatically sets up message handlers for all RemoteMessageTypes and manages
	their lifecycle.

	Attributes:
		excluded (Set[RemoteMessageType]): Message types that should not be forwarded between transports.
			By default includes connection management messages that should remain local.
		t1 (Transport): First transport instance to bridge
		t2 (Transport): Second transport instance to bridge
		t1_callbacks (Dict[RemoteMessageType, callable]): Storage for t1's message handlers
		t2_callbacks (Dict[RemoteMessageType, callable]): Storage for t2's message handlers
	"""

	excluded: Set[RemoteMessageType] = {
		RemoteMessageType.CLIENT_JOINED,
		RemoteMessageType.CLIENT_LEFT,
		RemoteMessageType.CHANNEL_JOINED,
		RemoteMessageType.SET_BRAILLE_INFO,
	}

	def __init__(self, t1: Transport, t2: Transport) -> None:
		"""Initialize the bridge between two transports.

		Sets up message routing between the two provided transport instances
		by registering handlers for all possible message types.

		Args:
			t1 (Transport): First transport instance to bridge
			t2 (Transport): Second transport instance to bridge
		"""
		self.t1 = t1
		self.t2 = t2
		# Store callbacks for each message type
		self.t1Callbacks: Dict[RemoteMessageType, callable] = {}
		self.t2Callbacks: Dict[RemoteMessageType, callable] = {}

		for messageType in RemoteMessageType:
			# Create and store callbacks
			self.t1Callbacks[messageType] = self.makeCallback(self.t1, messageType)
			self.t2Callbacks[messageType] = self.makeCallback(self.t2, messageType)
			# Register with stored references
			t1.registerInbound(messageType, self.t2Callbacks[messageType])
			t2.registerInbound(messageType, self.t1Callbacks[messageType])

	def makeCallback(self, targetTransport: Transport, messageType: RemoteMessageType):
		"""Create a callback function for handling a specific message type.

		Creates a closure that will forward messages of the specified type
		to the target transport, unless the message type is in the excluded set.

		Args:
			targetTransport (Transport): Transport instance to forward messages to
			messageType (RemoteMessageType): Type of message this callback will handle

		Returns:
			callable: A callback function that forwards messages to the target transport
		"""

		def callback(*args, **kwargs):
			if messageType not in self.excluded:
				targetTransport.send(messageType, *args, **kwargs)

		return callback

	def disconnect(self):
		"""Disconnect the bridge and clean up all message handlers.

		Unregisters all message handlers from both transports that were set up
		during bridge initialization. This should be called before disposing of
		the bridge to prevent memory leaks and ensure proper cleanup.
		"""
		for messageType in RemoteMessageType:
			self.t1.unregisterInbound(messageType, self.t2Callbacks[messageType])
			self.t2.unregisterInbound(messageType, self.t1Callbacks[messageType])
