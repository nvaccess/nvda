#appModules/chrome.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
# Copyright (C) 2010 James Teh <jamie@jantrid.net>

"""App module for Google Chrome
"""

import controlTypes
import appModuleHandler
from NVDAObjects.IAccessible import IAccessible, getNVDAObjectFromEvent
from virtualBuffers.gecko_ia2 import Gecko_ia2 as GeckoVBuf

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
		if obj.windowClassName == "Chrome_RenderWidgetHostHWND" and obj.role == controlTypes.ROLE_DOCUMENT:
			clsList.insert(0, Document)
			return
