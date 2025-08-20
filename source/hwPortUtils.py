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

import config
import hidpi
import winKernel
from comtypes import GUID
from logHandler import log
from winAPI.constants import SystemErrorCodes
from winBindings.advapi32 import RegCloseKey as _RegCloseKey
from winBindings.bthprops import (
	BLUETOOTH_DEVICE_INFO as _BLUETOOTH_DEVICE_INFO,
	BluetoothGetDeviceInfo as _BluetoothGetDeviceInfo,
)
from winBindings.hid import (
	HIDD_ATTRIBUTES as _HIDD_ATTRIBUTES,
	HidD_FreePreparsedData as _HidD_FreePreparsedData,
	HidD_GetAttributes as _HidD_GetAttributes,
	HidD_GetHidGuid as _HidD_GetHidGuid,
	HidD_GetManufacturerString as _HidD_GetManufacturerString,
	HidD_GetPreparsedData as _HidD_GetPreparsedData,
	HidD_GetProductString as _HidD_GetProductString,
	HidP_GetCaps as _HidP_GetCaps,
)
from winBindings.setupapi import (
	DICS_FLAG,
	DIGCF,
	DIREG,
	GUID_CLASS_COMPORT as _GUID_CLASS_COMPORT,
	GUID_DEVINTERFACE_USB_DEVICE as _GUID_DEVINTERFACE_USB_DEVICE,
	HDEVINFO as _HDEVINFO,
	SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W as _SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W,
	SP_DEVICE_INTERFACE_DATA as _SP_DEVICE_INTERFACE_DATA,
	SP_DEVINFO_DATA as _SP_DEVINFO_DATA,
	SPDRP,
	DEVPKEY_Device_BusReportedDeviceDesc as _DEVPKEY_Device_BusReportedDeviceDesc,
	SetupDiDestroyDeviceInfoList as _SetupDiDestroyDeviceInfoList,
	SetupDiEnumDeviceInterfaces as _SetupDiEnumDeviceInterfaces,
	SetupDiGetClassDevs as _SetupDiGetClassDevs,
	SetupDiGetDeviceInterfaceDetail as _SetupDiGetDeviceInterfaceDetail,
	SetupDiGetDeviceProperty as _SetupDiGetDeviceProperty,
	SetupDiGetDeviceRegistryProperty as _SetupDiGetDeviceRegistryProperty,
	SetupDiOpenDevRegKey as _SetupDiOpenDevRegKey,
	_Dummy,
)


def ValidHandle(value):
	if value == 0:
		raise ctypes.WinError()
	return value


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
	for g_hdi, _idd, devinfo, buf in _listDevices(_GUID_CLASS_COMPORT, onlyAvailable):
		entry = {}
		# hardware ID
		if not _SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP.HARDWAREID,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# Ignore ERROR_INSUFFICIENT_BUFFER
			if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
				raise ctypes.WinError()
		else:
			hwID = entry["hardwareID"] = buf.value

		# Port info
		regKey = _SetupDiOpenDevRegKey(
			g_hdi,
			ctypes.byref(devinfo),
			DICS_FLAG.GLOBAL,
			0,
			DIREG.DEV,
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
			_RegCloseKey(regKey)

		# friendly name
		if not _SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP.FRIENDLYNAME,
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
	devInfo = _BLUETOOTH_DEVICE_INFO(address=address)
	res = _BluetoothGetDeviceInfo(None, ctypes.byref(devInfo))
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
) -> typing.Iterator[tuple[_HDEVINFO, ctypes.Structure, _SP_DEVINFO_DATA, ctypes.c_wchar * 1024]]:
	"""Internal helper function to list devices on the system for a specific device class.
	@param deviceClass: The device class GUID.
	:param onlyAvailable: Only return devices that are currently available.
	"""
	flags = DIGCF.DEVICEINTERFACE
	if onlyAvailable:
		flags |= DIGCF.PRESENT

	buf = ctypes.create_unicode_buffer(1024)
	g_hdi = _SetupDiGetClassDevs(ctypes.byref(deviceClass), None, None, flags)
	try:
		for dwIndex in range(256):
			did = _SP_DEVICE_INTERFACE_DATA()
			did.cbSize = ctypes.sizeof(did)

			if not _SetupDiEnumDeviceInterfaces(
				g_hdi,
				None,
				ctypes.byref(deviceClass),
				dwIndex,
				ctypes.byref(did),
			):
				if ctypes.GetLastError() != SystemErrorCodes.NO_MORE_ITEMS:
					raise ctypes.WinError()
				break

			dwNeeded = DWORD()
			# get the size
			if not _SetupDiGetDeviceInterfaceDetail(
				g_hdi,
				ctypes.byref(did),
				None,
				0,
				ctypes.byref(dwNeeded),
				None,
			):
				# Ignore ERROR_INSUFFICIENT_BUFFER
				if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
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
				_pack_ = _Dummy._pack_

				def __str__(self):
					return f"DevicePath:{self.DevicePath!r}"

			idd = SP_DEVICE_INTERFACE_DETAIL_DATA_W()
			idd.cbSize = _SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W
			devinfo = _SP_DEVINFO_DATA()
			devinfo.cbSize = ctypes.sizeof(devinfo)
			if not _SetupDiGetDeviceInterfaceDetail(
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
		_SetupDiDestroyDeviceInfoList(g_hdi)


def listUsbDevices(onlyAvailable: bool = True) -> typing.Iterator[dict]:
	"""List USB devices on the system.
	:param onlyAvailable: Only return devices that are currently available.
	:return: Generates dicts including keys of usbID (VID and PID), devicePath and hardwareID.
	"""
	for g_hdi, idd, devinfo, buf in _listDevices(_GUID_DEVINTERFACE_USB_DEVICE, onlyAvailable):
		entry = {}
		# hardware ID
		if not _SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP.HARDWAREID,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# Ignore ERROR_INSUFFICIENT_BUFFER
			if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
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
		if not _SetupDiGetDeviceProperty(
			g_hdi,
			ctypes.byref(devinfo),
			ctypes.byref(_DEVPKEY_Device_BusReportedDeviceDesc),
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
		attribs = _HIDD_ATTRIBUTES()
		if _HidD_GetAttributes(handle, ctypes.byref(attribs)):
			info["vendorID"] = attribs.VendorID
			info["productID"] = attribs.ProductID
			info["versionNumber"] = attribs.VersionNumber
		else:
			if _isDebug():
				log.debugWarning("HidD_GetAttributes failed")
		buf = ctypes.create_unicode_buffer(128)
		nrOfBytes = ctypes.sizeof(buf)
		if _HidD_GetManufacturerString(handle, buf, nrOfBytes):
			info["manufacturer"] = buf.value
		if _HidD_GetProductString(handle, buf, nrOfBytes):
			info["product"] = buf.value
		pd = ctypes.c_void_p()
		if _HidD_GetPreparsedData(handle, ctypes.byref(pd)):
			try:
				caps = hidpi.HIDP_CAPS()
				_HidP_GetCaps(pd, ctypes.byref(caps))
				info["HIDUsagePage"] = caps.UsagePage
			finally:
				_HidD_FreePreparsedData(pd)
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
		_HidD_GetHidGuid(ctypes.byref(_hidGuid))

	for g_hdi, idd, devinfo, buf in _listDevices(_hidGuid, onlyAvailable):
		# hardware ID
		if not _SetupDiGetDeviceRegistryProperty(
			g_hdi,
			ctypes.byref(devinfo),
			SPDRP.HARDWAREID,
			None,
			ctypes.byref(buf),
			ctypes.sizeof(buf) - 1,
			None,
		):
			# Ignore ERROR_INSUFFICIENT_BUFFER
			if ctypes.GetLastError() != SystemErrorCodes.INSUFFICIENT_BUFFER:
				raise ctypes.WinError()
		else:
			hwId = buf.value
			info = _getHidInfo(hwId, idd.DevicePath)
			if _isDebug():
				log.debug(f"{info!r}")
			yield info

	if _isDebug():
		log.debug("Finished listing HID devices")


_MOVED_SYMBOLS: dict[str, tuple[str, ...]] = {
	"RegCloseKey": ("winBindings.advapi32",),
	"BLUETOOTH_ADDRESS": ("winBindings.bthprops",),
	"BLUETOOTH_MAX_NAME_SIZE": ("winBindings.bthprops",),
	"BTH_ADDR": ("winBindings.bthprops", "BLUETOOTH_ADDRESS"),
	"BLUETOOTH_DEVICE_INFO": ("winBindings.bthprops",),
	"BluetoothGetDeviceInfo": ("winBindings.bthprops",),
	"CM_Get_Device_ID": ("winBindings.cfgmgr32",),
	"CR_SUCCESS": ("winBindings.cfgmgr32",),
	"MAX_DEVICE_ID_LEN": ("winBindings.cfgmgr32",),
	"HIDD_ATTRIBUTES": ("winBindings.hid",),
	"HidD_FreePreparsedData": ("winBindings.hid",),
	"HidD_GetAttributes": ("winBindings.hid",),
	"HidD_GetHidGuid": ("winBindings.hid",),
	"HidD_GetManufacturerString": ("winBindings.hid",),
	"HidD_GetPreparsedData": ("winBindings.hid",),
	"HidD_GetProductString": ("winBindings.hid",),
	"HidP_GetCaps": ("winBindings.hid",),
	"DEVPROPKEY": ("winBindings.setupapi",),
	"dummy": ("winBindings.setupapi", "_Dummy"),
	"PSP_DEVICE_INTERFACE_DATA": ("winBindings.setupapi",),
	"PSP_DEVICE_INTERFACE_DETAIL_DATA": ("winBindings.setupapi",),
	"PSP_DEVINFO_DATA": ("winBindings.setupapi",),
	"SetupDiEnumDeviceInfo": ("winBindings.setupapi",),
	"DIGCF_PRESENT": ("winBindings.setupapi", "DIGCF", "PRESENT"),
	"DIGCF_DEVICEINTERFACE": ("winBindings.setupapi", "DIGCF", "DEVICEINTERFACE"),
	"SPDRP_DEVICEDESC": ("winBindings.setupapi", "SPDRP", "DEVICEDESC"),
	"SPDRP_HARDWAREID": ("winBindings.setupapi", "SPDRP", "HARDWAREID"),
	"SPDRP_FRIENDLYNAME": ("winBindings.setupapi", "SPDRP", "FRIENDLYNAME"),
	"SPDRP_LOCATION_INFORMATION": ("winBindings.setupapi", "SPDRP", "LOCATION_INFORMATION"),
	"DICS_FLAG_GLOBAL": ("winBindings.setupapi", "DICS_FLAG", "GLOBAL"),
	"DIREG_DEV": ("winBindings.setupapi", "DIREG", "DEV"),
	"GUID_CLASS_COMPORT": ("winBindings.setupapi",),
	"GUID_DEVINTERFACE_USB_DEVICE": ("winBindings.setupapi",),
	"HDEVINFO": ("winBindings.setupapi",),
	"SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W": ("winBindings.setupapi",),
	"SP_DEVICE_INTERFACE_DATA": ("winBindings.setupapi",),
	"SP_DEVINFO_DATA": ("winBindings.setupapi",),
	"DEVPKEY_Device_BusReportedDeviceDesc": ("winBindings.setupapi",),
	"SetupDiDestroyDeviceInfoList": ("winBindings.setupapi",),
	"SetupDiEnumDeviceInterfaces": ("winBindings.setupapi",),
	"SetupDiGetClassDevs": ("winBindings.setupapi",),
	"SetupDiGetDeviceInterfaceDetail": ("winBindings.setupapi",),
	"SetupDiGetDeviceProperty": ("winBindings.setupapi",),
	"SetupDiGetDeviceRegistryProperty": ("winBindings.setupapi",),
	"SetupDiOpenDevRegKey": ("winBindings.setupapi",),
	"ERROR_NO_MORE_ITEMS": ("winAPI.constants", "SystemErrorCodes", "NO_MORE_ITEMS"),
	"ERROR_INSUFFICIENT_BUFFER": ("winAPI.constants", "SystemErrorCodes", "INSUFFICIENT_BUFFER"),
}
"""Mapping from symbol name to new (absolute) module and symbol path."""


def __getattr__(attrName: str) -> typing.Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	import NVDAState

	if NVDAState._allowDeprecatedAPI():
		# Symbols that have simply been moved elsewhere
		if attrName in _MOVED_SYMBOLS:
			from importlib import import_module

			newModule, *newPath = _MOVED_SYMBOLS[attrName]
			newPath = newPath or [attrName]
			log.warning(
				f"hwPortUtils.{attrName} is deprecated. Use {newModule}.{'.'.join(newPath)} instead.",
				stack_info=True,
			)
			value = import_module(newModule)
			for segment in newPath:
				value = getattr(value, segment)
			return value

		# Other symbols
		match attrName:
			case "INVALID_HANDLE_VALUE":
				log.warning(f"hwPortUtils.{attrName} is deprecated.", stack_info=True)
				return 0
			case _:
				pass
	raise AttributeError(f"module {__name__!r} has no attribute {attrName!r}")
