# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2017-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from dataclasses import dataclass
from enum import Enum
from typing import Any, Optional, Tuple, Union
from baseObject import AutoPropertyObject, ScriptableObject
import config
import textInfos
import controlTypes

_TableID = Union[int, Tuple, Any]
"""
A variety of types can be used for a tableID.
Known to be a tuple for UIA, an integer for virtual buffers.
"""


class _Axis(str, Enum):
	ROW = "row"
	COLUMN = "column"


class _Movement(str, Enum):
	NEXT = "next"
	PREVIOUS = "previous"
	FIRST = "first"
	LAST = "last"


@dataclass
class _TableSelection:
	"""
		Caches information about user navigating around the table.
		This class is used to store true row/column number when navigating through merged cells.
		lastRow/lastCol store coordinates of the last cell user explicitly navigated to.
		If they don't match current selection we invalidate this cache.
		If they match, we use trueRow/trueCol to maintain row/column through merged cells.
	"""
	axis: _Axis
	lastRow: int
	lastCol: int
	trueRow: int
	rowSpan: int
	trueCol: int
	colSpan: int


class TextContainerObject(AutoPropertyObject):
	"""
	An object that contains text which can be accessed via a call to a makeTextInfo method.
	E.g. NVDAObjects, BrowseModeDocument TreeInterceptors.
	"""

	def _get_TextInfo(self):
		raise NotImplementedError

	def makeTextInfo(self, position) -> textInfos.TextInfo:
		return self.TextInfo(self,position)

	selection: textInfos.TextInfo

	def _get_selection(self):
		return self.makeTextInfo(textInfos.POSITION_SELECTION)

	def _set_selection(self,info):
		info.updateSelection()

class DocumentWithTableNavigation(TextContainerObject,ScriptableObject):
	"""
	A document that supports standard table navigiation comments (E.g. control+alt+arrows to move between table cells).
	The document could be an NVDAObject, or a BrowseModeDocument treeIntercepter for example.
	"""

	_lastTableSelection: Optional[_TableSelection] = None

	def _maybeGetLayoutTableIds(self, info: textInfos.TextInfo):
		"""
		If "Include layout tables" option is on, this will
		compute the set of layout tables that this textInfo is enclosed in,
		otherwise it will return empty set.
		@param info:  the position where the layout tables should be looked for.
		@returns: A set of table IDs or empty set.
		"""
		fields = list(info.getTextWithFields())
		# If layout tables should not be reported, we should First record the ID of all layout tables,
		# so that we can skip them when searching for the deepest table
		layoutIDs = set()
		if not config.conf["documentFormatting"]["includeLayoutTables"]:
			for field in fields:
				if (
					isinstance(field, textInfos.FieldCommand)
					and field.command == "controlStart"
					and field.field.get('table-layout')
				):
					tableID = field.field.get('table-id')
					if tableID is not None:
						layoutIDs.add(tableID)
		return layoutIDs

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
		layoutIDs = self._maybeGetLayoutTableIds(info)
		for field in reversed(fields):
			if not (isinstance(field, textInfos.FieldCommand) and field.command == "controlStart"):
				# Not a control field.
				continue
			attrs = field.field
			tableID=attrs.get('table-id')
			if tableID is None or tableID in layoutIDs:
				continue
			if "table-columnnumber" in attrs and not attrs.get('table-layout'):
				break
		else:
			raise LookupError("Not in a table cell")
		return (attrs["table-id"],
			attrs["table-rownumber"], attrs["table-columnnumber"],
			attrs.get("table-rowsspanned", 1), attrs.get("table-columnsspanned", 1))

	def _getTableDimensions(self, info: textInfos.TextInfo) -> Tuple[int, int]:
		"""
		Fetches information about the deepest table dimension.
		@param info:  the position where the table cell should be looked for.
		@returns: a tuple of table height and width.
		@raises: LookupError if there is no table cell at this position.
		"""
		if info.isCollapsed:
			info = info.copy()
			info.expand(textInfos.UNIT_CHARACTER)
		fields = list(info.getTextWithFields())
		layoutIDs = self._maybeGetLayoutTableIds(info)
		for field in reversed(fields):
			if not (
				isinstance(field, textInfos.FieldCommand)
				and field.command == "controlStart"
				and field.field.get("role") == controlTypes.Role.TABLE
			):
				# Not a table control field.
				continue
			attrs = field.field
			tableID = attrs.get('table-id')
			if tableID is None or tableID in layoutIDs:
				continue
			break
		else:
			raise LookupError("Not in a table cell")
		try:
			nRows = int(attrs.get("table-rowcount"))
			nCols = int(attrs.get("table-columncount"))
		except (TypeError, ValueError):
			raise LookupError("Not in a table cell")
		return (nRows, nCols)

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

	def _getNearestTableCell(
			self,
			tableID: _TableID,
			startPos: textInfos.TextInfo,
			origRow: int,
			origCol: int,
			origRowSpan: int,
			origColSpan: int,
			movement: _Movement,
			axis: _Axis,
	) -> textInfos.TextInfo:
		"""
		Locates the nearest table cell relative to another table cell in a given direction, given its coordinates.
		For example, this is used to move to the cell in the next column, previous row, etc.
		This method will skip over missing table cells (where L{_getTableCellAt} raises LookupError), up to the number of times set by _missingTableCellSearchLimit set on this instance.
		@param tableID: the ID of the table
		@param startPos: the position in the document to start searching from.
		@param origRow: the row number of the starting cell
		@param origCol: the column number  of the starting cell
		@param origRowSpan: the row span of the row of the starting cell
		@param origColSpan: the column span of the column of the starting cell
		@param movement: the direction ("next" or "previous")
		@param axis: the axis of movement ("row" or "column")
		@returns: the position of the nearest table cell
		"""
		if not axis:
			raise ValueError("Axis must be row or column")

		# Determine destination row and column.
		destRow = origRow
		destCol = origCol
		if axis == _Axis.ROW:
			destRow += origRowSpan if movement == _Movement.NEXT else -1
		elif axis == _Axis.COLUMN:
			destCol += origColSpan if movement == _Movement.NEXT else -1

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
			if axis == _Axis.ROW:
				destRow += 1 if movement == _Movement.NEXT else -1
			else:
				destCol += 1 if movement == _Movement.NEXT else -1
		raise LookupError

	def _getFirstOrLastTableCell(
			self,
			tableID: _TableID,
			startPos: textInfos.TextInfo,
			origRow: int,
			origCol: int,
			origRowSpan: int,
			origColSpan: int,
			movement: _Movement,
			axis: _Axis
	) -> textInfos.TextInfo:
		"""
		Locates the first or last cell in current row or column given coordinates of current cell.
		When jumping to the first row/column, It will try to set current row/column index to 1.
		When jumping to the last row/column, it will query table dimensions and set row/column index
		to corresponding dimension.
		After figuring out exact coordinates of the cell it will try to jump directly to that cell,
		or if that fails (due to missing table cell), it will walk in the opposite direction skipping missing cells
		up to the number of times set by _missingTableCellSearchLimit set on this instance.
		@param tableID: the ID of the table
		@param startPos: the position in the document to start searching from.
		@param origRow: the row number of the starting cell
		@param origCol: the column number  of the starting cell
		@param origRowSpan: the row span of the row of the starting cell
		@param origColSpan: the column span of the column of the starting cell
		@param movement: the direction ("first" or "last")
		@param axis: the axis of movement ("row" or "column")
		@returns: the position of the destination table cell
		"""
		destRow, destCol = origRow, origCol
		if movement == _Movement.FIRST:
			if axis == _Axis.COLUMN:
				destCol = 1
			else:
				destRow = 1
		else:
			nRows, nCols = self._getTableDimensions(startPos)
			if axis == _Axis.COLUMN:
				destCol = nCols
			else:
				destRow = nRows
		try:
			return self._getTableCellAt(tableID, startPos, destRow, destCol)
		except LookupError:
			oppositeMovement = _Movement.PREVIOUS if movement == _Movement.LAST else _Movement.NEXT
			return self._getNearestTableCell(
				tableID,
				startPos,
				destRow,
				destCol,
				origRowSpan=1,
				origColSpan=1,
				movement=oppositeMovement,
				axis=axis
			)

	def _tableMovementScriptHelper(
			self,
			movement: _Movement = _Movement.NEXT,
			axis: Optional[_Axis] = None
	):
		# documentBase is a core module and should not depend on these UI modules and so they are imported
		# at run-time. (#12404)
		from scriptHandler import isScriptWaiting
		from speech import speakTextInfo
		import ui

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

		# The following lines check whether user has been issuing table navigation commands repeatedly.
		# In this case, instead of using current column/row index, we used cached value
		# to allow users being able to skip merged cells without affecting the initial column/row index.
		# For more info see issue #11919 and #7278.
		if (
			self._lastTableSelection
			and origRow == self._lastTableSelection.lastRow
			and origCol == self._lastTableSelection.lastCol
			and self._lastTableSelection.axis == axis
		):
			if axis == _Axis.ROW:
				origCol = self._lastTableSelection.trueCol
				origColSpan = self._lastTableSelection.colSpan
			else:
				origRow = self._lastTableSelection.trueRow
				origRowSpan = self._lastTableSelection.rowSpan

		try:
			if movement in {_Movement.PREVIOUS, _Movement.NEXT}:
				info = self._getNearestTableCell(
					tableID,
					self.selection,
					origRow,
					origCol,
					origRowSpan,
					origColSpan,
					movement,
					axis
				)
			elif movement in {_Movement.FIRST, _Movement.LAST}:
				info = self._getFirstOrLastTableCell(
					tableID,
					self.selection,
					origRow,
					origCol,
					origRowSpan,
					origColSpan,
					movement,
					axis
				)
			else:
				raise ValueError(f"Unknown movement {movement}")
			newTableID, newRow, newCol, newRowSpan, newColSpan = self._getTableCellCoords(info)
		except LookupError:
			# Translators: The message reported when a user attempts to use a table movement command
			# but the cursor can't be moved in that direction because it is at the edge of the table.
			ui.message(_("Edge of table"))
			# Retrieve the cell on which we started.
			info = self._getTableCellAt(tableID, self.selection,origRow, origCol)
			newTableID, newRow, newCol, newRowSpan, newColSpan = self._getTableCellCoords(info)

		speakTextInfo(info, formatConfig=formatConfig, reason=controlTypes.OutputReason.CARET)
		info.collapse()
		self.selection = info
		self._lastTableSelection = _TableSelection(
			lastRow=newRow,
			lastCol=newCol,
			axis=axis,
			trueRow=origRow,
			rowSpan=origRow,
			trueCol=origCol,
			colSpan=origColSpan,
		)

	def script_nextRow(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.ROW, movement=_Movement.NEXT)
	# Translators: the description for the next table row script on browseMode documents.
	script_nextRow.__doc__ = _("moves to the next table row")

	def script_previousRow(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.ROW, movement=_Movement.PREVIOUS)
	# Translators: the description for the previous table row script on browseMode documents.
	script_previousRow.__doc__ = _("moves to the previous table row")

	def script_nextColumn(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.COLUMN, movement=_Movement.NEXT)
	# Translators: the description for the next table column script on browseMode documents.
	script_nextColumn.__doc__ = _("moves to the next table column")

	def script_previousColumn(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.COLUMN, movement=_Movement.PREVIOUS)
	# Translators: the description for the previous table column script on browseMode documents.
	script_previousColumn.__doc__ = _("moves to the previous table column")

	def script_firstRow(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.ROW, movement=_Movement.FIRST)
	# Translators: the description for the first table row script on browseMode documents.
	script_firstRow.__doc__ = _("moves to the first table row")

	def script_lastRow(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.ROW, movement=_Movement.LAST)
	# Translators: the description for the last table row script on browseMode documents.
	script_lastRow.__doc__ = _("moves to the last table row")

	def script_firstColumn(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.COLUMN, movement=_Movement.FIRST)
	# Translators: the description for the first table column script on browseMode documents.
	script_firstColumn.__doc__ = _("moves to the first table column")

	def script_lastColumn(self, gesture):
		self._tableMovementScriptHelper(axis=_Axis.COLUMN, movement=_Movement.LAST)
	# Translators: the description for the last table column script on browseMode documents.
	script_lastColumn.__doc__ = _("moves to the last table column")

	def script_toggleIncludeLayoutTables(self,gesture):
		# documentBase is a core module and should not depend on UI, so it is imported at run-time. (#12404)
		import ui
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
		"kb:control+alt+pageUp": "firstRow",
		"kb:control+alt+pageDown": "lastRow",
		"kb:control+alt+Home": "firstColumn",
		"kb:control+alt+End": "lastColumn",
	}
