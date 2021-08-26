# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2015-2018 NV Access Limited, Babbage B.V.


"""Raw input/output for braille displays via HID
Braille display drivers must be thread-safe to use this, as it utilises a background thread.
See L{braille.BrailleDisplayDriver.isThreadSafe}.
"""

import ctypes
from ctypes import byref
from ctypes.wintypes import USHORT
from typing import Tuple, Callable

from serial.win32 import FILE_FLAG_OVERLAPPED, INVALID_HANDLE_VALUE, CreateFile
import winKernel
from logHandler import log
from .base import IoBase, _isDebug
import hidpi


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
	_reportBuf: "ctypes.Array"

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
		usageList = (hidpi.USAGE * maxUsages)()
		check_HidP_status(
			hidDll.HidP_GetUsages,
			self._reportType,
			hidpi.USAGE(usagePage),
			USHORT(linkCollection),
			ctypes.byref(usageList),
			ctypes.byref(numUsages),
			self._dev._pd,
			self._reportBuf,
			self._reportSize
		)
		return usageList[0:numUsages.value]

	def getDataItems(self):
		maxDataLength = hidDll.HidP_MaxDataListLength(self._reportType, self._dev._pd)
		numDataLength = ctypes.c_ulong(maxDataLength)
		dataList = (hidpi.HIDP_DATA * maxDataLength)()
		check_HidP_status(
			hidDll.HidP_GetData,
			self._reportType,
			dataList,
			ctypes.byref(numDataLength),
			self._dev._pd,
			self._reportBuf,
			self._reportSize
		)
		return dataList[0:numDataLength.value]


class HidOutputReport(HidReport):

	_reportType = hidpi.HIDP_REPORT_TYPE.OUTPUT

	def __init__(self, device, reportID=0):
		self._reportSize = device.caps.OutputReportByteLength
		self._reportBuf = ctypes.c_buffer(self._reportSize)
		self._reportBuf[0] = reportID
		super().__init__(device)

	@property
	def data(self):
		return self._reportBuf.raw

	def setUsageValueArray(self, usagePage, linkCollection, usage, data):
		dataBuf = ctypes.c_buffer(data)
		check_HidP_status(
			hidDll.HidP_SetUsageValueArray,
			self._reportType,
			hidpi.USAGE(usagePage),
			ctypes.c_ushort(linkCollection),
			hidpi.USAGE(usage),
			dataBuf,
			len(dataBuf),
			self._dev._pd,
			self._reportBuf,
			self._reportSize
		)


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
			0 if exclusive else winKernel.FILE_SHARE_READ | winKernel.FILE_SHARE_WRITE,
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
			log.debug("usage ID: 0X%X" % caps.Usage)
			log.debug("usage page: 0X%X" % caps.UsagePage)
			log.debug(
				"Report byte lengths: input %d, output %d, feature %d"
				% (
					caps.InputReportByteLength, caps.OutputReportByteLength, caps.FeatureReportByteLength
				)
			)
		self._featureSize = caps.FeatureReportByteLength
		self._writeSize = caps.OutputReportByteLength
		self._readSize = caps.InputReportByteLength
		# Reading any less than caps.InputReportByteLength is an error.
		super().__init__(
			handle, onReceive, onReceiveSize=caps.InputReportByteLength
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
		valueCapsList = (hidpi.HIDP_VALUE_CAPS * self.caps.NumberInputButtonCaps)()
		numValueCaps = ctypes.c_long(self.caps.NumberInputButtonCaps)
		check_HidP_status(
			hidDll.HidP_GetButtonCaps,
			hidpi.HIDP_REPORT_TYPE.INPUT,
			ctypes.byref(valueCapsList),
			ctypes.byref(numValueCaps),
			self._pd
		)
		self._inputButtonCaps = valueCapsList
		return self._inputButtonCaps

	@property
	def inputValueCaps(self):
		if hasattr(self, '_inputValueCaps'):
			return self._inputValueCaps
		valueCapsList = (hidpi.HIDP_VALUE_CAPS * self.caps.NumberInputValueCaps)()
		numValueCaps = ctypes.c_long(self.caps.NumberInputValueCaps)
		check_HidP_status(
			hidDll.HidP_GetValueCaps,
			hidpi.HIDP_REPORT_TYPE.INPUT,
			ctypes.byref(valueCapsList),
			ctypes.byref(numValueCaps),
			self._pd
		)
		self._inputValueCaps = valueCapsList
		return self._inputValueCaps

	@property
	def outputValueCaps(self):
		if hasattr(self, '_outputValueCaps'):
			return self._outputValueCaps
		valueCapsList = (hidpi.HIDP_VALUE_CAPS * self.caps.NumberOutputValueCaps)()
		numValueCaps = ctypes.c_long(self.caps.NumberOutputValueCaps)
		check_HidP_status(
			hidDll.HidP_GetValueCaps,
			hidpi.HIDP_REPORT_TYPE.OUTPUT,
			ctypes.byref(valueCapsList),
			ctypes.byref(numValueCaps),
			self._pd
		)
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
			log.error("Attempting to send a buffer larger than supported.")
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
				log.debug(
					"Get feature %r failed: %s"
					% (reportId, ctypes.WinError())
				)
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
