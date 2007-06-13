#NVDAObjects/Edit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

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

class EditTextInfo(text.TextInfo):

	def _getSelOffsets(self):
		if self.obj.editAPIVersion>=1:
			charRange=CharRangeStruct()
			processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ,False,self.obj.windowProcessID)
			internalCharRange=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(charRange),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winUser.sendMessage(self.obj.windowHandle,EM_EXGETSEL,0, internalCharRange)
			winKernel.readProcessMemory(processHandle,internalCharRange,ctypes.byref(charRange),ctypes.sizeof(charRange),None)
			winKernel.virtualFreeEx(processHandle,internalCharRange,0,winKernel.MEM_RELEASE)
			return [charRange.cpMin,charRange.cpMax]
		else:
			long=winUser.sendMessage(self.obj.windowHandle,EM_GETSEL,0,0)
			return [winUser.LOWORD(long),winUser.HIWORD(long)]

	def _getStoryLength(self):
		if self.obj.editAPIVersion>=2:
			info=getTextLengthExStruct()
			info.flags=GTL_NUMCHARS
			info.codepage=1200
			processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ|winKernel.PROCESS_VM_WRITE,False,self.obj.windowProcessID)
			internalInfo=winKernel.virtualAllocEx(processHandle,None,ctypes.sizeof(info),winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
			winKernel.writeProcessMemory(processHandle,internalInfo,ctypes.byref(info),ctypes.sizeof(info),None)
			textLen=winUser.sendMessage(self.obj.windowHandle,EM_GETTEXTLENGTHEX,internalInfo,0)
			winKernel.virtualFreeEx(processHandle,internalInfo,0,winKernel.MEM_RELEASE)
			return textLen
		else:
			return winUser.sendMessage(self.obj.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)

	def _getText(self,start,end):
		if self.obj.editAPIVersion>=2:
			bufLen=((end-start)+1)*2
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
			buf=ctypes.create_unicode_buffer(bufLen)
			winKernel.readProcessMemory(processHandle,internalBuf,buf,bufLen,None)
			winKernel.virtualFreeEx(processHandle,internalBuf,0,winKernel.MEM_RELEASE)
			return buf.value
		else:
			return self.obj.windowText[start:end]

	def _getExWordOffsets(self,offset):
		start=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDLEFT,offset)
		end=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,start)
		if end<=offset:
			start=end
			end=winUser.sendMessage(self.obj.windowHandle,EM_FINDWORDBREAK,WB_MOVEWORDRIGHT,offset)
		return [start,end]


	def _lineNumFromOffset(self,offset):
		if self.obj.editAPIVersion>=1:
			return winUser.sendMessage(self.obj.windowHandle,EM_EXLINEFROMCHAR,0,offset)
		else:
			return winUser.sendMessage(self.obj.windowHandle,EM_LINEFROMCHAR,offset,0)

	def _updateLineCache(self,_lineNum=None,_lineText=None,_lineStartOffset=None,_lineLength=None):
		#If any of the line info is missing, then get it all  
		if (_lineNum is None or _lineText is None or _lineStartOffset is None or _lineLength is None):
			_lineNum=self._lineNumFromOffset(self._startOffset)
			_lineStartOffset=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,_lineNum,0)
			_lineLength=winUser.sendMessage(self.obj.windowHandle,EM_LINELENGTH,_lineStartOffset,0)
			buf=(ctypes.c_char*((_lineLength*2)+2))()
			buf.value=struct.pack('h',_lineLength+1)
			winUser.sendMessage(self.obj.windowHandle,EM_GETLINE,_lineNum,buf)
			_lineText=ctypes.c_wchar_p(ctypes.cast(buf,ctypes.c_void_p).value).value[0:_lineLength]
			#Edit controls lye about their line length, grow it to its actual length
			#Fill it in with a \r, a \r\n, or nulls and then \r\n.
			offset=_lineStartOffset+_lineLength
			count=0
			limit=self._storyLength-1
			while self._lineNumFromOffset(offset)==_lineNum and offset<limit:
				count+=1
				offset+=1
			if count==1:
				_lineText+="\r"
			elif count==2:
				_lineText+="\r\n"
			else:
				_lineText+="".join(['\0']*(count-2))+"\r\n"
			_lineLength=len(_lineText)
		#Cache all info in the object
		self._lineNum=_lineNum
		self._lineText=_lineText
		self._lineStartOffset=_lineStartOffset
		self._lineLength=_lineLength

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None,_storyText=None,_storyLength=None,_lineNum=None,_lineText=None,_lineStartOffset=None,_lineLength=None):
		super(EditTextInfo,self).__init__(obj,position,expandToUnit,limitToUnit)
		#Find out the size of the entire text
		if _storyLength is not None:
			self._storyLength=_storyLength
		else:
				self._storyLength=self._getStoryLength()
		#Translate the position in to offsets and cache it
		if position==text.POSITION_FIRST:
			self._startOffset=self._endOffset=0
		elif position==text.POSITION_LAST:
			self._startOffset=self._endOffset=self._storyLength-1
		elif position==text.POSITION_CARET:
			self._startOffset=self._endOffset=self._getSelOffsets()[0]
		elif position==text.POSITION_SELECTION:
			(self._startOffset,self._endOffset)=self._getSelOffsets()
		elif isinstance(position,text.OffsetPosition):
			self._startOffset=self._endOffset=position.offset
		elif isinstance(position,text.OffsetsPosition):
			self._startOffset=position.start
			self._endOffset=position.end
		else:
			raise NotImplementedError("position: %s not supported"%position)
		#If working with in a line, grab its text
		if expandToUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE] or limitToUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE]:
			self._updateLineCache(_lineNum=_lineNum,_lineText=_lineText,_lineStartOffset=_lineStartOffset,_lineLength=_lineLength)
		elif expandToUnit==text.UNIT_PARAGRAPH:
			if _storyText is not None:
				self._storyText=_storyText
			else:
				self._storyText=self._getText(0,self._storyLength)
			if len(self._storyText)==0:
				self._storyText="\0"
		#Set the start and end offsets from expanding position to a unit 
		if expandToUnit==text.UNIT_CHARACTER:
			self._startOffset=self._startOffset
			self._endOffset=self.startOffset+1
		elif expandToUnit==text.UNIT_WORD:
			if self.obj.editAPIVersion>=1:
				(self._startOffset,self._endOffset)=self._getExWordOffsets(self._startOffset)
			else:
				self._startOffset=text.findStartOfWord(self._lineText,self._startOffset-self._lineStartOffset)+self._lineStartOffset 
				self._endOffset=text.findEndOfWord(self._lineText,self._startOffset-self._lineStartOffset)+self._lineStartOffset
		elif expandToUnit==text.UNIT_LINE:
			self._startOffset=self._lineStartOffset
			self._endOffset=self._lineStartOffset+self._lineLength
		elif expandToUnit==text.UNIT_PARAGRAPH:
			self._startOffset=text.findStartOfLine(self._storyText,self._startOffset)
			self._endOffset=text.findEndOfLine(self._storyText,self._startOffset)
		elif expandToUnit==text.UNIT_SCREEN:
			self._startOffset=0 #winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,winUser.sendMessage(self.obj.windowHandle,EM_GETFIRSTVISIBLELINE,0,0),0)
			self._endOffset=self._storyLength
		elif expandToUnit==text.UNIT_STORY:
			self._startOffset=0
			self._endOffset=self._storyLength
		elif expandToUnit is not None:
			raise NotImplementedError("unit: %s not supported"%expandToUnit)
		if limitToUnit==text.UNIT_CHARACTER:
			self._lowOffsetLimit=self._startOffset
			self._highOffsetLimit=self._lowOffsetLimit+1
		elif limitToUnit==text.UNIT_WORD:
			if self.obj.editAPIVersion>=1:
				(self._lowOffsetLimit,self._highOffsetLimit)=self._getExWordOffsets(self._startOffset)
			else:
				self._lowOffsetLimit=text.findStartOfWord(self._lineText,self._lowOffsetLimit-self._lineStartOffset)+self._lineStartOffset 
				self._highOffsetLimit=text.findEndOfWord(self._lineText,self._startOffsetLimit-self._lineStartOffset)+self._lineStartOffset
		elif limitToUnit==text.UNIT_LINE:
			self._lowOffsetLimit=self._lineStartOffset
			self._highOffsetLimit=self._lineStartOffset+self._lineLength
		elif limitToUnit==text.UNIT_PARAGRAPH:
			self._lowOffsetLimit=text.findStartOfLine(self._storyText,self._startOffset)
			self._highOffsetLimit=text.findEndOfLine(self._storyText,self._startOffset)
		elif limitToUnit==text.UNIT_SCREEN:
			self._lowOffsetLimit=0 #winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,winUser.sendMessage(self.obj.windowHandle,EM_GETFIRSTVISIBLELINE,0,0),0)
			self._highOffsetLimit=self._storyLength
		elif limitToUnit in [None,text.UNIT_STORY]:
			self._lowOffsetLimit=0
			self._highOffsetLimit=self._storyLength
		else:
			raise NotImplementedError("limitToUnit: %s not supported"%limitToUnit)

	def _get_startOffset(self):
		return self._startOffset

	def _get_endOffset(self):
		return self._endOffset

	def _get_text(self):
		if self.unit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE] or self.limitUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE]:
			return self._lineText[self._startOffset-self._lineStartOffset:self._endOffset-self._lineStartOffset]
		elif self.unit==text.UNIT_PARAGRAPH:
			return self._storyText[self._startOffset:self._endOffset]
		else:
			return self._getText(self._startOffset,self._endOffset)

	def getRelatedUnit(self,relation):
		if self.unit is None:
			raise RuntimeError("no unit specified")
		debug.writeMessage("getRelatedUnit: releation %s, unit %s, limitUnit %s"%(relation,self.unit,self.limitUnit))
		if relation==text.UNITRELATION_NEXT:
			newOffset=self._endOffset
		elif relation==text.UNITRELATION_PREVIOUS:
			newOffset=self._startOffset-1
		elif relation==text.UNITRELATION_FIRST:
			newOffset=self._lowOffsetLimit
		elif relation==text.UNITRELATION_LAST:
			newOffset=self._highOffsetLimit-1
		else:
			raise NotImplementedError("unit relation: %s not supported"%relation)
		if newOffset<self._lowOffsetLimit or newOffset>=self._highOffsetLimit:
			raise text.E_noRelatedUnit("offset %d is out of range for limits %d, %d"%(newOffset,self._lowOffsetLimit,self._highOffsetLimit))
		if  self.limitUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE] or (self.unit in [text.UNIT_CHARACTER,text.UNIT_WORD] and newOffset>=self._lineStartOffset and newOffset<(self._lineStartOffset+self._lineLength)):
			return self.__class__(self.obj,text.OffsetPosition(newOffset),_lineText=self._lineText,_lineNum=self._lineNum,_lineStartOffset=self._lineStartOffset,_lineLength=self._lineLength,_storyLength=self._storyLength,expandToUnit=self.unit,limitToUnit=self.limitUnit)
		elif hasattr(self,"_storyText"):
			return self.__class__(self.obj,text.OffsetPosition(newOffset),_storyText=self._storyText,_storyLength=self._storyLength,expandToUnit=self.unit,limitToUnit=self.limitUnit)
		else:
			return self.__class__(self.obj,text.OffsetPosition(newOffset),_storyLength=self._storyLength,expandToUnit=self.unit,limitToUnit=self.limitUnit)

	def _get_inUnit(self):
		if self.unit is None:
			raise RuntimeError("no unit specified")
		return True


class Edit(IAccessible):

	TextInfo=EditTextInfo
	editAPIVersion=0

	def _get_value(self):
		return self.makeTextInfo(text.POSITION_CARET,expandToUnit=text.UNIT_LINE).text

	def event_valueChange(self):
		pass

	def _get_caretOffset(self):
		long=winUser.sendMessage(self.windowHandle,EM_GETSEL,0,0)
		pos=winUser.LOWORD(long)
		return pos

	def _set_caretOffset(self,pos):
		winUser.sendMessage(self.windowHandle,EM_SETSEL,pos,pos)

	def _get_selectionOffsets(self):
		long=winUser.sendMessage(self.windowHandle,EM_GETSEL,0,0)
		start=winUser.LOWORD(long)
		end=winUser.HIWORD(long)
		if start!=end:
			return (start,end)
		else:
			return None

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

