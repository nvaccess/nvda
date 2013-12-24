#bdDetect.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

"""Support for braille display detection.
This allows devices to be automatically detected and used when they become available,
as well as providing utilities to query for possible devices for a particular driver.
To support detection for a driver, devices need to be associated
using the C{add*} functions.
Drivers distributed with NVDA do this at the bottom of this module.
For drivers in add-ons, this must be done in a global plugin.
"""

import itertools
from collections import namedtuple
import threading
import weakref
import wx
import hwPortUtils
import braille
import windowUtils

#: How often (in ms) to poll for Bluetooth devices.
POLL_INTERVAL = 10000

_driverDevices = {}

_KEY_USBDEVS = "usbDevices"
_KEY_BTCOMS = "bluetoothComPorts"

def _getDriver(driver):
	try:
		return _driverDevices[driver]
	except KeyError:
		ret = _driverDevices[driver] = {
				_KEY_USBDEVS: set(),
			}
		return ret

def addUsbDevices(driver, ids):
	"""Associate USB devices with a driver.
	@param driver: The name of the driver.
	@type driver: str
	@param ids: A set of USB IDs in the form C{"VID_xxxx&PID_XXXX"}.
	@type ids: set of str
	"""
	devs = _getDriver(driver)
	driverUsb = devs[_KEY_USBDEVS]
	driverUsb.update(ids)

UsbDeviceMatch = namedtuple("UsbDeviceMatch", ("id",))

def addBluetoothComPorts(driver, matchFunc):
	"""Associate Bluetooth com ports with a driver.
	@param driver: The name of the driver.
	@type driver: str
	@param matchFunc: A function which determines whether a given Bluetooth com port matches.
		It takes a L{BluetoothComPortMatch} as its only argument
		and returns a C{bool} indicating whether it matched.
	@type matchFunc: callable
	"""
	devs = _getDriver(driver)
	devs[_KEY_BTCOMS] = matchFunc

class BluetoothComPortMatch(
	namedtuple("BluetoothComPortMatch", ("address", "name", "port"))
):
	"""Represents a detected Bluetooth com port.
	@ivar address: The MAC address of the device.
	@type address: int
	@ivar name: The Bluetooth name of the device.
	@type name: unicode
	@ivar port: The com port.
	@type port: unicode
	"""
	__slots__ = ()

def _isComAvailable(port):
	import serial
	try:
		ser = serial.Serial(port)
	except:
		return False
	else:
		ser.close()
		return True
	return False

def getDriversForConnectedUsbDevices():
	"""Get any matching drivers for connected USB devices.
	@return: Pairs of drivers and device information.
	@rtype: generator of (str, L{UsbDeviceMatch}) tuples
	"""
	usbDevs = set(hwPortUtils.listUsbDevices())
	for driver, devs in _driverDevices.iteritems():
		driverUsb = devs[_KEY_USBDEVS]
		matching = driverUsb & usbDevs
		for usbId in matching:
			yield driver, UsbDeviceMatch(usbId)

def getDriversForPossibleBluetoothComPorts():
	"""Get any matching drivers for possible Bluetooth com ports.
	@return: Pairs of drivers and port information.
	@rtype: generator of (str, L{BluetoothComPortMatch}) tuples
	"""
	btComs = [BluetoothComPortMatch(port["bluetoothAddress"], port["bluetoothName"], port["port"])
		for port in hwPortUtils.listComPorts()
		if "bluetoothName" in port]
	for driver, devs in _driverDevices.iteritems():
		try:
			match = devs[_KEY_BTCOMS]
		except KeyError:
			continue
		for port in btComs:
			if match(port):
				yield driver, port

WM_DEVICECHANGE = 0x0219
DBT_DEVNODES_CHANGED = 0x0007
class _DeviceChangeListener(windowUtils.CustomWindow):
	className = u"NVDADeviceChangeListener"

	def __init__(self, detector):
		super(_DeviceChangeListener, self).__init__()
		self._detector = weakref.ref(detector)
		self._callLater = None

	def windowProc(self, hwnd, message, wParam, lParam):
		if message != WM_DEVICECHANGE or wParam != DBT_DEVNODES_CHANGED:
			return
		if self._callLater and not self._callLater.HasRun():
			# There's already a pending call.
			return
		# Delay the call to avoid flooding.
		self._callLater = wx.CallLater(300, self._detector().handleDeviceChange)

class Detector(object):
	"""Automatically detect braille displays.
	This should only be used by the L{braille} module.
	"""

	def __init__(self):
		self._btComs = None
		self._callLater = None
		self._thread = None
		self._devChangeListener = _DeviceChangeListener(self)
		# Perform initial scan.
		self._startBgScan(dict(usb=True, bluetooth=True))

	def _startBgScan(self, kwargs):
		self._stopEvent = kwargs["stopEvent"] = threading.Event()
		self._thread = threading.Thread(target=self._bgScan, kwargs=kwargs)
		self._thread.start()

	def _stopBgScan(self):
		if not self._thread:
			return
		self._stopEvent.set()
		if self._callLater:
			self._callLater.Stop()
			self._callLater = None

	def _bgScan(self, usb=False, bluetooth=False, stopEvent=None):
		if usb:
			if stopEvent.isSet():
				return
			for driver, match in getDriversForConnectedUsbDevices():
				wx.CallAfter(braille.handler.handleDetectedDisplay, driver, match)
				return

		if bluetooth:
			if self._btComs is None:
				btComs = getDriversForPossibleBluetoothComPorts()
				# Cache Bluetooth com ports for next time.
				btComsCache = []
			else:
				btComs = self._btComs
				btComsCache = btComs
			for driver, match in btComs:
				if stopEvent.isSet():
					return
				if _isComAvailable(match.port):
					if stopEvent.isSet():
						return
					wx.CallAfter(braille.handler.handleDetectedDisplay, driver, match)
					return
				if btComsCache is not btComs:
					btComsCache.append((driver, match))
			if stopEvent.isSet():
				return
			if btComsCache is not btComs:
				self._btComs = btComsCache
			if btComsCache:
				# There were possible ports, so poll them periodically.
				self._callLater = wx.CallLater(POLL_INTERVAL, self._startBgScan, dict(bluetooth=True))

	def handleDeviceChange(self):
		self._stopBgScan()
		# A Bluetooth com port might have been added.
		self._btComs = None
		self._startBgScan(dict(usb=True, bluetooth=True))

	def terminate(self):
		self._devChangeListener.destroy()
		self._stopBgScan()

def getConnectedUsbDevicesForDriver(driver):
	"""Get any connected USB devices associated with a particular driver.
	@param driver: The name of the driver.
	@type driver: str
	@return: Device information for each device.
	@rtype: generator of L{UsbDeviceMatch}
	@raise LookupError: If there is no detection data for this driver.
	"""
	driverUsb = _driverDevices[driver][_KEY_USBDEVS]
	matching = driverUsb & set(hwPortUtils.listUsbDevices())
	for usbId in matching:
		yield UsbDeviceMatch(usbId)

def getPossibleBluetoothComPortsForDriver(driver):
	"""Get any possible Bluetooth com ports associated with a particular driver.
	@param driver: The name of the driver.
	@type driver: str
	@return: Port information for each port.
	@rtype: generator of L{BluetoothComPortMatch}
	@raise LookupError: If there is no detection data for this driver.
	"""
	matchFunc = _driverDevices[driver][_KEY_BTCOMS]
	for port in hwPortUtils.listComPorts():
		try:
			match = BluetoothComPortMatch(port["bluetoothAddress"], port["bluetoothName"], port["port"])
		except KeyError:
			continue
		if matchFunc(match):
			yield match

def arePossibleDevicesForDriver(driver):
	"""Determine whether there are any possible devices associated with a given driver.
	@param driver: The name of the driver.
	@type driver: str
	@return: C{True} if there are possible devices, C{False} otherwise.
	@rtype: bool
	@raise LookupError: If there is no detection data for this driver.
	"""
	try:
		next(itertools.chain(
			getConnectedUsbDevicesForDriver(driver),
			getPossibleBluetoothComPortsForDriver(driver)))
		return True
	except StopIteration:
		return False

### Detection data
# alvaBC6
addUsbDevices("alvaBC6", {
	"VID_0798&PID_0640", # BC640
	"VID_0798&PID_0680", # BC680
})
addBluetoothComPorts("alvaBC6", lambda m: m.name.startswith("ALVA "))
# baum
addUsbDevices("baum", {
	"VID_0403&PID_FE70", # Vario 40
	"VID_0403&PID_FE71", # PocketVario
	"VID_0403&PID_FE72", # SuperVario/Brailliant 40
	"VID_0403&PID_FE73", # SuperVario/Brailliant 32
	"VID_0403&PID_FE74", # SuperVario/Brailliant 64
	"VID_0403&PID_FE75", # SuperVario/Brailliant 80
	"VID_0403&PID_FE76", # VarioPro 80
	"VID_0403&PID_FE77", # VarioPro 64
	"VID_0904&PID_2000", # VarioPro 40
	"VID_0904&PID_2001", # EcoVario 24
	"VID_0904&PID_2002", # EcoVario 40
	"VID_0904&PID_2007", # VarioConnect/BrailleConnect 40
	"VID_0904&PID_2008", # VarioConnect/BrailleConnect 32
	"VID_0904&PID_2009", # VarioConnect/BrailleConnect 24
	"VID_0904&PID_2010", # VarioConnect/BrailleConnect 64
	"VID_0904&PID_2011", # VarioConnect/BrailleConnect 80
	"VID_0904&PID_2014", # EcoVario 32
	"VID_0904&PID_2015", # EcoVario 64
	"VID_0904&PID_2016", # EcoVario 80
	"VID_0904&PID_3000", # RefreshaBraille 18
})
addBluetoothComPorts("baum", lambda m: any(m.name.startswith(prefix) for prefix in (
	"Baum SuperVario",
	"Baum PocketVario",
	"Baum SVario",
	"HWG Brailliant",
	"Refreshabraille",
	"VarioConnect",
	"BrailleConnect",
)))
# brailliantB
addUsbDevices("brailliantB", {"VID_1C71&PID_C005"})
addBluetoothComPorts("brailliantB", lambda m:
	m.name.startswith("Brailliant B") or m.name == "Brailliant 80")
# freedomScientific
addUsbDevices("freedomScientific", {
	"VID_0F4E&PID_0100", # Focus 1
	"VID_0F4E&PID_0111", # PAC Mate
	"VID_0F4E&PID_0112", # Focus 2
	"VID_0F4E&PID_0114", # Focus Blue
})
addBluetoothComPorts("freedomScientific", lambda m: any(
	m.name == prefix or m.name.startswith(prefix + " ") for prefix in (
		"F14", "Focus 14 BT",
		"Focus 40 BT",
		"Focus 80 BT",
)))
