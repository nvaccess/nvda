import weakref
from textwrap import TextWrapper
import time
import winsound
import baseObject
import speech
import NVDAObjects
import winUser
import sayAllHandler
import controlTypes
import textHandler
from virtualBuffer_new_wrapper import *
import globalVars
import config

class VirtualBufferTextInfo(NVDAObjects.NVDAObjectTextInfo):

	hasXML=True

	def _getSelectionOffsets(self):
		start,end=VBufStorage_getBufferSelectionOffsets(self.obj.VBufHandle)
		return (start,end)

	def _setSelectionOffsets(self,start,end):
		VBufStorage_setBufferSelectionOffsets(self.obj.VBufHandle,start,end)

	def _getCaretOffset(self):
		return self._getSelectionOffsets()[0]

	def _setCaretOffset(self,offset):
		return self._setSelectionOffsets(offset,offset)

	def _getStoryLength(self):
		return VBufStorage_getBufferTextLength(self.obj.VBufHandle)

	def _getTextRange(self,start,end):
		text=VBufStorage_getBufferTextByOffsets(self.obj.VBufHandle,start,end)
		return text

	def _getLineOffsets(self,offset):
		return VBufStorage_getBufferLineOffsets(self.obj.VBufHandle,offset)

	def _get_XMLContext(self):
		return VBufStorage_getXMLContextAtBufferOffset(self.obj.VBufHandle,self._startOffset)

	def _get_XMLText(self):
		start=self._startOffset
		end=self._endOffset
		text=VBufStorage_getXMLBufferTextByOffsets(self.obj.VBufHandle,start,end)
		return text

class VirtualBuffer(baseObject.scriptableObject):

	def __init__(self,rootNVDAObject,TextInfo=VirtualBufferTextInfo):
		self.TextInfo=TextInfo
		self.rootNVDAObject=rootNVDAObject
		self.VBufHandle=VBufStorage_createBuffer()
		self.fillVBuf()
		super(VirtualBuffer,self).__init__()

	def __del__(self):
		VBufStorage_destroyBuffer(self.VBufHandle)

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def isNVDAObjectInVirtualBuffer(self,obj):
		pass

	def isAlive(self):
		pass

	def _calculateLineBreaks(self,text):
		maxLineLength=config.conf["virtualBuffers"]["maxLineLength"]
		lastBreak=0
		lineBreakOffsets=[]
		for offset in range(len(text)):
			if offset-lastBreak>maxLineLength and offset>0 and text[offset-1].isspace() and not text[offset].isspace():
				lineBreakOffsets.append(offset)
				lastBreak=offset
		return lineBreakOffsets

	def _fillVBufHelper(self):
		pass

	def fillVBuf(self):
		VBufStorage_clearBuffer(self.VBufHandle)
		startTime=time.time()
		speech.cancelSpeech()
		speech.speakMessage(_("Loading document..."))
		self._fillVBufHelper()
		endTime=time.time()
		globalVars.log.warning("load took %s seconds"%(endTime-startTime))
		speech.cancelSpeech()
		speech.speakMessage(_("Done"))
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		sayAllHandler.readText(info,sayAllHandler.CURSOR_CARET)

	def activatePosition(self,ID):
		pass

	def script_activatePosition(self,keyPress,nextScript):
		start,end=VBufStorage_getBufferSelectionOffsets(self.VBufHandle)
		ID=VBufStorage_getFieldIDFromBufferOffset(self.VBufHandle,start)
		self.activatePosition(ID)

	def _caretMovementScriptHelper(self,unit,direction=None,posConstant=textHandler.POSITION_CARET,posUnit=None,posUnitEnd=False,extraDetail=False):
		info=self.makeTextInfo(posConstant)
		info.collapse()
		if posUnit is not None:
			info.expand(posUnit)
			info.collapse(end=posUnitEnd)
			if posUnitEnd:
				info.moveByUnit(textHandler.UNIT_CHARACTER,-1)
		info.expand(unit)
		if direction is not None:
			info.collapse()
			info.moveByUnit(unit,direction)
			info.expand(unit)
		info.updateCaret()
		if unit!=textHandler.UNIT_CHARACTER:
			speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,extraDetail=extraDetail)
		else:
			speech.speakFormattedTextWithXML(info.XMLContext,None,info.obj,info.getXMLFieldSpeech,extraDetail=extraDetail)
			speech.speakSpelling(info.text)

	def script_moveByCharacter_back(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,-1,extraDetail=True)

	def script_moveByCharacter_forward(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,1,extraDetail=True)

	def script_moveByWord_back(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_WORD,-1,extraDetail=True)

	def script_moveByWord_forward(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_WORD,1,extraDetail=True)

	def script_moveByLine_back(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,-1)

	def script_moveByLine_forward(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,1)

	def script_startOfLine(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,posUnit=textHandler.UNIT_LINE,extraDetail=True)

	def script_endOfLine(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,posUnit=textHandler.UNIT_LINE,posUnitEnd=True,extraDetail=True)

	def script_topOfDocument(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,posConstant=textHandler.POSITION_FIRST)

	def script_bottomOfDocument(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,posConstant=textHandler.POSITION_LAST)

[VirtualBuffer.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine_back"),
	("ExtendedDown","moveByLine_forward"),
	("ExtendedLeft","moveByCharacter_back"),
	("ExtendedRight","moveByCharacter_forward"),
	("Control+ExtendedLeft","moveByWord_back"),
	("Control+ExtendedRight","moveByWord_forward"),
	("ExtendedHome","startOfLine"),
	("ExtendedEnd","endOfLine"),
	("control+ExtendedHome","topOfDocument"),
	("control+ExtendedEnd","bottomOfDocument"),
	("Return","activatePosition"),
	("Space","activatePosition"),
]]
