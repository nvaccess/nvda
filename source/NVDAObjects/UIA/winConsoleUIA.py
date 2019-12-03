# NVDAObjects/UIA/winConsoleUIA.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019 Bill Dengler

import ctypes
import NVDAHelper
import textInfos
import textUtils
import UIAHandler

from comtypes import COMError
from UIAUtils import isTextRangeOffscreen
from . import UIATextInfo
from ..behaviors import KeyboardHandlerBasedTypedCharSupport
from ..window import Window


class consoleUIATextInfo(UIATextInfo):
	#: At least on Windows 10 1903, expanding then collapsing the text info
	#: caused review to get stuck, so disable it.
	#: There may be no need to disable this anymore, but doing so doesn't seem
	#: to do much good either.
	_expandCollapseBeforeReview = False

	def __init__(self, obj, position, _rangeObj=None):
		super(consoleUIATextInfo, self).__init__(obj, position, _rangeObj)
		# Re-implement POSITION_FIRST and POSITION_LAST in terms of
		# visible ranges to fix review top/bottom scripts.
		if position == textInfos.POSITION_FIRST:
			visiRanges = self.obj.UIATextPattern.GetVisibleRanges()
			firstVisiRange = visiRanges.GetElement(0)
			self._rangeObj = firstVisiRange
			self.collapse()
		elif position == textInfos.POSITION_LAST:
			visiRanges = self.obj.UIATextPattern.GetVisibleRanges()
			lastVisiRange = visiRanges.GetElement(visiRanges.length - 1)
			self._rangeObj = lastVisiRange
			self.collapse(True)

	def collapse(self, end=False):
		"""Works around a UIA bug on Windows 10 1803 and later."""
		# When collapsing, consoles seem to incorrectly push the start of the
		# textRange back one character.
		# Correct this by bringing the start back up to where the end is.
		oldInfo = self.copy()
		super(consoleUIATextInfo, self).collapse(end=end)
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
		try:
			if (
				oldRange
				and isTextRangeOffscreen(self._rangeObj, visiRanges)
				and not isTextRangeOffscreen(oldRange, visiRanges)
			):
				self._rangeObj = oldRange
				return 0
		except (COMError, RuntimeError):
			pass
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

	def compareEndPoints(self, other, which):
		"""Works around a UIA bug on Windows 10 1803 and later."""
		# Even when a console textRange's start and end have been moved to the
		# same position, the console incorrectly reports the end as being
		# past the start.
		# Compare to the start (not the end) when collapsed.
		selfEndPoint, otherEndPoint = which.split("To")
		if selfEndPoint == "end" and self._isCollapsed():
			selfEndPoint = "start"
		if otherEndPoint == "End" and other._isCollapsed():
			otherEndPoint = "Start"
		which = f"{selfEndPoint}To{otherEndPoint}"
		return super().compareEndPoints(other, which=which)

	def setEndPoint(self, other, which):
		"""Override of L{textInfos.TextInfo.setEndPoint}.
		Works around a UIA bug on Windows 10 1803 and later that means we can
		not trust the "end" endpoint of a collapsed (empty) text range
		for comparisons.
		"""
		selfEndPoint, otherEndPoint = which.split("To")
		# In this case, there is no need to check if self is collapsed
		# since the point of this method is to change its text range, modifying the "end" endpoint of a collapsed
		# text range is fine.
		if otherEndPoint == "End" and other._isCollapsed():
			otherEndPoint = "Start"
		which = f"{selfEndPoint}To{otherEndPoint}"
		return super().setEndPoint(other, which=which)

	def _isCollapsed(self):
		"""Works around a UIA bug on Windows 10 1803 and later that means we
		cannot trust the "end" endpoint of a collapsed (empty) text range
		for comparisons.
		Instead we check to see if we can get the first character from the
		text range. A collapsed range will not have any characters
		and will return an empty string."""
		return not bool(self._rangeObj.getText(1))

	def _get_isCollapsed(self):
		# To decide if the textRange is collapsed,
		# Check if it has no text.
		return self._isCollapsed()

	def _getCurrentOffsetInThisLine(self, lineInfo):
		"""
		Given a caret textInfo expanded to line, returns the index into the
		line where the caret is located.
		This is necessary since Uniscribe requires indices into the text to
		find word boundaries, but UIA only allows for relative movement.
		"""
		# position a textInfo from the start of the line up to the current position.
		charInfo = lineInfo.copy()
		charInfo.setEndPoint(self, "endToStart")
		text = charInfo.text
		offset = textUtils.WideStringOffsetConverter(text).wideStringLength
		return offset

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
		lineTextLen = textUtils.WideStringOffsetConverter(lineText).wideStringLength
		NVDAHelper.localLib.calculateWordOffsets(
			lineText,
			lineTextLen,
			offset,
			ctypes.byref(start),
			ctypes.byref(end)
		)
		return (
			start.value,
			min(end.value, max(1, lineTextLen - 2))
		)

	def __ne__(self, other):
		"""Support more accurate caret move detection."""
		return not self == other

	def _get_text(self):
		# #10036: return a space if the text range is empty.
		# Consoles don't actually store spaces, the character is merely left blank.
		res = super(consoleUIATextInfo, self)._get_text()
		if not res:
			return ' '
		else:
			return res


class consoleUIAWindow(Window):
	# This is the parent of the console text area, which sometimes gets focus after the text area.
	shouldAllowUIAFocusEvent = False


class WinConsoleUIA(KeyboardHandlerBasedTypedCharSupport):
	#: Disable the name as it won't be localized
	name = ""
	#: Only process text changes every 30 ms, in case the console is getting
	#: a lot of text.
	STABILIZE_DELAY = 0.03
	#: the caret in consoles can take a while to move on Windows 10 1903 and later.
	_caretMovementTimeoutMultiplier = 1.5

	def _get_windowThreadID(self):
		# #10113: Windows forces the thread of console windows to match the thread of the first attached process.
		# However, To correctly handle speaking of typed characters,
		# NVDA really requires the real thread the window was created in,
		# I.e. a thread inside conhost.
		from IAccessibleHandler import consoleWindowsToThreadIDs
		threadID = consoleWindowsToThreadIDs.get(self.windowHandle, 0)
		if not threadID:
			threadID = super().windowThreadID
		return threadID

	def _get_TextInfo(self):
		"""Overriding _get_TextInfo and thus the TextInfo property
		on NVDAObjects.UIA.UIA
		consoleUIATextInfo fixes expand/collapse, implements word movement, and
		bounds review to the visible text."""
		return consoleUIATextInfo

	def _getTextLines(self):
		# Filter out extraneous empty lines from UIA
		ptr = self.UIATextPattern.GetVisibleRanges()
		res = [ptr.GetElement(i).GetText(-1) for i in range(ptr.length)]
		return res


def findExtraOverlayClasses(obj, clsList):
	if obj.UIAElement.cachedAutomationId == "Text Area":
		clsList.append(WinConsoleUIA)
	elif obj.UIAElement.cachedAutomationId == "Console Window":
		clsList.append(consoleUIAWindow)
