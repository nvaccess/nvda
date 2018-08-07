#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited

import controlTypes
import UIAHandler
from . import UIA

class ExcelCell(UIA):

	name=u""
	role=controlTypes.ROLE_TABLECELL
	rowHeaderText=None
	columnHeaderText=None

	def _get_states(self):
		states=super(ExcelCell,self).states
		states.discard(controlTypes.STATE_SELECTED)
		return states

	def _get_description(self):
		return self.UIAElement.currentItemStatus
		
	def _get_cellCoordsText(self):
		return super(ExcelCell,self).name

class ExcelWorksheet(UIA):
	role=controlTypes.ROLE_TABLE

	def _get_name(self):
		return super(ExcelWorksheet,self).parent.name

	def _get_parent(self):
		return super(ExcelWorksheet,self).parent.parent

class CellEdit(UIA):
	name=u""

class BadExcelFormulaEdit(UIA):
	shouldAllowUIAFocusEvent=False
