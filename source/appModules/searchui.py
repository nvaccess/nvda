# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2015-2022 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Start menu/Windows Search/Cortana user interface in Windows 10 Version 1909 and earlier.
This app module also serves as the basis for Start menu in Windows 10 Version 2004 and later
as well as Windows 11, represented by alias app modules.
"""

import appModuleHandler
import controlTypes
import winVersion
from NVDAObjects.IAccessible import IAccessible, ContentGenericClient
from NVDAObjects.UIA import UIA, SearchField, SuggestionListItem


class StartMenuSearchField(SearchField):

	# #7370: do not announce text when start menu (searchui) closes.
	announceNewLineText = False


class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, UIA):
			# #10341: Build 18363 introduces modern search experience in File Explorer.
			# As part of this, suggestion count is part of a live region.
			# Although it is geared for Narrator, it is applicable to other screen readers as well.
			# The live region itself is a child of the one shown here.
			if (
				winVersion.getWinVer() >= winVersion.WIN10_1909
				and obj.UIAAutomationId == "suggestionCountForNarrator"
				and obj.firstChild is not None
			):
				obj.name = obj.firstChild.name

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, IAccessible):
			try:
				# #5288: Never use ContentGenericClient, as this uses displayModel
				# which will freeze if the process is suspended.
				clsList.remove(ContentGenericClient)
			except ValueError:
				pass
		elif isinstance(obj, UIA):
			if obj.UIAAutomationId == "SearchTextBox":
				clsList.insert(0, StartMenuSearchField)
			# #10329: Since 2019, some suggestion items are grouped inside another suggestions list item.
			# #13544: grandparent must be checked due to redesign in 2019.
			# Because of this, result details will not be announced like in the past.
			elif (
				obj.role == controlTypes.Role.LISTITEM and (
					isinstance(obj.parent, SuggestionListItem)
					or isinstance(obj.parent.parent, SuggestionListItem)
				)
			):
				clsList.insert(0, SuggestionListItem)
