# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Windows Graphics Capture support for content recognition."""

import ctypes
from ctypes import POINTER, cast

from NVDAHelper.localWin10 import _wgcCapture_captureScreenRegion, _wgcCapture_isSupported
import watchdog
from winBindings.gdi32 import RGBQUAD

from . import RecogImageInfo


def isSupported() -> bool:
	"""Return whether Windows Graphics Capture can be used for content recognition."""
	return bool(_wgcCapture_isSupported())


def _captureScreenRegion(imageInfo: RecogImageInfo, buffer: ctypes.Array) -> bool:
	return bool(
		_wgcCapture_captureScreenRegion(
			imageInfo.screenLeft,
			imageInfo.screenTop,
			imageInfo.screenWidth,
			imageInfo.screenHeight,
			cast(buffer, POINTER(RGBQUAD)),
			imageInfo.recogWidth,
			imageInfo.recogHeight,
		),
	)


def captureImage(imageInfo: RecogImageInfo) -> ctypes.Array:
	"""Capture the specified screen region using Windows Graphics Capture."""
	buffer = (RGBQUAD * imageInfo.recogWidth * imageInfo.recogHeight)()
	captureSucceeded = watchdog.cancellableExecute(_captureScreenRegion, imageInfo, buffer)
	if not captureSucceeded:
		raise RuntimeError(
			"Windows Graphics Capture failed for region "
			f"{imageInfo.screenLeft}, {imageInfo.screenTop}, "
			f"{imageInfo.screenWidth}, {imageInfo.screenHeight}",
		)
	return buffer
