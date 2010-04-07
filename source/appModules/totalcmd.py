#appModules/totalcmd.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import _default
from NVDAObjects.IAccessible import IAccessible
import speech
import controlTypes

oldActivePannel=0

class AppModule(_default.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.windowClassName in ("TMyListBox", "TMyListBox.UnicodeClass"):
			clsList.insert(0, TCList)

class TCList(IAccessible):

	def event_gainFocus(self):
		global oldActivePannel
		if oldActivePannel !=self.windowControlID:
			oldActivePannel=self.windowControlID
			obj=self
			while obj and obj.parent and obj.parent.windowClassName!="TTOTAL_CMD":
				obj=obj.parent
			counter=0
			while obj and obj.previous and obj.windowClassName!="TPanel":
				obj=obj.previous
				if obj.windowClassName!="TDrivePanel":
					counter+=1
			if counter==2:
				speech.speakMessage(_("left"))
			else:
				speech.speakMessage(_("right"))
		super(TCList,self).event_gainFocus()

	def reportFocus(self):
		if self.name:
			speakList=[]
			if controlTypes.STATE_SELECTED in self.states:
				speakList.append(controlTypes.speechStateLabels[controlTypes.STATE_SELECTED])
			speakList.append(self.name.split("\\")[-1])
			speech.speakMessage(" ".join(speakList))
		else:
			super(TCList,self).reportFocus()
