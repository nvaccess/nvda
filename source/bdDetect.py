#bdDetect.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013-2017 NV Access Limited

"""Support for braille display detection.
This allows devices to be automatically detected and used when they become available,
as well as providing utilities to query for possible devices for a particular driver.
To support detection for a driver, devices need to be associated
using the C{add*} functions.
Drivers distributed with NVDA do this at the bottom of this module.
For drivers in add-ons, this must be done in a global plugin.
"""

import itertools
from collections import namedtuple, defaultdict, OrderedDict
import threading

import typing
import wx
import hwPortUtils
import braille
import winKernel
import winUser
import core
import ctypes
from logHandler import log
import config
import time
import appModuleHandler
from baseObject import AutoPropertyObject
import re


HID_USAGE_PAGE_BRAILLE = 0x41


DBT_DEVNODES_CHANGED=7

_driverDevices = OrderedDict()
USB_ID_REGEX = re.compile(r"^VID_[0-9A-F]{4}&PID_[0-9A-F]{4}$", re.U)

class DeviceMatch(
	namedtuple("DeviceMatch", ("type","id", "port", "deviceInfo"))
):
	"""Represents a detected device.
	@ivar id: The identifier of the device.
	@type id: str
	@ivar port: The port that can be used by a driver to communicate with a device.
	@type port: str
	@ivar deviceInfo: all known information about a device.
	@type deviceInfo: dict
	"""
	__slots__ = ()

# Device type constants
#: Key constant for HID devices
KEY_HID = "hid"
#: Key for serial devices (COM ports)
KEY_SERIAL = "serial"
#: Key for devices with a manufacturer specific driver
KEY_CUSTOM = "custom"
#: Key for bluetooth devices
KEY_BLUETOOTH = "bluetooth"

# Constants for USB and bluetooth detection to be used by the background thread scanner.
DETECT_USB = 1
DETECT_BLUETOOTH = 2

def _isDebug():
	return config.conf["debugLog"]["hwIo"]

def _getDriver(driver):
	try:
		return _driverDevices[driver]
	except KeyError:
		ret = _driverDevices[driver] = defaultdict(set)
		return ret

def addUsbDevices(driver, type, ids):
	"""Associate USB devices with a driver.
	@param driver: The name of the driver.
	@type driver: str
	@param type: The type of the driver, either C{KEY_HID}, C{KEY_SERIAL} or C{KEY_CUSTOM}.
	@type type: str
	@param ids: A set of USB IDs in the form C{"VID_xxxx&PID_XXXX"}.
		Note that alphabetical characters in hexadecimal numbers should be uppercase.
	@type ids: set of str
	@raise ValueError: When one of the provided IDs is malformed.
	"""
	malformedIds = [id for id in ids if not isinstance(id, str) or not USB_ID_REGEX.match(id)]
	if malformedIds:
		raise ValueError("Invalid IDs provided for driver %s, type %s: %s"
			% (driver, type, u", ".join(malformedIds)))
	devs = _getDriver(driver)
	driverUsb = devs[type]
	driverUsb.update(ids)

def addBluetoothDevices(driver, matchFunc):
	"""Associate Bluetooth HID or COM ports with a driver.
	@param driver: The name of the driver.
	@type driver: str
	@param matchFunc: A function which determines whether a given Bluetooth device matches.
		It takes a L{DeviceMatch} as its only argument
		and returns a C{bool} indicating whether it matched.
	@type matchFunc: callable
	"""
	devs = _getDriver(driver)
	devs[KEY_BLUETOOTH] = matchFunc


def getDriversForConnectedUsbDevices() -> typing.Iterator[typing.Tuple[str, DeviceMatch]]:
	"""Get any matching drivers for connected USB devices.
	Looks for (and yields) custom drivers first, then considers if the device is may be compatible with the
	Standard HID Braille spec.
	@return: Generator of pairs of drivers and device information.
	"""
	usbCustomDeviceMatches = (
		DeviceMatch(KEY_CUSTOM, port["usbID"], port["devicePath"], port)
		for port in deviceInfoFetcher.usbDevices
	)
	usbComDeviceMatches = (
		DeviceMatch(KEY_SERIAL, port["usbID"], port["port"], port)
		for port in deviceInfoFetcher.comPorts
		if "usbID" in port
	)
	# Tee is used to ensure that the DeviceMatches aren't created multiple times.
	# The processing of these HID device matches, looking for a custom driver, means that all
	# HID device matches are created, and by teeing the output the matches don't need to be created again.
	# The corollary is that clients of this method don't have to process all devices (and create all
	# device matches), if one is found early the iteration can stop.
	usbHidDeviceMatches, usbHidDeviceMatchesForCustom = itertools.tee((
		DeviceMatch(KEY_HID, port["usbID"], port["devicePath"], port)
		for port in deviceInfoFetcher.hidDevices
		if port["provider"] == "usb"
	))
	for match in itertools.chain(usbCustomDeviceMatches, usbHidDeviceMatchesForCustom, usbComDeviceMatches):
		for driver, devs in _driverDevices.items():
			for type, ids in devs.items():
				if match.type==type and match.id in ids:
					yield driver, match

	if _isHidBrailleStandardSupported():
		for match in usbHidDeviceMatches:
			# Check for the Braille HID protocol after any other device matching.
			# This ensures that a vendor specific driver is preferred over the braille HID protocol.
			# This preference may change in the future.
			if _isHIDBrailleMatch(match):
				yield (
					_getStandardHidDriverName(),
					match
				)


def _getStandardHidDriverName() -> str:
	"""Return the name of the standard HID Braille device driver
	"""
	import brailleDisplayDrivers.hidBrailleStandard
	return brailleDisplayDrivers.hidBrailleStandard.HidBrailleDriver.name


def _isHidBrailleStandardSupported() -> bool:
	"""Check if standard HID braille is supported"""
	import brailleDisplayDrivers.hidBrailleStandard
	return brailleDisplayDrivers.hidBrailleStandard.isSupportEnabled()


def _isHIDBrailleMatch(match: DeviceMatch) -> bool:
	return match.type == KEY_HID and match.deviceInfo.get('HIDUsagePage') == HID_USAGE_PAGE_BRAILLE


def getDriversForPossibleBluetoothDevices() -> typing.Iterator[typing.Tuple[str, DeviceMatch]]:
	"""Get any matching drivers for possible Bluetooth devices.
	Looks for (and yields) custom drivers first, then considers if the device is may be compatible with the
	Standard HID Braille spec.
	@return: Generator of pairs of drivers and port information.
	"""
	btSerialMatchesForCustom = (
		DeviceMatch(KEY_SERIAL, port["bluetoothName"], port["port"], port)
		for port in deviceInfoFetcher.comPorts
		if "bluetoothName" in port
	)
	# Tee is used to ensure that the DeviceMatches aren't created multiple times.
	# The processing of these HID device matches, looking for a custom driver, means that all
	# HID device matches are created, and by teeing the output the matches don't need to be created again.
	# The corollary is that clients of this method don't have to process all devices (and create all
	# device matches), if one is found early the iteration can stop.
	btHidDevMatchesForHid, btHidDevMatchesForCustom = itertools.tee((
		DeviceMatch(KEY_HID, port["hardwareID"], port["devicePath"], port)
		for port in deviceInfoFetcher.hidDevices
		if port["provider"] == "bluetooth"
	))
	for match in itertools.chain(btSerialMatchesForCustom, btHidDevMatchesForCustom):
		for driver, devs in _driverDevices.items():
			matchFunc = devs[KEY_BLUETOOTH]
			if not callable(matchFunc):
				continue
			if matchFunc(match):
				yield driver, match

	if _isHidBrailleStandardSupported():
		for match in btHidDevMatchesForHid:
			# Check for the Braille HID protocol after any other device matching.
			# This ensures that a vendor specific driver is preferred over the braille HID protocol.
			# This preference may change in the future.
			if _isHIDBrailleMatch(match):
				yield (
					_getStandardHidDriverName(),
					match
				)


class _DeviceInfoFetcher(AutoPropertyObject):
	"""Utility class that caches fetched info for available devices for the duration of one core pump cycle."""
	cachePropertiesByDefault = True

	#: Type info for auto property: _get_comPorts
	comPorts: typing.List[typing.Dict]

	def _get_comPorts(self) -> typing.List[typing.Dict]:
		return list(hwPortUtils.listComPorts(onlyAvailable=True))

	#: Type info for auto property: _get_usbDevices
	usbDevices: typing.List[typing.Dict]

	def _get_usbDevices(self) -> typing.List[typing.Dict]:
		return list(hwPortUtils.listUsbDevices(onlyAvailable=True))

	#: Type info for auto property: _get_hidDevices
	hidDevices: typing.List[typing.Dict]

	def _get_hidDevices(self) -> typing.List[typing.Dict]:
		return list(hwPortUtils.listHidDevices(onlyAvailable=True))

#: The single instance of the device info fetcher.
#: @type: L{_DeviceInfoFetcher}
deviceInfoFetcher = _DeviceInfoFetcher()

class Detector(object):
	"""Detector class used to automatically detect braille displays.
	This should only be used by the L{braille} module.
	"""

	def __init__(self, usb=True, bluetooth=True, limitToDevices=None):
		"""Constructor.
		The keyword arguments initialize the detector in a particular state.
		On an initialized instance, these initial arguments can be overridden by calling L{_startBgScan} or L{rescan}.
		@param usb: Whether this instance should detect USB devices initially.
		@type usb: bool
		@param bluetooth: Whether this instance should detect Bluetooth devices initially.
		@type bluetooth: bool
		@param limitToDevices: Drivers to which detection should be limited initially.
			C{None} if no driver filtering should occur.
		"""
		self._BgScanApc = winKernel.PAPCFUNC(self._bgScan)
		self._btDevsLock = threading.Lock()
		self._btDevs = None
		core.post_windowMessageReceipt.register(self.handleWindowMessage)
		appModuleHandler.post_appSwitch.register(self.pollBluetoothDevices)
		self._stopEvent = threading.Event()
		self._queuedScanLock = threading.Lock()
		self._scanQueued = False
		self._detectUsb = usb
		self._detectBluetooth = bluetooth
		self._limitToDevices = limitToDevices
		self._runningApcLock = threading.Lock()
		# Perform initial scan.
		self._startBgScan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)

	@property
	def _scanQueuedSafe(self):
		"""Returns L{_scanQueued} in a thread safe way by using L{_queuedScanLock}."""
		with self._queuedScanLock:
			return self._scanQueued

	@_scanQueuedSafe.setter
	def _scanQueuedSafe(self, state):
		"""Sets L{_scanQueued} in a thread safe way by using L{_queuedScanLock}."""
		with self._queuedScanLock:
			self._scanQueued = state

	def _startBgScan(self, usb=False, bluetooth=False, limitToDevices=None):
		"""Starts a scan for devices.
		If a scan is already in progress, a new scan will be queued after the current scan.
		To explicitely cancel a scan in progress, use L{rescan}.
		@param usb: Whether USB devices should be detected for this and subsequent scans.
		@type usb: bool
		@param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
		@type bluetooth: bool
		@param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
			C{None} if no driver filtering should occur.
		"""
		with self._queuedScanLock:
			self._detectUsb = usb
			self._detectBluetooth = bluetooth
			self._limitToDevices = limitToDevices
			if not self._scanQueued:
				self._scanQueued = True
				if self._runningApcLock.locked():
					# There's currently a scan in progress.
					# Since the scan is embeded in a loop, it will automatically do another scan,
					# unless a display has been found.
					return
				braille._BgThread.queueApc(self._BgScanApc)

	def _stopBgScan(self):
		"""Stops the current scan as soon as possible and prevents a queued scan to start."""
		if not self._runningApcLock.locked():
			# No scan to stop
			return
		self._stopEvent.set()
		self._scanQueuedSafe = False

	def _bgScan(self, param):
		if self._runningApcLock.locked():
			log.debugWarning("Braille display detection background scan APC executed while one is already running")
			return
		with self._runningApcLock:
			while self._scanQueuedSafe:
				# Clear the stop event before a scan is started.
				# Since a scan can take some time to complete, another thread can set the stop event to cancel it.
				self._stopEvent.clear()
				with self._queuedScanLock:
					self._scanQueued = False
					detectUsb = self._detectUsb
					detectBluetooth = self._detectBluetooth
					limitToDevices = self._limitToDevices
				if detectUsb:
					if self._stopEvent.isSet():
						continue
					for driver, match in getDriversForConnectedUsbDevices():
						if self._stopEvent.isSet() or (self._limitToDevices and driver not in self._limitToDevices):
							continue
						if braille.handler.setDisplayByName(driver, detected=match):
							return
				if detectBluetooth:
					if self._stopEvent.isSet():
						continue
					with self._btDevsLock:
						if self._btDevs is None:
							btDevs = list(getDriversForPossibleBluetoothDevices())
							# Cache Bluetooth devices for next time.
							btDevsCache = []
						else:
							btDevs = self._btDevs
							btDevsCache = btDevs
					for driver, match in btDevs:
						if self._stopEvent.isSet() or (self._limitToDevices and driver not in self._limitToDevices):
							continue
						if btDevsCache is not btDevs:
							btDevsCache.append((driver, match))
						if braille.handler.setDisplayByName(driver, detected=match):
							return
					if self._stopEvent.isSet():
						continue
					if btDevsCache is not btDevs:
						with self._btDevsLock:
							self._btDevs = btDevsCache

	def rescan(self, usb=True, bluetooth=True, limitToDevices=None):
		"""Stop a current scan when in progress, and start scanning from scratch.
		@param usb: Whether USB devices should be detected for this and subsequent scans.
		@type usb: bool
		@param bluetooth: Whether Bluetooth devices should be detected for this and subsequent scans.
		@type bluetooth: bool
		@param limitToDevices: Drivers to which detection should be limited for this and subsequent scans.
			C{None} if no driver filtering should occur.
		"""
		self._stopBgScan()
		with self._btDevsLock:
			# A Bluetooth com port or HID device might have been added.
			self._btDevs = None
		self._startBgScan(usb=usb, bluetooth=bluetooth, limitToDevices=limitToDevices)

	def handleWindowMessage(self, msg=None, wParam=None):
		if msg == winUser.WM_DEVICECHANGE and wParam == DBT_DEVNODES_CHANGED:
			self.rescan(bluetooth=self._detectBluetooth, limitToDevices=self._limitToDevices)

	def pollBluetoothDevices(self):
		"""Poll bluetooth devices that might be in range.
		This does not cancel the current scan."""
		if not self._detectBluetooth:
			# Do not poll bluetooth devices at all when bluetooth is disabled.
			return
		with self._btDevsLock:
			if not self._btDevs:
				return
		self._startBgScan(bluetooth=self._detectBluetooth, limitToDevices=self._limitToDevices)

	def terminate(self):
		appModuleHandler.post_appSwitch.unregister(self.pollBluetoothDevices)
		core.post_windowMessageReceipt.unregister(self.handleWindowMessage)
		self._stopBgScan()


def getConnectedUsbDevicesForDriver(driver) -> typing.Iterator[DeviceMatch]:
	"""Get any connected USB devices associated with a particular driver.
	@param driver: The name of the driver.
	@type driver: str
	@return: Device information for each device.
	@raise LookupError: If there is no detection data for this driver.
	"""
	usbDevs = itertools.chain(
		(DeviceMatch(KEY_CUSTOM, port["usbID"], port["devicePath"], port)
			for port in deviceInfoFetcher.usbDevices),
		(DeviceMatch(KEY_HID, port["usbID"], port["devicePath"], port)
			for port in deviceInfoFetcher.hidDevices if port["provider"]=="usb"),
		(DeviceMatch(KEY_SERIAL, port["usbID"], port["port"], port)
			for port in deviceInfoFetcher.comPorts if "usbID" in port)
	)
	for match in usbDevs:
		if driver == _getStandardHidDriverName():
			if(
				_isHidBrailleStandardSupported()
				and _isHIDBrailleMatch(match)
			):
				yield match
		else:
			devs = _driverDevices[driver]
			for type, ids in devs.items():
				if match.type == type and match.id in ids:
					yield match


def getPossibleBluetoothDevicesForDriver(driver) -> typing.Iterator[DeviceMatch]:
	"""Get any possible Bluetooth devices associated with a particular driver.
	@param driver: The name of the driver.
	@type driver: str
	@return: Port information for each port.
	@raise LookupError: If there is no detection data for this driver.
	"""
	if driver == _getStandardHidDriverName():
		def matchFunc(checkMatch: DeviceMatch) -> bool:
			return (
				_isHidBrailleStandardSupported()
				and _isHIDBrailleMatch(checkMatch)
			)
	else:
		matchFunc = _driverDevices[driver][KEY_BLUETOOTH]
		if not callable(matchFunc):
			return
	btDevs = itertools.chain(
		(DeviceMatch(KEY_SERIAL, port["bluetoothName"], port["port"], port)
			for port in deviceInfoFetcher.comPorts
			if "bluetoothName" in port),
		(DeviceMatch(KEY_HID, port["hardwareID"], port["devicePath"], port)
			for port in deviceInfoFetcher.hidDevices if port["provider"]=="bluetooth"),
	)
	for match in btDevs:
		if matchFunc(match):
			yield match

def driverHasPossibleDevices(driver):
	"""Determine whether there are any possible devices associated with a given driver.
	@param driver: The name of the driver.
	@type driver: str
	@return: C{True} if there are possible devices, C{False} otherwise.
	@rtype: bool
	@raise LookupError: If there is no detection data for this driver.
	"""
	return bool(next(itertools.chain(
		getConnectedUsbDevicesForDriver(driver),
		getPossibleBluetoothDevicesForDriver(driver)
	), None))

def driverSupportsAutoDetection(driver):
	"""Returns whether the provided driver supports automatic detection of displays.
	@param driver: The name of the driver.
	@type driver: str
	@return: C{True} if de driver supports auto detection, C{False} otherwise.
	@rtype: bool
	"""
	return driver in _driverDevices


def initializeDetectionData():
	""" Initialize detection data.
	Calls to addUsbDevices, and addBluetoothDevices.
	Specify the requirements for a detected device to be considered a
	match for a specific driver.
	"""
	# alva
	addUsbDevices("alva", KEY_HID, {
		"VID_0798&PID_0640",  # BC640
		"VID_0798&PID_0680",  # BC680
		"VID_0798&PID_0699",  # USB protocol converter
	})

	addBluetoothDevices("alva", lambda m: m.id.startswith("ALVA "))

	# baum
	addUsbDevices("baum", KEY_HID, {
		"VID_0904&PID_3001",  # RefreshaBraille 18
		"VID_0904&PID_6101",  # VarioUltra 20
		"VID_0904&PID_6103",  # VarioUltra 32
		"VID_0904&PID_6102",  # VarioUltra 40
		"VID_0904&PID_4004",  # Pronto! 18 V3
		"VID_0904&PID_4005",  # Pronto! 40 V3
		"VID_0904&PID_4007",  # Pronto! 18 V4
		"VID_0904&PID_4008",  # Pronto! 40 V4
		"VID_0904&PID_6001",  # SuperVario2 40
		"VID_0904&PID_6002",  # SuperVario2 24
		"VID_0904&PID_6003",  # SuperVario2 32
		"VID_0904&PID_6004",  # SuperVario2 64
		"VID_0904&PID_6005",  # SuperVario2 80
		"VID_0904&PID_6006",  # Brailliant2 40
		"VID_0904&PID_6007",  # Brailliant2 24
		"VID_0904&PID_6008",  # Brailliant2 32
		"VID_0904&PID_6009",  # Brailliant2 64
		"VID_0904&PID_600A",  # Brailliant2 80
		"VID_0904&PID_6201",  # Vario 340
		"VID_0483&PID_A1D3",  # Orbit Reader 20
		"VID_0904&PID_6301",  # Vario 4
	})

	addUsbDevices("baum", KEY_SERIAL, {
		"VID_0403&PID_FE70",  # Vario 40
		"VID_0403&PID_FE71",  # PocketVario
		"VID_0403&PID_FE72",  # SuperVario/Brailliant 40
		"VID_0403&PID_FE73",  # SuperVario/Brailliant 32
		"VID_0403&PID_FE74",  # SuperVario/Brailliant 64
		"VID_0403&PID_FE75",  # SuperVario/Brailliant 80
		"VID_0904&PID_2001",  # EcoVario 24
		"VID_0904&PID_2002",  # EcoVario 40
		"VID_0904&PID_2007",  # VarioConnect/BrailleConnect 40
		"VID_0904&PID_2008",  # VarioConnect/BrailleConnect 32
		"VID_0904&PID_2009",  # VarioConnect/BrailleConnect 24
		"VID_0904&PID_2010",  # VarioConnect/BrailleConnect 64
		"VID_0904&PID_2011",  # VarioConnect/BrailleConnect 80
		"VID_0904&PID_2014",  # EcoVario 32
		"VID_0904&PID_2015",  # EcoVario 64
		"VID_0904&PID_2016",  # EcoVario 80
		"VID_0904&PID_3000",  # RefreshaBraille 18
	})

	addBluetoothDevices("baum", lambda m: any(m.id.startswith(prefix) for prefix in (
		"Baum SuperVario",
		"Baum PocketVario",
		"Baum SVario",
		"HWG Brailliant",
		"Refreshabraille",
		"VarioConnect",
		"BrailleConnect",
		"Pronto!",
		"VarioUltra",
		"Orbit Reader 20",
		"Vario 4",
	)))

	# brailleNote
	addUsbDevices("brailleNote", KEY_SERIAL, {
		"VID_1C71&PID_C004",  # Apex
	})
	addBluetoothDevices("brailleNote", lambda m: (
		any(
			first <= m.deviceInfo.get("bluetoothAddress", 0) <= last
			for first, last in (
				(0x0025EC000000, 0x0025EC01869F),  # Apex
			)
		)
		or m.id.startswith("Braillenote")
	))

	# brailliantB
	addUsbDevices("brailliantB", KEY_HID, {
		"VID_1C71&PID_C111",  # Mantis Q 40
		"VID_1C71&PID_C101",  # Chameleon 20
		"VID_1C71&PID_C121",  # Humanware BrailleOne 20 HID
		"VID_1C71&PID_CE01",  # NLS eReader 20 HID
		"VID_1C71&PID_C006",  # Brailliant BI 32, 40 and 80
		"VID_1C71&PID_C022",  # Brailliant BI 14
		"VID_1C71&PID_C131",  # Brailliant BI 40X
		"VID_1C71&PID_C141",  # Brailliant BI 20X
		"VID_1C71&PID_C00A",  # BrailleNote Touch
		"VID_1C71&PID_C00E",  # BrailleNote Touch v2
	})
	addUsbDevices("brailliantB", KEY_SERIAL, {
		"VID_1C71&PID_C005",  # Brailliant BI 32, 40 and 80
		"VID_1C71&PID_C021",  # Brailliant BI 14
	})
	addBluetoothDevices(
		"brailliantB", lambda m: (
			m.type == KEY_SERIAL
			and (
				m.id.startswith("Brailliant B")
				or m.id == "Brailliant 80"
				or "BrailleNote Touch" in m.id
			)
		)
		or (
			m.type == KEY_HID
			and m.deviceInfo.get("manufacturer") == "Humanware"
			and m.deviceInfo.get("product") in (
				"Brailliant HID",
				"APH Chameleon 20",
				"APH Mantis Q40",
				"Humanware BrailleOne",
				"NLS eReader",
				"NLS eReader Humanware",
				"Brailliant BI 40X",
				"Brailliant BI 20X",
			)
		)
	)

	# eurobraille
	addUsbDevices("eurobraille", KEY_HID, {
		"VID_C251&PID_1122",  # Esys (version < 3.0, no SD card
		"VID_C251&PID_1123",  # Esys (version >= 3.0, with HID keyboard, no SD card
		"VID_C251&PID_1124",  # Esys (version < 3.0, with SD card
		"VID_C251&PID_1125",  # Esys (version >= 3.0, with HID keyboard, with SD card
		"VID_C251&PID_1126",  # Esys (version >= 3.0, no SD card
		"VID_C251&PID_1127",  # Reserved
		"VID_C251&PID_1128",  # Esys (version >= 3.0, with SD card
		"VID_C251&PID_1129",  # Reserved
		"VID_C251&PID_112A",  # Reserved
		"VID_C251&PID_112B",  # Reserved
		"VID_C251&PID_112C",  # Reserved
		"VID_C251&PID_112D",  # Reserved
		"VID_C251&PID_112E",  # Reserved
		"VID_C251&PID_112F",  # Reserved
		"VID_C251&PID_1130",  # Esytime
		"VID_C251&PID_1131",  # Reserved
		"VID_C251&PID_1132",  # Reserved
	})

	addBluetoothDevices("eurobraille", lambda m: m.id.startswith("Esys"))

	# freedomScientific
	addUsbDevices("freedomScientific", KEY_CUSTOM, {
		"VID_0F4E&PID_0100",  # Focus 1
		"VID_0F4E&PID_0111",  # PAC Mate
		"VID_0F4E&PID_0112",  # Focus 2
		"VID_0F4E&PID_0114",  # Focus Blue
	})

	addBluetoothDevices("freedomScientific", lambda m: (
		any(
			m.id.startswith(prefix)
			for prefix in (
				"F14", "Focus 14 BT",
				"Focus 40 BT",
				"Focus 80 BT",
			)
		)
	))

	# handyTech
	addUsbDevices("handyTech", KEY_SERIAL, {
		"VID_0403&PID_6001",  # FTDI chip
		"VID_0921&PID_1200",  # GoHubs chip
	})

	# Newer Handy Tech displays have a native HID processor
	addUsbDevices("handyTech", KEY_HID, {
		"VID_1FE4&PID_0054",  # Active Braille
		"VID_1FE4&PID_0055",  # Connect Braille
		"VID_1FE4&PID_0061",  # Actilino
		"VID_1FE4&PID_0064",  # Active Star 40
		"VID_1FE4&PID_0081",  # Basic Braille 16
		"VID_1FE4&PID_0082",  # Basic Braille 20
		"VID_1FE4&PID_0083",  # Basic Braille 32
		"VID_1FE4&PID_0084",  # Basic Braille 40
		"VID_1FE4&PID_008A",  # Basic Braille 48
		"VID_1FE4&PID_0086",  # Basic Braille 64
		"VID_1FE4&PID_0087",  # Basic Braille 80
		"VID_1FE4&PID_008B",  # Basic Braille 160
		"VID_1FE4&PID_008C",  # Basic Braille 84
		"VID_1FE4&PID_0093",  # Basic Braille Plus 32
		"VID_1FE4&PID_0094",  # Basic Braille Plus 40
	})

	# Some older HT displays use a HID converter and an internal serial interface
	addUsbDevices("handyTech", KEY_HID, {
		"VID_1FE4&PID_0003",  # USB-HID adapter
		"VID_1FE4&PID_0074",  # Braille Star 40
		"VID_1FE4&PID_0044",  # Easy Braille
	})

	addBluetoothDevices("handyTech", lambda m: any(m.id.startswith(prefix) for prefix in (
		"Actilino AL",
		"Active Braille AB",
		"Active Star AS",
		"Basic Braille BB",
		"Basic Braille Plus BP",
		"Braille Star 40 BS",
		"Braillino BL",
		"Braille Wave BW",
		"Easy Braille EBR",
	)))

	# hims
	# Bulk devices
	addUsbDevices("hims", KEY_CUSTOM, {
		"VID_045E&PID_930A",  # Braille Sense & Smart Beetle
		"VID_045E&PID_930B",  # Braille EDGE 40
	})

	# Sync Braille, serial device
	addUsbDevices("hims", KEY_SERIAL, {
		"VID_0403&PID_6001",
	})

	addBluetoothDevices("hims", lambda m: any(m.id.startswith(prefix) for prefix in (
		"BrailleSense",
		"BrailleEDGE",
		"SmartBeetle",
	)))

	# NattiqBraille
	addUsbDevices("nattiqbraille", KEY_SERIAL, {
		"VID_2341&PID_8036",  # Atmel-based USB Serial for Nattiq nBraille
	})

	# superBrl
	addUsbDevices("superBrl", KEY_SERIAL, {
		"VID_10C4&PID_EA60",  # SuperBraille 3.2
	})

	# seika
	addUsbDevices("seikantk", KEY_HID, {
		"VID_10C4&PID_EA80",  # Seika Notetaker
	})

	from brailleDisplayDrivers.seikantk import isSeikaBluetoothDeviceMatch
	addBluetoothDevices(
		"seikantk",
		isSeikaBluetoothDeviceMatch
	)
