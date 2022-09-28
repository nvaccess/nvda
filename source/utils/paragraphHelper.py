# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import api
import speech
import controlTypes
import textInfos
import tones
import config
from NVDAObjects.window.winword import WordDocumentTextInfo
from NVDAObjects.window.winword import BrowseModeWordDocumentTextInfo
from NVDAObjects.UIA import UIATextInfo
from displayModel import EditableTextDisplayModelTextInfo
from typing import (
	Tuple,
	List,
	FrozenSet,
)
from enum import IntEnum
from dataclasses import dataclass

MAX_LINES = 250  # give up after searching this many lines


@dataclass(frozen=True)
class _ErrorToneData:
	frequencyHz: float = 1000.0
	durationMs: int = 30


_ERROR_TONE = _ErrorToneData()


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


def getTextInfoAtCaret() -> textInfos.TextInfo:
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


def _splitParagraphIntoChunks(paragraph: str) -> List[str]:
	CHUNK_SIZE = 2048
	SENTENCE_TERMINATORS: FrozenSet[str] = {".", "?", "!"}
	start = 0
	paragraphLen = len(paragraph)
	if paragraphLen <= CHUNK_SIZE:
		return [paragraph]
	chunks = []
	while start < paragraphLen:
		remaining = paragraphLen - start
		if remaining <= CHUNK_SIZE:
			chunks.append(paragraph[start:])
			break
		end = start
		maxNextChunk = min(remaining, CHUNK_SIZE)
		lastTerminatorEnd = -1
		while (end != -1) and ((end - start) < maxNextChunk):
			end = paragraph.find(" ", end)
			if end > 0 and paragraph[end - 1] in SENTENCE_TERMINATORS:
				lastTerminatorEnd = end + 1
			if end != -1:
				end += 1
		end = lastTerminatorEnd
		if end == -1:
			chunks.append(paragraph[start:])
			break
		chunks.append(paragraph[start: end])
		start = end
	return chunks


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
		chunks = _splitParagraphIntoChunks(paragraph)
		for chunk in chunks:
			speech.speakMessage(chunk)
	else:
		# Translators: This is spoken when a paragraph is considered blank.
		speech.speakMessage(_("blank"))


def moveToParagraph(nextParagraph: bool, speakNew: bool) -> Tuple[bool, bool]:
	"""
	Moves to the previous or next normal paragraph, delimited by a single line break.
	@param nextParagraph: bool indicating desired direction of movement,
	True for next paragraph, False for previous paragraph
	@param speakNew: bool indicating if new paragraph should be spoken after navigating
	@returns: A boolean 2-tuple of:
	- passKey: if True, should send the gesture on
	- moved: if True, position has changed
	"""
	ti = getTextInfoAtCaret()
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
		tones.beep(_ERROR_TONE.frequencyHz, _ERROR_TONE.durationMs)
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

	chunks = _splitParagraphIntoChunks(paragraph)
	for chunk in chunks:
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
		ti = getTextInfoAtCaret()
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
		tones.beep(_ERROR_TONE.frequencyHz, _ERROR_TONE.durationMs)

	return (False, moved)
