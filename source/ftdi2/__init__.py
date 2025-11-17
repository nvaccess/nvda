# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013-2025, NV Access Limited, Jonathan Roadley-Battin
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Lo-level pythonic interface to FTDI chips.

Based on work from http://fluidmotion.dyndns.org/zenphoto/index.php?p=news&title=Python-interface-to-FTDI-driver-chip.
"""

from ctypes import (
	byref,
	c_char_p,
	cast,
	create_string_buffer,
)
from ctypes.wintypes import DWORD
from typing import TypedDict, NotRequired

from .ftd2xx import (
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


class DeviceInfo(TypedDict):
	"""Typing information for dictionaries returned by :func:`getDeviceInfoDetail` and :func:`getDeviceInfoList`."""

	Dev: NotRequired[int]
	Flags: int
	Type: int
	ID: int
	LocId: int
	SerialNumber: bytes
	Description: bytes
	ftHandle: FT_HANDLE


class FTD2XX:
	"""Low-level interface to an FTDI device via the the FTD2XX driver."""

	def __init__(self, ftHandle: FT_HANDLE):
		"""
		Class initialiser.

		:param ftHandle: Handle to the device to be controlled.
		"""
		self.ftHandle = ftHandle

	def setBaudRate(self, dwBaudRate: int = 921600) -> None:
		"""
		Set baud rate of communication.

		:param dwBaudRate: Baud rate to use, defaults to 921600.
		"""
		FT_SetBaudRate(self.ftHandle, dwBaudRate)

	# For compatibility with serial.Serial
	set_baud_rate = setBaudRate

	def setTimeouts(self, dwReadTimeout: int = 100, dwWriteTimeout: int = 100) -> None:
		"""
		Set read and write timeouts.

		:param dwReadTimeout: New read timeout in milliseconds, defaults to 100
		:param dwWriteTimeout: New write timeout in milliseconds, defaults to 100
		"""
		FT_SetTimeouts(self.ftHandle, dwReadTimeout, dwWriteTimeout)

	def setLatencyTimer(self, ucTimer: int = 16) -> None:
		"""
		Set the latency timer value.

		:param ucTimer: New latency timer value, defaults to 16
		"""
		FT_SetLatencyTimer(self.ftHandle, ucTimer)

	def setBitMode(self, ucMask: int = 0, ucMode: int = 0) -> None:
		"""
		Set the chip's operating mode.

		:param ucMask: Sets which pins are inputs and which are outputs, defaults to 0
		:param ucMode: Sets the bit mode, defaults to 0
		"""
		FT_SetBitMode(self.ftHandle, ucMask, ucMode)

	def setUsbParameters(self, dwInTransferSize: int = 4096, dwOutTransferSize: int = 0) -> None:
		"""
		set the device's input and output buffer size.

		:param dwInTransferSize: Transfer size for USB IN request, defaults to 4096
		:param dwOutTransferSize: Transfer size for USB OUT request, defaults to 0
		"""
		FT_SetUSBParameters(self.ftHandle, dwInTransferSize, dwOutTransferSize)

	def purge(self, toPurge: str = "TXRX") -> None:
		"""
		Purge the device's transmit and/or receive buffers.

		:param toPurge: Which buffers to purge, defaults to "TXRX"
			* "TX" purges the transmit buffer;
			* "RX" purges the receive buffer;
			* "TXRX" purges both the transmit and receive buffers.
		:raises ValueError: If ``toPurge`` is not one of "TX", "RX" or "TXRX".
		"""
		if toPurge == "TXRX":
			dwMask = FT_PURGE.RX | FT_PURGE.TX
		elif toPurge == "TX":
			dwMask = FT_PURGE.TX
		elif toPurge == "RX":
			dwMask = FT_PURGE.RX
		else:
			raise ValueError(f"Got invalid value for toPurge: {toPurge}")
		FT_Purge(self.ftHandle, dwMask)

	def getQueueStatus(self) -> int:
		"""
		Gets the number of bytes in the receive queue.

		:return: The number of bytes in the read queue.
		"""
		lpdwAmountInRxQueue = DWORD()
		FT_GetQueueStatus(self.ftHandle, byref(lpdwAmountInRxQueue))
		return lpdwAmountInRxQueue.value

	def write(self, lpBuffer: bytes = b"") -> int:
		"""
		Writes data to the device.

		:param lpBuffer: Data to write, defaults to b""
		:return: The number of bytes written to the device.
		"""
		lpdwBytesWritten = DWORD()
		FT_Write(self.ftHandle, lpBuffer, len(lpBuffer), byref(lpdwBytesWritten))
		return lpdwBytesWritten.value

	def read(self, dwBytesToRead: int, raw: bool = True) -> bytes:
		"""
		Read data from the device.

		:param dwBytesToRead: Number of bytes of data to read.
		:param raw: Whether to return the raw data, defaults to True
			* If ``True``, exactly the data received is returned;
			* If ``False``, the data is treated as a c-style string.
		:return: The data read from the device.
		"""
		lpdwBytesReturned = DWORD()
		lpBuffer = create_string_buffer(dwBytesToRead)
		FT_Read(self.ftHandle, lpBuffer, dwBytesToRead, byref(lpdwBytesReturned))
		return (lpBuffer.raw if raw else lpBuffer.value)[: lpdwBytesReturned.value]

	def resetDevice(self) -> None:
		"""Sends a reset command to the device."""
		FT_ResetDevice(self.ftHandle)

	def close(self) -> None:
		"""closes the device."""
		FT_Close(self.ftHandle)


def listDevices() -> list[bytes]:
	"""
	Retrieve a list of serial numbers of devices connected to the system.

	:return: List of device serial numbers, as bytes.
	"""
	# Get the number of devices connected.
	n = DWORD()
	FT_ListDevices(byref(n), None, FT_LIST.NUMBER_ONLY)
	if n.value:
		# Per the D2XX programmer's guide, the last entry in the array should be a null pointer
		serialNumbers = (c_char_p * (n.value + 1))()
		for i in range(n.value):
			serialNumbers[i] = cast(create_string_buffer(MAX_SERIAL_NUMBER_SIZE), c_char_p)
		# Request the serial numbers of all connected devices.
		FT_ListDevices(serialNumbers, byref(n), FT_LIST.ALL | FT_OPEN_BY.SERIAL_NUMBER)
		return [ser for ser in serialNumbers[: n.value]]
	else:
		return []


def createDeviceInfoList() -> int:
	"""
	Create the internal device info list.

	:return: The number of entries in the device info list.
	"""
	lpdwNumDevs = DWORD()
	FT_CreateDeviceInfoList(byref(lpdwNumDevs))
	return lpdwNumDevs.value


def getDeviceInfoDetail(index: int = 0) -> DeviceInfo:
	"""
	Get an entry from the internal device info list.

	.. warning::
		You must call :func:`createDeviceInfoList` before calling this function.

	:param index: Index of the device in the device info list, defaults to 0.
	:return: Information about the device at ``index``.
	"""
	dwIndex = DWORD(index)
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


def getDeviceInfoList() -> list[DeviceInfo]:
	"""
	Get information about all FTDI devices connected to the system.

	.. note::
		There is no need to call :func:`createDeviceInfoList` before calling this function.

	:return: A list of dictionaries containing information about each FTDI device connected to the system.
	"""
	numDevs = createDeviceInfoList()
	devInfos = (FT_DEVICE_LIST_INFO_NODE * numDevs)()
	lpdwNumDevs = DWORD()
	FT_GetDeviceInfoList(devInfos, byref(lpdwNumDevs))
	return [
		{
			"Flags": devInfo.Flags,
			"Type": devInfo.Type,
			"ID": devInfo.ID,
			"LocId": devInfo.LocId,
			"SerialNumber": devInfo.SerialNumber,
			"Description": devInfo.Description,
			"ftHandle": devInfo.ftHandle,
		}
		for devInfo in devInfos
	]


def openEx(serial: bytes = b"") -> FTD2XX:
	"""
	Open an FTDI device by serial number.

	.. note::
		Serial numbers can be retrieved with the :func:`getDeviceInfoDetail` or :func:`getDeviceInfoList` functions.

	:param serial: Target device serial number.
	:return: An object that can be used to interact with the device.
	"""
	ftHandle = FT_HANDLE()
	FT_OpenEx(serial, FT_OPEN_BY.SERIAL_NUMBER, byref(ftHandle))
	return FTD2XX(ftHandle)
