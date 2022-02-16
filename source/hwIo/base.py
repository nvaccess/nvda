# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2018 NV Access Limited, Babbage B.V.


"""Raw input/output for braille displays via serial and HID.
See the L{Serial} and L{Hid} classes.
Braille display drivers must be thread-safe to use this, as it utilises a background thread.
See L{braille.BrailleDisplayDriver.isThreadSafe}.
"""

import sys
import ctypes
from ctypes import byref
from ctypes.wintypes import DWORD
from typing import Optional, Any, Union, Tuple, Callable

import serial
from serial.win32 import OVERLAPPED, FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE, ERROR_IO_PENDING, COMMTIMEOUTS, CreateFile, SetCommTimeouts
import winKernel
import braille
from logHandler import log
import config
import time

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
			onReceiveSize: int = 1,
			onReadError: Optional[Callable[[int], bool]] = None
	):
		"""Constructor.
		@param fileHandle: A handle to an open I/O device opened for overlapped I/O.
			If L{writeFileHandle} is specified, this is only for input.
			The serial implementation uses a _port_handle member for this argument.
		@param onReceive: A callable taking the received data as its only argument.
		@param writeFileHandle: A handle to an open output device opened for overlapped I/O.
		@param onReceiveSize: The size (in bytes) of the data with which to call C{onReceive}.
		@param onReadError: If provided, a callback that takes the error code for a failed read
		  and returns True if the I/O loop should exit cleanly or False if an
		  exception should be thrown
		"""
		self._file = fileHandle
		self._onReceive = onReceive
		self._writeFile = writeFileHandle if writeFileHandle is not None else fileHandle
		self._readSize = onReceiveSize
		self._onReadError = onReadError
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
			if not self._onReadError or not self._onReadError(error):
				raise ctypes.WinError(error)
			else:
				self._ioDone = None
				return
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


class Bulk(IoBase):
	"""Raw I/O for bulk USB devices.
	This implementation assumes that the used Bulk device has two separate end points for input and output.
	"""

	def __init__(
			self, path: str, epIn: int, epOut: int,
			onReceive: Callable[[bytes], None],
			onReceiveSize: int = 1,
			onReadError: Optional[Callable[[int], bool]] = None
	):
		"""Constructor.
		@param path: The device path.
		@param epIn: The endpoint to read data from.
		@param epOut: The endpoint to write data to.
		@param onReceive: A callable taking a received input report as its only argument.
		@param onReadError: An optional callable that handles read errors.
		  It takes an error code and returns True if the error has been handled,
		  allowing the read loop to exit cleanly, or False if an exception should be thrown.
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
		                           writeFileHandle=writeHandle, onReceiveSize=onReceiveSize,
		                           onReadError=onReadError)

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
