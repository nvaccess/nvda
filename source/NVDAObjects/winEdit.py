#NVDAObjects/winEdit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import struct
import ctypes
import speech
import debug
import winUser
from keyUtils import key
import IAccessibleHandler
import IAccessible

class NVDAObject_winEdit(IAccessible.NVDAObject_IAccessible):

	def text_getText(self,start=None,end=None):
		start=start if isinstance(start,int) else 0
		end=end if isinstance(end,int) else len(self.value)
		if self.text_lineCount>1:
			startLineNum=self.text_getLineNumber(start)-1
			startOffset=start-self.text_getLineOffsets(start)[0]
			endLineNum=self.text_getLineNumber(end-1)-1
			lines=[]
			for lineNum in xrange(startLineNum,endLineNum+1):
				lineStart=winUser.sendMessage(self.windowHandle,winUser.EM_LINEINDEX,lineNum,0)
				lineLength=winUser.sendMessage(self.windowHandle,winUser.EM_LINELENGTH,lineStart,0)
				#em_getline needs a buffer in which to place a unicode string.
				#However it must already contain the length of the line as its first word.
				#We use a char array to hold the word, plus receive the line, then we cast to unicode 
				buf=(ctypes.c_char*((lineLength*2)+2))()
				buf.value=struct.pack('h',lineLength+1)
				winUser.sendMessage(self.windowHandle,winUser.EM_GETLINE,lineNum,buf)
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
		long=winUser.sendMessage(self.windowHandle,winUser.EM_GETSEL,0,0)
		start=winUser.LOWORD(long)
		end=winUser.HIWORD(long)
		if start!=end:
			return (start,end)
		else:
			return None

	def _get_text_caretOffset(self):
		long=winUser.sendMessage(self.windowHandle,winUser.EM_GETSEL,0,0)
		pos=winUser.LOWORD(long)
		return pos

	def _set_text_caretOffset(self,pos):
		winUser.sendMessage(self.windowHandle,winUser.EM_SETSEL,pos,pos)

	def text_getLineNumber(self,offset):
		return winUser.sendMessage(self.windowHandle,winUser.EM_LINEFROMCHAR,offset,0)+1

	def _get_text_lineCount(self):
		return winUser.sendMessage(self.windowHandle,winUser.EM_GETLINECOUNT,0,0)

	def text_getLineOffsets(self,offset):
		if self.text_lineCount<1:
			return (0,self.text_characterCount)
		lineNum=self.text_getLineNumber(offset)-1
		lineStart=winUser.sendMessage(self.windowHandle,winUser.EM_LINEINDEX,lineNum,0)
		lineLength=winUser.sendMessage(self.windowHandle,winUser.EM_LINELENGTH,lineStart,0)
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

[NVDAObject_winEdit.bindKey(keyName,scriptName) for keyName,scriptName in [
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
