# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2011-2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""
When working on this file, consider moving to winAPI.
"""

from ctypes import (
	windll,
	POINTER,
	byref,
)
from contextlib import contextmanager
from winBindings import gdiplus
from winBindings import gdi32
from utils import _deprecate

__getattr__ = _deprecate.handleDeprecations(
	_deprecate.MovedSymbol(
		"GdiplusStartupInput",
		"gdiplus",
	),
	_deprecate.MovedSymbol(
		"GdiplusStartupOutput",
		"gdiplus",
	),
	_deprecate.MovedSymbol(
		"RGBQUAD",
		"gdi32",
	),
	_deprecate.MovedSymbol(
		"BITMAPINFOHEADER",
		"gdi32",
	),
	_deprecate.MovedSymbol(
		"BITMAPINFO",
		"gdi32",
	),
)


user32 = windll.user32


BI_RGB = 0
SRCCOPY = 0x00CC0020
DIB_RGB_COLORS = 0



# GDI+ dash style enumeration
DashStyleSolid = 0  # Specifies a solid line.
DashStyleDash = 1  # Specifies a dashed line.
DashStyleDot = 2  # Specifies a dotted line.
DashStyleDashDot = 3  # Specifies an alternating dash-dot line.
DashStyleDashDotDot = 4  # Specifies an alternating dash-dot-dot line.
DashStyleCustom = 5  # Specifies a user-defined, custom dashed line.

# GDI+ unit enumeration
UnitPixel = 2

gdipToken = None


def gdiPlusInitialize():
	global gdipToken
	if gdipToken:
		return  # Already initialized
	gdipToken = gdiplus.ULONG_PTR()
	startupInput = gdiplus.GdiplusStartupInput()
	startupInput.GdiplusVersion = 1
	startupOutput = gdiplus.GdiplusStartupOutput()
	gdiplus.GdiplusStartup(byref(gdipToken), byref(startupInput), byref(startupOutput))


def gdiPlusTerminate():
	global gdipToken
	if not gdipToken:
		return  # Not initialized
	gdiplus.GdiplusShutdown(gdipToken)
	gdipToken = None


@contextmanager
def GDIPlusGraphicsContext(hdc):
	"""Creates a GDI+ graphics context from a device context handle."""
	gpGraphics = POINTER(gdiplus.GpGraphics)()
	gpStatus = gdiplus.GdipCreateFromHDC(hdc, byref(gpGraphics))
	if gpStatus:
		# See https://docs.microsoft.com/en-us/windows/desktop/api/Gdiplustypes/ne-gdiplustypes-status
		# for a list of applicable status codes
		raise RuntimeError("GdipCreateFromHDC failed with status code %d" % gpStatus)
	try:
		yield gpGraphics
	finally:
		gdiplus.GdipDeleteGraphics(gpGraphics)


@contextmanager
def GDIPlusPen(color, width, dashStyle=DashStyleSolid):
	"""Creates a GDI+ pen that is automatically destroyed when finished drawing.
	@param color: an ARGB color.
	@type color: int
	@param width: The width of the pen, in pixels.
	@type width: int
	@param dashStyle: The style of the line(s) to be drawn.
		This is one of the C{DashStyle*} constants.
		Defaults to C{DashStyleSolid}, which draws solid lines.
	@type dashStyle: int
	"""
	gpPen = POINTER(gdiplus.GpPen)()
	gpStatus = gdiplus.GdipCreatePen1(color, width, UnitPixel, byref(gpPen))
	if gpStatus:
		raise RuntimeError("GdipCreatePen1 failed with status code %d" % gpStatus)
	gpStatus = gdiplus.GdipSetPenDashStyle(gpPen, dashStyle)
	if gpStatus:
		raise RuntimeError("GdipSetPenDashStyle failed with status code %d" % gpStatus)
	try:
		yield gpPen
	finally:
		gdiplus.GdipDeletePen(gpPen)


def gdiPlusDrawRectangle(gpGraphics, gpPen, left, top, width, height):
	gpStatus = gdiplus.GdipDrawRectangle(
		gpGraphics,
		gpPen,
		float(left),
		float(top),
		float(width),
		float(height),
	)
	if gpStatus:
		raise RuntimeError("GdipDrawRectangle failed with status code %d" % gpStatus)
