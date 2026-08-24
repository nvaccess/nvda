# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2025 NV Access Limited, Leonard de Ruijter

"""Unit tests for braille display drivers."""

from brailleDisplayDrivers import seikantk
import unittest
from unittest.mock import patch
import bdDetect
import braille
import braille.display
import braille.display.gesture


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
			seikantk._getKeyNames(brailleDots, seikantk._dotNames),
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
		example16Cell = bytes([0xFF, 0xFF, 0xA2, 0x11, 0x16, 0x10, 0x10]) + SBDDesc
		example40Cell = bytes([0xFF, 0xFF, 0xA2, 0x11, 0x16, 0x28, 0x28]) + SBDDesc
		seikaTestDriver = FakeSeikantkDriver(isHid=True)
		seikaTestDriver.simulateMessageReceived(example16Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(16, seikaTestDriver.numCells)
		self.assertEqual(16, seikaTestDriver.numCols)
		self.assertEqual(1, seikaTestDriver.numRows)
		self.assertEqual(16, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

		seikaTestDriver = FakeSeikantkDriver(isHid=True)
		seikaTestDriver.simulateMessageReceived(example40Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(40, seikaTestDriver.numCells)
		self.assertEqual(40, seikaTestDriver.numCols)
		self.assertEqual(1, seikaTestDriver.numRows)
		self.assertEqual(40, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

	def test_handleRouting(self):
		example16Cell = bytes([0xFF, 0xFF, 0xA4, 0x02, 0b10000001, 0b10000001])
		example40Cell = bytes(
			[0xFF, 0xFF, 0xA4, 0x05, 0b10000001, 0b10000001, 0b10000001, 0b10000001, 0b10000001],
		)
		self._simulateKeyPress(example16Cell, set(), {0, 7, 8, 15})
		self._simulateKeyPress(example40Cell, set(), {0, 7, 8, 15, 16, 23, 24, 31, 32, 39})

	def test_handleKeys(self):
		example4 = bytes([0xFF, 0xFF, 0xA6, 0x03, 0b10000001, 0x00, 0b00100000])
		self._simulateKeyPress(example4, {"d1", "d8", "RJ_DOWN"}, set())

	def test_handleKeysAndRouting(self):
		example16Cell = bytes([0xFF, 0xFF, 0xA8, 0x05, 0x00, 0b10010000, 0x00, 0x00, 0x40])
		example40Cell = bytes([0xFF, 0xFF, 0xA8, 0x08, 0x00, 0b00100000, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00])
		self._simulateKeyPress(example16Cell, {"LJ_CENTER", "LJ_UP"}, {14})
		self._simulateKeyPress(example40Cell, {"LJ_LEFT", "LJ_DOWN"}, {17})

	def _simulateKeyPress(
		self,
		sampleMessage: bytes,
		expectedKeyNames: set[str],
		expectedRoutingIndexes: set[int],
	):
		seikaTestDriver = FakeSeikantkDriver(isHid=True)
		seikaTestDriver.simulateMessageReceived(sampleMessage)
		self.assertEqual(expectedKeyNames, seikaTestDriver._pressedKeys)
		self.assertEqual(expectedRoutingIndexes, seikaTestDriver._routingIndexes)


class TestSeikantkDriver_Serial(unittest.TestCase):
	def test_handleInfo(self):
		SBDDesc = b"foobarloremips"  # a dummy description as this isn't specified in the spec
		example16Cell = bytes([0xFF, 0xFF, 0xA2, 0x11, 0x16, 0x10, 0x10]) + SBDDesc
		example40Cell = bytes([0xFF, 0xFF, 0xA2, 0x11, 0x16, 0x28, 0x28]) + SBDDesc
		seikaTestDriver = FakeSeikantkDriver(isHid=False)
		seikaTestDriver.simulateMessageReceived(example16Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(16, seikaTestDriver.numCells)
		self.assertEqual(16, seikaTestDriver.numCols)
		self.assertEqual(1, seikaTestDriver.numRows)
		self.assertEqual(16, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

		seikaTestDriver = FakeSeikantkDriver(isHid=False)
		seikaTestDriver.simulateMessageReceived(example40Cell)
		self.assertEqual(22, seikaTestDriver.numBtns)
		self.assertEqual(40, seikaTestDriver.numCells)
		self.assertEqual(40, seikaTestDriver.numCols)
		self.assertEqual(1, seikaTestDriver.numRows)
		self.assertEqual(40, seikaTestDriver.numRoutingKeys)
		self.assertEqual(SBDDesc.decode("UTF-8"), seikaTestDriver._description)

	def test_handleRouting(self):
		example16Cell = bytes([0xFF, 0xFF, 0xA4, 0x02, 0b10000001, 0b10000001])
		example40Cell = bytes(
			[0xFF, 0xFF, 0xA4, 0x05, 0b10000001, 0b10000001, 0b10000001, 0b10000001, 0b10000001],
		)
		self._simulateKeyPress(example16Cell, set(), {0, 7, 8, 15})
		self._simulateKeyPress(example40Cell, set(), {0, 7, 8, 15, 16, 23, 24, 31, 32, 39})

	def test_handleKeys(self):
		example4 = bytes([0xFF, 0xFF, 0xA6, 0x03, 0b10000001, 0x00, 0b00100000])
		self._simulateKeyPress(example4, {"d1", "d8", "RJ_DOWN"}, set())

	def test_handleKeysAndRouting(self):
		example16Cell = bytes([0xFF, 0xFF, 0xA8, 0x05, 0x00, 0b10010000, 0x00, 0x00, 0x40])
		example40Cell = bytes([0xFF, 0xFF, 0xA8, 0x08, 0x00, 0b00100000, 0x01, 0x00, 0x00, 0x02, 0x00, 0x00])
		self._simulateKeyPress(example16Cell, {"LJ_CENTER", "LJ_UP"}, {14})
		self._simulateKeyPress(example40Cell, {"LJ_LEFT", "LJ_DOWN"}, {17})

	def _simulateKeyPress(
		self,
		sampleMessage: bytes,
		expectedKeyNames: set[str],
		expectedRoutingIndexes: set[int],
	):
		seikaTestDriver = FakeSeikantkDriver(isHid=False)
		seikaTestDriver.simulateMessageReceived(sampleMessage)
		self.assertEqual(expectedKeyNames, seikaTestDriver._pressedKeys)
		self.assertEqual(expectedRoutingIndexes, seikaTestDriver._routingIndexes)


class TestGestureMap(unittest.TestCase):
	"""Tests the integrity of braille display driver gesture maps."""

	def test_identifiers(self):
		"""Checks whether all defined braille display gestures contain valid braille display key identifiers."""
		for name, description in braille.display.getDisplayList(excludeNegativeChecks=False):
			driver = braille.display._getDisplayDriver(name)
			gmap = driver.gestureMap
			if not gmap:
				continue
			for cls, gesture, scriptName in gmap.getScriptsForAllGestures():
				if gesture.startswith("br"):
					self.assertRegex(gesture, braille.display.gesture.BrailleDisplayGesture.ID_PARTS_REGEX)


class _RoutingGesture(braille.display.gesture.BrailleDisplayGesture):
	source = "test"
	id = "routing"


class _MultiRoutingGesture(braille.display.gesture.BrailleDisplayGesture):
	source = "test"
	id = "multiRouting"


class _ModelRoutingGesture(braille.display.gesture.BrailleDisplayGesture):
	source = "testDriver"
	model = "testModel"
	id = "routing"


class _ComboGesture(braille.display.gesture.BrailleDisplayGesture):
	"""Gesture whose id contains '+', simulating a routing key combined with a modifier."""

	source = "test"
	id = "key1+routing"


class TestBrailleDisplayGestureCellIndexes(unittest.TestCase):
	"""Tests for :attr:`braille.BrailleDisplayGesture.cellIndexes` and the deprecated ``routingIndex`` shim."""

	def test_default_cellIndexes_none(self):
		g = _RoutingGesture()
		self.assertIsNone(g.cellIndexes)

	def test_idForCellCount(self):
		self.assertEqual("routing", braille.display.gesture.BrailleDisplayGesture.idForCellCount(0))
		self.assertEqual("routing", braille.display.gesture.BrailleDisplayGesture.idForCellCount(1))
		self.assertEqual("multiRouting", braille.display.gesture.BrailleDisplayGesture.idForCellCount(2))
		self.assertEqual("multiRouting", braille.display.gesture.BrailleDisplayGesture.idForCellCount(5))

	def test_idForCellCount_custom_baseName(self):
		self.assertEqual(
			"secondRouting",
			braille.display.gesture.BrailleDisplayGesture.idForCellCount(1, "secondRouting"),
		)
		self.assertEqual(
			"multiSecondRouting",
			braille.display.gesture.BrailleDisplayGesture.idForCellCount(2, "secondRouting"),
		)
		self.assertEqual("route", braille.display.gesture.BrailleDisplayGesture.idForCellCount(1, "route"))
		self.assertEqual(
			"multiRoute",
			braille.display.gesture.BrailleDisplayGesture.idForCellCount(2, "route"),
		)
		self.assertEqual(
			"multiUpperRouting",
			braille.display.gesture.BrailleDisplayGesture.idForCellCount(3, "upperRouting"),
		)

	def test_routingIndex_getter_returns_highest_cell(self):
		g = _RoutingGesture()
		g.cellIndexes = [3, 7]
		self.assertEqual(7, g.routingIndex)

	def test_routingIndex_getter_none_when_empty(self):
		g = _RoutingGesture()
		self.assertIsNone(g.routingIndex)

	def test_routingIndex_setter_wraps_into_cellIndexes(self):
		g = _RoutingGesture()
		g.routingIndex = 5
		self.assertEqual([5], g.cellIndexes)

	def test_routingIndex_setter_none_clears_cellIndexes(self):
		g = _RoutingGesture()
		g.cellIndexes = [1, 2]
		g.routingIndex = None
		self.assertIsNone(g.cellIndexes)

	def test_multiRouting_identifier_matches_regex(self):
		g = _MultiRoutingGesture()
		g.cellIndexes = [0, 3, 7]
		for identifier in g.identifiers:
			if identifier.startswith("br"):
				self.assertRegex(identifier, braille.display.gesture.BrailleDisplayGesture.ID_PARTS_REGEX)

	def test_cellIndexesStr_none_when_no_cellIndexes(self):
		g = _RoutingGesture()
		self.assertIsNone(g._cellIndexesStr)

	def test_cellIndexesStr_single_cell(self):
		g = _RoutingGesture()
		g.cellIndexes = [2]
		self.assertEqual("3", g._cellIndexesStr)

	def test_cellIndexesStr_multiple_cells(self):
		g = _MultiRoutingGesture()
		g.cellIndexes = [0, 3, 7]
		self.assertEqual("1+4+8", g._cellIndexesStr)

	def test_cellIndexesStr_none_when_id_contains_plus(self):
		g = _ComboGesture()
		g.cellIndexes = [2]
		self.assertIsNone(g._cellIndexesStr)

	def test_identifiers_no_cellIndexes(self):
		g = _RoutingGesture()
		self.assertEqual(["br(test):routing"], g.identifiers)

	def test_identifiers_single_cell(self):
		g = _RoutingGesture()
		g.cellIndexes = [2]
		self.assertEqual(["br(test):routing3", "br(test):routing"], g.identifiers)

	def test_identifiers_multi_cell(self):
		g = _MultiRoutingGesture()
		g.cellIndexes = [0, 3]
		self.assertEqual(["br(test):multiRouting1+4", "br(test):multiRouting"], g.identifiers)

	def test_identifiers_with_model_single_cell(self):
		g = _ModelRoutingGesture()
		g.cellIndexes = [4]
		self.assertEqual(
			[
				"br(testDriver.testModel):routing5",
				"br(testDriver.testModel):routing",
				"br(testDriver):routing5",
				"br(testDriver):routing",
			],
			g.identifiers,
		)

	def test_identifiers_combo_no_cellIndexesStr(self):
		g = _ComboGesture()
		g.cellIndexes = [2]
		self.assertEqual(["br(test):key1+routing"], g.identifiers)

	def test_displayName_no_cellIndexes(self):
		g = _RoutingGesture()
		self.assertEqual("routing", g.displayName)

	def test_displayName_single_cell(self):
		g = _RoutingGesture()
		g.cellIndexes = [2]
		self.assertEqual("routing3", g.displayName)

	def test_displayName_multi_cell(self):
		g = _MultiRoutingGesture()
		g.cellIndexes = [0, 3, 7]
		self.assertEqual("multiRouting1+4+8", g.displayName)


class TestBRLTTY(unittest.TestCase):
	"""Tests the integrity of the bundled brlapi module."""

	def test_brlapi(self):
		try:
			# SUpress Flake8 F401 imported but unused, as we're testing the import
			import brlapi  # noqa: F401
		except Exception:
			self.fail("Couldn't import the brlapi module")


class _FakeBleDriver(braille.display.BrailleDisplayDriver):
	"""A driver that only exists to exercise the BLE port helpers."""

	name = "fakeBleDisplay"
	description = "Fake BLE display"


def _bleMatch(deviceName: str, address: str) -> bdDetect.DeviceMatch:
	"""Build a BLE device match as L{bdDetect.getBleDevicesForDriver} would yield it."""
	return bdDetect.DeviceMatch(
		bdDetect.ProtocolType.BLE,
		deviceName,
		address,
		{"name": deviceName, "address": address, "provider": bdDetect.CommunicationType.BLE},
	)


class TestBleDisplayPorts(unittest.TestCase):
	"""Tests for the BLE ports offered and resolved by L{braille.display.BrailleDisplayDriver}."""

	_ADDRESS = "AA:BB:CC:DD:EE:FF"

	def _patchBleDevices(self, *devices: bdDetect.DeviceMatch):
		"""Make L{bdDetect.getBleDevicesForDriver} report the given devices."""
		return patch("bdDetect.getBleDevicesForDriver", return_value=iter(devices))

	def test_getBlePorts_formatsPortAndDescription(self):
		with self._patchBleDevices(_bleMatch("DotPad320", self._ADDRESS)):
			ports = list(_FakeBleDriver._getBlePorts())
		self.assertEqual(len(ports), 1)
		port, description = ports[0]
		self.assertEqual(port, f"ble:DotPad320@{self._ADDRESS}")
		self.assertIn("DotPad320", description)

	def test_getBlePorts_noDevices(self):
		with self._patchBleDevices():
			self.assertEqual(list(_FakeBleDriver._getBlePorts()), [])

	def test_getBlePorts_enumerationFailureIsContained(self):
		"""A failing scan yields no ports rather than propagating."""
		with patch("bdDetect.getBleDevicesForDriver", side_effect=RuntimeError("scan failed")):
			self.assertEqual(list(_FakeBleDriver._getBlePorts()), [])

	def test_getBleTryPorts_deviceInScanResults(self):
		"""A port matching a scanned device resolves to that device match."""
		match = _bleMatch("DotPad320", self._ADDRESS)
		with self._patchBleDevices(_bleMatch("SomethingElse", "11:22:33:44:55:66"), match):
			result = list(_FakeBleDriver._getBleTryPorts(f"ble:DotPad320@{self._ADDRESS}"))
		self.assertEqual(result, [match])

	def test_getBleTryPorts_matchesOnAddressWhenNameChanged(self):
		"""A renamed device is still found by its address."""
		match = _bleMatch("DotPad320 renamed", self._ADDRESS)
		with self._patchBleDevices(match):
			result = list(_FakeBleDriver._getBleTryPorts(f"ble:DotPad320@{self._ADDRESS}"))
		self.assertEqual(result, [match])

	def test_getBleTryPorts_fallsBackToConfiguredAddress(self):
		"""A device that is not advertising is still offered for connection by address."""
		with self._patchBleDevices():
			result = list(_FakeBleDriver._getBleTryPorts(f"ble:DotPad320@{self._ADDRESS}"))
		self.assertEqual(len(result), 1)
		match = result[0]
		self.assertEqual(match.type, bdDetect.ProtocolType.BLE)
		self.assertEqual(match.id, "DotPad320")
		self.assertEqual(match.port, self._ADDRESS)
		self.assertEqual(match.deviceInfo["address"], self._ADDRESS)

	def test_getBleTryPorts_addressContainingSeparator(self):
		"""The port is split on the last separator, so a name containing one is preserved."""
		with self._patchBleDevices():
			result = list(_FakeBleDriver._getBleTryPorts(f"ble:Dot@Pad@{self._ADDRESS}"))
		self.assertEqual(len(result), 1)
		self.assertEqual(result[0].id, "Dot@Pad")
		self.assertEqual(result[0].port, self._ADDRESS)

	def test_getBleTryPorts_malformedPortYieldsNothing(self):
		"""A port without an address is rejected rather than half-parsed."""
		with self._patchBleDevices(_bleMatch("DotPad320", self._ADDRESS)):
			self.assertEqual(list(_FakeBleDriver._getBleTryPorts("ble:DotPad320")), [])

	def test_getBleTryPorts_addressWinsOverName(self):
		"""The address disambiguates two devices sharing a name, whatever the scan order."""
		byName = _bleMatch("DotPad320", "11:22:33:44:55:66")
		byAddress = _bleMatch("DotPad320", self._ADDRESS)
		with self._patchBleDevices(byName, byAddress):
			result = list(_FakeBleDriver._getBleTryPorts(f"ble:DotPad320@{self._ADDRESS}"))
		self.assertEqual(result, [byAddress])

	def test_getTryPorts_automaticPortYieldsBleDevices(self):
		"""The automatic port tries BLE devices, as it is offered when only those are known."""
		match = _bleMatch("DotPad320", self._ADDRESS)
		with (
			patch("bdDetect.getConnectedUsbDevicesForDriver", return_value=iter(())),
			patch("bdDetect.getPossibleBluetoothDevicesForDriver", return_value=iter(())),
			self._patchBleDevices(match),
		):
			result = list(_FakeBleDriver._getTryPorts("auto"))
		self.assertEqual(result, [match])

	def test_getTryPorts_usbPortDoesNotYieldBleDevices(self):
		"""Explicitly asking for USB must not fall back to BLE devices."""
		with (
			patch("bdDetect.getConnectedUsbDevicesForDriver", return_value=iter(())),
			patch("bdDetect.getBleDevicesForDriver") as mockBle,
		):
			result = list(_FakeBleDriver._getTryPorts("usb"))
		self.assertEqual(result, [])
		mockBle.assert_not_called()

	def test_getTryPorts_routesBlePortToHelper(self):
		"""A BLE port reaches _getBleTryPorts rather than the serial port handling."""
		match = _bleMatch("DotPad320", self._ADDRESS)
		with self._patchBleDevices(match):
			result = list(_FakeBleDriver._getTryPorts(f"ble:DotPad320@{self._ADDRESS}"))
		self.assertEqual(result, [match])
