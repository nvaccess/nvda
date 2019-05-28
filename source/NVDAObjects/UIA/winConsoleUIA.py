# NVDAObjects/UIA/winConsoleUIA.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

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
		if position == textInfos.POSITION_CARET:
			if isAtLeastWin10(1903):
				# The UIA implementation in 1903 causes the caret to be
				# off-by-one, so move it one position to the right
				# to compensate.
				self._rangeObj.MoveEndpointByUnit(
					UIAHandler.TextPatternRangeEndpoint_Start,
					UIAHandler.NVDAUnitsToUIAUnits[textInfos.UNIT_CHARACTER],
					1
				)

	def move(self,unit,direction,endPoint=None):
		# Insure we haven't gone beyond the visible text.
		# UIA adds thousands of blank lines to the end of the console.
		visiRanges = self.obj.UIATextPattern.GetVisibleRanges()
		lastVisiRange = visiRanges.GetElement(visiRanges.length - 1)
		if self._rangeObj.CompareEndPoints(UIAHandler.TextPatternRangeEndpoint_Start, lastVisiRange, UIAHandler.TextPatternRangeEndpoint_End) >= 0:
			return 0
		super(consoleUIATextInfo, self).move(unit, direction, endPoint)

class winConsoleUIA(Terminal):
	STABILIZE_DELAY = 0.03
	_TextInfo = consoleUIATextInfo
	_isTyping = False
	_lastCharTime = 0
	_TYPING_TIMEOUT = 1

	def _reportNewText(self, line):
		# Additional typed character filtering beyond that in LiveText
		if self._isTyping and time.time() - self._lastCharTime <= self._TYPING_TIMEOUT:
			return
		super(winConsoleUIA, self)._reportNewText(line)

	def event_typedCharacter(self, ch):
		if not ch.isspace():
			self._isTyping = True
		self._lastCharTime = time.time()
		super(winConsoleUIA, self).event_typedCharacter(ch)

	@script(gestures=["kb:enter", "kb:numpadEnter", "kb:tab"])
	def script_clear_isTyping(self, gesture):
		gesture.send()
		self._isTyping = False

	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		ptr = self.UIATextPattern.GetVisibleRanges()
		res = [ptr.GetElement(i).GetText(-1) for i in range(ptr.length)]
		return res
