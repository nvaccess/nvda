# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Dot Incorporated, Bram Duvigneau

"""Unit tests for the dotPad braille display driver."""

import unittest
from unittest.mock import MagicMock
import struct
import functools
import operator


class TestDotPadBufferedReceive(unittest.TestCase):
	"""Tests for the buffered receive logic in the DotPad driver."""

	def setUp(self):
		"""Set up test fixtures."""
		# Import after patching to avoid hardware dependencies
		from brailleDisplayDrivers.dotPad.driver import BrailleDisplayDriver
		from brailleDisplayDrivers.dotPad.defs import (
			DP_Command,
			DP_PacketSyncByte,
			DP_CHECKSUM_BASE,
		)

		self.BrailleDisplayDriver = BrailleDisplayDriver
		self.DP_Command = DP_Command
		self.DP_PacketSyncByte = DP_PacketSyncByte
		self.DP_CHECKSUM_BASE = DP_CHECKSUM_BASE

		# Create a minimal driver instance for testing receive logic
		self.driver = MagicMock(spec=BrailleDisplayDriver)
		self.driver._receiveBuffer = bytearray()
		self.driver.MAX_PACKET_SIZE = 512
		self.driver._lastResponse = {}

		# Track processed packets
		self.processedPackets = []

		def mockProcessPacket(packetBody):
			self.processedPackets.append(bytes(packetBody))

		self.driver._processPacket = mockProcessPacket

		# Bind the actual _onReceive method
		self.driver._onReceive = BrailleDisplayDriver._onReceive.__get__(self.driver, type(self.driver))

	def _createPacket(self, dest=0, cmd=0x0101, seqNum=0, data=b""):
		"""Helper to create a valid DotPad packet.

		:param dest: Destination address
		:param cmd: Command code
		:param seqNum: Sequence number
		:param data: Packet data payload
		:return: Complete packet as bytes
		"""
		# Build packet body
		packetBody = bytearray([dest])
		packetBody.extend(struct.pack(">H", cmd))
		packetBody.append(seqNum)
		packetBody.extend(data)

		# Calculate checksum
		checksum = functools.reduce(operator.xor, packetBody, self.DP_CHECKSUM_BASE)
		packetBody.append(checksum)

		# Add header
		packet = bytearray(
			[
				self.DP_PacketSyncByte.SYNC1,
				self.DP_PacketSyncByte.SYNC2,
			],
		)
		packet.extend(struct.pack(">H", len(packetBody)))
		packet.extend(packetBody)

		return bytes(packet)

	def test_completePacketAtOnce(self):
		"""Test receiving a complete packet in a single call (BLE behavior)."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"test")

		# Receive entire packet at once
		self.driver._onReceive(packet)

		# Verify packet was processed
		self.assertEqual(len(self.processedPackets), 1)
		# Verify buffer is empty after processing
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_byteAtATime(self):
		"""Test receiving a packet one byte at a time (Serial behavior)."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"AB")

		# Send packet byte by byte
		for byte in packet:
			self.driver._onReceive(bytes([byte]))

		# Verify packet was processed after all bytes arrived
		self.assertEqual(len(self.processedPackets), 1)
		# Verify buffer is empty
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_partialPacket(self):
		"""Test receiving a packet in multiple chunks."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"test data")

		# Split packet in the middle
		chunk1 = packet[: len(packet) // 2]
		chunk2 = packet[len(packet) // 2 :]

		# Send first chunk
		self.driver._onReceive(chunk1)
		# No packet processed yet
		self.assertEqual(len(self.processedPackets), 0)
		# Buffer should contain first chunk
		self.assertGreater(len(self.driver._receiveBuffer), 0)

		# Send second chunk
		self.driver._onReceive(chunk2)
		# Now packet should be processed
		self.assertEqual(len(self.processedPackets), 1)
		# Buffer should be empty
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_multiplePacketsAtOnce(self):
		"""Test receiving multiple complete packets in a single call."""
		packet1 = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"A")
		packet2 = self._createPacket(dest=0, cmd=0x0102, seqNum=2, data=b"B")
		packet3 = self._createPacket(dest=0, cmd=0x0103, seqNum=3, data=b"C")

		# Concatenate all packets
		allPackets = packet1 + packet2 + packet3

		# Receive all at once
		self.driver._onReceive(allPackets)

		# Verify all three packets were processed
		self.assertEqual(len(self.processedPackets), 3)
		# Buffer should be empty
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_badSyncByte_resynchronize(self):
		"""Test that bad sync bytes are discarded and driver resynchronizes."""
		# Bad data followed by valid packet
		badData = b"\x00\x11\x22"
		goodPacket = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"OK")

		# Receive bad data + good packet
		self.driver._onReceive(badData + goodPacket)

		# Only the good packet should be processed
		self.assertEqual(len(self.processedPackets), 1)
		# Buffer should be empty
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_bufferOverflow_cleared(self):
		"""Test that buffer is cleared when it exceeds MAX_PACKET_SIZE."""
		# Create garbage data exceeding limit
		garbageData = b"\xff" * (self.driver.MAX_PACKET_SIZE + 10)

		# Send garbage
		self.driver._onReceive(garbageData)

		# No packets should be processed
		self.assertEqual(len(self.processedPackets), 0)
		# Buffer should be cleared (safety mechanism)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_incompletePacketInBuffer(self):
		"""Test that incomplete packet stays in buffer."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"test")

		# Send only first 6 bytes (header is 4 bytes, need more for complete packet)
		partialData = packet[:6]
		self.driver._onReceive(partialData)

		# No packets processed yet
		self.assertEqual(len(self.processedPackets), 0)
		# Buffer should contain the partial data
		self.assertEqual(len(self.driver._receiveBuffer), 6)
		self.assertEqual(bytes(self.driver._receiveBuffer), partialData)

	def test_emptyData(self):
		"""Test receiving empty data doesn't cause errors."""
		self.driver._onReceive(b"")

		# Nothing processed
		self.assertEqual(len(self.processedPackets), 0)
		# Buffer remains empty
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_partialHeaderOnly(self):
		"""Test receiving only partial header (less than 4 bytes)."""
		# Send only 3 bytes (need 4 for complete header)
		self.driver._onReceive(
			bytes(
				[
					self.DP_PacketSyncByte.SYNC1,
					self.DP_PacketSyncByte.SYNC2,
					0x00,
				],
			),
		)

		# No packets processed
		self.assertEqual(len(self.processedPackets), 0)
		# Buffer contains the 3 bytes
		self.assertEqual(len(self.driver._receiveBuffer), 3)
