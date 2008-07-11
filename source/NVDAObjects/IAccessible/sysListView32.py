#NVDAObjects/sysListView32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import controlTypes
import speech
import api
import winKernel
import winUser
from . import IAccessible, List

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
	processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,processID)
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
		return (localHeader.value,localFooter.value,localInfo.state,localInfo.uAlign)
	else:
		return None

class List(List):

	def _get_focusedGroupInfo(self):
		if self is not api.getFocusObject():
			return None
		if not hasattr(self,'_focusedGroupInfo'):
			groupIndex=winUser.sendMessage(self.windowHandle,LVM_GETFOCUSEDGROUP,0,0)
			if groupIndex<0:
				self._focusedGroupInfo=None
			self._focusedGroupInfo=getListGroupInfo(self.windowHandle,groupIndex)
		return self._focusedGroupInfo

	def _get_name(self):
		if self.focusedGroupInfo is not None:
			return self.focusedGroupInfo[0]
		name=super(List,self)._get_name()
		if not name:
			name=super(IAccessible,self)._get_name()
		return name

	def _get_role(self):
		if self.focusedGroupInfo is not None:
			return controlTypes.ROLE_GROUPING
		return super(List,self)._get_role()

	def _get_value(self):
		if self.focusedGroupInfo is not None:
			return self.focusedGroupInfo[1]
		return super(List,self)._get_value()

	def _get_states(self):
		states=super(List,self)._get_states()
		if self.focusedGroupInfo is not None:
			if self.focusedGroupInfo[-2]&1:
				states.add(controlTypes.STATE_COLLAPSED)
			else:
				states.add(controlTypes.STATE_EXPANDED)
		return states

class ListItem(IAccessible):

	def _get_lvAppImageID(self):
		item=LVItemStruct(iItem=self.IAccessibleChildID-1,mask=LVIF_IMAGE)
		(processID,threadID)=winUser.getWindowThreadProcessID(self.windowHandle)
		processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,processID)
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
		return super(ListItem,self)._get_description()

	def _get_positionString(self):
		totalCount=winUser.sendMessage(self.windowHandle,LVM_GETITEMCOUNT,0,0)
		return _("%s of %s")%(self.IAccessibleChildID,totalCount)

	def event_stateChange(self):
		if self.hasFocus:
			super(ListItem,self).event_stateChange()
