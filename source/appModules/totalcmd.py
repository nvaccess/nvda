#appModules/totalcmd.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
import speech
import controlTypes

oldActivePannel=0

class appModule(appModuleHandler.AppModule):

	def event_NVDAObject_init(self,obj):
		if obj.windowClassName=="TMyListBox":
			obj.__class__=TCList

class TCList(IAccessible):

	def event_gainFocus(self):
		global oldActivePannel
		if oldActivePannel !=self.windowControlID:
			oldActivePannel=self.windowControlID
			obj=self
			while obj and obj.parent.windowClassName!="TTOTAL_CMD":
				obj=obj.parent
			obj=obj.previous
			try:
				obj=obj.previous
			except:
				obj=None
			if obj:
				speech.speakMessage(_("left"))
			else:
				speech.speakMessage(_("right"))
		super(TCList,self).event_gainFocus()

	def reportFocus(self):
		if self.name:
			speakList=[]
			if controlTypes.STATE_SELECTED in self.states:
				speakList.append(controlTypes.speechStateLabels[controlTypes.STATE_SELECTED])
			speakList.append(self.name)
			speech.speakMessage(" ".join(speakList))
		else:
			super(TCList,self).reportFocus()
