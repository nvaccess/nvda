#appModules/chrome.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# Copyright (C) 2010-2012 NV Access Limited

"""App module for Google Chrome
"""

import controlTypes
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, getNVDAObjectFromEvent
from virtualBuffers.gecko_ia2 import Gecko_ia2 as GeckoVBuf
from NVDAObjects.behaviors import Dialog

class ChromeVBuf(GeckoVBuf):

	def __contains__(self, obj):
		return obj.windowHandle == self.rootNVDAObject.windowHandle

class Document(IAccessible):

	def _get_treeInterceptorClass(self):
		states = self.states
		if controlTypes.STATE_READONLY in states and controlTypes.STATE_BUSY not in states:
			return ChromeVBuf
		return super(Document, self).treeInterceptorClass

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName == "Chrome_RenderWidgetHostHWND":
			if obj.role == controlTypes.ROLE_DOCUMENT:
				clsList.insert(0, Document)
				return
			if obj.role == controlTypes.ROLE_DIALOG:
				xmlRoles = obj.IA2Attributes.get("xml-roles", "").split(" ")
				if "dialog" in xmlRoles:
					# #2390: Don't try to calculate text for ARIA dialogs.
					try:
						clsList.remove(Dialog)
					except ValueError:
						pass
