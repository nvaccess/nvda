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
		sv=s*v
		if sv<0.02:
			# There is not enough saturation to perceive a hue, therefore its on the scale from black to white.
			v=v*100
			nv=min(shadeNames,key=lambda i: abs(i-v))
			closestName=shadeNames[nv]
		else:
			h*=360
			s*=100
			v*=100
			# Find the closest named hue (red, orange, yellow...)
			nh=min(hueNames,key=lambda i: 180-abs(abs(i-h)-180))
			hueName=hueNames[nh]
			ns=min(brightnessLabelsBySaturation,key=lambda i: abs(i-s))
			brightnessLabels=brightnessLabelsBySaturation[ns]
			nv=min(brightnessLabels,key=lambda i: abs(i-v))
			if nh in brownHueNames:
				brownNV=brownBrightnessRedirectionValues.get(nv)
				if brownNV is not None:
					nv=brownNV
					hueName=brownHueNames[nh]
			variationTemplate=brightnessLabels.get(nv)
			if variationTemplate:
				closestName=variationTemplate.format(color=hueName)
			else:
				closestName=hueName
		RGBToNamesCache[self]=closestName
		return closestName

RGBToNamesCache={}

shadeNames={
	# Translators: the color white (HSV saturation0%, value 100%)
	100:pgettext('color hue','white'),
	# Translators: the color very light grey (HSV saturation 0%, value 84%)
	84:pgettext('color hue','very light grey'),
	# Translators: the color light grey (HSV saturation 0%, value 66%)
	66:pgettext('color hue','light grey'),
	# Translators: the color grey (HSV saturation 0%, value 50%)
	50:pgettext('color hue','grey'),
	# Translators: the color dark grey (HSV saturation 0%, value 34%)
	34:pgettext('color hue','dark grey'),
	# Translators: the color very dark grey (HSV saturation 0%, value 16%)
	16:pgettext('color hue','very dark grey'),
	# Translators: the color black (HSV saturation 0%, value 0%)
	0:pgettext('color hue','black'),
}

hueNames={
	# Translators: The color red (HSV hue 0 degrees)
	0:pgettext('color hue','red'),
	# Translators: The color between  red and orange (HSV hue 15 degrees)
	15:pgettext('color hue','red-orange'),
	# Translators: The color orange (HSV hue 30 degrees)
	30:pgettext('color hue','orange'),
	# Translators: The color between  orange and yellow (HSV hue 45 degrees)
	45:pgettext('color hue','orange-yellow'),
	# Translators: The color yellow (HSV hue 60 degrees)
	60:pgettext('color hue','yellow'),
	# Translators: The color between  yellow and green (HSV hue 90 degrees)
	90:pgettext('color hue','yellow-green'),
	# Translators: The color green (HSV hue 120 degrees)
	120:pgettext('color hue','green'),
	# Translators: The color between  green and aqua (HSV hue 150 degrees)
	150:pgettext('color hue','green-aqua'),
	# Translators: The color aqua (HSV hue 180 degrees)
	180:pgettext('color hue','aqua'),
	# Translators: The color between  aqua and blue (HSV hue 210 degrees)
	210:pgettext('color hue','aqua-blue'),
	# Translators: The color blue (HSV hue 240 degrees)
	240:pgettext('color hue','blue'),
	# Translators: The color between  blue and purple (HSV hue 270 degrees)
	270:pgettext('color hue','blue-purple'),
	# Translators: The color purple (HSV hue 300 degrees)
	300:pgettext('color hue','purple'),
	# Translators: The color between  purple and pink (HSV hue 312 degrees)
	312:pgettext('color hue','purple-pink'),
	# Translators: The color pink (HSV hue 324 degrees)
	324:pgettext('color hue','pink'),
	# Translators: The color between  pink and red (HSV hue 342 degrees)
	342:pgettext('color hue','pink-red'),
}

brightnessLabelsBySaturation={
	100:{
		# Translators: a bright color (HSV saturation 100% and value 100%)
		100:pgettext('color variation','bright {color}'),
		# Translators: color (HSV saturation 100% and value 72%)
		72:pgettext('color variation','{color}'),
		# Translators: a dark color (HSV saturation 100% and value 44%)
		44:pgettext('color variation','dark {color}'),
		# Translators: a very dark color (HSV saturation 100% and value 16%)
		16:pgettext('color variation','very dark {color}'),
	},
	60:{
		# Translators: a light pale color (HSV saturation 50% and value 100%)
		100:pgettext('color variation','light pale {color}'),
		# Translators: a pale color (HSV saturation 50% and value 72%)
		72:pgettext('color variation','pale {color}'),
		# Translators: a dark pale color (HSV saturation 50% and value 44%)
		44:pgettext('color variation','dark pale {color}'),
		# Translators: a very dark color (HSV saturation 50% and value 16%)
		16:pgettext('color variation','very dark pale {color}'),
	},
	10:{
		# Translators: a light color almost white - hardly any hue (HSV saturation 10% and value 100%)
		100:pgettext('color variation','{color} white'),
		# Translators: a color almost grey - hardly any hue (HSV saturation 10% and value 72%)
		72:pgettext('color variation','{color} grey'),
		# Translators: a dark color almost grey - hardly any hue (HSV saturation 10% and value 44%)
		44:pgettext('color variation','dark {color} grey'),
		# Translators: a very dark color almost grey - hardly any hue (HSV saturation 10% and value 16%)
		16:pgettext('color variation','very dark {color} grey'),
	},
}

brownHueNames={
	# Translators: The color between  red and brown (HSV hue 15 degrees, below 50% brightness)
	15:pgettext('color hue','red-brown'),
	# Translators: The color brown (HSV hue 30 degrees, below 50% brightness)
	30:pgettext('color hue','brown'),
	# Translators: The color between  brown and yellow (HSV hue 45 degrees, below 50% brightness)
	45:pgettext('color hue','brown-yellow'),
}

brownBrightnessRedirectionValues={44:72,16:44}
