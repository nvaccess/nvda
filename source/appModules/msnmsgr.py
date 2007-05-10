#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalVars
import winUser
from NVDAObjects.IAccessible import IAccessible 
import controlTypes
import appModuleHandler
import speech

lastMSNHistoryValue=None

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_EDITABLETEXT and obj.name=="History":
			obj.__class__=MSNHistory

class MSNHistory(IAccessible):

	def _get_textRepresentation(self):
		return "%s - %s\r%s"%(self.name,self.description,self.value)

	def _get_value(self):
		value=super(self.__class__,self)._get_value()
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
		super(self.__class__,self).event_gainFocus()
		self.reviewOffset=len(self.textRepresentation)-1

	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True)

[MSNHistory.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","review_nextLine"),
	("extendedUp","review_prevLine"),
	("extendedLeft","review_prevCharacter"),
	("extendedRight","review_nextCharacter"),
	("extendedHome","review_startOfLine"),
	("extendedEnd","review_endOfLine"),
	("control+extendedLeft","review_prevWord"),
	("control+extendedRight","review_nextWord"),
	("control+extendedHome","review_top"),
	("control+extendedEnd","review_bottom"),
]]
