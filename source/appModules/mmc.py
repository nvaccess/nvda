#appModules/mmc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2019 NVDA Contributors, David Parduhn, Bill Dengler
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible import IAccessible


class MMCTable(IAccessible):
	def _get_value(self):
		"#1486: workaround to read tables in MMC, such as the disk management graphical view."
		for i in self.children:
			if controlTypes.STATE_SELECTED in i.states:
				return i.name + ' ' + i.value


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_TABLE and obj.windowClassName == "AfxWnd42u":
			clsList.insert(0, MMCTable)
