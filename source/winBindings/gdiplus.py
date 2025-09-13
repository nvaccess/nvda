# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Functions exported by gdiplus.dll, and supporting data structures and enumerations."""

from ctypes import (
	Structure,
	c_float,
	c_int,
	c_uint32,
	c_void_p,
	POINTER,
	windll,
	c_size_t,
)
from ctypes.wintypes import (
	BOOL,
	DWORD,
	HDC,
)


ULONG_PTR = c_size_t
ARGB = DWORD
REAL = c_float
GpUnit = c_int
GpStatus = c_int
GpPen = c_void_p
GpGraphics = c_void_p
GpDashStyle = c_int


dll = windll.gdiplus


class GdiplusStartupInput(Structure):
	"""
	Holds a block of arguments that are required by the GdiplusStartup function.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/gdiplusinit/ns-gdiplusinit-gdiplusstartupinput
	"""

	_fields_ = [
		("GdiplusVersion", c_uint32),
		("DebugEventCallback", c_void_p),
		("SuppressBackgroundThread", BOOL),
		("SuppressExternalCodecs", BOOL),
	]


class GdiplusStartupOutput(Structure):
	"""
	Stores a pointer to a hook function and a pointer to an unhook function as returned by GdiplusStartup.

	..seealso::
		https://learn.microsoft.com/en-us/windows/win32/api/gdiplusinit/ns-gdiplusinit-GdiplusStartupOutput
	"""

	_fields_ = [
		("NotificationHookProc", c_void_p),
		("NotificationUnhookProc", c_void_p),
	]


GdiplusStartup = dll.GdiplusStartup
"""
Initializes Windows GDI+.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdiplusinit/nf-gdiplusinit-gdiplusstartup
"""
GdiplusStartup.restype = c_int
GdiplusStartup.argtypes = (
	POINTER(ULONG_PTR),  # token: A pointer to a ULONG_PTR that receives a token
	POINTER(GdiplusStartupInput),  # input: A pointer to a GdiplusStartupInput structure
	POINTER(GdiplusStartupOutput),  # output: A pointer to a GdiplusStartupOutput structure
)


GdiplusShutdown = dll.GdiplusShutdown
"""
Cleans up resources used by Windows GDI+.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdiplusinit/nf-gdiplusinit-gdiplusshutdown
"""
GdiplusShutdown.restype = None
GdiplusShutdown.argtypes = (
	ULONG_PTR,  # token: A token that was returned by a previous call to GdiplusStartup
)


GdipCreateFromHDC = dll.GdipCreateFromHDC
"""
Creates a Graphics object that is associated with a specified device context.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdiplusgraphics/nf-gdiplusgraphics-graphics-graphics(inhdc)
"""
GdipCreateFromHDC.restype = GpStatus
GdipCreateFromHDC.argtypes = (
	HDC,  # hdc: Handle to a device context
	POINTER(
		POINTER(GpGraphics),
	),  # graphics: Pointer to a variable that receives a pointer to the new Graphics object
)


GdipCreatePen1 = dll.GdipCreatePen1
"""
Creates a Pen object that has specified color, width, and style.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdipluspen/nf-gdipluspen-pen-pen(inconstcolor__inreal__inunit)
"""
GdipCreatePen1.restype = GpStatus
GdipCreatePen1.argtypes = (
	ARGB,  # color: ARGB color
	REAL,  # width: Width of the pen
	GpUnit,  # unit: Unit of measure for the pen width
	POINTER(POINTER(GpPen)),  # pen: Pointer to a variable that receives a pointer to the new Pen object
)


GdipSetPenDashStyle = dll.GdipSetPenDashStyle
"""
Sets the dash style of a Pen object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdipluspen/nf-gdipluspen-pen-setdashstyle
"""
GdipSetPenDashStyle.restype = GpStatus
GdipSetPenDashStyle.argtypes = (
	POINTER(GpPen),  # pen: Pointer to the Pen object
	GpDashStyle,  # dashStyle: Element of the DashStyle enumeration
)


GdipDrawLine = dll.GdipDrawLine
"""
Draws a line.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdiplusgraphics/nf-gdiplusgraphics-graphics-drawline(inconstpen_inreal_inreal_inreal_inreal)
"""
GdipDrawLine.restype = GpStatus
GdipDrawLine.argtypes = (
	POINTER(GpGraphics),  # graphics: Pointer to the Graphics object
	POINTER(GpPen),  # pen: Pointer to a pen that is used to draw the line
	REAL,  # x1: x-coordinate of the starting point of the line
	REAL,  # y1: y-coordinate of the starting point of the line
	REAL,  # x2: x-coordinate of the ending point of the line
	REAL,  # y2: y-coordinate of the ending point of the line
)


GdipDrawRectangle = dll.GdipDrawRectangle
"""
Draws a rectangle.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdiplusgraphics/nf-gdiplusgraphics-graphics-drawrectangle(inconstpen_inreal_inreal_inreal_inreal)
"""
GdipDrawRectangle.restype = GpStatus
GdipDrawRectangle.argtypes = (
	POINTER(GpGraphics),  # graphics: Pointer to the Graphics object
	POINTER(GpPen),  # pen: Pointer to a pen that is used to draw the rectangle
	REAL,  # x: x-coordinate of the upper-left corner of the rectangle
	REAL,  # y: y-coordinate of the upper-left corner of the rectangle
	REAL,  # width: Width of the rectangle
	REAL,  # height: Height of the rectangle
)


GdipDeletePen = dll.GdipDeletePen
"""
Deletes a Pen object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdipluspen/nf-gdipluspen-pen-pen
"""
GdipDeletePen.restype = GpStatus
GdipDeletePen.argtypes = (
	POINTER(GpPen),  # pen: Pointer to the Pen object to be deleted
)


GdipDeleteGraphics = dll.GdipDeleteGraphics
"""
Deletes a Graphics object.

.. seealso::
	https://learn.microsoft.com/en-us/windows/win32/api/gdiplusgraphics/nf-gdiplusgraphics-graphics-graphics
"""
GdipDeleteGraphics.restype = GpStatus
GdipDeleteGraphics.argtypes = (
	POINTER(GpGraphics),  # graphics: Pointer to the Graphics object to be deleted
)
