#appModules/mmc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2019 NV Access Limited, David Parduhn, Bill Dengler, Leonard de Ruijter
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import api
import appModuleHandler
import controlTypes
import eventHandler
from NVDAObjects.IAccessible import IAccessible

class MMCTable(IAccessible):
	def _get_focusRedirect(self):
		# #1486: workaround to read tables in MMC, such as the disk management graphical view.
		for child in self.children:
			if controlTypes.STATE_SELECTED in child.states:
				return child
		return None


class MMCTableCell(IAccessible):
	def event_selection(self):
		if self.parent.hasFocus and api.getFocusObject() != self:
			eventHandler.executeEvent("gainFocus", self)


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "AfxWnd42u":
			if obj.role == controlTypes.ROLE_TABLE:
				clsList.insert(0, MMCTable)
			elif obj.role in (controlTypes.ROLE_TABLECELL,
			controlTypes.ROLE_TABLEROWHEADER):
				clsList.insert(0, MMCTableCell)
