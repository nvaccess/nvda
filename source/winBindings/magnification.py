# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by magnification.dll, and supporting data structures and enumerations."""

from ctypes import POINTER, WINFUNCTYPE, Structure, WinError, c_float, windll
from ctypes.wintypes import BOOL


class MAGCOLOREFFECT(Structure):
	_fields_ = (("transform", c_float * 5 * 5),)


def _errCheck(result, func, args):
	if result == 0:
		raise WinError()
	return args


_magnification = windll.Magnification
# Set full screen color effect
_MagSetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
_MagSetFullscreenColorEffectArgTypes = ((1, "effect"),)
MagSetFullscreenColorEffect = _MagSetFullscreenColorEffectFuncType(
	("MagSetFullscreenColorEffect", _magnification),
	_MagSetFullscreenColorEffectArgTypes,
)
MagSetFullscreenColorEffect.errcheck = _errCheck

# Get full screen color effect
_MagGetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
_MagGetFullscreenColorEffectArgTypes = ((2, "effect"),)
MagGetFullscreenColorEffect = _MagGetFullscreenColorEffectFuncType(
	("MagGetFullscreenColorEffect", _magnification),
	_MagGetFullscreenColorEffectArgTypes,
)
MagGetFullscreenColorEffect.errcheck = _errCheck

# show system cursor
_MagShowSystemCursorFuncType = WINFUNCTYPE(BOOL, BOOL)
_MagShowSystemCursorArgTypes = ((1, "showCursor"),)
MagShowSystemCursor = _MagShowSystemCursorFuncType(
	("MagShowSystemCursor", _magnification),
	_MagShowSystemCursorArgTypes,
)
MagShowSystemCursor.errcheck = _errCheck

# initialize
_MagInitializeFuncType = WINFUNCTYPE(BOOL)
MagInitialize = _MagInitializeFuncType(("MagInitialize", _magnification))
MagInitialize.errcheck = _errCheck

# uninitialize
_MagUninitializeFuncType = WINFUNCTYPE(BOOL)
MagUninitialize = _MagUninitializeFuncType(("MagUninitialize", _magnification))
MagUninitialize.errcheck = _errCheck
