#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
import UIAHandler
from NVDAObjects.UIA.wordDocument import WordDocument

class MailWordDocumentTreeInterceptor(WordDocument.treeInterceptorClass):

	def _get_isAlive(self):
		return super(MailWordDocumentTreeInterceptor,self).isAlive and self.rootNVDAObject.shouldCreateTreeInterceptor

class MailWordDocument(WordDocument):

	treeInterceptorClass=MailWordDocumentTreeInterceptor
	def _get_shouldCreateTreeInterceptor(self):
		# Locate the Reading pane in the ancestors
		condition=UIAHandler.handler.clientObject.createPropertyCondition(UIAHandler.UIA_ClassNamePropertyId,"ReadingPaneModern")
		walker=UIAHandler.handler.clientObject.createTreeWalker(condition)
		parent=walker.NormalizeElement(self.UIAElement)
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
