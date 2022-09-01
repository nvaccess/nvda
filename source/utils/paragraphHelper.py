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

MAX_LINES = 250  # give up after searching this many lines


def nextParagraphStyle() -> config.featureFlag.FeatureFlag:
	from config.featureFlagEnums import ParagraphNavigationFlag
	flag: config.featureFlag.FeatureFlag = config.conf["documentNavigation"]["paragraphStyle"]
	numStyles = len(ParagraphNavigationFlag.__members__)
	newEnumVal = flag.value.value + 1
	newEnumVal %= numStyles
	newFlag: config.featureFlag.FeatureFlag = ParagraphNavigationFlag(newEnumVal)
	return newFlag


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


def isAcceptableTextInfo(ti: textInfos.TextInfo) -> bool:
	acceptable = True
	# disallow if in a Word document, as Word has performance issues
	if isinstance(ti, WordDocumentTextInfo) or isinstance(ti, BrowseModeWordDocumentTextInfo):
		acceptable = False
	# disallow if EditableTextDisplayModelTextInfo, as has performance issues (TextPad for example)
	if isinstance(ti, EditableTextDisplayModelTextInfo):
		acceptable = False
	return acceptable


def isLastLineOfParagraph(line: str) -> bool:
	stripped = line.strip(' \t')
	return stripped.endswith('\r') or stripped.endswith('\n')


def splitParagraphIntoChunks(paragraph: str) -> list([str]):
	CHUNK_SIZE = 2048
	SENTENCE_TERMINATOR = ". "
	TERMINATOR_LEN = len(SENTENCE_TERMINATOR)
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
		while (end != -1) and ((end - start) < maxNextChunk):
			end = paragraph.find(SENTENCE_TERMINATOR, end)
			if end != -1:
				end += TERMINATOR_LEN
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
		if isLastLineOfParagraph(tempTi.text):
			break
		if not tempTi.move(textInfos.UNIT_LINE, 1):
			break
		numLines += 1

	if len(paragraph.strip()) > 0:
		chunks = splitParagraphIntoChunks(paragraph)
		for chunk in chunks:
			speech.speakMessage(chunk)
	else:
		# Translators: This is spoken when a paragraph is considered blank.
		speech.speakMessage(_("blank"))


def moveToParagraph(nextParagraph: bool, speakNew: bool) -> tuple((bool, bool)):
	"""
	Moves to the previous or next normal paragraph, delimited by a single line break.
	@param nextParagraph: bool indicating desired direction of movement,
	True for next paragraph, False for previous paragraph
	@param speakNew: bool indicating if new paragraph should be spoken after navigating
	@returns: A boolean 2-tuple of:
	-passKey: if True, should send the gesture on
	- moved: if True, position has changed
	"""
	ti = getTextInfoAtCaret()
	if (ti is None) or (not isAcceptableTextInfo(ti)):
		return (True, False)
	ti.expand(textInfos.UNIT_LINE)
	ti.collapse()  # move to start of line
	moveOffset = 1 if nextParagraph else -1
	moved = False
	numLines = 0
	tempTi = ti.copy()
	tempTi.expand(textInfos.UNIT_LINE)
	# if starting line is the last line of a paragraph, move back two paragraph markers
	moveBackTwice = isLastLineOfParagraph(tempTi.text)
	while numLines < MAX_LINES:
		tempTi = ti.copy()
		tempTi.expand(textInfos.UNIT_LINE)
		if isLastLineOfParagraph(tempTi.text):
			if not nextParagraph:
				if not moveBackTwice:
					while numLines < MAX_LINES:
						if not ti.move(textInfos.UNIT_LINE, -1):
							moved = True  # pin to beginning
							break
						tempTi = ti.copy()
						tempTi.expand(textInfos.UNIT_LINE)
						if isLastLineOfParagraph(tempTi.text):
							ti.move(textInfos.UNIT_LINE, 1)
							moved = True
							break
						numLines += 1

					break  # break out of outer while loop
				else:
					moveBackTwice = False
			else:  # moving to next paragraph
				if ti.move(textInfos.UNIT_LINE, 1):
					moved = True
				break
		if not ti.move(textInfos.UNIT_LINE, moveOffset):
			break
		numLines += 1

	if moved:
		ti.updateCaret()
		if isinstance(ti, UIATextInfo):
			ti._rangeObj.ScrollIntoView(False)
		speakParagraph(ti)
	else:
		tones.beep(1000, 30)
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
		if not tempTi.move(textInfos.UNIT_LINE, 1):
			break
		numLines += 1

	chunks = splitParagraphIntoChunks(paragraph)
	for chunk in chunks:
		speech.speakMessage(chunk)


def moveToBlockParagraph(
		nextParagraph: bool, speakNew: bool, ti: textInfos.TextInfo = None) -> tuple((bool, bool)):
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
	if (ti is None) or (not isAcceptableTextInfo(ti)):
		return (True, False)
	moved = False
	lookingForBlank = True
	moveOffset = 1 if nextParagraph else -1
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
			if not ti.move(textInfos.UNIT_LINE, -1):
				moved = True
				break  # leave at top
			tempTi = ti.copy()
			tempTi.expand(textInfos.UNIT_LINE)
			if not len(tempTi.text.strip()):
				# found blank line before desired paragraph
				ti.move(textInfos.UNIT_LINE, 1)  # first line of paragraph
				moved = True
				break
			numLines += 1

	if moved:
		ti.updateCaret()
		if isinstance(ti, UIATextInfo):
			# Updating caret position in UITextInfo does not scroll the display. Force it to scroll here.
			ti._rangeObj.ScrollIntoView(False)
		if speakNew:
			speakBlockParagraph(ti)
	else:
		tones.beep(1000, 30)

	return (False, moved)
