# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""App module for Microsoft Teams."""

import appModuleHandler
from NVDAObjects.IAccessible.ia2Web import Ia2Web


class PopOverMenu(Ia2Web):
	shouldAllowIAccessibleMenuStartEvent = False


class AppModule(appModuleHandler.AppModule):
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# #11821, #14355
		# Teams will sometimes create an element with an ARIA role of menu
		# at the same time another element gets focus,
		# E.g. an emoji menu appears every time a conversation message is focused.
		# Web frameworks such as Chromium will tend to fire a menu_popupStart event
		# when a node with a role of menu is added to the DOM.
		# NVDA's default behaviour for handling menu_popupStart is to set NVDA's focus to the menu
		# and cancel speech.
		# We should deliberately suppress this in Teams however,
		# Otherwise the focused message cannot be read.
		# Previously this was limited to message menus, however
		# As Teams keeps changing the layout,
		# and all menus in Teams do set focus to their first item when truly focused,
		# It is safer just to ignore all menu popupStart events within Teams content for now.
		if Ia2Web in clsList and obj.IA2Attributes.get("xml-roles") == "menu":
			clsList.insert(0, PopOverMenu)
