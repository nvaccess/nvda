#colors.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from collections import namedtuple
import math
from ctypes.wintypes import COLORREF
import re

class RGB(namedtuple('RGB',('red','green','blue'))):
	"""Represents a color as an RGB (red green blue) value"""

	@classmethod
	def fromCOLORREF(cls,c):
		"""factory method to create an RGB from a COLORREF ctypes instance"""
		if isinstance(c,COLORREF):
			c=c.value
		return cls(c&0xff,(c>>8)&0xff,(c>>16)&0xff)

	_re_RGBFunctionString=re.compile(r'rgb\(\s*(\d+%?)\s*,\s*(\d+%?)\s*,\s*(\d+%?)\s*\)',re.I)
	_re_RGBAFunctionString=re.compile(r'rgba\(\s*(\d+%?)\s*,\s*(\d+%?)\s*,\s*(\d+%?)\s*,\s*\d+(\.\d+)?\s*\)',re.I)

	@staticmethod
	def _RGBStringValToInt(s):
		val=int(round(int(s[:-1])*2.55)) if s.endswith('%') else int(s)
		if val<0 or val>255:
			raise ValueError("%s out of range"%val)
		return val

	@classmethod
	def fromString(cls,s):
		"""
		Factory method to create an RGB instance from a css RGB string representation.
		"""
		s=s.strip()
		#Try to match on the form RGB(x,y,z)
		m=cls._re_RGBFunctionString.match(s) or cls._re_RGBAFunctionString.match(s)
		if m:
			r=cls._RGBStringValToInt(m.group(1))
			g=cls._RGBStringValToInt(m.group(2))
			b=cls._RGBStringValToInt(m.group(3))
			return RGB(r,g,b)
		if s.startswith('#'):
			sLen=len(s)
			try:
				val=int(s[1:],16)
			except ValueError:
				val=None
			if val is not None:
				#Perhaps its a #aarrggbb or #rrggbb hex string
				if sLen==7 or sLen==9:
					r=(val>>16)&0xff
					g=(val>>8)&0xff
					b=val&0xff
					return RGB(r,g,b)
				#Perhaps its a #argb or #rgb hex string
				if sLen==4 or sLen==5:
					r=((val>>8)&0xf)+(((val>>8)&0xf)<<4)
					g=((val>>4)&0xf)+(((val>>4)&0xf)<<4)
					b=(val&0xf)+((val&0xf)<<4)
					return RGB(r,g,b)
		raise ValueError("invalid RGB string: %s"%s)

	@property
	def name(self):
		foundName=RGBToNames.get(self,None)
		if not foundName:
			closestRGB=sorted(RGBToNames.iterkeys(),key=lambda x: math.sqrt((abs(self.red-x.red)*0.3)**2+(abs(self.green-x.green)*0.59)**2+(abs(self.blue-x.blue)*0.11)**2))[0]
			foundName=RGBToNames[closestRGB]
			RGBToNames[self]=foundName
		return foundName

RGBToNames={
	#Standard 16 HTML 4 colors
	RGB(0x00,0x00,0x00):_('black'),
	RGB(0x00,0x80,0x00):_('green'),
	RGB(0xc0,0xc0,0xc0):_('light grey'),
	RGB(0x00,0xff,0x00):_('lime'),
	RGB(0x80,0x80,0x80):_('grey'),
	RGB(0x80,0x80,0x00):_('olive'),
	RGB(0xff,0xff,0xff):_('white'),
	RGB(0xff,0xff,0x00):_('yellow'),
	RGB(0x80,0x00,0x00):_('dark red'),
	RGB(0x00,0x00,0xa0):_('navy blue'),
	RGB(0xff,0x00,0x00):_('red'),
	RGB(0x00,0x00,0xff):_('blue'),
	RGB(0x80,0x00,0x80):_('purple'),
	RGB(0x00,0x80,0x80):_('teal'),
	RGB(0xff,0x00,0xff):_('fuchsia'),
	RGB(0x00,0xff,0xff):_('aqua'),
	#Extra CSS 2.1 color
	RGB(0xff,0xa5,0x00):_('orange'),
}

