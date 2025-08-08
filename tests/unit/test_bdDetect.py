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


class TestGenericDeviceDetection(unittest.TestCase):
	"""Tests for generic USB-to-serial device detection."""

	def test_isGenericUsbDevice_withGenericVidPidAndGenericDescription(self):
		"""Test that devices with generic VID/PID and generic descriptions are detected as generic."""
		test_cases = [
			("VID_0403&PID_6001", {"busDescription": "USB Serial Port"}),
			("VID_0403&PID_6001", {"busDescription": "FTDI USB Serial Device"}),
			("VID_1A86&PID_7523", {"busDescription": "CH340 USB to Serial"}),
			("VID_067B&PID_2303", {"busDescription": "Prolific USB-to-Serial Comm Port"}),
			("VID_10C4&PID_EA60", {"busDescription": "Silicon Labs CP210x USB to UART Bridge"}),
		]
		for usbId, deviceInfo in test_cases:
			with self.subTest(usbId=usbId, deviceInfo=deviceInfo):
				result = bdDetect._isGenericUsbDevice(usbId, deviceInfo)
				self.assertTrue(result)

	def test_isGenericUsbDevice_withGenericVidPidAndNoBusDescription(self):
		"""Test that devices with generic VID/PID but no busDescription are detected as generic."""
		test_cases = [
			("VID_0403&PID_6001", {}),
			("VID_0403&PID_6001", {"busDescription": ""}),
			("VID_1A86&PID_7523", {"someOtherField": "value"}),
		]
		for usbId, deviceInfo in test_cases:
			with self.subTest(usbId=usbId, deviceInfo=deviceInfo):
				result = bdDetect._isGenericUsbDevice(usbId, deviceInfo)
				self.assertTrue(result)

	def test_isGenericUsbDevice_withGenericVidPidButSpecificDescription(self):
		"""Test that devices with generic VID/PID but specific descriptions are NOT detected as generic."""
		test_cases = [
			("VID_0403&PID_6001", {"busDescription": "DotPad Braille Display"}),
			("VID_0403&PID_6001", {"busDescription": "HumanWare Brailliant"}),
			("VID_1A86&PID_7523", {"busDescription": "NLS eReader Zoomax Braille Device"}),
			("VID_067B&PID_2303", {"busDescription": "Papenmeier Braille Terminal"}),
		]
		for usbId, deviceInfo in test_cases:
			with self.subTest(usbId=usbId, deviceInfo=deviceInfo):
				result = bdDetect._isGenericUsbDevice(usbId, deviceInfo)
				self.assertFalse(result)

	def test_isGenericUsbDevice_withNonGenericVidPid(self):
		"""Test that devices with non-generic VID/PID are never detected as generic."""
		test_cases = [
			("VID_1234&PID_5678", {"busDescription": "USB Serial Port"}),
			("VID_ABCD&PID_EFGH", {}),
			("VID_0F4E&PID_0100", {"busDescription": "FTDI Serial Converter"}),
		]
		for usbId, deviceInfo in test_cases:
			with self.subTest(usbId=usbId, deviceInfo=deviceInfo):
				result = bdDetect._isGenericUsbDevice(usbId, deviceInfo)
				self.assertFalse(result)

	def test_isGenericUsbDevice_caseInsensitive(self):
		"""Test that bus description matching is case-insensitive."""
		test_cases = [
			("VID_0403&PID_6001", {"busDescription": "USB SERIAL PORT"}),
			("VID_0403&PID_6001", {"busDescription": "Ftdi USB Serial Device"}),
			("VID_1A86&PID_7523", {"busDescription": "CH340 usb-serial controller"}),
		]
		for usbId, deviceInfo in test_cases:
			with self.subTest(usbId=usbId, deviceInfo=deviceInfo):
				result = bdDetect._isGenericUsbDevice(usbId, deviceInfo)
				self.assertTrue(result)

	def test_deviceMatch_isGenericProperty(self):
		"""Test that DeviceMatch properly includes the isGeneric property."""
		# Generic device
		genericMatch = bdDetect.DeviceMatch(
			bdDetect.ProtocolType.SERIAL,
			"VID_0403&PID_6001",
			"COM1",
			{"busDescription": "USB Serial Port"},
			True,
		)
		self.assertTrue(genericMatch.isGeneric)

		# Non-generic device
		specificMatch = bdDetect.DeviceMatch(
			bdDetect.ProtocolType.SERIAL,
			"VID_0403&PID_6001",
			"COM2",
			{"busDescription": "DotPad Braille Display"},
			False,
		)
		self.assertFalse(specificMatch.isGeneric)

		# Default value should be False
		defaultMatch = bdDetect.DeviceMatch(
			bdDetect.ProtocolType.HID,
			"VID_1234&PID_5678",
			r"\\?\hid#vid_1234&pid_5678#1&2345678&0&0000#{4d1e55b2-f16f-11cf-88cb-001111000030}",
			{},
		)
		self.assertFalse(defaultMatch.isGeneric)
