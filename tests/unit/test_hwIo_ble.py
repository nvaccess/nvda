# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2025 NV Access Limited, Dot Incorporated, Bram Duvigneau

"""Unit tests for the hwIo.ble module."""

import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


class TestScanner(unittest.TestCase):
	"""Tests for hwIo.ble.Scanner"""

	def setUp(self):
		"""Set up patches and create Scanner instance."""
		# Patch bleak.BleakScanner before importing
		self.bleakScannerPatcher = patch("hwIo.ble._scanner.bleak.BleakScanner")
		self.mockBleakScannerClass = self.bleakScannerPatcher.start()

		# Patch runCoroutine to avoid async event loop issues in tests
		self.runCoroutinePatcher = patch("hwIo.ble._scanner.runCoroutine")
		self.mockRunCoroutine = self.runCoroutinePatcher.start()
		# Make runCoroutine return a completed future
		mockFuture = MagicMock()
		mockFuture.result.return_value = None
		mockFuture.exception.return_value = None
		self.mockRunCoroutine.return_value = mockFuture

		# Create mock scanner instance
		self.mockScannerInstance = MagicMock()
		self.mockScannerInstance.start = AsyncMock()
		self.mockScannerInstance.stop = AsyncMock()
		self.mockBleakScannerClass.return_value = self.mockScannerInstance

		# Import Scanner after patching
		from hwIo.ble._scanner import Scanner

		self.Scanner = Scanner

	def tearDown(self):
		"""Clean up patches."""
		self.runCoroutinePatcher.stop()
		self.bleakScannerPatcher.stop()

	def test_startScanning(self):
		"""Test that starting scan calls Bleak scanner and sets isScanning flag."""
		scanner = self.Scanner()

		# Initially not scanning
		self.assertFalse(scanner.isScanning)

		# Start scanning in background mode
		scanner.start(duration=0)

		# Verify Bleak scanner was started
		self.mockScannerInstance.start.assert_called_once()

		# Verify isScanning flag is set
		self.assertTrue(scanner.isScanning)

	def test_stopScanning(self):
		"""Test that stopping scan calls Bleak scanner and clears isScanning flag."""
		scanner = self.Scanner()
		scanner.start(duration=0)

		# Verify scanning
		self.assertTrue(scanner.isScanning)

		# Stop scanning
		scanner.stop()

		# Verify Bleak scanner was stopped
		self.mockScannerInstance.stop.assert_called_once()

		# Verify isScanning flag is cleared
		self.assertFalse(scanner.isScanning)

	def test_deviceDiscoveredExtensionPoint(self):
		"""Test that deviceDiscovered extension point fires when device is advertised."""
		scanner = self.Scanner()

		# Track handler calls
		handlerCalls = []

		def testHandler(device, advertisementData, isNew):
			handlerCalls.append(
				{
					"device": device,
					"advertisementData": advertisementData,
					"isNew": isNew,
				},
			)

		# Register handler - keep reference to prevent weak ref cleanup
		scanner.deviceDiscovered.register(testHandler)

		# Create fake device and advertisement data
		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"
		fakeAdvData = MagicMock(spec=AdvertisementData)

		# Trigger device discovery
		scanner._onDeviceAdvertised(fakeDevice, fakeAdvData)

		# Verify handler was called once
		self.assertEqual(len(handlerCalls), 1)

		# Verify handler received correct arguments
		self.assertEqual(handlerCalls[0]["device"], fakeDevice)
		self.assertEqual(handlerCalls[0]["advertisementData"], fakeAdvData)
		self.assertTrue(handlerCalls[0]["isNew"])

		# Trigger same device again - should not be new
		scanner._onDeviceAdvertised(fakeDevice, fakeAdvData)

		# Verify handler was called again
		self.assertEqual(len(handlerCalls), 2)
		self.assertFalse(handlerCalls[1]["isNew"])

	def test_deviceTracking(self):
		"""Test that devices are tracked in internal dict and returned by results()."""
		scanner = self.Scanner()

		# Create fake device
		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"
		fakeAdvData = MagicMock(spec=AdvertisementData)

		# Initially no devices
		self.assertEqual(len(scanner.results()), 0)

		# Trigger device discovery
		scanner._onDeviceAdvertised(fakeDevice, fakeAdvData)

		# Verify device is tracked
		self.assertIn(fakeDevice.address, scanner._discoveredDevices)
		self.assertEqual(scanner._discoveredDevices[fakeDevice.address], fakeDevice)

		# Verify device is in results
		results = scanner.results()
		self.assertEqual(len(results), 1)
		self.assertEqual(results[0], fakeDevice)

	def test_resultsFiltering(self):
		"""Test that results() filter function works correctly."""
		scanner = self.Scanner()

		# Create multiple fake devices
		device1 = MagicMock(spec=BLEDevice)
		device1.address = "AA:BB:CC:DD:EE:01"
		device1.name = "TestDevice1"

		device2 = MagicMock(spec=BLEDevice)
		device2.address = "AA:BB:CC:DD:EE:02"
		device2.name = "OtherDevice"

		device3 = MagicMock(spec=BLEDevice)
		device3.address = "AA:BB:CC:DD:EE:03"
		device3.name = "TestDevice2"

		fakeAdvData = MagicMock(spec=AdvertisementData)

		# Add devices
		scanner._onDeviceAdvertised(device1, fakeAdvData)
		scanner._onDeviceAdvertised(device2, fakeAdvData)
		scanner._onDeviceAdvertised(device3, fakeAdvData)

		# Get all results
		allResults = scanner.results()
		self.assertEqual(len(allResults), 3)

		# Filter for devices starting with "Test"
		filteredResults = scanner.results(filterFunc=lambda d: d.name.startswith("Test"))
		self.assertEqual(len(filteredResults), 2)
		self.assertIn(device1, filteredResults)
		self.assertIn(device3, filteredResults)
		self.assertNotIn(device2, filteredResults)


class TestBle(unittest.TestCase):
	"""Tests for hwIo.ble.Ble"""

	def setUp(self):
		"""Set up patches for Ble testing."""
		# Patch BleakClient
		self.bleakClientPatcher = patch("hwIo.ble._io.bleak.BleakClient")
		self.mockBleakClientClass = self.bleakClientPatcher.start()

		# Create mock client instance
		self.mockClient = MagicMock()
		self.mockClient.connect = AsyncMock()
		self.mockClient.disconnect = AsyncMock()
		self.mockClient.start_notify = AsyncMock()
		self.mockClient.write_gatt_char = AsyncMock()
		self.mockClient.is_connected = True
		self.mockBleakClientClass.return_value = self.mockClient

		# Mock services - needs to have at least one service for waitForConnection
		self.mockService = MagicMock()
		self.mockCharacteristic = MagicMock()
		self.mockCharacteristic.max_write_without_response_size = 20
		self.mockService.get_characteristic.return_value = self.mockCharacteristic

		# Create mock services object
		self.mockServices = MagicMock()
		self.mockServices.get_service.return_value = self.mockService
		# Create a mock services collection
		mockServicesDict = MagicMock()
		mockServicesDict.__len__ = lambda self: 1  # Non-empty to pass waitForConnection
		mockServicesDict.values.return_value = [self.mockService]
		self.mockServices.services = mockServicesDict
		self.mockClient.services = self.mockServices

		# Patch runCoroutineSync (just returns None, as it's a synchronous wrapper)
		self.runCoroutineSyncPatcher = patch("hwIo.ble._io.runCoroutineSync")
		self.mockRunCoroutineSync = self.runCoroutineSyncPatcher.start()
		self.mockRunCoroutineSync.return_value = None

		# Import Ble after patching
		from hwIo.ble._io import Ble

		self.Ble = Ble

	def tearDown(self):
		"""Clean up patches."""
		self.runCoroutineSyncPatcher.stop()
		self.bleakClientPatcher.stop()

	def test_connectionSuccess(self):
		"""Test that Ble connects successfully and starts notifications."""
		# Create mock device and IoThread
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"

		mockIoThread = MagicMock()

		# Track onReceive calls
		receivedData = []

		def onReceive(data):
			receivedData.append(data)

		# Create Ble instance
		ble = self.Ble(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=onReceive,
			ioThread=mockIoThread,
		)

		# Verify BleakClient was created with device
		self.mockBleakClientClass.assert_called_once()
		callArgs = self.mockBleakClientClass.call_args
		self.assertEqual(callArgs[0][0], mockDevice)

		# Verify runCoroutineSync was called for initialization
		self.mockRunCoroutineSync.assert_called()

		# Verify the connection is established
		self.assertTrue(ble.isConnected())

	def test_writeData(self):
		"""Test writing data to BLE characteristic."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		ble = self.Ble(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=lambda data: None,
			ioThread=mockIoThread,
		)

		# Write data
		testData = b"test data"
		ble.write(testData)

		# Verify service and characteristic were retrieved
		self.mockServices.get_service.assert_called_with("service-uuid")
		self.mockService.get_characteristic.assert_called_with("write-char-uuid")

		# Verify write was called (through runCoroutineSync)
		self.assertGreater(self.mockRunCoroutineSync.call_count, 1)  # At least init + write

	def test_writeDataChunking(self):
		"""Test that large data is split into MTU-sized chunks."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		# Set MTU size to 10
		self.mockCharacteristic.max_write_without_response_size = 10

		ble = self.Ble(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=lambda data: None,
			ioThread=mockIoThread,
		)

		# Reset call count after initialization
		initialCallCount = self.mockRunCoroutineSync.call_count

		# Write 25 bytes (should split into 3 chunks: 10, 10, 5)
		testData = b"A" * 25
		ble.write(testData)

		# Verify runCoroutineSync was called 3 times for writes
		writeCalls = self.mockRunCoroutineSync.call_count - initialCallCount
		self.assertEqual(writeCalls, 3)

	def test_receiveNotification(self):
		"""Test receiving data via BLE notification."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		# Track received data
		receivedData = []

		def onReceive(data):
			receivedData.append(data)

		ble = self.Ble(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=onReceive,
			ioThread=mockIoThread,
		)

		# Verify initialization occurred
		self.mockRunCoroutineSync.assert_called()

		# Simulate notification by calling _notifyReceive directly
		testData = bytearray(b"notification data")
		mockChar = MagicMock()
		ble._notifyReceive(mockChar, testData)

		# Verify data was queued
		self.assertFalse(ble._queuedData.empty())

	def test_closeCleanup(self):
		"""Test that close() properly disconnects and cleans up resources."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		ble = self.Ble(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=lambda data: None,
			ioThread=mockIoThread,
		)

		# Close the connection
		ble.close()

		# Verify disconnect was called via runCoroutineSync (init + close)
		self.assertGreater(self.mockRunCoroutineSync.call_count, 1)

		# Verify onReceive callback was cleared
		self.assertIsNone(ble._onReceive)


class TestFindDeviceByAddress(unittest.TestCase):
	"""Tests for hwIo.ble.findDeviceByAddress"""

	def setUp(self):
		"""Set up patches for findDeviceByAddress testing."""
		# Patch the scanner module-level instance
		self.scannerPatcher = patch("hwIo.ble.scanner")
		self.mockScanner = self.scannerPatcher.start()

		# Import function after patching
		from hwIo.ble import findDeviceByAddress

		self.findDeviceByAddress = findDeviceByAddress

	def tearDown(self):
		"""Clean up patches."""
		self.scannerPatcher.stop()

	def test_deviceAlreadyInResults(self):
		"""Test finding device that's already in scanner results."""
		# Create fake device
		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"

		# Mock scanner to return device immediately
		self.mockScanner.results.return_value = [fakeDevice]
		self.mockScanner.isScanning = False

		# Find device
		result = self.findDeviceByAddress("AA:BB:CC:DD:EE:FF")

		# Verify device was found
		self.assertEqual(result, fakeDevice)

		# Verify scanner was not started (device already in results)
		self.mockScanner.start.assert_not_called()

	def test_deviceNotFound(self):
		"""Test that None is returned when device is not found after timeout."""
		# Mock scanner to return empty results
		self.mockScanner.results.return_value = []
		self.mockScanner.isScanning = False

		# Find device with short timeout
		result = self.findDeviceByAddress("AA:BB:CC:DD:EE:FF", timeout=0.1)

		# Verify None was returned
		self.assertIsNone(result)

		# Verify scanner was started
		self.mockScanner.start.assert_called_once()

	def test_deviceFoundDuringScan(self):
		"""Test finding device that appears during scanning."""
		# Create fake device
		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"

		# Simulate device appearing after a delay
		callCount = 0

		def mockResults():
			nonlocal callCount
			callCount += 1
			if callCount <= 1:
				# First call - no devices
				return []
			else:
				# Subsequent calls - device appears
				return [fakeDevice]

		self.mockScanner.results.side_effect = mockResults
		self.mockScanner.isScanning = False

		# Find device with reasonable timeout
		result = self.findDeviceByAddress("AA:BB:CC:DD:EE:FF", timeout=0.5, pollInterval=0.05)

		# Verify device was found
		self.assertEqual(result, fakeDevice)

		# Verify scanner was started
		self.mockScanner.start.assert_called_once()
