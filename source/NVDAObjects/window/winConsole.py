#NVDAObjects/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2007-2012 NV Access Limited

import winConsoleHandler
from . import Window
from ..behaviors import Terminal, EditableTextWithoutAutoSelectDetection
import api

class WinConsole(Terminal, EditableTextWithoutAutoSelectDetection, Window):
	STABILIZE_DELAY = 0.03

	def _get_TextInfo(self):
		consoleObject=winConsoleHandler.consoleObject
		if consoleObject and self.windowHandle == consoleObject.windowHandle:
			return winConsoleHandler.WinConsoleTextInfo
		return super(WinConsole,self).TextInfo

	def event_becomeNavigatorObject(self):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
			if self == api.getFocusObject():
				# The user is returning to the focus object with object navigation.
				# The focused console should always be monitored if possible.
				self.startMonitoring()
		super(WinConsole,self).event_becomeNavigatorObject()

	def event_gainFocus(self):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
		super(WinConsole, self).event_gainFocus()

	def event_loseFocus(self):
		super(WinConsole, self).event_loseFocus()
		if winConsoleHandler.consoleObject is self:
			winConsoleHandler.disconnectConsole()

	def event_nameChange(self):
		pass

	def _getTextLines(self):
		return winConsoleHandler.getConsoleVisibleLines()

	def script_caret_backspaceCharacter(self, gesture):
		super(WinConsole, self).script_caret_backspaceCharacter(gesture)
		# #2586: We use console update events for typed characters,
		# so the typedCharacter event is never fired for the backspace key.
		# Call it here so that speak typed words works as expected.
		self.event_typedCharacter(u"\b")
