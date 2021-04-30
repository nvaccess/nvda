# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2020 NV Access Limited, Bill Dengler

import config

from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport
from winVersion import getWinVer, WIN10_1607

from . import IAccessible
from ..window import winConsole


class EnhancedLegacyWinConsole(KeyboardHandlerBasedTypedCharSupport, winConsole.WinConsole, IAccessible):
	"""
		A hybrid approach to console access, using legacy APIs to read output
		and KeyboardHandlerBasedTypedCharSupport for input.
	"""
	#: Legacy consoles take quite a while to send textChange events.
	#: This significantly impacts typing performance, so don't queue chars.
	_supportsTextChange = False


class LegacyWinConsole(winConsole.WinConsole, IAccessible):
	"""
		NVDA's original console support, used by default on Windows versions
		before 1607.
	"""

	def _get_diffAlgo(self):
		# Non-enhanced legacy consoles use caret proximity to detect
		# typed/deleted text.
		# Single-character changes are not reported as
		# they are confused for typed characters.
		# Force difflib to keep meaningful edit reporting in these consoles.
		from diffHandler import get_difflib_algo
		return get_difflib_algo()


def findExtraOverlayClasses(obj, clsList):
	if getWinVer() >= WIN10_1607 and config.conf['terminals']['keyboardSupportInLegacy']:
		clsList.append(EnhancedLegacyWinConsole)
	else:
		clsList.append(LegacyWinConsole)
