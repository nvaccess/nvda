# NVDAObjects/UIA/ConsoleUIA.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

import time
import textInfos
import UIAHandler

from scriptHandler import script
from winVersion import winVersion
from . import UIATextInfo
from ..behaviors import Terminal


class consoleUIATextInfo(UIATextInfo):
	def __init__(self, obj, position, _rangeObj=None):
		super(consoleUIATextInfo, self).__init__(obj, position, _rangeObj)
		if position == textInfos.POSITION_CARET:
			if winVersion.build >= 18362:  # Windows 10 version 1903
				# The UIA implementation in 1903 causes the caret to be
				# off-by-one, so move it one position to the right
				# to compensate.
				self._rangeObj.MoveEndpointByUnit(
					UIAHandler.TextPatternRangeEndpoint_Start,
					UIAHandler.NVDAUnitsToUIAUnits['character'],
					1
				)


class consoleUIA(Terminal):
	_TextInfo = consoleUIATextInfo
	_isTyping=False
	_lastCharTime = 0
	_TYPING_TIMEOUT = 1

	def _reportNewText(self, line):
		# Additional typed character filtering beyond that in LiveText
		if self._isTyping and time.time()-self._lastCharTime <= self._TYPING_TIMEOUT:
			return
		super(consoleUIA, self)._reportNewText(line)

	def event_textChanged(self):
		# fire textChange for liveText
		self.event_textChange()

	def event_typedCharacter(self, ch):
		if len(''.join(ch.split())) > 0:
			self._isTyping = True
		self._lastCharTime = time.time()
		super(consoleUIA, self).event_typedCharacter(ch)

	@script(gestures=["kb:enter", "kb:numpadEnter"])
	def script_clear_isTyping(self, gesture):
		gesture.send()
		self._isTyping = False

	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		# Todo: do this (also) somewhere else so they aren't in document review either
		return self.makeTextInfo(textInfos.POSITION_ALL).text.strip().split("\r\n")
