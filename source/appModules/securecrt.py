#appModules/securecrt.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2012 NV Access Limited

"""App module for automatic reading of the terminal in all versions of SecureCRT
"""

import oleacc
import re
from NVDAObjects.behaviors import Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if re.match("AfxFrameOrView\d{2,}u", obj.windowClassName) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = (Terminal, DisplayModelLiveText)
