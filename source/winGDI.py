from ctypes import *
from ctypes.wintypes import *

user32=windll.user32
gdi32=windll.gdi32

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
