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
