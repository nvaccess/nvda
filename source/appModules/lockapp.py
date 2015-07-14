#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
from NVDAObjects.UIA import UIA

# Windows 10 lock screen container
class LockAppContainer(UIA):
	presentationType=UIA.presType_content

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA) and obj.role==controlTypes.ROLE_PANE and obj.UIAElement.cachedClassName=="LockAppContainer":
			clsList.insert(0,LockAppContainer)
