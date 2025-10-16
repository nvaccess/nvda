#!/usr/bin/env python
"""This module is the first implementation of FTD2xx driver for the
FTDI USB chips. Initial implementation is for functions from the
dll required for present project"""
# (from: http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip)

from ctypes import c_ubyte, POINTER, c_char_p, c_void_p, WINFUNCTYPE, c_int
from ctypes.wintypes import DWORD, LPDWORD, PHANDLE
import sys
import ctypes as c
from typing import Any
from _ctypes import CFuncPtr

__FT_VERSION__ = "1.1"
__FT_LICENCE__ = "LGPL3"
__FT_AUTHOR__ = "Jonathan Roadley-Battin"


MAX_DESCRIPTION_SIZE = 256


UCHAR = c_ubyte
PUCHAR = POINTER(UCHAR)
PCHAR = c_char_p
FT_HANDLE = PHANDLE
FT_STATUS = FT_DEVICE = DWORD
PVOID = LPVOID = c_void_p

FT_OK = 0
FT_LIST_NUMBER_ONLY = 0x80000000
FT_LIST_BY_INDEX = 0x40000000
FT_LIST_ALL = 0x20000000
FT_OPEN_BY_SERIAL_NUMBER = 1
FT_PURGE_RX = 1
FT_PURGE_TX = 2


class FtdiBitModes:  # added by CJBH
	RESET = 0x0
	ASYNC_BITBANG = 0x1
	MPSSE = 0x2
	SYNC_BITBANG = 0x4
	MCU_HOST = 0x8
	FAST_SERIAL = 0x10


ft_messages = [
	"OK",
	"INVALID_HANDLE",
	"DEVICE_NOT_FOUND",
	"DEVICE_NOT_OPENED",
	"IO_ERROR",
	"INSUFFICIENT_RESOURCES",
	"INVALID_PARAMETER",
	"INVALID_BAUD_RATE",
	"DEVICE_NOT_OPENED_FOR_ERASE",
	"DEVICE_NOT_OPENED_FOR_WRITE",
	"FAILED_TO_WRITE_DEVICE0",
	"EEPROM_READ_FAILED",
	"EEPROM_WRITE_FAILED",
	"EEPROM_ERASE_FAILED",
	"EEPROM_NOT_PRESENT",
	"EEPROM_NOT_PROGRAMMED",
	"INVALID_ARGS",
	"NOT_SUPPORTED",
	"OTHER_ERROR",
]


if sys.platform == "win32":
	ft = c.windll.ftd2xx
else:
	ft = c.CDLL("libftd2xx.so")


######################################
##      FTDI exception classes      ##
######################################
class FTDeviceError(Exception):
	"""Exception class for FTDI function returns"""

	def __init__(self, msgnum):
		self.parameter = ft_messages[msgnum]
		self.status = msgnum

	def __str__(self):
		return repr(self.parameter)


#####################################
# CTYPES structure for DeviceInfo   #
#####################################
class FT_DEVICE_LIST_INFO_NODE(c.Structure):
	_fields_ = (
		("Flags", DWORD),  # c.c_ulong
		("Type", DWORD),  # c.c_ulong
		("ID", DWORD),  # c.c_ulong
		# ("LocID", c.c_ulong),
		("LocId", DWORD),
		("SerialNumber", c.c_char * 16),
		("Description", c.c_char * 64),
		# ("none", c.c_void_p),
		("ftHandle", FT_HANDLE),
	)


####################################################
# Shared Lib functions via python function decorator
# for i in $(strings /usr/lib/libftd2xx.so.0.4.16 | grep FT_);do echo -e "@ftExceptionDecorator\ndef _${i/FT/PY}(*args):\n    return ft.$i(*args)\n";done
# Allows common exception routine to be performed on each fn
# Via Bash-liner additional fn can easily be added and specific pythonic fn added when needed
####################################################
# def ftExceptionDecorator(f):
# def fn_wrap(*args):
# status = f(*args)
# if status is None:
# status = 18
# if status != FT_OK:
# raise FTDeviceError(status)
#
# return fn_wrap


def _ftd2xxErrorCheck(result: int, func: CFuncPtr, args: tuple[Any, ...]) -> tuple[Any, ...]:
	if result != FT_OK:
		raise FTDeviceError(result)
	return args


FT_GetDeviceInfo = WINFUNCTYPE(FT_STATUS, FT_HANDLE, POINTER(FT_DEVICE), LPDWORD, PCHAR, PCHAR, PVOID)(
	("FT_GetDeviceInfo", ft),
	(
		(1, "ftHandle"),
		(2, "pftType"),
		(2, "lpdwID"),
		(2, "pcSerialNumber"),
		(2, "pcDescription"),
		(2, "pvDummy"),
	),
)
FT_GetDeviceInfo.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDeviceInfo(*args):
# return ft.FT_GetDeviceInfo(*args)

FT_OpenEx = WINFUNCTYPE(FT_STATUS, PVOID, DWORD, POINTER(FT_HANDLE))(
	("FT_OpenEx", ft),
	(
		(1, "pvArg1"),
		(1, "dwFlags"),
		(2, "ftHandle"),
	),
)
FT_OpenEx.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_OpenEx(*args):
# return ft.FT_OpenEx(*args)


FT_Open = WINFUNCTYPE(FT_STATUS, c_int, POINTER(FT_HANDLE))(
	("FT_Open", ft),
	((1, "iDevice"), (2, "ftHandle")),
)
FT_Open.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Open(*args):
# return ft.FT_Open(*args)

FT_ListDevices = WINFUNCTYPE(FT_STATUS, PVOID, PVOID, DWORD)(
	("FT_ListDevices", ft),
	((3, "pvArg1"), (3, "pvArg2"), (1, "dwFlags")),
)
FT_ListDevices.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_ListDevices(*args):
# return ft.FT_ListDevices(*args)

FT_Close = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(
	("FT_Close", ft),
	((1, "ftHandle"),),
)
FT_Close.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Close(*args):
# return ft.FT_Close(*args)

FT_Read = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPVOID, DWORD, LPDWORD)(
	("FT_Read", ft),
	((1, "ftHandle"), (2, "lpBuffer"), (1, "dwBytesToRead"), (2, "lpdwBytesReturned")),
)
FT_Read.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Read(*args):
# return ft.FT_Read(*args)

FT_Write = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPVOID, DWORD, LPDWORD)(
	("FT_Write", ft),
	((1, "ftHandle"), (1, "lpBuffer"), (1, "dwBytesToWrite"), (2, "lpdwBytesWritten")),
)
FT_Write.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Write(*args):
# return ft.FT_Write(*args)


FT_SetBaudRate = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD)(
	("FT_SetBaudRate", ft),
	((1, "ftHandle"), (1, "dwBaudRate")),
)
FT_SetBaudRate.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetBaudRate(*args):
# return ft.FT_SetBaudRate(*args)

FT_ResetDevice = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(
	("FT_ResetDevice", ft),
	((1, "ftHandle"),),
)
FT_ResetDevice.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_ResetDevice(*args):
# return ft.FT_ResetDevice(*args)

FT_Purge = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD)(
	("FT_Purge", ft),
	((1, "ftHandle"), (1, "uEventCh")),
)
FT_Purge.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Purge(*args):
# return ft.FT_Purge(*args)

FT_SetTimeouts = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD, DWORD)(
	("FT_SetTimeouts", ft),
	((1, "ftHandle"), (1, "dwReadTimeout"), (1, "dwWriteTimeout")),
)
FT_SetTimeouts.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetTimeouts(*args):
# return ft.FT_SetTimeouts(*args)

FT_SetBitMode = WINFUNCTYPE(FT_STATUS, FT_HANDLE, UCHAR, UCHAR)(
	("FT_SetBitMode", ft),
	((1, "ftHandle"), (1, "ucMask"), (1, "ucMode")),
)
FT_SetBitMode.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetBitMode(*args):  # added by CJBH
# return ft.FT_SetBitMode(*args)

FT_GetQueueStatus = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPDWORD)(
	("FT_GetQueueStatus", ft),
	((1, "ftHandle"), (2, "lpdwAmountInRxQueue")),
)
FT_GetQueueStatus.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetQueueStatus(*args):
# return ft.FT_GetQueueStatus(*args)

FT_GetStatus = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPDWORD, LPDWORD, LPDWORD)(
	("FT_GetStatus", ft),
	((1, "ftHandle"), (2, "lpdwAmountInRxQueue"), (2, "lpdwAmountInTxQueue"), (2, "lpdwEventStatus")),
)
FT_GetStatus.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetStatus(*args):
# return ft.FT_GetStatus(*args)


FT_SetLatencyTimer = WINFUNCTYPE(FT_STATUS, FT_HANDLE, UCHAR)(
	("FT_SetLatencyTimer", ft),
	((1, "ftHandle"), (1, "ucTimer")),
)
FT_SetLatencyTimer.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetLatencyTimer(*args):
# return ft.FT_SetLatencyTimer(*args)

FT_SetUSBParameters = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD, DWORD)(
	("FT_SetUSBParameters", ft),
	((1, "ftHandle"), (1, "dwInTransferSize"), (1, "dwOutTransferSize")),
)
FT_SetUSBParameters.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetUSBParameters(*args):
# return ft.FT_SetUSBParameters(*args)

FT_ResetPort = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(("FT_ResetPort", ft), ((1, "ftHandle"),))
FT_ResetPort.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_ResetPort(*args):
# return ft.FT_ResetPort(*args)

FT_CyclePort = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(("FT_CyclePort", ft), ((1, "ftHandle"),))
FT_CyclePort.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_CyclePort(*args):
# return ft.FT_CyclePort(*args)

FT_CreateDeviceInfoList = WINFUNCTYPE(FT_STATUS, LPDWORD)(
	("FT_CreateDeviceInfoList", ft),
	((2, "lpdwNumDevs"),),
)
FT_CreateDeviceInfoList.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_CreateDeviceInfoList(*args):
# return ft.FT_CreateDeviceInfoList(*args)

FT_GetDeviceInfoList = WINFUNCTYPE(FT_STATUS, POINTER(FT_DEVICE_LIST_INFO_NODE), LPDWORD)(
	("FT_GetDeviceInfoList", ft),
	((2, "pDest"), (1, "lpdwNumDevs")),
)
FT_GetDeviceInfoList.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDeviceInfoList(*args):
# return ft.FT_GetDeviceInfoList(*args)


FT_GetDeviceInfoDetail = WINFUNCTYPE(
	FT_STATUS,
	DWORD,
	LPDWORD,
	LPDWORD,
	LPDWORD,
	LPDWORD,
	PCHAR,
	PCHAR,
	POINTER(FT_HANDLE),
)(
	("FT_GetDeviceInfoDetail", ft),
	(
		(1, "dwIndex"),
		(2, "lpdwFlags"),
		(2, "lpdwType"),
		(2, "lpdwID"),
		(2, "lpdwLocId"),
		(2, "pcSerialNumber"),
		(2, "pcDescription"),
		(2, "ftHandle"),
	),
)
FT_GetDeviceInfoDetail.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDeviceInfoDetail(*args):
# return ft.FT_GetDeviceInfoDetail(*args)

FT_GetDriverVersion = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPDWORD)(
	("FT_GetDriverVersion", ft),
	((1, "ftHandle"), (2, "lpdwDriverVersion")),
)
FT_GetDriverVersion.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDriverVersion(*args):
# return ft.FT_GetDriverVersion(*args)

FT_GetLibraryVersion = WINFUNCTYPE(FT_STATUS, LPDWORD)(("FT_GetLibraryVersion", ft), ((2, "lpdwDLLVersion"),))
FT_GetLibraryVersion.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetLibraryVersion(*args):
# return ft.FT_GetLibraryVersion(*args)


################################################
# Start of pythonic functions for specific     #
# functionality around FTDI API                #
################################################
def list_devices():
	"""method to list devices connected.
	total connected and specific serial for a device position"""
	n = c.c_ulong()
	FT_ListDevices(c.byref(n), None, c.c_ulong(FT_LIST_NUMBER_ONLY))

	if n.value:
		p_array = (c.c_char_p * (n.value + 1))()
		for i in range(n.value):
			p_array[i] = c.cast(c.c_buffer(64), c.c_char_p)
		FT_ListDevices(p_array, c.byref(n), c.c_ulong(FT_LIST_ALL | FT_OPEN_BY_SERIAL_NUMBER))
		return [ser for ser in p_array[: n.value]]
	else:
		return []


# ------------------------------------------------------------------------------
def create_device_info_list():
	"""Create the internal device info list and return number of entries"""
	lpdwNumDevs = c.c_ulong()
	FT_CreateDeviceInfoList(c.byref(lpdwNumDevs))
	return lpdwNumDevs.value


# ------------------------------------------------------------------------------
def get_device_info_detail(dev=0):
	"""Get an entry from the internal device info list."""
	dwIndex = c.c_ulong(dev)
	lpdwFlags = c.c_ulong()
	lpdwType = c.c_ulong()
	lpdwID = c.c_ulong()
	lpdwLocId = c.c_ulong()
	pcSerialNumber = c.c_buffer(MAX_DESCRIPTION_SIZE)
	pcDescription = c.c_buffer(MAX_DESCRIPTION_SIZE)
	ftHandle = c.c_ulong()
	FT_GetDeviceInfoDetail(
		dwIndex,
		c.byref(lpdwFlags),
		c.byref(lpdwType),
		c.byref(lpdwID),
		c.byref(lpdwLocId),
		pcSerialNumber,
		pcDescription,
		c.byref(ftHandle),
	)
	return {
		"Dev": dwIndex.value,
		"Flags": lpdwFlags.value,
		"Type": lpdwType.value,
		"ID": lpdwID.value,
		"LocId": lpdwLocId.value,
		"SerialNumber": pcSerialNumber.value,
		"Description": pcDescription.value,
		"ftHandle": ftHandle,
	}


# ------------------------------------------------------------------------------
def get_device_info_list():
	num_dev = create_device_info_list()
	dev_info = FT_DEVICE_LIST_INFO_NODE * (num_dev + 1)
	pDest = c.pointer(dev_info())
	lpdwNumDevs = c.c_ulong()
	FT_GetDeviceInfoList(pDest, c.byref(lpdwNumDevs))

	return_list = []
	data = pDest.contents
	for i in data:
		return_list.append(
			{
				"Flags": i.Flags,
				"Type": i.Type,
				"LocID": i.LocId,
				"SerialNumber": i.SerialNumber,
				"Description": i.Description,
			},
		)
	return return_list[:-1]


# ------------------------------------------------------------------------------
def open_ex(serial=b""):
	"""open's FTDI-device by EEPROM-serial (prefered method).
	Serial fetched by the ListDevices fn"""
	ftHandle = FT_HANDLE()
	FT_OpenEx(serial, FT_OPEN_BY_SERIAL_NUMBER, c.byref(ftHandle))
	return FTD2XX(ftHandle)


# ------------------------------------------------------------------------------


######################################
##     FTDI ctypes DLL wrapper      ##
######################################
class FTD2XX(object):
	"""class that implements a ctype interface to the FTDI d2xx driver"""

	def __init__(self, ftHandle):
		"""setup initial ctypes link and some varabled"""
		self.ftHandle = ftHandle

	# ------------------------------------------------------------------------------
	def set_baud_rate(self, dwBaudRate=921600):
		"""Set baud rate of driver, non-intelgent checking of allowed BAUD"""
		FT_SetBaudRate(self.ftHandle, c.c_ulong(dwBaudRate))
		return None

	# ------------------------------------------------------------------------------
	def set_timeouts(self, dwReadTimeout=100, dwWriteTimeout=100):
		"""setup timeout times for TX and RX"""
		FT_SetTimeouts(self.ftHandle, c.c_ulong(dwReadTimeout), c.c_ulong(dwWriteTimeout))
		return None

	# ------------------------------------------------------------------------------
	def set_latency_timer(self, ucTimer=16):  # added by CJBH
		"""setup latency timer"""
		FT_SetLatencyTimer(self.ftHandle, c.c_ubyte(ucTimer))
		return None

	# ------------------------------------------------------------------------------
	def set_bit_mode(self, ucMask=0, ucMode=0):  # added by CJBH
		"""setup bit mode"""
		FT_SetBitMode(self.ftHandle, c.c_ubyte(ucMask), c.c_ubyte(ucMode))
		return None

	# ------------------------------------------------------------------------------
	def set_usb_parameters(self, dwInTransferSize=4096, dwOutTransferSize=0):
		"""set the drivers input and output buffer size"""
		FT_SetUSBParameters(self.ftHandle, c.c_ulong(dwInTransferSize), c.c_ulong(dwOutTransferSize))
		return None

	# ------------------------------------------------------------------------------
	def purge(self, to_purge="TXRX"):
		"""purge the in and out buffer of driver.
		Valid arguement = TX,RX,TXRX"""
		if to_purge == "TXRX":
			dwMask = c.c_ulong(FT_PURGE_RX | FT_PURGE_TX)
		elif to_purge == "TX":
			dwMask = c.c_ulong(FT_PURGE_TX)
		elif to_purge == "RX":
			dwMask = c.c_ulong(FT_PURGE_RX)

		FT_Purge(self.ftHandle, dwMask)
		return None

	# ------------------------------------------------------------------------------
	def get_queue_status(self):
		"""returns the number of bytes in the RX buffer
		else raises an exception"""
		lpdwAmountInRxQueue = c.c_ulong()
		FT_GetQueueStatus(self.ftHandle, c.byref(lpdwAmountInRxQueue))
		return lpdwAmountInRxQueue.value

	# ------------------------------------------------------------------------------
	def write(self, lpBuffer=b""):
		"""writes the bytes-type "data" to the opened port."""
		lpdwBytesWritten = c.c_ulong()
		FT_Write(self.ftHandle, lpBuffer, len(lpBuffer), c.byref(lpdwBytesWritten))
		return lpdwBytesWritten.value

	# ------------------------------------------------------------------------------
	def read(self, dwBytesToRead, raw=True):
		"""Read in int-type of bytes. Returns either the data
		or raises an exception"""
		lpdwBytesReturned = c.c_ulong()
		lpBuffer = c.c_buffer(dwBytesToRead)
		FT_Read(self.ftHandle, lpBuffer, dwBytesToRead, c.byref(lpdwBytesReturned))
		return lpBuffer.raw[: lpdwBytesReturned.value] if raw else lpBuffer.value[: lpdwBytesReturned.value]

	# ------------------------------------------------------------------------------
	def reset_device(self):
		"""closes the port."""
		FT_ResetDevice(self.ftHandle)
		return None

	# ------------------------------------------------------------------------------
	def close(self):
		"""closes the port."""
		FT_Close(self.ftHandle)
		return None
