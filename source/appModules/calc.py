#appModules/calc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2012 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""App module for Windows Calculator (desktop version)
"""

import appModuleHandler
import NVDAObjects.IAccessible
import speech

class AppModule(appModuleHandler.AppModule):

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		windowClassName=obj.windowClassName
		windowControlID=obj.windowControlID
		if ((windowClassName=="Edit" and windowControlID==403)
			or (windowClassName=="Static" and windowControlID==150)
		):
			clsList.insert(0, Display)

class Display(NVDAObjects.IAccessible.IAccessible):

	shouldAllowIAccessibleFocusEvent=True

	calcCommandChars=['!','=','@','#']

	calcCommandGestures=(
		"kb:backspace","kb:escape","kb:enter","kb:numpadEnter",
		"kb:f2","kb:f3","kb:f4","kb:f5","kb:f6","kb:f7","kb:f8","kb:f9",
		"kb:l","kb:n","kb:o","kb:p","kb:r","kb:s","kb:t",
	)

	def _get_name(self):
		name=super(Display,self).name
		if not name:
			name=_("Display")
		return name

	def event_typedCharacter(self,ch):
		super(Display,self).event_typedCharacter(ch)
		if ch in self.calcCommandChars:
			speech.speakObjectProperties(self,value=True)

	def script_executeAndRead(self,gesture):
		gesture.send()
		speech.speakObjectProperties(self,value=True)

	def initOverlayClass(self):
		for g in Display.calcCommandGestures:
			self.bindGesture(g,"executeAndRead")
