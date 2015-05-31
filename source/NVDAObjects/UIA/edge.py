#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2015 NV Access Limited

from comtypes import COMError
import eventHandler
import controlTypes
import winUser
import browseMode
import treeInterceptorHandler
import cursorManager
from . import UIA

class EdgeHTMLRootContainer(UIA):

	shouldAllowUIAFocusEvent=True

	def event_gainFocus(self):
		firstChild=self.firstChild
		if isinstance(firstChild,UIA):
			eventHandler.executeEvent("gainFocus",firstChild)
			return
		return super(EdgeHTML,self).event_gainFocus()

class EdgeHTMLTreeInterceptor(cursorManager.ReviewCursorManager,browseMode.BrowseModeTreeInterceptor,treeInterceptorHandler.DocumentTreeInterceptor):

	TextInfo=treeInterceptorHandler.RootProxyTextInfo

	def _get_isAlive(self):
		if not winUser.isWindow(self.rootNVDAObject.windowHandle):
			return False
		try:
			self.rootNVDAObject.UIAElement.currentProviderDescription
		except COMError:
			return False
		return True

	def __contains__(self,obj):
		if not isinstance(obj,UIA):
			return False
		try:
			self.rootNVDAObject.makeTextInfo(obj)
		except LookupError:
			return False
		return True

	def event_gainFocus(self,obj,nextHandler):
		info=self.makeTextInfo(obj)
		info.updateCaret()
		nextHandler()

class EdgeHTMLRoot(UIA):

	treeInterceptorClass=EdgeHTMLTreeInterceptor
	role=controlTypes.ROLE_DOCUMENT
