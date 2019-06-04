# NVDAObjects/UIA/winConsoleUIA.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

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

	def __init__(self, obj, position, _rangeObj=None):
		super(consoleUIATextInfo, self).__init__(obj, position, _rangeObj)
		if position == textInfos.POSITION_CARET and isAtLeastWin10(1903):
			# The UIA implementation in 1903 causes the caret to be
			# off-by-one, so move it one position to the right
			# to compensate.
			self._rangeObj.MoveEndpointByUnit(
				UIAHandler.TextPatternRangeEndpoint_Start,
				UIAHandler.NVDAUnitsToUIAUnits[textInfos.UNIT_CHARACTER],
				1
			)

	def move(self, unit, direction, endPoint=None):
		oldRange=None
		if self.basePosition != textInfos.POSITION_CARET:
			# Insure we haven't gone beyond the visible text.
			# UIA adds thousands of blank lines to the end of the console.
			visiRanges = self.obj.UIATextPattern.GetVisibleRanges()
			visiLength = visiRanges.length
			if visiLength > 0:
				firstVisiRange = visiRanges.GetElement(0)
				lastVisiRange = visiRanges.GetElement(visiLength - 1)
				oldRange=self._rangeObj.clone()
		if unit == textInfos.UNIT_WORD and direction != 0:
			# UIA doesn't implement word movement, so we need to do it manually.
			lineInfo = self.copy()
			lineInfo.expand(textInfos.UNIT_LINE)
			offset = self._getCurrentOffsetInThisLine(lineInfo)
			index = 1 if direction > 0 else 0
			start, end = self._getWordOffsetsInThisLine(offset, lineInfo)
			wordMoveDirections = (
				(offset - start) * -1,
				end - offset
			)
			res = self.move(
				textInfos.UNIT_CHARACTER,
				wordMoveDirections[index],
				endPoint=endPoint
			)
			if res != 0:
				return direction
			else:
				if self.move(textInfos.UNIT_CHARACTER, -1): # Reset word boundaries to move to the previous word
					return self.move(unit, direction, endPoint=endPoint)
				else:
					return res
		res = super(consoleUIATextInfo, self).move(unit, direction, endPoint)
		if oldRange and (
			self._rangeObj.CompareEndPoints(
				UIAHandler.TextPatternRangeEndpoint_Start,
				firstVisiRange,
				UIAHandler.TextPatternRangeEndpoint_Start
			) < 0
			or self._rangeObj.CompareEndPoints(
				UIAHandler.TextPatternRangeEndpoint_Start,
				lastVisiRange,
				UIAHandler.TextPatternRangeEndpoint_End
			) >= 0
		):
			self._rangeObj = oldRange
			return 0
		return res

	def expand(self, unit):
		if unit == textInfos.UNIT_WORD:
			# UIA doesn't implement word movement, so we need to do it manually.
			lineInfo = self.copy()
			lineInfo.expand(textInfos.UNIT_LINE)
			offset = self._getCurrentOffsetInThisLine(lineInfo)
			start, end = self._getWordOffsetsInThisLine(offset, lineInfo)
			wordEndPoints = (
				(offset - start) * -1,
				end - offset - 1
			)
			if wordEndPoints[0]:
				self._rangeObj.MoveEndpointByUnit(
					UIAHandler.TextPatternRangeEndpoint_Start,
					UIAHandler.NVDAUnitsToUIAUnits[textInfos.UNIT_CHARACTER],
					wordEndPoints[0]
				)
			if wordEndPoints[1]:
				self._rangeObj.MoveEndpointByUnit(
					UIAHandler.TextPatternRangeEndpoint_End,
					UIAHandler.NVDAUnitsToUIAUnits[textInfos.UNIT_CHARACTER],
					wordEndPoints[1]
				)
		else:
			return super(consoleUIATextInfo, self).expand(unit)

	def _getCurrentOffsetInThisLine(self, lineInfo):
		charInfo = self.copy()
		res = 0
		chars = None
		while charInfo.compareEndPoints(
			lineInfo,
			"startToEnd"
		) <= 0:
			charInfo.expand(textInfos.UNIT_CHARACTER)
			chars = charInfo.move(textInfos.UNIT_CHARACTER, -1) * -1
			if chars != 0 and charInfo.compareEndPoints(
				lineInfo,
				"startToStart"
			) >= 0:
				res += chars
			else:
				break
		return res

	def _getWordOffsetsInThisLine(self, offset, lineInfo):
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
			start.value,
			min(end.value, len(lineText) - 2)
		)


class winConsoleUIA(Terminal):
	STABILIZE_DELAY = 0.03
	_TextInfo = consoleUIATextInfo
	_isTyping = False
	_lastCharTime = 0
	_TYPING_TIMEOUT = 1

	def _reportNewText(self, line):
		# Additional typed character filtering beyond that in LiveText
		if (
			self._isTyping
			and time.time() - self._lastCharTime <= self._TYPING_TIMEOUT
		):
			return
		super(winConsoleUIA, self)._reportNewText(line)

	def event_typedCharacter(self, ch):
		if not ch.isspace():
			self._isTyping = True
		if ch in ('\n', '\r', '\t'):
			# Clear the typed word buffer for tab and return.
			# This will need to be changed once #8110 is merged.
			speech.curWordChars = []
		self._lastCharTime = time.time()
		super(winConsoleUIA, self).event_typedCharacter(ch)

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

	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		ptr = self.UIATextPattern.GetVisibleRanges()
		res = [ptr.GetElement(i).GetText(-1) for i in range(ptr.length)]
		return res
