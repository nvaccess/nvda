import weakref
import speech
import NVDAObjects
import winUser
import controlTypes
import textHandler
from virtualBuffer_new_wrapper import *

class VirtualBufferTextInfo(NVDAObjects.NVDAObjectTextInfo):

	def _getSelectionOffsets(self):
		return VBufStorage_getBufferSelectionOffsets(self.obj.VBufHandle)

	def _setSelectionOffsets(self,start,end):
		VBufStorage_setBufferSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return VBufStorage_getBufferTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		return VBufStorage_getBufferTextByOffsets(self.obj.VBufHandle,start,end)

	def _getLineOffsets(self,offset):
		return VBufStorage_getBufferLineOffsets(self.obj.VBufHandle,offset)

	def _get_XMLContext(self):
		return VBufStorage_getXMLContextAtBufferOffset(self.obj.VBufHandle,offset)

	def _get_XMLText(self):
		start=self._startOffset
		end=self._endOffset
		return VBufStorage_getXMLBufferTextByOffsets(self.obj.VBufHandle,start,end)

class VirtualBuffer(NVDAObjects.NVDAObject):

	def __init__(self,rootNVDAObject):
		self.TextInfo=VirtualBufferTextInfo
		self._rootNVDAObject=weakref.ref(rootNVDAObject)
		self.VBufHandle=VBufStorage_createBuffer(0)
		self.fillVBuf()
		super(VirtualBuffer,self).__init__()

	def __del__(self):
		VBufStorage_destroyBuffer(self.VBufHandle)

	def isNVDAObjectInVirtualBuffer(self,obj):
		pass

	def isAlive(self):
		pass

	def fillVBuf(self,ID=None):
 		pass

	def getFieldSpeech(self,attrs,fieldType,extraDetail=False):
		pass

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
			speech.speakFormattedTextWithXML(info.XMLContext,None,info.obj,self.getFieldSpeech,extraDetail=extraDetail)
			speech.speakSymbol(info.text)
		else:
			speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,self.getFieldspeech,extraDetail=extraDetail)

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
