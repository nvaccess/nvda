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

from __future__ import annotations

import time
from typing import TYPE_CHECKING

from logHandler import log

from ..base import requiresBackgroundThread
from ._io import Ble
from ._scanner import Scanner

if TYPE_CHECKING:
	from bleak.backends.device import BLEDevice

__all__ = ["Ble", "Scanner", "findDeviceByAddress", "scanner"]

#: Module-level singleton scanner shared by all BLE consumers.
#: Using a single scanner avoids contention over the Windows BLE stack and
#: lets multiple callers share the set of already-discovered devices.
#: None until a BLE device lookup is first attempted.
scanner: Scanner | None = None


def initialize() -> None:
	"""Initialize the hwIo.ble module.

	The BLE scanner singleton is created lazily on first use to avoid
	importing the heavy bleak library at startup when no BLE device is connected.
	"""
	log.debug("Initializing BLE I/O")


def terminate() -> None:
	"""Terminate the hwIo.ble module, stopping any active BLE scan and releasing the scanner."""
	log.debug("Terminating BLE I/O")
	global scanner
	if scanner is not None:
		if scanner.isScanning:
			scanner.stop()
		scanner = None


def _ensureScanner() -> Scanner:
	"""Return the shared scanner, creating it on first call."""
	global scanner
	if scanner is None:
		scanner = Scanner()
	return scanner


@requiresBackgroundThread
def findDeviceByAddress(address: str, timeout: float = 5.0, pollInterval: float = 0.1) -> BLEDevice | None:
	"""Find a BLE device by its address.

	Checks already-discovered devices first, then scans if needed.

	:param address: The BLE device address (MAC address)
	:param timeout: Maximum time to scan in seconds (default 5.0)
	:param pollInterval: How often to check results in seconds (default 0.1)
	:return: The BLE device object if found, None otherwise
	"""
	_scanner = _ensureScanner()
	log.debug(f"Searching for BLE device with address {address}")

	# Check if device already discovered
	for device in _scanner.results():
		if device.address == address:
			log.debug(f"Found BLE device {address} in existing results")
			return device

	# Not found - start scanning if not already running
	if not _scanner.isScanning:
		# Delayed import of bleak to avoid importing it at NVDA startup,
		# slowing down the startup time when no BLE device is connected.
		from bleak.exc import BleakError
		try:
			_scanner.start()  # Start in background mode
		except (BleakError, OSError):
			log.error(f"Failed to start BLE scanner while searching for device {address}", exc_info=True)  # noqa: G201
			return None

	startTime = time.time()
	while time.time() - startTime < timeout:
		time.sleep(pollInterval)

		# Check if device appeared
		for device in _scanner.results():
			if device.address == address:
				elapsed = time.time() - startTime
				log.debug(f"Found BLE device {address} after {elapsed:.2f}s")
				return device

	# Timeout - device not found
	log.debug(f"BLE device {address} not found after {timeout}s timeout")
	return None
