#NVDAObjects/IAccessible/hh.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2009 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDAObjects for Microsoft HTML Help.
"""

import IAccessibleHandler
from . import IAccessible

class KeywordList(IAccessible):

	def _get_parent(self):
		# Overridden so that accNavigate next/prev won't be called, as it causes the focus to move to another list item, even when called on the list.
		res = IAccessibleHandler.accParent(self.IAccessibleObject, self.IAccessibleChildID)
		if res:
			return self._correctRelationForWindow(IAccessible(IAccessibleObject=res[0], IAccessibleChildID=res[1]))

	def _get_next(self):
		# accNavigate on this list returns a child and moves the focus, both of which are wrong. Grrr!
		return None

	def _get_previous(self):
		# accNavigate on this list returns a child and moves the focus, both of which are wrong. Grrr!
		return None

	def _get_activeChild(self):
		# accFocus doesn't work, but accSelection does.
		sel = self.IAccessibleObject.accSelection
		if sel:
			return IAccessible(windowHandle=self.windowHandle, IAccessibleObject=self.IAccessibleObject, IAccessibleChildID=sel, event_windowHandle=self.event_windowHandle, event_objectID=self.event_objectID, event_childID=sel)
		return None

	def event_gainFocus(self):
		# When the list gains focus, it doesn't fire a focus event for the focused item.
		child = self.activeChild
		if child:
			self.event_focusEntered()
			# Redirect the focus to the active child.
			# We do this at the IAccessibleHandler level so that duplicate focus event checks will work properly.
			IAccessibleHandler.processFocusNVDAEvent(child)
		else:
			super(KeywordList, self).event_gainFocus()
