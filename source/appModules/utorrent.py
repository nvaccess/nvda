#appModules/utorrent.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

u"""App module for µTorrent
"""

import _default
import api
import controlTypes
import displayModel
from logHandler import log
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window

class DuplicateFocusListView(IAccessible):
	"""A list view which annoyingly fires focus events every second, even when a menu is open.
	"""

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# Stop annoying duplicate focus events, which are fired even if a menu is open.
		focus = api.getFocusObject()
		focusRole = focus.role
		focusStates = focus.states
		if (self == focus or
			(focusRole == controlTypes.ROLE_MENUITEM and controlTypes.STATE_FOCUSED in focusStates) or
			(focusRole == controlTypes.ROLE_POPUPMENU and controlTypes.STATE_INVISIBLE not in focusStates)
		):
			return False
		return super(DuplicateFocusListView, self).shouldAllowIAccessibleFocusEvent

class TorrentContentsListItem(IAccessible):
	"""Items of the Torrent Contents list in the Add Torrent dialog.
	The file names aren't exposed to MSAA, though the other column (size) is.
	"""

	def _get_name(self):
		superName = super(TorrentContentsListItem, self).name
		if superName:
			return superName

		# We need to use the display model to retrieve the Name column.
		try:
			# We don't want to just use displayText because it also contains the size, which is exposed correctly in the value property.
			# Therefore, use the left and right of the Name column as obtained from the column header.
			nameHdrLoc = Window._get_firstChild(self).firstChild.firstChild.location
			left = nameHdrLoc[0]
			right = left + nameHdrLoc[2]
			# Use the top and bottom of the list item.
			selfLoc = self.location
			top = selfLoc[1]
			bottom = top + selfLoc[3]
			return displayModel.getWindowTextInRect(self.appModule.helperLocalBindingHandle, self.windowHandle,
				left, top, right, bottom,
				displayModel.DisplayModelTextInfo.minHorizontalWhitespace, displayModel.DisplayModelTextInfo.minVerticalWhitespace)[0]
		except:
			log.debugWarning("Error retrieving name using display model", exc_info=True)
			return superName

class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		role = obj.role
		if role == controlTypes.ROLE_WINDOW:
			return

		if obj.windowClassName == "SysListView32":
			if obj.windowControlID == 1206 and role == controlTypes.ROLE_LISTITEM:
				clsList.insert(0, TorrentContentsListItem)
			else:
				clsList.insert(0, DuplicateFocusListView)
