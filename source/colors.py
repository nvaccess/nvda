#colors.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from collections import namedtuple
import math
import colorsys
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
		foundName=RGBToNamesCache.get(self,None)
		if foundName:
			return foundName
		# convert to hsv (hue, saturation, value)
		h,s,v=colorsys.rgb_to_hsv(self.red/255.0,self.green/255.0,self.blue/255.0)
		h=int(h*360)
		sv=s*v
		if sv<0.05:
			# There is not enough saturation to perceive a hue, therefore its on the scale from black to white.
			closestName=shadeNames[int(round((len(shadeNames)-1)*(1-v)))]
		else:
			# Find the closest named hue (red, orange, yellow...)
			# or a paile, dark or paile dark variation
			nh=min((x for x in colorNamesByHue),key=lambda x: abs(x-h))
			hueShadeNames=colorNamesByHue[nh][int(s<=0.5)]
			closestName=hueShadeNames[int(round((len(hueShadeNames)-1)*(1-v)))]
		RGBToNamesCache[self]=closestName
		return closestName

RGBToNamesCache={}

# a dictionary whos keys are hues in degrees, and values are:
# a 2d array containing labels for normal and dark, and also pale versions of all of these 
colorNamesByHue={
	0:[
		[
			# Translators: The color red (HSV 0 degrees H, 100% S, 100% V)
			pgettext('color name','red'),
			# Translators: The color dark red (HSV 0 degrees H, 100% S, 50% V)
			pgettext('color name','dark red'),
		],
		[
			# Translators: The color pale red (HSV 0 degrees H, 50% S, 100% V)
			pgettext('color name','pale red'),
			# Translators: The color pale dark red (HSV 0 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark red'),
		],
	],
	15:[
		[
			# Translators: The color red-orange (HSV 15 degrees H, 100% S, 100% V)
			pgettext('color name','red-orange'),
			# Translators: The color red-brown (HSV 15 degrees H, 100% S, 50% V)
			pgettext('color name','red-brown'),
			# Translators: The color dark red-brown (HSV 15 degrees H, 100% S, 25% V)
			pgettext('color name','dark red-brown'),
		],
		[
			# Translators: The color pale red-orange (HSV 15 degrees H, 50% S, 100% V)
			pgettext('color name','pale red-orange'),
			# Translators: The color pale red-brown (HSV 15 degrees H, 50% S, 50% V)
			pgettext('color name','pale red-brown'),
			# Translators: The color pale dark red-brown (HSV 15 degrees H, 50% S, 25% V)
			pgettext('color name','pale dark red-brown'),
		],
	],
	30:[
		[
			# Translators: The color orange (HSV 30 degrees H, 100% S, 100% V)
			pgettext('color name','orange'),
			# Translators: The color brown (HSV 30 degrees H, 100% S, 50% V)
			pgettext('color name','brown'),
			# Translators: The color dark brown (HSV 30 degrees H, 100% S, 25% V)
			pgettext('color name','dark brown'),
		],
		[
			# Translators: The color pale orange (HSV 30 degrees H, 50% S, 100% V)
			pgettext('color name','pale orange'),
			# Translators: The color pale brown (HSV 30 degrees H, 50% S, 50% V)
			pgettext('color name','pale brown'),
			# Translators: The color pale dark brown (HSV 30 degrees H, 50% S, 25% V)
			pgettext('color name','pale dark brown'),
		],
	],
	45:[
		[
			# Translators: The color orange-yellow (HSV 45 degrees H, 100% S, 100% V)
			pgettext('color name','orange-yellow'),
			# Translators: The color brown-yellow (HSV 45 degrees H, 100% S, 50% V)
			pgettext('color name','brown-yellow'),
			# Translators: The color dark brown-yellow (HSV 45 degrees H, 100% S, 25% V)
			pgettext('color name','dark brown-yellow'),
		],
		[
			# Translators: The color pale orange-yellow (HSV 45 degrees H, 50% S, 100% V)
			pgettext('color name','pale orange-yellow'),
			# Translators: The color pale brown-yellow (HSV 45 degrees H, 50% S, 50% V)
			pgettext('color name','pale brown-yellow'),
			# Translators: The color pale dark brown-yellow (HSV 45 degrees H, 50% S, 25% V)
			pgettext('color name','pale dark brown-yellow'),
		],
	],
	60:[
		[
			# Translators: The color yellow (HSV 60 degrees H, 100% S, 100% V)
			pgettext('color name','yellow'),
			# Translators: The color dark yellow (HSV 60 degrees H, 100% S, 50% V)
			pgettext('color name','dark yellow'),
		],
		[
			# Translators: The color pale yellow (HSV 60 degrees H, 50% S, 100% V)
			pgettext('color name','pale yellow'),
			# Translators: The color pale dark yellow (HSV 60 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark yellow'),
		],
	],
	90:[
		[
			# Translators: The color yellow-green (HSV 90 degrees H, 100% S, 100% V)
			pgettext('color name','yellow-green'),
			# Translators: The color dark yellow-green (HSV 90 degrees H, 100% S, 50% V)
			pgettext('color name','dark yellow-green'),
		],
		[
			# Translators: The color pale yellow-green (HSV 90 degrees H, 50% S, 100% V)
			pgettext('color name','pale yellow-green'),
			# Translators: The color pale dark yellow-green (HSV 90 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark yellow-green'),
		],
	],
	120:[
		[
			# Translators: The color green (HSV 120 degrees H, 100% S, 100% V)
			pgettext('color name','green'),
			# Translators: The color dark green (HSV 120 degrees H, 100% S, 50% V)
			pgettext('color name','dark green'),
		],
		[
			# Translators: The color pale green (HSV 120 degrees H, 50% S, 100% V)
			pgettext('color name','pale green'),
			# Translators: The color pale dark green (HSV 120 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark green'),
		],
	],
	150:[
		[
			# Translators: The color green-aqua (HSV 150 degrees H, 100% S, 100% V)
			pgettext('color name','green-aqua'),
			# Translators: The color dark green-aqua (HSV 150 degrees H, 100% S, 50% V)
			pgettext('color name','dark green-aqua'),
		],
		[
			# Translators: The color pale green-aqua (HSV 150 degrees H, 50% S, 100% V)
			pgettext('color name','pale green-aqua'),
			# Translators: The color pale dark green-aqua (HSV 150 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark green-aqua'),
		],
	],
	180:[
		[
			# Translators: The color aqua (HSV 180 degrees H, 100% S, 100% V)
			pgettext('color name','aqua'),
			# Translators: The color dark aqua (HSV 180 degrees H, 100% S, 50% V)
			pgettext('color name','dark aqua'),
		],
		[
			# Translators: The color pale aqua (HSV 180 degrees H, 50% S, 100% V)
			pgettext('color name','pale aqua'),
			# Translators: The color pale dark aqua (HSV 180 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark aqua'),
		],
	],
	210:[
		[
			# Translators: The color aqua-blue (HSV 210 degrees H, 100% S, 100% V)
			pgettext('color name','aqua-blue'),
			# Translators: The color dark aqua-blue (HSV 210 degrees H, 100% S, 50% V)
			pgettext('color name','dark aqua-blue'),
		],
		[
			# Translators: The color pale aqua-blue (HSV 210 degrees H, 50% S, 100% V)
			pgettext('color name','pale aqua-blue'),
			# Translators: The color pale dark aqua-blue (HSV 210 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark aqua-blue'),
		],
	],
	240:[
		[
			# Translators: The color blue (HSV 240 degrees H, 100% S, 100% V)
			pgettext('color name','blue'),
			# Translators: The color dark blue (HSV 240 degrees H, 100% S, 50% V)
			pgettext('color name','dark blue'),
		],
		[
			# Translators: The color pale blue (HSV 240 degrees H, 50% S, 100% V)
			pgettext('color name','pale blue'),
			# Translators: The color pale dark blue (HSV 240 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark blue'),
		],
	],
	263:[
		[
			# Translators: The color blue-purple (HSV 263 degrees H, 100% S, 100% V)
			pgettext('color name','blue-purple'),
			# Translators: The color dark blue-purple (HSV 263 degrees H, 100% S, 50% V)
			pgettext('color name','dark blue-purple'),
		],
		[
			# Translators: The color pale blue-purple (HSV 263 degrees H, 50% S, 100% V)
			pgettext('color name','pale blue-purple'),
			# Translators: The color pale dark blue-purple (HSV 263 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark blue-purple'),
		],
	],
	285:[
		[
			# Translators: The color purple (HSV 285 degrees H, 100% S, 100% V)
			pgettext('color name','purple'),
			# Translators: The color dark purple (HSV 285 degrees H, 100% S, 50% V)
			pgettext('color name','dark purple'),
		],
		[
			# Translators: The color pale purple (HSV 285 degrees H, 50% S, 100% V)
			pgettext('color name','pale purple'),
			# Translators: The color pale dark purple (HSV 285 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark purple'),
		],
	],
	300:[
		[
			# Translators: The color purple-pink (HSV 300 degrees H, 100% S, 100% V)
			pgettext('color name','purple-pink'),
			# Translators: The color dark purple-pink (HSV 300 degrees H, 100% S, 50% V)
			pgettext('color name','dark purple-pink'),
		],
		[
			# Translators: The color pale purple-pink (HSV 300 degrees H, 50% S, 100% V)
			pgettext('color name','pale purple-pink'),
			# Translators: The color pale dark purple-pink (HSV 300 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark purple-pink'),
		],
	],
	315:[
		[
			# Translators: The color pink (HSV 315 degrees H, 100% S, 100% V)
			pgettext('color name','pink'),
			# Translators: The color dark pink (HSV 315 degrees H, 100% S, 50% V)
			pgettext('color name','dark pink'),
		],
		[
			# Translators: The color pale pink (HSV 315 degrees H, 50% S, 100% V)
			pgettext('color name','pale pink'),
			# Translators: The color pale dark pink (HSV 315 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark pink'),
		],
	],
	338:[
		[
			# Translators: The color pink-red (HSV 338 degrees H, 100% S, 100% V)
			pgettext('color name','pink-red'),
			# Translators: The color dark pink-red (HSV 338 degrees H, 100% S, 50% V)
			pgettext('color name','dark pink-red'),
		],
		[
			# Translators: The color pale pink-red (HSV 338 degrees H, 50% S, 100% V)
			pgettext('color name','pale pink-red'),
			# Translators: The color pale dark pink-red (HSV 338 degrees H, 50% S, 50% V)
			pgettext('color name','pale dark pink-red'),
		],
	],
}

shadeNames=[
	# Translators: the color white (RGB 255,255,255)
	pgettext('color name','white'),
	# Translators: the color light grey (RGB 192,192,192)
	pgettext('color name','light grey'),
	# Translators: the color grey (RGB 128,128,128)
	pgettext('color name','grey'),
	# Translators: the color dark grey (RGB 64,64,64)
	pgettext('color name','dark grey'),
	# Translators: the color black (RGB 0,0,0)
	pgettext('color name','black'),
]

