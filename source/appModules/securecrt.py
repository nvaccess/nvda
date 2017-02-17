			#appModules/securecrt.py
# Modified to include a regular expression so that all Secure CRT versions are supported past, present, and future.
# Modification of original securecrt.py by Noel Romey 9/2016
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2016 NV Access Limited

"""App module for automatic reading of terminal windows in all versions of SecureCRT past, present and future
"""

import oleacc
import re
from NVDAObjects.behaviors import Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
import appModuleHandler
#initialize a compiles regexp object for all window names following the standard SecureCrt Window naming comvention for all versions
RE_Terminal_WinClass = re.compile ("AfxFrameOrView\d{2,}u")
class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
	#perform the match with the compiled object
		if Terminal_WinClass.match (obj.windowClassName) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT: 
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = (Terminal, DisplayModelLiveText)
