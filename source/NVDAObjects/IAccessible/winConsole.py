#NVDAObjects/IAccessible/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2019 NV Access Limited, Bill Dengler

from . import IAccessible
from ..window.winConsole import WinConsole

class WinConsole(WinConsole, IAccessible):
	"The legacy console implementation for situations where UIA isn't supported."
	pass