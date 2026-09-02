# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Lightweight capture sizing rules shared by the NVDA integration and tests."""

_SMALL_OBJECT_EDGE = 100
_MAX_RESIZE_FACTOR = 4.0
# Both bundled model profiles use this detector input limit. Keeping capture
# scaling within it avoids creating pixels which the worker would immediately
# downscale again.
_DETECTOR_MAX_SIDE = 1280
_MAX_CAPTURE_SIDE = 16384
_MAX_CAPTURE_PIXELS = 7680 * 4320


def getAdaptiveResizeFactor(width: int, height: int) -> int | float:
	"""Upscale only small captures, without exceeding the detector input limit."""
	if type(width) is not int or type(height) is not int or width <= 0 or height <= 0:
		return 1
	if width >= _SMALL_OBJECT_EDGE and height >= _SMALL_OBJECT_EDGE:
		return 1
	factor = min(
		_MAX_RESIZE_FACTOR,
		_DETECTOR_MAX_SIDE / width,
		_DETECTOR_MAX_SIDE / height,
	)
	return max(1, factor)


def isCaptureSizeSupported(width: int, height: int) -> bool:
	"""Reject pathological captures before NVDA allocates their BGRA buffers."""
	return (
		type(width) is int
		and type(height) is int
		and width > 0
		and height > 0
		and width <= _MAX_CAPTURE_SIDE
		and height <= _MAX_CAPTURE_SIDE
		and width * height <= _MAX_CAPTURE_PIXELS
	)
