#appModules/putty.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2019 NV Access Limited, Bill Dengler

"""App module for PuTTY
"""

import oleacc
from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport, Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
from winVersion import getWinVer, WIN10_1607

class AppModule(appModuleHandler.AppModule):
	# Allow this to be overridden for derived applications.
	TERMINAL_WINDOW_CLASS = "PuTTY"

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName ==  self.TERMINAL_WINDOW_CLASS and isinstance(obj,IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			if getWinVer() >= WIN10_1607:
				clsList[0:0] = (KeyboardHandlerBasedTypedCharSupport, DisplayModelLiveText)
			else:
				clsList[0:0] = (Terminal, DisplayModelLiveText)
