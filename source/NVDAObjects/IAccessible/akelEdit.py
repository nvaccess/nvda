#NVDAObjects/IAccessible/akelEdit.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.window.akelEdit import AkelEdit
from . import IAccessible

AkelEdit=type("AkelEdit",(AkelEdit,IAccessible),{})
