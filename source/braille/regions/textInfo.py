# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2008-2026 NV Access Limited, Joseph Lee, Babbage B.V., Davy Kager, Bram Duvigneau, Leonard de Ruijter, Burman's Computer and Education Ltd., Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from __future__ import annotations

import time
from typing import TYPE_CHECKING

import api
import config
import controlTypes
import languageHandler
import louis
import textInfos
from config.configFlags import OutputMode
from config.featureFlagEnums import FontFormattingBrailleModeFlag
from logHandler import log
from utils.security import objectBelowLockScreenAndWindowsIsLocked

if TYPE_CHECKING:
	from NVDAObjects import NVDAObject

import braille

from .base import Region
from ..constants import (
	INPUT_END_IND,
	INPUT_START_IND,
	TEXT_SEPARATOR,
)
from .properties import getFormatFieldBraille
from ._routing import _routingShouldMoveSystemCaret
from ..labels import positiveStateLabels


class TextInfoRegion(Region):
	pendingCaretUpdate = False  #: True if the cursor should be updated for this region on the display
	allowPageTurns = True  #: True if a page turn should be tried when a TextInfo cannot move anymore and the object supports page turns.

	def __init__(self, obj: "NVDAObject"):
		if objectBelowLockScreenAndWindowsIsLocked(obj):
			raise RuntimeError("NVDA object is secure and should not be initialized as a braille region")
		super().__init__()
		self.obj = obj

	def _isMultiline(self):
		# A region's object can either be an NVDAObject or a tree interceptor.
		# Tree interceptors should always be multiline.
		from treeInterceptorHandler import TreeInterceptor

		if isinstance(self.obj, TreeInterceptor):
			return True
		# Terminals and documents are inherently multiline, so they don't have the multiline state.
		return (
			self.obj.role in (controlTypes.Role.TERMINAL, controlTypes.Role.DOCUMENT)
			or controlTypes.State.MULTILINE in self.obj.states
		)

	def _getSelection(self):
		"""Retrieve the selection.
		If there is no selection, retrieve the collapsed cursor.
		@return: The selection.
		@rtype: L{textInfos.TextInfo}
		"""
		try:
			return self.obj.makeTextInfo(textInfos.POSITION_SELECTION)
		except:  # noqa: E722
			return self.obj.makeTextInfo(textInfos.POSITION_FIRST)

	def _setCursor(self, info: textInfos.TextInfo):
		"""Set the cursor.
		@param info: The range to which the cursor should be moved.
		"""
		try:
			info.updateCaret()
		except NotImplementedError:
			log.debugWarning("", exc_info=True)

	def _getTypeformFromFormatField(self, field, formatConfig):
		typeform = louis.plain_text
		if not (
			(formatConfig["fontAttributeReporting"] & OutputMode.BRAILLE)
			and (
				config.conf["braille"]["fontFormattingDisplay"].calculated()
				== FontFormattingBrailleModeFlag.LIBLOUIS
			)
		):
			return typeform
		if field.get("bold", False):
			typeform |= louis.bold
		if field.get("italic", False):
			typeform |= louis.italic
		if field.get("underline", False):
			typeform |= louis.underline
		return typeform

	def _addFieldText(
		self,
		text: str,
		contentPos: int,
		separate: bool = True,
	):
		if separate and self.rawText:
			# Separate this field text from the rest of the text.
			text = TEXT_SEPARATOR + text
		textLen = len(text)
		# Fields are reported in NVDA's language
		fieldLanguage = languageHandler.getLanguage()
		rawTextLen = len(self.rawText)
		lastLanguage = self._getLanguageAtPos(rawTextLen)
		if fieldLanguage != lastLanguage:
			self._languageIndexes[rawTextLen] = fieldLanguage
			self._languageIndexes[rawTextLen + textLen] = lastLanguage
		self.rawText += text
		self.rawTextTypeforms.extend((louis.plain_text,) * textLen)
		self._rawToContentPos.extend((contentPos,) * textLen)

	def _addTextWithFields(self, info, formatConfig, isSelection=False):
		shouldMoveCursorToFirstContent = not isSelection and self.cursorPos is not None
		ctrlFields = []
		typeform = louis.plain_text
		formatFieldAttributesCache = getattr(info.obj, "_brailleFormatFieldAttributesCache", {})
		# When true, we are inside a clickable field, and should therefore not report any more new clickable fields
		inClickable = False
		# Collapsed ranges should never produce text and fields,
		# But later on we may still need to draw the cursor at this position.
		if not info.isCollapsed:
			commands = info.getTextWithFields(formatConfig=formatConfig)
		else:
			commands = []
		for command in commands:
			if isinstance(command, str):
				# Text should break a run of clickables
				inClickable = False
				self._isFormatFieldAtStart = False
				if not command:
					continue
				if self._endsWithField:
					# The last item added was a field,
					# so add a space before the content.
					self.rawText += TEXT_SEPARATOR
					self.rawTextTypeforms.append(louis.plain_text)
					self._rawToContentPos.append(self._currentContentPos)
				if isSelection and self.selectionStart is None:
					# This is where the content begins.
					self.selectionStart = len(self.rawText)
				elif shouldMoveCursorToFirstContent:
					# This is the first piece of content after the cursor.
					# Position the cursor here, as it may currently be positioned on control field text.
					self.cursorPos = len(self.rawText)
					shouldMoveCursorToFirstContent = False
				self.rawText += command
				commandLen = len(command)
				self.rawTextTypeforms.extend((typeform,) * commandLen)
				endPos = self._currentContentPos + commandLen
				self._rawToContentPos.extend(range(self._currentContentPos, endPos))
				self._currentContentPos = endPos
				if isSelection:
					# The last time this is set will be the end of the content.
					self.selectionEnd = len(self.rawText)
				self._endsWithField = False
			elif isinstance(command, textInfos.FieldCommand):
				cmd = command.command
				field = command.field
				if cmd == "formatChange":
					typeform = self._getTypeformFromFormatField(field, formatConfig)
					language = field.get("language")
					text = getFormatFieldBraille(
						field,
						formatFieldAttributesCache,
						self._isFormatFieldAtStart,
						formatConfig,
					)
					if text:
						# Map this field text to the start of the field's content.
						self._addFieldText(text, self._currentContentPos)
					rawTextLen = len(self.rawText)
					if language and self._getLanguageAtPos(rawTextLen) != language:
						self._languageIndexes[rawTextLen] = language
					if not text:
						continue
				elif cmd == "controlStart":
					if self._skipFieldsNotAtStartOfNode and not field.get("_startOfNode"):
						text = None
					else:
						textList = []
						if not inClickable and formatConfig["reportClickable"]:
							states = field.get("states")
							if states and controlTypes.State.CLICKABLE in states:
								# We have entered an outer most clickable or entered a new clickable after exiting a previous one
								# Report it if there is nothing else interesting about the field
								field._presCat = presCat = field.getPresentationCategory(
									ctrlFields,
									formatConfig,
								)
								if not presCat or presCat is field.PRESCAT_LAYOUT:
									textList.append(positiveStateLabels[controlTypes.State.CLICKABLE])
								inClickable = True
						text = info.getControlFieldBraille(field, ctrlFields, True, formatConfig)
						if text:
							textList.append(text)
						text = " ".join(textList)
					# Place this field on a stack so we can access it for controlEnd.
					ctrlFields.append(field)
					if not text:
						continue
					if getattr(field, "_presCat") == field.PRESCAT_MARKER:
						# In this case, the field text is what the user cares about,
						# not the actual content.
						fieldStart = len(self.rawText)
						if fieldStart > 0:
							# There'll be a space before the field text.
							fieldStart += 1
						if isSelection and self.selectionStart is None:
							self.selectionStart = fieldStart
						elif shouldMoveCursorToFirstContent:
							self.cursorPos = fieldStart
							shouldMoveCursorToFirstContent = False
					# Map this field text to the start of the field's content.
					self._addFieldText(text, self._currentContentPos)
				elif cmd == "controlEnd":
					# Exiting a controlField should break a run of clickables
					inClickable = False
					field = ctrlFields.pop()
					text = info.getControlFieldBraille(field, ctrlFields, False, formatConfig)
					if not text:
						continue
					# Map this field text to the end of the field's content.
					self._addFieldText(text, self._currentContentPos - 1)
				self._endsWithField = True
		if isSelection and self.selectionStart is None:
			# There is no selection. This is a cursor.
			self.cursorPos = len(self.rawText)
		if not self._skipFieldsNotAtStartOfNode:
			# We only render fields that aren't at the start of their nodes for the first part of the reading unit.
			# Otherwise, we'll render fields that have already been rendered.
			self._skipFieldsNotAtStartOfNode = True
		info.obj._brailleFormatFieldAttributesCache = formatFieldAttributesCache

	def _getReadingUnit(self):
		return textInfos.UNIT_PARAGRAPH if config.conf["braille"]["readByParagraph"] else textInfos.UNIT_LINE

	def update(self):
		formatConfig = config.conf["documentFormatting"]
		unit = self._getReadingUnit()
		self.rawText = ""
		self.rawTextTypeforms = []
		self.cursorPos = None
		self._languageIndexes: dict[int, str] = {0: self._getDefaultRegionLanguage()}
		# The output includes text representing fields which isn't part of the real content in the control.
		# Therefore, maintain a map of positions in the output to positions in the content.
		self._rawToContentPos = []
		self._currentContentPos = 0
		self.selectionStart = self.selectionEnd = None
		self._isFormatFieldAtStart = True
		self._skipFieldsNotAtStartOfNode = False
		self._endsWithField = False

		# Selection has priority over cursor.
		# HACK: Some TextInfos only support UNIT_LINE properly if they are based on POSITION_CARET,
		# and copying the TextInfo breaks this ability.
		# So use the original TextInfo for line and a copy for cursor/selection.
		self._readingInfo = readingInfo = self._getSelection()
		sel = readingInfo.copy()
		if not sel.isCollapsed:
			# There is a selection.
			if self.obj.isTextSelectionAnchoredAtStart:
				# The end of the range is exclusive, so make it inclusive first.
				readingInfo.move(textInfos.UNIT_CHARACTER, -1, "end")
			# Collapse the selection to the unanchored end.
			readingInfo.collapse(end=self.obj.isTextSelectionAnchoredAtStart)
			# Get the reading unit at the selection.
			readingInfo.expand(unit)
			# Restrict the selection to the reading unit.
			if sel.compareEndPoints(readingInfo, "startToStart") < 0:
				sel.setEndPoint(readingInfo, "startToStart")
			if sel.compareEndPoints(readingInfo, "endToEnd") > 0:
				sel.setEndPoint(readingInfo, "endToEnd")
		else:
			# There is a cursor.
			# Get the reading unit at the cursor.
			readingInfo.expand(unit)

		# Not all text APIs support offsets, so we can't always get the offset of the selection relative to the start of the reading unit.
		# Therefore, grab the reading unit in three parts.
		# First, the chunk from the start of the reading unit to the start of the selection.
		chunk = readingInfo.copy()
		chunk.collapse()
		chunk.setEndPoint(sel, "endToStart")
		self._addTextWithFields(chunk, formatConfig)
		# If the user is entering braille, place any untranslated braille before the selection.
		# Import late to avoid circular import.
		import brailleInput

		text = brailleInput.handler.untranslatedBraille
		if text:
			rawInputIndStart = len(self.rawText)
			# _addFieldText adds text to self.rawText and updates other state accordingly.
			self._addFieldText(INPUT_START_IND + text + INPUT_END_IND, None, separate=False)
			rawInputIndEnd = len(self.rawText)
		else:
			rawInputIndStart = None
		# Now, the selection itself.
		self._addTextWithFields(sel, formatConfig, isSelection=True)
		# Finally, get the chunk from the end of the selection to the end of the reading unit.
		chunk.setEndPoint(readingInfo, "endToEnd")
		chunk.setEndPoint(sel, "startToEnd")
		self._addTextWithFields(chunk, formatConfig)

		# Strip line ending characters.
		self.rawText = self.rawText.rstrip("\r\n\0\v\f")
		rawTextLen = len(self.rawText)
		if rawTextLen < len(self._rawToContentPos):
			# The stripped text is shorter than the original.
			self._currentContentPos = self._rawToContentPos[rawTextLen]
			del self.rawTextTypeforms[rawTextLen:]
			# Trimming _rawToContentPos doesn't matter,
			# because we'll only ever ask for indexes valid in rawText.
			# del self._rawToContentPos[rawTextLen:]
		if rawTextLen == 0 or not self._endsWithField:
			# There is no text left after stripping line ending characters,
			# or the last item added can be navigated with a cursor.
			# Add a space in case the cursor is at the end of the reading unit.
			self.rawText += TEXT_SEPARATOR
			rawTextLen += 1
			self.rawTextTypeforms.append(louis.plain_text)
			self._rawToContentPos.append(self._currentContentPos)
		if self.cursorPos is not None and self.cursorPos >= rawTextLen:
			self.cursorPos = rawTextLen - 1
		# The selection end doesn't have to be checked, Region.update() makes sure brailleSelectionEnd is valid.

		# If this is not the start of the object, hide all previous regions.
		start = readingInfo.obj.makeTextInfo(textInfos.POSITION_FIRST)
		self.hidePreviousRegions = start.compareEndPoints(readingInfo, "startToStart") < 0
		# Don't touch focusToHardLeft if it is already true
		# For example, it can be set to True in getFocusContextRegions when this region represents the first new focus ancestor
		# Alternatively, BrailleHandler._doNewObject can set this to True when this region represents the focus object and the focus ancestry didn't change
		if not self.focusToHardLeft:
			# If this is a multiline control, position it at the absolute left of the display when focused.
			self.focusToHardLeft = self._isMultiline()
		super(TextInfoRegion, self).update()

		if rawInputIndStart is not None:
			assert rawInputIndEnd is not None, "rawInputIndStart set but rawInputIndEnd isn't"
			# These are the start and end of the untranslated input area,
			# including the start and end indicators.
			self._brailleInputIndStart = self.rawToBraillePos[rawInputIndStart]
			self._brailleInputIndEnd = self.rawToBraillePos[rawInputIndEnd]
			# These are the start and end of the actual untranslated input, excluding indicators.
			self._brailleInputStart = self._brailleInputIndStart + len(INPUT_START_IND)
			self._brailleInputEnd = self._brailleInputIndEnd - len(INPUT_END_IND)
			self.brailleCursorPos = self._brailleInputStart + brailleInput.handler.untranslatedCursorPos
		else:
			self._brailleInputIndStart = None

	def getTextInfoForBraillePos(self, braillePos: int) -> textInfos.TextInfo:
		"""Fetches a collapsed TextInfo at the specified braille position in the region.
		:param braillePos: The braille position.
			If no textInfo could be found at braillePos,
			try to find one at braillePos - 1 until a position has been found.
		"""
		pos = self._rawToContentPos[self.brailleToRawPos[braillePos]]
		# pos is relative to the start of the reading unit.
		maxIterations = 10
		startTime = time.time()
		for i, curPos in enumerate(range(pos, max(-1, pos - maxIterations), -1)):
			if curPos == 0:
				# Not necessary to find offset.
				break
			# Move curPos code points from the start.
			# Note that, as liblouis uses 32 bit encoding internally,
			# it is really safe to assume that one code point offset is equal to one character within liblouis.
			# If an attempt fails, we try to move to the previous character
			try:
				return self._readingInfo.moveToCodepointOffset(curPos)
			except RuntimeError:
				msg = f"Error in moveToCodepointOffset in iteration {i + 1} (position {curPos}"
				if i + 1 >= maxIterations or (exceeded := time.time() - startTime > 0.5):
					logFunc = log.exception
					curPos = pos
					if exceeded:
						msg += ", exceeded time limit of 0.5 seconds"
				else:
					logFunc = log.debug
				logFunc(msg)
		dest = self._readingInfo.copy()
		dest.collapse()
		if curPos > 0:
			dest.move(textInfos.UNIT_CHARACTER, curPos)
		return dest

	def routeTo(self, braillePos: int):
		if (
			self._brailleInputIndStart is not None
			and self._brailleInputIndStart <= braillePos < self._brailleInputIndEnd
		):
			# The user is moving within untranslated braille input.
			if braillePos < self._brailleInputStart:
				# The user routed to the start indicator. Route to the start of the input.
				braillePos = self._brailleInputStart
			elif braillePos > self._brailleInputEnd:
				# The user routed to the end indicator. Route to the end of the input.
				braillePos = self._brailleInputEnd
			# Import late to avoid circular import.
			import brailleInput

			brailleInput.handler.untranslatedCursorPos = braillePos - self._brailleInputStart
			self.brailleCursorPos = self._brailleInputStart + brailleInput.handler.untranslatedCursorPos
			brailleInput.handler.updateDisplay()
			return

		dest = self.getTextInfoForBraillePos(braillePos)
		self._routeToTextInfo(dest)

	def _routeToTextInfo(self, info: textInfos.TextInfo):
		# When there is a selection, brailleCursorPos will be None
		# Don't activate, but move the cursor to the new cell (dropping the
		# selection). An alternative behavior may be to activate on the selection.
		# Moving the cursor was considered more intuitive.
		if self.brailleCursorPos is not None:
			cursor = self.getTextInfoForBraillePos(self.brailleCursorPos)
			if info.compareEndPoints(cursor, "startToStart") == 0:
				# The cursor is already at this position,
				# so activate the position.
				try:
					self._getSelection().activate()
				except NotImplementedError:
					pass
				return
		self._setCursor(info)
		_speakOnRouting(info.copy())

	def nextLine(self):
		dest = self._readingInfo.copy()
		shouldCollapseToEnd = False
		moved = dest.move(self._getReadingUnit(), 1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj, textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage()
				except RuntimeError:
					braille.handler.autoScroll(enable=False)
				else:
					dest = dest.obj.makeTextInfo(textInfos.POSITION_FIRST)
			else:  # no page turn support
				braille.handler.autoScroll(enable=False)
				shouldCollapseToEnd = True
		dest.collapse(shouldCollapseToEnd)
		self._setCursor(dest)
		_speakOnNavigatingByUnit(dest, self._getReadingUnit())

	def previousLine(self, start=False):
		dest = self._readingInfo.copy()
		dest.collapse()
		if start:
			unit = self._getReadingUnit()
		else:
			# If the end of the reading unit is desired, move to the last character.
			unit = textInfos.UNIT_CHARACTER
		moved = dest.move(unit, -1)
		if not moved:
			if self.allowPageTurns and isinstance(dest.obj, textInfos.DocumentWithPageTurns):
				try:
					dest.obj.turnPage(previous=True)
				except RuntimeError:
					pass
				else:
					dest = dest.obj.makeTextInfo(textInfos.POSITION_LAST)
					dest.expand(unit)
			else:
				# no page turn support
				return
		dest.collapse()
		self._setCursor(dest)
		_speakOnNavigatingByUnit(dest, self._getReadingUnit())


class CursorManagerRegion(TextInfoRegion):
	def _isMultiline(self):
		return True

	def _getSelection(self):
		return self.obj.selection

	def _setCursor(self, info: textInfos.TextInfo):
		self.obj.selection = info


class ReviewTextInfoRegion(TextInfoRegion):
	allowPageTurns = False

	def _getSelection(self):
		return api.getReviewPosition().copy()

	def _routeToTextInfo(self, info: textInfos.TextInfo):
		super()._routeToTextInfo(info)
		if not _routingShouldMoveSystemCaret():
			return
		from displayModel import DisplayModelTextInfo, EditableTextDisplayModelTextInfo

		if isinstance(info, DisplayModelTextInfo) and not isinstance(info, EditableTextDisplayModelTextInfo):
			# This region either reviews the screen or an object that has
			# DisplayModelTextInfo without a caret, e.g. IAccessible.ContentGenericClient.
			# In this case, we can at least emulate a kind of caret
			# by trying to focus the object at start of the range.
			obj = info.NVDAObjectAtStart
			if not objectBelowLockScreenAndWindowsIsLocked(obj) and obj.isFocusable and not obj.hasFocus:
				obj.setFocus()
		else:
			# Update the physical caret using the super class.
			super()._setCursor(info)

	def _setCursor(self, info: textInfos.TextInfo):
		api.setReviewPosition(info)


class ReviewCursorManagerRegion(ReviewTextInfoRegion, CursorManagerRegion): ...


def _speakOnRouting(info: textInfos.TextInfo):
	"""Speaks the character at the cursor position after routing.

	:param info: The TextInfo at the cursor position after routing.
	"""
	if not config.conf["braille"]["speakOnRouting"]:
		return
	# Import late to avoid circular import.
	from speech.speech import spellTextInfo

	info.expand(textInfos.UNIT_CHARACTER)
	spellTextInfo(info)


def _speakOnNavigatingByUnit(info: textInfos.TextInfo, readingUnit: str) -> None:
	"""Speaks the reading unit after navigating by it with braille.

	This only has an effect if the user has enabled "Speak when navigating by line or paragraph" in braille settings.

	:param info: The TextInfo at the cursor position after navigating.
	:param readingUnit: The reading unit to expand TextInfo.
	"""
	if not config.conf["braille"]["speakOnNavigatingByUnit"]:
		return
	# Import late to avoid circular import.
	from speech.speech import cancelSpeech, speakTextInfo

	copy = info.copy()
	copy.expand(readingUnit)
	cancelSpeech()
	speakTextInfo(copy, unit=readingUnit, reason=controlTypes.OutputReason.CARET)
