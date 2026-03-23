# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023-25 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Unit tests for the bdDetect module."""

import unittest
import bdDetect
from .extensionPointTestHelpers import chainTester
import braille
from utils.blockUntilConditionMet import blockUntilConditionMet


class TestBdDetectExtensionPoints(unittest.TestCase):
	"""A test for the extension points on the bdDetect module."""

	def test_scanForDevices(self):
		kwargs = dict(usb=False, bluetooth=False, limitToDevices=["noBraille"])
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

	@unittest.skip("Requires BLE support in bdDetect from #19122")
	def test_addBleDevices(self):
		"""Test adding a BLE match function."""
		from brailleDisplayDrivers import dotPad

		registrar = bdDetect.DriverRegistrar(dotPad.BrailleDisplayDriver.name)

		def matchFunc(match: bdDetect.DeviceMatch) -> bool:
			return match.id.startswith("DotPad")

		registrar.addBleDevices(matchFunc)

		stored_match_func = registrar._getDriverDict().get(bdDetect.CommunicationType.BLE)
		self.assertEqual(stored_match_func, matchFunc)
		self.assertTrue(callable(stored_match_func))

	@unittest.skip("Requires BLE support in bdDetect from #19122")
	def test_bleDeviceMatching(self):
		"""Test that BLE device matching works correctly."""
		from brailleDisplayDrivers import dotPad

		registrar = bdDetect.DriverRegistrar(dotPad.BrailleDisplayDriver.name)

		registrar.addBleDevices(dotPad.BrailleDisplayDriver._isBleDotPad)

		matching_device = bdDetect.DeviceMatch(
			type=bdDetect.ProtocolType.BLE,
			id="DotPad320",
			port="AA:BB:CC:DD:EE:FF",
			deviceInfo={"name": "DotPad320", "address": "AA:BB:CC:DD:EE:FF"},
		)

		non_matching_device = bdDetect.DeviceMatch(
			type=bdDetect.ProtocolType.BLE,
			id="SomeOtherDevice",
			port="11:22:33:44:55:66",
			deviceInfo={"name": "SomeOtherDevice", "address": "11:22:33:44:55:66"},
		)

		match_func = registrar._getDriverDict().get(bdDetect.CommunicationType.BLE)

		self.assertTrue(match_func(matching_device))
		self.assertFalse(match_func(non_matching_device))
