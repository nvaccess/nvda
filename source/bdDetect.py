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
import wx
import hwPortUtils
import braille

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

BluetoothComPortMatch = namedtuple("BluetoothComPortMatch", ("address", "name", "port"))
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
		if driverUsb & usbDevs:
			yield driver, ("usbDevice", usbId)

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

class Detector(object):

	def __init__(self):
		self._btComs = None
		self._callLater = None
		# Perform initial scan.
		self._startBgScan(dict(usb=True, bluetooth=True))

	def _startBgScan(self, kwargs):
		self._stopEvent = kwargs["stopEvent"] = threading.Event()
		self._thread = threading.Thread(target=self._bgScan, kwargs=kwargs)
		self._thread.start()

	def _stopBgScan(self):
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
				self._callLater = wx.CallLater(POLL_INTERVAL, self._startBgScan, dict(bluetooth=True))

	def terminate(self):
		if self._callLater:
			self._callLater.Stop()
			self._callLater = None
		self._stopBgScan()
