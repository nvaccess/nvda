#appModules/openWith.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2011 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from comtypes import COMError
import appModuleHandler
import controlTypes
from NVDAObjects.UIA import UIA
from NVDAObjects.behaviors import Dialog

#win8hack: the nondefault items in the list of applications are not labeled
class NonDefaultAppTile(UIA):

	def _get_name(self):
		firstChild=self.firstChild
		if firstChild:
			next=firstChild.next
			if next:
				return next.name
		return super(NonDefaultAppTile,self).name

class ImmersiveOpenWithFlyout(Dialog,UIA):

	role=controlTypes.ROLE_DIALOG

	#win8hack: This window never actually gets the physical focus thus tabbing etc goes to the original window
	#So Force it to get focus
	def event_focusEntered(self):
		self.setFocus()
		super(ImmersiveOpenWithFlyout,self).event_focusEntered()

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj,UIA):
			try:
				automationID=obj.UIAElement.currentAutomationID
			except COMError:
				automationID=None
			if automationID=="NonDefaultAppTile":
				clsList.insert(0,NonDefaultAppTile)
			elif automationID=="ImmersiveOpenWithFlyout":
				clsList.insert(0,ImmersiveOpenWithFlyout)

