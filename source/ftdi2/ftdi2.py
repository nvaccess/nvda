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


################################################
# Start of pythonic functions for specific     #
# functionality around FTDI API                #
################################################
def list_devices():
	"""method to list devices connected.
	total connected and specific serial for a device position"""
	n = DWORD()
	FT_ListDevices(byref(n), None, FT_LIST.NUMBER_ONLY)

	if n.value:
		p_array = (c_char_p * (n.value + 1))()
		for i in range(n.value):
			p_array[i] = cast(create_string_buffer(64), c_char_p)
		FT_ListDevices(p_array, byref(n), FT_LIST.ALL | FT_OPEN_BY.SERIAL_NUMBER)
		return [ser for ser in p_array[: n.value]]
	else:
		return []


# ------------------------------------------------------------------------------
def create_device_info_list():
	"""Create the internal device info list and return number of entries"""
	lpdwNumDevs = DWORD()
	FT_CreateDeviceInfoList(byref(lpdwNumDevs))
	return lpdwNumDevs.value


# ------------------------------------------------------------------------------
def get_device_info_detail(dev=0):
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


# ------------------------------------------------------------------------------
def get_device_info_list():
	num_dev = create_device_info_list()
	dev_info = FT_DEVICE_LIST_INFO_NODE * (num_dev + 1)
	# pDest = pointer(dev_info())
	lpdwNumDevs = DWORD()
	FT_GetDeviceInfoList(dev_info, byref(lpdwNumDevs))

	return_list = []
	# data = pDest.contents
	for i in dev_info:
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
	FT_OpenEx(serial, FT_OPEN_BY.SERIAL_NUMBER, byref(ftHandle))
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
		# FT_SetBaudRate(self.ftHandle, c.c_ulong(dwBaudRate))
		FT_SetBaudRate(self.ftHandle, dwBaudRate)
		return None

	# ------------------------------------------------------------------------------
	def set_timeouts(self, dwReadTimeout=100, dwWriteTimeout=100):
		"""setup timeout times for TX and RX"""
		# FT_SetTimeouts(self.ftHandle, c.c_ulong(dwReadTimeout), c.c_ulong(dwWriteTimeout))
		FT_SetTimeouts(self.ftHandle, dwReadTimeout, dwWriteTimeout)
		return None

	# ------------------------------------------------------------------------------
	def set_latency_timer(self, ucTimer=16):  # added by CJBH
		"""setup latency timer"""
		# FT_SetLatencyTimer(self.ftHandle, c.c_ubyte(ucTimer))
		FT_SetLatencyTimer(self.ftHandle, ucTimer)
		return None

	# ------------------------------------------------------------------------------
	def set_bit_mode(self, ucMask=0, ucMode=0):  # added by CJBH
		"""setup bit mode"""
		# FT_SetBitMode(self.ftHandle, c.c_ubyte(ucMask), c.c_ubyte(ucMode))
		FT_SetBitMode(self.ftHandle, ucMask, ucMode)
		return None

	# ------------------------------------------------------------------------------
	def set_usb_parameters(self, dwInTransferSize=4096, dwOutTransferSize=0):
		"""set the drivers input and output buffer size"""
		# FT_SetUSBParameters(self.ftHandle, c.c_ulong(dwInTransferSize), c.c_ulong(dwOutTransferSize))
		FT_SetUSBParameters(self.ftHandle, dwInTransferSize, dwOutTransferSize)
		return None

	# ------------------------------------------------------------------------------
	def purge(self, to_purge="TXRX"):
		"""purge the in and out buffer of driver.
		Valid arguement = TX,RX,TXRX"""
		if to_purge == "TXRX":
			dwMask = FT_PURGE.RX | FT_PURGE.TX
		elif to_purge == "TX":
			dwMask = FT_PURGE.TX
		elif to_purge == "RX":
			dwMask = FT_PURGE.RX

		FT_Purge(self.ftHandle, dwMask)
		return None

	# ------------------------------------------------------------------------------
	def get_queue_status(self):
		"""returns the number of bytes in the RX buffer
		else raises an exception"""
		lpdwAmountInRxQueue = DWORD()
		FT_GetQueueStatus(self.ftHandle, byref(lpdwAmountInRxQueue))
		return lpdwAmountInRxQueue.value

	# ------------------------------------------------------------------------------
	def write(self, lpBuffer=b""):
		"""writes the bytes-type "data" to the opened port."""
		lpdwBytesWritten = DWORD()
		FT_Write(self.ftHandle, lpBuffer, len(lpBuffer), byref(lpdwBytesWritten))
		return lpdwBytesWritten.value

	# ------------------------------------------------------------------------------
	def read(self, dwBytesToRead, raw=True):
		"""Read in int-type of bytes. Returns either the data
		or raises an exception"""
		lpdwBytesReturned = DWORD()
		lpBuffer = create_string_buffer(dwBytesToRead)
		FT_Read(self.ftHandle, lpBuffer, dwBytesToRead, byref(lpdwBytesReturned))
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
