#NVDAObjects/sysListView32.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from ctypes import *
from ctypes.wintypes import *
import speech
import winKernel
import winUser
from . import IAccessible

#Window messages
LVM_FIRST=0x1000
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

#Item states
LVIS_FOCUSED=0x01
LVIS_SELECTED=0x02
LVIS_IMAGESTATEMASK=0xF000

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

	def _get_positionString(self):
		totalCount=winUser.sendMessage(self.windowHandle,LVM_GETITEMCOUNT,0,0)
		return _("%s of %s")%(self.IAccessibleChildID,totalCount)

	def oldevent_gainFocus(self):
		speech.speakMessage("%s"%self.lvAppImageID)
		super(self.__class__,self).event_gainFocus()

	def event_stateChange(self):
		if self.hasFocus:
			super(ListItem,self).event_stateChange()
