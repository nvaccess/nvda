# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2022 Bill Dengler

import ctypes
import NVDAHelper
import textInfos
import textUtils
import UIAHandler

from comtypes import COMError
from diffHandler import prefer_difflib
from logHandler import log
from UIAHandler.utils import _getConhostAPILevel
from UIAHandler.constants import WinConsoleAPILevel
from . import UIATextInfo
from ..behaviors import EnhancedTermTypedCharSupport, KeyboardHandlerBasedTypedCharSupport
from ..window import Window


class ConsoleUIATextInfo(UIATextInfo):
	"A TextInfo implementation for consoles with an IMPROVED, but not FORMATTED, API level."
	def __init__(self, obj, position, _rangeObj=None):
		collapseToEnd = None
		# We want to limit  textInfos to just the visible part of the console.
		# Therefore we specifically handle POSITION_FIRST, POSITION_LAST and POSITION_ALL.
		if not _rangeObj and position in (
			textInfos.POSITION_FIRST,
			textInfos.POSITION_LAST,
			textInfos.POSITION_ALL
		):
			try:
				_rangeObj, collapseToEnd = self._getBoundingRange(obj, position)
			except (COMError, RuntimeError):
				# We couldn't bound the console.
				log.warning("Couldn't get bounding range for console", exc_info=True)
				# Fall back to presenting the entire buffer.
				_rangeObj, collapseToEnd = None, None
		super(ConsoleUIATextInfo, self).__init__(obj, position, _rangeObj)
		if collapseToEnd is not None:
			self.collapse(end=collapseToEnd)

	def _getBoundingRange(self, obj, position):
		"""Returns the UIA text range to which the console should be bounded,
		and whether the textInfo should be collapsed after instantiation."""
		# microsoft/terminal#4495: In newer consoles,
		# IUIAutomationTextRange::getVisibleRanges returns a reliable contiguous range.
		_rangeObj = obj.UIATextPattern.GetVisibleRanges().GetElement(0)
		collapseToEnd = None
		if position == textInfos.POSITION_FIRST:
			collapseToEnd = False
		elif position == textInfos.POSITION_LAST:
			# The exclusive end hangs off the end of the visible ranges.
			# Move back one character to remain within bounds.
			_rangeObj.MoveEndpointByUnit(
				UIAHandler.TextPatternRangeEndpoint_End,
				UIAHandler.NVDAUnitsToUIAUnits['character'],
				-1
			)
			collapseToEnd = True
		return (_rangeObj, collapseToEnd)

	def move(self, unit, direction, endPoint=None):
		oldInfo = None
		if self.basePosition != textInfos.POSITION_CARET:
			# Ensure we haven't gone beyond the visible text.
			# UIA adds thousands of blank lines to the end of the console.
			boundingInfo = self.obj.makeTextInfo(textInfos.POSITION_ALL)
			oldInfo = self.copy()
		res = self._move(unit, direction, endPoint)
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

	def _move(self, unit, direction, endPoint=None):
		"Perform a move without respect to bounding."
		return super(ConsoleUIATextInfo, self).move(unit, direction, endPoint)

	def __ne__(self, other):
		"""Support more accurate caret move detection."""
		return not self == other


class ConsoleUIATextInfoWorkaroundEndInclusive(ConsoleUIATextInfo):
	"""Implementation of various workarounds for pre-microsoft/terminal#4018
	conhost: fixes expand/collapse, uses rangeFromPoint instead of broken
	GetVisibleRanges for bounding, and implements word movement support."""
	def _getBoundingRange(self, obj, position):
		# We could use IUIAutomationTextRange::getVisibleRanges, but it seems very broken in consoles
		# once more than a few screens worth of content has been written to the console.
		# Therefore we resort to using IUIAutomationTextPattern::rangeFromPoint
		# for the top left, and bottom right of the console window.
		_rangeObj = None
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
		return (_rangeObj, None)

	def collapse(self, end=False):
		"""Works around a UIA bug on conhost versions before microsoft/terminal#4018.
		When collapsing, consoles seem to incorrectly push the start of the
		textRange back one character.
		Correct this by bringing the start back up to where the end is."""
		oldInfo = self.copy()
		super(ConsoleUIATextInfo, self).collapse(end=end)
		if not end:
			self._rangeObj.MoveEndpointByRange(
				UIAHandler.TextPatternRangeEndpoint_Start,
				oldInfo._rangeObj,
				UIAHandler.TextPatternRangeEndpoint_Start
			)

	def compareEndPoints(self, other, which):
		"""Works around a UIA bug on conhost versions before microsoft/terminal#4018.
		Even when a console textRange's start and end have been moved to the
		same position, the console incorrectly reports the end as being
		past the start.
		Compare to the start (not the end) when collapsed."""
		selfEndPoint, otherEndPoint = which.split("To")
		if selfEndPoint == "end" and self._isCollapsed():
			selfEndPoint = "start"
		if otherEndPoint == "End" and other._isCollapsed():
			otherEndPoint = "Start"
		which = f"{selfEndPoint}To{otherEndPoint}"
		return super().compareEndPoints(other, which=which)

	def setEndPoint(self, other, which):
		"""Override of L{textInfos.TextInfo.setEndPoint}.
		Works around a UIA bug on conhost versions before microsoft/terminal#4018 that means we can
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
			return super(ConsoleUIATextInfo, self).expand(unit)

	def _move(self, unit, direction, endPoint=None):
		if unit == textInfos.UNIT_WORD and direction != 0:
			# On conhost versions before microsoft/terminal#4018, UIA doesn't implement word
			# movement, so we need to do it manually.
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
			res = super(ConsoleUIATextInfo, self).move(unit, direction, endPoint)
		if not endPoint:
			# #10191: IUIAutomationTextRange::move in consoles does not correctly produce a collapsed range
			# after moving.
			# Therefore manually collapse.
			self.collapse()
		return res

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

	def _isCollapsed(self):
		"""Works around a UIA bug on conhost versions before microsoft/terminal#4018 that means we
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

	def _get_text(self):
		# #10036: return a space if the text range is empty.
		# Consoles don't actually store spaces, the character is merely left blank.
		res = super()._get_text()
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

	def _get_apiLevel(self) -> WinConsoleAPILevel:
		"""
		This property shows which of several console UIA workarounds are
		needed in a given conhost instance.
		See the comments on the WinConsoleAPILevel enum for details.
		"""
		self.apiLevel = _getConhostAPILevel(self.windowHandle)
		return self.apiLevel

	def _get__caretMovementTimeoutMultiplier(self):
		"On older consoles, the caret can take a while to move."
		return (
			1 if self.apiLevel >= WinConsoleAPILevel.IMPROVED
			else 1.5
		)

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
		"""Overriding _get_TextInfo and thus the ConsoleUIATextInfo property
		on NVDAObjects.UIA.UIA
		ConsoleUIATextInfo bounds review to the visible text.
		ConsoleUIATextInfoWorkaroundEndInclusive fixes expand/collapse and implements
		word movement."""
		if self.apiLevel >= WinConsoleAPILevel.FORMATTED:
			return UIATextInfo  # No TextInfo workarounds needed
		elif self.apiLevel >= WinConsoleAPILevel.IMPROVED:
			return ConsoleUIATextInfo
		else:
			return ConsoleUIATextInfoWorkaroundEndInclusive

	def _get_devInfo(self):
		info = super().devInfo
		info.append(f"API level: {self.apiLevel} ({self.apiLevel.name})")
		return info

	def _get_diffAlgo(self):
		if self.apiLevel < WinConsoleAPILevel.FORMATTED:
			# #12974: These consoles are constrained to onscreen text.
			# Use Difflib to reduce choppiness in reading.
			return prefer_difflib()
		else:
			return super().diffAlgo

	def detectPossibleSelectionChange(self):
		try:
			return super().detectPossibleSelectionChange()
		except COMError:
			# microsoft/terminal#5399: when attempting to compare text ranges
			# from the standard and alt mode buffers, E_FAIL is returned.
			# Downgrade this to a debugWarning.
			log.debugWarning((
				"Exception raised when comparing selections, "
				"probably due to a switch to/from the alt buffer."
			), exc_info=True)

	def event_UIA_notification(self, **kwargs):
		"""
		In Windows Sun Valley 2 (SV2 M2), UIA notification events will be sent
		to announce new text. Block these for now to avoid double-reporting of
		text changes.
		@note: In the longer term, NVDA should leverage these events in place
		of the current LiveText strategy, as performance will likely be
		significantly improved and #11002 can be completely mitigated.
		"""
		log.debugWarning(f"Notification event blocked to avoid double-report: {kwargs}")


def findExtraOverlayClasses(obj, clsList):
	if obj.UIAAutomationId == "Text Area":
		clsList.append(WinConsoleUIA)
	elif obj.UIAAutomationId == "Console Window":
		clsList.append(consoleUIAWindow)


class WinTerminalUIA(EnhancedTermTypedCharSupport):
	def event_UIA_notification(self, **kwargs):
		"""
		In an upcoming terminal release, UIA notification events will be sent
		to announce new text. Block these for now to avoid double-reporting of
		text changes.
		@note: In the longer term, NVDA should leverage these events in place
		of the current LiveText strategy, as performance will likely be
		significantly improved and #11002 can be completely mitigated.
		"""
		log.debugWarning(f"Notification event blocked to avoid double-report: {kwargs}")
