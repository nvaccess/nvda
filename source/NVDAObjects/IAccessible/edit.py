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
import speech
import debug
import winKernel
from IAccessibleHandler import pointer_IAccessible
import api
import winUser
import textHandler
from keyUtils import key, sendKey, isKeyWaiting
import IAccessibleHandler
import controlTypes
from . import IAccessible
from .. import NVDAObjectTextInfo

IServiceProvider=comtypes.client.GetModule('lib/ServProv.tlb').IServiceProvider

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
				dataObj=pythoncom._univgw.interface(ctypes.cast(dataObj,ctypes.c_void_p).value,pythoncom.IID_IDataObject)
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
			if self.obj.editAPIUnicode:
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
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_SINGLETON,textHandler.Format(role=controlTypes.ROLE_FONTNAME,value=charFormat.szFaceName))
				formatList.append(f)
			if (charFormat.dwEffects&CFM_BOLD) and textHandler.isFormatEnabled(controlTypes.ROLE_BOLD,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_ON,textHandler.Format(role=controlTypes.ROLE_BOLD))
				formatList.append(f)
			if (charFormat.dwEffects&CFM_ITALIC) and textHandler.isFormatEnabled(controlTypes.ROLE_ITALIC,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_ON,textHandler.Format(role=controlTypes.ROLE_ITALIC))
				formatList.append(f)
			if (charFormat.dwEffects&CFM_UNDERLINE) and textHandler.isFormatEnabled(controlTypes.ROLE_UNDERLINE,includes=includes,excludes=excludes):
				f=textHandler.FormatCommand(textHandler.FORMAT_CMD_ON,textHandler.Format(role=controlTypes.ROLE_UNDERLINE))
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
			long=winUser.sendMessage(self.obj.windowHandle,EM_GETSEL,0,0)
			return (winUser.LOWORD(long),winUser.HIWORD(long))

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
			if self.obj.editAPIUnicode:
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
			bufLen=(end-start)+1
			if self.obj.editAPIUnicode:
				bufLen*=2
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
		elif self.basePosition in (textHandler.POSITION_CARET,textHandler.POSITION_SELECTION):
			oldSel=self._getSelectionOffsets()
			if offset>=(self._getStoryLength()-1):
				return [offset,offset+1]
			self._setSelectionOffsets(offset,offset)
			sendKey(key("control+shift+ExtendedLeft"))
			back=self._getSelectionOffsets()
			sendKey(key("control+shift+ExtendedRight"))
			forward=self._getSelectionOffsets()
			if (back[1]-back[0])>0 and (forward[1]-forward[0])>0 and forward[0]>back[0]:
				start=back[0]
				end=forward[1]
			elif back[0]<forward[0]:
				sendKey(key("control+shift+ExtendedRight"))
	 			forward=self._getSelectionOffsets()
				start,end=forward
			else:
				start,end=forward
			self._setSelectionOffsets(oldSel[0],oldSel[1])
			return [start,end]
		else:
			return super(EditTextInfo,self)._getWordOffsets(offset)

	def _getLineNumFromOffset(self,offset):
		if self.obj.editAPIVersion>=1:
			return winUser.sendMessage(self.obj.windowHandle,EM_EXLINEFROMCHAR,0,offset)
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
		#edit controls lye about their line length
		limit=end+4
		while self._getLineNumFromOffset(end)==lineNum and end<limit:
			end+=1
		return (start,end)

	def _getParagraphOffsets(self,offset):
		return super(EditTextInfo,self)._getLineOffsets(offset)

class Edit(IAccessible):

	TextInfo=EditTextInfo
	editAPIVersion=0
	editAPIUnicode=True
	editAPIHasITextDocument=False
	editValueUnit=textHandler.UNIT_LINE

	def __init__(self,*args,**kwargs):
		super(Edit,self).__init__(*args,**kwargs)
		if self.editAPIVersion>=1:
			self.editProcessHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,self.windowProcessID)
		self.reviewPosition=self.makeTextInfo(textHandler.POSITION_CARET)
		self._editLastSelectionPos=self.reviewPosition.copy()

	def __del__(self):
		if self.editAPIVersion>=1:
			winKernel.closeHandle(self.editProcessHandle)
		super(Edit,self).__del__()

	def _get_value(self):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		info.expand(self.editValueUnit)
		return info.text

	def event_valueChange(self):
		self._editLastSelectionPos=self.makeTextInfo(textHandler.POSITION_SELECTION).copy()

	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True,keyboardShortcut=True,positionString=True)
		info=self.makeTextInfo(textHandler.POSITION_SELECTION)
		self._editLastSelectionPos=info
		if info.isCollapsed:
			info=info.copy()
			info.expand(self.editValueUnit)
			speech.speakFormattedText(info)
		else:
			text=info.text
			if len(text)<=1:
				text=speech.processSymbol(text)
			speech.speakMessage(_("selected %s")%text)

	def event_caret(self):
		newInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		oldInfo=self._editLastSelectionPos
		#speakSelectionChange must be in interactive queue so it happens after key scripts
		queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakSelectionChange,oldInfo,newInfo,speakUnselected=False)
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

class RichEdit20A(RichEdit20):
	editAPIUnicode=False


