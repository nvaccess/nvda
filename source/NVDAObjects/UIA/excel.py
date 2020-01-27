# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018 NV Access Limited

import UIAHandler
import controlTypes
from . import UIA


class ExcelCell(UIA):

	shouldAllowDuplicateUIAFocusEvent = True

	name = u""
	role = controlTypes.ROLE_TABLECELL
	rowHeaderText = None
	columnHeaderText = None

	def _get_value(self):
		if self.selectionContainer and self.selectionContainer.getSelectedItemsCount() > 1:
			return
		return super().value

	def _get_description(self):
		if self.selectionContainer and self.selectionContainer.getSelectedItemsCount() > 1:
			return
		return self.UIAElement.currentItemStatus

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

	def _get_name(self):
		return super().parent.name

	def _get_parent(self):
		return super().parent.parent


class CellEdit(UIA):
	name = u""


class BadExcelFormulaEdit(UIA):
	shouldAllowUIAFocusEvent = False
