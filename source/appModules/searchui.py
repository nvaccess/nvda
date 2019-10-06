# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2019 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Start menu/Windows Search/Cortana user interface in Windows 10 Version 1909 and earlier.
"""

import appModuleHandler
import controlTypes
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient
from NVDAObjects.UIA import UIA, SearchField, SuggestionListItem

class StartMenuSearchField(SearchField):

	# #7370: do not announce text when start menu (searchui) closes.
	announceNewLineText = False

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if isinstance(obj, IAccessible):
			try:
				# #5288: Never use ContentGenericClient, as this uses displayModel
				# which will freeze if the process is suspended.
				clsList.remove(ContentGenericClient)
			except ValueError:
				pass
		elif isinstance(obj, UIA):
			if obj.UIAElement.cachedAutomationID == "SearchTextBox":
				clsList.insert(0, StartMenuSearchField)
			# #10329: Since 2019, some suggestion items are grouped inside another suggestions list item.
			# Because of this, result details will not be announced like in the past.
			elif obj.role == controlTypes.ROLE_LISTITEM and isinstance(obj.parent, SuggestionListItem):
				clsList.insert(0, SuggestionListItem)
