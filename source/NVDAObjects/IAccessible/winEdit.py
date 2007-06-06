#NVDAObjects/WinEdit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import struct
import ctypes
import speech
import debug
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

class WinEdit(IAccessible):

	def _get_name(self):
		name=super(WinEdit,self)._get_name()
		if not isinstance(name,basestring):
			name=""
		if self.text_getText().strip()!=name.strip():
			return name

	def text_getText(self,start=None,end=None):
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.value)
		if self.text_lineCount>1:
			startLineNum=self.text_getLineNumber(start)-1
			startOffset=start-self.text_getLineOffsets(start)[0]
			endLineNum=self.text_getLineNumber(end-1)-1
			lines=[]
			for lineNum in xrange(startLineNum,endLineNum+1):
				lineStart=winUser.sendMessage(self.windowHandle,EM_LINEINDEX,lineNum,0)
				lineLength=winUser.sendMessage(self.windowHandle,EM_LINELENGTH,lineStart,0)
				#em_getline needs a buffer in which to place a unicode string.
				#However it must already contain the length of the line as its first word.
				#We use a char array to hold the word, plus receive the line, then we cast to unicode 
				buf=(ctypes.c_char*((lineLength*2)+2))()
				buf.value=struct.pack('h',lineLength+1)
				winUser.sendMessage(self.windowHandle,EM_GETLINE,lineNum,buf)
				bufPtr=ctypes.cast(buf,ctypes.POINTER(ctypes.c_wchar*(lineLength+1)))
				lines.append(bufPtr.contents.value[0:lineLength])
			text="".join(lines)
			text=text[startOffset:][:end-start]
			if text=="":
				text='\r'
			return text
		else:
			text=self.windowText
			return text[start:end]

	def _get_text_characterCount(self):
		return winUser.sendMessage(self.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)
 
	def _get_typeString(self):
		typeString=IAccessibleHandler.getRoleName(IAccessibleHandler.ROLE_SYSTEM_TEXT)
		if self.isProtected:
			typeString=_("protected %s ")%typeString
		return typeString

	def _get_value(self):
		r=self.text_getLineOffsets(self.text_caretOffset)
		return self.text_getText(r[0],r[1])

	def _get_text_selectionCount(self):
		if self.text_getSelectionOffsets(0) is not None:
			return 1
		else:
			return 0

	def text_getSelectionOffsets(self,index):
		if index!=0:
			return None
		long=winUser.sendMessage(self.windowHandle,EM_GETSEL,0,0)
		start=winUser.LOWORD(long)
		end=winUser.HIWORD(long)
		if start!=end:
			return (start,end)
		else:
			return None

	def _get_text_caretOffset(self):
		long=winUser.sendMessage(self.windowHandle,EM_GETSEL,0,0)
		pos=winUser.LOWORD(long)
		return pos

	def _set_text_caretOffset(self,pos):
		winUser.sendMessage(self.windowHandle,EM_SETSEL,pos,pos)

	def text_getLineNumber(self,offset):
		return winUser.sendMessage(self.windowHandle,EM_LINEFROMCHAR,offset,0)+1

	def _get_text_lineCount(self):
		return winUser.sendMessage(self.windowHandle,EM_GETLINECOUNT,0,0)

	def text_getLineOffsets(self,offset):
		if self.text_lineCount<1:
			return (0,self.text_characterCount)
		lineNum=self.text_getLineNumber(offset)-1
		lineStart=winUser.sendMessage(self.windowHandle,EM_LINEINDEX,lineNum,0)
		lineLength=winUser.sendMessage(self.windowHandle,EM_LINELENGTH,lineStart,0)
		lineEnd=lineStart+lineLength
		return (lineStart,lineEnd)

	def text_getNextLineOffsets(self,offset):
		(start,end)=self.text_getLineOffsets(offset)
		startLineNum=self.text_getLineNumber(start)
		if self.text_getLineNumber(end)!=startLineNum:
			return self.text_getLineOffsets(end)
		limit=self.text_characterCount
		while end<limit:
			end+=1
			if self.text_getLineNumber(end)!=startLineNum:
				return self.text_getLineOffsets(end)
		return None

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

[WinEdit.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","text_moveByLine"),
	("ExtendedDown","text_moveByLine"),
	("ExtendedLeft","text_moveByCharacter"),
	("ExtendedRight","text_moveByCharacter"),
	("Control+ExtendedLeft","text_moveByWord"),
	("Control+ExtendedRight","text_moveByWord"),
	("Shift+ExtendedRight","text_changeSelection"),
	("Shift+ExtendedLeft","text_changeSelection"),
	("Shift+ExtendedHome","text_changeSelection"),
	("Shift+ExtendedEnd","text_changeSelection"),
	("Shift+ExtendedUp","text_changeSelection"),
	("Shift+ExtendedDown","text_changeSelection"),
	("Control+Shift+ExtendedLeft","text_changeSelection"),
	("Control+Shift+ExtendedRight","text_changeSelection"),
	("ExtendedHome","text_moveByCharacter"),
	("ExtendedEnd","text_moveByCharacter"),
	("control+extendedHome","text_moveByLine"),
	("control+extendedEnd","text_moveByLine"),
	("control+shift+extendedHome","text_changeSelection"),
	("control+shift+extendedEnd","text_changeSelection"),
	("ExtendedDelete","text_delete"),
	("Back","text_backspace"),
]]

class TextInfo(text.TextInfo):

	def _fetchLine(self,lineNum,lineLength):
		buf=(ctypes.c_char*((lineLength*2)+2))()
		buf.value=struct.pack('h',lineLength+1)
		winUser.sendMessage(self.obj.windowHandle,EM_GETLINE,lineNum,buf)
		return ctypes.c_wchar_p(ctypes.cast(buf,ctypes.c_void_p).value).value

	def __init__(self,obj,position,expandToUnit=None,limitToUnit=None,endPosition=None,_storyText=None,_storyLength=None,_lineNum=None,_lineText=None,_lineStartOffset=None,_lineLength=None):
		super(self.__class__,self).__init__(obj,position,expandToUnit,limitToUnit,endPosition)
		#Find out the size of the entire text
		if _storyLength is not None:
			self._storyLength=_storyLength
		else:
			self._storyLength=winUser.sendMessage(self.obj.windowHandle,winUser.WM_GETTEXTLENGTH,0,0)
		#Translate the position in to an offset and cache it
		if position==text.POSITION_FIRST:
			self._startOffset=0
		elif position==text.POSITION_LAST:
			self._startOffset=self._storyLength-1
		elif position==text.POSITION_CARET:
			self._startOffset=obj.caretOffset
		elif isinstance(position,int):
			self._startOffset=position
		elif position is not None:
			raise NotImplementedError("position: %s not supported"%position)
		#Set the possible end position
		elif endPosition==text.POSITION_LAST:
			self._endOffset=self._storyLength
		elif endPosition==text.POSITION_CARET:
			self._endOffset=obj.caretOffset
		elif isinstance(endPosition,int):
			self._endOffset=endPosition
		elif endPosition is not None:
			raise NotImplementedError("endPosition: %s not supported"%endPosition)
		#If working with in a line, grab its text
		#Otherwise grab the entire text
		if expandToUnit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE] or limitToUnitIn [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE]:
			if _lineNum is not None:
				self._lineNum=_lineNum
			else:
				self._lineNum=winUser.sendMessage(self.obj.windowHandle,EM_LINEFROMCHAR,self._startOffset,0)
			if _lineStartOffset is not None:
				self._lineStartOffset=_lineStartOffset
			else:
				self._lineStartOffset=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,self._lineNum,0)
			if _lineLength is not None:
				self._lineLength=_lineLength
			else:
				self._lineLength=winUser.sendMessage(self.obj.windowHandle,EM_LINELENGTH,self._lineStartOffset,0)
			if _lineText is not None:
				self._lineText=_lineText
			else:
				self._lineText=self._fetchLine(self._lineNum,self._lineLength)
			if len(self._lineText)==0:
				self._lineText="\0"
		else:
			if _storyText is not None:
				self._storyText=_storyText
			else:
				self._storyText=self.obj.windowText
			if len(self._storyText)==0:
				self._storyText="\0"
		#Set the start and end offsets from expanding position to a unit 
		if expandToUnit==text.UNIT_CHARACTER:
			self._startOffset=self._startOffset
			self._endOffset=self.startOffset+1
		elif expandToUnit==text.UNIT_WORD:
			self._startOffset=text.findStartOfWord(self._lineText,self._startOffset-self._lineStartOffset)+self._lineStartOffset 
			self._endOffset=text.findEndOfWord(self._lineText,self._startOffset-self._lineStartOffset)+self._lineStartOffset
		elif expandToUnit==text.UNIT_LINE:
			self._startOffset=self._lineStartOffset
			self._endOffset=self._lineStartOffset+self._lineLength
		elif expandToUnit==text.UNIT_SCREEN:
			self._startOffset=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,winUser.sendMessage(self.obj.windowHandle,EM_GETFIRSTVISIBLELINE,0,0),0)
			self._endOffset=self._storyLength
		elif expandToUnit==text.UNIT_STORY:
			self._startOffset=0
			self._endOffset=self._storyLength
		else:
			raise NotImplementedError("unit: %s not supported"%unit)
		if limitToUnit==text.UNIT_CHARACTER:
			self._lowOffsetLimit=self._startOffset
			self._highOffsetLimit=self._lowOffsetLimit+1
		elif limitToUnit==text.UNIT_WORD:
			self._lowOffsetLimit=text.findStartOfWord(self._lineText,self._lowOffsetLimit-self._lineStartOffset)+self._lineStartOffset 
			self._highOffsetLimit=text.findEndOfWord(self._lineText,self._startOffsetLimit-self._lineStartOffset)+self._lineStartOffset
		elif limitToUnit==text.UNIT_LINE:
			self._lowOffsetLimit=self._lineStartOffset
			self._highOffsetLimit=self._lineStartOffset+self._lineLength
		elif limitToUnit==text.UNIT_SCREEN:
			self._lowOffsetLimit=winUser.sendMessage(self.obj.windowHandle,EM_LINEINDEX,winUser.sendMessage(self.obj.windowHandle,EM_GETFIRSTVISIBLELINE,0,0),0)
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
		if self.unit in [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE] or limitToUnitIn [text.UNIT_CHARACTER,text.UNIT_WORD,text.UNIT_LINE]:
			return self._lineText[self._startOffset-self._lineStartOffset:self._endOffset-self._lineStartOffset]
		else:
			return self._storyText[self._startOffset:self._endOffset]

	def getRelatedUnit(self,relation):
		if self.unit is None:
			raise RuntimeError("no unit specified")
		debug.writeMessage("getRelatedUnit: releation %s, unit %s, limitUnit %s"%(relation,self.unit,self.limitUnit))
		if relation==text.UNITRELATION_NEXT:
			newOffset=self._endOffset
			if self.unit==text.UNIT_LINE:
				#the control gives back line offsets sometimes with line break chars, sometimes not,
				#So Keep moving till the line number changes, or we reach the end of the text
				while winUser.sendMessage(self.obj.windowHandle,EM_LINEFROMCHAR,newOffset,0)==self._lineNum and newOffset<self._highOffsetLimit:
					newOffset+=1 
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
			return self.__class__(self.obj,newOffset,_lineText=self._lineText,_lineNum=self._lineNum,_lineStartOffset=self._lineStartOffset,_lineLength=self._lineLength,_storyLength=self._storyLength,expandToUnit=self.unit,limitToUnit=self.limitUnit)
		elif hasattr(self,"_storyText"):
			return self.__class__(self.obj,newOffset,_storyText=self._storyText,_storyLength=self._storyLength,expandToUnit=self.unit,limitToUnit=self.limitUnit)
		else:
			return self.__class__(self.obj,newOffset,_storyLength=self._storyLength,expandToUnit=self.unit,limitToUnit=self.limitUnit)

	def _get_inUnit(self):
		if self.unit is None:
			raise RuntimeError("no unit specified")
		return True

WinEdit.TextInfo=TextInfo
