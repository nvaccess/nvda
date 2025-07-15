# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file is covered by the GNU Lesser General Public License.
# See the file COPYING for more details.

"""Braille module proxy for add-ons running in ART."""

import typing
from typing import List, Tuple, OrderedDict, Optional, Union, Any

from .base import ServiceProxyMixin
import driverHandler


class BrailleDisplayDriver(driverHandler.Driver):
	"""
	Proxy base class for braille display drivers in ART.
	
	This class provides the same interface as the core BrailleDisplayDriver
	but runs in the ART process. Drivers inherit from this class and their
	instances are registered with NVDA Core via the BrailleService.
	"""
	
	_configSection = "braille"
	supportedSettings = ()
	
	#: Whether this driver is thread-safe.
	isThreadSafe: bool = False
	#: Whether this driver is supported for automatic detection of braille displays.
	supportsAutomaticDetection: bool = False
	#: Whether displays for this driver return acknowledgements for sent packets.
	receivesAckPackets: bool = False
	#: Whether this driver is awaiting an Ack for a connected display.
	_awaitingAck: bool = False
	#: Maximum timeout to use for communication with a device (in seconds).
	timeout: float = 0.2
	
	#: Number of braille cells on the display.
	numCells: int = 0
	#: Number of rows of braille cells (for multi-line displays).
	numRows: int = 1
	#: Number of columns of braille cells (for multi-line displays).
	numCols: int = 0

	def __init__(self, port: typing.Union[None, str, Any] = None):
		"""Constructor
		@param port: Information on how to connect to the device.
		"""
		super().__init__()
		self._port = port

	@classmethod
	def check(cls) -> bool:
		"""Check whether this braille display is available.
		This method should return True if the display is available.
		@return: True if available, False otherwise.
		"""
		return False

	def terminate(self):
		"""Terminate this braille display driver."""
		pass

	def display(self, cells):
		"""Display braille cells.
		@param cells: The braille cells to display; a sequence of integers.
		"""
		pass

	@classmethod
	def getPossiblePorts(cls) -> typing.OrderedDict[str, str]:
		"""Get possible ports for this braille display.
		@return: An ordered dictionary of port names to descriptions.
		"""
		return typing.OrderedDict()


class BrailleProxy(ServiceProxyMixin):
	"""Proxy for core braille module functionality."""
	
	_service_env_var = "NVDA_ART_BRAILLE_SERVICE_URI"

	def getDisplayList(self, excludeNegativeChecks: bool = True) -> List[Tuple[str, str]]:
		"""Get a list of available braille display drivers.
		@param excludeNegativeChecks: Whether to exclude drivers that return False from check().
		@return: List of (driver_name, description) tuples.
		"""
		result = self._call_service("getDisplayList", excludeNegativeChecks)
		return result if result is not None else []

	def getDisplayDrivers(self) -> typing.Iterator[Any]:
		"""Get an iterator of available braille display driver modules.
		@return: Iterator of driver modules.
		"""
		result = self._call_service("getDisplayDrivers")
		return iter(result) if result is not None else iter([])


# Create proxy instance for module-level access
_brailleProxy = BrailleProxy()

# Expose module-level functions
getDisplayList = _brailleProxy.getDisplayList
getDisplayDrivers = _brailleProxy.getDisplayDrivers

# Expose key constants and classes
handler = None  # Will be set by NVDA core when a display is active