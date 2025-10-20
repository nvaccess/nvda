import time
from threading import Event
from typing import Callable

from asyncioEventLoop import runCoroutine
import extensionPoints
from logHandler import log

import bleak
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData


class Scanner:
	"""Scan for BLE devices

	This is a small synchronous wrapper around Bleak's Scanner.
	It allows starting and stopping scans, retrieving results, and checking if scanning is active.
	"""

	_scanner: bleak.BleakScanner
	_discoveredDevices: dict[str, BLEDevice]
	_isScanning: Event

	def __init__(self):
		self._discoveredDevices = {}
		self._scanner = bleak.BleakScanner(self._onDeviceAdvertised)
		self._isScanning = Event()
		#: Action called when a BLE device is discovered or re-advertises.
		#: Handlers receive: device (BLEDevice), advertisementData (AdvertisementData), isNew (bool)
		self.deviceDiscovered = extensionPoints.Action()

	def _onDeviceAdvertised(self, device: BLEDevice, adv: AdvertisementData) -> None:
		# Check if this is a new device before updating the dict
		isNew = device.address not in self._discoveredDevices

		# Store all devices, even those without a local_name
		# Devices without names can still be found by address in findDeviceByAddress()
		self._discoveredDevices[device.address] = device

		# Notify extension point handlers
		self.deviceDiscovered.notify(device=device, advertisementData=adv, isNew=isNew)

		# Play a tone for newly discovered devices
		if isNew:
			log.debug(f"Discovered BLE device: {device.name or device.address}")

	def start(self, duration: float = 0):
		"""Start scanning for BLE devices.

		:param duration: If 0 (default), scan continues in background until stop() is called.
			If > 0, scan for specified duration in seconds then stop automatically.
		"""
		log.debug("Scanning for devices")
		# Clear device cache only on first start to allow multiple callers to share results
		if not self._isScanning.is_set():
			self._discoveredDevices.clear()
		self._isScanning.set()
		runCoroutine(self._scanner.start())
		if duration > 0:
			time.sleep(duration)
			runCoroutine(self._scanner.stop())
			self._isScanning.clear()

	def stop(self):
		"""Stop scanning"""
		runCoroutine(self._scanner.stop())
		self._isScanning.clear()

	def results(self, filterFunc: Callable[[BLEDevice], bool] | None = None) -> list[BLEDevice]:
		"""Get the discovered BLE devices.

		:param filterFunc: Optional filter function to select specific devices.
		:return: List of BLE devices found during the scan, optionally filtered.
		"""
		results = list(self._discoveredDevices.values())
		if filterFunc:
			results = [device for device in results if filterFunc(device)]
		return results

	@property
	def isScanning(self) -> bool:
		"""Check if scanning is currently active"""
		return self._isScanning.is_set()
