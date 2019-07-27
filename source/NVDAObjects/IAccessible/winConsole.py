#NVDAObjects/IAccessible/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2019 NV Access Limited, Bill Dengler

import config

from winVersion import isWin10

from . import IAccessible
from ..window.winConsole import WinConsole as LegacyWinConsole

class WinConsole(LegacyWinConsole, IAccessible):
	"The legacy console implementation for situations where UIA isn't supported."
	pass

def findExtraOverlayClasses(obj, clsList):
	if isWin10(1607) and config.conf['terminals']['keyboardSupportInLegacy']:
		from NVDAObjects.behaviors import TerminalWithKeyboardSupport
		clsList.append(TerminalWithKeyboardSupport)
	clsList.append(WinConsole)