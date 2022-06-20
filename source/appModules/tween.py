# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2022 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""App module for Tween
"""

from typing import Optional
import appModuleHandler
import controlTypes
from NVDAObjects.window import Window
import winUser
from NVDAObjects.IAccessible.sysListView32 import ListItem
import displayModel
import locationHelper


class TweetListItem(ListItem):

	def initOverlayClass(self):
		self._isGettingName = False

	def _get_name(self):
		self._isGettingName = True
		try:
			return super(TweetListItem, self).name
		finally:
			self._isGettingName = False

	def _getColumnHeaderRaw(self, index: int) -> Optional[str]:
		if self._isGettingName and index in (1, 2):
			# If this is for use in the name property,
			# don't include the headers for the Name and Post columns.
			return None
		res = super()._getColumnHeaderRaw(index)
		if res:
			res = res.replace("▾", "")
		return res

	def _getColumnContentRaw(self, index: int) -> Optional[str]:
		if controlTypes.State.INVISIBLE not in self.states and index == 3:
			# This is the date column.
			# Its content is overridden on screen,
			# so use display model.
			left, top, width, height = self._getColumnLocationRaw(index)
			content = displayModel.DisplayModelTextInfo(
				self,
				locationHelper.RectLTRB(left, top, left + width, top + height)
			).text
			if content:
				return content
		return super()._getColumnContentRaw(index)


class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if not isinstance(obj, Window):
			return
		role = obj.role
		if role == controlTypes.Role.WINDOW:
			return
		wclass = Window.normalizeWindowClassName(obj.windowClassName)

		if wclass == "Window.8" and role == controlTypes.Role.PANE:
			# optimisation: There are quite a lot of these, so let's not instantiate parent NVDAObjects unnecessarily.
			parentWindow = winUser.getAncestor(obj.windowHandle, winUser.GA_PARENT)
			if parentWindow and Window.normalizeWindowClassName(winUser.getClassName(parentWindow)) == "SysTabControl32":
				obj.role = controlTypes.Role.PROPERTYPAGE

		elif wclass == "SysTabControl32":
			obj.isPresentableFocusAncestor = False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if ListItem in clsList:
			clsList.insert(0, TweetListItem)
