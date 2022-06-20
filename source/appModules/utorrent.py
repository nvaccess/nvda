# -*- coding: UTF-8 -*-
#appModules/utorrent.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

u"""App module for µTorrent
"""

import appModuleHandler
import api
import controlTypes
import displayModel
from logHandler import log
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.window import Window
from NVDAObjects.IAccessible.sysListView32 import ListItem
import locationHelper

class DuplicateFocusListView(IAccessible):
	"""A list view which annoyingly fires focus events every second, even when a menu is open.
	"""

	def _get_shouldAllowIAccessibleFocusEvent(self):
		# Stop annoying duplicate focus events, which are fired even if a menu is open.
		focus = api.getFocusObject()
		focusRole = focus.role
		focusStates = focus.states
		if (self == focus or
			(focusRole == controlTypes.Role.MENUITEM and controlTypes.State.FOCUSED in focusStates) or
			(focusRole == controlTypes.Role.POPUPMENU and controlTypes.State.INVISIBLE not in focusStates)
		):
			return False
		return super(DuplicateFocusListView, self).shouldAllowIAccessibleFocusEvent

class TorrentContentsListItem(ListItem):
	"""Items of the Torrent Contents list in the Add Torrent dialog.
	The file names aren't exposed via APIs, though the other column (size) is.
	"""

	def _getColumnContent(self, column):
		superContent = super(TorrentContentsListItem, self)._getColumnContent(column)
		if superContent or column != 1:
			return superContent
		# We need to use the display model to retrieve the Name column.
		try:
			left, top, width, height = self._getColumnLocation(column)
			return displayModel.DisplayModelTextInfo(self, locationHelper.RectLTRB(
				left, top, left + width, top + height)).text
		except:
			log.debugWarning("Error retrieving name using display model", exc_info=True)
			return superContent

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		role = obj.role
		if role == controlTypes.Role.WINDOW:
			return

		if isinstance(obj, Window) and obj.windowClassName == "SysListView32":
			if obj.windowControlID == 1206 and role == controlTypes.Role.LISTITEM:
				clsList.insert(0, TorrentContentsListItem)
			else:
				clsList.insert(0, DuplicateFocusListView)
