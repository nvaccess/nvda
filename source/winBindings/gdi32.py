# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by gdi32.dll, and supporting data structures and enumerations."""

from ctypes import (
	Structure,
	c_ubyte,
	c_int,
	c_void_p,
	POINTER,
	windll,
)
from ctypes.wintypes import (
	BOOL,
	WORD,
	LONG,
	COLORREF,
	DWORD,
	HBITMAP,
	HBRUSH,
	HDC,
	HGDIOBJ,
	LPCWSTR,
	LPVOID,
	UINT,
)


dll = windll.gdi32


GetDeviceCaps = dll.GetDeviceCaps
"""
Retrieves device-specific information for the specified device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdevicecaps
"""
GetDeviceCaps.restype = c_int
GetDeviceCaps.argtypes = (
	HDC,  # hdc: A handle to the DC
	c_int,  # nIndex: The item to be returned
)


CreateCompatibleDC = dll.CreateCompatibleDC
"""
Creates a memory device context (DC) compatible with the specified device.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createcompatibledc
"""
CreateCompatibleDC.restype = HDC
CreateCompatibleDC.argtypes = (
	HDC,  # hdc: A handle to an existing DC
)


CreateCompatibleBitmap = dll.CreateCompatibleBitmap
"""
Creates a bitmap compatible with the device that is associated with the specified device context.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createcompatiblebitmap
"""
CreateCompatibleBitmap.restype = HBITMAP
CreateCompatibleBitmap.argtypes = (
	HDC,  # hdc: A handle to a device context
	c_int,  # cx: The bitmap width, in pixels
	c_int,  # cy: The bitmap height, in pixels
)


SelectObject = dll.SelectObject
"""
Selects an object into the specified device context (DC).

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-selectobject
"""
SelectObject.restype = HGDIOBJ
SelectObject.argtypes = (
	HDC,  # hdc: A handle to the DC
	HGDIOBJ,  # h: A handle to the object to be selected
)


DeleteObject = dll.DeleteObject
"""
Deletes a logical pen, brush, font, bitmap, region, or palette, freeing all system resources associated with the object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deleteobject
"""
DeleteObject.restype = BOOL
DeleteObject.argtypes = (
	HGDIOBJ,  # ho: A handle to a logical pen, brush, font, bitmap, region, or palette
)


DeleteDC = dll.DeleteDC
"""
Deletes the specified device context (DC).

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-deletedc
"""
DeleteDC.restype = BOOL
DeleteDC.argtypes = (
	HDC,  # hdc: A handle to the device context
)


StretchBlt = dll.StretchBlt
"""
Copies a bitmap from a source rectangle into a destination rectangle, stretching or compressing the bitmap to fit the dimensions of the destination rectangle.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-stretchblt
"""
StretchBlt.restype = BOOL
StretchBlt.argtypes = (
	HDC,  # hdcDest: A handle to the destination device context
	c_int,  # xDest: The x-coordinate, in logical units, of the upper-left corner of the destination rectangle
	c_int,  # yDest: The y-coordinate, in logical units, of the upper-left corner of the destination rectangle
	c_int,  # wDest: The width, in logical units, of the destination rectangle
	c_int,  # hDest: The height, in logical units, of the destination rectangle
	HDC,  # hdcSrc: A handle to the source device context
	c_int,  # xSrc: The x-coordinate, in logical units, of the upper-left corner of the source rectangle
	c_int,  # ySrc: The y-coordinate, in logical units, of the upper-left corner of the source rectangle
	c_int,  # wSrc: The width, in logical units, of the source rectangle
	c_int,  # hSrc: The height, in logical units, of the source rectangle
	DWORD,  # rop: The raster operation to be performed
)


class RGBQUAD(Structure):
	"""
	Describes a color consisting of relative intensities of red, green, and blue.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-rgbquad
	"""

	_fields_ = [
		("rgbBlue", c_ubyte),
		("rgbGreen", c_ubyte),
		("rgbRed", c_ubyte),
		("rgbReserved", c_ubyte),
	]


class BITMAPINFOHEADER(Structure):
	"""
	Contains information about the dimensions and color format of a device-independent bitmap (DIB).

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfoheader
	"""

	_fields_ = [
		("biSize", DWORD),
		("biWidth", LONG),
		("biHeight", LONG),
		("biPlanes", WORD),
		("biBitCount", WORD),
		("biCompression", DWORD),
		("biSizeImage", DWORD),
		("biXPelsPerMeter", LONG),
		("biYPelsPerMeter", LONG),
		("biClrUsed", DWORD),
		("biClrImportant", DWORD),
	]


class BITMAPINFO(Structure):
	"""
	Defines the dimensions and color information for a DIB.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/wingdi/ns-wingdi-bitmapinfo
	"""

	_fields_ = [
		("bmiHeader", BITMAPINFOHEADER),
		("bmiColors", (RGBQUAD * 1)),
	]


GetDIBits = dll.GetDIBits
"""
Retrieves the bits of the specified compatible bitmap and copies them into a buffer as a DIB using the specified format.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-getdibits
"""
GetDIBits.restype = c_int
GetDIBits.argtypes = (
	HDC,  # hdc: A handle to the device context
	HBITMAP,  # hbm: A handle to the bitmap
	UINT,  # start: The first scan line to retrieve
	UINT,  # cLines: The number of scan lines to retrieve
	LPVOID,  # lpvBits: A pointer to a buffer to receive the bitmap data
	POINTER(
		BITMAPINFO,
	),  # lpbmi: A pointer to a BITMAPINFO structure that specifies the desired format for the DIB data
	UINT,  # usage: The format of the bmiColors member of the BITMAPINFO structure
)


CreateSolidBrush = dll.CreateSolidBrush
"""
Creates a logical brush that has the specified solid color.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-createsolidbrush
"""
CreateSolidBrush.restype = HBRUSH
CreateSolidBrush.argtypes = (
	COLORREF,  # color: The color of the brush
)


AddFontResourceEx = dll.AddFontResourceExW
"""
Adds the font resource from the specified file to the system.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/wingdi/nf-wingdi-addfontresourceexw
"""
AddFontResourceEx.restype = c_int
AddFontResourceEx.argtypes = (
	LPCWSTR,  # name: A pointer to a null-terminated string that contains a valid font file name
	DWORD,  # fl: The characteristics of the font to be added to the system
	c_void_p,  # res: Reserved. Must be zero
)
