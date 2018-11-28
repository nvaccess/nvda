#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2018 NV Access Limited, Joseph Lee
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

	# Somehow, item status property repeats when Action Center is opened more than once.
	_itemStatusMessageCache = None

	def event_UIA_itemStatus(self, obj, nextHandler):
		# Do not fetch cached status as doing so causes a COM error to be logged.
		itemStatus = obj.UIAElement.currentItemStatus
		if itemStatus != self._itemStatusMessageCache:
			ui.message(": ".join([obj.name, itemStatus]))
			self._itemStatusMessageCache = itemStatus
		nextHandler()
