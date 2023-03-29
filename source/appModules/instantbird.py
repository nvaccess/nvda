#appModules/instantbird.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2013 NV Access Limited

"""App module for Instantbird
"""

import appModuleHandler
import NVDAObjects.IAccessible.mozilla
import controlTypes

class AppModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self, obj):
		if isinstance(obj, NVDAObjects.IAccessible.IAccessible) and obj.windowClassName == "MozillaWindowClass" and not isinstance(obj, NVDAObjects.IAccessible.mozilla.Mozilla) and obj.role == controlTypes.Role.UNKNOWN:
			# #2667: This is a Mozilla accessible that has already died.
			# Instantbird fires focus on a dead accessible first every time you focus a contact,
			# so block focus on these to eliminate annoyance.
			obj.shouldAllowIAccessibleFocusEvent = False
