# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Wang Chong
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from enum import IntFlag

# shared bit masks (explicit powers of two)
_ON_SEGMENTER: int = 1 << 0
_UNISCRIBE: int = 1 << 1
_CHINESE: int = 1 << 2


class CharSegFlag(IntFlag):
	"""Character-level segmentation flags."""

	NONE: int = 0
	ON_SEGMENTER: int = _ON_SEGMENTER
	UNISCRIBE: int = _UNISCRIBE


class WordSegFlag(IntFlag):
	"""Word-level segmentation flags."""

	NONE: int = 0
	ON_SEGMENTER: int = _ON_SEGMENTER
	UNISCRIBE: int = _UNISCRIBE
	CHINESE: int = _CHINESE
