#appModules/securecrt.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2017 NV Access Limited, Noel Romey

"""App module for SecureCRT
"""

import re
import oleacc
from NVDAObjects.behaviors import Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
import appModuleHandler

# Regexp which matches the terminal window class in all existing versions
# (and hopefully future ones).
# For example, it matches "AfxFrameOrView80u", "AfxFrameOrView90u" and "AfxFrameOrView100u".
RE_TERMINAL_WINCLASS = re.compile (r"AfxFrameOrView\d{2,}u")

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if RE_TERMINAL_WINCLASS.match (obj.windowClassName) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT: 
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = (Terminal, DisplayModelLiveText)
