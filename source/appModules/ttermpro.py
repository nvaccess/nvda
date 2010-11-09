#appModules/ttermpro.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010 James Teh <jamie@jantrid.net>

"""App module for Tera Term
"""

import oleacc
from NVDAObjects.behaviors import Terminal
from NVDAObjects.window import DisplayModelEditableText, DisplayModelLiveText
from appModules import _default

class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "VTWin32" and obj.IAccessibleRole == oleacc.ROLE_SYSTEM_CLIENT:
			try:
				clsList.remove(DisplayModelEditableText)
			except ValueError:
				pass
			clsList[0:0] = (Terminal, DisplayModelLiveText)
