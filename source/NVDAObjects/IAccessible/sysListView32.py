# -*- coding: UTF-8 -*-
#NVDAObjects/IAccessible/sysListView32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NV Access Limited, Peter Vágner
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
from ctypes import *
from ctypes.wintypes import *
from comtypes import BSTR
import oleacc
import NVDAHelper
import watchdog
import controlTypes
import speech
import api
import eventHandler
import winKernel
import winUser
from . import IAccessible, List
from ..window import Window
import watchdog
from NVDAObjects.behaviors import RowWithoutCellObjects, RowWithFakeNavigation
import config

#Window messages
LVM_FIRST=0x1000
LVM_GETITEMW=LVM_FIRST+75
LVM_GETITEMSTATE=LVM_FIRST+44
LVM_GETFOCUSEDGROUP=LVM_FIRST+93
LVM_GETITEMCOUNT=LVM_FIRST+4
LVM_GETITEM=LVM_FIRST+75
LVN_GETDISPINFO=0xFFFFFF4F
LVM_GETITEMTEXTW=LVM_FIRST+115
LVM_GETHEADER=LVM_FIRST+31
LVM_GETCOLUMNORDERARRAY=LVM_FIRST+59
LVM_GETCOLUMNW=LVM_FIRST+95
LVM_GETSELECTEDCOUNT =(LVM_FIRST+50)
LVNI_SELECTED =2
LVM_GETNEXTITEM =(LVM_FIRST+12)
LVM_GETVIEW=LVM_FIRST+143
LV_VIEW_DETAILS=0x0001
LVM_GETSUBITEMRECT=LVM_FIRST+56
LV_VIEW_TILE=0x0004

#item mask flags
LVIF_TEXT=0x01 
LVIF_IMAGE=0x02
LVIF_PARAM=0x04
LVIF_STATE=0x08
LVIF_INDENT=0x10
LVIF_GROUPID=0x100
LVIF_COLUMNS=0x200

#Item states
LVIS_FOCUSED=0x01
LVIS_SELECTED=0x02
LVIS_STATEIMAGEMASK=0xF000

LVS_REPORT=0x0001
LVS_TYPEMASK=0x0003
LVS_OWNERDRAWFIXED=0x0400

#column mask flags
LVCF_FMT=1
LVCF_WIDTH=2
LVCF_TEXT=4
LVCF_SUBITEM=8
LVCF_IMAGE=16
LVCF_ORDER=32

CBEMAXSTRLEN=260

# listview header window messages
HDM_FIRST=0x1200
HDM_GETITEMCOUNT=HDM_FIRST

class LVITEM(Structure):
	_fields_=[
		('mask',c_uint),
		('iItem',c_int),
		('iSubItem',c_int),
		('state',c_uint),
		('stateMask',c_uint),
		('pszText',c_void_p),
		('cchTextMax',c_int),
		('iImage',c_int),
		('lParam',LPARAM),
		('iIndent',c_int),
		('iGroupID',c_int),
		('cColumns',c_uint),
		('puColumns',c_uint),
		('piColFmt',POINTER(c_int)),
		('iGroup',c_int),
	]

class LVITEM64(Structure):
	_fields_=[
		('mask',c_uint),
		('iItem',c_int),
		('iSubItem',c_int),
		('state',c_uint),
		('stateMask',c_uint),
		('pszText',c_ulonglong),
		('cchTextMax',c_int),
		('iImage',c_int),
		('lParam',c_ulonglong),
		('iIndent',c_int),
		('iGroupID',c_int),
		('cColumns',c_uint),
		('puColumns',c_uint),
		('piColFmt',c_ulonglong),
		('iGroup',c_int),
	]

class LVCOLUMN(Structure):
	_fields_=[
		('mask',c_uint),
		('fmt',c_int),
		('cx',c_int),
		('pszText',c_void_p),
		('cchTextMax',c_int),
		('iSubItem',c_int),
		('iImage',c_int),
		('iOrder',c_int),
		('cxMin',c_int),
		('cxDefault',c_int),
		('cxIdeal',c_int),
	]

class LVCOLUMN64(Structure):
	_fields_=[
		('mask',c_uint),
		('fmt',c_int),
		('cx',c_int),
		('pszText',c_ulonglong),
		('cchTextMax',c_int),
		('iSubItem',c_int),
		('iImage',c_int),
		('iOrder',c_int),
		('cxMin',c_int),
		('cxDefault',c_int),
		('cxIdeal',c_int),
	]

class AutoFreeBSTR(BSTR):
	"""A BSTR that *always* frees itself on deletion.""" 
	_needsfree=True

class List(List):

	def getListGroupInfo(self,groupIndex):
		header=AutoFreeBSTR()
		footer=AutoFreeBSTR()
		state=c_int()
		if watchdog.cancellableExecute(NVDAHelper.localLib.nvdaInProcUtils_sysListView32_getGroupInfo,self.appModule.helperLocalBindingHandle,self.windowHandle,groupIndex,byref(header),byref(footer),byref(state))!=0:
			return None
		return dict(header=header.value,footer=footer.value,state=state.value,groupIndex=groupIndex)

	def _get_name(self):
		name=super(List,self)._get_name()
		if not name:
			name=super(IAccessible,self)._get_name()
		return name

	def event_gainFocus(self):
		#See if this object is the focus and the focus is on a group item.
		#if so, then morph this object to a groupingItem object
		if self is api.getFocusObject():
			groupIndex=watchdog.cancellableSendMessage(self.windowHandle,LVM_GETFOCUSEDGROUP,0,0)
			if groupIndex>=0:
				info=self.getListGroupInfo(groupIndex)
				if info is not None:
					ancestors=api.getFocusAncestors()
					if api.getFocusDifferenceLevel()==len(ancestors)-1:
						self.event_focusEntered()
					groupingObj=GroupingItem(windowHandle=self.windowHandle,parentNVDAObject=self,groupInfo=info)
					return eventHandler.queueEvent("gainFocus",groupingObj)
		return super(List,self).event_gainFocus()

	def _get_isMultiColumn(self):
		view =  watchdog.cancellableSendMessage(self.windowHandle, LVM_GETVIEW, 0, 0)
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

	def _get_columnCount(self):
		if not self.isMultiColumn:
			return 0
		headerHwnd= watchdog.cancellableSendMessage(self.windowHandle,LVM_GETHEADER,0,0)
		count = watchdog.cancellableSendMessage(headerHwnd, HDM_GETITEMCOUNT, 0, 0)
		if not count:
			return 1
		return count

	def _get__columnOrderArray(self):
		coa=(c_int *self.columnCount)()
		processHandle=self.processHandle
		internalCoa=winKernel.virtualAllocEx(processHandle,None,sizeof(coa),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			winKernel.writeProcessMemory(processHandle,internalCoa,byref(coa),sizeof(coa),None)
			res = watchdog.cancellableSendMessage(self.windowHandle,LVM_GETCOLUMNORDERARRAY, self.columnCount, internalCoa)
			if res:
				winKernel.readProcessMemory(processHandle,internalCoa,byref(coa),sizeof(coa),None)
		finally:
			winKernel.virtualFreeEx(processHandle,internalCoa,0,winKernel.MEM_RELEASE)
		return coa

class GroupingItem(Window):

	def __init__(self,windowHandle=None,parentNVDAObject=None,groupInfo=None):
		super(GroupingItem,self).__init__(windowHandle=windowHandle)
		self.parent=parentNVDAObject
		self.groupInfo=groupInfo

	def _isEqual(self,other):
		return isinstance(other,self.__class__) and self.groupInfo==other.groupInfo

	def _set_groupInfo(self,info):
		self._groupInfoTime=time.time()
		self._groupInfo=info
		for gesture in ("kb:leftArrow", "kb:rightArrow"):
			self.bindGesture(gesture, "collapseOrExpand")

	def _get_groupInfo(self):
		now=time.time()
		if (now-self._groupInfoTime)>0.25:
			self._groupInfoTime=now
			self._groupInfo=self.parent.getListGroupInfo(self._groupInfo['groupIndex'])
		return self._groupInfo

	def _get_name(self):
		return self.groupInfo['header']

	role = controlTypes.ROLE_GROUPING

	def _get_value(self):
		return self.groupInfo['footer']

	def _get_states(self):
		states=set()
		if self.groupInfo['state']&1:
			states.add(controlTypes.STATE_COLLAPSED)
		else:
			states.add(controlTypes.STATE_EXPANDED)
		return states

	def script_collapseOrExpand(self,gesture):
		gesture.send()
		eventHandler.queueEvent("stateChange",self)

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
		value=super(ListItemWithoutColumnSupport,self)._get_description()
		if (not value or value.isspace()) and self.windowStyle & LVS_OWNERDRAWFIXED:
			value=self.displayText
		if not value:
			return None
		#Some list view items in Vista can contain annoying left-to-right and right-to-left indicator characters which really should not be there.
		value=value.replace(u'\u200E','')
		value=value.replace(u'\u200F','')
		return value

	def _get_positionInfo(self):
		index=self.IAccessibleChildID
		totalCount=watchdog.cancellableSendMessage(self.windowHandle,LVM_GETITEMCOUNT,0,0)
		return dict(indexInGroup=index,similarItemsInGroup=totalCount) 

	def event_stateChange(self):
		if self.hasFocus:
			super(ListItemWithoutColumnSupport,self).event_stateChange()

class ListItem(RowWithFakeNavigation, RowWithoutCellObjects, ListItemWithoutColumnSupport):

	def _getColumnLocationRaw(self,index):
		processHandle=self.processHandle
		localRect=RECT(left=2,top=index)
		internalRect=winKernel.virtualAllocEx(processHandle,None,sizeof(localRect),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			winKernel.writeProcessMemory(processHandle,internalRect,byref(localRect),sizeof(localRect),None)
			watchdog.cancellableSendMessage(self.windowHandle,LVM_GETSUBITEMRECT, (self.IAccessibleChildID-1), internalRect)
			winKernel.readProcessMemory(processHandle,internalRect,byref(localRect),sizeof(localRect),None)
		finally:
			winKernel.virtualFreeEx(processHandle,internalRect,0,winKernel.MEM_RELEASE)
		windll.user32.ClientToScreen(self.windowHandle,byref(localRect))
		windll.user32.ClientToScreen(self.windowHandle,byref(localRect,8))
		return (localRect.left,localRect.top,localRect.right-localRect.left,localRect.bottom-localRect.top)

	def _getColumnLocation(self,column):
		return self._getColumnLocationRaw(self.parent._columnOrderArray[column - 1])

	def _getColumnContentRaw(self, index):
		buffer=None
		processHandle=self.processHandle
		internalItem=winKernel.virtualAllocEx(processHandle,None,sizeof(self.LVITEM),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			internalText=winKernel.virtualAllocEx(processHandle,None,CBEMAXSTRLEN*2,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			try:
				item=self.LVITEM(iItem=self.IAccessibleChildID-1,mask=LVIF_TEXT|LVIF_COLUMNS,iSubItem=index,pszText=internalText,cchTextMax=CBEMAXSTRLEN)
				winKernel.writeProcessMemory(processHandle,internalItem,byref(item),sizeof(self.LVITEM),None)
				len = watchdog.cancellableSendMessage(self.windowHandle,LVM_GETITEMTEXTW, (self.IAccessibleChildID-1), internalItem)
				if len:
					winKernel.readProcessMemory(processHandle,internalItem,byref(item),sizeof(self.LVITEM),None)
					buffer=create_unicode_buffer(len)
					winKernel.readProcessMemory(processHandle,item.pszText,buffer,sizeof(buffer),None)
			finally:
				winKernel.virtualFreeEx(processHandle,internalText,0,winKernel.MEM_RELEASE)
		finally:
			winKernel.virtualFreeEx(processHandle,internalItem,0,winKernel.MEM_RELEASE)
		return buffer.value if buffer else None

	def _getColumnContent(self, column):
		return self._getColumnContentRaw(self.parent._columnOrderArray[column - 1])

	def _getColumnImageIDRaw(self, index):
		processHandle=self.processHandle
		internalItem=winKernel.virtualAllocEx(processHandle,None,sizeof(self.LVITEM),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			item=self.LVITEM(iItem=self.IAccessibleChildID-1,mask=LVIF_IMAGE|LVIF_COLUMNS,iSubItem=index)
			winKernel.writeProcessMemory(processHandle,internalItem,byref(item),sizeof(self.LVITEM),None)
			item.mask=LVIF_IMAGE|LVIF_COLUMNS
			winKernel.writeProcessMemory(processHandle,internalItem,byref(item),sizeof(self.LVITEM),None)
			watchdog.cancellableSendMessage(self.windowHandle,LVM_GETITEMW, 0, internalItem)
			winKernel.readProcessMemory(processHandle,internalItem,byref(item),sizeof(item),None)
		finally:
			winKernel.virtualFreeEx(processHandle,internalItem,0,winKernel.MEM_RELEASE)
		return item.iImage

	def _getColumnImageID(self, column):
		return self._getColumnImageIDRaw(self.parent._columnOrderArray[column - 1])

	def _getColumnHeaderRaw(self,index):
		buffer=None
		processHandle=self.processHandle
		internalColumn=winKernel.virtualAllocEx(processHandle,None,sizeof(self.LVCOLUMN),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			internalText=winKernel.virtualAllocEx(processHandle,None,CBEMAXSTRLEN*2,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			try:
				column=self.LVCOLUMN(mask=LVCF_TEXT,iSubItem=index,pszText=internalText,cchTextMax=CBEMAXSTRLEN)
				winKernel.writeProcessMemory(processHandle,internalColumn,byref(column),sizeof(self.LVCOLUMN),None)
				res = watchdog.cancellableSendMessage(self.windowHandle,LVM_GETCOLUMNW, index, internalColumn)
				if res:
					winKernel.readProcessMemory(processHandle,internalColumn,byref(column),sizeof(self.LVCOLUMN),None)
					buffer=create_unicode_buffer(column.cchTextMax)
					winKernel.readProcessMemory(processHandle,column.pszText,buffer,sizeof(buffer),None)
			finally:
				winKernel.virtualFreeEx(processHandle,internalText,0,winKernel.MEM_RELEASE)
		finally:
			winKernel.virtualFreeEx(processHandle,internalColumn,0,winKernel.MEM_RELEASE)
		return buffer.value if buffer else None

	def _getColumnHeader(self, column):
		return self._getColumnHeaderRaw(self.parent._columnOrderArray[column - 1])

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
		for col in xrange(1, self.childCount + 1):
			content = self._getColumnContent(col)
			if not content:
				continue
			if config.conf["documentFormatting"]["reportTableHeaders"] and col != 1:
				header = self._getColumnHeader(col)
			else:
				header = None
			if header:
				textList.append("%s: %s" % (header, content))
			else:
				textList.append(content)
		return "; ".join(textList)

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
