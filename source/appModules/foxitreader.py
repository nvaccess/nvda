#foxitreader.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, adobeAcrobat
import controlTypes
import winUser

class AppModule(appModuleHandler.AppModule):

	def isBadUIAWindow(self, hwnd):
		# #8944: The Foxit Reader UIA implementation is known to be incomplete.
		if winUser.getClassName(hwnd) == "FoxitDocWnd":
			return True
		return False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj, IAccessible) and obj.windowClassName == "FoxitDocWnd":
			clsList[:]=[]
			adobeAcrobat.findExtraOverlayClasses(obj, clsList)
