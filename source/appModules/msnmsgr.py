#coding=UTF-8
#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalVars
import winUser
from NVDAObjects.IAccessible import IAccessible 
import controlTypes
import textHandler
import appModuleHandler
import speech
import cursorManager

lastMSNHistoryValue=None
possibleHistoryWindowNames=frozenset([
u'History',
u'Geskiedenis',
u'Verlauf',
u'Historia',
u'Historique',
u'Cronologia',
u'HistÃ³rico',
u'Histórico',
u'HistÃ³ria',
u'LÆ°á»£c Sá',
u'è¨˜éŒ',
u'Historik',
])

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_EDITABLETEXT and obj.name in possibleHistoryWindowNames:
			obj.__class__=MSNHistory
			# This is necessary because we're reassigning __class__ and the __init__ for the new class doesn't get called.
			obj.initCursorManager()

class MSNHistory(cursorManager.ReviewCursorManager,IAccessible):

	def _get_basicText(self):
		return "%s - %s\r%s"%(self.name,self.description,self.value)

	def _get_value(self):
		value=super(MSNHistory,self)._get_value()
		if not isinstance(value,basestring):
			value=""
		return value

	def event_valueChange(self):
		global lastMSNHistoryValue
		if isinstance(self,MSNHistory) and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			value=self.value
			if value!=lastMSNHistoryValue and globalVars.reportDynamicContentChanges:
				speech.speakText(value)
				lastMSNHistoryValue=value

	def event_gainFocus(self):
		super(MSNHistory,self).event_gainFocus()
		self.selection=self.makeTextInfo(textHandler.POSITION_LAST)

	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True)
