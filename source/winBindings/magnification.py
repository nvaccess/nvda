# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by magnification.dll, and supporting data structures and enumerations."""

from ctypes import POINTER, WINFUNCTYPE, Structure, WinError, c_float, windll
from ctypes.wintypes import BOOL
from _ctypes import CFuncPtr
from typing import Any

dll = windll.Magnification


class MAGCOLOREFFECT(Structure):
	"""
	Describes a color transformation matrix that a magnifier control uses to apply a color effect to magnified screen content.

	.. seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/magnification/ns-magnification-magcoloreffect
	"""

	_fields_ = (("transform", c_float * 5 * 5),)


PMAGCOLOREFFECT = POINTER(MAGCOLOREFFECT)


def _errCheck[T: tuple[Any]](result: int, func: CFuncPtr, args: T) -> T:
	if result == 0:
		raise WinError()
	return args


MagSetFullscreenColorEffect = WINFUNCTYPE(BOOL, PMAGCOLOREFFECT)(
	("MagSetFullscreenColorEffect", dll),
	((1, "pEffect"),),
)
"""
Changes the color transformation matrix associated with the full-screen magnifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-magsetfullscreencoloreffect
"""
MagSetFullscreenColorEffect.errcheck = _errCheck

MagGetFullscreenColorEffect = WINFUNCTYPE(BOOL, PMAGCOLOREFFECT)(
	("MagGetFullscreenColorEffect", dll),
	((2, "effect"),),
)
"""
Retrieves the color transformation matrix associated with the full-screen magnifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-maggetfullscreencoloreffect
"""
MagGetFullscreenColorEffect.errcheck = _errCheck

MagShowSystemCursor = WINFUNCTYPE(BOOL, BOOL)(
	("MagShowSystemCursor", dll),
	((1, "showCursor"),),
)
"""
Shows or hides the system cursor.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-magshowsystemcursor
"""
MagShowSystemCursor.errcheck = _errCheck

MagInitialize = WINFUNCTYPE(BOOL)(("MagInitialize", dll))
"""
Creates and initializes the magnifier run-time objects.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-maginitialize
"""
MagInitialize.errcheck = _errCheck

MagUninitialize = WINFUNCTYPE(BOOL)(("MagUninitialize", dll))
"""
Destroys the magnifier run-time objects.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-maguninitialize
"""
MagUninitialize.errcheck = _errCheck
