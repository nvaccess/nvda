#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import edit
import IAccessibleHandler
import winUser
import winKernel
import ctypes

# Messages
AEM_GETINDEX          =(winUser.WM_USER + 2106)
AEM_CHARFROMPOS       =(winUser.WM_USER + 2151)
AEM_POSFROMCHAR       =(winUser.WM_USER + 2152)
AEM_INDEXTORICHOFFSET =(winUser.WM_USER + 2112)
AEM_RICHOFFSETTOINDEX =(winUser.WM_USER + 2113)


#AEM_GETINDEX flags
AEGI_LASTCHAR         =2
AEGI_NEXTBREAK        =12
AEGI_PREVBREAK        =13


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
		global ignoreCaretEvents
		ignoreCaretEvents=True
		ciChar=AECHARINDEX()
		processHandle=self.obj.processHandle
		internalCiChar=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(ciChar),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winUser.sendMessage(self.obj.windowHandle,AEM_RICHOFFSETTOINDEX,offset,internalCiChar)
		winKernel.readProcessMemory(processHandle,internalCiChar,ctypes.byref(ciChar),ctypes.sizeof(ciChar),None)
		winKernel.virtualFreeEx(processHandle,internalCiChar,0,winKernel.MEM_RELEASE)
		ignoreCaretEvents=False
		return ciChar.nLine

	def _getStoryLength(self):
		ciChar=AECHARINDEX()
		processHandle=self.obj.processHandle
		internalCiChar=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(ciChar),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winUser.sendMessage(self.obj.windowHandle,AEM_GETINDEX,AEGI_LASTCHAR,internalCiChar)
		end=winUser.sendMessage(self.obj.windowHandle,AEM_INDEXTORICHOFFSET,0,internalCiChar)
		winKernel.virtualFreeEx(processHandle,internalCiChar,0,winKernel.MEM_RELEASE)
		return end+1


class AkelEdit(edit.RichEdit20):

	TextInfo=AkelEditTextInfo

[AkelEdit.bindKey(keyName,scriptName) for keyName,scriptName in [
	("Control+ExtendedUp","moveByLine"),
	("Control+ExtendedDown","moveByLine"),
]]
