# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2021 NV Access Limited, Mesar Hameed, Peter Vágner
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import config
import winUser
from NVDAObjects.IAccessible import IAccessible 
import controlTypes
import oleacc
import textInfos
import appModuleHandler
import speech
import cursorManager
from comtypes import COMError


lastMSNHistoryValue=None
possibleHistoryWindowNames=frozenset([
u'History',
u'Geskiedenis',
u'Verlauf',
u'Historia',
u'Historial',
u'Historique',
u'Cronologia',
u'HistÃ³rico',
u'Histórico',
u'HistÃ³ria',
u'LÆ°á»£c Sá',
u'è¨˜éŒ',
u'Historik',
u'Előzmények',
u'Geçmiş',
u'المحفوظات',
])

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.Role.EDITABLETEXT and obj.name in possibleHistoryWindowNames:
			from NVDAObjects.window import DisplayModelEditableText 
			clsList.remove(DisplayModelEditableText)
			clsList.insert(0, OldMSNHistory)
		elif obj.windowClassName==u'WLXDUI' and obj.role==controlTypes.Role.ALERT and obj.IAccessibleStates&oleacc.STATE_SYSTEM_ALERT_MEDIUM:
			clsList.insert(0, MSNHistory)

class OldMSNHistory(cursorManager.ReviewCursorManager,IAccessible):

	def _get_basicText(self):
		return "%s - %s\r%s"%(self.name,self.description,self.value)

	def _get_value(self):
		value=super(OldMSNHistory,self).value
		if not isinstance(value,str):
			value=""
		return value

	def event_valueChange(self):
		global lastMSNHistoryValue
		if isinstance(self,OldMSNHistory) and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			value=self.value
			if value!=lastMSNHistoryValue and config.conf["presentation"]["reportDynamicContentChanges"]:
				speech.speakText(value)
				lastMSNHistoryValue=value

	def event_gainFocus(self):
		super(OldMSNHistory,self).event_gainFocus()
		self.selection=self.makeTextInfo(textInfos.POSITION_LAST)

	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True)

class MSNHistory(IAccessible):

	def _get_value(self):
		try:
			value=self.IAccessibleObject.accValue(self.IAccessibleChildID)
		except COMError:
			value=None
		return value or ""

	def event_valueChange(self):
		global lastMSNHistoryValue
		if winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			value=self.value
			if value!=lastMSNHistoryValue and config.conf["presentation"]["reportDynamicContentChanges"]:
				speech.speakText(value)
				lastMSNHistoryValue=value
