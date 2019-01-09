#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2019 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Shell Experience Host, part of Windows 10.
Shell Experience Host is home to a number of things, including Action Center and other shell features.
"""

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient
from NVDAObjects.UIA import UIA
import controlTypes
import ui

class ActionCenterToggleButton(UIA):

	# Somehow, item status property repeats when Action Center is opened more than once.
	_itemStatusMessageCache = None

	def _get_value(self):
		return self.UIAElement.currentItemStatus

	def event_UIA_itemStatus(self):
		self.event_valueChange()

	def event_valueChange(self):
		# Do not repeat item status multiple times.
		currentItemStatus = self.value
		if currentItemStatus and currentItemStatus != self._itemStatusMessageCache:
			ui.message(currentItemStatus)
		self._itemStatusMessageCache = currentItemStatus


class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, UIA):
			# #8845: Brightness button in Action Center is a button, not a toggle button.
			# Brightness control is now a slider in build 18277.
			if obj.UIAElement.cachedAutomationID == "Microsoft.QuickAction.Brightness":
				obj.role = controlTypes.ROLE_BUTTON
				obj.states.discard(controlTypes.STATE_CHECKABLE)

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj, IAccessible):
			try:
				# #5288: Never use ContentGenericClient, as this uses displayModel
				# which will freeze if the process is suspended.
				clsList.remove(ContentGenericClient)
			except ValueError:
				pass
		elif isinstance(obj, UIA) and obj.role == controlTypes.ROLE_TOGGLEBUTTON and obj.UIAElement.cachedClassName == "ToggleButton":
			clsList.insert(0, ActionCenterToggleButton)
