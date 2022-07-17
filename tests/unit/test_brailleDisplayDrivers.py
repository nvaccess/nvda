# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2020 NV Access Limited, Leonard de Ruijter

"""Unit tests for braille display drivers.
"""

from typing import Set
from brailleDisplayDrivers import seikantk
import unittest
import braille


class FakeSeikantkDriver(seikantk.BrailleDisplayDriver):
	def __init__(self, isHid: bool):
		"""Sets the variables necessary to test _onReceive without a braille device connected.
		@param isHid: True if hid messages should be tested, False if serial (bluetooth) messages should be
		tested.
		"""
		# Variables that need to be set to spoof receiving data
		self._hidBuffer = b""
		self._command = None
		self._argsLen = None
		# Used to capture information for testing
		self._pressedKeys = set()
		self._routingIndexes = set()
		self.isHid = isHid

	def _handleKeys(self, arg: bytes):
		"""Overridden method to capture data"""
		brailleDots = arg[0]
		keys = arg[1] | (arg[2] << 8)
		self._pressedKeys = set(seikantk._getKeyNames(keys, seikantk._keyNames)).union(
			seikantk._getKeyNames(brailleDots, seikantk._dotNames)
		)

	def _handleRouting(self, arg: bytes):
		"""Overridden method to capture data"""
		self._routingIndexes = seikantk._getRoutingIndexes(arg)

	def simulateMessageReceived(self, sampleMessage: bytes) -> None:
		if self.isHid:
			return self.simulateHidMessageReceived(sampleMessage)
		else:
			return self.simulateSerialMessageReceived(sampleMessage)

	def simulateHidMessageReceived(self, sampleMessage: bytes):
		PRE_CANARY = bytes([2])  # start of text character
		POST_CANARY = bytes([3])  # end of text character

		for byteToSend in sampleMessage:
			# the middle byte is the only one used, padded by a byte on either side.
			self._onReceiveHID(PRE_CANARY + bytes([byteToSend]) + POST_CANARY)

	def simulateSerialMessageReceived(self, sampleMessage: bytes):
		for byteToSend in sampleMessage:
			# the bytes sent one at a time, with no padding
			self._onReceiveSerial(bytes([byteToSend]))


class TestSeikantkDriver_HID(unittest.TestCase):
	def test_handleInfo(self):
		SBDDesc = b"foobarloremips"  # a dummy description as this isn't specified in the spec
		example16Cell = bytes([0xff, 0xff, 0xa2, 0x11, 0x16, 0x10, 0x10]) + SBDDesc
		example40Cell = bytes([0xff, 0xff, 0xa2, 0x11, 0x16, 0x28, 0x28]) + SBDDesc
		seikaTestDriver = FakeSeikantkDriver(isHid=True)
		seikaTestDriver.simulateMessageReceived(example16Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(16, seikaTestDriver.numCells)
		self.assertEqual(16, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

		seikaTestDriver = FakeSeikantkDriver(isHid=True)
		seikaTestDriver.simulateMessageReceived(example40Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(40, seikaTestDriver.numCells)
		self.assertEqual(40, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

	def test_handleRouting(self):
		example16Cell = bytes([0xff, 0xff, 0xa4, 0x02, 0b10000001, 0b10000001])
		example40Cell = bytes([0xff, 0xff, 0xa4, 0x05, 0b10000001, 0b10000001, 0b10000001, 0b10000001, 0b10000001])
		self._simulateKeyPress(example16Cell, set(), {0, 7, 8, 15})
		self._simulateKeyPress(example40Cell, set(), {0, 7, 8, 15, 16, 23, 24, 31, 32, 39})

	def test_handleKeys(self):
		example4 = bytes([0xff, 0xff, 0xa6, 0x03, 0b10000001, 0x00, 0b00100000])
		self._simulateKeyPress(example4, {"d1", "d8", "RJ_DOWN"}, set())

	def test_handleKeysAndRouting(self):
		example16Cell = bytes([0xff, 0xff, 0xa8, 0x05, 0x00, 0b10010000, 0x00, 0x00, 0x40])
		example40Cell = bytes([0xff, 0xff, 0xa8, 0x08, 0x00, 0b00100000, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00])
		self._simulateKeyPress(example16Cell, {"LJ_CENTER", "LJ_UP"}, {14})
		self._simulateKeyPress(example40Cell, {"LJ_LEFT", "LJ_DOWN"}, {17})

	def _simulateKeyPress(
			self,
			sampleMessage: bytes,
			expectedKeyNames: Set[str],
			expectedRoutingIndexes: Set[int]
	):
		seikaTestDriver = FakeSeikantkDriver(isHid=True)
		seikaTestDriver.simulateMessageReceived(sampleMessage)
		self.assertEqual(expectedKeyNames, seikaTestDriver._pressedKeys)
		self.assertEqual(expectedRoutingIndexes, seikaTestDriver._routingIndexes)


class TestSeikantkDriver_Serial(unittest.TestCase):
	def test_handleInfo(self):
		SBDDesc = b"foobarloremips"  # a dummy description as this isn't specified in the spec
		example16Cell = bytes([0xff, 0xff, 0xa2, 0x11, 0x16, 0x10, 0x10]) + SBDDesc
		example40Cell = bytes([0xff, 0xff, 0xa2, 0x11, 0x16, 0x28, 0x28]) + SBDDesc
		seikaTestDriver = FakeSeikantkDriver(isHid=False)
		seikaTestDriver.simulateMessageReceived(example16Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(16, seikaTestDriver.numCells)
		self.assertEqual(16, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

		seikaTestDriver = FakeSeikantkDriver(isHid=False)
		seikaTestDriver.simulateMessageReceived(example40Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(40, seikaTestDriver.numCells)
		self.assertEqual(40, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

	def test_handleRouting(self):
		example16Cell = bytes([0xff, 0xff, 0xa4, 0x02, 0b10000001, 0b10000001])
		example40Cell = bytes([0xff, 0xff, 0xa4, 0x05, 0b10000001, 0b10000001, 0b10000001, 0b10000001, 0b10000001])
		self._simulateKeyPress(example16Cell, set(), {0, 7, 8, 15})
		self._simulateKeyPress(example40Cell, set(), {0, 7, 8, 15, 16, 23, 24, 31, 32, 39})

	def test_handleKeys(self):
		example4 = bytes([0xff, 0xff, 0xa6, 0x03, 0b10000001, 0x00, 0b00100000])
		self._simulateKeyPress(example4, {"d1", "d8", "RJ_DOWN"}, set())

	def test_handleKeysAndRouting(self):
		example16Cell = bytes([0xff, 0xff, 0xa8, 0x05, 0x00, 0b10010000, 0x00, 0x00, 0x40])
		example40Cell = bytes([0xff, 0xff, 0xa8, 0x08, 0x00, 0b00100000, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00])
		self._simulateKeyPress(example16Cell, {"LJ_CENTER", "LJ_UP"}, {14})
		self._simulateKeyPress(example40Cell, {"LJ_LEFT", "LJ_DOWN"}, {17})

	def _simulateKeyPress(
			self,
			sampleMessage: bytes,
			expectedKeyNames: Set[str],
			expectedRoutingIndexes: Set[int]
	):
		seikaTestDriver = FakeSeikantkDriver(isHid=False)
		seikaTestDriver.simulateMessageReceived(sampleMessage)
		self.assertEqual(expectedKeyNames, seikaTestDriver._pressedKeys)
		self.assertEqual(expectedRoutingIndexes, seikaTestDriver._routingIndexes)


class TestGestureMap(unittest.TestCase):
	"""Tests the integrity of braille display driver gesture maps."""

	def test_identifiers(self):
		"""Checks whether all defined braille display gestures contain valid braille display key identifiers."""
		for name, description in braille.getDisplayList(excludeNegativeChecks=False):
			driver=braille._getDisplayDriver(name)
			gmap=driver.gestureMap
			if not gmap:
				continue
			for cls, gesture, scriptName in gmap.getScriptsForAllGestures():
				if gesture.startswith("br"):
					self.assertRegexpMatches(gesture, braille.BrailleDisplayGesture.ID_PARTS_REGEX)


class TestBRLTTY(unittest.TestCase):
	"""Tests the integrity of the bundled brlapi module."""

	def test_brlapi(self):
		try:
			# SUpress Flake8 F401 imported but unused, as we're testing the import
			import brlapi  # noqa: F401
		except Exception:
			self.fail("Couldn't import the brlapi module")
