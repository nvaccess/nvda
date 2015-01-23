#hwPortUtils.py
#A part of NonVisual Desktop Access (NVDA)
# Original serial scanner code from http://pyserial.svn.sourceforge.net/viewvc/*checkout*/pyserial/trunk/pyserial/examples/scanwin32.py
# Modifications and enhancements by James Teh

"""Utilities for working with hardware connection ports.
"""

import itertools
import ctypes
from ctypes.wintypes import BOOL, WCHAR, HWND, DWORD, ULONG, WORD
import _winreg as winreg
from winKernel import SYSTEMTIME

def ValidHandle(value):
	if value == 0:
		raise ctypes.WinError()
	return value

HDEVINFO = ctypes.c_void_p
PCWSTR = ctypes.c_wchar_p
HWND = ctypes.c_uint
PDWORD = ctypes.POINTER(DWORD)
ULONG_PTR = ctypes.POINTER(ULONG)
ULONGLONG = ctypes.c_ulonglong
NULL = 0

class GUID(ctypes.Structure):
	_fields_ = (
		('Data1', ctypes.c_ulong),
		('Data2', ctypes.c_ushort),
		('Data3', ctypes.c_ushort),
		('Data4', ctypes.c_ubyte*8),
	)
	def __str__(self):
		return "{%08x-%04x-%04x-%s-%s}" % (
			self.Data1,
			self.Data2,
			self.Data3,
			''.join(["%02x" % d for d in self.Data4[:2]]),
			''.join(["%02x" % d for d in self.Data4[2:]]),
		)

class SP_DEVINFO_DATA(ctypes.Structure):
	_fields_ = (
		('cbSize', DWORD),
		('ClassGuid', GUID),
		('DevInst', DWORD),
		('Reserved', ULONG_PTR),
	)
	def __str__(self):
		return "ClassGuid:%s DevInst:%s" % (self.ClassGuid, self.DevInst)
PSP_DEVINFO_DATA = ctypes.POINTER(SP_DEVINFO_DATA)

class SP_DEVICE_INTERFACE_DATA(ctypes.Structure):
	_fields_ = (
		('cbSize', DWORD),
		('InterfaceClassGuid', GUID),
		('Flags', DWORD),
		('Reserved', ULONG_PTR),
	)
	def __str__(self):
		return "InterfaceClassGuid:%s Flags:%s" % (self.InterfaceClassGuid, self.Flags)

PSP_DEVICE_INTERFACE_DATA = ctypes.POINTER(SP_DEVICE_INTERFACE_DATA)

PSP_DEVICE_INTERFACE_DETAIL_DATA = ctypes.c_void_p

class dummy(ctypes.Structure):
	_fields_=(("d1", DWORD), ("d2", WCHAR))
	_pack_ = 1
SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W = ctypes.sizeof(dummy)

SetupDiDestroyDeviceInfoList = ctypes.windll.setupapi.SetupDiDestroyDeviceInfoList
SetupDiDestroyDeviceInfoList.argtypes = (HDEVINFO,)
SetupDiDestroyDeviceInfoList.restype = BOOL

SetupDiGetClassDevs = ctypes.windll.setupapi.SetupDiGetClassDevsW
SetupDiGetClassDevs.argtypes = (ctypes.POINTER(GUID), PCWSTR, HWND, DWORD)
SetupDiGetClassDevs.restype = ValidHandle # HDEVINFO

SetupDiEnumDeviceInterfaces = ctypes.windll.setupapi.SetupDiEnumDeviceInterfaces
SetupDiEnumDeviceInterfaces.argtypes = (HDEVINFO, PSP_DEVINFO_DATA, ctypes.POINTER(GUID), DWORD, PSP_DEVICE_INTERFACE_DATA)
SetupDiEnumDeviceInterfaces.restype = BOOL

SetupDiGetDeviceInterfaceDetail = ctypes.windll.setupapi.SetupDiGetDeviceInterfaceDetailW
SetupDiGetDeviceInterfaceDetail.argtypes = (HDEVINFO, PSP_DEVICE_INTERFACE_DATA, PSP_DEVICE_INTERFACE_DETAIL_DATA, DWORD, PDWORD, PSP_DEVINFO_DATA)
SetupDiGetDeviceInterfaceDetail.restype = BOOL

SetupDiGetDeviceRegistryProperty = ctypes.windll.setupapi.SetupDiGetDeviceRegistryPropertyW
SetupDiGetDeviceRegistryProperty.argtypes = (HDEVINFO, PSP_DEVINFO_DATA, DWORD, PDWORD, ctypes.c_void_p, DWORD, PDWORD)
SetupDiGetDeviceRegistryProperty.restype = BOOL

GUID_CLASS_COMPORT = GUID(0x86e0d1e0L, 0x8089, 0x11d0,
	(ctypes.c_ubyte*8)(0x9c, 0xe4, 0x08, 0x00, 0x3e, 0x30, 0x1f, 0x73))

DIGCF_PRESENT = 2
DIGCF_DEVICEINTERFACE = 16
INVALID_HANDLE_VALUE = 0
ERROR_INSUFFICIENT_BUFFER = 122
SPDRP_HARDWAREID = 1
SPDRP_FRIENDLYNAME = 12
SPDRP_LOCATION_INFORMATION = 13
ERROR_NO_MORE_ITEMS = 259
DICS_FLAG_GLOBAL = 0x00000001
DIREG_DEV = 0x00000001

def listComPorts(onlyAvailable=True):
	"""List com ports on the system.
	@param onlyAvailable: Only return ports that are currently available.
	@type onlyAvailable: bool
	@return: Generates dicts including keys of port, friendlyName and hardwareID.
	@rtype: generator of (str, str, str)
	"""
	flags = DIGCF_DEVICEINTERFACE
	if onlyAvailable:
		flags |= DIGCF_PRESENT

	buf = ctypes.create_unicode_buffer(1024)
	g_hdi = SetupDiGetClassDevs(ctypes.byref(GUID_CLASS_COMPORT), None, NULL, flags)
	try:
		for dwIndex in xrange(256):
			entry = {}
			did = SP_DEVICE_INTERFACE_DATA()
			did.cbSize = ctypes.sizeof(did)

			if not SetupDiEnumDeviceInterfaces(
				g_hdi,
				None,
				ctypes.byref(GUID_CLASS_COMPORT),
				dwIndex,
				ctypes.byref(did)
			):
				if ctypes.GetLastError() != ERROR_NO_MORE_ITEMS:
					raise ctypes.WinError()
				break

			dwNeeded = DWORD()
			# get the size
			if not SetupDiGetDeviceInterfaceDetail(
				g_hdi,
				ctypes.byref(did),
				None, 0, ctypes.byref(dwNeeded),
				None
			):
				# Ignore ERROR_INSUFFICIENT_BUFFER
				if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
					raise ctypes.WinError()
			# allocate buffer
			class SP_DEVICE_INTERFACE_DETAIL_DATA_W(ctypes.Structure):
				_fields_ = (
					('cbSize', DWORD),
					('DevicePath', WCHAR*(dwNeeded.value - ctypes.sizeof(DWORD))),
				)
				def __str__(self):
					return "DevicePath:%s" % (self.DevicePath,)
			idd = SP_DEVICE_INTERFACE_DETAIL_DATA_W()
			idd.cbSize = SIZEOF_SP_DEVICE_INTERFACE_DETAIL_DATA_W
			devinfo = SP_DEVINFO_DATA()
			devinfo.cbSize = ctypes.sizeof(devinfo)
			if not SetupDiGetDeviceInterfaceDetail(
				g_hdi,
				ctypes.byref(did),
				ctypes.byref(idd), dwNeeded, None,
				ctypes.byref(devinfo)
			):
				raise ctypes.WinError()

			# hardware ID
			if not SetupDiGetDeviceRegistryProperty(
				g_hdi,
				ctypes.byref(devinfo),
				SPDRP_HARDWAREID,
				None,
				ctypes.byref(buf), ctypes.sizeof(buf) - 1,
				None
			):
				# Ignore ERROR_INSUFFICIENT_BUFFER
				if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
					raise ctypes.WinError()
			else:
				hwID = entry["hardwareID"] = buf.value

			regKey = ctypes.windll.setupapi.SetupDiOpenDevRegKey(g_hdi, ctypes.byref(devinfo), DICS_FLAG_GLOBAL, 0, DIREG_DEV, winreg.KEY_READ)
			port = entry["port"] = winreg.QueryValueEx(regKey, "PortName")[0]
			if hwID.startswith("BTHENUM\\"):
				# This is a Microsoft bluetooth port.
				try:
					addr = winreg.QueryValueEx(regKey, "Bluetooth_UniqueID")[0].split("#", 1)[1].split("_", 1)[0]
					addr = int(addr, 16)
					entry["bluetoothAddress"] = addr
					if addr:
						entry["bluetoothName"] = getBluetoothDeviceInfo(addr).szName
				except:
					pass
			elif hwID == r"Bluetooth\0004&0002":
				# This is a Toshiba bluetooth port.
				try:
					entry["bluetoothAddress"], entry["bluetoothName"] = getToshibaBluetoothPortInfo(port)
				except:
					pass
			elif hwID == r"{95C7A0A0-3094-11D7-A202-00508B9D7D5A}\BLUETOOTHPORT":
				try:
					entry["bluetoothAddress"], entry["bluetoothName"] = getWidcommBluetoothPortInfo(port)
				except:
					pass
			ctypes.windll.advapi32.RegCloseKey(regKey)

			# friendly name
			if not SetupDiGetDeviceRegistryProperty(
				g_hdi,
				ctypes.byref(devinfo),
				SPDRP_FRIENDLYNAME,
				None,
				ctypes.byref(buf), ctypes.sizeof(buf) - 1,
				None
			):
				# Ignore ERROR_INSUFFICIENT_BUFFER
				if ctypes.GetLastError() != ERROR_INSUFFICIENT_BUFFER:
					raise ctypes.WinError()
			else:
				entry["friendlyName"] = buf.value

			yield entry

	finally:
		SetupDiDestroyDeviceInfoList(g_hdi)

BLUETOOTH_MAX_NAME_SIZE = 248
BTH_ADDR = BLUETOOTH_ADDRESS = ULONGLONG

class BLUETOOTH_DEVICE_INFO(ctypes.Structure):
	_fields_ = (
		("dwSize", DWORD),
		("address", BLUETOOTH_ADDRESS),
		("ulClassofDevice", ULONG),
		("fConnected", BOOL),
		("fRemembered", BOOL),
		("fAuthenticated", BOOL),
		("stLastSeen", SYSTEMTIME),
		("stLastUsed", SYSTEMTIME),
		("szName", WCHAR * BLUETOOTH_MAX_NAME_SIZE)
	)
	def __init__(self, **kwargs):
		super(BLUETOOTH_DEVICE_INFO, self).__init__(dwSize=ctypes.sizeof(self), **kwargs)

def getBluetoothDeviceInfo(address):
	devInfo = BLUETOOTH_DEVICE_INFO(address=address)
	res = ctypes.windll["bthprops.cpl"].BluetoothGetDeviceInfo(None, ctypes.byref(devInfo))
	if res != 0:
		raise ctypes.WinError(res)
	return devInfo

def getToshibaBluetoothPortInfo(port):
	with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Toshiba\BluetoothStack\V1.0\EZC\DATA") as rootKey:
		for index in itertools.count():
			try:
				keyName = winreg.EnumKey(rootKey, index)
			except WindowsError:
				break
			with winreg.OpenKey(rootKey, keyName) as itemKey:
				with winreg.OpenKey(itemKey, "SCORIGINAL") as scorigKey:
					try:
						if winreg.QueryValueEx(scorigKey, "PORTNAME")[0].rstrip("\0") != port:
							# This isn't the port we're interested in.
							continue
					except WindowsError:
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
			except WindowsError:
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
