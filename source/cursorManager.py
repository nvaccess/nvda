import weakref
import baseObject
import textHandler
import api

class CursorManager(baseObject.AutoPropertyObject):

	def __init__(self, obj):
		self._obj = weakref.ref(obj)
		self._lastSelectionMovedStart=False

	def _get_obj(self):
		return self._obj()

	def makeTextInfo(self, position):
		return self.obj.makeTextInfo(position)

	def _get_caret(self):
		return self.obj.makeTextInfo(POSITION_CARETT)

	def _set_caret(self, info):
		info.updateCaret()

	def _get_selection(self):
		return self.obj.makeTextInfo(POSITION_SELECTIONT)

	def _set_selection(self, info):
		info.updateSelection()

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
		self.caret = info
		if unit!=textHandler.UNIT_CHARACTER:
			speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,extraDetail=extraDetail,reason=speech.REASON_CARET)
		else:
			speech.speakFormattedTextWithXML(info.XMLContext,None,info.obj,info.getXMLFieldSpeech,extraDetail=extraDetail,reason=speech.REASON_CARET)
			speech.speakSpelling(info.text)

	def script_pageUp(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,-config.conf["virtualBuffers"]["linesPerPage"],extraDetail=False)

	def script_pageDown(self,keyPress,nextScript):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,config.conf["virtualBuffers"]["linesPerPage"],extraDetail=False)

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
		if unit:
			if self._lastSelectionMovedStart:
				newInfo.move(unit,direction,endPoint="start")
			else:
				newInfo.move(unit,direction,endPoint="end")
		self.selection = newInfo
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
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_LAST,unit=textHandler.UNIT_CHARACTER,direction=1)

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
		if api.copyToClip(text):
			speech.speakMessage(_("copied to clipboard"))

class ReviewCursorManager(CursorManager):

	def __init__(self, obj, startSelection):
		super(ReviewCursorManager, self).__init__(obj)
		self._selection = startSelection
	
	def makeTextInfo(self, position):
		if position in (POSITION_CARET, POSITION_SELECTION):
			return self._selection
		return super(ReviewCursorManager, self).makeTextInfo(position)
	def _get_selection(self):
		return self._selection

	def _set_selection(self, info):
		self._selection = info

	_get_caret = _get_selection
	_set_caret = _set_selection
