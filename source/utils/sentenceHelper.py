# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited, Rob Meredith
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import re

WESTERN_TERMINATORS_PATTERN: re.Pattern = re.compile("[.?!]( |\r|\n)+")
WESTERN_TERMINATORS_SINGLE_PATTERN: re.Pattern = re.compile("[.?!]")
FULL_WIDTH_TERMINATORS_PATTERN: re.Pattern = re.compile("[。！？]")


def findEndOfSentence(sentence: str, offset: int) -> int:
	res = -1
	m = re.search(FULL_WIDTH_TERMINATORS_PATTERN, sentence[offset:])
	if m:
		res = m.end() + offset
	else:
		m = re.search(WESTERN_TERMINATORS_PATTERN, sentence[offset:])
		if m:
			res = m.end() + offset
		else:
			if re.match(WESTERN_TERMINATORS_SINGLE_PATTERN, sentence[-1]):  # check for terminator at end of string
				res = len(sentence)
	return res
