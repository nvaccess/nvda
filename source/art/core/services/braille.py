# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Braille service for ART - handles braille displays from ART runtime."""

import threading
from typing import Dict, List, Any, Optional

import Pyro5.api
from logHandler import log
import inputCore

from .base import BaseService


@Pyro5.api.expose
class BrailleService(BaseService):
	"""Receives braille display registrations from ART and manages braille display operations."""

	def __init__(self):
		super().__init__("BrailleService")
		self._registeredDrivers: Dict[str, dict] = {}
		self._artProcessConnections: Dict[str, Any] = {}  # Maps driver names to ART service proxies
		self._activeDriver: Optional[str] = None
		self._lock = threading.Lock()

	def registerBrailleDriver(
		self,
		name: str,
		description: str,
		addon_name: str,
		numCells: int,
		numRows: int,
		numCols: int,
		supportedGestures: List[str],
		deviceInfo: Dict[str, Any],
		art_service_proxy: Any,
	) -> bool:
		"""Register a braille display driver from ART.

		@param name: The driver name (must match the module name)
		@param description: Human-readable description
		@param addon_name: The addon that provides this driver
		@param numCells: Number of braille cells (0 if multi-line display)
		@param numRows: Number of display rows (0 if single-line display)
		@param numCols: Number of display columns (0 if single-line display)
		@param supportedGestures: List of supported input gesture identifiers
		@param deviceInfo: Hardware detection and capability information
		@param art_service_proxy: Proxy to the ART BrailleDisplayService
		@return: True if registration successful
		"""
		log.debug(f"BrailleService.registerBrailleDriver called: name={name}, addon={addon_name}")
		try:
			with self._lock:
				self._registeredDrivers[name] = {
					"description": description,
					"addon_name": addon_name,
					"numCells": numCells,
					"numRows": numRows,
					"numCols": numCols,
					"supportedGestures": supportedGestures,
					"deviceInfo": deviceInfo,
					"isActive": False,
					"isAvailable": True,
				}

				# Store connection to ART service for this driver
				self._artProcessConnections[name] = art_service_proxy

				log.info(f"Registered ART braille driver: {name} from addon {addon_name}")
				log.debug(f"Driver specs: cells={numCells}, rows={numRows}, cols={numCols}")
				log.debug(f"Supported gestures: {supportedGestures}")

				# TODO: Integrate with existing BrailleHandler.getDisplayList()
				# This will require modifying source/braille.py to include ART drivers

				log.debug(f"Registration completed successfully for {name}")
				return True
		except Exception:
			self._log_error("registerBrailleDriver", name)
			return False

	def unregisterBrailleDriver(self, name: str) -> bool:
		"""Unregister a braille display driver.

		@param name: The driver name to unregister
		@return: True if unregistration successful
		"""
		try:
			with self._lock:
				if name in self._registeredDrivers:
					# If this was the active driver, deactivate it
					if self._activeDriver == name:
						self._activeDriver = None
						log.info(f"Deactivated braille driver {name}")

					# Clean up resources
					if name in self._artProcessConnections:
						del self._artProcessConnections[name]

					del self._registeredDrivers[name]
					log.info(f"Unregistered braille driver: {name}")
					return True
				else:
					log.warning(f"Attempted to unregister unknown braille driver: {name}")
					return False
		except Exception:
			self._log_error("unregisterBrailleDriver", name)
			return False

	def getRegisteredDrivers(self) -> List[Dict[str, Any]]:
		"""Get list of all registered braille drivers.

		@return: List of driver information dictionaries
		"""
		try:
			with self._lock:
				return [
					{
						"name": name,
						**driver_info
					}
					for name, driver_info in self._registeredDrivers.items()
				]
		except Exception:
			self._log_error("getRegisteredDrivers")
			return []

	def setActiveDriver(self, name: str) -> bool:
		"""Set the active braille display driver.

		@param name: The driver name to activate
		@return: True if activation successful
		"""
		try:
			with self._lock:
				if name not in self._registeredDrivers:
					log.error(f"Cannot activate unknown braille driver: {name}")
					return False

				# Deactivate current driver if any
				if self._activeDriver and self._activeDriver != name:
					if self._activeDriver in self._registeredDrivers:
						self._registeredDrivers[self._activeDriver]["isActive"] = False

				# Activate new driver
				self._activeDriver = name
				self._registeredDrivers[name]["isActive"] = True
				log.info(f"Activated braille driver: {name}")
				return True
		except Exception:
			self._log_error("setActiveDriver", name)
			return False

	def displayCells(self, driverName: str, cells: List[int]) -> bool:
		"""Send braille cells to display on the specified driver.

		@param driverName: Name of the driver to send cells to
		@param cells: List of braille cell values to display
		@return: True if display successful
		"""
		try:
			with self._lock:
				if driverName not in self._registeredDrivers:
					log.error(f"Cannot display cells on unknown driver: {driverName}")
					return False

				if driverName not in self._artProcessConnections:
					log.error(f"No ART connection for driver: {driverName}")
					return False

				art_service = self._artProcessConnections[driverName]

			# Call outside the lock to avoid blocking other operations
			result = art_service.displayCells(cells)
			log.debug(f"Displayed {len(cells)} cells on driver {driverName}")
			return result

		except Exception:
			self._log_error("displayCells", f"driver={driverName}, cells_count={len(cells) if cells else 0}")
			return False

	def forwardInputGesture(self, driverName: str, gestureId: str, **kwargs) -> bool:
		"""Forward an input gesture from ART braille driver to NVDA Core.

		@param driverName: Name of the driver that generated the gesture
		@param gestureId: Identifier for the gesture
		@param kwargs: Additional gesture parameters
		@return: True if gesture was forwarded successfully
		"""
		try:
			with self._lock:
				if driverName not in self._registeredDrivers:
					log.error(f"Gesture from unknown driver: {driverName}")
					return False

				driver_info = self._registeredDrivers[driverName]

			# Validate gesture is supported by this driver
			if gestureId not in driver_info["supportedGestures"]:
				log.warning(f"Unsupported gesture {gestureId} from driver {driverName}")
				return False

			# TODO: Create proper BrailleDisplayGesture instance and execute via inputCore
			# For now, log the gesture
			log.debug(f"Input gesture from {driverName}: {gestureId} {kwargs}")

			# Basic gesture forwarding - this needs to be enhanced
			# to create proper gesture objects and integrate with inputCore
			try:
				# This is a placeholder - real implementation needs to create
				# a proper BrailleDisplayGesture instance
				log.info(f"Processing braille gesture: {gestureId} from {driverName}")
				return True
			except Exception:
				log.error(f"Failed to process gesture {gestureId} from {driverName}")
				return False

		except Exception:
			self._log_error("forwardInputGesture", f"driver={driverName}, gesture={gestureId}")
			return False

	def getDriverInfo(self, name: str) -> Optional[Dict[str, Any]]:
		"""Get detailed information about a specific driver.

		@param name: Driver name
		@return: Driver information dict or None if not found
		"""
		try:
			with self._lock:
				if name in self._registeredDrivers:
					return {
						"name": name,
						**self._registeredDrivers[name]
					}
				return None
		except Exception:
			self._log_error("getDriverInfo", name)
			return None

	def isDriverActive(self, name: str) -> bool:
		"""Check if a driver is currently active.

		@param name: Driver name
		@return: True if driver is active
		"""
		try:
			with self._lock:
				return self._activeDriver == name
		except Exception:
			self._log_error("isDriverActive", name)
			return False

	def getActiveDriver(self) -> Optional[str]:
		"""Get the name of the currently active driver.

		@return: Active driver name or None
		"""
		try:
			with self._lock:
				return self._activeDriver
		except Exception:
			self._log_error("getActiveDriver")
			return None

	def checkDriverAvailability(self, name: str) -> bool:
		"""Check if a driver is available for use.

		@param name: Driver name
		@return: True if driver is available
		"""
		try:
			with self._lock:
				if name not in self._registeredDrivers:
					return False
				
				# Check if ART process connection is still valid
				if name not in self._artProcessConnections:
					self._registeredDrivers[name]["isAvailable"] = False
					return False

				# TODO: Add health check ping to ART service
				return self._registeredDrivers[name]["isAvailable"]
		except Exception:
			self._log_error("checkDriverAvailability", name)
			return False

	def terminate(self):
		"""Clean up the service and all registered drivers."""
		try:
			with self._lock:
				log.info("Terminating BrailleService")
				
				# Deactivate active driver
				if self._activeDriver:
					self._activeDriver = None

				# Clear all connections and registrations
				self._artProcessConnections.clear()
				self._registeredDrivers.clear()

				log.info("BrailleService terminated")
		except Exception:
			self._log_error("terminate")