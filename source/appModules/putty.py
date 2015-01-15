#appModules/putty.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2014 NV Access Limited

"""App module for PuTTY
"""

import oleacc
from NVDAObjects.behaviors import Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible

class AppModule(appModuleHandler.AppModule):
	# Allow this to be overridden for derived applications.
	TERMINAL_WINDOW_CLASS = "PuTTY"

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName ==  self.TERMINAL_WINDOW_CLASS and isinstance(obj,IAccessible) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = (Terminal, DisplayModelLiveText)
