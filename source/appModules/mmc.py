#appModules/mmc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2019 NVDA Contributors, David Parduhn, Bill Dengler
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import ui
from NVDAObjects.IAccessible import IAccessible


class MMCTable(IAccessible):
	def script_getCurrentObject(self, gesture):
		"#1486: workaround to read tables in MMC, such as the disk management graphical view."
		gesture.send()
		for i in self.children:
			if controlTypes.STATE_SELECTED in i.states:
				ui.message(i.name + ' ' + i.value)

	__tableReviewGestures = (
		"kb:rightarrow",
		"kb:leftarrow",
		"kb:uparrow",
		"kb:downarrow",
		"kb:pageup",
		"kb:pagedown"
	)

	def initOverlayClass(self):
		# #1486: bind the navigation keys to our custom script
		for i in self.__tableReviewGestures:
			self.bindGesture(i, "getCurrentObject")


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.ROLE_TABLE:
			clsList.insert(0, MMCTable)
