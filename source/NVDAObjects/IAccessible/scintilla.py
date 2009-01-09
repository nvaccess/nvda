#NVDAObjects/IAccessible/scintilla.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.scintilla import Scintilla
from . import IAccessible

Scintilla=type("Scintilla",(Scintilla,IAccessible),{})
