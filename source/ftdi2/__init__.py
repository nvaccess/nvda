#!/usr/bin/env python

"""This module is the first implementation of FTD2xx driver for the
FTDI USB chips. Initial implementation is for functions from the
dll required for present project"""
# (from: http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip)

from ctypes import (
	byref,
	c_char_p,
	cast,
	create_string_buffer,
)
from ctypes.wintypes import DWORD
from typing import Any

from .ftdi2xx import (
	FT_DEVICE_LIST_INFO_NODE,
	FT_HANDLE,
	FT_LIST,
	FT_OPEN_BY,
	FT_PURGE,
	MAX_DESCRIPTION_SIZE,
	MAX_SERIAL_NUMBER_SIZE,
	FT_Close,
	FT_CreateDeviceInfoList,
	FT_GetDeviceInfoDetail,
	FT_GetDeviceInfoList,
	FT_GetQueueStatus,
	FT_ListDevices,
	FT_OpenEx,
	FT_Purge,
	FT_Read,
	FT_ResetDevice,
	FT_SetBaudRate,
	FT_SetBitMode,
	FT_SetLatencyTimer,
	FT_SetTimeouts,
	FT_SetUSBParameters,
	FT_Write,
)

__FT_VERSION__ = "1.1"
__FT_LICENCE__ = "LGPL3"
__FT_AUTHOR__ = "Jonathan Roadley-Battin"


class FTD2XX:
	"""class that implements a ctype interface to the FTDI d2xx driver"""

	def __init__(self, ftHandle: FT_HANDLE):
		"""setup initial ctypes link and some varabled"""
		self.ftHandle = ftHandle

	def setBaudRate(self, dwBaudRate: int = 921600) -> None:
		"""Set baud rate of driver, non-intelgent checking of allowed BAUD"""
		FT_SetBaudRate(self.ftHandle, dwBaudRate)

	def setTimeouts(self, dwReadTimeout: int = 100, dwWriteTimeout: int = 100) -> None:
		"""setup timeout times for TX and RX"""
		FT_SetTimeouts(self.ftHandle, dwReadTimeout, dwWriteTimeout)

	def setLatencyTimer(self, ucTimer: int = 16) -> None:
		"""setup latency timer"""
		FT_SetLatencyTimer(self.ftHandle, ucTimer)

	def setBitMode(self, ucMask: int = 0, ucMode: int = 0) -> None:
		"""setup bit mode"""
		FT_SetBitMode(self.ftHandle, ucMask, ucMode)

	def setUsbParameters(self, dwInTransferSize: int = 4096, dwOutTransferSize: int = 0) -> None:
		"""set the drivers input and output buffer size"""
		FT_SetUSBParameters(self.ftHandle, dwInTransferSize, dwOutTransferSize)

	def purge(self, toPurge: str = "TXRX") -> None:
		"""purge the in and out buffer of driver.
		Valid arguement = TX,RX,TXRX"""
		if toPurge == "TXRX":
			dwMask = FT_PURGE.RX | FT_PURGE.TX
		elif toPurge == "TX":
			dwMask = FT_PURGE.TX
		elif toPurge == "RX":
			dwMask = FT_PURGE.RX
		FT_Purge(self.ftHandle, dwMask)

	def getQueueStatus(self) -> int:
		"""returns the number of bytes in the RX buffer
		else raises an exception"""
		lpdwAmountInRxQueue = DWORD()
		FT_GetQueueStatus(self.ftHandle, byref(lpdwAmountInRxQueue))
		return lpdwAmountInRxQueue.value

	def write(self, lpBuffer: bytes = b"") -> int:
		"""writes the bytes-type "data" to the opened port."""
		lpdwBytesWritten = DWORD()
		FT_Write(self.ftHandle, lpBuffer, len(lpBuffer), byref(lpdwBytesWritten))
		return lpdwBytesWritten.value

	def read(self, dwBytesToRead: int, raw: bool = True) -> bytes:
		"""Read in int-type of bytes. Returns either the data
		or raises an exception"""
		lpdwBytesReturned = DWORD()
		lpBuffer = create_string_buffer(dwBytesToRead)
		FT_Read(self.ftHandle, lpBuffer, dwBytesToRead, byref(lpdwBytesReturned))
		return lpBuffer.raw[: lpdwBytesReturned.value] if raw else lpBuffer.value[: lpdwBytesReturned.value]

	def resetDevice(self) -> None:
		"""closes the port."""
		FT_ResetDevice(self.ftHandle)

	def close(self) -> None:
		"""closes the port."""
		FT_Close(self.ftHandle)


def listDevices() -> list[bytes]:
	"""method to list devices connected.
	total connected and specific serial for a device position"""
	n = DWORD()
	FT_ListDevices(byref(n), None, FT_LIST.NUMBER_ONLY)

	if n.value:
		serialNumbers = (c_char_p * (n.value + 1))()
		for i in range(n.value):
			serialNumbers[i] = cast(create_string_buffer(MAX_SERIAL_NUMBER_SIZE), c_char_p)
		FT_ListDevices(serialNumbers, byref(n), FT_LIST.ALL | FT_OPEN_BY.SERIAL_NUMBER)
		return [ser for ser in serialNumbers[: n.value]]
	else:
		return []


def createDeviceInfoList() -> int:
	"""Create the internal device info list and return number of entries"""
	lpdwNumDevs = DWORD()
	FT_CreateDeviceInfoList(byref(lpdwNumDevs))
	return lpdwNumDevs.value


def getDeviceInfoDetail(dev=0) -> dict[str, Any]:
	"""Get an entry from the internal device info list."""
	dwIndex = DWORD(dev)
	lpdwFlags = DWORD()
	lpdwType = DWORD()
	lpdwID = DWORD()
	lpdwLocId = DWORD()
	pcSerialNumber = create_string_buffer(MAX_SERIAL_NUMBER_SIZE)
	pcDescription = create_string_buffer(MAX_DESCRIPTION_SIZE)
	ftHandle = FT_HANDLE()
	FT_GetDeviceInfoDetail(
		dwIndex,
		byref(lpdwFlags),
		byref(lpdwType),
		byref(lpdwID),
		byref(lpdwLocId),
		pcSerialNumber,
		pcDescription,
		byref(ftHandle),
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


def getDeviceInfoList() -> list[dict[str, Any]]:
	numDevs = createDeviceInfoList()
	devInfos = FT_DEVICE_LIST_INFO_NODE * (numDevs + 1)
	lpdwNumDevs = DWORD()
	FT_GetDeviceInfoList(devInfos, byref(lpdwNumDevs))
	returnList = []
	for i in devInfos:
		returnList.append(
			{
				"Flags": i.Flags,
				"Type": i.Type,
				"LocID": i.LocId,
				"SerialNumber": i.SerialNumber,
				"Description": i.Description,
			},
		)
	return returnList[:-1]


def openEx(serial: bytes = b"") -> FTD2XX:
	"""open's FTDI-device by EEPROM-serial (prefered method).
	Serial fetched by the ListDevices fn"""
	ftHandle = FT_HANDLE()
	FT_OpenEx(serial, FT_OPEN_BY.SERIAL_NUMBER, byref(ftHandle))
	return FTD2XX(ftHandle)
