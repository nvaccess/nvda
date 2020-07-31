# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2018 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
from typing import Optional, Any, Callable


def scaleSize(scaleFactor, size):
	"""Helper method to scale a size using the logical DPI
	@param size: The size (x,y) as a tuple or a single numerical type to scale
	@returns: The scaled size, returned as the same type"""
	if isinstance(size, tuple):
		return (scaleFactor * size[0], scaleFactor * size[1])
	return scaleFactor * size

def getScaleFactor(windowHandle):
	"""Helper method to get the window scale factor. The window needs to be constructed first, in
	order to get the window handle, this likely means calling the wx.window __init__ method prior
	to calling self.GetHandle()"""
	import windowUtils
	return windowUtils.getWindowScalingFactor(windowHandle)


class DpiScalingHelperMixin(object):
	""" mixin to provide size scaling intended to be used with wx.Window (usually wx.Dialog)
			Sub-classes are responsible for calling wx.Window init
	"""

	def __init__(self, windowHandle):
		self._scaleFactor = getScaleFactor(windowHandle)

	def scaleSize(self, size):
		assert getattr(self, u"_scaleFactor", None)
		return scaleSize(self._scaleFactor, size)


class DpiScalingHelperMixinWithoutInit:
	"""Same concept as DpiScalingHelperMixin, but ensures you do not have to explicitly call the init
		of wx.Window or this mixin
	"""
	GetHandle: Callable[[], Any]  # Should be provided by wx.Window
	_scaleFactor: Optional[float] = None

	def scaleSize(self, size):
		if self._scaleFactor is None:
			windowHandle = self.GetHandle()
			self._scaleFactor = getScaleFactor(windowHandle)
		return scaleSize(self._scaleFactor, size)
