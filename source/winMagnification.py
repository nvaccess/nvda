#winMagnification.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018-2019 NV Access Limited, Babbage B.V., Leonard de Ruijter

"""Wrapper for the windows magnification library (magnification.dll)
"""

from ctypes import Structure, windll, byref, c_int, c_float, POINTER, WINFUNCTYPE, WinError
from ctypes.wintypes import BOOL, HWND, RECT, DWORD
from comtypes import GUID

MS_SHOWMAGNIFIEDCURSOR = 0x0001
MS_CLIPAROUNDCURSOR =	0x0002
MS_INVERTCOLORS =  0x0004
MW_FILTERMODE_EXCLUDE = 0
MW_FILTERMODE_INCLUDE = 1

class MAGTRANSFORM(Structure):
	_fields_ = (("v", c_float*3*3),)

	@classmethod
	def fromMagLevel(cls, level):
		return cls((
			(level, 0.0, 0.0),
			(0.0, level, 0.0),
			(0.0, 0.0, 1.0)
		))

	def toMagLevel(self):
		assert self.v[0][0] == self.v[1][1], "Unsuported MAGTRANSFORM instance for toMagLevel"
		return self.v[0][0]

class MAGCOLOREFFECT(Structure):
	_fields_ = (("transform", c_float*5*5),)

def errCheck(result, func, args):
	if result == 0:
		raise WinError()
	return args

magnification = windll.magnification

# Prototype declarations
MagInitializeFuncType = WINFUNCTYPE(BOOL)
MagUninitializeFuncType = WINFUNCTYPE(BOOL)
MagSetWindowSourceFuncType = WINFUNCTYPE(BOOL, HWND, RECT)
MagSetWindowSourceArgTypes = ((1, "hwnd"), (1, "rect"))
MagGetWindowSourceFuncType = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
MagGetWindowSourceArgTypes = ((1, "hwnd"), (2, "rect"))
MagSetWindowTransformFuncType = WINFUNCTYPE(BOOL, HWND, POINTER(MAGTRANSFORM))
MagSetWindowTransformArgTypes = ((1, "hwnd"), (1, "transform"))
MagGetWindowTransformFuncType = WINFUNCTYPE(BOOL, HWND, POINTER(MAGTRANSFORM))
MagGetWindowTransformArgTypes = ((1, "hwnd"), (2, "transform"))
MagSetWindowFilterListFuncType = WINFUNCTYPE(BOOL, HWND, DWORD, c_int, POINTER(HWND))
MagGetWindowFilterListFuncType = WINFUNCTYPE(c_int, HWND, POINTER(DWORD), c_int, POINTER(HWND))
MagSetColorEffectFuncType = WINFUNCTYPE(BOOL, HWND, POINTER(MAGCOLOREFFECT))
MagSetColorEffectArgTypes = ((1, "hwnd"), (1, "effect"))
MagGetColorEffectFuncType = WINFUNCTYPE(BOOL, HWND, POINTER(MAGCOLOREFFECT))
MagGetColorEffectArgTypes = ((1, "hwnd"), (2, "effect"))
MagSetFullscreenTransformFuncType = WINFUNCTYPE(BOOL, c_float, c_int, c_int)
MagSetFullscreenTransformArgTypes = ((1, "magLevel"), (1, "xOffset"), (1, "yOffset"))
MagGetFullscreenTransformFuncType = WINFUNCTYPE(BOOL, POINTER(c_float), POINTER(c_int), POINTER(c_int))
MagGetFullscreenTransformArgTypes = ((2, "magLevel"), (2, "xOffset"), (2, "yOffset"))
MagSetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
MagSetFullscreenColorEffectArgTypes = ((1, "effect"),)
MagGetFullscreenColorEffectFuncType = WINFUNCTYPE(BOOL, POINTER(MAGCOLOREFFECT))
MagGetFullscreenColorEffectArgTypes = ((2, "effect"),)
MagSetInputTransformFuncType = WINFUNCTYPE(BOOL, BOOL, POINTER(RECT), POINTER(RECT))
MagGetInputTransformFuncType = WINFUNCTYPE(BOOL, POINTER(BOOL), POINTER(RECT), POINTER(RECT))
MagShowSystemCursorFuncType = WINFUNCTYPE(BOOL, BOOL)
MagShowSystemCursorArgTypes = ((1, "showCursor"),)
MagSetLensUseBitmapSmoothingFuncType = WINFUNCTYPE(BOOL, HWND, BOOL)
MagSetLensUseBitmapSmoothingArgTypes = ((1, "hwnd"), (1, "useSmoothing"))
MagSetFullscreenUseBitmapSmoothingFuncType = WINFUNCTYPE(BOOL, BOOL)
MagSetFullscreenUseBitmapSmoothingArgTypes = ((1, "useSmoothing"),)

MagInitialize = MagInitializeFuncType(("MagInitialize", magnification))
MagInitialize.errcheck = errCheck
MagUninitialize = MagUninitializeFuncType(("MagUninitialize", magnification))
MagUninitialize.errcheck = errCheck
MagSetWindowSource = MagSetWindowSourceFuncType(("MagSetWindowSource", magnification), MagSetWindowSourceArgTypes)
MagSetWindowSource.errcheck = errCheck
MagGetWindowSource = MagGetWindowSourceFuncType(("MagGetWindowSource", magnification), MagGetWindowSourceArgTypes)
MagGetWindowSource.errcheck = errCheck
MagSetWindowTransform = MagSetWindowTransformFuncType(("MagSetWindowTransform", magnification), )
MagSetWindowTransform.errcheck = errCheck
MagGetWindowTransform = MagGetWindowTransformFuncType(("MagGetWindowTransform", magnification), MagGetWindowTransformArgTypes)
MagGetWindowTransform.errcheck = errCheck
MagSetColorEffect = MagSetColorEffectFuncType(("MagSetColorEffect", magnification), MagSetColorEffectArgTypes)
MagSetColorEffect.errcheck = errCheck
MagGetColorEffect = MagGetColorEffectFuncType(("MagGetColorEffect", magnification), MagGetColorEffectArgTypes)
MagGetColorEffect.errcheck = errCheck
MagSetFullscreenTransform = MagSetFullscreenTransformFuncType(("MagSetFullscreenTransform", magnification), MagSetFullscreenTransformArgTypes)
MagSetFullscreenTransform.errcheck = errCheck
MagGetFullscreenTransform = MagGetFullscreenTransformFuncType(("MagGetFullscreenTransform", magnification), MagGetFullscreenTransformArgTypes)
MagGetFullscreenTransform.errcheck = errCheck
MagSetFullscreenColorEffect = MagSetFullscreenColorEffectFuncType(("MagSetFullscreenColorEffect", magnification), MagSetFullscreenColorEffectArgTypes )
MagSetFullscreenColorEffect.errcheck = errCheck
MagGetFullscreenColorEffect = MagGetFullscreenColorEffectFuncType(("MagGetFullscreenColorEffect", magnification), MagGetFullscreenColorEffectArgTypes)
MagGetFullscreenColorEffect.errcheck = errCheck
MagShowSystemCursor = MagShowSystemCursorFuncType(("MagShowSystemCursor", magnification), MagShowSystemCursorArgTypes)
MagShowSystemCursor.errcheck = errCheck
try:
	MagSetFullscreenUseBitmapSmoothing = MagSetFullscreenUseBitmapSmoothingFuncType(("MagSetFullscreenUseBitmapSmoothing", magnification), MagSetFullscreenUseBitmapSmoothingArgTypes)
	MagSetFullscreenUseBitmapSmoothing.errcheck = errCheck
except AttributeError:
	def MagSetFullscreenUseBitmapSmoothing(HWND, useSmoothing):
		raise NotImplementedError
try:
	MagSetLensUseBitmapSmoothing = MagSetLensUseBitmapSmoothingFuncType(("MagSetLensUseBitmapSmoothing", magnification), MagSetLensUseBitmapSmoothingArgTypes)
	MagSetLensUseBitmapSmoothing.errcheck = errCheck
except AttributeError:
	def MagSetLensUseBitmapSmoothing(useSmoothing):
		raise NotImplementedError
