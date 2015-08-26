#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import controlTypes
import api
import speech
from NVDAObjects.UIA import UIA
from NVDAObjects.UIA.edge import EdgeList
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient

# Windows 10 Search UI suggestion list item
class SuggestionListItem(UIA):

	role=controlTypes.ROLE_LISTITEM

	def event_UIA_elementSelected(self):
		focusControllerFor=api.getFocusObject().controllerFor
		if len(focusControllerFor)>0 and focusControllerFor[0].appModule is self.appModule and self.name:
			speech.cancelSpeech()
			api.setNavigatorObject(self)
			self.reportFocus()

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA) and isinstance(obj.parent,EdgeList):
			clsList.insert(0,SuggestionListItem)
		elif isinstance(obj,IAccessible):
			try:
				# #5288: Never use ContentGenericClient, as this uses displayModel
				# which will freeze if the process is suspended.
				clsList.remove(ContentGenericClient)
			except ValueError:
				pass
