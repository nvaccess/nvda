# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2026 NV Access Limited, Babbage B.V., Leonard de Ruijter, Dot Incorporated, Bram Duvigneau
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the bdDetect module."""

import unittest
from unittest.mock import MagicMock, patch
import bdDetect
from .extensionPointTestHelpers import chainTester
import braille
from brailleDisplayDrivers import dotPad
from utils.blockUntilConditionMet import blockUntilConditionMet


class TestBdDetectExtensionPoints(unittest.TestCase):
	"""A test for the extension points on the bdDetect module."""

	def test_scanForDevices(self):
		kwargs = dict(usb=False, bluetooth=False, ble=False, limitToDevices=["noBraille"])
		with chainTester(
			self,
			bdDetect.scanForDevices,
			[("noBraille", bdDetect.DeviceMatch("", "", "", {}))],
			**kwargs,
		):
			braille.handler._enableDetection(**kwargs)
			# wait for the detector to be terminated.
			success, _endTimeOrNone = blockUntilConditionMet(
				getValue=lambda: braille.handler._detector,
				giveUpAfterSeconds=3.0,
				shouldStopEvaluator=lambda detector: detector is None,
			)
			self.assertTrue(success)


class TestDriverRegistration(unittest.TestCase):
	"""A test for driver device registration."""

	def tearDown(self):
		bdDetect._driverDevices.clear()

	def test_addUsbDevice(self):
		"""Test adding a USB device."""
		from brailleDisplayDrivers import albatross

		registrar = bdDetect.DriverRegistrar(albatross.BrailleDisplayDriver.name)

		def matchFunc(match: bdDetect.DeviceMatch) -> bool:
			return match.deviceInfo.get("busReportedDeviceDescription") == albatross.driver.BUS_DEVICE_DESC

		registrar.addUsbDevice(
			bdDetect.ProtocolType.SERIAL,
			albatross.driver.VID_AND_PID,
			matchFunc=matchFunc,
		)
		expected = bdDetect._UsbDeviceRegistryEntry(
			albatross.driver.VID_AND_PID,
			bdDetect.ProtocolType.SERIAL,
			matchFunc=matchFunc,
		)
		self.assertIn(expected, registrar._getDriverDict().get(bdDetect.CommunicationType.USB))

	def test_addUsbDevices(self):
		"""Test adding multiple USB devices."""
		from brailleDisplayDrivers import albatross

		registrar = bdDetect.DriverRegistrar(albatross.BrailleDisplayDriver.name)

		def matchFunc(match: bdDetect.DeviceMatch) -> bool:
			return match.deviceInfo.get("busReportedDeviceDescription") == albatross.driver.BUS_DEVICE_DESC

		fakeVidAndPid = "VID_0403&PID_6002"
		registrar.addUsbDevices(
			bdDetect.ProtocolType.SERIAL,
			{albatross.driver.VID_AND_PID, fakeVidAndPid},
			matchFunc=matchFunc,
		)
		expected = bdDetect._UsbDeviceRegistryEntry(
			albatross.driver.VID_AND_PID,
			bdDetect.ProtocolType.SERIAL,
			matchFunc=matchFunc,
		)
		self.assertIn(expected, registrar._getDriverDict().get(bdDetect.CommunicationType.USB))
		expected2 = bdDetect._UsbDeviceRegistryEntry(
			fakeVidAndPid,
			bdDetect.ProtocolType.SERIAL,
			matchFunc=matchFunc,
		)
		self.assertIn(expected2, registrar._getDriverDict().get(bdDetect.CommunicationType.USB))

	def test_addBluetoothDevices(self):
		"""Test adding a fake Bluetooth match func."""
		from brailleDisplayDrivers import albatross

		registrar = bdDetect.DriverRegistrar(albatross.BrailleDisplayDriver.name)

		def matchFunc(match: bdDetect.DeviceMatch) -> bool:
			return True

		registrar.addBluetoothDevices(matchFunc)
		self.assertEqual(registrar._getDriverDict().get(bdDetect.CommunicationType.BLUETOOTH), matchFunc)

	def test_addBleDevices(self):
		"""addBleDevices stores the match function under the BLE communication type."""
		registrar = bdDetect.DriverRegistrar(dotPad.BrailleDisplayDriver.name)

		def matchFunc(match: bdDetect.DeviceMatch) -> bool:
			return match.id.startswith("DotPad")

		registrar.addBleDevices(matchFunc)

		storedMatchFunc = registrar._getDriverDict().get(bdDetect.CommunicationType.BLE)
		self.assertEqual(storedMatchFunc, matchFunc)
		self.assertTrue(callable(storedMatchFunc))

	def test_bleDeviceMatching(self):
		"""The registered DotPad match function accepts DotPad devices and rejects others."""
		registrar = bdDetect.DriverRegistrar(dotPad.BrailleDisplayDriver.name)
		registrar.addBleDevices(dotPad.BrailleDisplayDriver._isBleDotPad)

		matchingDevice = bdDetect.DeviceMatch(
			type=bdDetect.ProtocolType.BLE,
			id="DotPad320",
			port="AA:BB:CC:DD:EE:FF",
			deviceInfo={"name": "DotPad320", "address": "AA:BB:CC:DD:EE:FF"},
		)

		nonMatchingDevice = bdDetect.DeviceMatch(
			type=bdDetect.ProtocolType.BLE,
			id="SomeOtherDevice",
			port="11:22:33:44:55:66",
			deviceInfo={"name": "SomeOtherDevice", "address": "11:22:33:44:55:66"},
		)

		matchFunc = registrar._getDriverDict().get(bdDetect.CommunicationType.BLE)
		self.assertTrue(matchFunc(matchingDevice))
		self.assertFalse(matchFunc(nonMatchingDevice))


class TestBleDeviceDiscovery(unittest.TestCase):
	"""Tests for the detector reacting to BLE devices as they advertise.

	A background scan starts the scanner and moves on without waiting, so a device
	that is not already known reaches the detector only through this handler.
	"""

	_ADDRESS = "AA:BB:CC:DD:EE:FF"

	def _detector(self) -> MagicMock:
		"""Build a detector stub whose _onBleDeviceDiscovered is the real implementation."""
		detector = MagicMock(spec=bdDetect._Detector)
		detector._detectUsb = True
		detector._detectBluetooth = True
		detector._detectBle = True
		detector._limitToDevices = None
		detector._onBleDeviceDiscovered = bdDetect._Detector._onBleDeviceDiscovered.__get__(
			detector,
			type(detector),
		)
		return detector

	def _device(self, name: str) -> MagicMock:
		"""Build a stand-in for a discovered BLE device."""
		device = MagicMock()
		device.name = name
		device.address = self._ADDRESS
		return device

	def test_matchingDeviceQueuesScan(self):
		"""A newly discovered matching device is queued as the preferred device."""
		detector = self._detector()
		match = bdDetect.DeviceMatch(
			bdDetect.ProtocolType.BLE,
			"DotPad320",
			self._ADDRESS,
			{"name": "DotPad320", "address": self._ADDRESS},
		)
		detector._getBleDeviceMatch = MagicMock(return_value=("dotPad", match))

		detector._onBleDeviceDiscovered(self._device("DotPad320"), MagicMock(), True)

		detector._queueBgScan.assert_called_once_with(
			usb=True,
			bluetooth=True,
			ble=True,
			limitToDevices=None,
			preferredDevice=("dotPad", match),
		)

	def test_nonMatchingDeviceIsIgnored(self):
		"""A device no driver claims does not trigger a scan."""
		detector = self._detector()
		detector._getBleDeviceMatch = MagicMock(return_value=None)

		detector._onBleDeviceDiscovered(self._device("SomeOtherDevice"), MagicMock(), True)

		detector._queueBgScan.assert_not_called()

	def test_readvertisementIsIgnored(self):
		"""Only the first sighting queues a scan, so repeat advertisements stay cheap."""
		detector = self._detector()
		detector._getBleDeviceMatch = MagicMock()

		detector._onBleDeviceDiscovered(self._device("DotPad320"), MagicMock(), False)

		detector._getBleDeviceMatch.assert_not_called()
		detector._queueBgScan.assert_not_called()

	def test_bleDetectionDisabled(self):
		"""No scan is queued while BLE detection is off."""
		detector = self._detector()
		detector._detectBle = False
		detector._getBleDeviceMatch = MagicMock()

		detector._onBleDeviceDiscovered(self._device("DotPad320"), MagicMock(), True)

		detector._queueBgScan.assert_not_called()


class TestBleDriverMatching(unittest.TestCase):
	"""Tests for matching discovered BLE devices against the registered drivers."""

	def tearDown(self) -> None:
		# Registration writes into the global registry; keep tests isolated.
		bdDetect._driverDevices.clear()

	def _registerDriver(self, driver: str, prefix: str) -> None:
		"""Register a driver claiming any device whose name starts with the given prefix."""
		registrar = bdDetect.DriverRegistrar(driver)
		registrar.addBleDevices(lambda match, prefix=prefix: match.id.startswith(prefix))

	def _scannerWith(self, *names: str):
		"""Make the shared scanner report devices with the given names."""
		devices = []
		for i, name in enumerate(names):
			device = MagicMock()
			device.name = name
			device.address = f"AA:BB:CC:DD:EE:{i:02X}"
			devices.append(device)
		scanner = MagicMock()
		scanner.isScanning = True
		scanner.results.return_value = devices
		return patch("hwIo.ble.scanner", scanner)

	def test_devicesAreOfferedInDiscoveryOrder(self):
		"""The device discovered first is offered first, whichever driver claims it.

		Driver registration order is import order, so ordering by driver would let that
		decide which display is connected when several are in range.
		"""
		self._registerDriver("driverA", "Alpha")
		self._registerDriver("driverB", "Beta")
		with self._scannerWith("Beta1", "Alpha1"):
			result = list(bdDetect.getDriversForBleDevices())
		self.assertEqual([driver for driver, match in result], ["driverB", "driverA"])
		self.assertEqual([match.id for driver, match in result], ["Beta1", "Alpha1"])

	def test_limitToDevicesExcludesDrivers(self):
		"""A driver outside the limit never sees the devices."""
		self._registerDriver("driverA", "Alpha")
		self._registerDriver("driverB", "Beta")
		with self._scannerWith("Beta1", "Alpha1"):
			result = list(bdDetect.getDriversForBleDevices(limitToDevices=["driverA"]))
		self.assertEqual([(driver, match.id) for driver, match in result], [("driverA", "Alpha1")])

	def test_noBleDriversYieldsNothing(self):
		"""Without a driver that can match BLE devices the scan results are not inspected."""
		with self._scannerWith("Alpha1") as scanner:
			self.assertEqual(list(bdDetect.getDriversForBleDevices()), [])
		scanner.results.assert_not_called()
