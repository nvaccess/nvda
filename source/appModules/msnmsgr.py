#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalVars
import winUser
from NVDAObjects.IAccessible import IAccessible 
import controlTypes
import text
import appModuleHandler
import speech

lastMSNHistoryValue=None

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_EDITABLETEXT and obj.name==_("History"):
			obj.__class__=MSNHistory

class MSNHistory(IAccessible):

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
		self.reviewPosition=self.makeTextInfo(text.POSITION_LAST)


	def reportFocus(self):
		speech.speakObjectProperties(self,name=True,role=True)

[MSNHistory.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","review_nextLine"),
	("extendedUp","review_previousLine"),
	("extendedLeft","review_previousCharacter"),
	("extendedRight","review_nextCharacter"),
	("extendedHome","review_startOfLine"),
	("extendedEnd","review_endOfLine"),
	("control+extendedLeft","review_previousWord"),
	("control+extendedRight","review_nextWord"),
	("control+extendedHome","review_top"),
	("control+extendedEnd","review_bottom"),
]]
