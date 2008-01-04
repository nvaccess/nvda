import win32clipboard
import win32con
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
import api

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
		self._lastSelectionMovedStart=False


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
		if hasattr(self,'_speech_XMLCache'):
			del self._speech_XMLCache
		startTime=time.time()
		speech.cancelSpeech()
		speech.speakMessage(_("Loading document..."))
		self._fillVBufHelper()
		endTime=time.time()
		globalVars.log.debug("load took %s seconds"%(endTime-startTime))
		speech.cancelSpeech()
		speech.speakMessage(_("Done"))
		api.processPendingEvents()
		info=self.makeTextInfo(textHandler.POSITION_FIRST)
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
				info.move(textHandler.UNIT_CHARACTER,-1)
		info.expand(unit)
		if direction is not None:
			info.collapse()
			info.move(unit,direction)
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

	def script_refreshBuffer(self,keyPress,nextScript):
		self.fillVBuf()

	def _selectionMovementScriptHelper(self,unit=None,direction=None,toPosition=None):
		oldInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		if toPosition:
			newInfo=self.makeTextInfo(toPosition)
			if newInfo.compareEndPoints(oldInfo,"startToStart")>0:
				newInfo.setEndPoint(oldInfo,"startToStart")
			if newInfo.compareEndPoints(oldInfo,"endToEnd")<0:
				newInfo.setEndPoint(oldInfo,"endToEnd")
		elif unit:
			newInfo=oldInfo.copy()
			if self._lastSelectionMovedStart:
				newInfo.move(unit,direction,endPoint="start")
			else:
				newInfo.move(unit,direction,endPoint="end")
		newInfo.updateSelection()
		if newInfo.compareEndPoints(oldInfo,"startToStart")!=0:
			self._lastSelectionMovedStart=True
		else:
			self._lastSelectionMovedStart=False
		if newInfo.compareEndPoints(oldInfo,"endToEnd")!=0:
			self._lastSelectionMovedStart=False
		speech.speakSelectionChange(oldInfo,newInfo)

	def script_selectCharacter_forward(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_CHARACTER,direction=1)

	def script_selectCharacter_back(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_CHARACTER,direction=-1)

	def script_selectCharacter_forward(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_CHARACTER,direction=1)

	def script_selectCharacter_back(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_CHARACTER,direction=-1)

	def script_selectWord_forward(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_WORD,direction=1)

	def script_selectWord_back(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_WORD,direction=-1)

	def script_selectLine_forward(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=1)

	def script_selectLine_back(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=-1)

	def script_selectToBeginningOfLine(self,keyPress,nextScript):
		curInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		tempInfo=curInfo.copy()
		tempInfo.expand(textHandler.UNIT_LINE)
		if curInfo.compareEndPoints(tempInfo,"startToStart")>0:
			self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=-1)

	def script_selectToEndOfLine(self,keyPress,nextScript):
		curInfo=self.makeTextInfo(textHandler.POSITION_CARET)
		tempInfo=curInfo.copy()
		curInfo.expand(textHandler.UNIT_CHARACTER)
		tempInfo.expand(textHandler.UNIT_LINE)
		if curInfo.compareEndPoints(tempInfo,"endToEnd")<0:
			self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=1)

	def script_selectToTopOfDocument(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_FIRST)

	def script_selectToBottomOfDocument(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_LAST)

	def script_selectAll(self,keyPress,nextScript):
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_ALL)

	def script_copyToClipboard(self,keyPress,nextScript):
		info=self.makeTextInfo(textHandler.POSITION_SELECTION)
		if info.isCollapsed:
			speech.speakMessage(_("no selection"))
			return
		#To handle line lengths properly, grab each line separately
		lineInfo=info.copy()
		lineInfo.collapse()
		textList=[]
		while lineInfo.compareEndPoints(info,"startToEnd")<0:
			lineInfo.expand(textHandler.UNIT_LINE)
			chunkInfo=lineInfo.copy()
			if chunkInfo.compareEndPoints(info,"startToStart")<0:
				chunkInfo.setEndPoint(info,"startToStart")
			if chunkInfo.compareEndPoints(info,"endToEnd")>0:
				chunkInfo.setEndPoint(info,"endToEnd")
			textList.append(chunkInfo.text)
			lineInfo.collapse(end=True)
		text="\n".join(textList).replace('\n\n','\n')
		win32clipboard.OpenClipboard()
		try:
			win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, text)
		finally:
			win32clipboard.CloseClipboard()
		win32clipboard.OpenClipboard() # there seems to be a bug so to retrieve unicode text we have to reopen the clipboard
		try:
			got = 	win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
		finally:
			win32clipboard.CloseClipboard()
		if got == text:
			speech.speakMessage(_("copied to clipboard"))


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
	("NVDA+f5","refreshBuffer"),
	("shift+extendedRight","selectCharacter_forward"),
	("shift+extendedLeft","selectCharacter_back"),
	("control+shift+extendedRight","selectWord_forward"),
	("control+shift+extendedLeft","selectWord_back"),
	("shift+extendedDown","selectLine_forward"),
	("shift+extendedUp","selectLine_back"),
	("shift+extendedEnd","selectToEndOfLine"),
	("shift+extendedHome","selectToBeginningOfLine"),
	("control+shift+extendedEnd","selectToBottomOfDocument"),
	("control+shift+extendedHome","selectToTopOfDocument"),
	("control+a","selectAll"),
	("control+c","copyToClipboard"),
]]
