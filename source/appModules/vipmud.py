#appModules/vipmud.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2011 Willem Venter and Rynhardt Kruger
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from NVDAObjects.window import edit
import ui
import appModuleHandler
import controlTypes

"""
App module for VIP Mud
This module makes NVDA read incoming text, as well as allowing the user to review the last nine messages with control 1 through 9.
"""

class AppModule(appModuleHandler.AppModule):
	lastLength=0
	msgs =[]
	historyLength =9
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if controlTypes.State.READONLY in obj.states:
			clsList.insert(0, MudText)
	def __init__(self, *args, **kwargs):
		super(AppModule, self).__init__(*args, **kwargs)
		for n in range(1, self.historyLength +1):
			self.bindGesture("kb:control+%s" % n, "readMessage")
	def script_readMessage(self,gesture):
		num=int(gesture.mainKeyName[-1])
		try:
			ui.message(self.msgs[num-1])
		except IndexError:
			ui.message(_("No message yet"))
	script_readMessage.__doc__=_("Displays one of the recent messages")


class MudText(edit.Edit):
	def event_valueChange(self):
		text=self.windowText
		nt =text[self.appModule.lastLength:]
		ui.message(nt)
		lines =nt.split("\n")
		for line in lines:
			line =line.strip()
			if not line:
				continue
			self.appModule.msgs.insert(0, line)
		del self.appModule.msgs[self.appModule.historyLength:]
		self.appModule.lastLength =len(text)
