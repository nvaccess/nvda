# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2007-2020 NV Access Limited, Bill Dengler

import winConsoleHandler
from . import Window
from ..behaviors import Terminal, EditableTextWithoutAutoSelectDetection, KeyboardHandlerBasedTypedCharSupport
import api
import core
from scriptHandler import script
import speech
from diffHandler import prefer_difflib

class WinConsole(Terminal, EditableTextWithoutAutoSelectDetection, Window):
	"""
		Base class for NVDA's legacy Windows Console support.
		This is used in situations where UIA isn't available.
		Please consider using NVDAObjects.UIA.winConsoleUIA instead.
	"""
	STABILIZE_DELAY = 0.03

	def _get_windowThreadID(self):
		# #10113: Windows forces the thread of console windows to match the thread of the first attached process.
		# However, To correctly handle speaking of typed characters,
		# NVDA really requires the real thread the window was created in,
		# I.e. a thread inside conhost.
		from IAccessibleHandler.internalWinEventHandler import consoleWindowsToThreadIDs
		threadID = consoleWindowsToThreadIDs.get(self.windowHandle, 0)
		if not threadID:
			threadID = super().windowThreadID
		return threadID

	def _get_TextInfo(self):
		consoleObject=winConsoleHandler.consoleObject
		if consoleObject and self.windowHandle == consoleObject.windowHandle:
			return winConsoleHandler.WinConsoleTextInfo
		return super(WinConsole,self).TextInfo

	def _get_diffAlgo(self):
		# #12974: Legacy consoles contain only one screen of text at a time.
		# Use Difflib to reduce choppiness in reading.
		return prefer_difflib()

	def event_becomeNavigatorObject(self, isFocus=False):
		if winConsoleHandler.consoleObject is not self:
			if winConsoleHandler.consoleObject:
				winConsoleHandler.disconnectConsole()
			winConsoleHandler.connectConsole(self)
			if self == api.getFocusObject():
				# The user is returning to the focus object with object navigation.
				# The focused console should always be monitored if possible.
				self.startMonitoring()
		super(WinConsole,self).event_becomeNavigatorObject(isFocus=isFocus)

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

	def _getText(self):
		return '\n'.join(winConsoleHandler.getConsoleVisibleLines())

	def script_caret_backspaceCharacter(self, gesture):
		super(WinConsole, self).script_caret_backspaceCharacter(gesture)
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

	@script(gestures=[
		"kb:enter",
		"kb:numpadEnter",
		"kb:tab",
		"kb:control+c",
		"kb:control+d",
		"kb:control+pause"
	])
	def script_flush_queuedChars(self, gesture):
		"""
		Flushes the typed word buffer if present.
		Since these gestures clear the current word/line, we should flush the
		current words buffer to avoid erroneously reporting words that already have been processed.
		"""
		gesture.send()
		speech.clearTypedWordBuffer()

	__gestures={
		"kb:alt+f4":"close",
	}
