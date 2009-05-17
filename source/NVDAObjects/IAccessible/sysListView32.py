#NVDAObjects/sysListView32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
from ctypes import *
from ctypes.wintypes import *
import IAccessibleHandler
import controlTypes
import speech
import api
from keyUtils import sendKey
import eventHandler
import winKernel
import winUser
from . import IAccessible, List
from ..window import Window 

#Window messages
LVM_FIRST=0x1000
LVM_GETFOCUSEDGROUP=LVM_FIRST+93
LVM_GETGROUPINFOBYINDEX=LVM_FIRST+153
LVM_GETITEMCOUNT=LVM_FIRST+4
LVM_GETITEM=LVM_FIRST+75
LVN_GETDISPINFO=0xFFFFFF4F

#item mask flags
LVIF_TEXT=0x01 
LVIF_IMAGE=0x02
LVIF_PARAM=0x04
LVIF_STATE=0x08
LVIF_INDENT=0x10
LVIF_GROUPID=0x100
LVIF_COLUMNS=0x200

#group mask flags
LVGF_HEADER=0x1
LVGF_FOOTER=0x2
LVGF_STATE=0x4
LVGF_ALIGN=0x8
LVGF_GROUPID=0x10

#Item states
LVIS_FOCUSED=0x01
LVIS_SELECTED=0x02
LVIS_IMAGESTATEMASK=0xF000

class LVGROUP(Structure):
	_fields_=[
		('cbSize',c_uint),
		('mask',c_uint),
		('pszHeader',c_void_p),
		('cchHeader',c_int),
		('pszFooter',c_void_p),
		('cchFooter',c_int),
		('iGroupId',c_int),
		('stateMask',c_uint),
		('state',c_uint),
		('uAlign',c_uint),
		('pszSubtitle',c_void_p),
		('cchSubtitle',c_uint),
		('pszTask',c_void_p),
		('cchTask',c_uint),
		('pszDescriptionTop',c_void_p),
		('cchDescriptionTop',c_uint),
		('pszDescriptionBottom',c_void_p),
		('cchDescriptionBottom',c_uint),
		('iTitleImage',c_int),
		('iExtendedImage',c_int),
		('iFirstItem',c_int),
		('cItems',c_uint),
		('pszSubsetTitle',c_void_p),
		('cchSubsetTitle',c_uint),
	]

class LVItemStruct(Structure):
	_fields_=[
		('mask',c_uint),
		('iItem',c_int),
		('iSubItem',c_int),
		('state',c_uint),
		('stateMask',c_uint),
		('text',LPWSTR),
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

class NMLVDispInfoStruct(Structure):
	_fields_=[
		('hdr',winUser.NMHdrStruct),
		('item',c_int),
	]

def getListGroupInfo(windowHandle,groupIndex):
	(processID,threadID)=winUser.getWindowThreadProcessID(windowHandle)
	processHandle=IAccessibleHandler.getProcessHandleFromHwnd(windowHandle)
	localInfo=LVGROUP()
	localInfo.cbSize=sizeof(LVGROUP)
	localInfo.mask=LVGF_HEADER|LVGF_FOOTER|LVGF_STATE|LVGF_ALIGN|LVGF_GROUPID
	localInfo.stateMask=0xffffffff
	remoteInfo=winKernel.virtualAllocEx(processHandle,None,sizeof(LVGROUP),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
	winKernel.writeProcessMemory(processHandle,remoteInfo,byref(localInfo),sizeof(LVGROUP),None)
	messageRes=winUser.sendMessage(windowHandle,LVM_GETGROUPINFOBYINDEX,groupIndex,remoteInfo)
	winKernel.readProcessMemory(processHandle,remoteInfo,byref(localInfo),sizeof(LVGROUP),None)
	winKernel.virtualFreeEx(processHandle,remoteInfo,0,winKernel.MEM_RELEASE)
	localHeader=create_unicode_buffer(localInfo.cchHeader)
	winKernel.readProcessMemory(processHandle,localInfo.pszHeader,localHeader,localInfo.cchHeader*2,None)
	localFooter=create_unicode_buffer(localInfo.cchFooter)
	winKernel.readProcessMemory(processHandle,localInfo.pszFooter,localFooter,localInfo.cchFooter*2,None)
	winKernel.closeHandle(processHandle)
	if messageRes==1:
		return dict(header=localHeader.value,footer=localFooter.value,groupID=localInfo.iGroupId,state=localInfo.state,uAlign=localInfo.uAlign,groupIndex=groupIndex)
	else:
		return None

class List(List):

	def _get_name(self):
		name=super(List,self)._get_name()
		if not name:
			name=super(IAccessible,self)._get_name()
		return name

	def event_gainFocus(self):
		#See if this object is the focus and the focus is on a group item.
		#if so, then morph this object to a groupingItem object
		if self is api.getFocusObject():
			groupIndex=winUser.sendMessage(self.windowHandle,LVM_GETFOCUSEDGROUP,0,0)
			if groupIndex>=0:
				info=getListGroupInfo(self.windowHandle,groupIndex)
				if info is not None:
					ancestors=api.getFocusAncestors()
					if api.getFocusDifferenceLevel()==len(ancestors)-1:
						self.event_focusEntered()
					groupingObj=GroupingItem(self,info)
					return eventHandler.queueEvent("gainFocus",groupingObj)
		return super(List,self).event_gainFocus()

class GroupingItem(Window):

	@classmethod
	def findBestClass(cls, clsList, kwargs):
		# This class can be directly instantiated.
		return (cls,), kwargs

	def __init__(self,parent,groupInfo):
		super(GroupingItem,self).__init__(parent.windowHandle)
		self.parent=parent
		self.groupInfo=groupInfo

	def _isEqual(self,other):
		return isinstance(other,self.__class__) and self.groupInfo==othergroupInfo

	def _set_groupInfo(self,info):
		self._groupInfoTime=time.time()
		self._groupInfo=info

	def _get_groupInfo(self):
		now=time.time()
		if (now-self._groupInfoTime)>0.25:
			self._groupInfoTime=now
			self._groupInfo=getListGroupInfo(self.windowHandle,self._groupInfo['groupIndex'])
		return self._groupInfo

	def _get_name(self):
		return self.groupInfo['header']

	def _get_role(self):
		return controlTypes.ROLE_GROUPING

	def _get_value(self):
		return self.groupInfo['footer']

	def _get_states(self):
		states=set()
		if self.groupInfo['state']&1:
			states.add(controlTypes.STATE_COLLAPSED)
		else:
			states.add(controlTypes.STATE_EXPANDED)
		return states

	def script_collapseOrExpand(self,keyPress):
		sendKey(keyPress)
		self.event_stateChange()

[GroupingItem.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedLeft","collapseOrExpand"),
	("ExtendedRight","collapseOrExpand"),
]]

class ListItem(IAccessible):

	def _get_lvAppImageID(self):
		item=LVItemStruct(iItem=self.IAccessibleChildID-1,mask=LVIF_IMAGE)
		(processID,threadID)=winUser.getWindowThreadProcessID(self.windowHandle)
		processHandle=self.processHandle
		internalItem=winKernel.virtualAllocEx(processHandle,None,sizeof(LVItemStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winKernel.writeProcessMemory(processHandle,internalItem,byref(item),sizeof(LVItemStruct),None)
		winUser.sendMessage(self.windowHandle,LVM_GETITEM,0,internalItem)
		dispInfo=NMLVDispInfoStruct()
		dispInfo.item=internalItem
		dispInfo.hdr.hwndFrom=self.windowHandle
		dispInfo.hdr.idFrom=self.windowControlID
		dispInfo.hdr.code=LVN_GETDISPINFO
		internalDispInfo=winKernel.virtualAllocEx(processHandle,None,sizeof(NMLVDispInfoStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winKernel.writeProcessMemory(processHandle,internalDispInfo,byref(dispInfo),sizeof(NMLVDispInfoStruct),None)
		winUser.sendMessage(self.parent.parent.windowHandle,winUser.WM_NOTIFY,LVN_GETDISPINFO,internalDispInfo)
		winKernel.virtualFreeEx(processHandle,internalDispInfo,0,winKernel.MEM_RELEASE)
		winKernel.readProcessMemory(processHandle,internalItem,byref(item),sizeof(LVItemStruct),None)
		winKernel.virtualFreeEx(processHandle,internalItem,0,winKernel.MEM_RELEASE)
		return item.iImage

	def _get_description(self):
		return None

	def _get_value(self):
		value=super(ListItem,self)._get_description()
		if not value:
			return None
		#Some list view items in Vista can contain annoying left-to-right and right-to-left indicator characters which really should not be there.
		value=value.replace(u'\u200E','')
		value=value.replace(u'\u200F','')
		return value

	def _get_positionInfo(self):
		info=super(ListItem,self)._get_positionInfo()
		totalCount=winUser.sendMessage(self.windowHandle,LVM_GETITEMCOUNT,0,0)
		info['similarItemsInGroup']=totalCount
		return info

	def event_stateChange(self):
		if self.hasFocus:
			super(ListItem,self).event_stateChange()
