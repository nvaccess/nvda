# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018 NV Access Limited

import controlTypes
from . import UIA


class ExcelCell(UIA):

	name = u""
	role = controlTypes.ROLE_TABLECELL
	rowHeaderText = None
	columnHeaderText = None

	def _get_description(self):
		return self.UIAElement.currentItemStatus

	def _get_cellCoordsText(self):
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
