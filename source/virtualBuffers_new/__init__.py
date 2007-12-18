from ctypes import *
from ctypes.wintypes import *
import debug
import speech
import NVDAObjects
import winUser
import controlTypes
import textHandler

testWindow=None
testVirtualBuffer=None

def update(window):
	global testWindow, testVirtualBuffer
	if not testWindow and winUser.getClassName(window)=="Internet Explorer_Server":
		testWindow=window
		testVirtualBuffer=VirtualBuffer(window)

def getVirtualBuffer(obj):
	if obj and (obj.windowHandle==testWindow or winUser.isDescendantWindow(testWindow,obj.windowHandle)):
		return testVirtualBuffer

VBufLib=cdll.virtualBuffer

class VirtualBufferTextInfo(NVDAObjects.NVDAObjectTextInfo):

	def _getSelectionOffsets(self):
		start=c_int()
		end=c_int()
		VBufLib.VBufStorage_getBufferSelectionOffsets(self.obj.VBufHandle,byref(start),byref(end))
		return (start.value,end.value)

	def _setSelectionOffsets(self,start,end):
		VBufLib.VBufStorage_setBufferSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return VBufLib.VBufStorage_getBufferTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		textLength=end-start
		textBuf=create_unicode_buffer(textLength)
		VBufLib.VBufStorage_getBufferTextByOffsets(self.obj.VBufHandle,start,end,textBuf)
		return textBuf.value

	def _getLineOffsets(self,offset):
		start=c_int()
		end=c_int()
		VBufLib.VBufStorage_getBufferLineOffsets(self.obj.VBufHandle,offset,byref(start),byref(end))
		return (start.value,end.value)

	def _get_XMLContext(self):
		offset=self._startOffset
		textLength=VBufLib.VBufStorage_getXMLContextAtBufferOffset(self.obj.VBufHandle,offset,None)
		textBuf=create_unicode_buffer(textLength)
		VBufLib.VBufStorage_getXMLContextAtBufferOffset(self.obj.VBufHandle,offset,textBuf)
		return textBuf.value

	def _get_XMLText(self):
		start=self._startOffset
		end=self._endOffset
		textLength=VBufLib.VBufStorage_getXMLBufferTextByOffsets(self.obj.VBufHandle,start,end,None)
		textBuf=create_unicode_buffer(textLength)
		VBufLib.VBufStorage_getXMLBufferTextByOffsets(self.obj.VBufHandle,start,end,textBuf)
		debug.writeMessage("xml text: %s"%textBuf.value)
		return textBuf.value

class VirtualBuffer(NVDAObjects.NVDAObject):

	def __init__(self,windowHandle=None):
		self.TextInfo=VirtualBufferTextInfo
		self.windowHandle=windowHandle
		self.VBufHandle=VBufLib.VBufStorage_createBuffer()
		self.fillVBuf()
		super(VirtualBuffer,self).__init__()

	def __del__(self):
		VBufLib.VBufStorage_destroyBuffer(self.VBufHandle)

	def fillVBuf(self,ID=None):
		VBufLib.VBufStorage_addFieldToBuffer(self.VBufHandle,1,0,controlTypes.ROLE_DOCUMENT,None,0,None,None)
		VBufLib.VBufStorage_addFieldToBuffer(self.VBufHandle,2,1,controlTypes.ROLE_HEADING,None,0,None,None)
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,2,u"NVDA Test Virtual Buffer")
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,1,u"\n\n")
		VBufLib.VBufStorage_addFieldToBuffer(self.VBufHandle,3,1,controlTypes.ROLE_PARAGRAPH,None,0,None,None)
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,3,u"Click here to visit the ")
		VBufLib.VBufStorage_addFieldToBuffer(self.VBufHandle,4,3,controlTypes.ROLE_LINK,None,0,None,None)
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,4,u"Community Page")
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,3,u" and check out our email lists.")
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,1,u"\n")
		VBufLib.VBufStorage_addFieldToBuffer(self.VBufHandle,5,1,controlTypes.ROLE_PARAGRAPH,None,0,None,None)
		VBufLib.VBufStorage_appendTextToBufferField(self.VBufHandle,5,u"Copyright 2007 NVDA contributers")
 



	def _caretMovementScriptHelper(self,unit,direction):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		info.expand(unit)
		info.collapse()
		info.moveByUnit(unit,direction)
		info.updateCaret()
		info.expand(unit)
		if unit in (textHandler.UNIT_CHARACTER,textHandler.UNIT_WORD):
			extraDetail=True
		else:
			extraDetail=False
		if unit==textHandler.UNIT_CHARACTER:
			speech.newSpeakFormattedText(info.XMLContext,None,info.obj,extraDetail=extraDetail)
			speech.speakSymbol(info.text)
		else:
			speech.newSpeakFormattedText(info.XMLContext,info.XMLText,info.obj,extraDetail=extraDetail)

	def script_moveByCharacter_back(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,-1)

	def script_moveByCharacter_forward(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,1)

	def script_moveByWord_back(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_WORD,-1)

	def script_moveByWord_forward(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_WORD,1)

	def script_moveByLine_back(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,-1)

	def script_moveByLine_forward(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,1)

	def script_startOfLine(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		info.expand(textHandler.UNIT_LINE)
		info.collapse()
		info.expand(textHandler.UNIT_CHARACTER)
		info.updateCaret()
		speech.speakSymbol(info.text)

	def script_endOfLine(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		info.expand(textHandler.UNIT_LINE)
		info.collapse(end=True)
		info.moveByUnit(textHandler.UNIT_CHARACTER,-1)
		info.expand(textHandler.UNIT_CHARACTER)
		info.updateCaret()
		speech.speakSymbol(info.text)

[VirtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine_back"),
	("ExtendedDown","moveByLine_forward"),
	("ExtendedLeft","moveByCharacter_back"),
	("ExtendedRight","moveByCharacter_forward"),
	("Control+ExtendedLeft","moveByWord_back"),
	("Control+ExtendedRight","moveByWord_forward"),
	("ExtendedHome","startOfLine"),
	("ExtendedEnd","endOfLine"),
]]
