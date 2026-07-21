# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018-2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
from typing import Optional, Any, Callable, Tuple, Union, overload


_FloatInt = Union[int, float]
_Size = Union[Tuple[_FloatInt, _FloatInt], _FloatInt]
_ScaledSize = Union[Tuple[int, int], int]


@overload
def scaleSize(scaleFactor: float, size: tuple[_FloatInt, _FloatInt]) -> tuple[int, int]: ...


@overload
def scaleSize(scaleFactor: float, size: _FloatInt) -> int: ...


def scaleSize(scaleFactor: float, size: _Size) -> _ScaledSize:
	"""Helper method to scale a size using the logical DPI
	@param size: The size (x, y) as a tuple or a single numerical type to scale
	@returns: The scaled size, as a tuple or a single numerical type.
	"""
	if isinstance(size, tuple):
		return (round(scaleFactor * size[0]), round(scaleFactor * size[1]))
	return round(scaleFactor * size)


def getScaleFactor(windowHandle: int) -> int:
	"""Helper method to get the window scale factor. The window needs to be constructed first, in
	order to get the window handle, this likely means calling the wx.window __init__ method prior
	to calling self.GetHandle()"""
	import windowUtils

	return windowUtils.getWindowScalingFactor(windowHandle)


class DpiScalingHelperMixin(object):
	"""mixin to provide size scaling intended to be used with wx.Window (usually wx.Dialog)
	Sub-classes are responsible for calling wx.Window init
	"""

	def __init__(self, windowHandle: int):
		self._scaleFactor = getScaleFactor(windowHandle)

	@overload
	def scaleSize(self, size: tuple[_FloatInt, _FloatInt]) -> tuple[int, int]: ...

	@overload
	def scaleSize(self, size: _FloatInt) -> int: ...

	def scaleSize(self, size: _Size) -> _ScaledSize:
		assert getattr(self, "_scaleFactor", None)
		return scaleSize(self._scaleFactor, size)


class DpiScalingHelperMixinWithoutInit:
	"""Same concept as DpiScalingHelperMixin, but ensures you do not have to explicitly call the init
	of wx.Window or this mixin
	"""

	GetHandle: Callable[[], Any]  # Should be provided by wx.Window
	_scaleFactor: Optional[int] = None

	@overload
	def scaleSize(self, size: tuple[_FloatInt, _FloatInt]) -> tuple[int, int]: ...

	@overload
	def scaleSize(self, size: _FloatInt) -> int: ...

	def scaleSize(self, size: _Size) -> _ScaledSize:
		if self._scaleFactor is None:
			windowHandle = self.GetHandle()
			self._scaleFactor = getScaleFactor(windowHandle)
		return scaleSize(self._scaleFactor, size)
