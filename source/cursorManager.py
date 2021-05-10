#cursorManager.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Joseph Lee, Derek Riemer, Davy Kager
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""
Implementation of cursor managers.
A cursor manager provides caret navigation and selection commands for a virtual text range.
"""

import wx
import core
import baseObject
import documentBase
import gui
from gui import guiHelper
import gui.contextHelp
from speech import sayAll
import review
from scriptHandler import willSayAllResume, script
import textInfos
import api
import speech
import config
import braille
import vision
import controlTypes
from inputCore import SCRCAT_BROWSEMODE
import ui
from textInfos import DocumentWithPageTurns


class FindDialog(
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""A dialog used to specify text to find in a cursor manager.
	"""
	
	helpId = "SearchingForText"

	def __init__(self, parent, cursorManager, text, caseSensitivity, reverse=False):
		# Translators: Title of a dialog to find text.
		super().__init__(parent, title=_("Find"))

		# Have a copy of the active cursor manager, as this is needed later for finding text.
		self.activeCursorManager = cursorManager
		self.reverse = reverse
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		# Translators: Dialog text for NvDA's find command.
		findLabelText = _("Type the text you wish to find")
		self.findTextField = sHelper.addLabeledControl(findLabelText, wx.TextCtrl, value=text)
		# Translators: An option in find dialog to perform case-sensitive search.
		self.caseSensitiveCheckBox=wx.CheckBox(self,wx.ID_ANY,label=_("Case &sensitive"))
		self.caseSensitiveCheckBox.SetValue(caseSensitivity)
		sHelper.addItem(self.caseSensitiveCheckBox)
		sHelper.addDialogDismissButtons(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.CentreOnScreen()
		self.findTextField.SetFocus()

	def onOk(self, evt):
		text = self.findTextField.GetValue()
		caseSensitive = self.caseSensitiveCheckBox.GetValue()
		# We must use core.callLater rather than wx.CallLater to ensure that the callback runs within NVDA's core pump.
		# If it didn't, and it directly or indirectly called wx.Yield, it could start executing NVDA's core pump from within the yield, causing recursion.
		core.callLater(
			100,
			self.activeCursorManager.doFindText,
			text,
			caseSensitive=caseSensitive,
			reverse=self.reverse
		)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

class CursorManager(documentBase.TextContainerObject,baseObject.ScriptableObject):
	"""
	A mix-in providing caret navigation and selection commands for the object's virtual text range.
	This is required where a text range is not linked to a physical control and thus does not provide commands to move the cursor, select and copy text, etc.
	This base cursor manager requires that the text range being used stores its own caret and selection information.

	This is a mix-in class; i.e. it should be inherited alongside another L{baseObject.ScriptableObject}.
	The class into which it is inherited must provide a C{makeTextInfo(position)} method.

	@ivar selection: The current caret/selection range.
	@type selection: L{textInfos.TextInfo}
	"""

	# Translators: the script category for browse mode
	scriptCategory=SCRCAT_BROWSEMODE

	_lastFindText=""
	_lastCaseSensitivity=False

	def __init__(self, *args, **kwargs):
		super(CursorManager, self).__init__(*args, **kwargs)
		self.initCursorManager()

	def initOverlayClass(self):
		"""Performs automatic initialisation if this is being used as an overlay class."""
		self.initCursorManager()

	def initCursorManager(self):
		"""Initialise this cursor manager.
		This must be called before the cursor manager functionality can be used.
		It is normally called by L{__init__} or L{initOverlayClass}.
		"""
		self.isTextSelectionAnchoredAtStart=True

	def _get_selection(self):
		return self.makeTextInfo(textInfos.POSITION_SELECTION)

	def _set_selection(self, info):
		info.updateSelection()
		review.handleCaretMove(info)
		braille.handler.handleCaretMove(self)
		vision.handler.handleCaretMove(self)

	def _caretMovementScriptHelper(self,gesture,unit,direction=None,posConstant=textInfos.POSITION_SELECTION,posUnit=None,posUnitEnd=False,extraDetail=False,handleSymbols=False):
		oldInfo=self.makeTextInfo(posConstant)
		info=oldInfo.copy()
		info.collapse(end=self.isTextSelectionAnchoredAtStart)
		if self.isTextSelectionAnchoredAtStart and not oldInfo.isCollapsed:
			info.move(textInfos.UNIT_CHARACTER,-1)
		if posUnit is not None:
			# expand and collapse to ensure that we are aligned with the end of the intended unit
			info.expand(posUnit)
			try:
				info.collapse(end=posUnitEnd)
			except RuntimeError:
				# MS Word has a "virtual linefeed" at the end of the document which can cause RuntimeError to be raised.
				# In this case it can be ignored.
				# See #7009
				pass
			if posUnitEnd:
				info.move(textInfos.UNIT_CHARACTER,-1)
		if direction is not None:
			info.expand(unit)
			info.collapse(end=posUnitEnd)
			if info.move(unit,direction)==0 and isinstance(self,DocumentWithPageTurns):
				try:
					self.turnPage(previous=direction<0)
				except RuntimeError:
					pass
				else:
					info=self.makeTextInfo(textInfos.POSITION_FIRST if direction>0 else textInfos.POSITION_LAST)
		# #10343: Speak before setting selection because setting selection might
		# move the focus, which might mutate the document, potentially invalidating
		# info if it is offset-based.
		selection = info.copy()
		info.expand(unit)
		if not willSayAllResume(gesture):
			speech.speakTextInfo(info, unit=unit, reason=controlTypes.OutputReason.CARET)
		if not oldInfo.isCollapsed:
			speech.speakSelectionChange(oldInfo, selection)
		self.selection = selection

	def doFindText(self, text, reverse=False, caseSensitive=False, willSayAllResume=False):
		if not text:
			return
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		res=info.find(text,reverse=reverse,caseSensitive=caseSensitive)
		if res:
			self.selection=info
			speech.cancelSpeech()
			info.move(textInfos.UNIT_LINE,1,endPoint="end")
			if not willSayAllResume:
				speech.speakTextInfo(info, reason=controlTypes.OutputReason.CARET)
		else:
			wx.CallAfter(gui.messageBox,_('text "%s" not found')%text,_("Find Error"),wx.OK|wx.ICON_ERROR)
		CursorManager._lastFindText=text
		CursorManager._lastCaseSensitivity=caseSensitive

	def script_find(self, gesture, reverse=False):
		# #8566: We need this to be a modal dialog, but it mustn't block this script.
		def run():
			gui.mainFrame.prePopup()
			d = FindDialog(gui.mainFrame, self, self._lastFindText, self._lastCaseSensitivity, reverse)
			d.ShowModal()
			gui.mainFrame.postPopup()
		wx.CallAfter(run)
	# Translators: Input help message for NVDA's find command.
	script_find.__doc__ = _("find a text string from the current cursor position")

	@script(
		description=_(
			# Translators: Input help message for find next command.
			"find the next occurrence of the previously entered text string from the current cursor's position"
		),
		gesture="kb:NVDA+f3",
		resumeSayAllMode=sayAll.CURSOR.CARET,
	)
	def script_findNext(self,gesture):
		if not self._lastFindText:
			self.script_find(gesture)
			return
		self.doFindText(
			self._lastFindText,
			caseSensitive=self._lastCaseSensitivity,
			willSayAllResume=willSayAllResume(gesture),
		)

	@script(
		description=_(
			# Translators: Input help message for find previous command.
			"find the previous occurrence of the previously entered text string from the current cursor's position"
		),
		gesture="kb:NVDA+shift+f3",
		resumeSayAllMode=sayAll.CURSOR.CARET,
	)
	def script_findPrevious(self,gesture):
		if not self._lastFindText:
			self.script_find(gesture, reverse=True)
			return
		self.doFindText(
			self._lastFindText,
			reverse=True,
			caseSensitive=self._lastCaseSensitivity,
			willSayAllResume=willSayAllResume(gesture),
		)

	def script_moveByPage_back(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,-config.conf["virtualBuffers"]["linesPerPage"],extraDetail=False)
	script_moveByPage_back.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveByPage_forward(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,config.conf["virtualBuffers"]["linesPerPage"],extraDetail=False)
	script_moveByPage_forward.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveByCharacter_back(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_CHARACTER,-1,extraDetail=True,handleSymbols=True)

	def script_moveByCharacter_forward(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_CHARACTER,1,extraDetail=True,handleSymbols=True)

	def script_moveByWord_back(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_WORD,-1,extraDetail=True,handleSymbols=True)

	def script_moveByWord_forward(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_WORD,1,extraDetail=True,handleSymbols=True)

	def script_moveByLine_back(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,-1)
	script_moveByLine_back.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveByLine_forward(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,1)
	script_moveByLine_forward.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveBySentence_back(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_SENTENCE,-1)
	script_moveBySentence_back.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveBySentence_forward(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_SENTENCE,1)
	script_moveBySentence_forward.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveByParagraph_back(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_PARAGRAPH,-1)
	script_moveByParagraph_back.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_moveByParagraph_forward(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_PARAGRAPH,1)
	script_moveByParagraph_forward.resumeSayAllMode = sayAll.CURSOR.CARET

	def script_startOfLine(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_CHARACTER,posUnit=textInfos.UNIT_LINE,extraDetail=True,handleSymbols=True)

	def script_endOfLine(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_CHARACTER,posUnit=textInfos.UNIT_LINE,posUnitEnd=True,extraDetail=True,handleSymbols=True)

	def script_topOfDocument(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,posConstant=textInfos.POSITION_FIRST)

	def script_bottomOfDocument(self,gesture):
		self._caretMovementScriptHelper(gesture,textInfos.UNIT_LINE,posConstant=textInfos.POSITION_LAST)

	def _selectionMovementScriptHelper(self,unit=None,direction=None,toPosition=None):
		oldInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		# toPosition and unit might both be provided.
		# In this case, we move to the position before moving by the unit.
		if toPosition:
			newInfo=self.makeTextInfo(toPosition)
			if oldInfo.isCollapsed:
				self.isTextSelectionAnchoredAtStart = newInfo.compareEndPoints(oldInfo, "startToStart") >= 0
		elif unit:
			# position was not provided, so start from the old selection.
			newInfo = oldInfo.copy()
		if unit:
			if oldInfo.isCollapsed:
				# Starting a new selection, so set the selection direction
				# based on the direction of this movement.
				self.isTextSelectionAnchoredAtStart = direction > 0
			# Find the requested unit starting from the active end of the selection.
			# We can't just move the desired endpoint because this might cause
			# the end to move before the start in some cases
			# and some implementations don't support this.
			# For example, you might shift+rightArrow to select a character in the middle of a word
			# and then press shift+control+leftArrow to move to the previous word.
			newInfo.collapse(end=self.isTextSelectionAnchoredAtStart)
			newInfo.move(unit, direction, endPoint="start" if direction < 0 else "end")
			# Collapse this so we don't have to worry about which endpoint we used here.
			newInfo.collapse(end=direction > 0)
		# If we're selecting all, we're moving both endpoints.
		# Otherwise, newInfo is the collapsed new active endpoint
		# and we need to set the anchor endpoint.
		movingSingleEndpoint = toPosition != textInfos.POSITION_ALL
		if movingSingleEndpoint and not self.isTextSelectionAnchoredAtStart:
			if newInfo.compareEndPoints(oldInfo, "startToEnd") > 0:
				# We were selecting backwards, but now we're selecting forwards.
				# For example:
				# 1. Caret at 1
				# 2. Shift+leftArrow: selection (0, 1)
				# 3. Shift+control+rightArrow: next word at 3, so selection (1, 3)
				newInfo.setEndPoint(oldInfo, "startToEnd")
				self.isTextSelectionAnchoredAtStart = True
			else:
				# We're selecting backwards.
				# For example:
				# 1. Caret at 1; selection (1, 1)
				# 2. Shift+leftArrow: selection (0, 1)
				newInfo.setEndPoint(oldInfo, "endToEnd")
		elif movingSingleEndpoint:
			if newInfo.compareEndPoints(oldInfo, "startToStart") < 0:
				# We were selecting forwards, but now we're selecting backwards.
				# For example:
				# 1. Caret at 1
				# 2. Shift+rightArrow: selection (1, 2)
				# 3. Shift+control+leftArrow: previous word at 0, so selection (0, 1)
				newInfo.setEndPoint(oldInfo, "endToStart")
				self.isTextSelectionAnchoredAtStart = False
			else:
				# We're selecting forwards.
				# For example:
				# 1. Caret at 1; selection (1, 1)
				# 2. Shift+rightArrow: selection (1, 2)
				newInfo.setEndPoint(oldInfo, "startToStart")
		self.selection = newInfo
		speech.speakSelectionChange(oldInfo,newInfo)

	def script_selectCharacter_forward(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_CHARACTER,direction=1)

	def script_selectCharacter_back(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_CHARACTER,direction=-1)

	def script_selectWord_forward(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_WORD,direction=1)

	def script_selectWord_back(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_WORD,direction=-1)

	def script_selectLine_forward(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_LINE,direction=1)

	def script_selectLine_back(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_LINE,direction=-1)

	def script_selectPage_forward(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_LINE,direction=config.conf["virtualBuffers"]["linesPerPage"])

	def script_selectPage_back(self,gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_LINE,direction=-config.conf["virtualBuffers"]["linesPerPage"])

	def script_selectParagraph_forward(self, gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_PARAGRAPH, direction=1)

	def script_selectParagraph_back(self, gesture):
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_PARAGRAPH, direction=-1)

	def script_selectToBeginningOfLine(self,gesture):
		# Make sure the active endpoint of the selection is after the start of the line.
		sel=self.makeTextInfo(textInfos.POSITION_SELECTION)
		line=sel.copy()
		line.collapse()
		line.expand(textInfos.UNIT_LINE)
		compOp="startToStart" if not self.isTextSelectionAnchoredAtStart else "endToStart"
		if sel.compareEndPoints(line,compOp)>0:
			self._selectionMovementScriptHelper(unit=textInfos.UNIT_LINE,direction=-1)

	def script_selectToEndOfLine(self,gesture):
		# #7157: There isn't necessarily a line ending character or insertion point at the end of a line.
		# Therefore, always allow select to end of line,
		# even if the caret is already on the last character of the line.
		self._selectionMovementScriptHelper(unit=textInfos.UNIT_LINE,direction=1)

	def script_selectToTopOfDocument(self,gesture):
		self._selectionMovementScriptHelper(toPosition=textInfos.POSITION_FIRST)

	def script_selectToBottomOfDocument(self,gesture):
		self._selectionMovementScriptHelper(toPosition=textInfos.POSITION_LAST,unit=textInfos.UNIT_CHARACTER,direction=1)

	def script_selectAll(self,gesture):
		self._selectionMovementScriptHelper(toPosition=textInfos.POSITION_ALL)

	def script_copyToClipboard(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_SELECTION)
		if info.isCollapsed:
			# Translators: Reported when there is no text selected (for copying).
			ui.message(_("No selection"))
			return
		info.copyToClipboard(notify=True)

	def reportSelectionChange(self, oldTextInfo):
		newInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		speech.speakSelectionChange(oldTextInfo,newInfo)
		braille.handler.handleCaretMove(self)

	__gestures = {
		"kb:pageUp": "moveByPage_back",
		"kb:pageDown": "moveByPage_forward",
		"kb:upArrow": "moveByLine_back",
		"kb:downArrow": "moveByLine_forward",
		"kb:leftArrow": "moveByCharacter_back",
		"kb:rightArrow": "moveByCharacter_forward",
		"kb:control+leftArrow": "moveByWord_back",
		"kb:control+rightArrow": "moveByWord_forward",
		"kb:control+upArrow": "moveByParagraph_back",
		"kb:control+downArrow": "moveByParagraph_forward",
		"kb:home": "startOfLine",
		"kb:end": "endOfLine",
		"kb:control+home": "topOfDocument",
		"kb:control+end": "bottomOfDocument",
		"kb:shift+rightArrow": "selectCharacter_forward",
		"kb:shift+leftArrow": "selectCharacter_back",
		"kb:shift+control+rightArrow": "selectWord_forward",
		"kb:shift+control+leftArrow": "selectWord_back",
		"kb:shift+downArrow": "selectLine_forward",
		"kb:shift+upArrow": "selectLine_back",
		"kb:shift+pageDown": "selectPage_forward",
		"kb:shift+pageUp": "selectPage_back",
		"kb:shift+control+downArrow": "selectParagraph_forward",
		"kb:shift+control+upArrow": "selectParagraph_back",
		"kb:shift+end": "selectToEndOfLine",
		"kb:shift+home": "selectToBeginningOfLine",
		"kb:shift+control+end": "selectToBottomOfDocument",
		"kb:shift+control+home": "selectToTopOfDocument",
		"kb:control+a": "selectAll",
		"kb:control+c": "copyToClipboard",
		"kb:NVDA+Control+f": "find",
		"kb:alt+upArrow":"moveBySentence_back",
		"kb:alt+downArrow":"moveBySentence_forward",
	}

class _ReviewCursorManagerTextInfo(textInfos.TextInfo):
	"""For use with L{ReviewCursorManager}.
	Overrides L{updateCaret} and L{updateSelection} to use the selection property on the underlying object.
	"""

	def updateCaret(self):
		info=self.copy()
		info.collapse()
		self.obj._selection = info

	def updateSelection(self):
		self.obj._selection = self.copy()

class ReviewCursorManager(CursorManager):
	"""
	A cursor manager used for review.
	This cursor manager maintains its own caret and selection information.
	Thus, the underlying text range need not support updating the caret or selection.
	"""

	def initCursorManager(self):
		super(ReviewCursorManager, self).initCursorManager()
		realTI = self.TextInfo
		self.TextInfo = type("ReviewCursorManager_%s" % realTI.__name__, (_ReviewCursorManagerTextInfo, realTI), {})
		self._selection = self.makeTextInfo(textInfos.POSITION_FIRST)

	def makeTextInfo(self, position):
		if position == textInfos.POSITION_SELECTION:
			return self._selection.copy()
		elif position == textInfos.POSITION_CARET:
			sel = self._selection.copy()
			sel.collapse()
			return sel
		return super(ReviewCursorManager, self).makeTextInfo(position)
