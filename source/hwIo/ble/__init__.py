# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Dot Incorporated, Bram Duvigneau
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Raw I/O for Bluetooth Low Energy (BLE) devices

This module provides classes for scanning for BLE devices and communicating with them.
It uses the Bleak library for BLE communication.

Only use this if you need access to a device that only implements BLE and not Bluetooth Classic.
Bluetooth Classic devices should be paired through Windows' Bluetooth settings and accessed through the related serial/HID device.
"""

import time
from bleak.backends.device import BLEDevice
from logHandler import log

from ._scanner import Scanner  # noqa: F401
from ._io import Ble  # noqa: F401

# Module-level singleton scanner for all BLE operations
scanner = Scanner()


def findDeviceByAddress(address: str, timeout: float = 5.0, pollInterval: float = 0.1) -> BLEDevice | None:
	"""Find a BLE device by its address.

	Checks already-discovered devices first, then scans if needed.

	:param address: The BLE device address (MAC address)
	:param timeout: Maximum time to scan in seconds (default 5.0)
	:param pollInterval: How often to check results in seconds (default 0.1)
	:return: The BLE device object if found, None otherwise
	"""
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
		except Exception:
			log.error(f"Failed to start BLE scanner while searching for device {address}", exc_info=True)
			return None

	try:
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
	except Exception:
		log.error(f"Error while scanning for BLE device {address}", exc_info=True)
		return None
