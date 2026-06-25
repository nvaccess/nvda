# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import collections
import ctypes.wintypes
import importlib
import itertools
import pkgutil
import typing
from typing import (
	Iterable,
	Optional,
	Union,
)

import bdDetect
import brailleDisplayDrivers
import driverHandler
import hwPortUtils
import inputCore
import keyboardHandler
import winBindings.kernel32
from autoSettingsUtils.driverSetting import BooleanDriverSetting, NumericDriverSetting
from logHandler import log

import braille

from ..constants import (
	AUTOMATIC_PORT,
	BLUETOOTH_PORT,
	USB_PORT,
)


def _getDisplayDriver(moduleName: str, caseSensitive: bool = True) -> typing.Type["BrailleDisplayDriver"]:
	try:
		return importlib.import_module(
			"brailleDisplayDrivers.%s" % moduleName,
			package="brailleDisplayDrivers",
		).BrailleDisplayDriver
	except ImportError as initialException:
		if caseSensitive:
			raise initialException
		for loader, name, isPkg in pkgutil.iter_modules(brailleDisplayDrivers.__path__):
			if name.startswith("_") or name.lower() != moduleName.lower():
				continue
			return importlib.import_module(
				"brailleDisplayDrivers.%s" % name,
				package="brailleDisplayDrivers",
			).BrailleDisplayDriver
		else:
			raise initialException


class BrailleDisplayDriver(driverHandler.Driver):
	"""
	Abstract base braille display driver.

	Each braille display driver should be a separate Python module in the root ``brailleDisplayDrivers`` directory,
	containing a ``BrailleDisplayDriver`` class that inherits from this base class.

	At a minimum, drivers must:
		- Set :attr:`name` and :attr:`description`.
		- Override :meth:`check`.

	To display braille:
		- :meth:`display` must be implemented.
		- For a single-line display, :attr:`numCells` must be implemented.
		- For a multi-line display, :attr:`numRows` and :attr:`numCols` must be implemented.

	To support automatic detection of braille displays belonging to this driver:
		* The driver must be thread-safe, and :attr:`isThreadSafe` should be set to ``True``.
		* :attr:`supportsAutomaticDetection` must be set to ``True``.
		* :meth:`registerAutomaticDetection` must be implemented.

	Drivers should dispatch input (e.g., button presses or controls) using the :mod:`inputCore` framework.
	They should subclass :class:`BrailleDisplayGesture` and execute instances of those gestures
	using :meth:`inputCore.manager.executeGesture`. These gestures can be mapped in :attr:`gestureMap`.
	A driver can also inherit from :class:`baseObject.ScriptableObject` to provide display-specific scripts.

	.. seealso::
		:mod:`hwIo` for raw serial and HID I/O.

	There are factory functions to create :class:`autoSettingsUtils.driverSetting.DriverSetting` instances
	for common display-specific settings, such as :meth:`DotFirmnessSetting`.
	"""

	_configSection = "braille"
	# Most braille display drivers don't have settings yet.
	# Make sure supportedSettings is not abstract for these.
	supportedSettings = ()
	#: Whether this driver is thread-safe.
	#: If it is, NVDA may initialize, terminate or call this driver  on any thread.
	#: This allows NVDA to read from and write to the display in the background,
	#: which means the rest of NVDA is not blocked while this occurs,
	#: thus resulting in better performance.
	#: This is also required to use the L{hwIo} module.
	isThreadSafe: bool = False
	#: Whether this driver is supported for automatic detection of braille displays.
	supportsAutomaticDetection: bool = False
	#: Whether displays for this driver return acknowledgements for sent packets.
	#: L{_handleAck} should be called when an ACK is received.
	#: Note that thread safety is required for the generic implementation to function properly.
	#: If a display is not thread safe, a driver should manually implement ACK processing.
	receivesAckPackets: bool = False
	#: Whether this driver is awaiting an Ack for a connected display.
	#: This is set to C{True} after displaying cells when L{receivesAckPackets} is True,
	#: and set to C{False} by L{_handleAck} or when C{timeout} has elapsed.
	#: This is for internal use by NVDA core code only and shouldn't be touched by a driver itself.
	_awaitingAck: bool = False
	#: Maximum timeout to use for communication with a device (in seconds).
	#: This can be used for serial connections.
	#: Furthermore, it is used to stop waiting for missed acknowledgement packets.
	timeout: float = 0.2

	def __init__(self, port: typing.Union[None, str, bdDetect.DeviceMatch] = None):
		"""Constructor
		@param port: Information on how to connect to the device.
			Use L{_getTryPorts} to normalise to L{DeviceMatch} instances.
			- A string (from config "config.conf["braille"][name]["port"]"). When manually configured.
				This value is set via the settings dialog, the source of the options provided to the user
				is the BrailleDisplayDriver.getPossiblePorts method.
			- A L{DeviceMatch} instance. When automatically detected.
		"""
		super().__init__()

	@classmethod
	def check(cls) -> bool:
		"""Determine whether this braille display is available.
		The display will be excluded from the list of available displays if this method returns C{False}.
		For example, if this display is not present, C{False} should be returned.
		@return: C{True} if this display is available, C{False} if not.
		"""
		if cls.isThreadSafe:
			supportsAutomaticDetection = cls.supportsAutomaticDetection
			if supportsAutomaticDetection and bdDetect.driverHasPossibleDevices(cls.name):
				return True
		try:
			next(cls.getManualPorts())
		except (StopIteration, NotImplementedError):
			pass
		else:
			return True
		return False

	@classmethod
	def registerAutomaticDetection(cls, driverRegistrar: bdDetect.DriverRegistrar):
		"""
		This method may register the braille display driver in the braille display automatic detection framework.
		The framework provides a L{bdDetect.DriverRegistrar} object as its only parameter.
		The methods on the driver registrar can be used to register devices or device scanners.
		This method should only register itself with the bdDetect framework,
		and should refrain from doing anything else.
		Drivers with L{supportsAutomaticDetection} set to C{True} must implement this method.
		@param driverRegistrar: An object containing several methods to register device identifiers for this driver.
		"""
		raise NotImplementedError

	def terminate(self):
		"""Terminate this display driver.
		This will be called when NVDA is finished with this display driver.
		It should close any open connections, perform cleanup, etc.
		Subclasses should call the superclass method first.
		@postcondition: This instance can no longer be used unless it is constructed again.
		"""
		super().terminate()
		if getattr(self, "_suppressDisplayClear", False):
			self._suppressDisplayClear = False
			return
		# Clear the display.
		try:
			self.display([0] * self.numCells)
		except Exception:
			# The display driver seems to be failing, but we're terminating anyway, so just ignore it.
			log.error(f"Display driver {self} failed to display while terminating.", exc_info=True)

	#: typing information for autoproperty _get_numCells
	numCells: int

	def _get_numCells(self) -> int:
		"""Obtain the number of braille cells on this display.
		@note: 0 indicates that braille should be disabled.
		@note: For multi line displays, this is the total number of cells (e.g. numRows * numCols)
		@return: The number of cells.
		"""
		return self.numRows * self.numCols

	def _set_numCells(self, numCells: int):
		if self.numRows > 1:
			raise ValueError(
				"Please set numCols explicitly and don't set numCells for multi line braille displays",
			)
		self.numCols = numCells

	#: Number of rows of the braille display, this will be 1 for most displays
	#: Note: Setting this to 0 will cause numCells to be 0 and hence will disable braille.
	numRows: int = 1

	#: Number of columns (cells per row) of the braille display
	#: 0 indicates that braille should be disabled.
	numCols: int = 0

	def __repr__(self):
		return f"{self.__class__.__name__}({self.name!r}, numCells={self.numCells!r})"

	def display(self, cells):
		"""Display the given braille cells.
		@param cells: The braille cells to display.
		@type cells: [int, ...]
		"""

	#: Automatic port constant to be used by braille displays that support the "automatic" port
	#: Kept for backwards compatibility
	AUTOMATIC_PORT = AUTOMATIC_PORT

	@classmethod
	def getPossiblePorts(cls) -> typing.OrderedDict[str, str]:
		"""Returns possible hardware ports for this driver.
		Optionally and in addition to the values from L{getManualPorts},
		three special values may be returned if the driver supports
		them, "auto", "usb", and "bluetooth".

		Generally, drivers shouldn't implement this method directly.
		Instead, they should provide automatic detection data via L{bdDetect}
		and implement L{getPossibleManualPorts} if they support manual ports
		such as serial ports.

		@return: Ordered dictionary for each port a (key : value) of name : translated description.
		"""
		try:
			next(bdDetect.getConnectedUsbDevicesForDriver(cls.name))
			usb = True
		except (LookupError, StopIteration):
			usb = False
		try:
			next(bdDetect.getPossibleBluetoothDevicesForDriver(cls.name))
			bluetooth = True
		except (LookupError, StopIteration):
			bluetooth = False
		ports = collections.OrderedDict()
		if usb or bluetooth:
			ports.update((AUTOMATIC_PORT,))
			if usb:
				ports.update((USB_PORT,))
			if bluetooth:
				ports.update((BLUETOOTH_PORT,))
		try:
			ports.update(cls.getManualPorts())
		except NotImplementedError:
			pass
		return ports

	@classmethod
	def _getAutoPorts(cls, usb=True, bluetooth=True) -> Iterable[bdDetect.DeviceMatch]:
		"""Returns possible ports to connect to using L{bdDetect} automatic detection data.
		@param usb: Whether to search for USB devices.
		@type usb: bool
		@param bluetooth: Whether to search for bluetooth devices.
		@type bluetooth: bool
		@return: The device match for each port.
		@rtype: iterable of L{DeviceMatch}
		"""
		iters = []
		if usb:
			iters.append(bdDetect.getConnectedUsbDevicesForDriver(cls.name))
		if bluetooth:
			iters.append(bdDetect.getPossibleBluetoothDevicesForDriver(cls.name))

		try:
			for match in itertools.chain(*iters):
				yield match
		except LookupError:
			pass

	@classmethod
	def getManualPorts(cls) -> typing.Iterator[typing.Tuple[str, str]]:
		"""Get possible manual hardware ports for this driver.
		This is for ports which cannot be detected automatically
		such as serial ports.
		@return: An iterator containing the name and description for each port.
		"""
		raise NotImplementedError

	@classmethod
	def _getTryPorts(
		cls,
		port: Union[str, bdDetect.DeviceMatch],
	) -> typing.Iterator[bdDetect.DeviceMatch]:
		"""Returns the ports for this driver to which a connection attempt should be made.
		This generator function is usually used in L{__init__} to connect to the desired display.
		@param port: the port to connect to.
		@return: The name and description for each port
		"""
		if isinstance(port, bdDetect.DeviceMatch):
			yield port
		elif isinstance(port, str):
			isUsb = port in (AUTOMATIC_PORT[0], USB_PORT[0])
			isBluetooth = port in (AUTOMATIC_PORT[0], BLUETOOTH_PORT[0])
			if not isUsb and not isBluetooth:
				# Assume we are connecting to a com port, since these are the only manual ports supported.
				try:
					portInfo = next(info for info in hwPortUtils.listComPorts() if info["port"] == port)
				except StopIteration:
					pass
				else:
					yield bdDetect.DeviceMatch(
						bdDetect.ProtocolType.SERIAL,
						portInfo["bluetoothName" if "bluetoothName" in portInfo else "friendlyName"],
						portInfo["port"],
						portInfo,
					)
			else:
				for match in cls._getAutoPorts(usb=isUsb, bluetooth=isBluetooth):
					yield match

	#: Global input gesture map for this display driver.
	gestureMap: Optional[inputCore.GlobalGestureMap] = None

	@classmethod
	def _getModifierGestures(cls, model=None):
		"""Retrieves modifier gestures from this display driver's L{gestureMap}
		that are bound to modifier only keyboard emulate scripts.
		@param model: the optional braille display model for which modifier gestures should also be included.
		@type model: str; C{None} if model specific gestures should not be included
		@return: the ids of the display keys and the associated generalised modifier names
		@rtype: generator of (set, set)
		"""
		import globalCommands

		# Ignore the locale gesture map when searching for braille display gestures
		globalMaps = [inputCore.manager.userGestureMap]
		if cls.gestureMap:
			globalMaps.append(cls.gestureMap)
		prefixes = ["br({source})".format(source=cls.name)]
		if model:
			prefixes.insert(0, "br({source}.{model})".format(source=cls.name, model=model))
		for globalMap in globalMaps:
			for scriptCls, gesture, scriptName in globalMap.getScriptsForAllGestures():
				if (
					any(gesture.startswith(prefix.lower()) for prefix in prefixes)
					and scriptCls is globalCommands.GlobalCommands
					and scriptName
					and scriptName.startswith("kb")
				):
					emuGesture = keyboardHandler.KeyboardInputGesture.fromName(scriptName.split(":")[1])
					if emuGesture.isModifier:
						yield set(gesture.split(":")[1].split("+")), set(emuGesture._keyNamesInDisplayOrder)

	def _handleAck(self):
		"""Base implementation to handle acknowledgement packets."""
		if not self.receivesAckPackets:
			raise NotImplementedError("This display driver does not support ACK packet handling")
		if not winBindings.kernel32.CancelWaitableTimer(braille.handler.ackTimerHandle):
			raise ctypes.WinError()
		self._awaitingAck = False
		braille.handler._writeCellsInBackground()

	@classmethod
	def DotFirmnessSetting(cls, defaultVal, minVal, maxVal, useConfig=False):
		"""Factory function for creating dot firmness setting."""
		return NumericDriverSetting(
			"dotFirmness",
			# Translators: Label for a setting in braille settings dialog.
			_("Dot firm&ness"),
			defaultVal=defaultVal,
			minVal=minVal,
			maxVal=maxVal,
			useConfig=useConfig,
		)

	@classmethod
	def BrailleInputSetting(cls, useConfig=True):
		"""Factory function for creating braille input setting."""
		return BooleanDriverSetting(
			"brailleInput",
			# Translators: Label for a setting in braille settings dialog.
			_("Braille inp&ut"),
			useConfig=useConfig,
		)

	@classmethod
	def HIDInputSetting(cls, useConfig):
		"""Factory function for creating HID input setting."""
		return BooleanDriverSetting(
			"hidKeyboardInput",
			# Translators: Label for a setting in braille settings dialog.
			_("&HID keyboard input simulation"),
			useConfig=useConfig,
		)
