from textPositionUtils import *
import winUser
import controlTypes
from NVDAObjects.IAccessible import IAccessible 

#Window messages
SCI_GETLENGTH=2006
SCI_GETCURRENTPOS=2008
SCI_GETANCHOR=2009
SCI_GETLINEENDPOSITION=2136
SCI_GETLINECOUNT=2154
SCI_LINEFROMPOSITION=2166
SCI_POSITIONFROMLINE=2167

#The Scintilla NVDA object, inherists the generic MSAA NVDA object
class Scintilla(IAccessible):

#The name of the object is gotten by the standard way of getting a window name, can't use MSAA name (since it contains all the text)
	def _get_name(self):
		return winUser.getWindowText(self.windowHandle)

#The role of the object should be editable text
	def _get_role(self):
		return controlTypes.ROLE_EDITABLETEXT

#The value of the object should be the current line of the text
	def _get_value(self):
		(start,end)=self.text_getLineOffsets(self.text_caretOffset)
		return self.text_getText(start,end)

#The text is found in the MSAA name property
	def text_getText(self,start=None,end=None):
		text=self.IAccessibleObject.accName()
		if text is None:
			return "\0"
		start=start if start is not None else 0
		end=end if end is not None else len(text)
		if start>=0 and end>start:
			return text[start:end]
		else:
			return "\0"

#There is a window message to get the caret offset
	def _get_text_caretOffset(self):
		return winUser.sendMessage(self.windowHandle,SCI_GETCURRENTPOS,0,0)

	def _get_text_selectionCount(self):
		if winUser.sendMessage(self.windowHandle,SCI_GETANCHOR,0,0)!=winUser.sendMessage(self.windowHandle,SCI_GETCURRENTPOS,0,0):
			return 1
		else:
			return 0

	def text_getSelectionOffsets(self,index):
		a=winUser.sendMessage(self.windowHandle,SCI_GETCURRENTPOS,0,0)
		b=winUser.sendMessage(self.windowHandle,SCI_GETANCHOR,0,0)
		return [min(a,b),max(a,b)]

	def _get_text_lineCount(self):
		return winUser.sendMessage(self.windowHandle,SCI_GETLINECOUNT,0,0)

	def text_getLineNumber(self,offset):
		return winUser.sendMessage(self.windowHandle,SCI_LINEFROMPOSITION,offset,0)

	def text_getLineOffsets(self,offset):
		text=self.text_getText()
		if offset<len(text):
			return [findStartOfLine(text,offset),findEndOfLine(text,offset)]
		else:
			return [offset,offset+1]

	def text_getWordOffsets(self,offset):
		text=self.text_getText()
		if offset<len(text):
			return [findStartOfWord(text,offset),findEndOfWord(text,offset)]
		else:
			return [offset,offset+1]


#We want all the standard text editing key commands to be handled by NVDA
[Scintilla.bindKey(keyName,scriptName) for keyName,scriptName in [
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

