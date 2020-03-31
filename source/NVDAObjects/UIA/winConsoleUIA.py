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

	def __init__(self, obj, position, _rangeObj=None):
		# We want to limit  textInfos to just the visible part of the console.
		# Therefore we specifically handle POSITION_FIRST, POSITION_LAST and POSITION_ALL.
		# We could use IUIAutomationTextRange::getVisibleRanges, but it seems very broken in consoles
		# once more than a few screens worth of content has been written to the console.
		# Therefore we resort to using IUIAutomationTextPattern::rangeFromPoint
		# for the top left, and bottom right of the console window.
		if position is textInfos.POSITION_FIRST:
			_rangeObj = self.__class__(obj, obj.location.topLeft)._rangeObj
		elif position is textInfos.POSITION_LAST:
			# Asking for the range at the bottom right of the window
			# Seems to sometimes ignore the x coordinate.
			# Therefore use the bottom left, then move   to the last character on that line.
			tempInfo = self.__class__(obj, obj.location.bottomLeft)
			tempInfo.expand(textInfos.UNIT_LINE)
			# We must pull back the end by one character otherwise when we collapse to end,
			# a console bug results in a textRange covering the entire console buffer!
			# Strangely the *very* last character is a special blank point
			# so we never seem to miss a real character.
			UIATextInfo.move(tempInfo, textInfos.UNIT_CHARACTER, -1, endPoint="end")
			tempInfo.setEndPoint(tempInfo, "startToEnd")
			_rangeObj = tempInfo._rangeObj
		elif position is textInfos.POSITION_ALL:
			first = self.__class__(obj, textInfos.POSITION_FIRST)
			last = self.__class__(obj, textInfos.POSITION_LAST)
			first.setEndPoint(last, "endToEnd")
			_rangeObj = first._rangeObj
		super(consoleUIATextInfo, self).__init__(obj, position, _rangeObj)

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
		oldInfo = None
		if self.basePosition != textInfos.POSITION_CARET:
			# Insure we haven't gone beyond the visible text.
			# UIA adds thousands of blank lines to the end of the console.
			boundingInfo = self.obj.makeTextInfo(textInfos.POSITION_ALL)
			oldInfo = self.copy()
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
		if not endPoint:
			# #10191: IUIAutomationTextRange::move in consoles does not correctly produce a collapsed range
			# after moving.
			# Therefore manually collapse.
			self.collapse()
		# Console textRanges have access to the entire console buffer.
		# However, we want to limit ourselves to onscreen text.
		# Therefore, if the textInfo was originally visible,
		# but we are now above or below the visible range,
		# Restore the original textRange and pretend the move didn't work.
		if oldInfo:
			try:
				if (
					(
						self.compareEndPoints(boundingInfo, "startToStart") < 0
						or self.compareEndPoints(boundingInfo, "startToEnd") >= 0
					)
					and not (
						oldInfo.compareEndPoints(boundingInfo, "startToStart") < 0
						or oldInfo.compareEndPoints(boundingInfo, "startToEnd") >= 0
					)
				):
					self._rangeObj = oldInfo._rangeObj
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
		text = charInfo._rangeObj.getText(-1)
		offset = textUtils.WideStringOffsetConverter(text).wideStringLength
		return offset

	def _getWordOffsetsInThisLine(self, offset, lineInfo):
		lineText = lineInfo._rangeObj.getText(-1)
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
		from IAccessibleHandler.internalWinEventHandler import consoleWindowsToThreadIDs
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
		# This override of _getTextLines takes advantage of the fact that
		# the console text contains linefeeds for every line
		# Thus a simple string splitlines is much faster than splitting by unit line.
		ti = self.makeTextInfo(textInfos.POSITION_ALL)
		text = ti.text or ""
		return text.splitlines()

def findExtraOverlayClasses(obj, clsList):
	if obj.UIAElement.cachedAutomationId == "Text Area":
		clsList.append(WinConsoleUIA)
	elif obj.UIAElement.cachedAutomationId == "Console Window":
		clsList.append(consoleUIAWindow)
