# appModules/1password.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 James Teh
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import appModuleHandler
import UIAHandler


class AppModule(appModuleHandler.AppModule):

	def shouldProcessUIAPropertyChangedEvent(self, sender, propertyId):
		if propertyId in (
			UIAHandler.UIA_NamePropertyId,
			UIAHandler.UIA_ItemStatusPropertyId,
			UIAHandler.UIA_IsEnabledPropertyId
		):
			# #10508: 1Password floods property change events, resulting in very poor
			# performance. Just drop them.
			return False
		return True
