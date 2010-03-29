#NVDAObjects/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from keyUtils import sendKey, key
import winConsoleHandler
from . import Window
from ..behaviors import EditableTextWithoutAutoSelectDetection
import controlTypes

class WinConsole(EditableTextWithoutAutoSelectDetection, Window):

	def _get_TextInfo(self):
		consoleObject=winConsoleHandler.consoleObject
		if consoleObject and self.windowHandle == consoleObject.windowHandle:
			return winConsoleHandler.WinConsoleTextInfo
		return super(WinConsole,self).TextInfo

	def _get_role(self):
		return controlTypes.ROLE_TERMINAL

	def event_becomeNavigatorObject(self):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
		super(WinConsole,self).event_becomeNavigatorObject()

	def event_gainFocus(self):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
		super(WinConsole, self).event_gainFocus()

	def event_loseFocus(self):
		if winConsoleHandler.consoleObject is self:
			winConsoleHandler.disconnectConsole()

	def event_nameChange(self):
		pass
