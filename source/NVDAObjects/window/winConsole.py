#NVDAObjects/WinConsole.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from keyUtils import sendKey, key
import winConsoleHandler
from . import Window
import controlTypes

class WinConsole(Window):

	def _get_TextInfo(self):
		if self.windowHandle == winConsoleHandler.consoleObject.windowHandle:
			return winConsoleHandler.WinConsoleTextInfo
		return super(WinConsole,self).TextInfo

	def _get_role(self):
		return controlTypes.ROLE_TERMINAL

	def event_gainFocus(self):
		winConsoleHandler.connectConsole(self)
		super(WinConsole, self).event_gainFocus()

	def event_loseFocus(self):
		winConsoleHandler.disconnectConsole()

	def event_nameChange(self):
		pass

[WinConsole.bindKey(keyName,scriptName) for keyName,scriptName in [
	("ExtendedUp","moveByLine"),
	("ExtendedDown","moveByLine"),
	("ExtendedLeft","moveByCharacter"),
	("ExtendedRight","moveByCharacter"),
	("Control+ExtendedLeft","moveByWord"),
	("Control+ExtendedRight","moveByWord"),
	("Shift+ExtendedRight","changeSelection"),
	("Shift+ExtendedLeft","changeSelection"),
	("Shift+ExtendedHome","changeSelection"),
	("Shift+ExtendedEnd","changeSelection"),
	("Shift+ExtendedUp","changeSelection"),
	("Shift+ExtendedDown","changeSelection"),
	("Control+Shift+ExtendedLeft","changeSelection"),
	("Control+Shift+ExtendedRight","changeSelection"),
	("ExtendedHome","moveByCharacter"),
	("ExtendedEnd","moveByCharacter"),
	("control+extendedHome","moveByLine"),
	("control+extendedEnd","moveByLine"),
	("control+shift+extendedHome","changeSelection"),
	("control+shift+extendedEnd","changeSelection"),
	("ExtendedDelete","delete"),
	("Back","backspace"),
]]
