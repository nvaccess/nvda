from _ctypes import CFuncPtr
from ctypes import POINTER, WINFUNCTYPE, Structure, c_char, c_char_p, c_int, c_ubyte, c_void_p, windll
from ctypes.wintypes import DWORD, LPDWORD, PHANDLE
from enum import IntEnum, IntFlag
from typing import Any

dll = windll.ftd2xx

# Constants
MAX_SERIAL_NUMBER_SIZE = 16
MAX_DESCRIPTION_SIZE = 64

# Type definitions
UCHAR = c_ubyte
PUCHAR = POINTER(UCHAR)
PCHAR = c_char_p
FT_HANDLE = PHANDLE
FT_STATUS = FT_DEVICE = DWORD
PVOID = LPVOID = c_void_p


# Enumerations
class FT_MESSAGE(IntEnum):
	"""Possible values of FT_STATUS."""

	OK = 0
	INVALID_HANDLE = 1
	DEVICE_NOT_FOUND = 2
	DEVICE_NOT_OPENED = 3
	IO_ERROR = 4
	INSUFFICIENT_RESOURCES = 5
	INVALID_PARAMETER = 6
	INVALID_BAUD_RATE = 7
	DEVICE_NOT_OPENED_FOR_ERASE = 8
	DEVICE_NOT_OPENED_FOR_WRITE = 9
	FAILED_TO_WRITE_DEVICE = 10
	EEPROM_READ_FAILED = 11
	EEPROM_WRITE_FAILED = 12
	EEPROM_ERASE_FAILED = 13
	EEPROM_NOT_PRESENT = 14
	EEPROM_NOT_PROGRAMMED = 15
	INVALID_ARGS = 16
	NOT_SUPPORTED = 17
	OTHER_ERROR = 18


class FT_LIST(IntFlag):
	"""Flags for the FT_ListDevices function."""

	NUMBER_ONLY = 0x80000000
	BY_INDEX = 0x40000000
	ALL = 0x20000000


class FT_OPEN_BY(IntFlag):
	"""Flags for use with the FT_OpenEx function."""

	SERIAL_NUMBER = 1
	DESCRIPTION = 2
	LOCATION = 4


class FT_PURGE(IntFlag):
	"""Flags for use wth the FT_Purge function."""

	RX = 1
	TX = 2


class FT_BITMODE(IntEnum):
	"""Modes for use with the FT_SetBitMode  function."""

	RESET = 0x00
	ASYNC_BITBANG = 0x01
	MPSSE = 0x02
	SYNC_BITBANG = 0x04
	MCU_HOST = 0x08
	FAST_SERIAL = 0x10
	CBUS_BITBANG = 0x20
	SYNC_FIFO = 0x40


# Structures
#####################################
# CTYPES structure for DeviceInfo   #
#####################################
class FT_DEVICE_LIST_INFO_NODE(Structure):
	_fields_ = (
		("Flags", DWORD),  # c.c_ulong
		("Type", DWORD),  # c.c_ulong
		("ID", DWORD),  # c.c_ulong
		# ("LocID", c.c_ulong),
		("LocId", DWORD),
		("SerialNumber", c_char * 16),
		("Description", c_char * 64),
		# ("none", c.c_void_p),
		("ftHandle", FT_HANDLE),
	)


# Error checking
######################################
##      FTDI exception classes      ##
######################################
class FTDeviceError(Exception):
	"""Exception class for FTDI function returns"""

	def __init__(self, status: int):
		self.parameter = FT_MESSAGE(status)._name_
		self.status = status

	def __str__(self):
		return repr(self.parameter)


def _ftd2xxErrorCheck(result: int, func: CFuncPtr, args: tuple[Any, ...]) -> tuple[Any, ...]:
	if result != FT_MESSAGE.OK:
		raise FTDeviceError(result)
	return args


# Function prototypes
FT_CreateDeviceInfoList = WINFUNCTYPE(FT_STATUS, LPDWORD)(
	("FT_CreateDeviceInfoList", dll),
	# ((2, "lpdwNumDevs"),),
)
"""Builds a device information list and returns the number of D2XX devices connected to the system."""
FT_CreateDeviceInfoList.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_CreateDeviceInfoList(*args):
# return ft.FT_CreateDeviceInfoList(*args)

FT_GetDeviceInfoList = WINFUNCTYPE(FT_STATUS, POINTER(FT_DEVICE_LIST_INFO_NODE), LPDWORD)(
	("FT_GetDeviceInfoList", dll),
	# ((2, "pDest"), (1, "lpdwNumDevs")),
)
"""Returns a device information list and the number of D2XX devices in the list."""
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
	("FT_GetDeviceInfoDetail", dll),
	# (
	# (1, "dwIndex"),
	# (2, "lpdwFlags"),
	# (2, "lpdwType"),
	# (2, "lpdwID"),
	# (2, "lpdwLocId"),
	# (2, "pcSerialNumber"),
	# (2, "pcDescription"),
	# (2, "ftHandle"),
	# ),
)
"""Returns an entry from the device information list."""
FT_GetDeviceInfoDetail.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDeviceInfoDetail(*args):
# return ft.FT_GetDeviceInfoDetail(*args)

FT_ListDevices = WINFUNCTYPE(FT_STATUS, PVOID, PVOID, DWORD)(
	("FT_ListDevices", dll),
	# (
	# (3, "pvArg1"),
	# (3, "pvArg2"),
	# (1, "dwFlags"),
	# ),
)
"""Gets information concerning the devices currently connected."""
FT_ListDevices.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_ListDevices(*args):
# return ft.FT_ListDevices(*args)

FT_Open = WINFUNCTYPE(FT_STATUS, c_int, POINTER(FT_HANDLE))(
	("FT_Open", dll),
	# (
	# (1, "iDevice"),
	# (2, "ftHandle"),
	# ),
)
"""Open the device and return a handle which will be used for subsequent accesses."""
FT_Open.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Open(*args):
# return ft.FT_Open(*args)

FT_OpenEx = WINFUNCTYPE(FT_STATUS, PVOID, DWORD, POINTER(FT_HANDLE))(
	("FT_OpenEx", dll),
	# (
	# (1, "pvArg1"),
	# (1, "dwFlags"),
	# (2, "ftHandle"),
	# ),
)
"""Open the device specified by serial number, device description or location, and return a handle that will be used for subsequent accesses."""
FT_OpenEx.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_OpenEx(*args):
# return ft.FT_OpenEx(*args)

FT_Close = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(
	("FT_Close", dll),
	# ((1, "ftHandle"),),
)
"""Close an open device."""
FT_Close.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Close(*args):
# return ft.FT_Close(*args)

FT_Read = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPVOID, DWORD, LPDWORD)(
	("FT_Read", dll),
	# (
	# (1, "ftHandle"),
	# (2, "lpBuffer"),
	# (1, "dwBytesToRead"),
	# (2, "lpdwBytesReturned"),
	# ),
)
"""Read data from the device."""
FT_Read.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Read(*args):
# return ft.FT_Read(*args)

FT_Write = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPVOID, DWORD, LPDWORD)(
	("FT_Write", dll),
	# (
	# (1, "ftHandle"),
	# (1, "lpBuffer"),
	# (1, "dwBytesToWrite"),
	# (2, "lpdwBytesWritten"),
	# ),
)
"""Write data to the device."""
FT_Write.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Write(*args):
# return ft.FT_Write(*args)

FT_SetBaudRate = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD)(
	("FT_SetBaudRate", dll),
	# (
	# (1, "ftHandle"),
	# (1, "dwBaudRate"),
	# ),
)
"""Sets the baud rate for the device."""
FT_SetBaudRate.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetBaudRate(*args):
# return ft.FT_SetBaudRate(*args)

FT_SetTimeouts = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD, DWORD)(
	("FT_SetTimeouts", dll),
	# (
	# (1, "ftHandle"),
	# (1, "dwReadTimeout"),
	# (1, "dwWriteTimeout"),
	# ),
)
"""Sets the read and write timeouts for the device."""
FT_SetTimeouts.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetTimeouts(*args):
# return ft.FT_SetTimeouts(*args)

FT_GetQueueStatus = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPDWORD)(
	("FT_GetQueueStatus", dll),
	# (
	# (1, "ftHandle"),
	# (2, "lpdwAmountInRxQueue"),
	# ),
)
"""Gets the number of bytes in the receive queue."""
FT_GetQueueStatus.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetQueueStatus(*args):
# return ft.FT_GetQueueStatus(*args)


FT_GetDeviceInfo = WINFUNCTYPE(FT_STATUS, FT_HANDLE, POINTER(FT_DEVICE), LPDWORD, PCHAR, PCHAR, PVOID)(
	("FT_GetDeviceInfo", dll),
	# (
	# (1, "ftHandle"),
	# (2, "pftType"),
	# (2, "lpdwID"),
	# (2, "pcSerialNumber"),
	# (2, "pcDescription"),
	# (2, "pvDummy"),
	# ),
)
"""Get device information for an open device."""
FT_GetDeviceInfo.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDeviceInfo(*args):
# return ft.FT_GetDeviceInfo(*args)

FT_GetDriverVersion = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPDWORD)(
	("FT_GetDriverVersion", dll),
	# (
	# (1, "ftHandle"),
	# (2, "lpdwDriverVersion"),
	# ),
)
"""Returns the D2XX driver version number."""
FT_GetDriverVersion.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetDriverVersion(*args):
# return ft.FT_GetDriverVersion(*args)

FT_GetLibraryVersion = WINFUNCTYPE(FT_STATUS, LPDWORD)(
	("FT_GetLibraryVersion", dll),
	# ((2, "lpdwDLLVersion"),),
)
"""Returns D2XX DLL version number."""
FT_GetLibraryVersion.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetLibraryVersion(*args):
# return ft.FT_GetLibraryVersion(*args)

FT_GetStatus = WINFUNCTYPE(FT_STATUS, FT_HANDLE, LPDWORD, LPDWORD, LPDWORD)(
	("FT_GetStatus", dll),
	# (
	# (1, "ftHandle"),
	# (2, "lpdwAmountInRxQueue"),
	# (2, "lpdwAmountInTxQueue"),
	# (2, "lpdwEventStatus"),
	# ),
)
"""Gets the device status including number of characters in the receive queue, number of characters in the transmit queue, and the current event status."""
FT_GetStatus.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_GetStatus(*args):
# return ft.FT_GetStatus(*args)


FT_Purge = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD)(
	("FT_Purge", dll),
	# (
	# (1, "ftHandle"),
	# (1, "uEventCh"),
	# ),
)
"""Purges receive and transmit buffers in the device."""
FT_Purge.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_Purge(*args):
# return ft.FT_Purge(*args)

FT_ResetDevice = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(
	("FT_ResetDevice", dll),
	# ((1, "ftHandle"),),
)
"""Sends a reset command to the device."""
FT_ResetDevice.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_ResetDevice(*args):
# return ft.FT_ResetDevice(*args)

FT_ResetPort = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(
	("FT_ResetPort", dll),
	# ((1, "ftHandle"),),
)
FT_ResetPort.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_ResetPort(*args):
# return ft.FT_ResetPort(*args)

FT_CyclePort = WINFUNCTYPE(FT_STATUS, FT_HANDLE)(
	("FT_CyclePort", dll),
	# ((1, "ftHandle"),),
)
"""Send a cycle command to the USB port."""
FT_CyclePort.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_CyclePort(*args):
# return ft.FT_CyclePort(*args)

FT_SetLatencyTimer = WINFUNCTYPE(FT_STATUS, FT_HANDLE, UCHAR)(
	("FT_SetLatencyTimer", dll),
	# (
	# (1, "ftHandle"),
	# (1, "ucTimer"),
	# ),
)
"""
Set the latency timer value.

.. note::
	This is an extended API function, and may not be available on all FTDI devices.
"""
FT_SetLatencyTimer.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetLatencyTimer(*args):
# return ft.FT_SetLatencyTimer(*args)

FT_SetBitMode = WINFUNCTYPE(FT_STATUS, FT_HANDLE, UCHAR, UCHAR)(
	("FT_SetBitMode", dll),
	# (
	# (1, "ftHandle"),
	# (1, "ucMask"),
	# (1, "ucMode"),
	# ),
)
"""
Enables different chip modes.

.. note::
	This is an extended API function, and may not be available on all FTDI devices.
"""
FT_SetBitMode.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetBitMode(*args):  # added by CJBH
# return ft.FT_SetBitMode(*args)

FT_SetUSBParameters = WINFUNCTYPE(FT_STATUS, FT_HANDLE, DWORD, DWORD)(
	("FT_SetUSBParameters", dll),
	# (
	# (1, "ftHandle"),
	# (1, "dwInTransferSize"),
	# (1, "dwOutTransferSize"),
	# ),
)
"""
Set the USB request transfer size.

.. note::
	This is an extended API function, and may not be available on all FTDI devices.
"""
FT_SetUSBParameters.errcheck = _ftd2xxErrorCheck
# @ftExceptionDecorator
# def _PY_SetUSBParameters(*args):
# return ft.FT_SetUSBParameters(*args)
