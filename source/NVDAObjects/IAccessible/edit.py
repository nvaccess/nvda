#NVDAObjects/Edit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import locale
import struct
import ctypes
import speech
import debug
import winKernel
import winUser
import text
from keyUtils import key
import IAccessibleHandler
from . import IAccessible
from .. import NVDAObjectTextInfo

#Edit control window messages
EM_GETSEL=176
EM_SETSEL=177
EM_GETLINE=196
EM_GETLINECOUNT=186
EM_LINEFROMCHAR=201
EM_LINEINDEX=187
EM_LINELENGTH=193
EM_POSFROMCHAR=214 
EM_CHARFROMPOS=215
EM_GETFIRSTVISIBLELINE=0x0ce
#Rich edit messages
EM_EXGETSEL=winUser.WM_USER+52
EM_EXLINEFROMCHAR=winUser.WM_USER+54
EM_EXSETSEL=winUser.WM_USER+55
EM_GETCHARFORMAT=winUser.WM_USER+58
EM_GETPARAFORMAT=winUser.WM_USER+61
EM_GETTEXTRANGE=winUser.WM_USER+75
EM_FINDWORDBREAK=winUser.WM_USER+76
#Rich edit 2.0 messages
EM_GETTEXTEX=winUser.WM_USER+94
EM_GETTEXTLENGTHEX=winUser.WM_USER+95
#Rich edit 4.0 messages
EM_GETPAGE=winUser.WM_USER+228

#structures
class CharRangeStruct(ctypes.Structure):
	_fields_=[
		('cpMin',ctypes.c_long),
		('cpMax',ctypes.c_long),
	]

class TextRangeStruct(ctypes.Structure):
	_fields_=[
		('chrg',CharRangeStruct),
		('lpstrText',ctypes.c_wchar_p),
	]

class getTextExStruct(ctypes.Structure):
	_fields_=[
		('cb',ctypes.wintypes.DWORD),
		('flags',ctypes.wintypes.DWORD),
		('codepage',ctypes.c_uint),
		('lpDefaultChar',ctypes.wintypes.LPCSTR),
		('lpUsedDefChar',ctypes.c_void_p),
	]

class getTextLengthExStruct(ctypes.Structure):
	_fields_=[
		('flags',ctypes.wintypes.DWORD),
		('codepage',ctypes.c_uint),
	]

#getTextEx flags
GT_DEFAULT=0
GT_USECRLF=1
GT_SELECTION=2
GT_RAWTEXT=4
GT_NOHIDDENTEXT=8

#getTextLengthEx flags
GTL_DEFAULT=0
GTL_USECRLF=1
GTL_PRECISE=2
GTL_CLOSE=4
GTL_NUMCHARS=8
GTL_NUMBYTES=16

#findWordbreak constants
WB_CLASSIFY=3
WB_MOVEWORDLEFT=4
WB_MOVEWORDRIGHT=5
WB_LEFTBREAK=6
WB_RIGHTBREAK=7

class EditTextInfo(NVDAObjectTextInfo):

	def _getSelectionOffsets(self):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ,False,self.obj.windowProcessID)
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winUser.sendMessage(self.obj.windowHandle,EM_EXGETSEL,0, internalCharRange)
			winKernel.readProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
			return (charRange.cpMin,charRange.cpMax)
		else:
			long=winUser.sendMessage(self.obj.windowHandle,EM_GETSEL,0,0)
			return (winUser.LOWORD(long),winUser.HIWORD(long))

	def _setSelectionOffsets(self,start,end):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			charRange.cpMin=start
			charRange.cpMax=end
			processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,self.obj.windowProcessID)
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			winUser.sendMessage(self.obj.windowHandle,EM_EXSETSEL,0, internalCharRange)
			winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
		else:
			winUser.sendMessage(self.obj.windowHandle,EM_SETSEL,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryText(self):
		if not hasattr(self,'_storyText'):
			self._storyText=self.obj.windowText
		return self._storyText

	def _getStoryLength(self):
		if hasattr(self,'_storyLength'):
			return self._storyLength
		if self.obj.editAPIVersion>=2:
			info=getTextLengthExStruct()
			info.flags=GTL_NUMCHARS
			if self.obj.editAPIUnicode:
				info.codepage=1200
			else:
				info.codepage=0
			processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,self.obj.windowProcessID)
			internalInfo=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(info),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalInfo,ctypes.byref(info),ctypes.sizeof(info),None)
			textLen=winUser.sendMessage(self.obj.windowHandle,EM_GETTEXTLENGTHEX,internalInfo,0)
			winKernel.virtualFreeEx(processHandle,internalInfo,0,winKernel.MEM_RELEASE)
			self._storyLength=textLen+1
		else:
			self._storyLength=winUser.sendMessage(self.obj.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)+1
		return self._storyLength

	def _getLineCount(self):
		return winUser.sendMessage(self.obj.windowHandle,EM_GETLINECOUNT,0,0)

	def _getTextRange(self,start,end):
		if self.obj.editAPIVersion>=2:
			bufLen=(end-start)+1
			if self.obj.editAPIUnicode:
				bufLen*=2
			textRange=TextRangeStruct()
			textRange.chrg.cpMin=start
			textRange.chrg.cpMax=end
			processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,self.obj.windowProcessID)
			internalBuf=winKernel.virtualAllocEx(processHandle,None,bufLen,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			textRange.lpstrText=internalBuf
			internalTextRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(textRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalTextRange,ctypes.byref(textRange),ctypes.sizeof(textRange),None)
			winUser.sendMessage(self.obj.windowHandle,EM_GETTEXTRANGE,0,internalTextRange)
			winKernel.virtualFreeEx(processHandle,internalTextRange,0,winKernel.MEM_RELEASE)
			if self.obj.editAPIUnicode:
				buf=ctypes.create_unicode_buffer(bufLen)
			else:
				buf=ctypes.create_string_buffer(bufLen)
			winKernel.readProcessMemory(processHandle,internalBuf,buf,bufLen,None)
			winKernel.virtualFreeEx(processHandle,internalBuf,0,winKernel.MEM_RELEASE)
			if self.obj.editAPIUnicode:
				return buf.value
			else:
				return unicode(buf.value, errors="replace", encoding=locale.getlocale()[1])
		else:
			return self._getStoryText()[start:end]

	def _getWordOffsets(self,offset):
		if self.obj.editAPIVersion>=2:
			start=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDLEFT,offset)
			end=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,start)
			if end<=offset:
				start=end
				end=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,offset)
			return (start,end)
		else:
			return super(EditTextInfo,self)._getWordOffsets(offset)

	def _lineNumFromOffset(self,offset):
		if self.obj.editAPIVersion>=1:
			return winUser.sendMessage(self.obj.windowHandle,EM_EXLINEFROMCHAR,0,offset)
		else:
			return winUser.sendMessage(self.obj.windowHandle,EM_LINEFROMCHAR,offset,0)

	def _getLineOffsets(self,offset):
		lineNum=self._lineNumFromOffset(offset)
		start=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,lineNum,0)
		length=winUser.sendMessage(self.obj.windowHandle,EM_LINELENGTH,offset,0)
		end=start+length
		#If we just seem to get invalid line info, calculate manually
		if start<=0 and end<=0 and lineNum<=0 and self._getLineCount()<=0 and self._getStoryLength()>0:
			return super(EditTextInfo,self)._getLineOffsets(offset)
		#edit controls lye about their line length
		limit=end+4
		while self._lineNumFromOffset(end)==lineNum and end<limit:
			end+=1
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return super(EditTextInfo,self)._getLineOffsets(offset)

class Edit(IAccessible):

	TextInfo=EditTextInfo
	editAPIVersion=0
	editAPIUnicode=True


	def __init__(self,*args,**kwargs):
		super(Edit,self).__init__(*args,**kwargs)
		self.reviewPosition=self.makeTextInfo(text.POSITION_CARET)

	def _get_value(self):
		info=self.makeTextInfo(text.POSITION_CARET)
		info.expand(text.UNIT_LINE)
		return info.text

	def event_valueChange(self):
		pass

[Edit.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("Shift+ExtendedRight","changeSelection"),
	("control+extendedDown","moveByParagraph"),
	("control+extendedUp","moveByParagraph"),
	("Shift+ExtendedLeft","changeSelection"),
	("Shift+ExtendedHome","changeSelection"),
	("Shift+ExtendedEnd","changeSelection"),
	("Shift+ExtendedUp","changeSelection"),
	("Shift+ExtendedDown","changeSelection"),
	("Control+Shift+ExtendedLeft","changeSelection"),
	("Control+Shift+ExtendedRight","changeSelection"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("control+shift+extendedHome","changeSelection"),
	("control+shift+extendedEnd","changeSelection"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
]]

class RichEdit(Edit):
	editAPIVersion=1

class RichEdit20(RichEdit):
	editAPIVersion=2

class RichEdit20A(RichEdit20):
	editAPIUnicode=False


