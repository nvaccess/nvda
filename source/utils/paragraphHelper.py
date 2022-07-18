# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import api
import speech
import controlTypes
import textInfos
import tones

MAX_LINES = 250  # give up after searching this many lines


def getTextInfoAtCaret() -> textInfos.TextInfo:
	# returns None if not editable text or if in Microsoft Word document
	ti = None
	focus = api.getFocusObject()
	if controlTypes.State.MULTILINE not in focus.states:
		return ti
	if focus.role == controlTypes.Role.EDITABLETEXT:
		try:
			ti = focus.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			pass

	return ti


def isLastLineOfParagraph(line: str):
	stripped = line.strip(' \t')
	return stripped.endswith('\r') or stripped.endswith('\n')


def speakParagraph(ti: textInfos.TextInfo):
	paragraph = ""
	lines = 0
	tempTi = ti.copy()
	while lines < MAX_LINES:
		tempTi.expand(textInfos.UNIT_LINE)
		line = tempTi.text.strip()
		if len(line) > 0:
			paragraph += line + " "
		if isLastLineOfParagraph(tempTi.text):
			break
		if not tempTi.move(textInfos.UNIT_LINE, 1):
			break
		lines += 1

	if len(paragraph.strip()) > 0:
		speech.speakMessage(paragraph)
	else:
		# Translators: This is spoken when a paragraph is considered blank.
		speech.speakMessage(_("blank"))


def moveToParagraph(nextParagraph: bool, speakNew: bool) -> bool:
	# moves to previous or next regular paragraph, delineated by a single line break
	ti = getTextInfoAtCaret()
	if ti is None:
		return False
	ti.expand(textInfos.UNIT_LINE)
	ti.collapse()  # move to start of line
	moveOffset = 1 if nextParagraph else -1
	moved = False
	lines = 0
	tempTi = ti.copy()
	tempTi.expand(textInfos.UNIT_LINE)
	# if starting line is the last line of a paragraph, move back two paragraph markers
	moveBackTwice = isLastLineOfParagraph(tempTi.text)
	while lines < MAX_LINES:
		tempTi = ti.copy()
		tempTi.expand(textInfos.UNIT_LINE)
		if isLastLineOfParagraph(tempTi.text):
			if not nextParagraph:
				if not moveBackTwice:
					while lines < MAX_LINES:
						if not ti.move(textInfos.UNIT_LINE, -1):
							moved = True  # pin to beginning
							break
						tempTi = ti.copy()
						tempTi.expand(textInfos.UNIT_LINE)
						if isLastLineOfParagraph(tempTi.text):
							ti.move(textInfos.UNIT_LINE, 1)
							moved = True
							break
						lines += 1

					break  # break out of outer while loop
				else:
					moveBackTwice = False
			else:  # moving to next paragraph
				if ti.move(textInfos.UNIT_LINE, 1):
					moved = True
				break
		if not ti.move(textInfos.UNIT_LINE, moveOffset):
			break
		lines += 1

	if moved:
		ti.updateCaret()
		speakParagraph(ti)
	else:
		tones.beep(1000, 30)
	return True


def speakBlockParagraph(ti: textInfos.TextInfo):
	# ti is TextInfo object
	paragraph = ""
	lines = 0
	tempTi = ti.copy()
	while lines < MAX_LINES:
		tempTi.expand(textInfos.UNIT_LINE)
		line = tempTi.text.strip()
		if not len(line):
			break
		paragraph += line + "\r\n"
		if not tempTi.move(textInfos.UNIT_LINE, 1):
			break
		lines += 1

	speech.speakMessage(paragraph)


def moveToBlockParagraph(nextParagraph: bool, speakNew: bool) -> bool:
	ti = getTextInfoAtCaret()
	if ti is None:
		return False
	moved = False
	lookingForBlank = True
	moveOffset = 1 if nextParagraph else -1
	lines = 0
	while lines < MAX_LINES:
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
		lines += 1

	# exception: if moving backwards, need to move to top of now current paragraph
	if moved and not nextParagraph:
		while lines < MAX_LINES:
			if not ti.move(textInfos.UNIT_LINE, -1):
				break  # leave at top
			tempTi = ti.copy()
			tempTi.expand(textInfos.UNIT_LINE)
			if not len(tempTi.text.strip()):
				# found blank line before desired paragraph
				ti.move(textInfos.UNIT_LINE, 1)  # first line of paragraph
				break
			lines += 1

	if moved:
		ti.updateCaret()
		if speakNew:
			speakBlockParagraph(ti)
	else:
		tones.beep(1000, 30)

	return True
