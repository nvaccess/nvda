#cursorManager.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""
Implementation of cursor managers.
A cursor manager provides caret navigation and selection commands for a virtual text range.
"""

import baseObject
import gui.scriptUI
import textHandler
import api
import speech
import config

class CursorManager(baseObject.ScriptableObject):
	"""
	A mix-in providing caret navigation and selection commands for the object's virtual text range.
	This is required where a text range is not linked to a physical control and thus does not provide commands to move the cursor, select and copy text, etc.
	This base cursor manager requires that the text range being used stores its own caret and selection information.

	This is a mix-in class; i.e. it should be inherited alongside another L{baseObject.ScriptableObject}.
	The class into which it is inherited must provide a C{makeTextInfo(position)} method.

	@ivar selection: The current caret/selection range.
	@type selection: L{textHandler.TextInfo}
	"""

	_lastFindText=""

	def __init__(self, *args, **kwargs):
		super(CursorManager, self).__init__(*args, **kwargs)
		self.initCursorManager()

	def initCursorManager(self):
		"""Initialise this cursor manager.
		This must be called before the cursor manager functionality can be used.
		It is normally called by L{__init__}, but may not be if __class__ is reassigned.
		"""
		self._lastSelectionMovedStart=False
		self.bindToStandardKeys()

	def _get_selection(self):
		return self.makeTextInfo(textHandler.POSITION_SELECTION)

	def _set_selection(self, info):
		info.updateSelection()

	def _caretMovementScriptHelper(self,unit,direction=None,posConstant=textHandler.POSITION_SELECTION,posUnit=None,posUnitEnd=False,extraDetail=False):
		info=self.makeTextInfo(posConstant)
		info.collapse(end=not self._lastSelectionMovedStart)
		if posUnit is not None:
			info.expand(posUnit)
			info.collapse(end=posUnitEnd)
			if posUnitEnd:
				info.move(textHandler.UNIT_CHARACTER,-1)
		if direction is not None:
			info.expand(unit)
			info.collapse(end=posUnitEnd)
			info.move(unit,direction)
		self.selection=info
		info.expand(unit)
		if unit!=textHandler.UNIT_CHARACTER:
			if info.hasXML:
				speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,extraDetail=extraDetail,reason=speech.REASON_CARET)
			else:
				speech.speakFormattedText(info)
		else:
			if info.hasXML:
				speech.speakFormattedTextWithXML(info.XMLContext,None,info.obj,info.getXMLFieldSpeech,extraDetail=extraDetail,reason=speech.REASON_CARET)
			speech.speakSpelling(info.text)

	def doFindTextDialog(self):
		findDialog=gui.scriptUI.TextEntryDialog(_("Type the text you wish to find"),title=_("Find"),default=self._lastFindText,callback=self.doFindText)
		findDialog.run()

	def doFindText(self,text,reverse=False):
		if not text:
			return
		info=self.makeTextInfo(textHandler.POSITION_CARET)
		res=info.find(text,reverse=reverse)
		if res:
			self.selection=info
			speech.cancelSpeech()
			info.expand(textHandler.UNIT_LINE)
			if info.hasXML:
				speech.speakFormattedTextWithXML(info.XMLContext,info.XMLText,info.obj,info.getXMLFieldSpeech,extraDetail=False,reason=speech.REASON_CARET)
			else:
				speech.speakFormattedText(info)
		else:
			errorDialog=gui.scriptUI.MessageDialog(_("text \"%s\" not found")%text,title=_("Find Error"),style=gui.scriptUI.wx.OK|gui.scriptUI.wx.ICON_ERROR)
			errorDialog.run()
		CursorManager._lastFindText=text

	def script_find(self,keyPress): 
		self.doFindTextDialog()
	script_find.__doc__ = _("find a text string from the current cursor position")

	def script_findNext(self,keyPress):
		if not self._lastFindText:
			self.doFindTextDialog()
			return
		self.doFindText(self._lastFindText)
	script_findNext.__doc__ = _("find the next occurrence of the previously entered text string from the current cursor's position")

	def script_findPrevious(self,keyPress):
		if not self._lastFindText:
			self.doFindTextDialog()
			return
		self.doFindText(self._lastFindText,reverse=True)
	script_findPrevious.__doc__ = _("find the previous occurrence of the previously entered text string from the current cursor's position")

	def script_pageUp(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,-config.conf["virtualBuffers"]["linesPerPage"],extraDetail=False)

	def script_pageDown(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,config.conf["virtualBuffers"]["linesPerPage"],extraDetail=False)

	def script_moveByCharacter_back(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,-1,extraDetail=True)

	def script_moveByCharacter_forward(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,1,extraDetail=True)

	def script_moveByWord_back(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_WORD,-1,extraDetail=True)

	def script_moveByWord_forward(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_WORD,1,extraDetail=True)

	def script_moveByLine_back(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,-1)

	def script_moveByLine_forward(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,1)

	def script_moveByParagraph_back(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_PARAGRAPH,-1)

	def script_moveByParagraph_forward(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_PARAGRAPH,1)

	def script_startOfLine(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,posUnit=textHandler.UNIT_LINE,extraDetail=True)

	def script_endOfLine(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_CHARACTER,posUnit=textHandler.UNIT_LINE,posUnitEnd=True,extraDetail=True)

	def script_topOfDocument(self,keyPress):
		self._caretMovementScriptHelper(textHandler.UNIT_LINE,posConstant=textHandler.POSITION_FIRST)

	def script_bottomOfDocument(self,keyPress):
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

	def script_selectCharacter_forward(self,keyPress):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_CHARACTER,direction=1)

	def script_selectCharacter_back(self,keyPress):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_CHARACTER,direction=-1)

	def script_selectWord_forward(self,keyPress):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_WORD,direction=1)

	def script_selectWord_back(self,keyPress):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_WORD,direction=-1)

	def script_selectLine_forward(self,keyPress):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=1)

	def script_selectLine_back(self,keyPress):
		self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=-1)

	def script_selectToBeginningOfLine(self,keyPress):
		curInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		curInfo.collapse()
		tempInfo=curInfo.copy()
		tempInfo.expand(textHandler.UNIT_LINE)
		if curInfo.compareEndPoints(tempInfo,"startToStart")>0:
			self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=-1)

	def script_selectToEndOfLine(self,keyPress):
		curInfo=self.makeTextInfo(textHandler.POSITION_SELECTION)
		curInfo.collapse()
		tempInfo=curInfo.copy()
		curInfo.expand(textHandler.UNIT_CHARACTER)
		tempInfo.expand(textHandler.UNIT_LINE)
		if curInfo.compareEndPoints(tempInfo,"endToEnd")<0:
			self._selectionMovementScriptHelper(unit=textHandler.UNIT_LINE,direction=1)

	def script_selectToTopOfDocument(self,keyPress):
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_FIRST)

	def script_selectToBottomOfDocument(self,keyPress):
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_LAST,unit=textHandler.UNIT_CHARACTER,direction=1)

	def script_selectAll(self,keyPress):
		self._selectionMovementScriptHelper(toPosition=textHandler.POSITION_ALL)

	def script_copyToClipboard(self,keyPress):
		info=self.makeTextInfo(textHandler.POSITION_SELECTION)
		if info.isCollapsed:
			speech.speakMessage(_("no selection"))
			return
		if info.copyToClipboard():
			speech.speakMessage(_("copied to clipboard"))

	def bindToStandardKeys(self):
		"""Bind the standard navigation, selection and copy keys to the cursor manager scripts.
		"""
		for keyName, scriptName in (
			("extendedPrior","pageUp"),
			("extendedNext","pageDown"),
			("ExtendedUp","moveByLine_back"),
			("ExtendedDown","moveByLine_forward"),
			("ExtendedLeft","moveByCharacter_back"),
			("ExtendedRight","moveByCharacter_forward"),
			("Control+ExtendedLeft","moveByWord_back"),
			("Control+ExtendedRight","moveByWord_forward"),
			("Control+ExtendedUp","moveByParagraph_back"),
			("Control+ExtendedDown","moveByParagraph_forward"),
			("ExtendedHome","startOfLine"),
			("ExtendedEnd","endOfLine"),
			("control+ExtendedHome","topOfDocument"),
			("control+ExtendedEnd","bottomOfDocument"),
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
			("NVDA+Control+f","find"),
			("NVDA+f3","findNext"),
			("NVDA+shift+f3","findPrevious"),
		):
			self.bindKey_runtime(keyName, scriptName)

class ReviewCursorManager(CursorManager):
	"""
	A cursor manager used for review.
	This cursor manager maintains its own caret and selection information.
	Thus, the underlying text range need not support updating the caret or selection.
	"""

	def initCursorManager(self):
		super(ReviewCursorManager, self).initCursorManager()
		self._selection = super(ReviewCursorManager, self).makeTextInfo(textHandler.POSITION_SELECTION)

	def makeTextInfo(self, position):
		if position == textHandler.POSITION_SELECTION:
			return self.selection
		return super(ReviewCursorManager, self).makeTextInfo(position)

	def _get_selection(self):
		return self._selection.copy()

	def _set_selection(self, info):
		self._selection = info.copy()
