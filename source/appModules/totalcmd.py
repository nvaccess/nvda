#appModules/totalcmd.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2012 NVDA Contributors
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import appModuleHandler
from NVDAObjects.IAccessible import IAccessible
import speech
import controlTypes
import ui

currIndex = 0
allIndex = 0
oldActivePannel=0
x64trigger = 0

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if self.is64BitProcess:
			if obj.windowClassName in ("LCLListBox", "LCLListBox.UnicodeClass"):
				clsList.insert(0, TCList)
		else:
			x64trigger = 0
			if obj.windowClassName in ("TMyListBox", "TMyListBox.UnicodeClass"):
				clsList.insert(0, TCList)


class TCList(IAccessible):

	def event_gainFocus(self):
		global oldActivePannel
		global x64trigger
		if oldActivePannel !=self.windowControlID:
			oldActivePannel=self.windowControlID
			obj=self
			while obj and obj.parent and obj.parent.windowClassName!="TTOTAL_CMD":
				obj=obj.parent
			counter=0
			while obj and obj.previous and obj.windowClassName!="Window":
				obj=obj.previous
				if obj.windowClassName!="TDrivePanel":
					counter+=1
				if self.appModule.is64BitProcess:
					if counter == 3:
						x64trigger = 1
			if x64trigger == 1:
				counter-=1
			if counter==2:
				ui.message(_("left"))
			else:
				ui.message(_("right"))
		super(TCList,self).event_gainFocus()

	def reportFocus(self):
		if self.name:
			currIndex = self.IAccessibleChildID
			allIndex = self.parent.childCount
			indexString = (" %s of %s" % (currIndex, allIndex))
			speakList=[]
			if controlTypes.STATE_SELECTED in self.states:
				speakList.append(controlTypes.stateLabels[controlTypes.STATE_SELECTED])
			speakList.append(self.name.split("\\")[-1])
			speakList.append(indexString)
			speech.speakMessage(" ".join(speakList))
		else:
			super(TCList,self).reportFocus()
