# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Base braille display driver class for ART runtime."""

import os
import logging
from abc import abstractmethod, ABC
from typing import List, Dict, Any, Optional, OrderedDict, Union, Iterator, Tuple
import Pyro5.api


class BrailleDisplayDriver(ABC):
	"""Base class for braille display drivers running in ART.
	
	This mirrors the NVDA BrailleDisplayDriver API but runs in the ART process.
	
	Required implementations for subclasses:
	- check(): Class method to verify display availability
	- display(): Send braille cells to the hardware
	
	Optional implementations:
	- terminate(): Cleanup when driver is being unloaded
	- registerAutomaticDetection(): For auto-detection support
	- getManualPorts(): For manual port configuration
	
	The driver will be automatically registered with NVDA Core when instantiated.
	"""
	
	#: The name of the driver; must be the original module file name.
	name: str = ""
	
	#: A description of the driver.
	description: str = ""
	
	#: The configuration section where driver specific subsections should be saved.
	_configSection = "braille"
	
	#: Whether this driver is thread-safe.
	#: If it is, NVDA may initialize, terminate or call this driver on any thread.
	#: This allows NVDA to read from and write to the display in the background,
	#: which means the rest of NVDA is not blocked while this occurs,
	#: thus resulting in better performance.
	#: This is also required to use the hwIo module.
	isThreadSafe: bool = False
	
	#: Whether this driver is supported for automatic detection of braille displays.
	supportsAutomaticDetection: bool = False
	
	#: Whether displays for this driver return acknowledgements for sent packets.
	#: _handleAck should be called when an ACK is received.
	#: Note that thread safety is required for the generic implementation to function properly.
	#: If a display is not thread safe, a driver should manually implement ACK processing.
	receivesAckPackets: bool = False
	
	#: Whether this driver is awaiting an Ack for a connected display.
	#: This is set to True after displaying cells when receivesAckPackets is True,
	#: and set to False by _handleAck or when timeout has elapsed.
	#: This is for internal use by NVDA core code only and shouldn't be touched by a driver itself.
	_awaitingAck: bool = False
	
	#: Maximum timeout to use for communication with a device (in seconds).
	#: This can be used for serial connections.
	#: Furthermore, it is used to stop waiting for missed acknowledgement packets.
	timeout: float = 0.2
	
	#: Number of rows of the braille display, this will be 1 for most displays
	#: Note: Setting this to 0 will cause numCells to be 0 and hence will disable braille.
	numRows: int = 1
	
	#: Number of columns (cells per row) of the braille display
	#: 0 indicates that braille should be disabled.
	numCols: int = 0

	def __init__(self, port: Union[None, str, Any] = None):
		"""Constructor
		@param port: Information on how to connect to the device.
			- A string (from config). When manually configured.
				This value is set via the settings dialog, the source of the options provided to the user
				is the BrailleDisplayDriver.getPossiblePorts method.
			- A DeviceMatch instance. When automatically detected.
		"""
		self.logger = logging.getLogger(f"ART.BrailleDisplayDriver.{self.name}")
		self._port = port
		self._brailleService = None
		
		# Register this braille driver with NVDA Core
		self._registerWithCore()
		
		# Register this instance with the ART braille service
		self._registerWithARTService()
		
		self.logger.info(f"Braille display driver {self.name} initialized in ART")

	@classmethod
	@abstractmethod
	def check(cls) -> bool:
		"""Determine whether this braille display is available.
		The display will be excluded from the list of available displays if this method returns False.
		For example, if this display is not present, False should be returned.
		@return: True if this display is available, False if not.
		"""
		return False

	@abstractmethod
	def display(self, cells):
		"""Display the given braille cells.
		@param cells: The braille cells to display.
		@type cells: List[int]
		"""
		pass

	def terminate(self):
		"""Terminate this display driver.
		This will be called when NVDA is finished with this display driver.
		It should close any open connections, perform cleanup, etc.
		Subclasses should call the superclass method first.
		@postcondition: This instance can no longer be used unless it is constructed again.
		"""
		# Clear the display.
		try:
			self.display([0] * self.numCells)
		except Exception:
			# The display driver seems to be failing, but we're terminating anyway, so just ignore it.
			self.logger.error(f"Display driver {self} failed to display while terminating.", exc_info=True)

	@property
	def numCells(self) -> int:
		"""Obtain the number of braille cells on this display.
		@note: 0 indicates that braille should be disabled.
		@note: For multi line displays, this is the total number of cells (e.g. numRows * numCols)
		@return: The number of cells.
		"""
		return self.numRows * self.numCols

	@numCells.setter
	def numCells(self, numCells: int):
		if self.numRows > 1:
			raise ValueError(
				"Please set numCols explicitly and don't set numCells for multi line braille displays",
			)
		self.numCols = numCells

	def __repr__(self):
		return f"{self.__class__.__name__}({self.name!r}, numCells={self.numCells!r})"

	@classmethod
	def getPossiblePorts(cls) -> OrderedDict[str, str]:
		"""Returns possible hardware ports for this driver.
		This default implementation returns an empty OrderedDict.
		Subclasses should override this to provide actual ports.
		@return: Ordered dictionary for each port a (key : value) of name : translated description.
		"""
		return OrderedDict()

	@classmethod
	def getManualPorts(cls) -> Iterator[Tuple[str, str]]:
		"""Get possible manual hardware ports for this driver.
		This is for ports which cannot be detected automatically
		such as serial ports.
		@return: An iterator containing the name and description for each port.
		"""
		raise NotImplementedError

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar):
		"""
		This method may register the braille display driver in the braille display automatic detection framework.
		The framework provides a DriverRegistrar object as its only parameter.
		The methods on the driver registrar can be used to register devices or device scanners.
		This method should only register itself with the bdDetect framework,
		and should refrain from doing anything else.
		Drivers with supportsAutomaticDetection set to True must implement this method.
		@param driverRegistrar: An object containing several methods to register device identifiers for this driver.
		"""
		raise NotImplementedError

	def _registerWithARTService(self):
		"""Register this braille instance with the ART braille service."""
		try:
			self.logger.debug("Attempting to register with ART braille service")
			
			# Get the braille service from the ART runtime using clean API
			import art.runtime
			runtime = art.runtime.getRuntime()
			self.logger.debug(f"Got runtime: {runtime}")
			
			brailleService = runtime.services.get('braille')
			self.logger.debug(f"Got brailleService: {brailleService}")
			
			if brailleService:
				brailleService.setBrailleInstance(self)
				self.logger.debug("Successfully registered with ART braille service")
			else:
				self.logger.warning("ART brailleService not found in services")
		except Exception:
			self.logger.exception("Failed to register with ART braille service")

	def _registerWithCore(self):
		"""Register this braille driver with NVDA Core."""
		self.logger.debug(f"Attempting to register {self.name} with NVDA Core")
		try:
			# Get the braille service URI from environment
			braille_uri = os.environ.get("NVDA_ART_BRAILLE_SERVICE_URI")
			self.logger.debug(f"Braille service URI from environment: {braille_uri}")
			if not braille_uri:
				self.logger.error("No NVDA_ART_BRAILLE_SERVICE_URI found")
				return
			
			# Connect to NVDA Core's braille service
			self.logger.debug(f"Connecting to braille service at {braille_uri}")
			self._brailleService = Pyro5.api.Proxy(braille_uri)
			self._brailleService._pyroTimeout = 2.0
			
			# Get addon name from environment
			addon_name = os.environ.get("NVDA_ART_ADDON_NAME", "unknown")
			self.logger.debug(f"Addon name from environment: {addon_name}")
			
			# Get supported gestures
			supported_gestures = []
			if hasattr(self, 'gestureMap') and self.gestureMap:
				supported_gestures = list(self.gestureMap.keys())
			
			# Get device information
			device_info = {}
			for attr in ['isThreadSafe', 'supportsAutomaticDetection']:
				if hasattr(self, attr):
					device_info[attr] = getattr(self, attr)
			
			# Register this braille driver
			self.logger.debug(f"Calling registerBrailleDriver for {self.name}")
			result = self._brailleService.registerBrailleDriver(
				name=self.name,
				description=self.description,
				addon_name=addon_name,
				numCells=self.numCells,
				numRows=self.numRows,
				numCols=self.numCols,
				supportedGestures=supported_gestures,
				deviceInfo=device_info,
				art_service_proxy=None  # This will be set by the BrailleService
			)
			self.logger.debug(f"registerBrailleDriver returned: {result}")
			
			if result:
				self.logger.info(f"Successfully registered {self.name} with NVDA Core")
			else:
				self.logger.error(f"Failed to register {self.name} with NVDA Core - registerBrailleDriver returned False")
				
		except Exception:
			self.logger.exception("Error registering with NVDA Core")

	def _handleAck(self):
		"""Handle an acknowledgement packet from the display.
		This is called by the driver when an ACK is received.
		"""
		self._awaitingAck = False

	def _displayCells(self, cells):
		"""Internal method to display cells and handle ACK processing.
		This is called by NVDA Core via the BrailleDisplayService.
		"""
		try:
			self.display(cells)
			if self.receivesAckPackets:
				self._awaitingAck = True
		except Exception:
			self.logger.exception(f"Error displaying {len(cells)} cells")

	def _sendInputGesture(self, gesture_id: str, **kwargs):
		"""Send an input gesture to NVDA Core.
		@param gesture_id: The gesture identifier (e.g., "br(alva):etouch1")
		@param kwargs: Additional gesture data
		"""
		if self._brailleService:
			try:
				self._brailleService.sendInputGesture(
					driver_name=self.name,
					gesture_id=gesture_id,
					gesture_data=kwargs
				)
			except Exception:
				self.logger.exception(f"Error sending input gesture: {gesture_id}")


# Re-export for compatibility
__all__ = ["BrailleDisplayDriver"]