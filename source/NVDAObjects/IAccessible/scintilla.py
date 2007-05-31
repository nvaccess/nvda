from textPositionUtils import *
import winKernel
import winUser
import controlTypes
from NVDAObjects.IAccessible import IAccessible 
import ctypes
import debug
import speech

#Window messages
SCI_GETLENGTH=2006
SCI_GETCURRENTPOS=2008
SCI_GETANCHOR=2009
SCI_GETLINEENDPOSITION=2136
SCI_GETLINECOUNT=2154
SCI_LINEFROMPOSITION=2166
SCI_POSITIONFROMLINE=2167
SCI_GETSTYLEAT=2010
SCI_STYLEGETFONT=2486
SCI_STYLEGETSIZE=2485
SCI_STYLEGETBOLD=2483
SCI_STYLEGETITALIC=2484
SCI_STYLEGETUNDERLINE=2488
#constants
STYLE_DEFAULT=32

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

#To get font name, We need to allocate memory with in Scintilla's process, and then copy it out
	def text_getFontName(self,offset):
		style=winUser.sendMessage(self.windowHandle,SCI_GETSTYLEAT,offset,0)
		(processID,threadID)=winUser.getWindowThreadProcessID(self.windowHandle)
		processHandle=winKernel.openProcess(winKernel.PROCESS_VM_OPERATION|winKernel.PROCESS_VM_READ,False,processID)
		internalBuf=winKernel.virtualAllocEx(processHandle,None,100,winKernel.MEM_COMMIT,winKernel.PAGE_READWRITE)
		winUser.sendMessage(self.windowHandle,SCI_STYLEGETFONT,style, internalBuf)
		fontNameBuf=ctypes.create_string_buffer(100)
		winKernel.readProcessMemory(processHandle,internalBuf,fontNameBuf,100,None)
		winKernel.virtualFreeEx(processHandle,internalBuf,0,winKernel.MEM_RELEASE)
		return fontNameBuf.value



	def text_getFontSize(self,offset):
		style=winUser.sendMessage(self.windowHandle,SCI_GETSTYLEAT,offset,0)
		return winUser.sendMessage(self.windowHandle,SCI_STYLEGETSIZE,style,0)

	def text_isBold(self,offset):
		style=winUser.sendMessage(self.windowHandle,SCI_GETSTYLEAT,offset,0)
		return winUser.sendMessage(self.windowHandle,SCI_STYLEGETBOLD,style,0)

	def text_isItalic(self,offset):
		style=winUser.sendMessage(self.windowHandle,SCI_GETSTYLEAT,offset,0)
		return winUser.sendMessage(self.windowHandle,SCI_STYLEGETITALIC,style,0)

	def text_isUnderline(self,offset):
		style=winUser.sendMessage(self.windowHandle,SCI_GETSTYLEAT,offset,0)
		return winUser.sendMessage(self.windowHandle,SCI_STYLEGETUNDERLINE,style,0)

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

