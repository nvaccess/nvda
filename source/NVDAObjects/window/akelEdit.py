#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from . import edit
import winUser
import winKernel
import ctypes
import watchdog

# Messages
AEM_GETINDEX          =(winUser.WM_USER + 2106)
AEM_CHARFROMPOS       =(winUser.WM_USER + 2151)
AEM_POSFROMCHAR       =(winUser.WM_USER + 2152)
AEM_INDEXTORICHOFFSET =(winUser.WM_USER + 2112)
AEM_RICHOFFSETTOINDEX =(winUser.WM_USER + 2113)
AEM_CONTROLVERSION        =(winUser.WM_USER + 2200)

#AEM_GETINDEX flags
AEGI_LASTCHAR         =2
AEGI_CARETCHAR             =5
AEGI_NEXTLINE              =24


#Structures

class AELINEDATA(ctypes.Structure):
	pass

AELINEDATA._fields_=[
	('next',ctypes.POINTER(AELINEDATA)),
	('prev',ctypes.POINTER(AELINEDATA)),
	('wpLine',ctypes.c_wchar),
	('nLineLen',ctypes.c_int),
	('nLineBreak',ctypes.c_int),
	('nLineWidth',ctypes.c_int),
	('nSelStart',ctypes.c_int),
	('nSelEnd',ctypes.c_int),
]

class AECHARINDEX(ctypes.Structure):
	_fields_=[
		('nLine',ctypes.c_int),
		('lpLine',AELINEDATA),
		('nCharInLine',ctypes.c_int),
	]


class AkelEditTextInfo(edit.EditTextInfo):

	def _getLineNumFromOffset(self,offset):
		ciChar=AECHARINDEX()
		processHandle=self.obj.processHandle
		internalCiChar=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(ciChar),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			watchdog.cancellableSendMessage(self.obj.windowHandle,AEM_RICHOFFSETTOINDEX,offset,internalCiChar)
			winKernel.readProcessMemory(processHandle,internalCiChar,ctypes.byref(ciChar),ctypes.sizeof(ciChar),None)
		finally:
			winKernel.virtualFreeEx(processHandle,internalCiChar,0,winKernel.MEM_RELEASE)
		return ciChar.nLine

	def _getStoryLength(self):
		ciChar=AECHARINDEX()
		processHandle=self.obj.processHandle
		internalCiChar=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(ciChar),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			watchdog.cancellableSendMessage(self.obj.windowHandle,AEM_GETINDEX,AEGI_LASTCHAR,internalCiChar)
			end=watchdog.cancellableSendMessage(self.obj.windowHandle,AEM_INDEXTORICHOFFSET,0,internalCiChar)
		finally:
			winKernel.virtualFreeEx(processHandle,internalCiChar,0,winKernel.MEM_RELEASE)
		return end+1

	def _getLineOffsets(self,offset):
		(start,end)=super(AkelEditTextInfo,self)._getLineOffsets(offset)
		if end == self._getStoryLength():
			return (start,end)
		ciChar=AECHARINDEX()
		processHandle=self.obj.processHandle
		internalCiChar=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(ciChar),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		try:
			watchdog.cancellableSendMessage(self.obj.windowHandle,AEM_RICHOFFSETTOINDEX,offset,internalCiChar)
			watchdog.cancellableSendMessage(self.obj.windowHandle,AEM_GETINDEX,AEGI_NEXTLINE,internalCiChar)
			end=watchdog.cancellableSendMessage(self.obj.windowHandle,AEM_INDEXTORICHOFFSET,0,internalCiChar)
		finally:
			winKernel.virtualFreeEx(processHandle,internalCiChar,0,winKernel.MEM_RELEASE)
		return (start,end)


class AkelEdit(edit.RichEdit20):

	TextInfo=AkelEditTextInfo

	def initOverlayClass(self):
		global AEGI_NEXTLINE
		version=self._getControlVersion()
		if version <1.6:
			AEGI_NEXTLINE =8
		else:
			AEGI_NEXTLINE =24

		for gesture in ("kb:control+upArrow", "kb:control+downArrow"):
			self.bindGesture(gesture, "caret_moveByLine")

	def _getControlVersion(self):
		res=watchdog.cancellableSendMessage(self.windowHandle,AEM_CONTROLVERSION,None,None)
		major=winUser.LOBYTE(winUser.LOWORD(res))
		minor=winUser.HIBYTE(winUser.LOWORD(res))
		version=major+(0.1*minor)
		return version

