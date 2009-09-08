#NVDAObjects/IAccessible/qt.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import controlTypes
from NVDAObjects.IAccessible import IAccessible

class Menu(IAccessible):

	def _get_states(self):
		states = super(Menu, self)._get_states()
		# QT fires a focus event on the parent menu immediately after firing focus on the menu item.
		# The focus on the menu is invalid, so remove its focused state so it will be treated as such.
		states.discard(controlTypes.STATE_FOCUSED)
		return states
