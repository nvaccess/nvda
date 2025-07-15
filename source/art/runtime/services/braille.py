# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Braille display service for managing braille drivers in ART."""

import logging
import threading
from typing import Any, Dict, List, Optional

import Pyro5.api


@Pyro5.api.expose
class BrailleDisplayService:
	"""Service for managing braille display drivers in the ART process.

	This service manages a single braille display driver instance and handles
	communication between NVDA Core and the driver for both output and input.
	"""

	def __init__(self):
		self._driverInstance: Optional[Any] = None
		self._driverInfo: Optional[Dict[str, Any]] = None
		self._coreService: Optional[Any] = None  # Connection to BrailleService in NVDA Core
		self.logger = logging.getLogger("ART.BrailleDisplayService")
		self._lock = threading.Lock()
		self._isRegistered = False
		self.logger.info("BrailleDisplayService initialized")

	def setBrailleInstance(self, driver: Any) -> None:
		"""Set the braille display driver instance for this ART process.

		Called by the braille display driver when it initializes.

		@param driver: The braille display driver instance.
		"""
		with self._lock:
			self._driverInstance = driver
			self._extractDriverInfo()
			
			driver_name = getattr(driver, 'name', 'unknown')
			self.logger.info(f"Braille driver instance set: {driver_name}")
			
			# Attempt to register with NVDA Core
			self._registerWithCore()

	def _extractDriverInfo(self) -> None:
		"""Extract driver information for registration."""
		if not self._driverInstance:
			return

		try:
			self._driverInfo = {
				"name": getattr(self._driverInstance, 'name', 'unknown'),
				"description": getattr(self._driverInstance, 'description', 'Unknown Braille Display'),
				"numCells": getattr(self._driverInstance, 'numCells', 0),
				"numRows": getattr(self._driverInstance, 'numRows', 0),
				"numCols": getattr(self._driverInstance, 'numCols', 0),
				"isThreadSafe": getattr(self._driverInstance, 'isThreadSafe', False),
				"supportsAutomaticDetection": getattr(self._driverInstance, 'supportsAutomaticDetection', False),
				"receivesAckPackets": getattr(self._driverInstance, 'receivesAckPackets', False),
				"timeout": getattr(self._driverInstance, 'timeout', 0.2),
			}

			# Extract supported gestures from gestureMap if available
			gesture_map = getattr(self._driverInstance, 'gestureMap', {})
			supported_gestures = []
			if gesture_map:
				# Extract all gesture identifiers from the gesture map
				for script_name, gestures in gesture_map.items():
					if isinstance(gestures, (list, tuple)):
						supported_gestures.extend(gestures)
					else:
						supported_gestures.append(gestures)

			self._driverInfo["supportedGestures"] = supported_gestures

			self.logger.debug(f"Extracted driver info: {self._driverInfo}")

		except Exception:
			self.logger.exception("Error extracting driver information")

	def _registerWithCore(self) -> None:
		"""Register this driver with NVDA Core BrailleService."""
		if not self._driverInfo or not self._coreService:
			self.logger.warning("Cannot register: missing driver info or core service connection")
			return

		try:
			# TODO: Get addon name from current context
			addon_name = "unknown_addon"  # This should be passed from addon loading context

			success = self._coreService.registerBrailleDriver(
				name=self._driverInfo["name"],
				description=self._driverInfo["description"],
				addon_name=addon_name,
				numCells=self._driverInfo["numCells"],
				numRows=self._driverInfo["numRows"],
				numCols=self._driverInfo["numCols"],
				supportedGestures=self._driverInfo["supportedGestures"],
				deviceInfo=self._driverInfo,
				art_service_proxy=self,  # Pass this service instance as proxy
			)

			if success:
				self._isRegistered = True
				self.logger.info(f"Successfully registered driver {self._driverInfo['name']} with NVDA Core")
			else:
				self.logger.error(f"Failed to register driver {self._driverInfo['name']} with NVDA Core")

		except Exception:
			self.logger.exception("Error registering driver with NVDA Core")

	def setCoreService(self, core_service: Any) -> None:
		"""Set the connection to NVDA Core BrailleService.

		@param core_service: Proxy to BrailleService in NVDA Core
		"""
		with self._lock:
			self._coreService = core_service
			self.logger.info("Core service connection established")
			
			# If we already have a driver, try to register it
			if self._driverInstance and not self._isRegistered:
				self._registerWithCore()

	def displayCells(self, cells: List[int]) -> bool:
		"""Display braille cells on the physical display.

		@param cells: List of braille cell values to display
		@return: True if display was successful
		"""
		if not self._driverInstance:
			self.logger.error("No driver instance available for displayCells")
			return False

		try:
			self.logger.debug(f"Displaying {len(cells)} cells")

			# Ensure we have the display method
			if not hasattr(self._driverInstance, 'display'):
				self.logger.error("Driver instance has no display method")
				return False

			# Call the driver's display method
			self._driverInstance.display(cells)
			self.logger.debug("Successfully displayed cells")
			return True

		except Exception:
			self.logger.exception(f"Error displaying {len(cells) if cells else 0} cells")
			return False

	def getDriverInfo(self) -> Dict[str, Any]:
		"""Get driver information and capabilities.

		@return: Dictionary containing driver information
		"""
		with self._lock:
			if self._driverInfo:
				return self._driverInfo.copy()
			else:
				return {
					"name": "unknown",
					"description": "Unknown Driver",
					"numCells": 0,
					"numRows": 0,
					"numCols": 0,
					"supportedGestures": [],
				}

	def terminateDriver(self) -> bool:
		"""Terminate the current driver and clean up resources.

		@return: True if termination was successful
		"""
		try:
			with self._lock:
				if self._driverInstance:
					driver_name = getattr(self._driverInstance, 'name', 'unknown')
					self.logger.info(f"Terminating driver: {driver_name}")

					# Unregister from Core if registered
					if self._isRegistered and self._coreService:
						try:
							self._coreService.unregisterBrailleDriver(driver_name)
							self._isRegistered = False
						except Exception:
							self.logger.exception("Error unregistering from Core")

					# Call driver's terminate method if it exists
					if hasattr(self._driverInstance, 'terminate'):
						self._driverInstance.terminate()

					self._driverInstance = None
					self._driverInfo = None
					self.logger.info(f"Driver {driver_name} terminated successfully")

				return True

		except Exception:
			self.logger.exception("Error terminating driver")
			return False

	def handleInputGesture(self, gesture_id: str, **kwargs) -> bool:
		"""Handle an input gesture from the braille display hardware.

		This method is called by the driver when hardware input is received.

		@param gesture_id: Identifier for the gesture
		@param kwargs: Additional gesture parameters
		@return: True if gesture was handled successfully
		"""
		try:
			if not self._coreService:
				self.logger.error("No core service connection for gesture forwarding")
				return False

			if not self._driverInfo:
				self.logger.error("No driver info available for gesture validation")
				return False

			driver_name = self._driverInfo["name"]
			self.logger.debug(f"Handling input gesture: {gesture_id} from {driver_name}")

			# Forward gesture to NVDA Core
			success = self._coreService.forwardInputGesture(driver_name, gesture_id, **kwargs)
			
			if success:
				self.logger.debug(f"Successfully forwarded gesture {gesture_id}")
			else:
				self.logger.warning(f"Failed to forward gesture {gesture_id}")

			return success

		except Exception:
			self.logger.exception(f"Error handling input gesture {gesture_id}")
			return False

	def checkConnection(self) -> bool:
		"""Check if the driver connection is still valid.

		@return: True if connection is healthy
		"""
		try:
			with self._lock:
				if not self._driverInstance:
					return False

				# Basic health check - ensure driver is still responsive
				driver_name = getattr(self._driverInstance, 'name', None)
				return driver_name is not None

		except Exception:
			self.logger.exception("Error checking connection")
			return False

	def getStatus(self) -> Dict[str, Any]:
		"""Get current service status.

		@return: Status information dictionary
		"""
		try:
			with self._lock:
				status = {
					"hasDriver": self._driverInstance is not None,
					"isRegistered": self._isRegistered,
					"hasCoreConnection": self._coreService is not None,
					"driverName": getattr(self._driverInstance, 'name', None) if self._driverInstance else None,
				}

				if self._driverInfo:
					status.update({
						"numCells": self._driverInfo.get("numCells", 0),
						"numRows": self._driverInfo.get("numRows", 0),
						"numCols": self._driverInfo.get("numCols", 0),
						"isThreadSafe": self._driverInfo.get("isThreadSafe", False),
					})

				return status

		except Exception:
			self.logger.exception("Error getting status")
			return {"hasDriver": False, "isRegistered": False, "hasCoreConnection": False}

	def reconnectDriver(self) -> bool:
		"""Attempt to reconnect a failed driver.

		@return: True if reconnection was successful
		"""
		try:
			with self._lock:
				if not self._driverInstance:
					self.logger.error("No driver instance to reconnect")
					return False

				driver_name = getattr(self._driverInstance, 'name', 'unknown')
				self.logger.info(f"Attempting to reconnect driver: {driver_name}")

				# If the driver has a reconnect method, call it
				if hasattr(self._driverInstance, 'reconnect'):
					self._driverInstance.reconnect()
					self.logger.info(f"Driver {driver_name} reconnected successfully")
					return True
				else:
					# Some drivers might need to be reinitialized completely
					if hasattr(self._driverInstance, '__init__'):
						# This is risky but might work for some drivers
						self.logger.warning(f"No reconnect method, attempting re-initialization for {driver_name}")
						# We would need the original port/connection info here
						return False
					else:
						self.logger.error(f"Driver {driver_name} has no reconnect capability")
						return False

		except Exception:
			self.logger.exception("Error reconnecting driver")
			return False

	def getProperty(self, prop_name: str, default_value=None):
		"""Get a property from the driver.

		@param prop_name: Property name
		@param default_value: Default value if property doesn't exist
		@return: Property value or default
		"""
		try:
			with self._lock:
				if not self._driverInstance:
					return default_value

				if hasattr(self._driverInstance, prop_name):
					return getattr(self._driverInstance, prop_name)
				else:
					return default_value

		except Exception:
			self.logger.exception(f"Error getting property {prop_name}")
			return default_value

	def setProperty(self, prop_name: str, value) -> bool:
		"""Set a property on the driver.

		@param prop_name: Property name
		@param value: Property value
		@return: True if successful
		"""
		try:
			with self._lock:
				if not self._driverInstance:
					return False

				if hasattr(self._driverInstance, prop_name):
					setattr(self._driverInstance, prop_name, value)
					self.logger.debug(f"Set {prop_name} to {value}")
					return True
				else:
					self.logger.warning(f"Property {prop_name} not supported by driver")
					return False

		except Exception:
			self.logger.exception(f"Error setting property {prop_name} to {value}")
			return False