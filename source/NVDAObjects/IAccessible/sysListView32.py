# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Leonard de Ruijter, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import time
from ctypes import *  # noqa: F403
import ctypes
from ctypes.wintypes import *  # noqa: F403
from comtypes import BSTR
import NVDAHelper
import watchdog
import controlTypes
import api
import eventHandler
import winKernel
from . import IAccessible, List
from ..window import Window
from NVDAObjects.behaviors import RowWithoutCellObjects, RowWithFakeNavigation
import config
from config.configFlags import ReportTableHeaders
from locationHelper import RectLTRB
from logHandler import log
from typing import Optional

# Window messages
LVM_FIRST = 0x1000
LVM_GETITEMW = LVM_FIRST + 75
LVM_GETITEMSTATE = LVM_FIRST + 44
LVM_GETFOCUSEDGROUP = LVM_FIRST + 93
LVM_GETITEMCOUNT = LVM_FIRST + 4
LVM_GETITEM = LVM_FIRST + 75
LVN_GETDISPINFO = 0xFFFFFF4F
LVM_GETITEMTEXTW = LVM_FIRST + 115
LVM_GETHEADER = LVM_FIRST + 31
LVM_GETCOLUMNORDERARRAY = LVM_FIRST + 59
LVM_GETCOLUMNW = LVM_FIRST + 95
LVM_GETSELECTEDCOUNT = LVM_FIRST + 50
LVNI_SELECTED = 2
LVM_GETNEXTITEM = LVM_FIRST + 12
LVM_GETVIEW = LVM_FIRST + 143
LV_VIEW_DETAILS = 0x0001
LVM_GETSUBITEMRECT = LVM_FIRST + 56
LV_VIEW_TILE = 0x0004

# item mask flags
LVIF_TEXT = 0x01
LVIF_IMAGE = 0x02
LVIF_PARAM = 0x04
LVIF_STATE = 0x08
LVIF_INDENT = 0x10
LVIF_GROUPID = 0x100
LVIF_COLUMNS = 0x200

# GETSUBITEMRECT flags
# Returns the bounding rectangle of the entire item, including the icon and label
LVIR_BOUNDS = 0
# Returns the bounding rectangle of the icon or small icon.
LVIR_ICON = 1
# Returns the bounding rectangle of the entire item, including the icon and label.
# This is identical to LVIR_BOUNDS.
LVIR_LABEL = 2

# Item states
LVIS_FOCUSED = 0x01
LVIS_SELECTED = 0x02
LVIS_STATEIMAGEMASK = 0xF000

LVS_REPORT = 0x0001
LVS_TYPEMASK = 0x0003
LVS_OWNERDRAWFIXED = 0x0400

# column mask flags
LVCF_FMT = 1
LVCF_WIDTH = 2
LVCF_TEXT = 4
LVCF_SUBITEM = 8
LVCF_IMAGE = 16
LVCF_ORDER = 32

# The size of a buffer to hold text for listview items and columns etc
# #7828: Windows headers define this as 260 characters. However this is not long enough for modern Twitter clients that need at least 280 characters.
# Therefore, round it up to the nearest power of 2
CBEMAXSTRLEN = 512

# listview header window messages
HDM_FIRST = 0x1200
HDM_GETITEMCOUNT = HDM_FIRST


class LVITEM(Structure):  # noqa: F405
	_fields_ = [
		("mask", c_uint),  # noqa: F405
		("iItem", c_int),  # noqa: F405
		("iSubItem", c_int),  # noqa: F405
		("state", c_uint),  # noqa: F405
		("stateMask", c_uint),  # noqa: F405
		("pszText", c_void_p),  # noqa: F405
		("cchTextMax", c_int),  # noqa: F405
		("iImage", c_int),  # noqa: F405
		("lParam", LPARAM),  # noqa: F405
		("iIndent", c_int),  # noqa: F405
		("iGroupID", c_int),  # noqa: F405
		("cColumns", c_uint),  # noqa: F405
		("puColumns", c_uint),  # noqa: F405
		("piColFmt", POINTER(c_int)),  # noqa: F405
		("iGroup", c_int),  # noqa: F405
	]


class LVITEM64(Structure):  # noqa: F405
	_fields_ = [
		("mask", c_uint),  # noqa: F405
		("iItem", c_int),  # noqa: F405
		("iSubItem", c_int),  # noqa: F405
		("state", c_uint),  # noqa: F405
		("stateMask", c_uint),  # noqa: F405
		("pszText", c_ulonglong),  # noqa: F405
		("cchTextMax", c_int),  # noqa: F405
		("iImage", c_int),  # noqa: F405
		("lParam", c_ulonglong),  # noqa: F405
		("iIndent", c_int),  # noqa: F405
		("iGroupID", c_int),  # noqa: F405
		("cColumns", c_uint),  # noqa: F405
		("puColumns", c_uint),  # noqa: F405
		("piColFmt", c_ulonglong),  # noqa: F405
		("iGroup", c_int),  # noqa: F405
	]


class LVCOLUMN(Structure):  # noqa: F405
	_fields_ = [
		("mask", c_uint),  # noqa: F405
		("fmt", c_int),  # noqa: F405
		("cx", c_int),  # noqa: F405
		("pszText", c_void_p),  # noqa: F405
		("cchTextMax", c_int),  # noqa: F405
		("iSubItem", c_int),  # noqa: F405
		("iImage", c_int),  # noqa: F405
		("iOrder", c_int),  # noqa: F405
		("cxMin", c_int),  # noqa: F405
		("cxDefault", c_int),  # noqa: F405
		("cxIdeal", c_int),  # noqa: F405
	]


class LVCOLUMN64(Structure):  # noqa: F405
	_fields_ = [
		("mask", c_uint),  # noqa: F405
		("fmt", c_int),  # noqa: F405
		("cx", c_int),  # noqa: F405
		("pszText", c_ulonglong),  # noqa: F405
		("cchTextMax", c_int),  # noqa: F405
		("iSubItem", c_int),  # noqa: F405
		("iImage", c_int),  # noqa: F405
		("iOrder", c_int),  # noqa: F405
		("cxMin", c_int),  # noqa: F405
		("cxDefault", c_int),  # noqa: F405
		("cxIdeal", c_int),  # noqa: F405
	]


class AutoFreeBSTR(BSTR):
	"""A BSTR that *always* frees itself on deletion.
	A BSTR (Basic string or binary string) is a string data type that is used by COM,
	Automation, and Interop functions.

	AutoFreeBSTR is useful where another library allocates (SysAllocString/SysAllocStringLen)
	and you want to ensure that it will be deallocated (SysFreeString).
	@note The conditions requiring the use of this class are not clear.
		The current usage is considered legacy.
	@note The BSTR (base class) from comtypes will free the string when it
		is from an outparam (indicating that memory was allocated in the library).
	@warning Don't use this unless you are certain about taking ownership of the memory.
	@warning Deprecated, may be removed in future versions.
	"""

	_needsfree = True


class List(List):
	def getListGroupInfo(self, groupIndex):
		header = AutoFreeBSTR()
		footer = AutoFreeBSTR()
		state = c_int()  # noqa: F405
		if (
			watchdog.cancellableExecute(
				NVDAHelper.localLib.nvdaInProcUtils_sysListView32_getGroupInfo,
				self.appModule.helperLocalBindingHandle,
				self.windowHandle,
				groupIndex,
				byref(header),  # noqa: F405
				byref(footer),  # noqa: F405
				byref(state),  # noqa: F405
			)
			!= 0
		):  # noqa: F405
			return None
		return dict(header=header.value, footer=footer.value, state=state.value, groupIndex=groupIndex)

	def _get_name(self):
		name = super(List, self)._get_name()
		if not name:
			name = super(IAccessible, self)._get_name()
		return name

	def event_gainFocus(self):
		# See if this object is the focus and the focus is on a group item.
		# if so, then morph this object to a groupingItem object
		if self is api.getFocusObject():
			groupIndex = watchdog.cancellableSendMessage(self.windowHandle, LVM_GETFOCUSEDGROUP, 0, 0)
			if groupIndex >= 0:
				info = self.getListGroupInfo(groupIndex)
				if info is not None:
					ancestors = api.getFocusAncestors()
					if api.getFocusDifferenceLevel() == len(ancestors) - 1:
						self.event_focusEntered()
					groupingObj = GroupingItem(
						windowHandle=self.windowHandle,
						parentNVDAObject=self,
						groupInfo=info,
					)
					return eventHandler.queueEvent("gainFocus", groupingObj)
		return super(List, self).event_gainFocus()

	def _get_isMultiColumn(self):
		view = watchdog.cancellableSendMessage(self.windowHandle, LVM_GETVIEW, 0, 0)
		if view in (LV_VIEW_DETAILS, LV_VIEW_TILE):
			return True
		elif view == 0:
			# #2673: This could indicate that LVM_GETVIEW is not supported (comctl32 < 6.0).
			# Unfortunately, it could also indicate LV_VIEW_ICON.
			# Hopefully, no one sets LVS_REPORT and then LV_VIEW_ICON.
			return self.windowStyle & LVS_TYPEMASK == LVS_REPORT
		return False

	def _get_rowCount(self):
		return watchdog.cancellableSendMessage(self.windowHandle, LVM_GETITEMCOUNT, 0, 0)

	columnCount: int
	"""Typing information for auto-property: _get_columnCount"""

	def _get_columnCount(self) -> int:
		if not self.isMultiColumn:
			return 0
		headerHwnd = watchdog.cancellableSendMessage(self.windowHandle, LVM_GETHEADER, 0, 0)
		count = watchdog.cancellableSendMessage(headerHwnd, HDM_GETITEMCOUNT, 0, 0)
		if not count:
			return 1
		return count

	def _getColumnOrderArrayRawInProc(self, columnCount: int) -> Optional[ctypes.Array]:
		"""Retrieves a list of column indexes for a given list control.
		See `_getColumnOrderArrayRaw` for more comments.
		Note that this method operates in process and cannot be used in situations where NVDA cannot inject
		i.e when running as a Windows Store application or when no focus event was received on startup.
		"""
		columnOrderArray = (ctypes.c_int * columnCount)()
		res = watchdog.cancellableExecute(
			NVDAHelper.localLib.nvdaInProcUtils_sysListView32_getColumnOrderArray,
			self.appModule.helperLocalBindingHandle,
			self.windowHandle,
			columnCount,
			columnOrderArray,
		)
		if res:
			return None
		return columnOrderArray

	def _getColumnOrderArrayRawOutProc(self, columnCount: int) -> Optional[ctypes.Array]:
		"""Retrieves a list of column indexes for a given list control.
		See `_getColumnOrderArrayRaw` for more comments.
		Note that this method operates out of process and has to reserve memory inside a given application.
		As a consequence it may fail when reserved memory is above the range available
		for 32-bit processes.
		Use only when in process injection is not possible.
		"""
		coa = (ctypes.c_int * columnCount)()
		processHandle = self.processHandle
		internalCoa = winKernel.virtualAllocEx(
			processHandle,
			None,
			sizeof(coa),  # noqa: F405
			winKernel.MEM_COMMIT,
			winKernel.PAGE_READWRITE,  # noqa: F405
		)  # noqa: F405
		try:
			winKernel.writeProcessMemory(processHandle, internalCoa, byref(coa), sizeof(coa), None)  # noqa: F405
			# The meaning of the return value depends on the message sent, for LVM_GETCOLUMNORDERARRAY,
			# it returns nonzero if successful, or 0 otherwise.
			# https://docs.microsoft.com/en-us/windows/win32/controls/lvm-getcolumnorderarray#return-value
			res = watchdog.cancellableSendMessage(
				self.windowHandle,
				LVM_GETCOLUMNORDERARRAY,
				columnCount,
				internalCoa,
			)
			if res:
				winKernel.readProcessMemory(processHandle, internalCoa, byref(coa), sizeof(coa), None)  # noqa: F405
			else:
				coa = None
				log.debugWarning(
					f"LVM_GETCOLUMNORDERARRAY failed for list. "
					f"Windows Error: {ctypes.GetLastError()}, Handle: {self.windowHandle}",
				)
		finally:
			winKernel.virtualFreeEx(processHandle, internalCoa, 0, winKernel.MEM_RELEASE)
		return coa

	def _getColumnOrderArrayRaw(self, columnCount: int) -> Optional[ctypes.Array]:
		"""Retrieves an array of column indexes for a given list.
		The indexes are placed in order in which columns are displayed on screen from left to right.
		Note that when columns are reordered the indexes remain the same - only their order differs.
		"""
		if self.appModule.helperLocalBindingHandle is None:
			return self._getColumnOrderArrayRawOutProc(columnCount)
		return self._getColumnOrderArrayRawInProc(columnCount)

	def _getMappedColumn(self, presentationIndex: int) -> Optional[int]:
		"""
		Multi-column SysListViews can have their columns re-ordered.
		To keep a consistent internal mapping, a column order array is used
		to map a presentation index to a consistent internal index.
		For single-column SysListViews, the mapping is not necessary.
		If the column order array cannot be fetched from a multi-column SysListView,
		this returns None.

		@param presentationIndex: One based index for the column as presented to the user.
		@return: The internal / logical column zero based index for the column.
		None if the mapped column cannot be determined.
		"""
		if presentationIndex == 1 and self.columnCount == 1:
			# Use an implied default column mapping for single column list views
			return 0
		columnOrderArray = self._getColumnOrderArrayRaw(self.columnCount)
		if columnOrderArray is None:
			log.error("Cannot fetch column as column order array is unknown")
			return None
		return columnOrderArray[presentationIndex - 1]


class GroupingItem(Window):
	def __init__(self, windowHandle=None, parentNVDAObject=None, groupInfo=None):
		super(GroupingItem, self).__init__(windowHandle=windowHandle)
		self.parent = parentNVDAObject
		self.groupInfo = groupInfo

	def _isEqual(self, other):
		return isinstance(other, self.__class__) and self.groupInfo == other.groupInfo

	def _set_groupInfo(self, info):
		self._groupInfoTime = time.time()
		self._groupInfo = info
		for gesture in ("kb:leftArrow", "kb:rightArrow"):
			self.bindGesture(gesture, "collapseOrExpand")

	def _get_groupInfo(self):
		now = time.time()
		if (now - self._groupInfoTime) > 0.25:
			self._groupInfoTime = now
			self._groupInfo = self.parent.getListGroupInfo(self._groupInfo["groupIndex"])
		return self._groupInfo

	def _get_name(self):
		return self.groupInfo["header"]

	role = controlTypes.Role.GROUPING

	def _get_value(self):
		return self.groupInfo["footer"]

	def _get_states(self):
		states = set()
		if self.groupInfo["state"] & 1:
			states.add(controlTypes.State.COLLAPSED)
		else:
			states.add(controlTypes.State.EXPANDED)
		return states

	def script_collapseOrExpand(self, gesture):
		gesture.send()
		eventHandler.queueEvent("stateChange", self)


CHAR_LTR_MARK = "\u200e"
CHAR_RTL_MARK = "\u200f"


class ListItemWithoutColumnSupport(IAccessible):
	def initOverlayClass(self):
		if self.appModule.is64BitProcess:
			self.LVITEM = LVITEM64
			self.LVCOLUMN = LVCOLUMN64
		else:
			self.LVITEM = LVITEM
			self.LVCOLUMN = LVCOLUMN

	description = None

	def _get_value(self):
		value = super(ListItemWithoutColumnSupport, self)._get_description()
		if (not value or value.isspace()) and self.windowStyle & LVS_OWNERDRAWFIXED:
			value = self.displayText
		if not value:
			return None
		# Some list view items in Windows Vista and later can contain annoying left-to-right and right-to-left indicator characters which really should not be there.
		return value.replace(CHAR_LTR_MARK, "").replace(CHAR_RTL_MARK, "")

	def _get_positionInfo(self):
		index = self.IAccessibleChildID
		totalCount = watchdog.cancellableSendMessage(self.windowHandle, LVM_GETITEMCOUNT, 0, 0)
		return dict(indexInGroup=index, similarItemsInGroup=totalCount)

	def event_stateChange(self):
		if self.hasFocus:
			super(ListItemWithoutColumnSupport, self).event_stateChange()


class ListItem(RowWithFakeNavigation, RowWithoutCellObjects, ListItemWithoutColumnSupport):
	parent: List

	def _getColumnLocationRawInProc(self, index: int) -> ctypes.wintypes.RECT:
		"""Retrieves rectangle containing coordinates for a given column.
		Note that this method operates in process and cannot be used in situations where NVDA cannot inject
		i.e when running as a Windows Store application or when no focus event was received on startup.
		"""
		item = self.IAccessibleChildID - 1
		subItem = index
		rect = ctypes.wintypes.RECT()
		if (
			watchdog.cancellableExecute(
				NVDAHelper.localLib.nvdaInProcUtils_sysListView32_getColumnLocation,
				self.appModule.helperLocalBindingHandle,
				self.windowHandle,
				item,
				subItem,
				ctypes.byref(rect),
			)
			!= 0
		):
			return None
		return rect

	def _getColumnLocationRawOutProc(self, index: int) -> ctypes.wintypes.RECT:
		"""Retrieves rectangle containing coordinates for a given column.
		Note that this method operates out of process and has to reserve memory inside a given application.
		As a consequence it may fail when reserved memory is above the range available
		for 32-bit processes.
		Use only when in process injection is not possible.
		"""
		processHandle = self.processHandle
		# LVM_GETSUBITEMRECT requires a pointer to a RECT structure that will receive the subitem bounding rectangle information.
		localRect = RECT(  # noqa: F405
			# Returns the bounding rectangle of the entire item, including the icon and label.
			left=LVIR_LABEL,
			# According to Microsoft, top should be the one-based index of the subitem.
			# However, indexes coming from LVM_GETCOLUMNORDERARRAY are zero based.
			top=index,
		)
		internalRect = winKernel.virtualAllocEx(
			processHandle,
			None,
			sizeof(localRect),  # noqa: F405
			winKernel.MEM_COMMIT,
			winKernel.PAGE_READWRITE,  # noqa: F405
		)  # noqa: F405
		try:
			winKernel.writeProcessMemory(
				processHandle,
				internalRect,
				byref(localRect),  # noqa: F405
				sizeof(localRect),  # noqa: F405
				None,  # noqa: F405
			)  # noqa: F405
			res = watchdog.cancellableSendMessage(
				self.windowHandle,
				LVM_GETSUBITEMRECT,
				self.IAccessibleChildID - 1,
				internalRect,
			)
			if res:
				winKernel.readProcessMemory(
					processHandle,
					internalRect,
					ctypes.byref(localRect),
					ctypes.sizeof(localRect),
					None,
				)
		finally:
			winKernel.virtualFreeEx(processHandle, internalRect, 0, winKernel.MEM_RELEASE)
		if res == 0:
			log.debugWarning(f"LVM_GETSUBITEMRECT failed for index {index} in list")
			return None
		return localRect

	def _getColumnLocationRaw(self, index: int) -> Optional[RectLTRB]:
		if not self.appModule.helperLocalBindingHandle:
			rect = self._getColumnLocationRawOutProc(index)
		else:
			rect = self._getColumnLocationRawInProc(index)
		if rect is None:
			return None
		# #8268: this might be a malformed rectangle
		# (i.e. with a left coordinate that is greater than the right coordinate).
		# This happens in Becky! Internet Mail,
		# as well in applications that expose zero width columns.
		left = rect.left
		top = rect.top
		right = rect.right
		bottom = rect.bottom
		if left > right:
			left = right
		if top > bottom:
			top = bottom
		return RectLTRB(left, top, right, bottom).toScreen(self.windowHandle).toLTWH()

	def _getColumnLocation(self, column: int) -> Optional[RectLTRB]:
		mappedColumn = self.parent._getMappedColumn(column)
		if mappedColumn is None:
			return None
		return self._getColumnLocationRaw(mappedColumn)

	def _getColumnContentRawInProc(self, index: int) -> Optional[str]:
		"""Retrieves text for a given column.
		Note that this method operates in process and cannot be used in situations where NVDA cannot inject
		i.e when running as a Windows Store application or when no focus event was received on startup.
		"""
		item = self.IAccessibleChildID - 1
		subItem = index
		text = AutoFreeBSTR()
		if (
			watchdog.cancellableExecute(
				NVDAHelper.localLib.nvdaInProcUtils_sysListView32_getColumnContent,
				self.appModule.helperLocalBindingHandle,
				self.windowHandle,
				item,
				subItem,
				ctypes.byref(text),
			)
			!= 0
		):
			return None
		return text.value

	def _getColumnContentRawOutProc(self, index: int) -> Optional[str]:
		"""Retrieves text for a given column.
		Note that this method operates out of process and has to reserve memory inside a given application.
		As a consequence it may fail when reserved memory is above the range available
		for 32-bit processes.
		Use only when in process injection is not possible.
		"""
		buffer = None
		processHandle = self.processHandle
		internalItem = winKernel.virtualAllocEx(
			processHandle,
			None,
			sizeof(self.LVITEM),  # noqa: F405
			winKernel.MEM_COMMIT,
			winKernel.PAGE_READWRITE,  # noqa: F405
		)  # noqa: F405
		try:
			internalText = winKernel.virtualAllocEx(
				processHandle,
				None,
				CBEMAXSTRLEN * 2,
				winKernel.MEM_COMMIT,
				winKernel.PAGE_READWRITE,
			)
			try:
				item = self.LVITEM(
					iItem=self.IAccessibleChildID - 1,
					mask=LVIF_TEXT | LVIF_COLUMNS,
					iSubItem=index,
					pszText=internalText,
					cchTextMax=CBEMAXSTRLEN,
				)
				winKernel.writeProcessMemory(
					processHandle,
					internalItem,
					byref(item),  # noqa: F405
					sizeof(self.LVITEM),  # noqa: F405
					None,  # noqa: F405
				)  # noqa: F405
				len = watchdog.cancellableSendMessage(
					self.windowHandle,
					LVM_GETITEMTEXTW,
					(self.IAccessibleChildID - 1),
					internalItem,
				)
				if len:
					winKernel.readProcessMemory(
						processHandle,
						internalItem,
						byref(item),  # noqa: F405
						sizeof(self.LVITEM),  # noqa: F405
						None,  # noqa: F405
					)  # noqa: F405
					buffer = create_unicode_buffer(len)  # noqa: F405
					winKernel.readProcessMemory(processHandle, item.pszText, buffer, sizeof(buffer), None)  # noqa: F405
			finally:
				winKernel.virtualFreeEx(processHandle, internalText, 0, winKernel.MEM_RELEASE)
		finally:
			winKernel.virtualFreeEx(processHandle, internalItem, 0, winKernel.MEM_RELEASE)
		return buffer.value if buffer else None

	def _getColumnContentRaw(self, index: int) -> Optional[str]:
		if not self.appModule.helperLocalBindingHandle:
			return self._getColumnContentRawOutProc(index)
		return self._getColumnContentRawInProc(index)

	def _getColumnContent(self, column: int) -> Optional[str]:
		mappedColumn = self.parent._getMappedColumn(column)
		if mappedColumn is None:
			return None
		return self._getColumnContentRaw(mappedColumn)

	def _getColumnImageIDRaw(self, index):
		processHandle = self.processHandle
		internalItem = winKernel.virtualAllocEx(
			processHandle,
			None,
			sizeof(self.LVITEM),  # noqa: F405
			winKernel.MEM_COMMIT,
			winKernel.PAGE_READWRITE,  # noqa: F405
		)  # noqa: F405
		try:
			item = self.LVITEM(
				iItem=self.IAccessibleChildID - 1,
				mask=LVIF_IMAGE | LVIF_COLUMNS,
				iSubItem=index,
			)
			winKernel.writeProcessMemory(processHandle, internalItem, byref(item), sizeof(self.LVITEM), None)  # noqa: F405
			item.mask = LVIF_IMAGE | LVIF_COLUMNS
			winKernel.writeProcessMemory(processHandle, internalItem, byref(item), sizeof(self.LVITEM), None)  # noqa: F405
			watchdog.cancellableSendMessage(self.windowHandle, LVM_GETITEMW, 0, internalItem)
			winKernel.readProcessMemory(processHandle, internalItem, byref(item), sizeof(item), None)  # noqa: F405
		finally:
			winKernel.virtualFreeEx(processHandle, internalItem, 0, winKernel.MEM_RELEASE)
		return item.iImage

	def _getColumnImageID(self, column):
		mappedColumn = self.parent._getMappedColumn(column)
		if mappedColumn is None:
			return None
		return self._getColumnImageIDRaw(mappedColumn)

	def _getColumnHeaderRawOutProc(self, index: int) -> Optional[str]:
		"""Retrieves text of the header for the given column.
		Note that this method operates out of process and has to reserve memory inside a given application.
		As a consequence it may fail when reserved memory is above the range available
		for 32-bit processes.
		Use only when in process injection is not possible.
		"""
		buffer = None
		processHandle = self.processHandle
		internalColumn = winKernel.virtualAllocEx(
			processHandle,
			None,
			sizeof(self.LVCOLUMN),  # noqa: F405
			winKernel.MEM_COMMIT,
			winKernel.PAGE_READWRITE,  # noqa: F405
		)  # noqa: F405
		try:
			internalText = winKernel.virtualAllocEx(
				processHandle,
				None,
				CBEMAXSTRLEN * 2,
				winKernel.MEM_COMMIT,
				winKernel.PAGE_READWRITE,
			)
			try:
				column = self.LVCOLUMN(
					mask=LVCF_TEXT,
					iSubItem=index,
					pszText=internalText,
					cchTextMax=CBEMAXSTRLEN,
				)
				winKernel.writeProcessMemory(
					processHandle,
					internalColumn,
					byref(column),  # noqa: F405
					sizeof(self.LVCOLUMN),  # noqa: F405
					None,  # noqa: F405
				)  # noqa: F405
				res = watchdog.cancellableSendMessage(
					self.windowHandle,
					LVM_GETCOLUMNW,
					index,
					internalColumn,
				)
				if res:
					winKernel.readProcessMemory(
						processHandle,
						internalColumn,
						byref(column),  # noqa: F405
						sizeof(self.LVCOLUMN),  # noqa: F405
						None,  # noqa: F405
					)  # noqa: F405
					buffer = create_unicode_buffer(column.cchTextMax)  # noqa: F405
					winKernel.readProcessMemory(processHandle, column.pszText, buffer, sizeof(buffer), None)  # noqa: F405
			finally:
				winKernel.virtualFreeEx(processHandle, internalText, 0, winKernel.MEM_RELEASE)
		finally:
			winKernel.virtualFreeEx(processHandle, internalColumn, 0, winKernel.MEM_RELEASE)
		return buffer.value if buffer else None

	def _getColumnHeaderRawInProc(self, index: int) -> Optional[str]:
		"""Retrieves text of the header for the given column.
		Note that this method operates in process and cannot be used in situations where NVDA cannot inject
		i.e when running as a Windows Store application or when no focus event was received on startup.
		"""
		subItem = index
		text = AutoFreeBSTR()
		if (
			watchdog.cancellableExecute(
				NVDAHelper.localLib.nvdaInProcUtils_sysListView32_getColumnHeader,
				self.appModule.helperLocalBindingHandle,
				self.windowHandle,
				subItem,
				ctypes.byref(text),
			)
			!= 0
		):
			return None
		return text.value

	def _getColumnHeaderRaw(self, index: int) -> Optional[str]:
		if not self.appModule.helperLocalBindingHandle:
			return self._getColumnHeaderRawOutProc(index)
		return self._getColumnHeaderRawInProc(index)

	def _getColumnHeader(self, column: int) -> Optional[str]:
		mappedColumn = self.parent._getMappedColumn(column)
		if mappedColumn is None:
			return None
		return self._getColumnHeaderRaw(mappedColumn)

	def _get_name(self):
		parent = self.parent
		if not isinstance(parent, List) or not parent.isMultiColumn or self._shouldDisableMultiColumn:
			name = super(ListItem, self).name
			if name:
				return name
			elif self.windowStyle & LVS_OWNERDRAWFIXED:
				return self.displayText
			return name
		textList = []
		for col in range(1, self.childCount + 1):
			location = self._getColumnLocation(col)
			if location and location.width == 0:
				continue
			content = self._getColumnContent(col)
			if not content:
				continue
			if (
				config.conf["documentFormatting"]["reportTableHeaders"]
				in (
					ReportTableHeaders.ROWS_AND_COLUMNS,
					ReportTableHeaders.COLUMNS,
				)
				and col != 1
			):
				header = self._getColumnHeader(col)
			else:
				header = None
			if header:
				textList.append("%s: %s" % (header, content))
			else:
				textList.append(content)
		name = "; ".join(textList)
		# Some list view items in Windows Vista and later can contain annoying left-to-right and right-to-left
		# indicator characters which really should not be there.
		return name.replace(CHAR_LTR_MARK, "").replace(CHAR_RTL_MARK, "")

	value = None

	def _get__shouldDisableMultiColumn(self):
		if self.windowStyle & LVS_OWNERDRAWFIXED:
			# This is owner drawn, but there may still be column content.
			# accDescription will be empty if there is no column content,
			# in which case multi-column support must be disabled.
			ret = not super(ListItemWithoutColumnSupport, self).description
			if ret:
				self.childCount = 0
		else:
			ret = False
		self._shouldDisableMultiColumn = ret
		return ret
