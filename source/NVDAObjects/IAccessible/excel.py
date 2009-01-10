#NVDAObjects/IAccessible/excel.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.excel import ExcelGrid
from . import IAccessible

class ExcelGrid(ExcelGrid,IAccessible):
	pass
