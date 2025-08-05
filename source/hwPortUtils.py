# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2001-2025 Chris Liechti, NV Access Limited, Babbage B.V., Leonard de Ruijter
# Based on serial scanner code by Chris Liechti from https://raw.githubusercontent.com/pyserial/pyserial/81167536e796cc2e13aa16abd17a14634dc3aed1/pyserial/examples/scanwin32.py

"""Utilities for working with hardware connection ports."""

import ctypes
import itertools
import math
import typing
import winreg
from ctypes.wintypes import DWORD, WCHAR

from comtypes import GUID

import config
import hidpi
from winBindings.bthprops import BLUETOOTH_DEVICE_INFO, BluetoothGetDeviceInfo
from winBindings.hid import (
	HIDD_ATTRIBUTES,
	HidD_FreePreparsedData,
	HidD_GetAttributes,
	HidD_GetHidGuid,
	HidD_GetManufacturerString,
	HidD_GetPreparsedData,
	HidD_GetProductString,
	HidP_GetCaps,
)
from winBindings.setupapi import (
	SetupDiDestroyDeviceInfoList,
	HDEVINFO,
	SetupDiGetClassDevs,
	SetupDiGetDeviceProperty,
	DEVPROPKEY,
	SP_DEVINFO_DATA,
	SetupDiEnumDeviceInterfaces,
	SP_DEVICE_INTERFACE_DATA,
	SetupDiGetDeviceInterfaceDetail,
	SetupDiGetDeviceRegistryProperty,
	SetupDiOpenDevRegKey,
)
from winBindings.advapi32 import RegCloseKey
import winKernel
from logHandler import log
from winAPI.constants import SystemErrorCodes

def ValidHandle(value):
	if value == 0:
		raise ctypes.WinError()
	return value

class dummy(ctypes.Structure):
	_fields_ = (("d1", DWORD), ("d2", WCHAR))
	# SetupAPI.h in the Windows headers includes pshpack8.h when 64 bit, pshpack1.h otherwise
	_pack_ = 8 if ctypes.sizeof(ctypes.c_void_p) == 8 else 1


SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W = ctypes.sizeof(dummy)

CR_SUCCESS = 0
MAX_DEVICE_ID_LEN = 200

GUID_CLASS_COMPORT = GUID("{86e0d1e0-8089-11d0-9ce4-08003e301f73}")
GUID_DEVINTERFACE_USB_DEVICE = GUID("{a5dcbf10-6530-11d2-901f-00c04fb951ed}")
DEVPKEY_Device_BusReportedDeviceDesc = DEVPROPKEY(GUID("{540b947e-8b40-45bc-a8a2-6a0b894cbda2}"), 4)
DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_DEVICEDESC = 0
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
SPDRP_LOCATION_INFORMATION = 13
ERROR_NO_MORE_ITEMS = 259
DICS_FLAG_GLOBAL = 0x00000001
DIREG_DEV = 0x00000001


def _isDebug():
	return config.conf["debugLog"]["hwIo"]


def _getBluetoothPortInfo(regKey: int, hwID: str) -> dict:
	info = {}
	try:
		port = info["port"] = winreg.QueryValueEx(regKey, "PortName")[0]
	except OSError:
		# #6015: In some rare cases, this value doesn't exist.
		log.debugWarning(f"No PortName value for hardware ID {hwID!r}")
		return info
	if not port:
		log.debugWarning(f"Empty PortName value for hardware ID {hwID!r}")
		return info
	match hwID:
		case h if h.startswith("BTHENUM\\"):
			# This is a Microsoft bluetooth port.
			try:
				addr = (
					winreg.QueryValueEx(
						regKey,
						"Bluetooth_UniqueID",
					)[0]
					.split("#", 1)[1]
					.split("_", 1)[0]
				)
				addr = int(addr, 16)
				info["bluetoothAddress"] = addr
				if addr:
					info["bluetoothName"] = getBluetoothDeviceInfo(addr).szName
			except Exception:
				log.debugWarning(
					f"Couldn't get Microsoft bt name for hardware id {hwID!r}",
					exc_info=True,
				)
		case r"Bluetooth\0004&0002":
			# This is a Toshiba bluetooth port.
			try:
				info["bluetoothAddress"], info["bluetoothName"] = getToshibaBluetoothPortInfo(port)
			except Exception:
				log.debugWarning(f"Couldn't get Toshiba bt name for hardware id {hwID!r}", exc_info=True)
		case r"{95C7A0A0-3094-11D7-A202-00508B9D7D5A}\BLUETOOTHPORT":
			try:
				info["bluetoothAddress"], info["bluetoothName"] = getWidcommBluetoothPortInfo(port)
			except Exception:
				log.debugWarning(f"Couldn't get Widcomm bt name for hardware id {hwID!r}", exc_info=True)
				pass
		case h if "USB" in h or "FTDIBUS" in h:
			usbIDStart = h.find("VID_")
			if usbIDStart != -1:
				info["usbID"] = hwID[usbIDStart : usbIDStart + 17]  # VID_xxxx&PID_xxxx
		case _:
			log.debug(f"Unknown hardware ID {hwID!r}")
	return info


def listComPorts(onlyAvailable: bool = True) -> typing.Iterator[dict]:
	"""List com ports on the system.
	:param onlyAvailable: Only return ports that are currently available.
	:return: Dicts including keys of port, friendlyName and hardwareID.
	"""
	for g_hdi, _idd, devinfo, buf in _listDevices(GUID_CLASS_COMPORT, onlyAvailable):
		entry = {}
		# hardware ID
		if not SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP_HARDWAREID,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# Ignore ERROR_INSUFFICIENT_BUFFER
			if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
				raise ctypes.WinError()
		else:
			hwID = entry["hardwareID"] = buf.value

		# Port info
		regKey = SetupDiOpenDevRegKey(
			g_hdi,
			ctypes.byref(devinfo),
			DICS_FLAG_GLOBAL,
			0,
			DIREG_DEV,
			winreg.KEY_READ,
		)
		try:
			portInfo = _getBluetoothPortInfo(regKey, hwID)
			if not portInfo:
				continue
			else:
				port = portInfo["port"]
				entry.update(portInfo)
		finally:
			RegCloseKey(regKey)

		# friendly name
		if not SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP_FRIENDLYNAME,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# #6007: SPDRP_FRIENDLYNAME sometimes doesn't exist/isn't valid.
			log.debugWarning(f"Couldn't get SPDRP_FRIENDLYNAME for {entry!r}: {ctypes.WinError()}")
			entry["friendlyName"] = port
		else:
			entry["friendlyName"] = buf.value

		if _isDebug():
			log.debug("%r" % entry)
		yield entry

	if _isDebug():
		log.debug("Finished listing com ports")


def getBluetoothDeviceInfo(address):
	devInfo = BLUETOOTH_DEVICE_INFO(address=address)
	res = BluetoothGetDeviceInfo(None, ctypes.byref(devInfo))
	if res != 0:
		raise ctypes.WinError(res)
	return devInfo


def getToshibaBluetoothPortInfo(port):
	with winreg.OpenKey(
		winreg.HKEY_CURRENT_USER,
		r"Software\Toshiba\BluetoothStack\V1.0\EZC\DATA",
	) as rootKey:
		for index in itertools.count():
			try:
				keyName = winreg.EnumKey(rootKey, index)
			except OSError:
				break
			with winreg.OpenKey(rootKey, keyName) as itemKey:
				with winreg.OpenKey(itemKey, "SCORIGINAL") as scorigKey:
					try:
						if winreg.QueryValueEx(scorigKey, "PORTNAME")[0].rstrip("\0") != port:
							# This isn't the port we're interested in.
							continue
					except OSError:
						# This isn't a COM port.
						continue
				addr = winreg.QueryValueEx(itemKey, "BDADDR")[0]
				# addr is a string of raw bytes.
				# Convert it to a single number.
				addr = sum(ord(byte) << (byteNum * 8) for byteNum, byte in enumerate(reversed(addr)))
				name = winreg.QueryValueEx(itemKey, "FRIENDLYNAME")[0].rstrip("\0")
				return addr, name
	raise LookupError


def getWidcommBluetoothPortInfo(port):
	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Widcomm\BTConfig\AutoConnect") as rootKey:
		for index in itertools.count():
			try:
				keyName = winreg.EnumKey(rootKey, index)
			except OSError:
				break
			# The keys are the port number, but might be prefixed by 0s.
			# For example, COM4 is 0004.
			if keyName.lstrip("0") != port[3:]:
				# This isn't the port we're interested in.
				continue
			with winreg.OpenKey(rootKey, keyName) as itemKey:
				addr = winreg.QueryValueEx(itemKey, "BDAddress")[0]
				# addr is a string of raw bytes.
				# Convert it to a single number.
				addr = sum(ord(byte) << (byteNum * 8) for byteNum, byte in enumerate(reversed(addr)))
				name = winreg.QueryValueEx(itemKey, "BDName")[0]
				return addr, name
	raise LookupError


def _listDevices(
	deviceClass: GUID,
	onlyAvailable: bool = True,
) -> typing.Iterator[tuple[HDEVINFO, ctypes.Structure, SP_DEVINFO_DATA, ctypes.c_wchar * 1024]]:
	"""Internal helper function to list devices on the system for a specific device class.
	@param deviceClass: The device class GUID.
	:param onlyAvailable: Only return devices that are currently available.
	"""
	flags = DIGCF_DEVICEINTERFACE
	if onlyAvailable:
		flags |= DIGCF_PRESENT

	buf = ctypes.create_unicode_buffer(1024)
	g_hdi = SetupDiGetClassDevs(ctypes.byref(deviceClass), None, None, flags)
	try:
		for dwIndex in range(256):
			did = SP_DEVICE_INTERFACE_DATA()
			did.cbSize = ctypes.sizeof(did)

			if not SetupDiEnumDeviceInterfaces(
				g_hdi,
				None,
				ctypes.byref(deviceClass),
				dwIndex,
				ctypes.byref(did),
			):
				if ctypes.GetLastError() != ERROR_NO_MORE_ITEMS:
					raise ctypes.WinError()
				break

			dwNeeded = DWORD()
			# get the size
			if not SetupDiGetDeviceInterfaceDetail(
				g_hdi,
				ctypes.byref(did),
				None,
				0,
				ctypes.byref(dwNeeded),
				None,
			):
				# Ignore ERROR_INSUFFICIENT_BUFFER
				if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
					raise ctypes.WinError()

			# allocate buffer
			class SP_DEVICE_INTERFACE_DETAIL_DATA_W(ctypes.Structure):
				_fields_ = (
					("cbSize", DWORD),
					(
						"DevicePath",
						# Round up to the next WCHAR count to ensure proper memory alignment
						WCHAR * math.ceil((dwNeeded.value - ctypes.sizeof(DWORD)) / ctypes.sizeof(WCHAR)),
					),
				)
				_pack_ = dummy._pack_

				def __str__(self):
					return f"DevicePath:{self.DevicePath!r}"

			idd = SP_DEVICE_INTERFACE_DETAIL_DATA_W()
			idd.cbSize = SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W
			devinfo = SP_DEVINFO_DATA()
			devinfo.cbSize = ctypes.sizeof(devinfo)
			if not SetupDiGetDeviceInterfaceDetail(
				g_hdi,
				ctypes.byref(did),
				ctypes.byref(idd),
				dwNeeded,
				None,
				ctypes.byref(devinfo),
			):
				raise ctypes.WinError()

			yield (g_hdi, idd, devinfo, buf)

	finally:
		SetupDiDestroyDeviceInfoList(g_hdi)


def listUsbDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
	"""List USB devices on the system.
	:param onlyAvailable: Only return devices that are currently available.
	:return: Generates dicts including keys of usbID (VID and PID), devicePath and hardwareID.
	"""
	for g_hdi, idd, devinfo, buf in _listDevices(GUID_DEVINTERFACE_USB_DEVICE, onlyAvailable):
		entry = {}
		# hardware ID
		if not SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP_HARDWAREID,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# Ignore ERROR_INSUFFICIENT_BUFFER
			if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
				raise ctypes.WinError()
		else:
			# The string is of the form "usb\VID_xxxx&PID_xxxx&..."
			usbId = buf.value[4:21]  # VID_xxxx&PID_xxxx
			entry.update(
				{
					"hardwareID": buf.value,
					"usbID": usbId,
					"devicePath": idd.DevicePath,
				},
			)
			if _isDebug():
				log.debug(f"USB Id: {usbId!r}")

		# Bus reported device description
		propRegDataType = DWORD()
		if not SetupDiGetDeviceProperty(
			g_hdi,
			ctypes.byref(devinfo),
			ctypes.byref(DEVPKEY_Device_BusReportedDeviceDesc),
			ctypes.byref(propRegDataType),
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
			0,
		):
			log.debugWarning(
				f"Couldn't get DEVPKEY_Device_BusReportedDeviceDesc for {entry!r}: {ctypes.WinError()}",
			)
		else:
			entry["busReportedDeviceDescription"] = buf.value

		yield entry
	if _isDebug():
		log.debug("Finished listing USB devices")


_getHidInfoCache: dict[str, dict] = {}


def _getHidInfo(hwId: str, path: str) -> dict[str, typing.Any]:
	info = {
		"hardwareID": hwId,
		"devicePath": path,
	}
	hwId = hwId.split("\\", 1)[1]
	if hwId.startswith("VID"):
		info["provider"] = "usb"
		info["usbID"] = hwId[:17]  # VID_xxxx&PID_xxxx
	elif hwId.startswith("{00001124-0000-1000-8000-00805f9b34fb}"):
		info["provider"] = "bluetooth"
	elif hwId.startswith("{00001812-0000-1000-8000-00805f9b34fb}"):
		# Low energy bluetooth: #15470
		info["provider"] = "bluetooth"
	else:
		# Unknown provider.
		info["provider"] = None
		return info
	# Fetch additional info about the HID device.
	from serial.win32 import FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE, CreateFile

	if (
		handle := CreateFile(
			path,
			0,
			winKernel.FILE_SHARE_READ | winKernel.FILE_SHARE_WRITE,
			None,
			winKernel.OPEN_EXISTING,
			FILE_FLAG_OVERLAPPED,
			None,
		)
	) == INVALID_HANDLE_VALUE:
		if (err := ctypes.GetLastError()) == SystemErrorCodes.SHARING_VIOLATION:
			if _isDebug():
				log.debugWarning(
					f"Opening device {path} to get additional info failed because the device is being used. "
					"Falling back to cache for device info",
				)
			if cachedInfo := _getHidInfoCache.get(path):
				cachedInfo.update(info)
				return cachedInfo
		elif _isDebug():
			log.debugWarning(f"Opening device {path} to get additional info failed: {ctypes.WinError(err)}")
		return info
	try:
		attribs = HIDD_ATTRIBUTES()
		if HidD_GetAttributes(handle, ctypes.byref(attribs)):
			info["vendorID"] = attribs.VendorID
			info["productID"] = attribs.ProductID
			info["versionNumber"] = attribs.VersionNumber
		else:
			if _isDebug():
				log.debugWarning("HidD_GetAttributes failed")
		buf = ctypes.create_unicode_buffer(128)
		nrOfBytes = ctypes.sizeof(buf)
		if HidD_GetManufacturerString(handle, buf, nrOfBytes):
			info["manufacturer"] = buf.value
		if HidD_GetProductString(handle, buf, nrOfBytes):
			info["product"] = buf.value
		pd = ctypes.c_void_p()
		if HidD_GetPreparsedData(handle, ctypes.byref(pd)):
			try:
				caps = hidpi.HIDP_CAPS()
				HidP_GetCaps(pd, ctypes.byref(caps))
				info["HIDUsagePage"] = caps.UsagePage
			finally:
				HidD_FreePreparsedData(pd)
	finally:
		winKernel.closeHandle(handle)
	_getHidInfoCache[path] = info
	return info


_hidGuid = None


def listHidDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
	"""List HID devices on the system.
	@param onlyAvailable: Only return devices that are currently available.
	@return: Generates dicts including keys such as hardwareID,
		usbID (in the form "VID_xxxx&PID_xxxx")
		and devicePath.
	"""
	global _hidGuid
	if not _hidGuid:
		_hidGuid = GUID()
		HidD_GetHidGuid(ctypes.byref(_hidGuid))

	for g_hdi, idd, devinfo, buf in _listDevices(_hidGuid, onlyAvailable):
		# hardware ID
		if not SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP_HARDWAREID,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# Ignore ERROR_INSUFFICIENT_BUFFER
			if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
				raise ctypes.WinError()
		else:
			hwId = buf.value
			info = _getHidInfo(hwId, idd.DevicePath)
			if _isDebug():
				log.debug(f"{info!r}")
			yield info

	if _isDebug():
		log.debug("Finished listing HID devices")
