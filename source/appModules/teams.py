# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Leonard de Ruijter
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

""" App module for Microsoft Teams.
"""

import appModuleHandler
from NVDAObjects.IAccessible.ia2Web import Ia2Web


class PopOverMenu(Ia2Web):
	shouldAllowIAccessibleMenuStartEvent = False


class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if (
			Ia2Web in clsList
			and obj.IA2Attributes.get("xml-roles") == "menu"
			and obj.parent
			and obj.parent.parent
			and "message-actions-popover-container" in obj.parent.parent.IA2Attributes.get("class", "")
		):
			clsList.insert(0, PopOverMenu)
