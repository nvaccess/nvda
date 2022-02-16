# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016-2022 NV Access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""An appModule for the Windows Mail app, for Windows 10 and 11."""

import controlTypes
import appModuleHandler
from comtypes import COMError
import UIAHandler
from NVDAObjects.UIA.wordDocument import WordDocument

class MailWordDocumentTreeInterceptor(WordDocument.treeInterceptorClass):

	def _get_isAlive(self):
		return super(MailWordDocumentTreeInterceptor,self).isAlive and self.rootNVDAObject.shouldCreateTreeInterceptor

class MailWordDocument(WordDocument):

	treeInterceptorClass=MailWordDocumentTreeInterceptor
	def _get_shouldCreateTreeInterceptor(self):
		# Newer versions of Mail (Windows 11+) correctly set the readonly state for emails
		if controlTypes.State.READONLY in self.states:
			return True

		# For older versions of Mail (Windows 10), determine the readonly state
		# based on being in an email with set headers, rather than draft headers.

		# Locate the Reading pane in the ancestors
		condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ClassNamePropertyId,"ReadingPaneModern")
		walker=UIAHandler.handler.clientObject.createTreeWalker(condition)
		# #9341: when Mail app exits, tree interceptor isn't cleaned up properly ,raising COM error exception and causing NVDA to go silent.
		try:
			parent=walker.NormalizeElement(self.UIAElement)
		except COMError:
			parent=None
		if not parent:
			return False
		# If we can find the message headers, then it is read-only and therefore needs browseMode
		# An editable document contains draft headers instead
		condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_AutomationIdPropertyId,"MessageHeader")
		header=parent.findFirst(UIAHandler.TreeScope_Descendants,condition)
		return bool(header)

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self,obj,clsList):
		if WordDocument in clsList:
			clsList.insert(0,MailWordDocument)
