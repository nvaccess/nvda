#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015-2018 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Shell Experience Host, part of Windows 10.
Shell Experience Host is home to a number of things, including Action Center and other shell features.
"""

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient
import ui

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj, IAccessible):
			try:
				# #5288: Never use ContentGenericClient, as this uses displayModel
				# which will freeze if the process is suspended.
				clsList.remove(ContentGenericClient)
			except ValueError:
				pass

	# Argh, somehow, item status property repeats when Action Center is opened more than once.
	_itemStatusMessage = None

	def event_UIA_itemStatus(self, obj, nextHandler):
		itemStatus = obj.UIAElement.currentItemStatus
		if itemStatus != self._itemStatusMessage:
			ui.message(": ".join([obj.name, itemStatus]))
			self._itemStatusMessage = itemStatus
		nextHandler()
