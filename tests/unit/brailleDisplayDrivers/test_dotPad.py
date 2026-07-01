# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the DotPad braille display driver.

Tests cover the buffered-receive logic that handles both byte-at-a-time
delivery (Serial) and packet-based delivery (BLE).
"""

import functools
import operator
import struct
import unittest
from unittest.mock import MagicMock

import bdDetect
from brailleDisplayDrivers.dotPad.driver import BrailleDisplayDriver
from brailleDisplayDrivers.dotPad.defs import (
	DP_CHECKSUM_BASE,
	DP_Command,
	DP_MAX_PACKET_SIZE,
	DP_MIN_PACKET_SIZE,
	DP_PacketSyncByte,
)


class TestDotPadBufferedReceive(unittest.TestCase):
	"""Tests for the DotPad buffered receive logic in _onReceive."""

	def setUp(self) -> None:
		self.driver = MagicMock(spec=BrailleDisplayDriver)
		self.driver._receiveBuffer = bytearray()
		self.driver._lastResponse = {}

		self.processedPackets: list[bytes] = []

		def mockProcessPacket(packetBody: bytes) -> None:
			self.processedPackets.append(bytes(packetBody))

		self.driver._processPacket = mockProcessPacket
		self.driver._onReceive = BrailleDisplayDriver._onReceive.__get__(self.driver, type(self.driver))

	def _createPacket(
		self,
		dest: int = 0,
		cmd: int = DP_Command.RSP_DEVICE_NAME,
		seqNum: int = 0,
		data: bytes = b"",
	) -> bytes:
		"""Create a valid DotPad packet.

		:param dest: Destination address.
		:param cmd: Command code.
		:param seqNum: Sequence number.
		:param data: Packet data payload.
		:return: Complete packet as bytes.
		"""
		packetBody = bytearray([dest])
		packetBody.extend(struct.pack(">H", cmd))
		packetBody.append(seqNum)
		packetBody.extend(data)

		checksum = functools.reduce(operator.xor, packetBody, DP_CHECKSUM_BASE)
		packetBody.append(checksum)

		packet = bytearray(
			[
				DP_PacketSyncByte.SYNC1,
				DP_PacketSyncByte.SYNC2,
			],
		)
		packet.extend(struct.pack(">H", len(packetBody)))
		packet.extend(packetBody)

		return bytes(packet)

	def test_completePacketAtOnce(self) -> None:
		"""Test receiving a complete packet in a single call (BLE behavior)."""
		packet = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"test")

		self.driver._onReceive(packet)

		self.assertEqual(len(self.processedPackets), 1)
		# The body passed on is the packet with the 4-byte sync/length header stripped.
		self.assertEqual(self.processedPackets[0], packet[4:])
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_byteAtATime(self) -> None:
		"""Test receiving a packet one byte at a time (Serial behavior)."""
		packet = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"AB")

		for byte in packet:
			self.driver._onReceive(bytes([byte]))

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_partialPacket(self) -> None:
		"""Test receiving a packet in multiple chunks."""
		packet = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"test data")

		chunk1 = packet[: len(packet) // 2]
		chunk2 = packet[len(packet) // 2 :]

		self.driver._onReceive(chunk1)
		self.assertEqual(len(self.processedPackets), 0)
		self.assertGreater(len(self.driver._receiveBuffer), 0)

		self.driver._onReceive(chunk2)
		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_multiplePacketsAtOnce(self) -> None:
		"""Test receiving multiple complete packets in a single call."""
		packet1 = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"A")
		packet2 = self._createPacket(dest=0, cmd=DP_Command.REQ_DEVICE_NAME, seqNum=2, data=b"B")
		packet3 = self._createPacket(dest=0, cmd=DP_Command.REQ_BOARD_INFORMATION, seqNum=3, data=b"C")

		allPackets = packet1 + packet2 + packet3

		self.driver._onReceive(allPackets)

		self.assertEqual(len(self.processedPackets), 3)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_badSyncByte_resynchronize(self) -> None:
		"""Test that bad sync bytes are discarded and driver resynchronizes."""
		badData = b"\x00\x11\x22"
		goodPacket = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"OK")

		self.driver._onReceive(badData + goodPacket)

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_implausibleLength_resynchronize(self) -> None:
		"""Test that a header declaring an oversized length is treated as a false header.

		Valid sync bytes followed by a length that pushes the total packet size beyond
		DP_MAX_PACKET_SIZE indicate a desync rather than a real packet, so the driver
		should discard a byte, resync, and still process a valid packet that follows.
		"""
		# A body length that makes totalLength (4-byte header + body) exceed DP_MAX_PACKET_SIZE.
		oversizedBodyLength = DP_MAX_PACKET_SIZE
		bogusHeader = bytes([DP_PacketSyncByte.SYNC1, DP_PacketSyncByte.SYNC2]) + struct.pack(
			">H",
			oversizedBodyLength,
		)
		goodPacket = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"OK")

		self.driver._onReceive(bogusHeader + goodPacket)

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(self.processedPackets[0], goodPacket[4:])
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_tooSmallLength_resynchronize(self) -> None:
		"""Test that a header declaring a runt length is treated as a false header.

		Valid sync bytes followed by a length too small to form the minimum packet
		body indicate a desync rather than a real packet, so the driver should discard
		a byte, resync, and still process a valid packet that follows.
		"""
		# A body length that makes totalLength (4-byte header + body) fall below DP_MIN_PACKET_SIZE.
		runtBodyLength = DP_MIN_PACKET_SIZE - 4 - 1
		bogusHeader = bytes([DP_PacketSyncByte.SYNC1, DP_PacketSyncByte.SYNC2]) + struct.pack(
			">H",
			runtBodyLength,
		)
		goodPacket = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"OK")

		self.driver._onReceive(bogusHeader + goodPacket)

		self.assertEqual(len(self.processedPackets), 1)
		self.assertEqual(self.processedPackets[0], goodPacket[4:])
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_incompletePacketInBuffer(self) -> None:
		"""Test that an incomplete packet stays in the buffer."""
		packet = self._createPacket(dest=0, cmd=DP_Command.RSP_DEVICE_NAME, seqNum=1, data=b"test data")
		partialPacket = packet[:6]

		self.driver._onReceive(partialPacket)

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 6)

	def test_emptyData(self) -> None:
		"""Test that empty data doesn't crash or produce spurious packets."""
		self.driver._onReceive(b"")

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 0)

	def test_partialHeaderOnly(self) -> None:
		"""Test that a partial header stays buffered without processing."""
		partialHeader = bytes([DP_PacketSyncByte.SYNC1, DP_PacketSyncByte.SYNC2, 0x00])

		self.driver._onReceive(partialHeader)

		self.assertEqual(len(self.processedPackets), 0)
		self.assertEqual(len(self.driver._receiveBuffer), 3)


@unittest.skip("Requires BLE support from PR C (#19122)")
class TestDotPadBle(unittest.TestCase):
	"""Skipped tests for BLE-specific DotPad functionality.

	These tests document the expected BLE behavior and will be unskipped
	when the BLE driver integration lands in PR C.
	"""

	def test_isBleDotPad_matching(self) -> None:
		"""_isBleDotPad returns True for a device ID starting with 'DotPad'."""
		device = MagicMock()
		device.name = "DotPad320"
		self.assertTrue(BrailleDisplayDriver._isBleDotPad(device))

	def test_isBleDotPad_nonMatching(self) -> None:
		"""_isBleDotPad returns False for an unrelated device."""
		device = MagicMock()
		device.name = "SomeOtherDevice"
		self.assertFalse(BrailleDisplayDriver._isBleDotPad(device))

	def test_check_returnsTrue(self) -> None:
		"""check() returns True so DotPad always appears in the display list."""
		self.assertTrue(BrailleDisplayDriver.check())

	def test_addBleDevices_registration(self) -> None:
		"""addBleDevices registers _isBleDotPad as the BLE match function."""
		registrar = bdDetect.DriverRegistrar(BrailleDisplayDriver.name)
		BrailleDisplayDriver.registerAutomaticDetection(registrar)
		matchFunc = registrar._getDriverDict().get(bdDetect.CommunicationType.BLE)
		self.assertIsNotNone(matchFunc)
		self.assertTrue(callable(matchFunc))

	def test_tryConnect_bleDevice(self) -> None:
		"""_tryConnect with a BLE device creates a hwIo.ble.Ble instance.

		Requires hwIo.ble (PR A, #19838) and the _tryConnect BLE branch
		(PR C). Will mock findDeviceByAddress, hwIo.ble.Ble,
		_requestDeviceName, and _requestBoardInformation.
		"""
