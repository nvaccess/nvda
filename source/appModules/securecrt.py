#appModules/securecrt.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2016 NV Access Limited

"""App module for automatic reading of the terminal in all versions of SecureCRT
Uses regular expressions to support the ever-changing window title for different incremental SecureCRT Versions."""
import oleacc
import re
from NVDAObjects.behaviors import Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
import appModuleHandler

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		#initialize a compiles regexp object for all window names following the standard SecureCrt Window naming comvention for all versions
		MATCHER = re.compile ("AfxFrameOrView\d{2,}u")
			#perform the match with the compiled object
		if MATCHER.match (obj.windowClassName) and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT: 
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = (Terminal, DisplayModelLiveText)
