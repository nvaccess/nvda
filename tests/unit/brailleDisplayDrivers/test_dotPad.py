# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau

"""Unit tests for the dotPad braille display driver.

These tests cover the buffered receive logic that supports both serial (byte-at-a-time)
and BLE (complete packet) receive modes. The implementation is part of #19122.
"""

import unittest
from unittest.mock import MagicMock
import struct
import functools
import operator


@unittest.skip("Requires buffered receive implementation from #19122")
class TestDotPadBufferedReceive(unittest.TestCase):
	"""Tests for the buffered receive logic in the DotPad driver."""

	def setUp(self):
		"""Set up test fixtures."""
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
		packetBody = bytearray([dest])
		packetBody.extend(struct.pack(">H", cmd))
		packetBody.append(seqNum)
		packetBody.extend(data)

		checksum = functools.reduce(operator.xor, packetBody, self.DP_CHECKSUM_BASE)
		packetBody.append(checksum)

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

		self.driver._onReceive(packet)

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_byteAtATime(self):
		"""Test receiving a packet one byte at a time (Serial behavior)."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"AB")

		for byte in packet:
			self.driver._onReceive(bytes([byte]))

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_partialPacket(self):
		"""Test receiving a packet in multiple chunks."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"test data")

		chunk1 = packet[: len(packet) // 2]
		chunk2 = packet[len(packet) // 2 :]

		self.driver._onReceive(chunk1)
		self.assertEqual(len(self.processedPackets), 0)
		self.assertGreater(len(self.driver._receiveBuffer), 0)

		self.driver._onReceive(chunk2)
		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_multiplePacketsAtOnce(self):
		"""Test receiving multiple complete packets in a single call."""
		packet1 = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"A")
		packet2 = self._createPacket(dest=0, cmd=0x0102, seqNum=2, data=b"B")
		packet3 = self._createPacket(dest=0, cmd=0x0103, seqNum=3, data=b"C")

		allPackets = packet1 + packet2 + packet3

		self.driver._onReceive(allPackets)

		self.assertEqual(len(self.processedPackets), 3)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_badSyncByte_resynchronize(self):
		"""Test that bad sync bytes are discarded and driver resynchronizes."""
		badData = b"\x00\x11\x22"
		goodPacket = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"OK")

		self.driver._onReceive(badData + goodPacket)

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_bufferOverflow_cleared(self):
		"""Test that buffer is cleared when it exceeds MAX_PACKET_SIZE."""
		garbageData = b"\xff" * (self.driver.MAX_PACKET_SIZE + 10)

		self.driver._onReceive(garbageData)

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_incompletePacketInBuffer(self):
		"""Test that incomplete packet stays in buffer."""
		packet = self._createPacket(dest=0, cmd=0x0101, seqNum=1, data=b"test")

		partialData = packet[:6]
		self.driver._onReceive(partialData)

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 6)
		self.assertEqual(bytes(self.driver._receiveBuffer), partialData)

	def test_emptyData(self):
		"""Test receiving empty data doesn't cause errors."""
		self.driver._onReceive(b"")

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_partialHeaderOnly(self):
		"""Test receiving only partial header (less than 4 bytes)."""
		self.driver._onReceive(
			bytes(
				[
					self.DP_PacketSyncByte.SYNC1,
					self.DP_PacketSyncByte.SYNC2,
					0x00,
				],
			),
		)

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 3)
