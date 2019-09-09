from ctypes import windll, Structure, c_ubyte, c_uint32, c_void_p, c_int, c_float, POINTER, byref, c_ulong
from ctypes.wintypes import LONG, DWORD, WORD, BOOL
from contextlib import contextmanager

user32=windll.user32
gdi32=windll.gdi32
gdiplus = windll.gdiplus

class RGBQUAD(Structure):
	_fields_=[
		('rgbBlue',c_ubyte),
		('rgbGreen',c_ubyte),
		('rgbRed',c_ubyte),
		('rgbReserved',c_ubyte),
	]

class BITMAPINFOHEADER(Structure):
	_fields_=[
		('biSize',DWORD),
		('biWidth',LONG),
		('biHeight',LONG),
		('biPlanes',WORD),
		('biBitCount',WORD),
		('biCompression',WORD),
		('biSizeImage',DWORD),
		('biXPelsPerMeter',LONG),
		('biYPelsPerMeter',LONG),
		('biClrUsed',DWORD),
		('biClrImportant',DWORD),
	]

class BITMAPINFO(Structure):
	_fields_=[
		('bmiHeader',BITMAPINFOHEADER),
		('bmiColors',(RGBQUAD*1)),
	]

BI_RGB=0
SRCCOPY=0x00CC0020 
DIB_RGB_COLORS=0


class GdiplusStartupInput(Structure):
	_fields_ = [
		('GdiplusVersion', c_uint32),
		('DebugEventCallback', c_void_p),
		('SuppressBackgroundThread', BOOL),
		('SuppressExternalCodecs', BOOL)
	]


class GdiplusStartupOutput(Structure):
	_fields = [
		('NotificationHookProc', c_void_p),
		('NotificationUnhookProc', c_void_p)
	]


gdiplus.GdipCreateFromHDC.argtypes = [c_int, POINTER(c_void_p)]
gdiplus.GdipCreateFromHDC.restype = c_int

gdiplus.GdipCreatePen1.argtypes = [c_int, c_float, c_int, POINTER(c_void_p)]
gdiplus.GdipCreatePen1.restype = c_int

gdiplus.GdipSetPenDashStyle.argtypes = [c_void_p, c_int]
gdiplus.GdipSetPenDashStyle.restype = c_int

gdiplus.GdipDrawLine.argtypes = [c_void_p, c_void_p, c_float, c_float, c_float, c_float]
gdiplus.GdipDrawLine.restype = c_int

gdiplus.GdipDrawRectangle.argtypes = [c_void_p, c_void_p, c_float, c_float, c_float, c_float]
gdiplus.GdipDrawRectangle.restype = c_int

gdiplus.GdipDeletePen.argtypes = [c_void_p]
gdiplus.GdipDeletePen.restype = c_int

gdiplus.GdipDeleteGraphics.argtypes = [c_void_p]
gdiplus.GdipDeleteGraphics.restype = c_int

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
	gdipToken = c_ulong()
	startupInput = GdiplusStartupInput()
	startupInput.GdiplusVersion = 1
	startupOutput = GdiplusStartupOutput()
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
	gpGraphics = c_void_p()
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
	gpPen = c_void_p()
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
	gpStatus = gdiplus.GdipDrawRectangle(gpGraphics, gpPen, float(left), float(top), float(width), float(height))
	if gpStatus:
		raise RuntimeError("GdipDrawRectangle failed with status code %d" % gpStatus)
