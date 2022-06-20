# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2020 NV Access Limited, David Parduhn, Bill Dengler, Leonard de Ruijter, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import api
import appModuleHandler
import controlTypes
import eventHandler
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.behaviors import ToolTip

class MMCTable(IAccessible):
	def _get_focusRedirect(self):
		# #1486: workaround to read tables in MMC, such as the disk management graphical view.
		for child in self.children:
			if controlTypes.State.SELECTED in child.states:
				return child
		return None


class MMCTableCell(IAccessible):
	""" Cell and rowheader makes no sense for these controls. Mapping them to list items has added benefit
	of suppressing selected. """
	role = controlTypes.Role.LISTITEM

	def event_selection(self):
		if self.parent.hasFocus and api.getFocusObject() != self:
			eventHandler.executeEvent("gainFocus", self)

	def _get_positionInfo(self):
		""" When 'Guess object position info when unavailable' is enabled
		these controls report very strange information such as 65537 of 12, especially in braille.
		Disable reporting of position info all together. """
		return None


class toolTipWithEmptyName(ToolTip):
	previousToolTipText = ''

	def _get_name(self):
		""" ToolTips appearing when hovering mouse over graphical view have empty name,
		but it can be retrieved via display model. """
		return self.displayText

	def event_show(self):
		# Stop repeating the same tooltip over and over again.
		toolTipText = self.displayText
		if toolTipText != toolTipWithEmptyName.previousToolTipText:
			toolTipWithEmptyName.previousToolTipText = toolTipText
			super().event_show()


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "AfxWnd42u":
			if obj.role == controlTypes.Role.TABLE:
				clsList.insert(0, MMCTable)
			elif obj.role in (controlTypes.Role.TABLECELL,
			controlTypes.Role.TABLEROWHEADER):
				clsList.insert(0, MMCTableCell)
		if obj.windowClassName == "tooltips_class32" and obj.name is None:
			clsList.insert(0, toolTipWithEmptyName)
