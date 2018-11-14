#foxitreader.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

import appModuleHandler
from NVDAObjects.UIA import UIA
import cursorManager
from UIABrowseMode import UIABrowseModeDocument
import controlTypes

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if isinstance(obj,UIA) and obj.UIAElement.cachedClassName == "FoxitPDFDocument":
			clsList.insert(0, FoxitRoot)

class FoxitRoot(UIA):
	treeInterceptorClass = UIABrowseModeDocument

	def _get_shouldCreateTreeInterceptor(self):
		return self.role==controlTypes.ROLE_DOCUMENT
