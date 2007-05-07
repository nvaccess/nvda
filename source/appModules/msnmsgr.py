#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalVars
import winUser
import NVDAObjects
import controlTypes
import appModuleHandler
import speech

lastMSNHistoryValue=None

class appModule(appModuleHandler.appModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="DirectUIHWND" and obj.role==controlTypes.ROLE_EDITABLETEXT and obj.name=="History":
			obj.__class__=NVDAObject_MSNHistory

class NVDAObject_MSNHistory(NVDAObjects.IAccessible.NVDAObject_directUIHwndText):

	def __init__(self,*args,**kwargs):
		super(self.__class__,self).__init__(*args,**kwargs)
		self._lastMSNHistoryValue=None

	def event_valueChange(self):
		global lastMSNHistoryValue
		if isinstance(self,NVDAObject_MSNHistory) and winUser.isDescendantWindow(winUser.getForegroundWindow(),self.windowHandle):
			value=self.value
			if value!=lastMSNHistoryValue and globalVars.reportDynamicContentChanges:
				speech.speakText(value)
				lastMSNHistoryValue=value

	def event_gainFocus(self):
		super(self.__class__,self).event_gainFocus()
		self.text_reviewOffset=self.text_characterCount-1

	def reportFocus(self):
		speech.speakMessage("%s %s %s"%(self.name,self.typeString,self.description))

[NVDAObject_MSNHistory.bindKey(keyName,scriptName) for keyName,scriptName in [
	("extendedDown","text_review_nextLine"),
	("extendedUp","text_review_prevLine"),
	("extendedLeft","text_review_prevCharacter"),
	("extendedRight","text_review_nextCharacter"),
	("extendedHome","text_review_startOfLine"),
	("extendedEnd","text_review_endOfLine"),
	("control+extendedLeft","text_review_prevWord"),
	("control+extendedRight","text_review_nextWord"),
	("control+extendedHome","text_review_top"),
	("control+extendedEnd","text_review_bottom"),
]]
