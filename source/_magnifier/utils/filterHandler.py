# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Filter handler for the magnifier module.

Provides:
- :class:`FilterMatrix` – colour-effect matrices for the fullscreen Magnification API.
- :func:`applyBitmapFilter` – per-pixel filter applied to a GDI bitmap (windowed magnifiers).
- :func:`getBlitRasterOp` – raster-operation code to use when blitting.
"""

import ctypes
import ctypes.wintypes

from enum import Enum
from typing import Callable

import winGDI
import winBindings.gdi32 as gdi32
from winBindings.magnification import MAGCOLOREFFECT

from .types import Filter

_gdi32_dll = ctypes.windll.gdi32
_gdi32_dll.SetDIBits.argtypes = [
	ctypes.wintypes.HDC,
	ctypes.wintypes.HBITMAP,
	ctypes.c_uint,
	ctypes.c_uint,
	ctypes.c_void_p,
	ctypes.c_void_p,
	ctypes.c_uint,
]
_gdi32_dll.SetDIBits.restype = ctypes.c_int


def _createColorEffect(
	matrix: tuple,
) -> MAGCOLOREFFECT:
	"""Create a MAGCOLOREFFECT from a flat matrix tuple."""
	effect = MAGCOLOREFFECT()
	for i in range(5):
		for j in range(5):
			effect.transform[i][j] = matrix[i * 5 + j]
	return effect


class FilterMatrix(Enum):
	NORMAL = _createColorEffect(
		(
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
		),
	)

	GRAYSCALE = _createColorEffect(
		(
			0.33,
			0.33,
			0.33,
			0.0,
			0.0,
			0.59,
			0.59,
			0.59,
			0.0,
			0.0,
			0.11,
			0.11,
			0.11,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
		),
	)

	INVERTED = _createColorEffect(
		(
			-1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			-1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			-1.0,
			0.0,
			0.0,
			0.0,
			0.0,
			0.0,
			1.0,
			0.0,
			1.0,
			1.0,
			1.0,
			0.0,
			1.0,
		),
	)


def applyBitmapFilter(
	filterType: Filter,
	captureDC,
	captureBitmap,
	width: int,
	height: int,
) -> None:
	"""Apply a colour filter to a captured GDI bitmap in-place.

	Filters that require per-pixel manipulation (e.g. grayscale, inverted)
	are applied here.

	:param filterType: The colour filter to apply.
	:param captureDC: The device context that owns *captureBitmap*.
	:param captureBitmap: The bitmap handle to modify.
	:param width: Bitmap width in pixels.
	:param height: Bitmap height in pixels.
	"""
	if filterType == Filter.GRAYSCALE:
		_applyGrayscale(captureDC, captureBitmap, width, height)
	elif filterType == Filter.INVERTED:
		_applyInverted(captureDC, captureBitmap, width, height)


def getBlitRasterOp(filterType: Filter) -> int:
	"""Return the GDI raster-operation code to use when blitting for *filterType*.

	:param filterType: The active colour filter.
	:return: ``SRCCOPY`` – all filters are now applied at bitmap level.
	"""
	return winGDI.SRCCOPY


def _applyDIBTransform(
	captureDC,
	captureBitmap,
	width: int,
	height: int,
	transform: Callable[[bytearray, int], None],
) -> None:
	"""Read a GDI bitmap into a bytearray, apply *transform* to each BGRA pixel, then write it back.

	:param captureDC: Device context owning *captureBitmap*.
	:param captureBitmap: Bitmap handle to modify in-place.
	:param width: Bitmap width in pixels.
	:param height: Bitmap height in pixels.
	:param transform: Callable ``(data, i)`` that modifies ``data[i:i+3]`` (BGR channels)
	                  for the pixel starting at byte offset *i*.  Alpha (``data[i+3]``) is
	                  left unchanged unless the callable explicitly modifies it.
	"""
	numPixels = width * height
	bufferSize = numPixels * 4

	bmInfo = gdi32.BITMAPINFO()
	bmInfo.bmiHeader.biSize = ctypes.sizeof(gdi32.BITMAPINFO)
	bmInfo.bmiHeader.biWidth = width
	bmInfo.bmiHeader.biHeight = -height  # top-down
	bmInfo.bmiHeader.biPlanes = 1
	bmInfo.bmiHeader.biBitCount = 32
	bmInfo.bmiHeader.biCompression = winGDI.BI_RGB

	buffer = (ctypes.c_ubyte * bufferSize)()
	gdi32.GetDIBits(
		captureDC,
		captureBitmap,
		0,
		height,
		buffer,
		ctypes.byref(bmInfo),
		winGDI.DIB_RGB_COLORS,
	)

	data = bytearray(buffer)
	for i in range(0, bufferSize, 4):
		transform(data, i)

	ctypes.memmove(buffer, (ctypes.c_char * bufferSize).from_buffer(data), bufferSize)
	_gdi32_dll.SetDIBits(
		captureDC,
		captureBitmap,
		0,
		height,
		buffer,
		ctypes.byref(bmInfo),
		winGDI.DIB_RGB_COLORS,
	)


def _applyGrayscale(captureDC, captureBitmap, width: int, height: int) -> None:
	"""Convert a GDI bitmap to grayscale (ITU-R BT.601: 77R + 150G + 29B)."""

	def _transform(data: bytearray, i: int) -> None:
		b, g, r = data[i], data[i + 1], data[i + 2]
		gray = (77 * r + 150 * g + 29 * b) >> 8
		data[i] = data[i + 1] = data[i + 2] = gray

	_applyDIBTransform(captureDC, captureBitmap, width, height, _transform)


def _applyInverted(captureDC, captureBitmap, width: int, height: int) -> None:
	"""Invert the colour channels of a GDI bitmap (alpha preserved)."""

	def _transform(data: bytearray, i: int) -> None:
		data[i] = 255 - data[i]
		data[i + 1] = 255 - data[i + 1]
		data[i + 2] = 255 - data[i + 2]

	_applyDIBTransform(captureDC, captureBitmap, width, height, _transform)
