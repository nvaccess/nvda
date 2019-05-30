# NVDAObjects/UIA/winConsoleUIA.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

import config
import ctypes
import NVDAHelper
import speech
import time
import textInfos
import UIAHandler

from scriptHandler import script
from winVersion import isAtLeastWin10
from . import UIATextInfo
from ..behaviors import Terminal


class consoleUIATextInfo(UIATextInfo):
	_expandCollapseBeforeReview = False
	_isCaret = False

	def __init__(self, obj, position, _rangeObj=None):
		super(consoleUIATextInfo, self).__init__(obj, position, _rangeObj)
		if position == textInfos.POSITION_CARET:
			self._isCaret = True
			if isAtLeastWin10(1903):
				# The UIA implementation in 1903 causes the caret to be
				# off-by-one, so move it one position to the right
				# to compensate.
				self._rangeObj.MoveEndpointByUnit(
					UIAHandler.TextPatternRangeEndpoint_Start,
					UIAHandler.NVDAUnitsToUIAUnits[textInfos.UNIT_CHARACTER],
					1
				)

	def move(self, unit, direction, endPoint=None):
		if not self._isCaret:
			# Insure we haven't gone beyond the visible text.
			# UIA adds thousands of blank lines to the end of the console.
			visiRanges = self.obj.UIATextPattern.GetVisibleRanges()
			lastVisiRange = visiRanges.GetElement(visiRanges.length - 1)
			if self._rangeObj.CompareEndPoints(UIAHandler.TextPatternRangeEndpoint_Start, lastVisiRange, UIAHandler.TextPatternRangeEndpoint_End) >= 0:
				return 0
		if unit == textInfos.UNIT_WORD and direction != 0:
			# UIA doesn't implement word movement, so we need to do it manually.
			offset = self._countCharsToEnd(reverse=True)
			index = 1 if direction > 0 else 0
			wordOffsets = self._getWordOffsets(offset)
			res = self.move(
				textInfos.UNIT_CHARACTER,
				wordOffsets[index],
				endPoint=endPoint
			)
			if res != 0:
				return direction
			else:
				return res
		return super(consoleUIATextInfo, self).move(unit, direction, endPoint)

	def _countCharsToEnd(self, reverse=False):
		direction = -1 if reverse else 1
		lineInfo = self.copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		charInfo = self.copy()
		res = 0
		chars = None
		compareCondition = True
		while True:
			charInfo.expand(textInfos.UNIT_CHARACTER)
			if reverse:
				compareCondition = charInfo.compareEndPoints(
					lineInfo,
					"startToStart"
				) >= 0
			else:
				compareCondition = charInfo.compareEndPoints(
					lineInfo,
					"endToEnd"
				) < 0
			chars = charInfo.move(textInfos.UNIT_CHARACTER, direction)
			if reverse:
				chars *= -1
			if chars != 0 and compareCondition:
				res += chars
			else:
				break
		# Subtract 1 from res since UIA seems to wrap around
		res -= 1
		return res

	def _getWordOffsets(self, offset):
		lineInfo = self.copy()
		lineInfo.expand(textInfos.UNIT_LINE)
		lineText = lineInfo.text
		# Convert NULL and non-breaking space to space to make sure
		# that words will break on them
		lineText = lineText.translate({0: u' ', 0xa0: u' '})
		start = ctypes.c_int()
		end = ctypes.c_int()
		# Uniscribe does some strange things when you give it a string  with
		# not more than two alphanumeric chars in a row.
		# Inject two alphanumeric characters at the end to fix this.
		lineText += "xx"
		NVDAHelper.localLib.calculateWordOffsets(
			lineText,
			len(lineText),
			offset,
			ctypes.byref(start),
			ctypes.byref(end)
		)
		return (
			(offset - start.value) * -1,
			min(end.value, len(lineText)) - offset
		)


class winConsoleUIA(Terminal):
	STABILIZE_DELAY = 0.03
	_TextInfo = consoleUIATextInfo
	_isTyping = False
	_lastCharTime = 0
	_queuedChars = []
	_TYPING_TIMEOUT = 1

	def _reportNewText(self, line):
		# Additional typed character filtering beyond that in LiveText
		if self._isTyping and time.time() - self._lastCharTime <= self._TYPING_TIMEOUT:
			return
		super(winConsoleUIA, self)._reportNewText(line)

	def event_typedCharacter(self, ch):
		if not ch.isspace():
			self._isTyping = True
		if ch in ('\r', '\t'):
			# Clear the typed word buffer for tab and return.
			# This will need to be changed once #8110 is merged.
			speech.curWordChars = []
		self._lastCharTime = time.time()
		if (
			(
				config.conf['keyboard']['speakTypedCharacters']
				or config.conf['keyboard']['speakTypedWords']
			)
			and not config.conf['UIA']['winConsoleSpeakPasswords']
		):
			self._queuedChars.append(ch)
		else:
			super(winConsoleUIA, self).event_typedCharacter(ch)

	def event_textChange(self):
		while self._queuedChars:
			ch = self._queuedChars.pop(0)
			super(winConsoleUIA, self).event_typedCharacter(ch)
		super(winConsoleUIA, self).event_textChange()

	@script(gestures=[
		"kb:enter",
		"kb:numpadEnter",
		"kb:tab",
		"kb:control+c",
		"kb:control+d",
		"kb:control+pause"
	])
	def script_clear_isTyping(self, gesture):
		gesture.send()
		self._isTyping = False
		self._queuedChars = []

	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		ptr = self.UIATextPattern.GetVisibleRanges()
		res = [ptr.GetElement(i).GetText(-1) for i in range(ptr.length)]
		return res
