# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import time
from threading import Event
from typing import Callable

from _asyncioEventLoop.utils import runCoroutineSync
import extensionPoints
from logHandler import log

import bleak
from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

SCAN_CONTROL_TIMEOUT_SECONDS: int = 10
"""How long to wait for a scan to start or stop.

Both reach the Bluetooth stack, which can be slow to answer when the adapter is
busy, so the wait is bounded while staying generous enough not to give up on a
stack that is merely slow.
"""


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

		if isNew:
			log.debug(f"Discovered BLE device: {device.name or device.address}")

	def start(self, duration: float = 0):
		"""Start scanning for BLE devices.

		:param duration: If 0 (default), scan continues in background until stop() is called.
			If > 0, scan for specified duration in seconds then stop automatically.
		:raises bleak.exc.BleakError: If scanning could not be started, for example because
			the machine has no Bluetooth adapter or its radio is switched off.
		"""
		log.debug("Scanning for devices")
		# Clear device cache only on first start to allow multiple callers to share results
		if not self._isScanning.is_set():
			self._discoveredDevices.clear()
		# Waiting for the result lets a refused start reach the caller. Bleak refuses
		# when the machine has no Bluetooth adapter or its radio is off, and a scan that
		# never started must not be recorded as running: that would suppress every later
		# attempt and leave callers waiting for results that cannot arrive.
		runCoroutineSync(self._scanner.start(), SCAN_CONTROL_TIMEOUT_SECONDS)
		self._isScanning.set()
		if duration > 0:
			time.sleep(duration)
			self.stop()

	def stop(self):
		"""Stop scanning.

		:raises bleak.exc.BleakError: If the scan could not be stopped.
		"""
		# Waiting means the watcher has really stopped before this returns. Starting a
		# new scan while the old one is still running is refused by Bleak.
		runCoroutineSync(self._scanner.stop(), SCAN_CONTROL_TIMEOUT_SECONDS)
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
