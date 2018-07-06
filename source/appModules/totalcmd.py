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

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if self.is64BitProcess:
			if obj.windowClassName in ("LCLListBox", "LCLListBox.UnicodeClass"):
				clsList.insert(0, TCList)
		else:
			if obj.windowClassName in ("TMyListBox", "TMyListBox.UnicodeClass"):
				clsList.insert(0, TCList)


class TCList(IAccessible):

	def event_gainFocus(self):
		global oldActivePannel
		if oldActivePannel !=self.windowControlID:
			oldActivePannel=self.windowControlID
			obj=self
			obj2 = self
			while obj and obj.parent and obj.parent.windowClassName!="TTOTAL_CMD":
				obj=obj.parent
			while obj and obj.previous and obj.windowClassName!="Window":
				obj=obj.previous
			try:
				if obj2.parent.parent.previous.firstChild.role  == controlTypes.ROLE_LIST:
					# Translators: the word left for the left window in your language (only the word left).
					ui.message(_("left"))
				else:
					# Translators: the word right for the right window in your language (only the word right).
					ui.message(_("right"))
			except AttributeError:
				pass
		super(TCList,self).event_gainFocus()

	def reportFocus(self):
		if self.name:
			currIndex = self.IAccessibleChildID
			allIndex = self.parent.childCount
			if currIndex == 1:
				# Translators: the word  Top for reaching the top of the list in your language (only the word Top).
				ui.message(_("Top"))
			if allIndex == currIndex:
				# Translators: the word  Bottom for reaching the Bottom of the list in your language (only the word Bottom).
				ui.message(_("Bottom"))
			# Translators: the phrase "{number} of {total}" in an index like 1 of 32 in your language.
			indexString=_("{number} of {total}").format( number = currIndex, total = allIndex)
			speakList=[]
			if controlTypes.STATE_SELECTED in self.states:
				speakList.append(controlTypes.stateLabels[controlTypes.STATE_SELECTED])
			speakList.append(self.name.split("\\")[-1])
			speakList.append(indexString)
			speech.speakMessage(" ".join(speakList))
		else:
			super(TCList,self).reportFocus()
