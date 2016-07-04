#hwIo.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015 NV Access Limited

"""Raw input/output for braille displays via serial and HID.
See the L{Serial} and L{Hid} classes.
Braille display drivers must be thread-safe to use this, as it utilises a background thread.
See L{braille.BrailleDisplayDriver.isThreadSafe}.
"""

import threading
import ctypes
from ctypes import byref
from ctypes.wintypes import DWORD, USHORT
import serial
from serial.win32 import MAXDWORD, OVERLAPPED, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE, ERROR_IO_PENDING, COMMTIMEOUTS, CreateFile, SetCommTimeouts
import winKernel
import braille
from logHandler import log
import config

LPOVERLAPPED_COMPLETION_ROUTINE = ctypes.WINFUNCTYPE(None, DWORD, DWORD, serial.win32.LPOVERLAPPED)

def _isDebug():
	return config.conf["debugLog"]["hwIo"]

class IoBase(object):
	"""Base class for raw I/O.
	This watches for data of a specified size and calls a callback when it is received.
	"""

	def __init__(self, fileHandle, onReceive, onReceiveSize=1, writeSize=None):
		"""Constructr.
		@param fileHandle: A handle to an open I/O device opened for overlapped I/O.
		@param onReceive: A callable taking the received data as its only argument.
		@type onReceive: callable(str)
		@param onReceiveSize: The size (in bytes) of the data with which to call C{onReceive}.
		@type onReceiveSize: int
		@param writeSize: The size of the buffer for writes,
			C{None} to use the length of the data written.
		@param writeSize: int or None
		"""
		self._file = fileHandle
		self._onReceive = onReceive
		self._readSize = onReceiveSize
		self._writeSize = writeSize
		self._readBuf = ctypes.create_string_buffer(onReceiveSize)
		self._readOl = OVERLAPPED()
		self._recvEvt = threading.Event()
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

	def waitForRead(self, timeout):
		"""Wait for a chunk of data to be received and processed.
		This will return after L{onReceive} has been called or when the timeout elapses.
		@param timeout: The maximum time to wait in seconds.
		@type timeout: int or float
		@return: C{True} if received data was processed before the timeout,
			C{False} if not.
		@rtype: bool
		"""
		if not self._recvEvt.wait(timeout):
			if _isDebug():
				log.debug("Wait timed out")
			return False
		self._recvEvt.clear()
		return True

	def write(self, data):
		if _isDebug():
			log.debug("Write: %r" % data)
		size = self._writeSize or len(data)
		buf = ctypes.create_string_buffer(size)
		buf.raw = data
		if not ctypes.windll.kernel32.WriteFile(self._file, data, size, None, byref(self._writeOl)):
			if ctypes.GetLastError() != ERROR_IO_PENDING:
				if _isDebug():
					log.debug("Write failed: %s" % ctypes.WinError())
				raise ctypes.WinError()
			bytes = DWORD()
			ctypes.windll.kernel32.GetOverlappedResult(self._file, byref(self._writeOl), byref(bytes), True)

	def close(self):
		if _isDebug():
			log.debug("Closing")
		self._onReceive = None
		ctypes.windll.kernel32.CancelIoEx(self._file, byref(self._readOl))

	def __del__(self):
		self.close()

	def _asyncRead(self):
		# Wait for _readSize bytes of data.
		# _ioDone will call onReceive once it is received.
		# onReceive can then optionally read additional bytes if it knows these are coming.
		ctypes.windll.kernel32.ReadFileEx(self._file, self._readBuf, self._readSize, byref(self._readOl), self._ioDoneInst)

	def _ioDone(self, error, bytes, overlapped):
		if not self._onReceive:
			# close has been called.
			self._ioDone = None
			return
		elif error != 0:
			raise ctypes.WinError(error)
		self._notifyReceive(self._readBuf[:bytes])
		self._recvEvt.set()
		self._asyncRead()

	def _notifyReceive(self, data):
		"""Called when data is received.
		The base implementation just calls the onReceive callback provided to the constructor.
		This can be extended to perform tasks before/after the callback.
		"""
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

	def __init__(self, *args, **kwargs):
		"""Constructor.
		Pass the arguments you would normally pass to L{serial.Serial}.
		There is also one additional keyword argument.
		@param onReceive: A callable taking a byte of received data as its only argument.
			This callable can then call C{read} to get additional data if desired.
		@type onReceive: callable(str)
		"""
		onReceive = kwargs.pop("onReceive")
		self._ser = None
		if _isDebug():
			port = args[0] if len(args) >= 1 else kwargs["port"]
			log.debug("Opening port %s" % port)
		try:
			self._ser = serial.Serial(*args, **kwargs)
		except Exception as e:
			if _isDebug():
				log.debug("Open failed: %s" % e)
			raise
		self._origTimeout = self._ser.timeout
		# We don't want a timeout while we're waiting for data.
		self._setTimeout(None)
		self.inWaiting = self._ser.inWaiting
		super(Serial, self).__init__(self._ser.hComPort, onReceive)

	def read(self, size=1):
		data = self._ser.read(size)
		if _isDebug():
			log.debug("Read: %r" % data)
		return data

	def write(self, data):
		if _isDebug():
			log.debug("Write: %r" % data)
		self._ser.write(data)

	def close(self):
		if not self._ser:
			return
		super(Serial, self).close()
		self._ser.close()

	def _notifyReceive(self, data):
		# Set the timeout for onReceive in case it does a sync read.
		self._setTimeout(self._origTimeout)
		super(Serial, self)._notifyReceive(data)
		self._setTimeout(None)

	def _setTimeout(self, timeout):
		# #6035: pyserial reconfigures all settings of the port when setting a timeout.
		# This can cause error 'Cannot configure port, some setting was wrong.'
		# Therefore, manually set the timeouts using the Win32 API.
		# Adapted from pyserial 3.1.1.
		timeouts = COMMTIMEOUTS()
		if timeout is not None:
			if timeout == 0:
				timeouts.ReadIntervalTimeout = win32.MAXDWORD
			else:
				timeouts.ReadTotalTimeoutConstant = max(int(timeout * 1000), 1)
		if timeout != 0 and self._ser._interCharTimeout is not None:
			timeouts.ReadIntervalTimeout = max(int(self._ser._interCharTimeout * 1000), 1)
		if self._ser._writeTimeout is not None:
			if self._ser._writeTimeout == 0:
				timeouts.WriteTotalTimeoutConstant = win32.MAXDWORD
			else:
				timeouts.WriteTotalTimeoutConstant = max(int(self._ser._writeTimeout * 1000), 1)
		SetCommTimeouts(self._ser.hComPort, ctypes.byref(timeouts))

class HIDP_CAPS (ctypes.Structure):
	_fields_ = (
		("Usage", USHORT),
		("UsagePage", USHORT),
		("InputReportByteLength", USHORT),
		("OutputReportByteLength", USHORT),
		("FeatureReportByteLength", USHORT),
		("Reserved", USHORT * 17),
		("NumberLinkCollectionNodes", USHORT),
		("NumberInputButtonCaps", USHORT),
		("NumberInputValueCaps", USHORT),
		("NumberInputDataIndices", USHORT),
		("NumberOutputButtonCaps", USHORT),
		("NumberOutputValueCaps", USHORT),
		("NumberOutputDataIndices", USHORT),
		("NumberFeatureButtonCaps", USHORT),
		("NumberFeatureValueCaps", USHORT),
		("NumberFeatureDataIndices", USHORT)
	)

class Hid(IoBase):
	"""Raw I/O for HID devices.
	"""

	def __init__(self, path, onReceive):
		"""Constructor.
		@param path: The device path.
			This can be retrieved using L{hwPortUtils.listHidDevices}.
		@type path: unicode
		@param onReceive: A callable taking a received input report as its only argument.
		@type onReceive: callable(str)
		"""
		if _isDebug():
			log.debug("Opening device %s" % path)
		handle = CreateFile(path, winKernel.GENERIC_READ | winKernel.GENERIC_WRITE,
			0, None, winKernel.OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None)
		if handle == INVALID_HANDLE_VALUE:
			if _isDebug():
				log.debug("Open failed: %s" % ctypes.WinError())
			raise ctypes.WinError()
		pd = ctypes.c_void_p()
		if not ctypes.windll.hid.HidD_GetPreparsedData(handle, byref(pd)):
			raise ctypes.WinError()
		caps = HIDP_CAPS()
		ctypes.windll.hid.HidP_GetCaps(pd, byref(caps))
		ctypes.windll.hid.HidD_FreePreparsedData(pd)
		if _isDebug():
			log.debug("Report byte lengths: input %d, output %d, feature %d"
				% (caps.InputReportByteLength, caps.OutputReportByteLength,
					caps.FeatureReportByteLength))
		self._featureSize = caps.FeatureReportByteLength
		# Reading any less than caps.InputReportByteLength is an error.
		# On Windows 7, writing any less than caps.OutputReportByteLength is also an error.
		super(Hid, self).__init__(handle, onReceive,
			onReceiveSize=caps.InputReportByteLength,
			writeSize=caps.OutputReportByteLength)

	def getFeature(self, reportId):
		"""Get a feature report from this device.
		@param reportId: The report id.
		@type reportId: str
		@return: The report, including the report id.
		@rtype: str
		"""
		buf = ctypes.create_string_buffer(self._featureSize)
		buf[0] = reportId
		if not ctypes.windll.hid.HidD_GetFeature(self._file, buf, self._featureSize):
			if _isDebug():
				log.debug("Get feature %r failed: %s"
					% (reportId, ctypes.WinError()))
			raise ctypes.WinError()
		if _isDebug():
			log.debug("Get feature: %r" % buf.raw)
		return buf.raw

	def setFeature(self, report):
		"""Send a feature report to this device.
		@param report: The report, including its id.
		@type report: str
		"""
		length = len(report)
		buf = ctypes.create_string_buffer(length)
		buf.raw = report
		if _isDebug():
			log.debug("Set feature: %r" % report)
		if not ctypes.windll.hid.HidD_SetFeature(self._file, buf, length):
			if _isDebug():
				log.debug("Set feature failed: %s" % ctypes.WinError())
			raise ctypes.WinError()

	def close(self):
		super(Hid, self).close()
		winKernel.closeHandle(self._file)
