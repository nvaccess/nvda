#brailleIo.py
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
from serial.win32 import OVERLAPPED, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE, ERROR_IO_PENDING, CreateFile
import winKernel
import braille
from logHandler import log

LPOVERLAPPED_COMPLETION_ROUTINE = ctypes.WINFUNCTYPE(None, DWORD, DWORD, serial.win32.LPOVERLAPPED)
ERROR_OPERATION_ABORTED = 995

class IoBase(object):
	"""Base class for raw I/O.
	This watches for data of a specified size and calls a callback when it is received.
	"""

	def __init__(self, fileHandle, onReceive, onReceiveSize=1):
		"""Consructr.
		@param fileHandle: A handle to an open I/O device opened for overlapped I/O.
		@param onReceive: A callable taking the received data as its only argument.
		@type onReceive: callable(str)
		@param onReceiveSize: The size (in bytes) of the data with which to call C{onReceive}.
		@type onReceiveSize: int
		"""
		self._file = fileHandle
		self._onReceive = onReceive
		self._readSize = onReceiveSize
		self._readBuf = ctypes.create_string_buffer(onReceiveSize)
		self._readOl = OVERLAPPED()
		self._recvEvt = threading.Event()
		self._ioDoneInst = LPOVERLAPPED_COMPLETION_ROUTINE(self._ioDone)
		# Do the initial read.
		@winKernel.PAPCFUNC
		def init(param):
			self._initApc = None
			self._asyncRead()
		# Ensure the APC stays alive until it runs.
		self._initApc = init
		braille._BgThread.queueApc(init)

	def waitForRead(self, timeout):
		self._recvEvt.wait(timeout)
		self._recvEvt.clear()

	def write(self, data):
		if not ctypes.windll.kernel32.WriteFile(self._file, data, len(data), None, byref(self._writeOl)):
			if ctypes.GetLastError() != ERROR_IO_PENDING:
				raise ctypes.WinError()
			bytes = DWORD()
			ctypes.windll.kernel32.GetOverlappedResult(self._file, byref(self._writeOl), byref(bytes), True)

	def close(self):
		ctypes.windll.kernel32.CancelIoEx(self._file, byref(self._readOl))
		self._onReceive = None

	def __del__(self):
		self.close()

	def _asyncRead(self):
		# Wait for _readSize bytes of data.
		# _ioDone will call onReceive once it is received.
		# onReceive can then optionally read additional bytes if it knows these are coming.
		ctypes.windll.kernel32.ReadFileEx(self._file, self._readBuf, self._readSize, byref(self._readOl), self._ioDoneInst)

	def _ioDone(self, error, bytes, overlapped):
		if error == ERROR_OPERATION_ABORTED:
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
		self._ser = serial.Serial(*args, **kwargs)
		self._origTimeout = self._ser.timeout
		# We don't want a timeout while we're waiting for data.
		self._ser.timeout = None
		self.read = self._ser.read
		self.write = self._ser.write
		self.inWaiting = self._ser.inWaiting
		super(Serial, self).__init__(self._ser.hComPort, onReceive)

	def close(self):
		if not self._ser:
			return
		super(Serial, self).close()
		self._ser.close()

	def _notifyReceive(self, data):
		# Set the timeout for onReceive in case it does a sync read.
		self._ser.timeout = self._origTimeout
		super(Serial, self)._notifyReceive(data)
		self._ser.timeout = None

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
		handle = CreateFile(path, winKernel.GENERIC_READ | winKernel.GENERIC_WRITE,
			0, None, winKernel.OPEN_EXISTING, FILE_FLAG_OVERLAPPED, None)
		if handle == INVALID_HANDLE_VALUE:
			raise ctypes.WinError()
		self._writeOl = OVERLAPPED()
		pd = ctypes.c_void_p()
		if not ctypes.windll.hid.HidD_GetPreparsedData(handle, byref(pd)):
			raise ctypes.WinError()
		caps = HIDP_CAPS()
		ctypes.windll.hid.HidP_GetCaps(pd, byref(caps))
		ctypes.windll.hid.HidD_FreePreparsedData(pd)
		# Reading any less than caps.InputReportByteLength is an error.
		super(Hid, self).__init__(handle, onReceive, onReceiveSize=caps.InputReportByteLength)

	def close(self):
		super(Hid, self).close()
		winKernel.closeHandle(self._file)
