#bdDetect.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

"""Support for braille display detection.
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
	usbDevs = set(hwPortUtils.listUsbDevices())
	for driver, devs in _driverDevices.iteritems():
		driverUsb = devs[_KEY_USBDEVS]
		matching = driverUsb & usbDevs
		for usbId in matching:
			yield driver, UsbDeviceMatch(usbId)

def getDriversForPossibleBluetoothComPorts():
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
class DeviceChangeListener(windowUtils.CustomWindow):
	className = u"NVDADeviceChangeListener"

	def __init__(self, detector):
		super(DeviceChangeListener, self).__init__()
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

	def __init__(self):
		self._btComs = None
		self._callLater = None
		self._thread = None
		self._devChangeListener = DeviceChangeListener(self)
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
	driverUsb = _driverDevices[driver][_KEY_USBDEVS]
	matching = driverUsb & set(hwPortUtils.listUsbDevices())
	for usbId in matching:
		yield UsbDeviceMatch(usbId)

def getPossibleBluetoothComPortsForDriver(driver):
	matchFunc = _driverDevices[driver][_KEY_BTCOMS]
	for port in hwPortUtils.listComPorts():
		try:
			match = BluetoothComPortMatch(port["bluetoothAddress"], port["bluetoothName"], port["port"])
		except KeyError:
			continue
		if matchFunc(match):
			yield match

### Detection data
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
