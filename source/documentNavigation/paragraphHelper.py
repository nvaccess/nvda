# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import api
import speech
import controlTypes
import textInfos
import ui
import config
from NVDAObjects.window.winword import WordDocumentTextInfo
from NVDAObjects.window.winword import BrowseModeWordDocumentTextInfo
from NVDAObjects.UIA import UIATextInfo
from displayModel import EditableTextDisplayModelTextInfo
from typing import (
	Tuple,
	Generator,
	List,
)
from enum import IntEnum

MAX_LINES = 250  # give up after searching this many lines


class _Offset(IntEnum):
	PREVIOUS_LINE = -1
	NEXT_LINE = 1


def nextParagraphStyle() -> config.featureFlag.FeatureFlag:
	from config.featureFlagEnums import ParagraphNavigationFlag
	flag: config.featureFlag.FeatureFlag = config.conf["documentNavigation"]["paragraphStyle"]
	numStyles = len(ParagraphNavigationFlag.__members__)
	newEnumVal = flag.calculated().value + 1
	if newEnumVal > numStyles:
		newEnumVal = ParagraphNavigationFlag.DEFAULT.value + 1  # wrap around, skip DEFAULT

	return ParagraphNavigationFlag(newEnumVal)


def _getTextInfoAtCaret() -> textInfos.TextInfo:
	# returns None if not editable text or document
	ti = None
	focus = api.getFocusObject()
	if (focus.role == controlTypes.Role.EDITABLETEXT) or (focus.role == controlTypes.Role.DOCUMENT):
		try:
			ti = focus.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			pass
	return ti


def _isAcceptableTextInfo(ti: textInfos.TextInfo) -> bool:
	acceptable = True
	# disallow if in a Word document and not using UIA, as Word has performance issues
	if isinstance(ti, WordDocumentTextInfo) or isinstance(ti, BrowseModeWordDocumentTextInfo):
		acceptable = False
	# disallow if EditableTextDisplayModelTextInfo, as has performance issues (TextPad for example)
	if isinstance(ti, EditableTextDisplayModelTextInfo):
		acceptable = False
	return acceptable


def _isLastLineOfParagraph(line: str) -> bool:
	stripped = line.strip(' \t')
	return stripped.endswith('\r') or stripped.endswith('\n')


def _splitParagraphIntoChunks(paragraph: str) -> Generator[str, None, None]:
	"""
	This function attempts to break large paragraphs into smaller chunks
	with the goal of improving processing efficiency by some synthesizers.
	If this function fails to break the paragraph into chunks, functionality will likely be fine,
	though responsiveness may not be optimal.
	"""
	from documentNavigation.sentenceHelper import _findEndOfSentence
	CHUNK_SIZE = 1024
	paragraphLen = len(paragraph)
	if paragraphLen <= CHUNK_SIZE:
		yield paragraph
		return
	sentenceEndPoints: List[int] = []
	endPoint = _findEndOfSentence(paragraph, 0)
	while endPoint is not None:
		sentenceEndPoints.append(endPoint)
		endPoint = _findEndOfSentence(paragraph, endPoint)
	chunkStart = chunkEnd = startIndex = endIndex = 0
	while endIndex < len(sentenceEndPoints):
		chunkLength = sentenceEndPoints[endIndex] - chunkStart
		if chunkLength > CHUNK_SIZE:
			if endIndex > startIndex:
				chunkEnd = sentenceEndPoints[endIndex - 1]
			else:
				chunkEnd = sentenceEndPoints[endIndex]
				endIndex += 1
			yield paragraph[chunkStart: chunkEnd]
			chunkStart = chunkEnd
			startIndex = endIndex
		else:
			endIndex += 1
	if chunkStart < paragraphLen:  # any leftovers?
		yield paragraph[chunkStart:]


def speakParagraph(ti: textInfos.TextInfo) -> None:
	paragraph = ""
	numLines = 0
	tempTi = ti.copy()
	while numLines < MAX_LINES:
		tempTi.expand(textInfos.UNIT_LINE)
		line = tempTi.text.strip()
		if len(line) > 0:
			paragraph += line + " "
		if _isLastLineOfParagraph(tempTi.text):
			break
		if not tempTi.move(textInfos.UNIT_LINE, _Offset.NEXT_LINE):
			break
		numLines += 1

	if len(paragraph.strip()) > 0:
		gen = _splitParagraphIntoChunks(paragraph)
		for chunk in gen:
			speech.speakMessage(chunk)
	else:
		# Translators: This is spoken when a paragraph is considered blank.
		speech.speakMessage(_("blank"))


def _notFoundMessage(nextParagraph: bool):
	if nextParagraph:
		# Translators: this message is given when there is no next paragraph when navigating by paragraph
		ui.message("No next paragraph")
	else:
		# Translators: this message is given when there is no previous paragraph when navigating by paragraph
		ui.message("No previous paragraph")


def moveToParagraph(
		nextParagraph: bool,
		speakNew: bool,
		ti: textInfos.TextInfo = None
) -> Tuple[bool, bool]:
	"""
	Moves to the previous or next normal paragraph, delimited by a single line break.
	@param nextParagraph: bool indicating desired direction of movement,
	True for next paragraph, False for previous paragraph
	@param speakNew: bool indicating if new paragraph should be spoken after navigating
	@param ti: TextInfo object on which to perform the move,
	if None, attempts to create a TextInfo using the current caret position
	@returns: A boolean 2-tuple of:
	- passKey: if True, should send the gesture on
	- moved: if True, position has changed
	"""
	if ti is None:
		ti = _getTextInfoAtCaret()
	if (ti is None) or (not _isAcceptableTextInfo(ti)):
		return (True, False)
	ti.expand(textInfos.UNIT_LINE)
	ti.collapse()  # move to start of line
	moveOffset: _Offset = _Offset.NEXT_LINE if nextParagraph else _Offset.PREVIOUS_LINE
	moved = False
	numLines = 0
	tempTi = ti.copy()
	tempTi.expand(textInfos.UNIT_LINE)
	# if starting line is the last line of a paragraph, move back two paragraph markers
	moveBackTwice = _isLastLineOfParagraph(tempTi.text)
	while numLines < MAX_LINES:
		tempTi = ti.copy()
		tempTi.expand(textInfos.UNIT_LINE)
		if _isLastLineOfParagraph(tempTi.text):
			if not nextParagraph:
				if not moveBackTwice:
					while numLines < MAX_LINES:
						if not ti.move(textInfos.UNIT_LINE, _Offset.PREVIOUS_LINE):
							moved = True  # pin to beginning
							break
						tempTi = ti.copy()
						tempTi.expand(textInfos.UNIT_LINE)
						if _isLastLineOfParagraph(tempTi.text):
							ti.move(textInfos.UNIT_LINE, _Offset.NEXT_LINE)
							moved = True
							break
						numLines += 1

					break  # break out of outer while loop
				else:
					moveBackTwice = False
			else:  # moving to next paragraph
				if ti.move(textInfos.UNIT_LINE, _Offset.NEXT_LINE):
					moved = True
				break
		if not ti.move(textInfos.UNIT_LINE, moveOffset):
			break
		numLines += 1

	if moved:
		ti.updateCaret()
		if isinstance(ti, UIATextInfo):
			# Updating caret position in UIATextInfo does not scroll the display. Force it to scroll here.
			ti._rangeObj.ScrollIntoView(False)
		speakParagraph(ti)
	else:
		_notFoundMessage(nextParagraph)
	return (False, moved)


def speakBlockParagraph(ti: textInfos.TextInfo) -> None:
	paragraph = ""
	numLines = 0
	tempTi = ti.copy()
	while numLines < MAX_LINES:
		tempTi.expand(textInfos.UNIT_LINE)
		line = tempTi.text.strip()
		if not len(line):
			break
		paragraph += line + "\r\n"
		if not tempTi.move(textInfos.UNIT_LINE, _Offset.NEXT_LINE):
			break
		numLines += 1

	gen = _splitParagraphIntoChunks(paragraph)
	for chunk in gen:
		speech.speakMessage(chunk)


def moveToBlockParagraph(
		nextParagraph: bool,
		speakNew: bool,
		ti: textInfos.TextInfo = None
) -> Tuple[bool, bool]:
	"""
	Moves to the previous or next block paragraph, delineated by a blank line.
	@param nextParagraph: bool indicating desired direction of movement,
	True for next paragraph, False for previous paragraph
	@param speakNew: bool indicating if new paragraph should be spoken after navigating
	@param ti: TextInfo object on which to perform the move,
	if None, attempts to create a TextInfo using the current caret position
	@returns: A boolean 2-tuple of:
	- passKey: if True, should send the gesture on
	- moved: if True, position has changed
	"""

	if ti is None:
		ti = _getTextInfoAtCaret()
	if (ti is None) or (not _isAcceptableTextInfo(ti)):
		return (True, False)
	moved = False
	lookingForBlank = True
	moveOffset: _Offset = _Offset.NEXT_LINE if nextParagraph else _Offset.PREVIOUS_LINE
	numLines = 0
	while numLines < MAX_LINES:
		tempTi = ti.copy()
		tempTi.expand(textInfos.UNIT_LINE)
		isBlank = len(tempTi.text.strip()) == 0
		if lookingForBlank and isBlank:
			lookingForBlank = False
		if not lookingForBlank and not isBlank:
			moved = True
			break
		if not ti.move(textInfos.UNIT_LINE, moveOffset):
			break
		numLines += 1

	# exception: if moving backwards, need to move to top of now current paragraph
	if moved and not nextParagraph:
		moved = False
		while numLines < MAX_LINES:
			if not ti.move(textInfos.UNIT_LINE, _Offset.PREVIOUS_LINE):
				moved = True
				break  # leave at top
			tempTi = ti.copy()
			tempTi.expand(textInfos.UNIT_LINE)
			if not len(tempTi.text.strip()):
				# found blank line before desired paragraph
				ti.move(textInfos.UNIT_LINE, _Offset.NEXT_LINE)  # first line of paragraph
				moved = True
				break
			numLines += 1

	if moved:
		ti.updateCaret()
		if isinstance(ti, UIATextInfo):
			# Updating caret position in UIATextInfo does not scroll the display. Force it to scroll here.
			ti._rangeObj.ScrollIntoView(False)
		if speakNew:
			speakBlockParagraph(ti)
	else:
		_notFoundMessage(nextParagraph)

	return (False, moved)
