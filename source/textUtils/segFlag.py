# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from enum import IntFlag

# shared bit masks (explicit powers of two)
_ON_SEGMENTER = 1 << 0
_UNISCRIBE = 1 << 1
_CHINESE = 1 << 2


class CharSegFlag(IntFlag):
	"""Character-level segmentation flags."""

	NONE = 0
	ON_SEGMENTER = _ON_SEGMENTER
	UNISCRIBE = _UNISCRIBE


class WordSegFlag(IntFlag):
	"""Word-level segmentation flags."""

	NONE = 0
	ON_SEGMENTER = _ON_SEGMENTER
	UNISCRIBE = _UNISCRIBE
	CHINESE = _CHINESE
