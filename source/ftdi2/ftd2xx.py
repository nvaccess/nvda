# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013-2025, NV Access Limited, Jonathan Roadley-Battin
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Functions exported by ftd2xx.dll, and supporting data structures, constants  and enumerations.

Based on work from http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip.

.. seealso::
	`D2XX Programmer’s Guide <https://ftdichip.com/document/programming-guides/>`_
		Guide to the API for the FTD2XX DLL function library.

		This file prepared with D2XX Programmer’s Guide Version 1.6.
"""

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
FT_STATUS = DWORD
FT_DEVICE = DWORD
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
	"""Flags for use with the FT_Purge function."""

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
class FT_DEVICE_LIST_INFO_NODE(Structure):
	"""Struct returned by the FT_GetDeviceInfoList function."""

	_fields_ = (
		("Flags", DWORD),
		("Type", DWORD),
		("ID", DWORD),
		("LocId", DWORD),
		("SerialNumber", c_char * MAX_SERIAL_NUMBER_SIZE),
		("Description", c_char * MAX_DESCRIPTION_SIZE),
		("ftHandle", FT_HANDLE),
	)


# Error checking
class FTDeviceError(Exception):
	"""Exception class for FTDI function returns"""

	def __init__(self, status: int):
		self.parameter = FT_MESSAGE(status)._name_
		self.status = status

	def __str__(self):
		return repr(self.parameter)


def _errorCheck(result: int, func: CFuncPtr, args: tuple[Any, ...]) -> tuple[Any, ...]:
	if result != FT_MESSAGE.OK:
		raise FTDeviceError(result)
	return args


# Function prototypes
FT_CreateDeviceInfoList = WINFUNCTYPE(
	FT_STATUS,
	LPDWORD,  # lpdwNumDevs
)(("FT_CreateDeviceInfoList", dll))
"""Builds a device information list and returns the number of D2XX devices connected to the system."""
FT_CreateDeviceInfoList.errcheck = _errorCheck

FT_GetDeviceInfoList = WINFUNCTYPE(
	FT_STATUS,
	POINTER(FT_DEVICE_LIST_INFO_NODE),  # pDest
	LPDWORD,  # lpdwNumDevs
)(("FT_GetDeviceInfoList", dll))
"""Returns a device information list and the number of D2XX devices in the list."""
FT_GetDeviceInfoList.errcheck = _errorCheck

FT_GetDeviceInfoDetail = WINFUNCTYPE(
	FT_STATUS,
	DWORD,  # dwIndex
	LPDWORD,  # lpdwFlags
	LPDWORD,  # lpdwType
	LPDWORD,  # lpdwID
	LPDWORD,  # lpdwLocId
	PCHAR,  # pcSerialNumber
	PCHAR,  # pcDescription
	POINTER(FT_HANDLE),  # ftHandle
)(("FT_GetDeviceInfoDetail", dll))
"""Returns an entry from the device information list."""
FT_GetDeviceInfoDetail.errcheck = _errorCheck

FT_ListDevices = WINFUNCTYPE(
	FT_STATUS,
	PVOID,  # pvArg1
	PVOID,  # pvArg2
	DWORD,  # dwFlags
)(("FT_ListDevices", dll))
"""Gets information concerning the devices currently connected."""
FT_ListDevices.errcheck = _errorCheck

FT_Open = WINFUNCTYPE(
	FT_STATUS,
	c_int,  # iDevice
	POINTER(FT_HANDLE),  # ftHandle
)(("FT_Open", dll))
"""Open the device and return a handle which will be used for subsequent accesses."""
FT_Open.errcheck = _errorCheck

FT_OpenEx = WINFUNCTYPE(
	FT_STATUS,
	PVOID,  # pvArg1
	DWORD,  # dwFlags
	POINTER(FT_HANDLE),  # ftHandle
)(("FT_OpenEx", dll))
"""Open the device specified by serial number, device description or location, and return a handle that will be used for subsequent accesses."""
FT_OpenEx.errcheck = _errorCheck

FT_Close = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
)(("FT_Close", dll))
"""Close an open device."""
FT_Close.errcheck = _errorCheck

FT_Read = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	LPVOID,  # lpBuffer
	DWORD,  # dwBytesToRead
	LPDWORD,  # lpdwBytesReturned
)(("FT_Read", dll))
"""Read data from the device."""
FT_Read.errcheck = _errorCheck

FT_Write = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	LPVOID,  # lpBuffer
	DWORD,  # dwBytesToWrite
	LPDWORD,  # lpdwBytesWritten
)(("FT_Write", dll))
"""Write data to the device."""
FT_Write.errcheck = _errorCheck

FT_SetBaudRate = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	DWORD,  # dwBaudRate
)(("FT_SetBaudRate", dll))
"""Sets the baud rate for the device."""
FT_SetBaudRate.errcheck = _errorCheck

FT_SetTimeouts = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	DWORD,  # dwReadTimeout
	DWORD,  # dwWriteTimeout
)(("FT_SetTimeouts", dll))
"""Sets the read and write timeouts for the device."""
FT_SetTimeouts.errcheck = _errorCheck

FT_GetQueueStatus = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	LPDWORD,  # lpdwAmountInRxQueue
)(("FT_GetQueueStatus", dll))
"""Gets the number of bytes in the receive queue."""
FT_GetQueueStatus.errcheck = _errorCheck

FT_GetDeviceInfo = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	POINTER(FT_DEVICE),  # pftType
	LPDWORD,  # lpdwID
	PCHAR,  # pcSerialNumber
	PCHAR,  # pcDescription
	PVOID,  # pvDummy
)(("FT_GetDeviceInfo", dll))
"""Get device information for an open device."""
FT_GetDeviceInfo.errcheck = _errorCheck

FT_GetDriverVersion = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	LPDWORD,  # lpdwDriverVersion
)(("FT_GetDriverVersion", dll))
"""Returns the D2XX driver version number."""
FT_GetDriverVersion.errcheck = _errorCheck

FT_GetLibraryVersion = WINFUNCTYPE(
	FT_STATUS,
	LPDWORD,  # lpdwDLLVersion
)(("FT_GetLibraryVersion", dll))
"""Returns D2XX DLL version number."""
FT_GetLibraryVersion.errcheck = _errorCheck

FT_GetStatus = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	LPDWORD,  # lpdwAmountInRxQueue
	LPDWORD,  # lpdwAmountInTxQueue
	LPDWORD,  # lpdwEventStatus
)(("FT_GetStatus", dll))
"""Gets the device status including number of characters in the receive queue, number of characters in the transmit queue, and the current event status."""
FT_GetStatus.errcheck = _errorCheck

FT_Purge = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	DWORD,  # uEventCh
)(("FT_Purge", dll))
"""Purges receive and transmit buffers in the device."""
FT_Purge.errcheck = _errorCheck

FT_ResetDevice = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
)(("FT_ResetDevice", dll))
"""Sends a reset command to the device."""
FT_ResetDevice.errcheck = _errorCheck

FT_ResetPort = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
)(("FT_ResetPort", dll))
"""Send a reset command to the port."""
FT_ResetPort.errcheck = _errorCheck

FT_CyclePort = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
)(("FT_CyclePort", dll))
"""Send a cycle command to the USB port."""
FT_CyclePort.errcheck = _errorCheck

FT_SetLatencyTimer = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	UCHAR,  # ucTimer
)(("FT_SetLatencyTimer", dll))
"""
Set the latency timer value.

.. note::
	This is an extended API function, and may not be available on all FTDI devices.
"""
FT_SetLatencyTimer.errcheck = _errorCheck

FT_SetBitMode = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle#ftHandle
	UCHAR,  # ucMask
	UCHAR,  # ucMode
)(("FT_SetBitMode", dll))
"""
Enables different chip modes.

.. note::
	This is an extended API function, and may not be available on all FTDI devices.
"""
FT_SetBitMode.errcheck = _errorCheck

FT_SetUSBParameters = WINFUNCTYPE(
	FT_STATUS,
	FT_HANDLE,  # ftHandle
	DWORD,  # dwInTransferSize
	DWORD,  # dwOutTransferSize
)(("FT_SetUSBParameters", dll))
"""
Set the USB request transfer size.

.. note::
	This is an extended API function, and may not be available on all FTDI devices.
"""
FT_SetUSBParameters.errcheck = _errorCheck
