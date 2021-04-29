#hwIo.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015-2018 NV Access Limited, Babbage B.V.

"""Raw input/output for braille displays via serial and hidpi.
See the L{Serial} and L{Hid} classes.
Braille display drivers must be thread-safe to use this, as it utilises a background thread.
See L{braille.BrailleDisplayDriver.isThreadSafe}.
"""

import sys
import enum
import ctypes
from ctypes import byref
from ctypes.wintypes import DWORD, USHORT, BOOLEAN, ULONG, LONG
from typing import Optional, Any, Union, Tuple, Callable

import serial
from serial.win32 import OVERLAPPED, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE, ERROR_IO_PENDING, COMMTIMEOUTS, CreateFile, SetCommTimeouts
import winKernel
import braille
from logHandler import log
import config
import time
import hidpi

LPOVERLAPPED_COMPLETION_ROUTINE = ctypes.WINFUNCTYPE(None, DWORD, DWORD, serial.win32.LPOVERLAPPED)

def _isDebug():
	return config.conf["debugLog"]["hwIo"]

class IoBase(object):
	"""Base class for raw I/O.
	This watches for data of a specified size and calls a callback when it is received.
	"""

	def __init__(
			self,
			fileHandle: Union[ctypes.wintypes.HANDLE],
			onReceive: Callable[[bytes], None],
			writeFileHandle: Optional[ctypes.wintypes.HANDLE] = None,
			onReceiveSize: int = 1
	):
		"""Constructor.
		@param fileHandle: A handle to an open I/O device opened for overlapped I/O.
			If L{writeFileHandle} is specified, this is only for input.
			The serial implementation uses a _port_handle member for this argument.
		@param onReceive: A callable taking the received data as its only argument.
		@param writeFileHandle: A handle to an open output device opened for overlapped I/O.
		@param onReceiveSize: The size (in bytes) of the data with which to call C{onReceive}.
		"""
		self._file = fileHandle
		self._onReceive = onReceive
		self._writeFile = writeFileHandle if writeFileHandle is not None else fileHandle
		self._readSize = onReceiveSize
		self._readBuf = ctypes.create_string_buffer(onReceiveSize)
		self._readOl = OVERLAPPED()
		self._recvEvt = winKernel.createEvent()
		self._ioDoneInst = LPOVERLAPPED_COMPLETION_ROUTINE(self._ioDone)
		self._writeOl = OVERLAPPED()
		# Do the initial read.
		@winKernel.PAPCFUNC
		def init(param):
			self._initApc = None
			self._asyncRead()
		# Ensure the APC stays alive until it runs.
		self._initApc = init
		braille._BgThread.queueApc(init)

	def waitForRead(self, timeout:Union[int, float]) -> bool:
		"""Wait for a chunk of data to be received and processed.
		This will return after L{onReceive} has been called or when the timeout elapses.
		@param timeout: The maximum time to wait in seconds.
		@return: C{True} if received data was processed before the timeout,
			C{False} if not.
		"""
		timeout= int(timeout*1000)
		while True:
			curTime = time.time()
			res = winKernel.waitForSingleObjectEx(self._recvEvt, timeout, True)
			if res==winKernel.WAIT_OBJECT_0:
				return True
			elif res==winKernel.WAIT_TIMEOUT:
				if _isDebug():
					log.debug("Wait timed out")
				return False
			elif res==winKernel.WAIT_IO_COMPLETION:
				if _isDebug():
					log.debug("Waiting interrupted by completed i/o")
				timeout -= int((time.time()-curTime)*1000)

	def _prepareWriteBuffer(self, data: bytes) -> Tuple[int, ctypes.c_char_p]:
		""" Private helper method to allow derived classes to prepare buffers in different ways"""
		size = len(data)
		return (
			size,
			ctypes.create_string_buffer(data) # this will append a null char, which is intentional
		)

	def write(self, data: bytes):
		if not isinstance(data, bytes):
			raise TypeError("Expected argument 'data' to be of type 'bytes'")
		if _isDebug():
			log.debug("Write: %r" % data)

		size, data = self._prepareWriteBuffer(data)
		if not ctypes.windll.kernel32.WriteFile(self._writeFile, data, size, None, byref(self._writeOl)):
			if ctypes.GetLastError() != ERROR_IO_PENDING:
				if _isDebug():
					log.debug("Write failed: %s" % ctypes.WinError())
				raise ctypes.WinError()
			byteData = DWORD()
			ctypes.windll.kernel32.GetOverlappedResult(self._writeFile, byref(self._writeOl), byref(byteData), True)

	def close(self):
		if _isDebug():
			log.debug("Closing")
		self._onReceive = None
		if hasattr(self, "_file") and self._file is not INVALID_HANDLE_VALUE:
			ctypes.windll.kernel32.CancelIoEx(self._file, byref(self._readOl))
		if hasattr(self, "_writeFile") and self._writeFile not in (self._file, INVALID_HANDLE_VALUE):
			ctypes.windll.kernel32.CancelIoEx(self._writeFile, byref(self._readOl))
		winKernel.closeHandle(self._recvEvt)

	def __del__(self):
		try:
			self.close()
		except AttributeError:
			if _isDebug():
				log.debugWarning("Couldn't delete object gracefully", exc_info=True)

	def _asyncRead(self):
		# Wait for _readSize bytes of data.
		# _ioDone will call onReceive once it is received.
		# onReceive can then optionally read additional bytes if it knows these are coming.
		ctypes.windll.kernel32.ReadFileEx(self._file, self._readBuf, self._readSize, byref(self._readOl), self._ioDoneInst)

	def _ioDone(self, error, numberOfBytes: int, overlapped):
		if not self._onReceive:
			# close has been called.
			self._ioDone = None
			return
		elif error != 0:
			raise ctypes.WinError(error)
		self._notifyReceive(self._readBuf[:numberOfBytes])
		winKernel.kernel32.SetEvent(self._recvEvt)
		self._asyncRead()

	def _notifyReceive(self, data: bytes):
		"""Called when data is received.
		The base implementation just calls the onReceive callback provided to the constructor.
		This can be extended to perform tasks before/after the callback.
		@type data: bytes
		"""
		if not isinstance(data, bytes):
			raise TypeError("Expected argument 'data' to be of type 'bytes'")
		if _isDebug():
			log.debug("Read: %r" % data)
		try:
			self._onReceive(data)
		except:
			log.error("", exc_info=True)

class Serial(IoBase):
	"""Raw I/O for serial devices.
	This extends pyserial to call a callback when data is received.
	"""

	def __init__(
		self,
		*args,
		onReceive: Callable[[bytes], None],
		**kwargs):
		"""Constructor.
		Pass the arguments you would normally pass to L{serial.Serial}.
		There is also one additional required keyword argument.
		@param onReceive: A callable taking a byte of received data as its only argument.
			This callable can then call C{read} to get additional data if desired.
		"""
		self._ser = None
		self.port = args[0] if len(args) >= 1 else kwargs["port"]
		if _isDebug():
			log.debug("Opening port %s" % self.port)
		try:
			self._ser = serial.Serial(*args, **kwargs)
		except Exception as e:
			if _isDebug():
				log.debug("Open failed: %s" % e)
			raise
		self._origTimeout = self._ser.timeout
		# We don't want a timeout while we're waiting for data.
		self._setTimeout(None)
		super(Serial, self).__init__(self._ser._port_handle, onReceive)

	def read(self, size=1) -> bytes:
		data = self._ser.read(size)
		if _isDebug():
			log.debug("Read: %r" % data)
		return data

	def write(self, data: bytes):
		if _isDebug():
			log.debug("Write: %r" % data)
		self._ser.write(data)

	def close(self):
		if not self._ser:
			return
		super(Serial, self).close()
		self._ser.close()

	def _notifyReceive(self, data: bytes):
		# Set the timeout for onReceive in case it does a sync read.
		self._setTimeout(self._origTimeout)
		super(Serial, self)._notifyReceive(data)
		self._setTimeout(None)

	def _setTimeout(self, timeout: Optional[int]):
		# #6035: pyserial reconfigures all settings of the port when setting a timeout.
		# This can cause error 'Cannot configure port, some setting was wrong.'
		# Therefore, manually set the timeouts using the Win32 API.
		# Adapted from pyserial 3.4.
		timeouts = COMMTIMEOUTS()
		if timeout is not None:
			if timeout == 0:
				timeouts.ReadIntervalTimeout = serial.win32.MAXDWORD
			else:
				timeouts.ReadTotalTimeoutConstant = max(int(timeout * 1000), 1)
		if timeout != 0 and self._ser._inter_byte_timeout is not None:
			timeouts.ReadIntervalTimeout = max(int(self._ser._inter_byte_timeout * 1000), 1)
		if self._ser._write_timeout is not None:
			if self._ser._write_timeout == 0:
				timeouts.WriteTotalTimeoutConstant = serial.win32.MAXDWORD
			else:
				timeouts.WriteTotalTimeoutConstant = max(int(self._ser._write_timeout * 1000), 1)
		SetCommTimeouts(self._ser._port_handle, ctypes.byref(timeouts))

hidDll = ctypes.windll.hid

class HidPError(RuntimeError):
	pass

def check_HidP_status(func, *args):
	res = func(*args)
	res = ctypes.c_ulong(res).value
	if res != hidpi.HIDP_STATUS.SUCCESS:
		try:
			code = hidpi.HIDP_STATUS(res)
		except ValueError:
			code = res
		raise HidPError(func.__name__, str(code))


class HidReport:

	_reportType: hidpi.HIDP_REPORT_TYPE
	_reportSize: int
	_reportBuf: "_ctypes.Array"

	def __init__(self, device):
		self._dev = device

class HidInputReport(HidReport):

	_reportType = hidpi.HIDP_REPORT_TYPE.INPUT

	def __init__(self, device, data):
		self._reportSize = device.caps.InputReportByteLength
		self._reportBuf = ctypes.c_buffer(data, size=self._reportSize)
		super().__init__(device)

	def getUsages(self, usagePage, linkCollection=0):
		maxUsages = hidDll.HidP_MaxUsageListLength(self._reportType, hidpi.USAGE(usagePage), self._dev._pd)
		numUsages = ctypes.c_long(maxUsages)
		usageList = (hidpi.USAGE*maxUsages)()
		check_HidP_status(hidDll.HidP_GetUsages,self._reportType, hidpi.USAGE(usagePage), USHORT(linkCollection), ctypes.byref(usageList), ctypes.byref(numUsages), self._dev._pd, self._reportBuf, self._reportSize)
		return usageList[0:numUsages.value]

	def getDataItems(self):
		maxDataLength = hidDll.HidP_MaxDataListLength (self._reportType, self._dev._pd)
		numDataLength = ctypes.c_ulong(maxDataLength)
		dataList = (hidpi.HIDP_DATA*maxDataLength)()
		check_HidP_status(hidDll.HidP_GetData, self._reportType, dataList, ctypes.byref(numDataLength), self._dev._pd, self._reportBuf, self._reportSize)
		return dataList[0:numDataLength.value]


class HidOutputReport(HidReport):

	_reportType = hidpi.HIDP_REPORT_TYPE.OUTPUT

	def __init__(self, device, reportID=0):
		self._reportSize = device.caps.OutputReportByteLength
		self._reportBuf = ctypes.c_buffer(self._reportSize)
		self._reportBuf[0]=reportID
		super().__init__(device)

	@property
	def data(self):
		return self._reportBuf.raw

	def setUsageValueArray(self, usagePage, linkCollection, usage, data):
		dataBuf = ctypes.c_buffer(data)
		check_HidP_status(hidDll.HidP_SetUsageValueArray, self._reportType, hidpi.USAGE(usagePage), ctypes.c_ushort(linkCollection), hidpi.USAGE(usage), dataBuf, len(dataBuf), self._dev._pd, self._reportBuf, self._reportSize)


class Hid(IoBase):
	"""Raw I/O for HID devices.
	"""
	_featureSize: int

	def __init__(self, path: str, onReceive: Callable[[bytes], None], exclusive: bool = True):
		"""Constructor.
		@param path: The device path.
			This can be retrieved using L{hwPortUtils.listHidDevices}.
		@param onReceive: A callable taking a received input report as its only argument.
		@param exclusive: Whether to block other application's access to this device.
		"""
		if _isDebug():
			log.debug("Opening device %s" % path)
		handle = CreateFile(
			path,
			winKernel.GENERIC_READ | winKernel.GENERIC_WRITE,
			0 if exclusive else winKernel.FILE_SHARE_READ|winKernel.FILE_SHARE_WRITE,
				None,
			winKernel.OPEN_EXISTING,
			FILE_FLAG_OVERLAPPED,
			None
		)
		if handle == INVALID_HANDLE_VALUE:
			if _isDebug():
				log.debug("Open failed: %s" % ctypes.WinError())
			raise ctypes.WinError()
		pd = ctypes.c_void_p()
		if not hidDll.HidD_GetPreparsedData(handle, byref(pd)):
			raise ctypes.WinError()
		self._pd = pd
		caps = self.caps
		self.usagePage = caps.UsagePage
		if _isDebug():
			log.debug("usage ID: 0X%X"%caps.Usage)
			log.debug("usage page: 0X%X"%caps.UsagePage)
			log.debug("Report byte lengths: input %d, output %d, feature %d"
				% (caps.InputReportByteLength, caps.OutputReportByteLength,
					caps.FeatureReportByteLength))
		self._featureSize = caps.FeatureReportByteLength
		self._writeSize = caps.OutputReportByteLength
		self._readSize = caps.InputReportByteLength
		# Reading any less than caps.InputReportByteLength is an error.
		super(Hid, self).__init__(handle, onReceive,
			onReceiveSize=caps.InputReportByteLength
		)

	@property
	def caps(self):
		if hasattr(self, '_caps'):
			return self._caps
		caps = hidpi.HIDP_CAPS()
		check_HidP_status(hidDll.HidP_GetCaps, self._pd, byref(caps))
		self._caps = caps
		return self._caps

	@property
	def inputButtonCaps(self):
		if hasattr(self, '_inputButtonCaps'):
			return self._inputButtonCaps
		valueCapsList = (hidpi.HIDP_VALUE_CAPS*self.caps.NumberInputButtonCaps)()
		numValueCaps = ctypes.c_long(self.caps.NumberInputButtonCaps)
		check_HidP_status(hidDll.HidP_GetButtonCaps, hidpi.HIDP_REPORT_TYPE.INPUT, ctypes.byref(valueCapsList), ctypes.byref(numValueCaps), self._pd)
		self._inputButtonCaps = valueCapsList
		return self._inputButtonCaps

	@property
	def inputValueCaps(self):
		if hasattr(self, '_inputValueCaps'):
			return self._inputValueCaps
		valueCapsList = (hidpi.HIDP_VALUE_CAPS*self.caps.NumberInputValueCaps)()
		numValueCaps = ctypes.c_long(self.caps.NumberInputValueCaps)
		log.info("numButtonCaps: %d"%numValueCaps.value)
		check_HidP_status(hidDll.HidP_GetValueCaps, hidpi.HIDP_REPORT_TYPE.INPUT, ctypes.byref(valueCapsList), ctypes.byref(numValueCaps), self._pd)
		self._inputValueCaps = valueCapsList
		return self._inputValueCaps

	@property
	def outputValueCaps(self):
		if hasattr(self, '_outputValueCaps'):
			return self._outputValueCaps
		valueCapsList = (hidpi.HIDP_VALUE_CAPS*self.caps.NumberOutputValueCaps)()
		numValueCaps = ctypes.c_long(self.caps.NumberOutputValueCaps)
		check_HidP_status(hidDll.HidP_GetValueCaps, hidpi.HIDP_REPORT_TYPE.OUTPUT, ctypes.byref(valueCapsList), ctypes.byref(numValueCaps), self._pd)
		self._outputValueCaps = valueCapsList
		return self._outputValueCaps

	def _prepareWriteBuffer(self, data: bytes) -> Tuple[int, ctypes.c_char_p]:
		""" For HID devices, the buffer to be written must match the
		OutputReportByteLength fetched from HIDP_CAPS, to ensure this is the case
		we create a buffer of that size. We also check that data is not bigger than
		the write size, which we do not currently support. If it becomes necessary to
		support this, we could split the data and send it several chunks.
		"""
		# On Windows 7, writing any less than caps.OutputReportByteLength is also an error.
		# See also: http://www.onarm.com/forum/20152/
		if len(data) > self._writeSize:
			log.error(u"Attempting to send a buffer larger than supported.")
			raise RuntimeError("Unable to send buffer of: %d", len(data))
		return (
			self._writeSize,
			ctypes.create_string_buffer(data, self._writeSize)
		)

	def getFeature(self, reportId: bytes) -> bytes:
		"""Get a feature report from this device.
		@param reportId: The report id.
		@return: The report, including the report id.
		"""
		buf = ctypes.create_string_buffer(reportId, size=self._featureSize)
		if not hidDll.HidD_GetFeature(self._file, buf, self._featureSize):
			if _isDebug():
				log.debug("Get feature %r failed: %s"
					% (reportId, ctypes.WinError()))
			raise ctypes.WinError()
		if _isDebug():
			log.debug("Get feature: %r" % buf.raw)
		return buf.raw

	def setFeature(self, report: bytes) -> None:
		"""Send a feature report to this device.
		@param report: The report, including its id.
		"""
		buf = ctypes.create_string_buffer(report, size=len(report))
		bufSize = ctypes.sizeof(buf)
		if _isDebug():
			log.debug("Set feature: %r" % report)
		result = hidDll.HidD_SetFeature(
			self._file,
			buf,
			bufSize
		)
		if not result:
			if _isDebug():
				log.debug("Set feature failed: %s" % ctypes.WinError())
			raise ctypes.WinError()

	def setOutputReport(self, report: bytes) -> None:
		"""
		Write the given report to the device using HidD_SetOutputReport.
		This is instead of using the standard WriteFile which may freeze with some USB HID implementations.
		@param report: The report, including its id.
		"""
		buf = ctypes.create_string_buffer(report, size=len(report))
		bufSize = ctypes.sizeof(buf)
		if _isDebug():
			log.debug("Set output report: %r" % report)
		result = hidDll.HidD_SetOutputReport(
			self._writeFile,
			buf,
			bufSize
		)
		if not result:
			if _isDebug():
				log.debug("Set output report failed: %s" % ctypes.WinError())
			raise ctypes.WinError()

	def close(self):
		super(Hid, self).close()
		winKernel.closeHandle(self._file)
		self._file = None
		hidDll.HidD_FreePreparsedData(self._pd)

class Bulk(IoBase):
	"""Raw I/O for bulk USB devices.
	This implementation assumes that the used Bulk device has two separate end points for input and output.
	"""

	def __init__(
			self, path: str, epIn: int, epOut: int,
			onReceive: Callable[[bytes], None],
			onReceiveSize: int = 1
	):
		"""Constructor.
		@param path: The device path.
		@param epIn: The endpoint to read data from.
		@param epOut: The endpoint to write data to.
		@param onReceive: A callable taking a received input report as its only argument.
		"""
		if _isDebug():
			log.debug("Opening device %s" % path)
		readPath="{path}\\{endpoint}".format(path=path,endpoint=epIn)
		writePath="{path}\\{endpoint}".format(path=path,endpoint=epOut)
		readHandle = CreateFile(readPath, winKernel.GENERIC_READ,
			0, None, winKernel.OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None)
		if readHandle == INVALID_HANDLE_VALUE:
			if _isDebug():
				log.debug("Open read handle failed: %s" % ctypes.WinError())
			raise ctypes.WinError()
		writeHandle = CreateFile(writePath, winKernel.GENERIC_WRITE,
			0, None, winKernel.OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None)
		if writeHandle == INVALID_HANDLE_VALUE:
			if _isDebug():
				log.debug("Open write handle failed: %s" % ctypes.WinError())
			raise ctypes.WinError()
		super(Bulk, self).__init__(readHandle, onReceive,
			writeFileHandle=writeHandle, onReceiveSize=onReceiveSize)

	def close(self):
		super(Bulk, self).close()
		if hasattr(self, "_file") and self._file is not INVALID_HANDLE_VALUE:
			winKernel.closeHandle(self._file)
		if hasattr(self, "_writeFile") and self._writeFile is not INVALID_HANDLE_VALUE:
			winKernel.closeHandle(self._writeFile)


def boolToByte(arg: bool) -> bytes:
	return arg.to_bytes(
		length=1,
		byteorder=sys.byteorder,  # for a single byte big/little endian does not matter.
		signed=False  # Since this represents length, it makes no sense to send a negative value.
	)


def intToByte(arg: int) -> bytes:
	""" Convert an int (value < 256) to a single byte bytes object
	"""
	return arg.to_bytes(
		length=1,  # Will raise if value overflows, eg arg > 255
		byteorder=sys.byteorder,  # for a single byte big/little endian does not matter.
		signed=False  # Since this represents length, it makes no sense to send a negative value.
	)

def getByte(arg: bytes, index: int) -> bytes:
	""" Return the single byte at index"""
	return arg[index:index+1]
