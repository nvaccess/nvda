# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import re

WESTERN_TERMINATORS = "[.?!](?: |\r|\n|$)+"
FULL_WIDTH_TERMINATORS = "[。！？](?:\r|\n)*"
TERMINATORS_PATTERN: re.Pattern = re.compile(WESTERN_TERMINATORS + "|" + FULL_WIDTH_TERMINATORS)


def _findNextEndOfSentence(sentence: str, offset: int) -> int | None:
	"""
	Returns an index which points one character past the end of the current sentence,
	or if the sentence is at the end of the string, returns the length of the string.
	Returns None if sentence end not found.
	In the case of western sentence terminators,
	combinations of space, \r, or \n at the end of the sentence are included.
	In the case of full width sentence terminators,
	combinations of \r or \n at the end of the sentence are included.
	@param sentence: string containing at least current sentence
	@param offset: int indicating where to start searching for the end of the sentence
	"""
	res = None
	if not len(sentence):
		return res  # do nothing if empty string
	m = re.search(TERMINATORS_PATTERN, sentence[offset:])
	if m:
		res = m.end() + offset
	return res
