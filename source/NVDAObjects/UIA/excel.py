# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2021 NV Access Limited

from typing import Optional, Tuple
import UIAHandler
import _UIAHandler
import _UIAConstants
from _UIAConstants import (
	UIAutomationType,
)
import colors
import locationHelper
import controlTypes
from _UIACustomProps import (
	CustomPropertyInfo,
)
from comtypes import GUID
from scriptHandler import script
import ui
from logHandler import log
from . import UIA


class ExcelCustomProperties:
	""" UIA 'custom properties' specific to Excel.
	Once registered, all subsequent registrations will return the same ID value.
	This class should be used as a singleton via ExcelCustomProperties.get()
	to prevent unnecessary work by repeatedly interacting with UIA.
	"""
	#: Singleton instance
	_instance: "Optional[ExcelCustomProperties]" = None

	@classmethod
	def get(cls) -> "ExcelCustomProperties":
		"""Get the singleton instance or initialise it.
		"""
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	def __init__(self):
		self.cellFormula = CustomPropertyInfo(
			guid=GUID("{E244641A-2785-41E9-A4A7-5BE5FE531507}"),
			programmaticName="CellFormula",
			uiaType=UIAutomationType.STRING,
		)

		self.cellNumberFormat = CustomPropertyInfo(
			guid=GUID("{626CF4A0-A5AE-448B-A157-5EA4D1D057D7}"),
			programmaticName="CellNumberFormat",
			uiaType=UIAutomationType.STRING,
		)

		self.hasDataValidation = CustomPropertyInfo(
			guid=GUID("{29F2E049-5DE9-4444-8338-6784C5D18ADF}"),
			programmaticName="HasDataValidation",
			uiaType=UIAutomationType.BOOL,
		)

		self.hasDataValidationDropdown = CustomPropertyInfo(
			guid=GUID("{1B93A5CD-0956-46ED-9BBF-016C1B9FD75F}"),
			programmaticName="HasDataValidationDropdown",
			uiaType=UIAutomationType.BOOL,
		)

		self.dataValidationPrompt = CustomPropertyInfo(
			guid=GUID("{7AAEE221-E14D-4DA4-83FE-842AAF06A9B7}"),
			programmaticName="DataValidationPrompt",
			uiaType=UIAutomationType.STRING,
		)

		self.hasConditionalFormatting = CustomPropertyInfo(
			guid=GUID("{DFEF6BBD-7A50-41BD-971F-B5D741569A2B}"),
			programmaticName="HasConditionalFormatting",
			uiaType=UIAutomationType.BOOL,
		)

		self.commentReplyCount = CustomPropertyInfo(
			guid=GUID("{312F7536-259A-47C7-B192-AA16352522C4}"),
			programmaticName="CommentReplyCount",
			uiaType=UIAutomationType.INT,
		)

		self.areGridLinesVisible = CustomPropertyInfo(
			guid=GUID("{4BB56516-F354-44CF-A5AA-96B52E968CFD}"),
			programmaticName="AreGridlinesVisible",
			uiaType=UIAutomationType.BOOL,
		)


class ExcelObject(UIA):
	"""Common base class for all Excel UIA objects
	"""
	_UIAExcelCustomProps = ExcelCustomProperties.get()


class ExcelCell(ExcelObject):

	# selecting cells causes duplicate focus events
	shouldAllowDuplicateUIAFocusEvent = True

	name = ""
	role = controlTypes.ROLE_TABLECELL
	rowHeaderText = None
	columnHeaderText = None

	#: Typing information for auto-property: _get_areGridlinesVisible
	areGridlinesVisible: bool

	def _get_areGridlinesVisible(self) -> bool:
		parent = self.parent
		# There will be at least one grid element between the cell and the sheet.
		# There could be multiple as there might be a data table defined on the sheet.
		while parent and parent.role == controlTypes.ROLE_TABLE:
			parent = parent.parent
		if parent:
			return parent._getUIACacheablePropertyValue(self._UIAExcelCustomProps.areGridLinesVisible.id)
		else:
			log.debugWarning("Could not locate worksheet element.")
			return False

	#: Typing information for auto-property: _get_outlineColor
	outlineColor: Optional[Tuple[colors.RGB]]

	def _get_outlineColor(self) -> Optional[Tuple[colors.RGB]]:
		val = self._getUIACacheablePropertyValue(_UIAHandler.UIA_OutlineColorPropertyId, True)
		if isinstance(val, tuple):
			return tuple(colors.RGB.fromCOLORREF(v) for v in val)
		return None

	#: Typing information for auto-property: _get_outlineThickness
	outlineThickness: Optional[Tuple[float]]

	def _get_outlineThickness(self) -> Optional[Tuple[float]]:
		val = self._getUIACacheablePropertyValue(_UIAHandler.UIA_OutlineThicknessPropertyId, True)
		if isinstance(val, tuple):
			return val
		return None

	#: Typing information for auto-property: _get_fillColor
	fillColor: Optional[colors.RGB]

	def _get_fillColor(self) -> Optional[colors.RGB]:
		val = self._getUIACacheablePropertyValue(_UIAHandler.UIA_FillColorPropertyId, True)
		if isinstance(val, int):
			return colors.RGB.fromCOLORREF(val)
		return None

	#: Typing information for auto-property: _get_fillType
	fillType: Optional[_UIAConstants.FillType]

	def _get_fillType(self) -> Optional[_UIAConstants.FillType]:
		val = self._getUIACacheablePropertyValue(_UIAHandler.UIA_FillTypePropertyId, True)
		if isinstance(val, int):
			try:
				return _UIAConstants.FillType(val)
			except ValueError:
				pass
		return None

	#: Typing information for auto-property: _get_rotation
	rotation: Optional[float]

	def _get_rotation(self) -> Optional[float]:
		val = self._getUIACacheablePropertyValue(_UIAHandler.UIA_RotationPropertyId, True)
		if isinstance(val, float):
			return val
		return None

	#: Typing information for auto-property: _get_cellSize
	cellSize: locationHelper.Point

	def _get_cellSize(self) -> locationHelper.Point:
		val = self._getUIACacheablePropertyValue(_UIAHandler.UIA_SizePropertyId, True)
		x = val[0]
		y = val[1]
		return locationHelper.Point(x, y)

	@script(
		description=pgettext(
			"excel-UIA",
			# Translators: the description of a script
			"Shows a browseable message Listing information about a cell's "
			"appearance such as outline and fill colors, rotation and size"
		),
		gestures=["kb:NVDA+o"],
	)
	def script_showCellAppearanceInfo(self, gesture):
		infoList = []
		tmpl = pgettext(
			"excel-UIA",
			# Translators: The width of the cell in points
			"Cell width: {0.x:.1f} pt"
		)
		infoList.append(tmpl.format(self.cellSize))

		tmpl = pgettext(
			"excel-UIA",
			# Translators: The height of the cell in points
			"Cell height: {0.y:.1f} pt"
		)
		infoList.append(tmpl.format(self.cellSize))

		if self.rotation is not None:
			tmpl = pgettext(
				"excel-UIA",
				# Translators: The rotation in degrees of an Excel cell
				"Rotation: {0} degrees"
			)
			infoList.append(tmpl.format(self.rotation))

		if self.outlineColor is not None:
			tmpl = pgettext(
				"excel-UIA",
				# Translators: The outline (border) colors of an Excel cell.
				"Outline color: top={0.name}, bottom={1.name}, left={2.name}, right={3.name}"
			)
			infoList.append(tmpl.format(*self.outlineColor))

		if self.outlineThickness is not None:
			tmpl = pgettext(
				"excel-UIA",
				# Translators: The outline (border) thickness values of an Excel cell.
				"Outline thickness: top={0}, bottom={1}, left={2}, right={3}"
			)
			infoList.append(tmpl.format(*self.outlineThickness))

		if self.fillColor is not None:
			tmpl = pgettext(
				"excel-UIA",
				# Translators: The fill color of an Excel cell
				"Fill color: {0.name}"
			)
			infoList.append(tmpl.format(self.fillColor))

		if self.fillType is not None:
			tmpl = pgettext(
				"excel-UIA",
				# Translators: The fill type (pattern, gradient etc) of an Excel Cell
				"Fill type: {0}"
			)
			infoList.append(tmpl.format(_UIAConstants.FillTypeLabels[self.fillType]))
		numberFormat = self._getUIACacheablePropertyValue(
			self._UIAExcelCustomProps.cellNumberFormat.id
		)
		if numberFormat:
			# Translators: the number format of an Excel cell
			tmpl = _("Number format: {0}")
			infoList.append(tmpl.format(numberFormat))
		hasDataValidation = self._getUIACacheablePropertyValue(
			self._UIAExcelCustomProps.hasDataValidation.id
		)
		if hasDataValidation:
			# Translators: If an excel cell has data validation set
			tmpl = _("Has data validation")
			infoList.append(tmpl)
		dataValidationPrompt = self._getUIACacheablePropertyValue(
			self._UIAExcelCustomProps.dataValidationPrompt.id
		)
		if dataValidationPrompt:
			# Translators: the data validation prompt (input message) for an Excel cell
			tmpl = _("Data validation prompt: {0}")
			infoList.append(tmpl.format(dataValidationPrompt))
		hasConditionalFormatting = self._getUIACacheablePropertyValue(
			self._UIAExcelCustomProps.hasConditionalFormatting.id
		)
		if hasConditionalFormatting:
			# Translators: If an excel cell has conditional formatting
			tmpl = _("Has conditional formatting")
			infoList.append(tmpl)
		if self.areGridlinesVisible:
			# Translators: If an excel cell has visible gridlines
			tmpl = _("Gridlines are visible")
			infoList.append(tmpl)
		infoString = "\n".join(infoList)
		ui.browseableMessage(
			infoString,
			title=pgettext(
				"excel-UIA",
				# Translators: Title for a browsable message that describes the appearance of a cell in Excel
				"Cell Appearance"
			)
		)

	def _hasSelection(self):
		return (
			self.selectionContainer
			and 1 < self.selectionContainer.getSelectedItemsCount()
		)

	def _get_value(self):
		if self._hasSelection():
			return
		return super().value

	def _get_errorText(self):
		for typeId, element in self.UIAAnnotationObjects.items():
			if typeId in {
				UIAHandler.AnnotationType_DataValidationError,
				UIAHandler.AnnotationType_FormulaError,
				UIAHandler.AnnotationType_CircularReferenceError,
			}:
				return element.GetCurrentPropertyValue(UIAHandler.UIA_FullDescriptionPropertyId)

	def _get_description(self):
		"""
		Prepends error messages and collaborator presence to any existing description.
		"""
		descriptionList = []
		if self.errorText:
			# Translators: an error message on a cell in Microsoft Excel
			descriptionList.append(
				# Translators:  an error message on a cell in Microsoft Excel.
				_("Error: {errorText}").format(errorText=self.errorText)
			)
		presence = self.UIAAnnotationObjects.get(UIAHandler.AnnotationType_Author)
		if presence:
			author = presence.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAuthorPropertyId)
			descriptionList.append(
				# Translators: a mesage when another author is editing a cell in a shared Excel spreadsheet.
				_("{author} is editing").format(
					author=author
				)
			)
		baseDescription = super().description
		if baseDescription:
			descriptionList.append(baseDescription)
		return ", ".join(descriptionList)

	#: Typing information for auto-property: _get__isContentTooLargeForCell
	_isContentTooLargeForCell: bool

	def _get__isContentTooLargeForCell(self) -> bool:
		if not self.UIATextPattern:
			return False
		r = self.UIATextPattern.documentRange
		vr = self.UIATextPattern.getvisibleRanges().getElement(0)
		return len(vr.getText(-1)) < len(r.getText(-1))

	#: Typing information for auto-property: _get__nextCellHasContent
	_nextCellHasContent: bool

	def _get__nextCellHasContent(self) -> bool:
		nextCell = self.next
		if nextCell and nextCell.UIATextPattern:
			return bool(nextCell.UIATextPattern.documentRange.getText(-1))
		return False

	def _get_states(self):
		states = super().states
		if self._isContentTooLargeForCell:
			if not self._nextCellHasContent:
				states.add(controlTypes.STATE_OVERFLOWING)
			else:
				states.add(controlTypes.STATE_CROPPED)
		if self._getUIACacheablePropertyValue(self._UIAExcelCustomProps.cellFormula.id):
			states.add(controlTypes.STATE_HASFORMULA)
		if self._getUIACacheablePropertyValue(self._UIAExcelCustomProps.hasDataValidationDropdown.id):
			states.add(controlTypes.STATE_HASPOPUP)
		return states

	def _get_cellCoordsText(self):
		if self._hasSelection():
			sc = self._getUIACacheablePropertyValue(
				UIAHandler.UIA_SelectionItemSelectionContainerPropertyId
			).QueryInterface(UIAHandler.IUIAutomationElement)

			firstSelected = sc.GetCurrentPropertyValue(
				UIAHandler.UIA_Selection2FirstSelectedItemPropertyId
			).QueryInterface(UIAHandler.IUIAutomationElement)

			firstAddress = firstSelected.GetCurrentPropertyValue(
				UIAHandler.UIA_NamePropertyId
			).replace('"', '')

			firstValue = firstSelected.GetCurrentPropertyValue(
				UIAHandler.UIA_ValueValuePropertyId
			)

			lastSelected = sc.GetCurrentPropertyValue(
				UIAHandler.UIA_Selection2LastSelectedItemPropertyId
			).QueryInterface(UIAHandler.IUIAutomationElement)

			lastAddress = lastSelected.GetCurrentPropertyValue(
				UIAHandler.UIA_NamePropertyId
			).replace('"', '')

			lastValue = lastSelected.GetCurrentPropertyValue(
				UIAHandler.UIA_ValueValuePropertyId
			)

			cellCoordsTemplate = pgettext(
				"excel-UIA",
				# Translators: Excel, report range of cell coordinates
				"{firstAddress} {firstValue} through {lastAddress} {lastValue}"
			)
			return cellCoordsTemplate.format(
				firstAddress=firstAddress,
				firstValue=firstValue,
				lastAddress=lastAddress,
				lastValue=lastValue
			)
		name = super().name
		# Later builds of Excel 2016 quote the letter coordinate.
		# We don't want the quotes.
		name = name.replace('"', '')
		return name

	@script(
		# Translators: the description  for a script for Excel
		description=_("Reports the note or comment thread on the current cell"),
		gesture="kb:NVDA+alt+c")
	def script_reportComment(self, gesture):
		commentsElement = self.UIAAnnotationObjects.get(UIAHandler.AnnotationType_Comment)
		if commentsElement:
			comment = commentsElement.GetCurrentPropertyValue(UIAHandler.UIA_FullDescriptionPropertyId)
			author = commentsElement.GetCurrentPropertyValue(UIAHandler.UIA_AnnotationAuthorPropertyId)
			numReplies = commentsElement.GetCurrentPropertyValue(self._UIAExcelCustomProps.commentReplyCount.id)
			if numReplies == 0:
				# Translators: a comment on a cell in Microsoft excel.
				text = _("{comment}  by {author}").format(
					comment=comment,
					author=author
				)
			else:
				# Translators: a comment on a cell in Microsoft excel.
				text = _("{comment}  by {author} with {numReplies} replies").format(
					comment=comment,
					author=author,
					numReplies=numReplies
				)
			ui.message(text)
		else:
			# Translators: A message in Excel when there is no note
			ui.message(_("No note or comment thread on this cell"))


class ExcelWorksheet(ExcelObject):
	role = controlTypes.ROLE_TABLE

	# The grid UIAElement dies each time the sheet is scrolled.
	# Therefore this grid would be announced in the focus ancestory each time which is bad.
	# Suppress this.
	isPresentableFocusAncestor = False

	def _get_parent(self):
		parent = super().parent
		# We want to present the parent (sheet) in the focus ancestry
		# As that is what has the sheet name.
		# Making this change in an overlay class was considered, however
		# the parent (sheet) has no useful properties (such as className) to be easily identified,
		# and identifying it by one of its children would be more costly than the current approach.
		parent.isPresentableFocusAncestor = True
		# However, the selection state on the sheet is not useful, so remove it.
		parent.states.discard(controlTypes.STATE_SELECTED)
		return parent


class CellEdit(ExcelObject):
	name = ""


class BadExcelFormulaEdit(ExcelObject):
	"""
	Suppresses focus events on the old formula bar, which does not have a usable UIA implementation.
	Excel used to focus the EXCEL6 window with the formula bar when editing a cell.
	However, now focus is moved to an edit control within the actual cell being edited,
	in the EXCEL7 window.
	Sometimes however focus (probably proxied from MSAA) still gets occasionally fired.
	"""

	shouldAllowUIAFocusEvent = False
