#appModules/mmc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2019 NV Access Limited, David Parduhn, Bill Dengler, Leonard de Ruijter
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible import IAccessible
import eventHandler


class MMCTable(IAccessible):
	def _get_focusRedirect(self):
		#1486: workaround to read tables in MMC, such as the disk management graphical view.
		for child in self.children:
			if controlTypes.STATE_SELECTED in child.states:
				return child
		return None

class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_TABLE and obj.windowClassName == "AfxWnd42u":
			clsList.insert(0, MMCTable)

	def event_selection(self, obj, nextHandler):
		parent = obj.parent
		if isinstance(parent, MMCTable) and parent.hasFocus:
			eventHandler.executeEvent("gainFocus", obj)
		nextHandler()
