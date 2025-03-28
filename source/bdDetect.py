# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2013-2023 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Support for braille display detection.
This allows devices to be automatically detected and used when they become available,
as well as providing utilities to query for possible devices for a particular driver.
To support detection for a driver, devices need to be associated
using the C{add*} functions.
Drivers distributed with NVDA do this at the bottom of this module.
For drivers in add-ons, this must be done in a global plugin.
"""

from dataclasses import dataclass, field
from functools import partial
import itertools
import threading
from concurrent.futures import ThreadPoolExecutor, Future
from enum import StrEnum
from typing import (
	Any,
	Callable,
	Dict,
	Generator,
	Iterable,
	Iterator,
	List,
	NamedTuple,
	Optional,
	OrderedDict,
	Tuple,
	Type,
)
import hwPortUtils
import NVDAState
import braille
import winUser
import config
import appModuleHandler
from baseObject import AutoPropertyObject
import re
from winAPI import messageWindow
import extensionPoints
from logHandler import log
from collections import defaultdict


HID_USAGE_PAGE_BRAILLE = 0x41

DBT_DEVNODES_CHANGED = 7

USB_ID_REGEX = re.compile(r"^VID_[0-9A-F]{4}&PID_[0-9A-F]{4}$", re.U)


class ProtocolType(StrEnum):
	HID = "hid"
	"""HID devices"""
	SERIAL = "serial"
	"""Serial devices (COM ports)"""
	CUSTOM = "custom"
	"""Devices with a manufacturer specific protocol"""


class CommunicationType(StrEnum):
	BLUETOOTH = "bluetooth"
	"""Bluetooth devices"""
	USB = "usb"
	"""USB devices"""


class _DeviceTypeMeta(type):
	# Mapping old attributes to the new enums
	_mapping = {
		"HID": ProtocolType.HID,
		"SERIAL": ProtocolType.SERIAL,
		"CUSTOM": ProtocolType.CUSTOM,
		"BLUETOOTH": CommunicationType.BLUETOOTH,
	}

	def __getattr__(cls, name: str) -> ProtocolType | CommunicationType:
		repl = cls._mapping.get(name)
		if repl is not None and NVDAState._allowDeprecatedAPI():
			log.warning(
				f"{cls.__name__}.{name} is deprecated. Use {repl.__class__.__name__}.{repl} instead.",
			)
			return repl
		raise AttributeError(f"'{cls.__name__}' object has no attribute '{name}'")


class DeviceType(metaclass=_DeviceTypeMeta):
	"""This class is kept for backwards compatibility.
	Former members were split into the L{ProtocolType} and L{CommunicationType} enums."""

	...


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if attrName == "DETECT_USB" and NVDAState._allowDeprecatedAPI():
		log.warning(f"{attrName} is deprecated.")
		return 1
	if attrName == "DETECT_BLUETOOTH" and NVDAState._allowDeprecatedAPI():
		log.warning(f"{attrName} is deprecated.")
		return 2
	_deprecatedConstantsMap = {
		"KEY_HID": ProtocolType.HID,
		"KEY_SERIAL": ProtocolType.SERIAL,
		"KEY_BLUETOOTH": CommunicationType.BLUETOOTH,
		"KEY_CUSTOM": ProtocolType.CUSTOM,
	}
	if attrName in _deprecatedConstantsMap and NVDAState._allowDeprecatedAPI():
		replacementSymbol = _deprecatedConstantsMap[attrName]
		log.warning(
			f"{attrName} is deprecated. "
			f"Use bdDetect.{replacementSymbol.__class__.__name__}.{replacementSymbol.value} instead. ",
		)
		return replacementSymbol.value
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


class DeviceMatch(NamedTuple):
	"""Represents a detected device."""

	type: ProtocolType
	"""The protocol type of the device."""
	id: str
	"""The identifier of the device."""
	port: str
	"""The port that can be used by a driver to communicate with a device."""
	deviceInfo: Dict[str, str]
	"""All known information about a device."""


MatchFuncT = Callable[[DeviceMatch], bool]


@dataclass(frozen=True)
class _UsbDeviceRegistryEntry:
	"""An internal class that contains information specific to an USB device registration."""

	id: str
	"""The identifier of the device."""
	type: ProtocolType
	"""The protocol type of the device."""
	useAsFallback: bool = field(default=False, compare=False)
	"""
	determine how a device is associated with a driver.
	If False (default), the device is immediately available for use with the driver.
	If True, the device is added to a fallback list and is used only if the primary driver cannot use
	initial devices, serving as a backup option in case of compatibility issues.
	This provides flexibility and robustness in managing driver-device connections.
	"""
	matchFunc: MatchFuncT | None = field(default=None, compare=False)
	"""
	An optional function which determines whether a given device matches.
	It takes a L{DeviceMatch} as its only argument
	and returns a C{bool} indicating whether it matched."""

	def matches(self, deviceMatch: DeviceMatch) -> bool:
		"""Returns whether this registry entry matches a specific device."""
		if deviceMatch.type != self.type or deviceMatch.id != self.id:
			return False
		if self.matchFunc is None:
			return True
		return self.matchFunc(deviceMatch)


DriverDictT = defaultdict[CommunicationType, set[_UsbDeviceRegistryEntry] | MatchFuncT]
_driverDevices = OrderedDict[str, DriverDictT]()

scanForDevices = extensionPoints.Chain[Tuple[str, DeviceMatch]]()
"""
A Chain that can be iterated to scan for devices.
Registered handlers should yield a tuple containing a driver name as str and DeviceMatch
Handlers are called with these keyword arguments:
@param usb: Whether the handler is expected to yield USB devices.
@type usb: bool
@param bluetooth: Whether the handler is expected to yield USB devices.
@type bluetooth: bool
@param limitToDevices: Drivers to which detection should be limited.
	C{None} if no driver filtering should occur.
@type limitToDevices: Optional[List[str]]
"""


def _isDebug():
	return config.conf["debugLog"]["hwIo"]


def getDriversForConnectedUsbDevices(
	limitToDevices: Optional[List[str]] = None,
) -> Iterator[Tuple[str, DeviceMatch]]:
	"""Get any matching drivers for connected USB devices.
	Looks for (and yields) custom drivers first, then considers if the device is may be compatible with the
	Standard HID Braille spec.
	@param limitToDevices: Drivers to which detection should be limited.
		C{None} if no driver filtering should occur.
	@return: Generator of pairs of drivers and device information.
	"""
	usbCustomDeviceMatches = (
		DeviceMatch(ProtocolType.CUSTOM, port["usbID"], port["devicePath"], port)
		for port in deviceInfoFetcher.usbDevices
	)
	usbComDeviceMatches = (
		DeviceMatch(ProtocolType.SERIAL, port["usbID"], port["port"], port)
		for port in deviceInfoFetcher.usbComPorts
	)
	# Tee is used to ensure that the DeviceMatches aren't created multiple times.
	# The processing of these HID device matches, looking for a custom driver, means that all
	# HID device matches are created, and by teeing the output the matches don't need to be created again.
	# The corollary is that clients of this method don't have to process all devices (and create all
	# device matches), if one is found early the iteration can stop.
	usbHidDeviceMatches, usbHidDeviceMatchesForCustom = itertools.tee(
		(
			DeviceMatch(ProtocolType.HID, port["usbID"], port["devicePath"], port)
			for port in deviceInfoFetcher.hidDevices
			if port["provider"] == CommunicationType.USB
		)
	)

	fallbackDriversAndMatches: list[set[str, DeviceMatch]] = []
	for match in itertools.chain(usbCustomDeviceMatches, usbHidDeviceMatchesForCustom, usbComDeviceMatches):
		for driver, devs in _driverDevices.items():
			if limitToDevices and driver not in limitToDevices:
				continue
			usbDefinitions = devs[CommunicationType.USB]
			for definition in usbDefinitions:
				if definition.matches(match):
					if definition.useAsFallback:
						fallbackDriversAndMatches.append({driver, match})
					else:
						yield (driver, match)

	hidName = _getStandardHidDriverName()
	if limitToDevices and hidName not in limitToDevices:
		return
	for match in usbHidDeviceMatches:
		# Check for the Braille HID protocol after any other device matching.
		# This ensures that a vendor specific driver is preferred over the braille HID protocol.
		# This preference may change in the future.
		if _isHIDBrailleMatch(match):
			yield (hidName, match)

	for driver, match in fallbackDriversAndMatches:
		yield (driver, match)


def _getStandardHidDriverName() -> str:
	"""Return the name of the standard HID Braille device driver"""
	import brailleDisplayDrivers.hidBrailleStandard

	return brailleDisplayDrivers.hidBrailleStandard.HidBrailleDriver.name


def _isHIDUsagePageMatch(match: DeviceMatch, usagePage: int) -> bool:
	return match.type == ProtocolType.HID and match.deviceInfo.get("HIDUsagePage") == usagePage


def _isHIDBrailleMatch(match: DeviceMatch) -> bool:
	return _isHIDUsagePageMatch(match, HID_USAGE_PAGE_BRAILLE)


def HIDUsagePageMatchFuncFactory(usagePage: int) -> MatchFuncT:
	"""
	Creates a match function that checks if a given HID usage page matches the specified usage page.
	:param usagePage: The HID usage page to match against.
	:returns: A partial function that takes an HID usage page and returns True if it matches the specified usage page, False otherwise.
	"""
	return partial(_isHIDUsagePageMatch, usagePage=usagePage)


def getDriversForPossibleBluetoothDevices(
	limitToDevices: Optional[List[str]] = None,
) -> Iterator[Tuple[str, DeviceMatch]]:
	"""Get any matching drivers for possible Bluetooth devices.
	Looks for (and yields) custom drivers first, then considers if the device is may be compatible with the
	Standard HID Braille spec.
	@param limitToDevices: Drivers to which detection should be limited.
		C{None} if no driver filtering should occur.
	@return: Generator of pairs of drivers and port information.
	"""
	btSerialMatchesForCustom = (
		DeviceMatch(ProtocolType.SERIAL, port["bluetoothName"], port["port"], port)
		for port in deviceInfoFetcher.comPorts
		if "bluetoothName" in port
	)
	# Tee is used to ensure that the DeviceMatches aren't created multiple times.
	# The processing of these HID device matches, looking for a custom driver, means that all
	# HID device matches are created, and by teeing the output the matches don't need to be created again.
	# The corollary is that clients of this method don't have to process all devices (and create all
	# device matches), if one is found early the iteration can stop.
	btHidDevMatchesForHid, btHidDevMatchesForCustom = itertools.tee(
		(
			DeviceMatch(ProtocolType.HID, port["hardwareID"], port["devicePath"], port)
			for port in deviceInfoFetcher.hidDevices
			if port["provider"] == CommunicationType.BLUETOOTH
		)
	)
	for match in itertools.chain(btSerialMatchesForCustom, btHidDevMatchesForCustom):
		for driver, devs in _driverDevices.items():
			if limitToDevices and driver not in limitToDevices:
				continue
			matchFunc = devs[CommunicationType.BLUETOOTH]
			if not callable(matchFunc):
				continue
			if matchFunc(match):
				yield (driver, match)

	hidName = _getStandardHidDriverName()
	if limitToDevices and hidName not in limitToDevices:
		return
	for match in btHidDevMatchesForHid:
		# Check for the Braille HID protocol after any other device matching.
		# This ensures that a vendor specific driver is preferred over the braille HID protocol.
		# This preference may change in the future.
		if _isHIDBrailleMatch(match):
			yield (hidName, match)


btDevsCacheT = Optional[List[Tuple[str, DeviceMatch]]]


class _DeviceInfoFetcher(AutoPropertyObject):
	"""Utility class that caches fetched info for available devices for the duration of one core pump cycle."""

	cachePropertiesByDefault = True

	def __init__(self):
		self._btDevsLock = threading.Lock()
		self._btDevsCache: btDevsCacheT = None

	#: Type info for auto property: _get_btDevsCache
	btDevsCache: btDevsCacheT

	def _get_btDevsCache(self) -> btDevsCacheT:
		with self._btDevsLock:
			return self._btDevsCache.copy() if self._btDevsCache else None

	def _set_btDevsCache(
		self,
		cache: btDevsCacheT,
	):
		with self._btDevsLock:
			self._btDevsCache = cache.copy() if cache else None

	#: Type info for auto property: _get_comPorts
	comPorts: list[dict[str, str]]

	def _get_comPorts(self) -> list[dict[str, str]]:
		return list(hwPortUtils.listComPorts(onlyAvailable=True))

	#: Type info for auto property: _get_usbDevices
	usbDevices: List[Dict]

	def _get_usbDevices(self) -> List[Dict]:
		return list(hwPortUtils.listUsbDevices(onlyAvailable=True))

	#: Type info for auto property: _get_usbComPorts
	usbComPorts: list[dict[str, str]]

	def _get_usbComPorts(self) -> list[dict[str, str]]:
		comPorts = []
		for port in self.comPorts:
			if (usbId := port.get("usbID")) is None:
				continue
			if (
				usbDict := next(
					(d for d in self.usbDevices if d.get("usbID") == usbId),
					None,
				)
			) is not None:
				comPorts.append(port | usbDict)
		return comPorts

	#: Type info for auto property: _get_hidDevices
	hidDevices: List[Dict]

	def _get_hidDevices(self) -> List[Dict]:
		return list(hwPortUtils.listHidDevices(onlyAvailable=True))


deviceInfoFetcher: Optional[_DeviceInfoFetcher] = None


class _Detector:
	"""Detector class used to automatically detect braille displays.
	This should only be used by the L{braille} module.
	"""

	def __init__(self):
		"""Constructor.
		After construction, a scan should be queued with L{queueBgScan}.
		"""
		self._executor = ThreadPoolExecutor(1)
		self._queuedFuture: Optional[Future] = None
		messageWindow.pre_handleWindowMessage.register(self.handleWindowMessage)
		appModuleHandler.post_appSwitch.register(self.pollBluetoothDevices)
		self._stopEvent = threading.Event()
		self._detectUsb = True
		self._detectBluetooth = True
		self._limitToDevices: Optional[List[str]] = None

	def _queueBgScan(
		self,
		usb: bool = False,
		bluetooth: bool = False,
		limitToDevices: Optional[List[str]] = None,
	):
		"""Queues a scan for devices.
		If a scan is already in progress, a new scan will be queued after the current scan.
		To explicitely cancel a scan in progress, use L{rescan}.
		@param usb: Whether USB devices should be detected for this and subsequent scans.
		@param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
		@param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
			C{None} if default driver filtering according to config should occur.
		"""
		self._detectUsb = usb
		self._detectBluetooth = bluetooth
		if limitToDevices is None and config.conf["braille"]["auto"]["excludedDisplays"]:
			limitToDevices = list(getBrailleDisplayDriversEnabledForDetection())
		self._limitToDevices = limitToDevices

		if self._queuedFuture:
			# This will cancel a queued scan (i.e. not the currently running scan, if any)
			# If this future belongs to a scan that is currently running or finished, this does nothing.
			self._queuedFuture.cancel()
		self._queuedFuture = self._executor.submit(self._bgScan, usb, bluetooth, limitToDevices)

	def _stopBgScan(self):
		"""Stops the current scan as soon as possible and prevents a queued scan to start."""
		self._stopEvent.set()
		if self._queuedFuture:
			# This will cancel a queued scan (i.e. not the currently running scan, if any)
			# If this future belongs to a scan that is currently running or finished, this does nothing.
			self._queuedFuture.cancel()

	@staticmethod
	def _bgScanUsb(
		usb: bool = True,
		limitToDevices: Optional[List[str]] = None,
	):
		"""Handler for L{scanForDevices} that yields USB devices.
		See the L{scanForDevices} documentation for information about the parameters.
		"""
		if not usb:
			return
		for driver, match in getDriversForConnectedUsbDevices(limitToDevices):
			yield (driver, match)

	@staticmethod
	def _bgScanBluetooth(
		bluetooth: bool = True,
		limitToDevices: Optional[List[str]] = None,
	):
		"""Handler for L{scanForDevices} that yields Bluetooth devices and keeps an internal cache of devices.
		See the L{scanForDevices} documentation for information about the parameters.
		"""
		if not bluetooth:
			return
		btDevs: Optional[Iterable[Tuple[str, DeviceMatch]]] = deviceInfoFetcher.btDevsCache
		if btDevs is None:
			btDevs = getDriversForPossibleBluetoothDevices(limitToDevices)
			# Cache Bluetooth devices for next time.
			btDevsCache = []
		else:
			btDevsCache = btDevs
		for driver, match in btDevs:
			if btDevsCache is not btDevs:
				btDevsCache.append((driver, match))
			yield (driver, match)
		if btDevsCache is not btDevs:
			deviceInfoFetcher.btDevsCache = btDevsCache

	def _bgScan(
		self,
		usb: bool,
		bluetooth: bool,
		limitToDevices: Optional[List[str]],
	):
		"""Performs the actual background scan.
		this function should be run on a background thread.
		@param usb: Whether USB devices should be detected for this particular scan.
		@param bluetooth: Whether Bluetooth devices should be detected for this particular scan.
		@param limitToDevices: Drivers to which detection should be limited for this scan.
			C{None} if no driver filtering should occur.
		"""
		# Clear the stop event before a scan is started.
		# Since a scan can take some time to complete, another thread can set the stop event to cancel it.
		self._stopEvent.clear()
		iterator = scanForDevices.iter(
			usb=usb,
			bluetooth=bluetooth,
			limitToDevices=limitToDevices,
		)
		for driver, match in iterator:
			if self._stopEvent.is_set():
				return
			if braille.handler.setDisplayByName(driver, detected=match):
				return
			if self._stopEvent.is_set():
				return

	def rescan(
		self,
		usb: bool = True,
		bluetooth: bool = True,
		limitToDevices: Optional[List[str]] = None,
	):
		"""Stop a current scan when in progress, and start scanning from scratch.
		@param usb: Whether USB devices should be detected for this and subsequent scans.
		@type usb: bool
		@param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
		@type bluetooth: bool
		@param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
			C{None} if default driver filtering according to config should occur.
		"""
		self._stopBgScan()
		# Clear the cache of bluetooth devices so new devices can be picked up.
		deviceInfoFetcher.btDevsCache = None
		self._queueBgScan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)

	def handleWindowMessage(self, msg=None, wParam=None):
		if msg == winUser.WM_DEVICECHANGE and wParam == DBT_DEVNODES_CHANGED:
			self.rescan(bluetooth=self._detectBluetooth, limitToDevices=self._limitToDevices)

	def pollBluetoothDevices(self):
		"""Poll bluetooth devices that might be in range.
		This does not cancel the current scan."""
		if not self._detectBluetooth:
			# Do not poll bluetooth devices at all when bluetooth is disabled.
			return
		if not deviceInfoFetcher.btDevsCache:
			return
		self._queueBgScan(bluetooth=self._detectBluetooth, limitToDevices=self._limitToDevices)

	def terminate(self):
		appModuleHandler.post_appSwitch.unregister(self.pollBluetoothDevices)
		messageWindow.pre_handleWindowMessage.unregister(self.handleWindowMessage)
		self._stopBgScan()
		# Clear the cache of bluetooth devices so new devices can be picked up with a new instance.
		deviceInfoFetcher.btDevsCache = None
		self._executor.shutdown(wait=False)


def getConnectedUsbDevicesForDriver(driver: str) -> Iterator[DeviceMatch]:
	"""Get any connected USB devices associated with a particular driver.
	@param driver: The name of the driver.
	@return: Device information for each device.
	@raise LookupError: If there is no detection data for this driver.
	"""
	usbDevs = itertools.chain(
		(
			DeviceMatch(ProtocolType.CUSTOM, port["usbID"], port["devicePath"], port)
			for port in deviceInfoFetcher.usbDevices
		),
		(
			DeviceMatch(ProtocolType.HID, port["usbID"], port["devicePath"], port)
			for port in deviceInfoFetcher.hidDevices
			if port["provider"] == CommunicationType.USB
		),
		(
			DeviceMatch(ProtocolType.SERIAL, port["usbID"], port["port"], port)
			for port in deviceInfoFetcher.usbComPorts
		),
	)

	fallbackMatches: list[DeviceMatch] = []

	for match in usbDevs:
		if driver == _getStandardHidDriverName():
			if _isHIDBrailleMatch(match):
				yield match
		else:
			usbDefinitions = _driverDevices[driver][CommunicationType.USB]
			for definition in usbDefinitions:
				if definition.matches(match):
					if definition.useAsFallback:
						fallbackMatches.append(match)
					else:
						yield match

	for match in fallbackMatches:
		yield match


def getPossibleBluetoothDevicesForDriver(driver: str) -> Iterator[DeviceMatch]:
	"""Get any possible Bluetooth devices associated with a particular driver.
	@param driver: The name of the driver.
	@return: Port information for each port.
	@raise LookupError: If there is no detection data for this driver.
	"""
	if driver == _getStandardHidDriverName():
		matchFunc = _isHIDBrailleMatch
	else:
		matchFunc = _driverDevices[driver][CommunicationType.BLUETOOTH]
		if not callable(matchFunc):
			return
	btDevs = itertools.chain(
		(
			DeviceMatch(ProtocolType.SERIAL, port["bluetoothName"], port["port"], port)
			for port in deviceInfoFetcher.comPorts
			if "bluetoothName" in port
		),
		(
			DeviceMatch(ProtocolType.HID, port["hardwareID"], port["devicePath"], port)
			for port in deviceInfoFetcher.hidDevices
			if port["provider"] == CommunicationType.BLUETOOTH
		),
	)
	for match in btDevs:
		if matchFunc(match):
			yield match


def driverHasPossibleDevices(driver: str) -> bool:
	"""Determine whether there are any possible devices associated with a given driver.
	@param driver: The name of the driver.
	@return: C{True} if there are possible devices, C{False} otherwise.
	@raise LookupError: If there is no detection data for this driver.
	"""
	return bool(
		next(
			itertools.chain(
				getConnectedUsbDevicesForDriver(driver),
				getPossibleBluetoothDevicesForDriver(driver),
			),
			None,
		),
	)


def driverSupportsAutoDetection(driver: str) -> bool:
	"""Returns whether the provided driver supports automatic detection of displays.
	@param driver: The name of the driver.
	@return: C{True} if de driver supports auto detection, C{False} otherwise.
	"""
	try:
		driverCls = braille._getDisplayDriver(driver)
	except ImportError:
		return False
	return driverCls.isThreadSafe and driverCls.supportsAutomaticDetection


def driverIsEnabledForAutoDetection(driver: str) -> bool:
	"""Returns whether the provided driver is enabled for automatic detection of displays.
	@param driver: The name of the driver.
	@return: C{True} if de driver is enabled for auto detection, C{False} otherwise.
	"""
	return driver in getBrailleDisplayDriversEnabledForDetection()


def getSupportedBrailleDisplayDrivers(
	onlyEnabled: bool = False,
) -> Generator[Type["braille.BrailleDisplayDriver"], Any, Any]:
	return braille.getDisplayDrivers(
		lambda d: (
			d.isThreadSafe
			and d.supportsAutomaticDetection
			and (not onlyEnabled or d.name not in config.conf["braille"]["auto"]["excludedDisplays"])
		),
	)


def getBrailleDisplayDriversEnabledForDetection() -> Generator[str, Any, Any]:
	return (d.name for d in getSupportedBrailleDisplayDrivers(onlyEnabled=True))


def initialize():
	"""Initializes bdDetect, such as detection data.
	Calls to addUsbDevice, addUsbDevices, and addBluetoothDevices.
	Specify the requirements for a detected device to be considered a
	match for a specific driver.
	"""
	global deviceInfoFetcher
	deviceInfoFetcher = _DeviceInfoFetcher()

	scanForDevices.register(_Detector._bgScanUsb)
	scanForDevices.register(_Detector._bgScanBluetooth)

	# Add devices
	for display in getSupportedBrailleDisplayDrivers():
		display.registerAutomaticDetection(DriverRegistrar(display.name))
	# Hack, Caiku Albatross detection conflicts with other drivers
	# when it isn't the last driver in the detection logic.
	_driverDevices.move_to_end("albatross")


def terminate():
	global deviceInfoFetcher
	_driverDevices.clear()
	scanForDevices.unregister(_Detector._bgScanBluetooth)
	scanForDevices.unregister(_Detector._bgScanUsb)
	deviceInfoFetcher = None


class DriverRegistrar:
	"""An object to facilitate registration of drivers in the bdDetect system.
	It is instanciated for a specific driver and
	passed to L{braille.BrailleDisplayDriver.registerAutomaticDetection}.
	"""

	_driver: str

	def __init__(self, driver: str):
		self._driver = driver

	def _getDriverDict(self) -> DriverDictT:
		try:
			return _driverDevices[self._driver]
		except KeyError:
			ret = _driverDevices[self._driver] = DriverDictT(set)
			return ret

	def addUsbDevice(
		self,
		type: ProtocolType,
		id: str,
		useAsFallback: bool = False,
		matchFunc: MatchFuncT | None = None,
	):
		"""Associate an USB device with the driver on this instance.
		:param type: The type of the driver.
		:param id: A USB ID in the form C{"VID_xxxx&PID_XXXX"}.
			Note that alphabetical characters in hexadecimal numbers should be uppercase.
		:param useAsFallback: A boolean flag to determine how this USB device is associated with the driver.
			If False (default), the device is added directly to the primary driver list for the specified type,
			meaning it is immediately available for use with the driver.
			If True, the device is used only if the primary driver cannot use
			the initial devices, serving as a backup option in case of compatibility issues.
			This provides flexibility and robustness in managing driver-device connections.
		@param matchFunc: An optional function which determines whether a given device matches.
			It takes a L{DeviceMatch} as its only argument
			and returns a C{bool} indicating whether it matched.
			It can be used to further constrain a device registration, such as for a specific HID usage page.
		:raise ValueError: When the provided ID is malformed.
		"""
		if not isinstance(id, str) or not USB_ID_REGEX.match(id):
			raise ValueError(
				f"Invalid ID provided for driver {self._driver!r}, type {type!r}: {id!r}",
			)
		devs = self._getDriverDict()
		driverUsb = devs[CommunicationType.USB]
		driverUsb.add(
			_UsbDeviceRegistryEntry(id=id, type=type, useAsFallback=useAsFallback, matchFunc=matchFunc),
		)

	def addUsbDevices(
		self,
		type: DeviceType,
		ids: set[str],
		useAsFallback: bool = False,
		matchFunc: MatchFuncT = None,
	):
		"""Associate USB devices with the driver on this instance.
		:param type: The type of the driver.
		:param ids: A set of USB IDs in the form C{"VID_xxxx&PID_XXXX"}.
			Note that alphabetical characters in hexadecimal numbers should be uppercase.
		:param useAsFallback: A boolean flag to determine how USB devices are associated with the driver.
			If False (default), the devices are added directly to the primary driver list for the specified type,
			meaning they are immediately available for use with the driver.
			If True, the devices are added to a fallback list and are used only if the primary driver cannot use
			the initial devices, serving as a backup option in case of compatibility issues.
			This provides flexibility and robustness in managing driver-device connections.
		@param matchFunc: An optional function which determines whether a given device matches.
			It takes a L{DeviceMatch} as its only argument
			and returns a C{bool} indicating whether it matched.
			It can be used to further constrain device registrations, such as for a specific HID usage page.
		:raise ValueError: When one of the provided IDs is malformed.
		"""
		malformedIds = [id for id in ids if not isinstance(id, str) or not USB_ID_REGEX.match(id)]
		if malformedIds:
			raise ValueError(
				f"Invalid IDs provided for driver {self._driver!r}, type {type!r}: {', '.join(malformedIds)}",
			)
		devs = self._getDriverDict()
		driverUsb = devs[CommunicationType.USB]
		driverUsb.update(
			(
				_UsbDeviceRegistryEntry(id=id, type=type, useAsFallback=useAsFallback, matchFunc=matchFunc)
				for id in ids
			)
		)

	def addBluetoothDevices(self, matchFunc: MatchFuncT):
		"""Associate Bluetooth HID or COM ports with the driver on this instance.
		@param matchFunc: A function which determines whether a given Bluetooth device matches.
			It takes a L{DeviceMatch} as its only argument
			and returns a C{bool} indicating whether it matched.
		"""
		devs = self._getDriverDict()
		devs[CommunicationType.BLUETOOTH] = matchFunc

	def addDeviceScanner(
		self,
		scanFunc: Callable[..., Iterable[Tuple[str, DeviceMatch]]],
		moveToStart: bool = False,
	):
		"""Register a callable to scan devices.
		This adds a handler to L{scanForDevices}.
		@param scanFunc: Callable that should yield a tuple containing a driver name as str and DeviceMatch.
			The callable is called with these keyword arguments:
			@param usb: Whether the handler is expected to yield USB devices.
			@type usb: bool
			@param bluetooth: Whether the handler is expected to yield USB devices.
			@type bluetooth: bool
			@param limitToDevices: Drivers to which detection should be limited.
				C{None} if no driver filtering should occur.
			@type limitToDevices: Optional[List[str]]
		@param moveToStart: If C{True}, the registered callable will be moved to the start
			of the list of registered handlers.
			Note that subsequent callback registrations may also request to be moved to the start.
			You should never rely on the registered callable being the first in order.
		"""
		scanForDevices.register(scanFunc)
		if moveToStart:
			scanForDevices.moveToEnd(scanFunc, last=False)
