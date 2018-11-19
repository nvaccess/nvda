#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from baseObject import AutoPropertyObject, ScriptableObject
from scriptHandler import isScriptWaiting
import config
import textInfos
import speech
import ui
import controlTypes
import braille

class TextContainerObject(AutoPropertyObject):
	"""
	An object that contains text which can be accessed via a call to a makeTextInfo method.
	E.g. NVDAObjects, BrowseModeDocument TreeInterceptors.
	"""

	def _get_TextInfo(self):
		raise NotImplementedError

	def makeTextInfo(self,position):
		return self.TextInfo(self,position)

	def _get_selection(self):
		return self.makeTextInfo(textInfos.POSITION_SELECTION)

	def _set_selection(self,info):
		info.updateSelection()

class DocumentWithTableNavigation(TextContainerObject,ScriptableObject):
	"""
	A document that supports standard table navigation commands (E.g. control+alt+arrows to move between table cells).
	The document could be an NVDAObject, or a BrowseModeDocument treeIntercepter for example.
	"""
	#: The controlField attribute name that should be used as the row number when navigating in a table. By default this is the same as the presentational attribute name
	navigationalTableRowNumberAttributeName="table-rownumber"
	#: The controlField attribute name that should be used as the column number when navigating in a table. By default this is the same as the presentational attribute name
	navigationalTableColumnNumberAttributeName="table-columnnumber"

	def _getTableCellCoords(self, info):
		"""
		Fetches information about the deepest table cell at the given position.
		@param info:  the position where the table cell should be looked for.
		@type info: L{textInfos.TextInfo}
		@returns: a tuple of table ID, row number, column number, row span, and column span.
		@rtype: tuple
		@raises: LookupError if there is no table cell at this position.
		"""
		if info.isCollapsed:
			info = info.copy()
			info.expand(textInfos.UNIT_CHARACTER)
		fields=list(info.getTextWithFields())
		# If layout tables should not be reported, we should First record the ID of all layout tables so that we can skip them when searching for the deepest table
		layoutIDs=set()
		if not config.conf["documentFormatting"]["includeLayoutTables"]:
			for field in fields:
				if isinstance(field, textInfos.FieldCommand) and field.command == "controlStart" and field.field.get('table-layout'):
					tableID=field.field.get('table-id')
					if tableID is not None:
						layoutIDs.add(tableID)
		for field in reversed(fields):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			tableID=attrs.get('table-id')
			if tableID is None or tableID in layoutIDs:
				continue
			if self.navigationalTableColumnNumberAttributeName in attrs and not attrs.get('table-layout'):
				break
		else:
			raise LookupError("Not in a table cell")
		return (attrs["table-id"],
			attrs[self.navigationalTableRowNumberAttributeName], attrs[self.navigationalTableColumnNumberAttributeName],
			attrs.get("table-rowsspanned", 1), attrs.get("table-columnsspanned", 1))

	def _getTableCellAt(self,tableID,startPos,row,column):
		"""
		Starting from the given start position, Locates the table cell with the given row and column coordinates and table ID.
		@param startPos: the position to start searching from.
		@type startPos: L{textInfos.TextInfo}
		@param tableID: the ID of the table.
		@param row: the row number of the cell
		@type row: int
		@param column: the column number of the table cell
		@type column: int
		@returns: the table cell's position in the document
		@rtype: L{textInfos.TextInfo}
		@raises: LookupError if the cell does not exist 
		"""
		raise NotImplementedError

	_missingTableCellSearchLimit=3 #: The number of missing  cells L{_getNearestTableCell} is allowed to skip over to locate the next available cell
	def _getNearestTableCell(self, tableID, startPos, origRow, origCol, origRowSpan, origColSpan, movement, axis):
		"""
		Locates the nearest table cell relative to another table cell in a given direction, given its coordinates.
		For example, this is used to move to the cell in the next column, previous row, etc.
		This method will skip over missing table cells (where L{_getTableCellAt} raises LookupError), up to the number of times set by _missingTableCellSearchLimit set on this instance.
		@param tableID: the ID of the table
		@param startPos: the position in the document to start searching from.
		@type startPos: L{textInfos.TextInfo}
		@param origRow: the row number of the starting cell
		@type origRow: int
		@param origCol: the column number  of the starting cell
		@type origCol: int
		@param origRowSpan: the row span of the row of the starting cell
		@type origRowSpan: int
		@param origColSpan: the column span of the column of the starting cell
		@type origColSpan: int
		@param movement: the direction ("next" or "previous")
		@type movement: string
		@param axis: the axis of movement ("row" or "column")
		@type axis: string
		@returns: the position of the nearest table cell
		@rtype: L{textInfos.TextInfo}
		"""
		if not axis:
			raise ValueError("Axis must be row or column")

		# Determine destination row and column.
		destRow = origRow
		destCol = origCol
		if axis == "row":
			destRow += origRowSpan if movement == "next" else -1
		elif axis == "column":
			destCol += origColSpan if movement == "next" else -1

		# Try and fetch the cell at these coordinates, though  if a  cell is missing, try  several more times moving the coordinates on by one cell each time
		limit=self._missingTableCellSearchLimit
		while limit>0:
			limit-=1
			if destCol < 1 or destRow<1:
				# Optimisation: We're definitely at the edge of the column or row.
				raise LookupError
			try:
				return self._getTableCellAt(tableID,startPos,destRow,destCol)
			except LookupError:
				pass
			if axis=="row":
				destRow+=1 if movement=="next" else -1
			else:
				destCol+=1 if movement=="next" else -1
		raise LookupError

	def _tableMovementScriptHelper(self, movement="next", axis=None):
		if isScriptWaiting():
			return
		formatConfig=config.conf["documentFormatting"].copy()
		formatConfig["reportTables"]=True
		try:
			tableID, origRow, origCol, origRowSpan, origColSpan = self._getTableCellCoords(self.selection)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# when the cursor is not within a table.
			ui.message(_("Not in a table cell"))
			return

		try:
			info = self._getNearestTableCell(tableID, self.selection, origRow, origCol, origRowSpan, origColSpan, movement, axis)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# but the cursor can't be moved in that direction because it is at the edge of the table.
			ui.message(_("Edge of table"))
			# Retrieve the cell on which we started.
			info = self._getTableCellAt(tableID, self.selection,origRow, origCol)

		speech.speakTextInfo(info,formatConfig=formatConfig,reason=controlTypes.REASON_CARET)
		info.collapse()
		self.selection = info

	def script_nextRow(self, gesture):
		self._tableMovementScriptHelper(axis="row", movement="next")
	# Translators: the description for the next table row script on browseMode documents.
	script_nextRow.__doc__ = _("moves to the next table row")

	def script_previousRow(self, gesture):
		self._tableMovementScriptHelper(axis="row", movement="previous")
	# Translators: the description for the previous table row script on browseMode documents.
	script_previousRow.__doc__ = _("moves to the previous table row")

	def script_nextColumn(self, gesture):
		self._tableMovementScriptHelper(axis="column", movement="next")
	# Translators: the description for the next table column script on browseMode documents.
	script_nextColumn.__doc__ = _("moves to the next table column")

	def script_previousColumn(self, gesture):
		self._tableMovementScriptHelper(axis="column", movement="previous")
	# Translators: the description for the previous table column script on browseMode documents.
	script_previousColumn.__doc__ = _("moves to the previous table column")

	def script_toggleIncludeLayoutTables(self,gesture):
		if config.conf["documentFormatting"]["includeLayoutTables"]:
			# Translators: The message announced when toggling the include layout tables browse mode setting.
			state = _("layout tables off")
			config.conf["documentFormatting"]["includeLayoutTables"]=False
		else:
			# Translators: The message announced when toggling the include layout tables browse mode setting.
			state = _("layout tables on")
			config.conf["documentFormatting"]["includeLayoutTables"]=True
		ui.message(state)
	# Translators: Input help mode message for include layout tables command.
	script_toggleIncludeLayoutTables.__doc__=_("Toggles on and off the inclusion of layout tables in browse mode")

	__gestures={
		"kb:control+alt+downArrow": "nextRow",
		"kb:control+alt+upArrow": "previousRow",
		"kb:control+alt+rightArrow": "nextColumn",
		"kb:control+alt+leftArrow": "previousColumn",
	}

class SelectableTextContainerObject(TextContainerObject):
	"""
	An object that contains text in which the selection can be fetched and changed.
	This doesn't necessarily mean that the text is editable.

	If the object notifies of selection changes, the following should be done:
		* When the object gains focus, L{initAutoSelectDetection} must be called.
		* When the object notifies of a possible selection change, L{detectPossibleSelectionChange} must be called.
		* Optionally, if the object notifies of changes to its content, L{hasContentChangedSinceLastSelection} should be set to C{True}.
	@ivar hasContentChangedSinceLastSelection: Whether the content has changed since the last selection occurred.
	@type hasContentChangedSinceLastSelection: bool
	"""

	#: Whether to speak the unselected content after new content has been selected.
	#: If C{False}, the old selection is ignored,
	#: and the new selection is reported without the redundant selected state.
	#: @type: bool
	speakUnselected = True

	def initAutoSelectDetection(self):
		"""Initialise automatic detection of selection changes.
		This should be called when the object gains focus.
		"""
		try:
			self._lastSelectionPos=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			self._lastSelectionPos=None
		self.isTextSelectionAnchoredAtStart=True
		self.hasContentChangedSinceLastSelection=False

	def detectPossibleSelectionChange(self):
		"""Detects if the selection has been changed, and if so it speaks the change.
		"""
		try:
			newInfo=self.makeTextInfo(textInfos.POSITION_SELECTION)
		except:
			# Just leave the old selection, which is usually better than nothing.
			return
		oldInfo=getattr(self,'_lastSelectionPos',None)
		self._lastSelectionPos=newInfo.copy()
		if not oldInfo:
			# There's nothing we can do, but at least the last selection will be right next time.
			self.isTextSelectionAnchoredAtStart=True
			return
		self._updateSelectionAnchor(oldInfo,newInfo)
		hasContentChanged=getattr(self,'hasContentChangedSinceLastSelection',False)
		self.hasContentChangedSinceLastSelection=False
		if not self.speakUnselected:
			# As the unselected state is not relevant here and all spoken content is selected,
			# use speech.speakTextInfo to make sure the new selection is spoken.
			speech.speakTextInfo(newInfo,reason=controlTypes.REASON_CARET)
		else:
			speech.speakSelectionChange(oldInfo,newInfo,generalize=hasContentChanged)

		# Import late to avoid circular import
		from editableText import EditableText
		if not isinstance(self, EditableText):
			# This object has no caret, manually trigger a braille update.
			braille.handler.handleUpdate(self)

	def _updateSelectionAnchor(self,oldInfo,newInfo):
		# Only update the value if the selection changed.
		if newInfo.compareEndPoints(oldInfo,"startToStart")!=0:
			self.isTextSelectionAnchoredAtStart=False
		elif newInfo.compareEndPoints(oldInfo,"endToEnd")!=0:
			self.isTextSelectionAnchoredAtStart=True

