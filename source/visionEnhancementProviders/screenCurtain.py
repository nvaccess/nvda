# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Screen curtain implementation based on the windows magnification API.
This implementation only works on Windows 8 and above.
"""

import vision
import winVersion
from ctypes import Structure, windll, c_float, POINTER, WINFUNCTYPE, WinError
from ctypes.wintypes import BOOL


class MAGCOLOREFFECT(Structure):
	_fields_ = (("transform", c_float * 5 * 5),)


TRANSFORM_BLACK = MAGCOLOREFFECT()
TRANSFORM_BLACK.transform[4][4] = 1.0


def _errCheck(result, func, args):
	if result == 0:
		raise WinError()
	return args


class Magnification:
	"""Static class that wraps necessary functions from the Windows magnification API."""

	_magnification = windll.Magnification

	_MagInitializeFuncType = WINFUNCTYPE(BOOL)
	_MagUninitializeFuncType = WINFUNCTYPE(BOOL)
	_MagSetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
	_MagSetFullscreenColorEffectArgTypes = ((1, "effect"),)
	_MagGetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
	_MagGetFullscreenColorEffectArgTypes = ((2, "effect"),)
	_MagShowSystemCursorFuncType = WINFUNCTYPE(BOOL, BOOL)
	_MagShowSystemCursorArgTypes = ((1, "showCursor"),)

	MagInitialize = _MagInitializeFuncType(("MagInitialize", _magnification))
	MagInitialize.errcheck = _errCheck
	MagUninitialize = _MagUninitializeFuncType(("MagUninitialize", _magnification))
	MagUninitialize.errcheck = _errCheck
	try:
		MagSetFullscreenColorEffect = _MagSetFullscreenColorEffectFuncType(
			("MagSetFullscreenColorEffect", _magnification),
			_MagSetFullscreenColorEffectArgTypes
		)
		MagSetFullscreenColorEffect.errcheck = _errCheck
		MagGetFullscreenColorEffect = _MagGetFullscreenColorEffectFuncType(
			("MagGetFullscreenColorEffect", _magnification),
			_MagGetFullscreenColorEffectArgTypes
		)
		MagGetFullscreenColorEffect.errcheck = _errCheck
	except AttributeError:
		MagSetFullscreenColorEffect = None
		MagGetFullscreenColorEffect = None
	MagShowSystemCursor = _MagShowSystemCursorFuncType(
		("MagShowSystemCursor", _magnification),
		_MagShowSystemCursorArgTypes
	)
	MagShowSystemCursor.errcheck = _errCheck


class VisionEnhancementProvider(vision.providerBase.VisionEnhancementProvider):
	name = "screenCurtain"
	# Translators: Description of a vision enhancement provider that disables output to the screen,
	# making it black.
	description = _("Screen Curtain")
	supportedRoles = frozenset([vision.constants.Role.COLORENHANCER])

	@classmethod
	def canStart(cls):
		return winVersion.isFullScreenMagnificationAvailable()

	def __init__(self):
		super(VisionEnhancementProvider, self).__init__()
		Magnification.MagInitialize()
		Magnification.MagShowSystemCursor(False)
		Magnification.MagSetFullscreenColorEffect(TRANSFORM_BLACK)

	def terminate(self):
		super(VisionEnhancementProvider, self).terminate()
		Magnification.MagShowSystemCursor(True)
		Magnification.MagUninitialize()

	def registerEventExtensionPoints(self, extensionPoints):
		# The screen curtain isn't interested in any events
		pass
