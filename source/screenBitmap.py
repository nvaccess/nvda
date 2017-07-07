#screenBitmap.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2011-2017 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Functionality to capture and work with bitmaps of the screen.
"""

import ctypes
import winGDI

user32=ctypes.windll.user32
gdi32=ctypes.windll.gdi32

class ScreenBitmap(object):
	"""Provides a way to capture a bitmap of any part of the screen. The object caches needed DCs and bitmaps therefore an instance of an object only handles one size of bitmap."""

	def __init__(self,width,height):
		"""
		@param width: the width of the resulting bitmap in rgb pixels.
		@param height: the height of the bitmap in rgb pixels.
		"""
		self.width=width
		self.height=height
		#Fetch the device context for the screen
		self._screenDC=user32.GetDC(0)
		#Create a memory device context with which we can copy screen content to on request.
		self._memDC=gdi32.CreateCompatibleDC(self._screenDC)
		#Create a new bitmap of the chosen size, and set this as the memory device context's bitmap, so that what is drawn is captured.
		self._memBitmap=gdi32.CreateCompatibleBitmap(self._screenDC,width,height)
		self._oldBitmap=gdi32.SelectObject(self._memDC,self._memBitmap)
		#We always want standard RGB data
		bmInfo=winGDI.BITMAPINFO()
		bmInfo.bmiHeader.biSize=ctypes.sizeof(bmInfo)
		bmInfo.bmiHeader.biWidth=width
		bmInfo.bmiHeader.biHeight=height*-1
		bmInfo.bmiHeader.biPlanes=1
		bmInfo.bmiHeader.biBitCount=32
		bmInfo.bmiHeader.biCompression=winGDI.BI_RGB
		self._bmInfo=bmInfo

	def __del__(self):
		gdi32.SelectObject(self._memDC,self._oldBitmap)
		gdi32.DeleteObject(self._memBitmap)
		gdi32.DeleteDC(self._memDC)
		user32.ReleaseDC(0,self._screenDC)

	def captureImage(self,x,y,w,h):
		"""
		Captures the part of the screen starting at x,y and extends by w (width) and h (height), and stretches/shrinks it to fit in to the object's bitmap size.
		"""
	#Copy the requested content from the screen in to our memory device context, stretching/shrinking its size to fit.
		gdi32.StretchBlt(self._memDC,0,0,self.width,self.height,self._screenDC,x,y,w,h,winGDI.SRCCOPY)
		#Fetch the pixels from our memory bitmap and store them in a buffer to be returned
		buffer=(winGDI.RGBQUAD*self.width*self.height)()
		gdi32.GetDIBits(self._memDC,self._memBitmap,0,self.height,buffer,ctypes.byref(self._bmInfo),winGDI.DIB_RGB_COLORS)
		return buffer

def rgbPixelBrightness(p):
	"""Converts a RGBQUAD pixel in to  one grey-scale brightness value."""
	return int((0.3*p.rgbBlue)+(0.59*p.rgbGreen)+(0.11*p.rgbRed))
