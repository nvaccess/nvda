#NVDAObjects/IAccessible/winConsoleLegacy.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2019 NV Access Limited, Bill Dengler

import winConsoleHandlerLegacy as winConsoleHandler
from . import IAccessible
from ..behaviors import Terminal, EditableTextWithoutAutoSelectDetection
import api
import core

class winConsoleLegacy(Terminal, EditableTextWithoutAutoSelectDetection, IAccessible):
	STABILIZE_DELAY = 0.03

	def _get_TextInfo(self):
		consoleObject=winConsoleHandler.consoleObject
		if consoleObject and self.windowHandle == consoleObject.windowHandle:
			return winConsoleHandler.legacyConsoleTextInfo
		return super(winConsoleLegacy,self).TextInfo

	def event_becomeNavigatorObject(self, isFocus=False):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
			if self == api.getFocusObject():
				# The user is returning to the focus object with object navigation.
				# The focused console should always be monitored if possible.
				self.startMonitoring()
		super(winConsoleLegacy,self).event_becomeNavigatorObject(isFocus=isFocus)

	def event_gainFocus(self):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
		super(winConsoleLegacy, self).event_gainFocus()

	def event_loseFocus(self):
		super(winConsoleLegacy, self).event_loseFocus()
		if winConsoleHandler.consoleObject is self:
			winConsoleHandler.disconnectConsole()

	def event_nameChange(self):
		pass

	def _getTextLines(self):
		return winConsoleHandler.getConsoleVisibleLines()

	def script_caret_backspaceCharacter(self, gesture):
		super(winConsoleLegacy, self).script_caret_backspaceCharacter(gesture)
		# #2586: We use console update events for typed characters,
		# so the typedCharacter event is never fired for the backspace key.
		# Call it here so that speak typed words works as expected.
		self.event_typedCharacter(u"\b")

	def script_close(self,gesture):
		# #5343: New consoles in Windows 10 close with alt+f4 and take any processes attached with it (including NVDA).
		# Therefore detach from the console temporarily while sending the gesture. 
		winConsoleHandler.disconnectConsole()
		gesture.send()
		def reconnect():
			if api.getFocusObject()==self:
				winConsoleHandler.connectConsole(self)
				self.startMonitoring()
		core.callLater(200,reconnect)

	__gestures={
		"kb:alt+f4":"close",
	}
