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
from winVersion import isWin10
from . import UIATextInfo
from ..behaviors import Terminal
from ..window import Window


class consoleUIATextInfo(UIATextInfo):
	#: At least on Windows 10 1903, expanding then collapsing the text info
	#: caused review to get stuck, so disable it.
	#: There may be no need to disable this anymore, but doing so doesn't seem
	#: to do much good either.
	_expandCollapseBeforeReview = False

	def collapse(self,end=False):
		"""Works around a UIA bug on Windows 10 1903 and later."""
		if not isWin10(1903):
			return super(consoleUIATextInfo, self).collapse(end=end)
		# When collapsing, consoles seem to incorrectly push the start of the
		# textRange back one character.
		# Correct this by bringing the start back up to where the end is.
		oldInfo=self.copy()
		super(consoleUIATextInfo,self).collapse(end=end)
		if not end:
			self._rangeObj.MoveEndpointByRange(
				UIAHandler.TextPatternRangeEndpoint_Start,
				oldInfo._rangeObj,
				UIAHandler.TextPatternRangeEndpoint_Start
			)

	def move(self, unit, direction, endPoint=None):
		oldRange = None
		if self.basePosition != textInfos.POSITION_CARET:
			# Insure we haven't gone beyond the visible text.
			# UIA adds thousands of blank lines to the end of the console.
			visiRanges = self.obj.UIATextPattern.GetVisibleRanges()
			visiLength = visiRanges.length
			if visiLength > 0:
				firstVisiRange = visiRanges.GetElement(0)
				lastVisiRange = visiRanges.GetElement(visiLength - 1)
				oldRange = self._rangeObj.clone()
		if unit == textInfos.UNIT_WORD and direction != 0:
			# UIA doesn't implement word movement, so we need to do it manually.
			# Relative to the current line, calculate our offset
			# and the current word's offsets.
			lineInfo = self.copy()
			lineInfo.expand(textInfos.UNIT_LINE)
			offset = self._getCurrentOffsetInThisLine(lineInfo)
			start, end = self._getWordOffsetsInThisLine(offset, lineInfo)
			if direction > 0:
				# Moving in a forward direction, we can just jump to the
				# end offset of the current word and we're done.
				res = self.move(
					textInfos.UNIT_CHARACTER,
					end - offset,
					endPoint=endPoint
				)
			else:
				# Moving backwards
				wordStartDistance = (offset - start) * -1
				if wordStartDistance < 0:
					# We are after the beginning of a word.
					# So first move back to the start of the word.
					self.move(
						textInfos.UNIT_CHARACTER,
						wordStartDistance,
						endPoint=endPoint
					)
					offset += wordStartDistance
				# Try to move one character back before the start of the word.
				res = self.move(textInfos.UNIT_CHARACTER, -1, endPoint=endPoint)
				if res == 0:
					return 0
				offset -= 1
				# We are now positioned  within the previous word.
				if offset < 0:
					# We've moved on to the previous line.
					# Recalculate the current offset based on the new line we are now on.
					lineInfo = self.copy()
					lineInfo.expand(textInfos.UNIT_LINE)
					offset = self._getCurrentOffsetInThisLine(lineInfo)
				# Finally using the new offset,

				# Calculate the current word offsets and move to the start of
				# this word if we are not already there.
				start, end = self._getWordOffsetsInThisLine(offset, lineInfo)
				wordStartDistance = (offset - start) * -1
				if wordStartDistance < 0:
					self.move(
						textInfos.UNIT_CHARACTER,
						wordStartDistance,
						endPoint=endPoint
					)
		else:  # moving by a unit other than word
			res = super(consoleUIATextInfo, self).move(unit, direction,
														endPoint)
		if oldRange and (
			self._rangeObj.CompareEndPoints(
				UIAHandler.TextPatternRangeEndpoint_Start, firstVisiRange,
				UIAHandler.TextPatternRangeEndpoint_Start) < 0
			or self._rangeObj.CompareEndPoints(
				UIAHandler.TextPatternRangeEndpoint_Start, lastVisiRange,
				UIAHandler.TextPatternRangeEndpoint_End) >= 0):
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

	def _get_isCollapsed(self):
		"""Works around a UIA bug on Windows 10 1903 and later."""
		if not isWin10(1903):
			return super(consoleUIATextInfo, self)._get_isCollapsed()
		# Even when a console textRange's start and end have been moved to the
		# same position, the console incorrectly reports the end as being
		# past the start.
		# Therefore to decide if the textRange is collapsed,
		# Check if it has no text.
		return not bool(self._rangeObj.getText(1))

	def _getCurrentOffsetInThisLine(self, lineInfo):
		"""
		Given a caret textInfo expanded to line, returns the index into the
		line where the caret is located.
		This is necessary since Uniscribe requires indices into the text to
		find word boundaries, but UIA only allows for relative movement.
		"""
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
		lineText = lineInfo.text or u" "
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
			min(end.value, max(1, len(lineText) - 2))
		)

	def __ne__(self,other):
		"""Support more accurate caret move detection."""
		return not self==other


class consoleUIAWindow(Window):
	def _get_focusRedirect(self):
		"""
		Sometimes, attempting to interact with the console too quickly after
		focusing the window can make NVDA unable to get any caret or review
		information or receive new text events.
		To work around this, we must redirect focus to the console text area.
		"""
		for child in self.children:
			if isinstance(child, WinConsoleUIA):
				return child
		return None


class WinConsoleUIA(Terminal):
	#: Disable the name as it won't be localized
	name = ""
	#: Only process text changes every 30 ms, in case the console is getting
	#: a lot of text.
	STABILIZE_DELAY = 0.03
	_TextInfo = consoleUIATextInfo
	#: A queue of typed characters, to be dispatched on C{textChange}.
	#: This queue allows NVDA to suppress typed passwords when needed.
	_queuedChars = []
	#: Whether the console got new text lines in its last update.
	#: Used to determine if typed character/word buffers should be flushed.
	_hasNewLines = False
	#: the caret in consoles can take a while to move on Windows 10 1903 and later.
	_caretMovementTimeoutMultiplier = 1.5

	def _reportNewText(self, line):
		# Additional typed character filtering beyond that in LiveText
		if len(line.strip()) < max(len(speech.curWordChars) + 1, 3):
			return
		if self._hasNewLines:
			# Clear the queued characters buffer for new text lines.
			self._queuedChars = []
		super(WinConsoleUIA, self)._reportNewText(line)

	def event_typedCharacter(self, ch):
		if ch == '\t':
			# Clear the typed word buffer for tab completion.
			speech.clearTypedWordBuffer()
		if (
			(
				config.conf['keyboard']['speakTypedCharacters']
				or config.conf['keyboard']['speakTypedWords']
			)
			and not config.conf['UIA']['winConsoleSpeakPasswords']
		):
			self._queuedChars.append(ch)
		else:
			super(WinConsoleUIA, self).event_typedCharacter(ch)

	def event_textChange(self):
		while self._queuedChars:
			ch = self._queuedChars.pop(0)
			super(WinConsoleUIA, self).event_typedCharacter(ch)
		super(WinConsoleUIA, self).event_textChange()

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
		Flushes the typed word buffer and queue of typedCharacter events if present.
		Since these gestures clear the current word/line, we should flush the
		queue to avoid erroneously reporting these chars.
		"""
		gesture.send()
		self._queuedChars = []
		speech.clearTypedWordBuffer()

	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		ptr = self.UIATextPattern.GetVisibleRanges()
		res = [ptr.GetElement(i).GetText(-1) for i in range(ptr.length)]
		return res

	def _calculateNewText(self, newLines, oldLines):
		self._hasNewLines = (
			self._findNonBlankIndices(newLines)
			!= self._findNonBlankIndices(oldLines)
		)
		return super(WinConsoleUIA, self)._calculateNewText(newLines, oldLines)

	def _findNonBlankIndices(self, lines):
		"""
		Given a list of strings, returns a list of indices where the strings
		are not empty.
		"""
		return [index for index, line in enumerate(lines) if line]

def findExtraOverlayClasses(obj, clsList):
	if obj.UIAElement.cachedAutomationId == "Text Area":
		clsList.append(WinConsoleUIA)
	elif obj.UIAElement.cachedAutomationId == "Console Window":
		clsList.append(consoleUIAWindow)
