#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import api
import speech
from NVDAObjects.UIA import UIA

# Windows 10 Search UI suggestion list item
class SuggestionListItem(UIA):

	role=controlTypes.ROLE_LISTITEM

	def event_UIA_elementSelected(self):
		focusControllerFor=api.getFocusObject().controllerFor
		if len(focusControllerFor)>0 and focusControllerFor[0].appModule is self.appModule:
			speech.cancelSpeech()
			api.setNavigatorObject(self)
			self.reportFocus()

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA) and obj.role==controlTypes.ROLE_DATAITEM and isinstance(obj.parent,UIA) and obj.parent.role==controlTypes.ROLE_LIST:
			clsList.insert(0,SuggestionListItem)
