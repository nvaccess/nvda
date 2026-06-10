# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Raw I/O for Bluetooth Low Energy (BLE) devices

This module provides classes for scanning for BLE devices and communicating with them.
It uses the Bleak library for BLE communication.

Only use this if you need access to a device that only implements BLE and not Bluetooth Classic.
Bluetooth Classic devices should be paired through Windows' Bluetooth settings and accessed through the related serial/HID device.
"""

import time
from bleak.exc import BleakError
from bleak.backends.device import BLEDevice
from logHandler import log

from ._scanner import Scanner
from ._io import Ble
from ..base import requiresBackgroundThread

__all__ = ["Scanner", "Ble", "scanner", "findDeviceByAddress"]

#: Module-level singleton scanner shared by all BLE consumers.
#: Using a single scanner avoids contention over the Windows BLE stack and
#: lets multiple callers share the set of already-discovered devices.
#: None until initialize() is called.
scanner: Scanner | None = None


def initialize() -> None:
	"""Initialize the hwIo.ble module, creating the shared BLE scanner singleton."""
	log.debug("Initializing BLE I/O")
	global scanner
	scanner = Scanner()


def terminate() -> None:
	"""Terminate the hwIo.ble module, stopping any active BLE scan and releasing the scanner."""
	log.debug("Terminating BLE I/O")
	global scanner
	if scanner is not None:
		if scanner.isScanning:
			scanner.stop()
		scanner = None


@requiresBackgroundThread
def findDeviceByAddress(address: str, timeout: float = 5.0, pollInterval: float = 0.1) -> BLEDevice | None:
	"""Find a BLE device by its address.

	Checks already-discovered devices first, then scans if needed.

	:param address: The BLE device address (MAC address)
	:param timeout: Maximum time to scan in seconds (default 5.0)
	:param pollInterval: How often to check results in seconds (default 0.1)
	:return: The BLE device object if found, None otherwise
	"""
	if scanner is None:
		raise RuntimeError("hwIo.ble.initialize() must be called before using findDeviceByAddress")
	log.debug(f"Searching for BLE device with address {address}")

	# Check if device already discovered
	for device in scanner.results():
		if device.address == address:
			log.debug(f"Found BLE device {address} in existing results")
			return device

	# Not found - start scanning if not already running
	if not scanner.isScanning:
		try:
			scanner.start()  # Start in background mode
		except (BleakError, OSError):
			log.error(f"Failed to start BLE scanner while searching for device {address}", exc_info=True)
			return None

	startTime = time.time()
	while time.time() - startTime < timeout:
		time.sleep(pollInterval)

		# Check if device appeared
		for device in scanner.results():
			if device.address == address:
				elapsed = time.time() - startTime
				log.debug(f"Found BLE device {address} after {elapsed:.2f}s")
				return device

	# Timeout - device not found
	log.debug(f"BLE device {address} not found after {timeout}s timeout")
	return None
