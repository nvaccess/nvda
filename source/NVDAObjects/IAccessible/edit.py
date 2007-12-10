#NVDAObjects/Edit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import locale
import comtypes.client
import struct
import ctypes
import pythoncom
import win32clipboard
import oleTypes
import queueHandler
import globalVars
import speech
import winKernel
import api
import winUser
import textHandler
from keyUtils import key, sendKey, isKeyWaiting
import IAccessibleHandler
import controlTypes
from . import IAccessible
from .. import NVDAObjectTextInfo

ignoreCaretEvents=False

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

LF_FACESIZE=32

#structures

class PointLStruct(ctypes.Structure):
 	_fields_=[
		('x',ctypes.c_long),
		('y',ctypes.c_long),
	]

class CharRangeStruct(ctypes.Structure):
	_fields_=[
		('cpMin',ctypes.c_long),
		('cpMax',ctypes.c_long),
	]

class TextRangeUStruct(ctypes.Structure):
	_fields_=[
		('chrg',CharRangeStruct),
		('lpstrText',ctypes.c_wchar_p),
	]

class TextRangeAStruct(ctypes.Structure):
	_fields_=[
		('chrg',CharRangeStruct),
		('lpstrText',ctypes.c_char_p),
	]

CFM_BOLD=0x1
CFM_ITALIC=0x2
CFM_UNDERLINE=0x4
CFM_STRIKEOUT=0x8
CFM_PROTECTED=0x10
CFM_LINK=0x20

SCF_SELECTION=0x1

class CharFormat2WStruct(ctypes.Structure):
	_fields_=[
		('cbSize',ctypes.c_uint),
		('dwMask',ctypes.wintypes.DWORD),
		('dwEffects',ctypes.wintypes.DWORD),
		('yHeight',ctypes.c_long),
		('yOffset',ctypes.c_long),
		('crTextColor',ctypes.wintypes.COLORREF),
		('bCharSet',ctypes.c_byte),
		('bPitchAndFamily',ctypes.c_byte),
		('szFaceName',ctypes.c_wchar*LF_FACESIZE),
		('wWeight',ctypes.wintypes.WORD),
		('sSpacing',ctypes.c_short),
		('crBackColor',ctypes.wintypes.COLORREF),
		('lcid',ctypes.wintypes.LCID),
		('dwReserved',ctypes.wintypes.DWORD),
		('sStyle',ctypes.c_short),
		('wKerning',ctypes.wintypes.WORD),
		('bUnderlineType',ctypes.c_byte),
		('bAnimation',ctypes.c_byte),
		('bRevAuthor',ctypes.c_byte),
		('bReserved1',ctypes.c_byte),
	]

class CharFormat2AStruct(ctypes.Structure):
	_fields_=CharFormat2WStruct._fields_[:]
	_fields_[8]=('szFaceName',ctypes.c_char*LF_FACESIZE)

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

	def _getTextRangeWithEmbeddedObjects(self,start,end):
		ptr=ctypes.POINTER(comtypes.client.GetModule('msftedit.dll').ITextDocument)()
		ctypes.windll.oleacc.AccessibleObjectFromWindow(self.obj.windowHandle,-16,ctypes.byref(ptr._iid_),ctypes.byref(ptr))
		r=ptr.Range(self._startOffset,self._endOffset)
		bufText=r.text
		newTextList=[]
		for offset in range(len(bufText)):
			if ord(bufText[offset])==0xfffc:
				embedRange=ptr.Range(start+offset,start+offset)
				o=embedRange.GetEmbeddedObject()
				o=o.QueryInterface(oleTypes.IOleObject)
				dataObj=o.GetClipboardData(0)
				dataObj=pythoncom._univgw.interface(hash(dataObj),pythoncom.IID_IDataObject)
				format=(win32clipboard.CF_UNICODETEXT, None, pythoncom.DVASPECT_CONTENT, -1, pythoncom.TYMED_HGLOBAL)
				medium=dataObj.GetData(format)
				buf=ctypes.create_string_buffer(medium.data)
				buf=ctypes.cast(buf,ctypes.c_wchar_p)
				newTextList.append(buf.value)
			else:
				newTextList.append(bufText[offset])
		return "".join(newTextList)

	def _getFormatAndOffsets(self,offset,includes=set(),excludes=set()):
		formatList,start,end=super(EditTextInfo,self)._getFormatAndOffsets(offset,includes=includes,excludes=excludes)
		if self.obj.editAPIVersion>=1:
			oldSel=self._getSelectionOffsets()
			if oldSel[0]!=offset and oldSel[1]!=offset:
				self._setSelectionOffsets(offset,offset)
			if self.obj.isWindowUnicode:
				charFormatStruct=CharFormat2WStruct
			else:
				charFormatStruct=CharFormat2AStruct
			charFormat=charFormatStruct()
			charFormat.cbSize=ctypes.sizeof(charFormatStruct)
			processHandle=self.obj.editProcessHandle
			internalCharFormat=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charFormat),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
			winUser.sendMessage(self.obj.windowHandle,EM_GETCHARFORMAT,SCF_SELECTION, internalCharFormat)
			winKernel.readProcessMemory(processHandle,internalCharFormat,ctypes.byref(charFormat),ctypes.sizeof(charFormat),None)
			winKernel.virtualFreeEx(processHandle,internalCharFormat,0,winKernel.MEM_RELEASE)
			if textHandler.isFormatEnabled(controlTypes.ROLE_FONTNAME,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_CHANGE,textHandler.Format(role=controlTypes.ROLE_FONTNAME,value=charFormat.szFaceName))
				formatList.append(f)
			if (charFormat.dwEffects&CFM_BOLD) and textHandler.isFormatEnabled(controlTypes.ROLE_BOLD,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHON,textHandler.Format(role=controlTypes.ROLE_BOLD))
				formatList.append(f)
			if (charFormat.dwEffects&CFM_ITALIC) and textHandler.isFormatEnabled(controlTypes.ROLE_ITALIC,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHON,textHandler.Format(role=controlTypes.ROLE_ITALIC))
				formatList.append(f)
			if (charFormat.dwEffects&CFM_UNDERLINE) and textHandler.isFormatEnabled(controlTypes.ROLE_UNDERLINE,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_SWITCHON,textHandler.Format(role=controlTypes.ROLE_UNDERLINE))
				formatList.append(f)
			if oldSel[0]!=offset and oldSel[1]!=offset:
				self._setSelectionOffsets(oldSel[0],oldSel[1])
		return (formatList,start,end)





	def _getSelectionOffsets(self):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			processHandle=self.obj.editProcessHandle
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winUser.sendMessage(self.obj.windowHandle,EM_EXGETSEL,0, internalCharRange)
			winKernel.readProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
			return (charRange.cpMin,charRange.cpMax)
		else:
			res=winUser.sendMessage(self.obj.windowHandle,EM_GETSEL,0,0)
			return (ctypes.c_ushort(winUser.LOWORD(res)).value,ctypes.c_ushort(winUser.HIWORD(res)).value)

	def _setSelectionOffsets(self,start,end):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			charRange.cpMin=start
			charRange.cpMax=end
			processHandle=self.obj.editProcessHandle
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
			if self.obj.isWindowUnicode:
				info.codepage=1200
			else:
				info.codepage=0
			processHandle=self.obj.editProcessHandle
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
			if self.obj.editAPIHasITextDocument:
				return self._getTextRangeWithEmbeddedObjects(start,end)
			bufLen=((end-start)+1)*2
			if self.obj.isWindowUnicode:
				textRange=TextRangeUStruct()
			else:
				textRange=TextRangeAStruct()
			textRange.chrg.cpMin=start
			textRange.chrg.cpMax=end
			processHandle=self.obj.editProcessHandle
			internalBuf=winKernel.virtualAllocEx(processHandle,None,bufLen,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			textRange.lpstrText=internalBuf
			internalTextRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(textRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalTextRange,ctypes.byref(textRange),ctypes.sizeof(textRange),None)
			res=winUser.sendMessage(self.obj.windowHandle,EM_GETTEXTRANGE,0,internalTextRange)
			winKernel.virtualFreeEx(processHandle,internalTextRange,0,winKernel.MEM_RELEASE)
			buf=(ctypes.c_byte*bufLen)()
			winKernel.readProcessMemory(processHandle,internalBuf,buf,bufLen,None)
			winKernel.virtualFreeEx(processHandle,internalBuf,0,winKernel.MEM_RELEASE)
			if self.obj.isWindowUnicode or (res>1 and (buf[res]!=0 or buf[res+1]!=0)): 
				return ctypes.cast(buf,ctypes.c_wchar_p).value
			else:
				return unicode(ctypes.cast(buf,ctypes.c_char_p).value, errors="replace", encoding=locale.getlocale()[1])
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
		elif self.basePosition in (textHandler.POSITION_CARET,textHandler.POSITION_SELECTION) and self.obj==api.getFocusObject():
			if offset>=(self._getStoryLength()-1):
				return [offset,offset+1]
			oldSel=self._getSelectionOffsets()
			self._setSelectionOffsets(offset,offset)
			sendKey(key("control+ExtendedLeft"))
			back=self._getSelectionOffsets()[0]
			sendKey(key("control+ExtendedRight"))
			forward=self._getSelectionOffsets()[0]
			if (back<=offset) and (forward>offset):
				start=back
				end=forward
			elif (back<offset) and (forward==offset):
				start=forward
				sendKey(key("control+ExtendedRight"))
	 			forward=self._getSelectionOffsets()[0]
				end=forward
			else:
				return super(EditTextInfo,self)._getWordOffsets(offset)
			self._setSelectionOffsets(oldSel[0],oldSel[1])
			return [start,end]
		else:
			return super(EditTextInfo,self)._getWordOffsets(offset)

	def _getLineNumFromOffset(self,offset):
		global ignoreCaretEvents
		if self.obj.editAPIVersion>=1:
			ignoreCaretEvents=True
			res=winUser.sendMessage(self.obj.windowHandle,EM_EXLINEFROMCHAR,0,offset)
			ignoreCaretEvents=False
			return res
		else:
			return winUser.sendMessage(self.obj.windowHandle,EM_LINEFROMCHAR,offset,0)

	def _getLineOffsets(self,offset):
		lineNum=self._getLineNumFromOffset(offset)
		start=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,lineNum,0)
		length=winUser.sendMessage(self.obj.windowHandle,EM_LINELENGTH,offset,0)
		end=start+length
		#If we just seem to get invalid line info, calculate manually
		if start<=0 and end<=0 and lineNum<=0 and self._getLineCount()<=0 and self._getStoryLength()>0:
			return super(EditTextInfo,self)._getLineOffsets(offset)
		if end<offset:
			start=offset
			end=offset+1
		#edit controls lye about their line length
		limit=self._getStoryLength()
		while self._getLineNumFromOffset(end)==lineNum and end<limit:
			end+=1
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return super(EditTextInfo,self)._getLineOffsets(offset)

class Edit(IAccessible):

	editAPIVersion=0
	editAPIUnicode=True
	editAPIHasITextDocument=False
	editValueUnit=textHandler.UNIT_LINE

	def __init__(self,*args,**kwargs):
		self.TextInfo=EditTextInfo
		super(Edit,self).__init__(*args,**kwargs)
		self._lastMouseTextOffsets=None
		if self.editAPIVersion>=1:
			self.editProcessHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,self.windowProcessID)
		self._editLastSelectionPos=self.makeTextInfo(textHandler.POSITION_CARET)


	def __del__(self):
		if self.editAPIVersion>=1:
			winKernel.closeHandle(self.editProcessHandle)

	def _get_value(self):
		return None

	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

	def event_mouseMove(self,x,y):
		mouseEntered=self._mouseEntered
		super(Edit,self).event_mouseMove(x,y)
		(left,top,width,height)=self.location
		if self.editAPIVersion>=1:
			processHandle=self.editProcessHandle
			internalP=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(PointLStruct),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			p=PointLStruct(x-left,y-top)
			winKernel.writeProcessMemory(processHandle,internalP,ctypes.byref(p),ctypes.sizeof(p),None)
			offset=winUser.sendMessage(self.windowHandle,EM_CHARFROMPOS,0,internalP)
			winKernel.virtualFreeEx(processHandle,internalP,0,winKernel.MEM_RELEASE)
		else:
			p=(x-left)+((y-top)<<16)
			offset=winUser.sendMessage(self.windowHandle,EM_CHARFROMPOS,0,p)&0xffff
		if self._lastMouseTextOffsets is None or offset<self._lastMouseTextOffsets[0] or offset>=self._lastMouseTextOffsets[1]:   
			if mouseEntered:
				speech.cancelSpeech()
			info=self.makeTextInfo(textHandler.Bookmark(self.TextInfo,(offset,offset)))
			info.expand(textHandler.UNIT_WORD)
			speech.speakText(info.text)
			self._lastMouseTextOffsets=(info._startOffset,info._endOffset)

	def event_valueChange(self):
		self._editLastSelectionPos=self.makeTextInfo(textHandler.POSITION_SELECTION).copy()

	def event_caret(self):
		newInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		oldInfo=self._editLastSelectionPos
		queueHandler.queueFunction(queueHandler.eventQueue,speech.speakSelectionChange,oldInfo,newInfo,speakUnselected=False)
		self._editLastSelectionPos=newInfo.copy()

	def script_changeSelection(self,keyPress,nextScript):
		oldInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		sendKey(keyPress)
		if not isKeyWaiting():
			api.processPendingEvents()
			focus=api.getFocusObject()
			newInfo=focus.makeTextInfo(textHandler.POSITION_SELECTION)
			speech.speakSelectionChange(oldInfo,newInfo,speakSelected=False)

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

class RichEdit30(RichEdit):
	editAPIVersion=3

class RichEdit50(RichEdit):
	editAPIVersion=5
