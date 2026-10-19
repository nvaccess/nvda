# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by magnification.dll, and supporting data structures and enumerations.

When the Magnification API is unavailable, function bindings raise :class:`OSError`.
"""

from ctypes import POINTER, WINFUNCTYPE, Structure, WinError, c_float, c_int, windll  # noqa: I001
from ctypes.wintypes import BOOL, LPRECT
from _ctypes import CFuncPtr
from typing import Any

try:
	dll = windll.Magnification
except (AttributeError, OSError) as e:
	dll = None
	MAGNIFICATION_LOAD_ERROR: Exception | None = e
else:
	MAGNIFICATION_LOAD_ERROR = None

MAGNIFICATION_AVAILABLE: bool = dll is not None
"""True if the Windows Magnification API is available."""


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


def _unavailable(*args: Any, **kwargs: Any) -> None:
	raise OSError("The Magnification API is not available")


def _bind(name: str, prototype: Any, paramFlags: tuple[Any, ...] | None = None) -> Any:
	if dll is None:
		return _unavailable
	function = prototype((name, dll), paramFlags) if paramFlags is not None else prototype((name, dll))
	function.errcheck = _errCheck
	return function


MagSetFullscreenColorEffect = _bind(
	"MagSetFullscreenColorEffect",
	WINFUNCTYPE(BOOL, PMAGCOLOREFFECT),
	((1, "pEffect"),),
)
"""
Changes the color transformation matrix associated with the full-screen magnifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-magsetfullscreencoloreffect
"""

MagGetFullscreenColorEffect = _bind(
	"MagGetFullscreenColorEffect",
	WINFUNCTYPE(BOOL, PMAGCOLOREFFECT),
	((2, "effect"),),
)
"""
Retrieves the color transformation matrix associated with the full-screen magnifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-maggetfullscreencoloreffect
"""

MagShowSystemCursor = _bind(
	"MagShowSystemCursor",
	WINFUNCTYPE(BOOL, BOOL),
	((1, "showCursor"),),
)
"""
Shows or hides the system cursor.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-magshowsystemcursor
"""

MagInitialize = _bind("MagInitialize", WINFUNCTYPE(BOOL))
"""
Creates and initializes the magnifier run-time objects.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-maginitialize
"""

MagUninitialize = _bind("MagUninitialize", WINFUNCTYPE(BOOL))
"""
Destroys the magnifier run-time objects.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-maguninitialize
"""

MagSetFullscreenTransform = _bind(
	"MagSetFullscreenTransform",
	WINFUNCTYPE(BOOL, c_float, c_int, c_int),
	((1, "magLevel"), (1, "xOffset"), (1, "yOffset")),
)
"""
Sets the magnification settings for the full-screen magnifier.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-magsetfullscreentransform
"""

MagSetInputTransform = _bind(
	"MagSetInputTransform",
	WINFUNCTYPE(BOOL, BOOL, LPRECT, LPRECT),
	((1, "fEnabled"), (1, "pRectSource"), (1, "pRectDest")),
)
"""
Sets the mapping between magnified coordinates and screen coordinates for pen and touch input.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/magnification/nf-magnification-magsetinputtransform
"""
