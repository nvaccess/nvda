# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018 NV Access Limited

from typing import Optional, Tuple
import UIAHandler
import colors
import locationHelper
import textInfos
import controlTypes
from scriptHandler import script
import ui
from . import UIA, UIATextInfo


class ExcelCell(UIA):

	shouldAllowDuplicateUIAFocusEvent = True

	name = u""
	role = controlTypes.ROLE_TABLECELL
	rowHeaderText = None
	columnHeaderText = None

	def _get_areGridlinesVisible(self):
		parent = self.parent
		# There will be at least one grid element between the cell and the sheet.
		# There could be multiple as there might be a data table defined on the sheet.
		while parent.role == controlTypes.ROLE_TABLE:
			parent = parent.parent
		return parent._getUIACacheablePropertyValue(UIAHandler.handler.AreGridlinesVisible_PropertyId)

	def _get_outlineColor(self) -> Optional[Tuple[colors.RGB]]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA_OutlineColorPropertyId, True)
		if isinstance(val, tuple):
			return tuple(colors.RGB.fromCOLORREF(v) for v in val)
		return None

	def _get_outlineThickness(self) -> Optional[Tuple[float]]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA_OutlineThicknessPropertyId, True)
		if isinstance(val, tuple):
			return val
		return None

	def _get_fillColor(self) -> Optional[colors.RGB]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA_FillColorPropertyId, True)
		if isinstance(val, int):
			return colors.RGB.fromCOLORREF(val)
		return None

	def _get_fillType(self) -> Optional[UIAHandler.FillType]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA_FillTypePropertyId, True)
		if isinstance(val, int):
			try:
				return UIAHandler.FillType(val)
			except ValueError:
				pass
		return None

	def _get_rotation(self) -> Optional[float]:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA_RotationPropertyId, True)
		if isinstance(val, float):
			return val
		return None

	def _get_cellSize(self) -> locationHelper.Point:
		val = self._getUIACacheablePropertyValue(UIAHandler.UIA_SizePropertyId, True)
		# width (x) seems to be in characters multiplied by roughly 5.5? 
		# 10 characters set in column width dialog results in 58
		# 100 characters set in column width dialog results in 544
		x = val[0] / 5.5
		y=val[1]
		return locationHelper.Point(x, y)

	@script(
		# Translators: the description of a script
		description=_("Shows a browseable message Listing information about a cell's appearence such as outline and fill colors, rotation and size"),
		gestures=["kb:NVDA+o"],
	)
	def script_showCellAppearanceInfo(self, gesture):
		infoList = []
		# Translators: The width of the cell in points 
		tmpl = _("Cell width: roughly {0.x:.0f} characters")
		infoList.append(tmpl.format(self.cellSize))
		# Translators: The height of the cell in points 
		tmpl = _("Cell height: {0.y:.1f} pt")
		infoList.append(tmpl.format(self.cellSize))
		if self.rotation is not None:
			# Translators: The rotation in degrees of an Excel cell 
			tmpl = _("Rotation: {0} degrees")
			infoList.append(tmpl.format(self.rotation))
		if self.outlineColor is not None:
			# Translators: The outline (border) colors of an Excel cell. 
			tmpl = _("Outline color: top={0.name}, bottom={1.name}, left={2.name}, right={3.name}")
			infoList.append(tmpl.format(*self.outlineColor))
		if self.outlineThickness is not None:
			# Translators: The outline (border) thickness values of an Excel cell. 
			tmpl = _("Outline thickness: top={0}, bottom={1}, left={2}, right={3}")
			infoList.append(tmpl.format(*self.outlineThickness))
		if self.fillColor is not None:
			# Translators: The fill color of an Excel cell
			tmpl = _("Fill color: {0.name}")
			infoList.append(tmpl.format(self.fillColor))
		if self.fillType is not None:
			# Translators: The fill type (pattern, gradient etc) of an Excel Cell
			tmpl = _("Fill type: {0}")
			infoList.append(tmpl.format(UIAHandler.FillTypeLabels[self.fillType]))
		numberFormat = self._getUIACacheablePropertyValue(UIAHandler.handler.CellNumberFormat_PropertyId)
		if numberFormat:
			# Translators: the number format of an Excel cell 
			tmpl = _("Number format: {0}")
			infoList.append(tmpl.format(numberFormat))
		hasDataValidation = self._getUIACacheablePropertyValue(UIAHandler.handler.HasDataValidation_PropertyId)
		if hasDataValidation:
			# Translators: If an excel cell has data validation set
			tmpl = _("Has data validation")
			infoList.append(tmpl)
		dataValidationPrompt = self._getUIACacheablePropertyValue(UIAHandler.handler.DataValidationPrompt_PropertyId)
		if dataValidationPrompt:
			# Translators: the data validation prompt (input message) for an Excel cell 
			tmpl = _("Data validation prompt: {0}")
			infoList.append(tmpl.format(dataValidationPrompt))
		hasConditionalFormatting = self._getUIACacheablePropertyValue(UIAHandler.handler.HasConditionalFormatting_PropertyId)
		if hasConditionalFormatting:
			# Translators: If an excel cell has conditional formatting 
			tmpl = _("Has conditional formatting")
			infoList.append(tmpl)
		if self.areGridlinesVisible:
			# Translators: If an excel cell has visible gridlines 
			tmpl = _("Gridlines are visible")
			infoList.append(tmpl)
		infoString = "\n".join(infoList)
		ui.browseableMessage(infoString, _("Cell Appearance"))

	def _get_value(self):
		if self.selectionContainer and self.selectionContainer.getSelectedItemsCount() > 1:
			return
		return super().value

	def old_get_description(self):
		if self.selectionContainer and self.selectionContainer.getSelectedItemsCount() > 1:
			return
		return self.UIAElement.currentItemStatus

	def _get__isContentTooLargeForCell(self):
		if not self.UIATextPattern:
			return False
		r = self.UIATextPattern.documentRange
		vr = self.UIATextPattern.getvisibleRanges().getElement(0)
		return len(vr.getText(-1)) < len(r.getText(-1))

	def _get__nextCellHasContent(self):
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
		if self._getUIACacheablePropertyValue(UIAHandler.handler.CellFormula_PropertyId):
			states.add(controlTypes.STATE_HASFORMULA)
		if self._getUIACacheablePropertyValue(UIAHandler.handler.HasDataValidationDropdown_PropertyId):
			states.add(controlTypes.STATE_HASPOPUP)
		return states

	def _get_cellCoordsText(self):
		if self.selectionContainer and self.selectionContainer.getSelectedItemsCount() > 1:
			sc = self._getUIACacheablePropertyValue(UIAHandler.UIA_SelectionItemSelectionContainerPropertyId)
			sc = sc.QueryInterface(UIAHandler.IUIAutomationElement)
			firstSelected = sc.GetCurrentPropertyValue(UIAHandler.UIA_Selection2FirstSelectedItemPropertyId)
			firstSelected = firstSelected.QueryInterface(UIAHandler.IUIAutomationElement)
			firstAddress = firstSelected.GetCurrentPropertyValue(UIAHandler.UIA_NamePropertyId)
			firstAddress = firstAddress.replace('"', '')
			firstValue = firstSelected.GetCurrentPropertyValue(UIAHandler.UIA_ValueValuePropertyId)
			lastSelected = sc.GetCurrentPropertyValue(UIAHandler.UIA_Selection2LastSelectedItemPropertyId)
			lastSelected = lastSelected.QueryInterface(UIAHandler.IUIAutomationElement)
			lastAddress = lastSelected.GetCurrentPropertyValue(UIAHandler.UIA_NamePropertyId)
			lastAddress = lastAddress.replace('"', '')
			lastValue = lastSelected.GetCurrentPropertyValue(UIAHandler.UIA_ValueValuePropertyId)
			return _("{firstAddress} {firstValue} through {lastAddress} {lastValue}").format(
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


class ExcelWorksheet(UIA):
	role = controlTypes.ROLE_TABLE

	# The grid UIAElement dies each time the sheet is scrolled.
	# therefore this grid would be announced in the focus ancestory each time which is bad.
	# Suppress this.
	isPresentableFocusAncestor = False

	def _get_parent(self):
		parent = super().parent
		# We want to present the parent (sheet) in the focus ancestry
		# As that is what has the sheet name.
		parent.isPresentableFocusAncestor = True
		# However, the selection state on the sheet is not useful, so remove it.
		parent.states.discard(controlTypes.STATE_SELECTED)
		return parent

class CellEdit(UIA):
	name = u""


class BadExcelFormulaEdit(UIA):
	shouldAllowUIAFocusEvent = False
