# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access, Cyrille Bougot and other NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from comtypes import COMError
import ctypes
import operator
import uuid
import time
from logHandler import log
import winUser
import speech
import braille
import controlTypes
import config
import tableUtils
import textInfos
import eventHandler
import scriptHandler
from scriptHandler import script
import ui
from . import IAccessible
from displayModel import EditableTextDisplayModelTextInfo
from ..behaviors import EditableTextWithoutAutoSelectDetection
import NVDAObjects.window.winword as winWordWindowModule
from speech import sayAll
import inputCore
from globalCommands import SCRCAT_SYSTEMCARET

class WordDocument(IAccessible, EditableTextWithoutAutoSelectDetection, winWordWindowModule.WordDocument):

	treeInterceptorClass = winWordWindowModule.WordDocumentTreeInterceptor
	shouldCreateTreeInterceptor=False
	TextInfo = winWordWindowModule.WordDocumentTextInfo
	# Should braille and review position be updated, set to True in
	# L{script_updateBrailleAndReviewPosition}.
	_fromUpdateBrailleAndReviewPosition = False

	def _get_ignoreEditorRevisions(self):
		try:
			ignore=not self.WinwordWindowObject.view.showRevisionsAndComments
		except COMError:
			log.debugWarning("showRevisionsAndComments",exc_info=True)
			ignore=False
		self.ignoreEditorRevisions=ignore
		return ignore

	#: True if page numbers (as well as section numbers and column numbers) should be ignored. Such as in outlook.
	ignorePageNumbers = False

	#: True if formatting should be ignored (text only) such as for spellCheck error field
	ignoreFormatting=False

	def event_caret(self) -> None:
		curSelectionPos=self.makeTextInfo(textInfos.POSITION_SELECTION)
		lastSelectionPos=getattr(self,'_lastSelectionPos',None)
		self._lastSelectionPos=curSelectionPos
		if lastSelectionPos:
			if curSelectionPos._rangeObj.isEqual(lastSelectionPos._rangeObj):
				if self._fromUpdateBrailleAndReviewPosition:
					super().event_caret()
					self._fromUpdateBrailleAndReviewPosition = False
				return
		super(WordDocument,self).event_caret()

	def _get_role(self):
		return controlTypes.Role.EDITABLETEXT

	def _get_states(self):
		states=super(WordDocument,self).states
		states.add(controlTypes.State.MULTILINE)
		return states

	def populateHeaderCellTrackerFromHeaderRows(self,headerCellTracker,table):
		rows=table.rows
		numHeaderRows=0
		for rowIndex in range(rows.count): 
			try:
				row=rows.item(rowIndex+1)
			except COMError:
				break
			try:
				headingFormat=row.headingFormat
			except (COMError,AttributeError,NameError):
				headingFormat=0
			if headingFormat==-1: # is a header row
				numHeaderRows+=1
			else:
				break
		if numHeaderRows>0:
			headerCellTracker.addHeaderCellInfo(rowNumber=1,columnNumber=1,rowSpan=numHeaderRows,isColumnHeader=True,isRowHeader=False)

	def populateHeaderCellTrackerFromBookmarks(self,headerCellTracker,bookmarks):
		for x in bookmarks: 
			name=x.name
			lowerName=name.lower()
			isColumnHeader=isRowHeader=False
			if lowerName.startswith('title'):
				isColumnHeader=isRowHeader=True
			elif lowerName.startswith('columntitle'):
				isColumnHeader=True
			elif lowerName.startswith('rowtitle'):
				isRowHeader=True
			else:
				continue
			try:
				headerCell=x.range.cells.item(1)
			except COMError:
				continue
			headerCellTracker.addHeaderCellInfo(rowNumber=headerCell.rowIndex,columnNumber=headerCell.columnIndex,name=name,isColumnHeader=isColumnHeader,isRowHeader=isRowHeader)

	_curHeaderCellTrackerTable=None
	_curHeaderCellTracker=None
	def getHeaderCellTrackerForTable(self,table):
		tableRange=table.range
		# Sometimes there is a valid reference in _curHeaderCellTrackerTable,
		# but we get a COMError when accessing the range (#6827)
		try:
			tableRangesEqual=tableRange.isEqual(self._curHeaderCellTrackerTable.range)
		except (COMError, AttributeError):
			tableRangesEqual=False
		if not tableRangesEqual:
			self._curHeaderCellTracker = tableUtils.HeaderCellTracker()
			self.populateHeaderCellTrackerFromBookmarks(self._curHeaderCellTracker,tableRange.bookmarks)
			self.populateHeaderCellTrackerFromHeaderRows(self._curHeaderCellTracker,table)
			self._curHeaderCellTrackerTable=table
		return self._curHeaderCellTracker

	def setAsHeaderCell(self,cell,isColumnHeader=False,isRowHeader=False):
		rowNumber=cell.rowIndex
		columnNumber=cell.columnIndex
		headerCellTracker=self.getHeaderCellTrackerForTable(cell.range.tables[1])
		oldInfo=headerCellTracker.getHeaderCellInfoAt(rowNumber,columnNumber)
		if oldInfo:
			if isColumnHeader and not oldInfo.isColumnHeader:
				oldInfo.isColumnHeader=True
			elif isRowHeader and not oldInfo.isRowHeader:
				oldInfo.isRowHeader=True
			else:
				return False
			isColumnHeader=oldInfo.isColumnHeader
			isRowHeader=oldInfo.isRowHeader
		if isColumnHeader and isRowHeader:
			name="Title_"
		elif isRowHeader:
			name="RowTitle_"
		elif isColumnHeader:
			name="ColumnTitle_"
		else:
			raise ValueError("One or both of isColumnHeader or isRowHeader must be True")
		name += uuid.uuid4().hex
		if oldInfo:
			self.WinwordDocumentObject.bookmarks[oldInfo.name].delete()
			oldInfo.name=name
		else:
			headerCellTracker.addHeaderCellInfo(rowNumber=rowNumber,columnNumber=columnNumber,name=name,isColumnHeader=isColumnHeader,isRowHeader=isRowHeader)
		self.WinwordDocumentObject.bookmarks.add(name,cell.range)
		return True

	def forgetHeaderCell(self,cell,isColumnHeader=False,isRowHeader=False):
		rowNumber=cell.rowIndex
		columnNumber=cell.columnIndex
		if not isColumnHeader and not isRowHeader: 
			return False
		headerCellTracker=self.getHeaderCellTrackerForTable(cell.range.tables[1])
		info=headerCellTracker.getHeaderCellInfoAt(rowNumber,columnNumber)
		if not info or not hasattr(info,'name'):
			return False
		if isColumnHeader and info.isColumnHeader:
			info.isColumnHeader=False
		elif isRowHeader and info.isRowHeader:
			info.isRowHeader=False
		else:
			return False
		headerCellTracker.removeHeaderCellInfo(info)
		self.WinwordDocumentObject.bookmarks(info.name).delete()
		if info.isColumnHeader or info.isRowHeader:
			self.setAsHeaderCell(cell,isColumnHeader=info.isColumnHeader,isRowHeader=info.isRowHeader)
		return True

	def fetchAssociatedHeaderCellText(self,cell,columnHeader=False):
		table=cell.range.tables[1]
		rowNumber=cell.rowIndex
		columnNumber=cell.columnIndex
		headerCellTracker=self.getHeaderCellTrackerForTable(table)
		for info in headerCellTracker.iterPossibleHeaderCellInfosFor(rowNumber,columnNumber,columnHeader=columnHeader):
			textList=[]
			if columnHeader:
				for headerRowNumber in range(info.rowNumber,info.rowNumber+info.rowSpan): 
					tempColumnNumber=columnNumber
					while tempColumnNumber>=1:
						try:
							headerCell=table.cell(headerRowNumber,tempColumnNumber)
						except COMError:
							tempColumnNumber-=1
							continue
						break
					textList.append(headerCell.range.text)
			else:
				for headerColumnNumber in range(info.columnNumber,info.columnNumber+info.colSpan): 
					tempRowNumber=rowNumber
					while tempRowNumber>=1:
						try:
							headerCell=table.cell(tempRowNumber,headerColumnNumber)
						except COMError:
							tempRowNumber-=1
							continue
						break
					textList.append(headerCell.range.text)
			text=" ".join(textList)
			if text:
				return text

	@script(
		gesture="kb:NVDA+shift+c",
		description=_(
			# Translators: The label of a shortcut of NVDA.
			"Set column header. Pressing once will set this cell as the first column header for any cell lower and "
			"to the right of it within this table. Pressing twice will forget the current column header for this "
			"cell."
		),
		category=SCRCAT_SYSTEMCARET
	)
	def script_setColumnHeader(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		try:
			cell=self.WinwordSelectionObject.cells[1]
		except COMError:
			# Translators: a message when trying to perform an action on a cell when not in one in Microsoft word
			ui.message(_("Not in a table cell"))
			return
		if scriptCount==0:
			if self.setAsHeaderCell(cell,isColumnHeader=True,isRowHeader=False):
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Set row {rowNumber} column {columnNumber} as start of column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Already set row {rowNumber} column {columnNumber} as start of column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
		elif scriptCount==1:
			if self.forgetHeaderCell(cell,isColumnHeader=True,isRowHeader=False):
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Removed row {rowNumber} column {columnNumber}  from column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetColumnHeader script for Microsoft Word.
				ui.message(_("Cannot find row {rowNumber} column {columnNumber}  in column headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))

	@script(
		gesture="kb:NVDA+shift+r",
		description=_(
			# Translators: The label of a shortcut of NVDA.
			"Set row header. Pressing once will set this cell as the first row header for any cell lower and to the "
			"right of it within this table. Pressing twice will forget the current row header for this cell."
		),
		category=SCRCAT_SYSTEMCARET
	)
	def script_setRowHeader(self,gesture):
		scriptCount=scriptHandler.getLastScriptRepeatCount()
		try:
			cell=self.WinwordSelectionObject.cells[1]
		except COMError:
			# Translators: a message when trying to perform an action on a cell when not in one in Microsoft word
			ui.message(_("Not in a table cell"))
			return
		if scriptCount==0:
			if self.setAsHeaderCell(cell,isColumnHeader=False,isRowHeader=True):
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Set row {rowNumber} column {columnNumber} as start of row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Already set row {rowNumber} column {columnNumber} as start of row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
		elif scriptCount==1:
			if self.forgetHeaderCell(cell,isColumnHeader=False,isRowHeader=True):
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Removed row {rowNumber} column {columnNumber}  from row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))
			else:
				# Translators: a message reported in the SetRowHeader script for Microsoft Word.
				ui.message(_("Cannot find row {rowNumber} column {columnNumber}  in row headers").format(rowNumber=cell.rowIndex,columnNumber=cell.columnIndex))

	@script(
		gestures=(
			"kb:alt+home",
			"kb:alt+end",
			"kb:alt+pageUp",
			"kb:alt+pageDown"
		)
	)
	def script_caret_moveByCell(self, gesture: inputCore.InputGesture) -> None:
		info = self.makeTextInfo(textInfos.POSITION_SELECTION)
		inTable = info._rangeObj.tables.count > 0
		if not inTable:
			gesture.send()
			return
		oldSelection = info.start, info.end
		gesture.send()
		start = time.time()
		retryInterval = 0.01
		maxTimeout = 0.15
		elapsed = 0
		while True:
			if scriptHandler.isScriptWaiting():
				# Prevent lag if keys are pressed rapidly
				return
			info = self.makeTextInfo(textInfos.POSITION_SELECTION)
			newSelection = info.start, info.end
			if newSelection != oldSelection:
				elapsed = time.time() - start
				log.debug(f"Detected new selection after {elapsed} sec")
				break
			elapsed = time.time() - start
			if elapsed >= maxTimeout:
				log.debug(f"Canceled detecting new selection after {elapsed} sec")
				break
			time.sleep(retryInterval)
		info.expand(textInfos.UNIT_CELL)
		speech.speakTextInfo(info, reason=controlTypes.OutputReason.FOCUS)
		braille.handler.handleCaretMove(self)

	@script(
		# Translators: a description for a script
		description=_("Reports the text of the comment where the system caret is located."),
		gesture="kb:NVDA+alt+c",
		category=SCRCAT_SYSTEMCARET,
		speakOnDemand=True,
	)
	def script_reportCurrentComment(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		fields=info.getTextWithFields(formatConfig={'reportComments':True})
		for field in reversed(fields):
			if isinstance(field,textInfos.FieldCommand) and isinstance(field.field,textInfos.FormatField): 
				commentReference=field.field.get('comment')
				if commentReference:
					offset=int(commentReference)
					textRange=self.WinwordDocumentObject.range(offset, offset + 1)
					try:
						text = textRange.comments[1].range.text
					except COMError:
						break
					if text:
						ui.message(text)
						return
		# Translators: a message when there is no comment to report in Microsoft Word
		ui.message(_("No comments"))

	def _moveInTable(self,row=True,forward=True):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		info.expand(textInfos.UNIT_CHARACTER)
		formatConfig=config.conf['documentFormatting'].copy()
		formatConfig['reportTables']=True
		commandList=info.getTextWithFields(formatConfig)
		if len(commandList)<3 or commandList[1].field.get('role',None)!=controlTypes.Role.TABLE or commandList[2].field.get('role',None)!=controlTypes.Role.TABLECELL:
			# Translators: The message reported when a user attempts to use a table movement command
			# when the cursor is not withnin a table.
			ui.message(_("Not in table"))
			return False
		rowCount=commandList[1].field.get('table-rowcount',1)
		columnCount=commandList[1].field.get('table-columncount',1)
		rowNumber=commandList[2].field.get('table-rownumber',1)
		columnNumber=commandList[2].field.get('table-columnnumber',1)
		try:
			table=info._rangeObj.tables[1]
		except COMError:
			log.debugWarning("Could not get MS Word table object indicated in XML")
			ui.message(_("Not in table"))
			return False
		_cell=table.cell
		getCell=lambda thisIndex,otherIndex: _cell(thisIndex,otherIndex) if row else _cell(otherIndex,thisIndex)
		thisIndex=rowNumber if row else columnNumber
		otherIndex=columnNumber if row else rowNumber
		thisLimit=(rowCount if row else columnCount) if forward else 1
		limitOp = operator.le if forward else operator.ge
		incdecFunc = operator.add if forward else operator.sub
		foundCell=None
		curOtherIndex=otherIndex
		while curOtherIndex>0:
			curThisIndex=incdecFunc(thisIndex,1)
			while limitOp(curThisIndex,thisLimit):
				try:
					foundCell=getCell(curThisIndex,curOtherIndex).range
				except COMError:
					pass
				if foundCell: break
				curThisIndex=incdecFunc(curThisIndex,1)
			if foundCell: break
			curOtherIndex-=1
		if not foundCell:
			ui.message(_("Edge of table"))
			return False
		newInfo = winWordWindowModule.WordDocumentTextInfo(
			self, textInfos.POSITION_CARET, _rangeObj=foundCell
		)
		speech.speakTextInfo(newInfo, reason=controlTypes.OutputReason.CARET, unit=textInfos.UNIT_CELL)
		newInfo.collapse()
		newInfo.updateCaret()
		return True

	@script(
		gesture="kb:control+alt+downArrow"
	)
	def script_nextRow(self,gesture):
		self._moveInTable(row=True,forward=True)

	@script(
		gesture="kb:control+alt+upArrow"
	)
	def script_previousRow(self,gesture):
		self._moveInTable(row=True,forward=False)

	@script(
		gesture="kb:control+alt+rightArrow"
	)
	def script_nextColumn(self,gesture):
		self._moveInTable(row=False,forward=True)

	@script(
		gesture="kb:control+alt+leftArrow"
	)
	def script_previousColumn(self,gesture):
		self._moveInTable(row=False,forward=False)

	@script(
		gesture="kb:control+downArrow",
		resumeSayAllMode=sayAll.CURSOR.CARET
	)
	def script_nextParagraph(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		# #4375: can't use self.move here as it may check document.chracters.count which can take for ever on large documents.
		info._rangeObj.move(winWordWindowModule.wdParagraph, 1)
		info.updateCaret()
		self._caretScriptPostMovedHelper(textInfos.UNIT_PARAGRAPH,gesture,None)

	@script(
		gesture="kb:control+upArrow",
		resumeSayAllMode=sayAll.CURSOR.CARET
	)
	def script_previousParagraph(self,gesture):
		info=self.makeTextInfo(textInfos.POSITION_CARET)
		# #4375: keeping symmetrical with nextParagraph script.
		info._rangeObj.move(winWordWindowModule.wdParagraph, -1)
		info.updateCaret()
		self._caretScriptPostMovedHelper(textInfos.UNIT_PARAGRAPH,gesture,None)

	@script(
		gestures=(
			"kb:control+v",
			"kb:control+x",
			"kb:control+y",
			"kb:control+z",
			"kb:alt+backspace",
		)
	)
	def script_updateBrailleAndReviewPosition(self, gesture: inputCore.InputGesture) -> None:
		"""Helper script to update braille and review position.
		"""
		# Ensuring braille and review position updates are allowed in caret event.
		self._fromUpdateBrailleAndReviewPosition = True
		gesture.send()
		# Caret event is not always fired when control+v, control+x, control+y
		# or control+z (alt+backspace) is pressed.
		self.event_caret()

	def _backspaceScriptHelper(self, unit: str, gesture: inputCore.InputGesture) -> None:
		"""Helper function to update braille and review position.
		"""
		# Ensuring braille and review position updates are allowed in caret event.
		self._fromUpdateBrailleAndReviewPosition = True
		super()._backspaceScriptHelper(unit, gesture)

	def focusOnActiveDocument(self, officeChartObject):
		rangeStart=officeChartObject.Parent.Range.Start
		self.WinwordApplicationObject.ActiveDocument.Range(rangeStart, rangeStart).Select()
		import api
		eventHandler.executeEvent("gainFocus", api.getDesktopObject().objectWithFocus())

class SpellCheckErrorField(IAccessible, winWordWindowModule.WordDocument_WwN):

	parentSDMCanOverrideName=False
	ignoreFormatting=True

	def _get_location(self):
		return super(IAccessible,self).location

	def _get_errorText(self):
		if self.WinwordVersion>=13:
			return self.value 		
		fields=EditableTextDisplayModelTextInfo(self,textInfos.POSITION_ALL).getTextWithFields()
		inBold=False
		textList=[]
		for field in fields:
			if isinstance(field,str):
				if inBold: textList.append(field)
			elif field.field:
				inBold=field.field.get('bold',False)
			if not inBold and len(textList)>0:
				break
		return u"".join(textList)

	def _get_name(self):
		if self.WinwordVersion<13:
			return super(SpellCheckErrorField,self).description
		return super(SpellCheckErrorField,self).name

	description=None

	def reportFocus(self):
		errorText=self.errorText
		speech.speakObjectProperties(self,name=True,role=True)
		if errorText:
			speech.speakText(errorText)
			speech.speakSpelling(errorText)

	def isDuplicateIAccessibleEvent(self,obj):
		""" We return false here because the spell	checker window raises the focus event every time the value changes instead of the value changed event 
		regardless of the fact that this window already has the focus."""
		return False

class ProtectedDocumentPane(IAccessible):
	"""
	The pane that directly contains a Word document control.
	This pane exists no matter if the document is protected or not, but specifically gets focus when a document is opened in protected mode, and therefore handles moving focus back to the actual document.
	This class also suppresses this pane from being presented in the focus ancestry as it contains  redundant information.
	This is mapped to the window class _WWB and role oleacc.ROLE_SYSTEM_CLIENT
	"""

	# This object should not be presented in the focus ancestry as it is redundant.
	isPresentableFocusAncestor=False

	def event_gainFocus(self):
		"""On gaining focus, simply set the focus on a child of type word document. 
		This is just a container window.
		"""
		if eventHandler.isPendingEvents("gainFocus"):
			return
		document=next((x for x in self.children if isinstance(x,WordDocument)), None)  
		if document:
			curThreadID=ctypes.windll.kernel32.GetCurrentThreadId()
			winUser.user32.AttachThreadInput(curThreadID, document.windowThreadID, True)
			winUser.user32.SetFocus(document.windowHandle)
			winUser.user32.AttachThreadInput(curThreadID, document.windowThreadID, False)
			if not document.WinwordWindowObject.active:
				document.WinwordWindowObject.activate()
