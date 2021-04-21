#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016-2019 NV Access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""An appModule for the Windows 10 Mail app"""

import appModuleHandler
from comtypes import COMError
import UIAHandler
from NVDAObjects.UIA.wordDocument import WordDocument

class MailWordDocumentTreeInterceptor(WordDocument.treeInterceptorClass):

	_wasInReadingPane: bool = False

	def event_treeInterceptor_gainFocus(self):
		isInReadingPane = self.rootNVDAObject.isInReadingPane
		if isInReadingPane != self._wasInReadingPane:
			self._wasInReadingPane = isInReadingPane
			# The base WordDocument TreeInterceptorClass forces focus mode by default
			# As a TreeInterceptor is created for all word documents
			# so that the NVDA elements list is available.
			# However, Windows 10 Mail's reading pane should use browse mode.
			if isInReadingPane:
				self.disableAutoPassThrough = False
				self.passThrough = False
			else:
				self.disableAutoPassThrough = True
				self.passThrough = True
		super().event_treeInterceptor_gainFocus()

class MailWordDocument(WordDocument):

	treeInterceptorClass=MailWordDocumentTreeInterceptor

	# typing information for isInReadingPane property
	isInReadingPane: bool

	def _get_isInReadingPane(self) -> bool:
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
