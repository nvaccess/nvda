#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import config
import winUser
from NVDAObjects.IAccessible import IAccessible 
import controlTypes
import oleacc
import textInfos
import appModuleHandler
import speech
import cursorManager

lastMSNHistoryValue=None
possibleHistoryWindowNames=frozenset([
'History',
'Geskiedenis',
'Verlauf',
'Historia',
'Historial',
'Historique',
'Cronologia',
'HistÃ³rico',
'Histórico',
'HistÃ³ria',
'LÆ°á»£c Sá',
'è¨˜éŒ',
'Historik',
'Előzmények',
'Geçmiş',
'المحفوظات',
])

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_EDITABLETEXT and obj.name in possibleHistoryWindowNames:
			from NVDAObjects.window import DisplayModelEditableText 
			clsList.remove(DisplayModelEditableText)
			clsList.insert(0, OldMSNHistory)
		elif obj.windowClassName=='WLXDUI' and obj.role==controlTypes.ROLE_ALERT and obj.IAccessibleStates&oleacc.STATE_SYSTEM_ALERT_MEDIUM:
			clsList.insert(0, MSNHistory)

class OldMSNHistory(cursorManager.ReviewCursorManager,IAccessible):

	def _get_basicText(self):
		return "%s - %s\r%s"%(self.name,self.description,self.value)

	def _get_value(self):
		value=super().value
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
		super().event_gainFocus()
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
