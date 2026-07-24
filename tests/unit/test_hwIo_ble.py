# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the hwIo.ble module.

These tests cover the BLE scanner, BLE I/O, and device discovery functionality.
"""

import unittest
from unittest.mock import MagicMock, patch

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData
from hwIo.ble._scanner import Scanner
from hwIo.ble._io import Ble
from hwIo.ble import findDeviceByAddress


class TestScanner(unittest.TestCase):
	"""Tests for hwIo.ble.Scanner"""

	def setUp(self):
		"""Set up patches and create Scanner instance."""

		self.bleakScannerPatcher = patch("hwIo.ble._scanner.bleak.BleakScanner")
		self.mockBleakScannerClass = self.bleakScannerPatcher.start()

		mockFuture = MagicMock()
		mockFuture.result.return_value = None
		mockFuture.exception.return_value = None

		def fakeRunCoroutine(coro: object) -> MagicMock:
			if hasattr(coro, "close"):
				coro.close()  # ty: ignore[call-non-callable]
			return mockFuture

		self.runCoroutinePatcher = patch(
			"hwIo.ble._scanner.runCoroutine",
			side_effect=fakeRunCoroutine,
		)
		self.mockRunCoroutine = self.runCoroutinePatcher.start()

		# Use regular MagicMock for start/stop: the coroutines they
		# return are immediately closed by fakeRunCoroutine without
		# being awaited, so they don't need to be awaitable.
		self.mockScannerInstance = MagicMock()
		self.mockBleakScannerClass.return_value = self.mockScannerInstance

		self.Scanner = Scanner

	def tearDown(self):
		"""Clean up patches."""

		self.runCoroutinePatcher.stop()
		self.bleakScannerPatcher.stop()

	def test_startScanning(self):
		"""Test that starting scan calls Bleak scanner and sets isScanning flag."""
		scanner = self.Scanner()

		self.assertFalse(scanner.isScanning)

		scanner.start(duration=0)

		self.mockScannerInstance.start.assert_called_once()
		self.assertTrue(scanner.isScanning)

	def test_stopScanning(self):
		"""Test that stopping scan calls Bleak scanner and clears isScanning flag."""
		scanner = self.Scanner()
		scanner.start(duration=0)

		self.assertTrue(scanner.isScanning)

		scanner.stop()

		self.mockScannerInstance.stop.assert_called_once()
		self.assertFalse(scanner.isScanning)

	def test_deviceDiscoveredExtensionPoint(self):
		"""Test that deviceDiscovered extension point fires when device is advertised."""
		scanner = self.Scanner()

		handlerCalls = []

		def testHandler(device: BLEDevice, advertisementData: AdvertisementData, isNew: bool) -> None:
			handlerCalls.append(
				{
					"device": device,
					"advertisementData": advertisementData,
					"isNew": isNew,
				},
			)

		scanner.deviceDiscovered.register(testHandler)

		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"
		fakeAdvData = MagicMock(spec=AdvertisementData)

		scanner._onDeviceAdvertised(fakeDevice, fakeAdvData)

		self.assertEqual(len(handlerCalls), 1)
		self.assertEqual(handlerCalls[0]["device"], fakeDevice)
		self.assertEqual(handlerCalls[0]["advertisementData"], fakeAdvData)
		self.assertTrue(handlerCalls[0]["isNew"])

		# Same device again - should not be new
		scanner._onDeviceAdvertised(fakeDevice, fakeAdvData)

		self.assertEqual(len(handlerCalls), 2)
		self.assertFalse(handlerCalls[1]["isNew"])

	def test_deviceTracking(self):
		"""Test that devices are tracked in internal dict and returned by results()."""
		scanner = self.Scanner()

		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"
		fakeAdvData = MagicMock(spec=AdvertisementData)

		self.assertEqual(len(scanner.results()), 0)

		scanner._onDeviceAdvertised(fakeDevice, fakeAdvData)

		self.assertIn(fakeDevice.address, scanner._discoveredDevices)
		self.assertEqual(scanner._discoveredDevices[fakeDevice.address], fakeDevice)

		results = scanner.results()
		self.assertEqual(len(results), 1)
		self.assertEqual(results[0], fakeDevice)

	def test_resultsFiltering(self):
		"""Test that results() filter function works correctly."""
		scanner = self.Scanner()

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

		scanner._onDeviceAdvertised(device1, fakeAdvData)
		scanner._onDeviceAdvertised(device2, fakeAdvData)
		scanner._onDeviceAdvertised(device3, fakeAdvData)

		allResults = scanner.results()
		self.assertEqual(len(allResults), 3)

		filteredResults = scanner.results(filterFunc=lambda d: d.name.startswith("Test"))
		self.assertEqual(len(filteredResults), 2)
		self.assertIn(device1, filteredResults)
		self.assertIn(device3, filteredResults)
		self.assertNotIn(device2, filteredResults)


class TestBle(unittest.TestCase):
	"""Tests for hwIo.ble.Ble"""

	def setUp(self):
		"""Set up patches for Ble testing."""

		self.bleakClientPatcher = patch("hwIo.ble._io.bleak.BleakClient")
		self.mockBleakClientClass = self.bleakClientPatcher.start()

		# Use regular MagicMock for client methods (not AsyncMock):
		# the Ble class wraps every async call in runCoroutineSync(),
		# which is itself mocked, so the coroutines returned by
		# _initAndConnect / disconnect / write_gatt_char are immediately
		# closed by fakeRunCoroutineSync without ever being awaited. The
		# inner self._client.connect() etc. are therefore never called,
		# so they don't need to be awaitable.
		self.mockClient = MagicMock()
		self.mockClient.is_connected = True
		self.mockBleakClientClass.return_value = self.mockClient

		self.mockService = MagicMock()
		self.mockCharacteristic = MagicMock()
		self.mockCharacteristic.max_write_without_response_size = 20
		self.mockService.get_characteristic.return_value = self.mockCharacteristic

		self.mockServices = MagicMock()
		self.mockServices.get_service.return_value = self.mockService
		mockServicesDict = MagicMock()
		# Configure the MagicMock's __len__ via return_value because Python
		# looks up dunder methods on the type, not the instance.
		mockServicesDict.__len__.return_value = 1
		mockServicesDict.values.return_value = [self.mockService]
		self.mockServices.services = mockServicesDict
		self.mockClient.services = self.mockServices

		# Ble uses runCoroutineSync() which blocks until the coroutine
		# completes and returns the result directly. Close the passed
		# coroutine immediately so Python does not warn about "coroutine
		# was never awaited" — the mock will never actually run it.
		def fakeRunCoroutineSync(coro: object, timeout: float | None = None) -> None:
			if hasattr(coro, "close"):
				coro.close()  # ty: ignore[call-non-callable]
			return None

		self.runCoroutineSyncPatcher = patch(
			"hwIo.ble._io.runCoroutineSync",
			side_effect=fakeRunCoroutineSync,
		)
		self.mockRunCoroutineSync = self.runCoroutineSyncPatcher.start()

		self.Ble = Ble
		# Track Ble instances so tearDown can close them while patches
		# are still active (avoiding __del__ errors at GC time when the
		# real runCoroutineSync would be called against a dead event
		# loop).
		self._bleInstances: list[Ble] = []

	def tearDown(self):
		"""Clean up Ble instances and patches."""

		# Mark the mock client disconnected so the close() called from
		# Ble.__del__ at GC time becomes a no-op (it would otherwise hit
		# the real, unmocked runCoroutineSync and raise).
		self.mockClient.is_connected = False
		for ble in self._bleInstances:
			try:
				ble.close()
			except Exception:
				pass
		self.runCoroutineSyncPatcher.stop()
		self.bleakClientPatcher.stop()

	def _makeBle(self, **kwargs) -> "object":
		"""Construct a Ble instance and track it for cleanup."""

		ble = self.Ble(**kwargs)
		self._bleInstances.append(ble)
		return ble

	def test_connectionSuccess(self):
		"""Test that Ble connects successfully and starts notifications."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"

		mockIoThread = MagicMock()

		receivedData = []

		def onReceive(data: bytes) -> None:
			receivedData.append(data)

		ble = self._makeBle(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=onReceive,
			ioThread=mockIoThread,
		)

		self.mockBleakClientClass.assert_called_once()
		callArgs = self.mockBleakClientClass.call_args
		self.assertEqual(callArgs[0][0], mockDevice)

		self.mockRunCoroutineSync.assert_called()
		self.assertTrue(ble.isConnected())

	def test_writeData(self):
		"""Test writing data to BLE characteristic."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		ble = self._makeBle(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=lambda data: None,
			ioThread=mockIoThread,
		)

		testData = b"test data"
		ble.write(testData)

		self.mockServices.get_service.assert_called_with("service-uuid")
		self.mockService.get_characteristic.assert_called_with("write-char-uuid")

		self.assertGreater(self.mockRunCoroutineSync.call_count, 1)

	def test_writeDataChunking(self):
		"""Test that large data is split into MTU-sized chunks."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		self.mockCharacteristic.max_write_without_response_size = 10

		ble = self._makeBle(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=lambda data: None,
			ioThread=mockIoThread,
		)

		initialCallCount = self.mockRunCoroutineSync.call_count

		testData = b"A" * 25
		ble.write(testData)

		writeCalls = self.mockRunCoroutineSync.call_count - initialCallCount
		self.assertEqual(writeCalls, 3)

	def test_receiveNotification(self):
		"""Test receiving data via BLE notification."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		receivedData: list[bytes] = []

		def onReceive(data: bytes) -> None:
			receivedData.append(data)

		ble = self._makeBle(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=onReceive,
			ioThread=mockIoThread,
		)

		self.mockRunCoroutineSync.assert_called()

		testData = bytearray(b"notification data")
		mockChar = MagicMock()
		ble._notifyReceive(mockChar, testData)

		self.assertFalse(ble._queuedData.empty())

	def test_closeCleanup(self):
		"""Test that close() properly disconnects and cleans up resources."""
		mockDevice = MagicMock(spec=BLEDevice)
		mockDevice.address = "AA:BB:CC:DD:EE:FF"
		mockDevice.name = "TestDevice"
		mockIoThread = MagicMock()

		ble = self._makeBle(
			device=mockDevice,
			writeServiceUuid="service-uuid",
			writeCharacteristicUuid="write-char-uuid",
			readServiceUuid="service-uuid",
			readCharacteristicUuid="read-char-uuid",
			onReceive=lambda data: None,
			ioThread=mockIoThread,
		)

		ble.close()

		self.assertGreater(self.mockRunCoroutineSync.call_count, 1)
		self.assertIsNone(ble._onReceive)


class TestFindDeviceByAddress(unittest.TestCase):
	"""Tests for hwIo.ble.findDeviceByAddress"""

	def setUp(self):
		"""Set up patches for findDeviceByAddress testing."""

		self.scannerPatcher = patch("hwIo.ble.scanner")
		self.mockScanner = self.scannerPatcher.start()

		# findDeviceByAddress is decorated with @requiresBackgroundThread; patch out the
		# main-thread check so tests can call it directly without spawning threads.
		self.mainThreadPatcher = patch("hwIo.base.threading.main_thread", return_value=MagicMock())
		self.mainThreadPatcher.start()

		self.findDeviceByAddress = findDeviceByAddress

	def tearDown(self):
		"""Clean up patches."""

		self.mainThreadPatcher.stop()
		self.scannerPatcher.stop()

	def test_deviceAlreadyInResults(self):
		"""Test finding device that's already in scanner results."""
		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"

		self.mockScanner.results.return_value = [fakeDevice]
		self.mockScanner.isScanning = False

		result = self.findDeviceByAddress("AA:BB:CC:DD:EE:FF")

		self.assertEqual(result, fakeDevice)
		self.mockScanner.start.assert_not_called()

	def test_deviceNotFound(self):
		"""Test that None is returned when device is not found after timeout."""
		self.mockScanner.results.return_value = []
		self.mockScanner.isScanning = False

		result = self.findDeviceByAddress("AA:BB:CC:DD:EE:FF", timeout=0.1)

		self.assertIsNone(result)
		self.mockScanner.start.assert_called_once()

	def test_deviceFoundDuringScan(self):
		"""Test finding device that appears during scanning."""
		fakeDevice = MagicMock(spec=BLEDevice)
		fakeDevice.address = "AA:BB:CC:DD:EE:FF"
		fakeDevice.name = "TestDevice"

		callCount = 0

		def mockResults() -> list[BLEDevice]:
			nonlocal callCount
			callCount += 1
			if callCount <= 1:
				return []
			else:
				return [fakeDevice]

		self.mockScanner.results.side_effect = mockResults
		self.mockScanner.isScanning = False

		result = self.findDeviceByAddress("AA:BB:CC:DD:EE:FF", timeout=0.5, pollInterval=0.05)

		self.assertEqual(result, fakeDevice)
		self.mockScanner.start.assert_called_once()
