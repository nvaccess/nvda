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
		foundName=RGBToNames.get(self,None)
		if foundName:
			return foundName
		foundName=RGBToNamesCache.get(self,None)
		if foundName:
			return foundName
		longestDistance=255.0
		# Translators: Reported when text is written in unknown color.
		closestName=_("unknown color")
		selfHSV=colorsys.rgb_to_hsv(self.red/255.0,self.green/255.0,self.blue/255.0)
		for possibleRGB,possibleName  in RGBToNames.iteritems():
			possibleHSV=colorsys.rgb_to_hsv(possibleRGB.red/255.0,possibleRGB.green/255.0,possibleRGB.blue/255.0)
			dh=abs(selfHSV[0]-possibleHSV[0])
			if dh>0.5:
				dh=1-dh
			ds=abs(selfHSV[1]-possibleHSV[1])
			dv=abs(selfHSV[2]-possibleHSV[2])
			distance=math.sqrt(0.4*(dh**2)+0.1*(ds**2)+0.1*(dv**2))
			if distance<longestDistance:
				longestDistance=distance
				closestName=possibleName
		RGBToNamesCache[self]=closestName
		return closestName

RGBToNamesCache={}

RGBToNames={
# Translators: the color Alice Blue (RGB 240, 248, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(240,248,255):pgettext('color name','Alice Blue'),
# Translators: the color Antique White (RGB 250, 235, 215) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(250,235,215):pgettext('color name','Antique White'),
# Translators: the color Aqua (RGB 0, 255, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,255,255):pgettext('color name','Aqua'),
# Translators: the color Aquamarine (RGB 127, 255, 212) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(127,255,212):pgettext('color name','Aquamarine'),
# Translators: the color Azure (RGB 240, 255, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(240,255,255):pgettext('color name','Azure'),
# Translators: the color Beige (RGB 245, 245, 220) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(245,245,220):pgettext('color name','Beige'),
# Translators: the color Bisque (RGB 255, 228, 196) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,228,196):pgettext('color name','Bisque'),
# Translators: the color Black (RGB 0, 0, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,0,0):pgettext('color name','Black'),
# Translators: the color Blanched Almond (RGB 255, 235, 205) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,235,205):pgettext('color name','Blanched Almond'),
# Translators: the color Blue (RGB 0, 0, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,0,255):pgettext('color name','Blue'),
# Translators: the color Blue Violet (RGB 138, 43, 226) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(138,43,226):pgettext('color name','Blue Violet'),
# Translators: the color Brown (RGB 165, 42, 42) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(165,42,42):pgettext('color name','Brown'),
# Translators: the color Burly Wood (RGB 222, 184, 135) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(222,184,135):pgettext('color name','Burly Wood'),
# Translators: the color Cadet Blue (RGB 95, 158, 160) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(95,158,160):pgettext('color name','Cadet Blue'),
# Translators: the color Chartreuse (RGB 127, 255, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(127,255,0):pgettext('color name','Chartreuse'),
# Translators: the color Chocolate (RGB 210, 105, 30) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(210,105,30):pgettext('color name','Chocolate'),
# Translators: the color Coral (RGB 255, 127, 80) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,127,80):pgettext('color name','Coral'),
# Translators: the color Cornflower Blue (RGB 100, 149, 237) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(100,149,237):pgettext('color name','Cornflower Blue'),
# Translators: the color Cornsilk (RGB 255, 248, 220) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,248,220):pgettext('color name','Cornsilk'),
# Translators: the color Crimson (RGB 220, 20, 60) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(220,20,60):pgettext('color name','Crimson'),
# Translators: the color Cyan (RGB 0, 255, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,255,255):pgettext('color name','Cyan'),
# Translators: the color Dark Blue (RGB 0, 0, 139) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,0,139):pgettext('color name','Dark Blue'),
# Translators: the color Dark Cyan (RGB 0, 139, 139) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,139,139):pgettext('color name','Dark Cyan'),
# Translators: the color Dark Goldenrod (RGB 184, 134, 11) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(184,134,11):pgettext('color name','Dark Goldenrod'),
# Translators: the color Dark Gray (RGB 169, 169, 169) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(169,169,169):pgettext('color name','Dark Gray'),
# Translators: the color Dark Green (RGB 0, 100, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,100,0):pgettext('color name','Dark Green'),
# Translators: the color Dark Khaki (RGB 189, 183, 107) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(189,183,107):pgettext('color name','Dark Khaki'),
# Translators: the color Dark Magenta (RGB 139, 0, 139) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(139,0,139):pgettext('color name','Dark Magenta'),
# Translators: the color Dark Olive Green (RGB 85, 107, 47) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(85,107,47):pgettext('color name','Dark Olive Green'),
# Translators: the color Dark Orange (RGB 255, 140, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,140,0):pgettext('color name','Dark Orange'),
# Translators: the color Dark Orchid (RGB 153, 50, 204) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(153,50,204):pgettext('color name','Dark Orchid'),
# Translators: the color Dark Red (RGB 139, 0, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(139,0,0):pgettext('color name','Dark Red'),
# Translators: the color Dark Salmon (RGB 233, 150, 122) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(233,150,122):pgettext('color name','Dark Salmon'),
# Translators: the color Dark Sea Green (RGB 143, 188, 143) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(143,188,143):pgettext('color name','Dark Sea Green'),
# Translators: the color Dark Slate Blue (RGB 72, 61, 139) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(72,61,139):pgettext('color name','Dark Slate Blue'),
# Translators: the color Dark Slate Gray (RGB 47, 79, 79) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(47,79,79):pgettext('color name','Dark Slate Gray'),
# Translators: the color Dark Turquoise (RGB 0, 206, 209) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,206,209):pgettext('color name','Dark Turquoise'),
# Translators: the color Dark Violet (RGB 148, 0, 211) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(148,0,211):pgettext('color name','Dark Violet'),
# Translators: the color Deep Pink (RGB 255, 20, 147) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,20,147):pgettext('color name','Deep Pink'),
# Translators: the color Deep Sky Blue (RGB 0, 191, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,191,255):pgettext('color name','Deep Sky Blue'),
# Translators: the color Dim Gray (RGB 105, 105, 105) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(105,105,105):pgettext('color name','Dim Gray'),
# Translators: the color Dodger Blue (RGB 30, 144, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(30,144,255):pgettext('color name','Dodger Blue'),
# Translators: the color Fire Brick (RGB 178, 34, 34) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(178,34,34):pgettext('color name','Fire Brick'),
# Translators: the color Floral White (RGB 255, 250, 240) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,250,240):pgettext('color name','Floral White'),
# Translators: the color Forest Green (RGB 34, 139, 34) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(34,139,34):pgettext('color name','Forest Green'),
# Translators: the color Fuchsia (RGB 255, 0, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,0,255):pgettext('color name','Fuchsia'),
# Translators: the color Gainsboro (RGB 220, 220, 220) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(220,220,220):pgettext('color name','Gainsboro'),
# Translators: the color Ghost White (RGB 248, 248, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(248,248,255):pgettext('color name','Ghost White'),
# Translators: the color Gold (RGB 255, 215, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,215,0):pgettext('color name','Gold'),
# Translators: the color Goldenrod (RGB 218, 165, 32) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(218,165,32):pgettext('color name','Goldenrod'),
# Translators: the color Gray (RGB 128, 128, 128) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(128,128,128):pgettext('color name','Gray'),
# Translators: the color Green (RGB 0, 128, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,128,0):pgettext('color name','Green'),
# Translators: the color Green Yellow (RGB 173, 255, 47) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(173,255,47):pgettext('color name','Green Yellow'),
# Translators: the color Honeydew (RGB 240, 255, 240) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(240,255,240):pgettext('color name','Honeydew'),
# Translators: the color Hot Pink (RGB 255, 105, 180) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,105,180):pgettext('color name','Hot Pink'),
# Translators: the color Indian Red (RGB 205, 92, 92) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(205,92,92):pgettext('color name','Indian Red'),
# Translators: the color Indigo (RGB 75, 0, 130) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(75,0,130):pgettext('color name','Indigo'),
# Translators: the color Ivory (RGB 255, 255, 240) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,255,240):pgettext('color name','Ivory'),
# Translators: the color Khaki (RGB 240, 230, 140) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(240,230,140):pgettext('color name','Khaki'),
# Translators: the color Lavender (RGB 230, 230, 250) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(230,230,250):pgettext('color name','Lavender'),
# Translators: the color Lavender Blush (RGB 255, 240, 245) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,240,245):pgettext('color name','Lavender Blush'),
# Translators: the color Lawn Green (RGB 124, 252, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(124,252,0):pgettext('color name','Lawn Green'),
# Translators: the color Lemon Chiffon (RGB 255, 250, 205) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,250,205):pgettext('color name','Lemon Chiffon'),
# Translators: the color Light Blue (RGB 173, 216, 230) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(173,216,230):pgettext('color name','Light Blue'),
# Translators: the color Light Coral (RGB 240, 128, 128) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(240,128,128):pgettext('color name','Light Coral'),
# Translators: the color Light Cyan (RGB 224, 255, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(224,255,255):pgettext('color name','Light Cyan'),
# Translators: the color Light Goldenrod Yellow (RGB 250, 250, 210) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(250,250,210):pgettext('color name','Light Goldenrod Yellow'),
# Translators: the color Light Green (RGB 144, 238, 144) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(144,238,144):pgettext('color name','Light Green'),
# Translators: the color Light Grey (RGB 211, 211, 211) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(211,211,211):pgettext('color name','Light Grey'),
# Translators: the color Light Pink (RGB 255, 182, 193) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,182,193):pgettext('color name','Light Pink'),
# Translators: the color Light Salmon (RGB 255, 160, 122) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,160,122):pgettext('color name','Light Salmon'),
# Translators: the color Light Sea Green (RGB 32, 178, 170) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(32,178,170):pgettext('color name','Light Sea Green'),
# Translators: the color Light Sky Blue (RGB 135, 206, 250) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(135,206,250):pgettext('color name','Light Sky Blue'),
# Translators: the color Light Slate Gray (RGB 119, 136, 153) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(119,136,153):pgettext('color name','Light Slate Gray'),
# Translators: the color Light Steel Blue (RGB 176, 196, 222) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(176,196,222):pgettext('color name','Light Steel Blue'),
# Translators: the color Light Yellow (RGB 255, 255, 224) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,255,224):pgettext('color name','Light Yellow'),
# Translators: the color Lime (RGB 0, 255, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,255,0):pgettext('color name','Lime'),
# Translators: the color Lime Green (RGB 50, 205, 50) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(50,205,50):pgettext('color name','Lime Green'),
# Translators: the color Linen (RGB 250, 240, 230) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(250,240,230):pgettext('color name','Linen'),
# Translators: the color Magenta (RGB 255, 0, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,0,255):pgettext('color name','Magenta'),
# Translators: the color Maroon (RGB 128, 0, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(128,0,0):pgettext('color name','Maroon'),
# Translators: the color Medium Aquamarine (RGB 102, 205, 170) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(102,205,170):pgettext('color name','Medium Aquamarine'),
# Translators: the color Medium Blue (RGB 0, 0, 205) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,0,205):pgettext('color name','Medium Blue'),
# Translators: the color Medium Orchid (RGB 186, 85, 211) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(186,85,211):pgettext('color name','Medium Orchid'),
# Translators: the color Medium Purple (RGB 147, 112, 219) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(147,112,219):pgettext('color name','Medium Purple'),
# Translators: the color Medium Sea Green (RGB 60, 179, 113) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(60,179,113):pgettext('color name','Medium Sea Green'),
# Translators: the color Medium Slate Blue (RGB 123, 104, 238) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(123,104,238):pgettext('color name','Medium Slate Blue'),
# Translators: the color Medium Spring Green (RGB 0, 250, 154) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,250,154):pgettext('color name','Medium Spring Green'),
# Translators: the color Medium Turquoise (RGB 72, 209, 204) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(72,209,204):pgettext('color name','Medium Turquoise'),
# Translators: the color Medium Violet Red (RGB 199, 21, 133) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(199,21,133):pgettext('color name','Medium Violet Red'),
# Translators: the color Midnight Blue (RGB 25, 25, 112) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(25,25,112):pgettext('color name','Midnight Blue'),
# Translators: the color Mint Cream (RGB 245, 255, 250) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(245,255,250):pgettext('color name','Mint Cream'),
# Translators: the color Misty Rose (RGB 255, 228, 225) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,228,225):pgettext('color name','Misty Rose'),
# Translators: the color Moccasin (RGB 255, 228, 181) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,228,181):pgettext('color name','Moccasin'),
# Translators: the color Navajo White (RGB 255, 222, 173) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,222,173):pgettext('color name','Navajo White'),
# Translators: the color Navy (RGB 0, 0, 128) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,0,128):pgettext('color name','Navy'),
# Translators: the color Old Lace (RGB 253, 245, 230) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(253,245,230):pgettext('color name','Old Lace'),
# Translators: the color Olive (RGB 128, 128, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(128,128,0):pgettext('color name','Olive'),
# Translators: the color Olive Drab (RGB 107, 142, 35) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(107,142,35):pgettext('color name','Olive Drab'),
# Translators: the color Orange (RGB 255, 165, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,165,0):pgettext('color name','Orange'),
# Translators: the color Orange Red (RGB 255, 69, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,69,0):pgettext('color name','Orange Red'),
# Translators: the color Orchid (RGB 218, 112, 214) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(218,112,214):pgettext('color name','Orchid'),
# Translators: the color Pale Goldenrod (RGB 238, 232, 170) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(238,232,170):pgettext('color name','Pale Goldenrod'),
# Translators: the color Pale Green (RGB 152, 251, 152) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(152,251,152):pgettext('color name','Pale Green'),
# Translators: the color Pale Turquoise (RGB 175, 238, 238) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(175,238,238):pgettext('color name','Pale Turquoise'),
# Translators: the color Pale Violet Red (RGB 219, 112, 147) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(219,112,147):pgettext('color name','Pale Violet Red'),
# Translators: the color Papaya Whip (RGB 255, 239, 213) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,239,213):pgettext('color name','Papaya Whip'),
# Translators: the color Peach Puff (RGB 255, 218, 185) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,218,185):pgettext('color name','Peach Puff'),
# Translators: the color Peru (RGB 205, 133, 63) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(205,133,63):pgettext('color name','Peru'),
# Translators: the color Pink (RGB 255, 192, 203) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,192,203):pgettext('color name','Pink'),
# Translators: the color Plum (RGB 221, 160, 221) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(221,160,221):pgettext('color name','Plum'),
# Translators: the color Powder Blue (RGB 176, 224, 230) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(176,224,230):pgettext('color name','Powder Blue'),
# Translators: the color Purple (RGB 128, 0, 128) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(128,0,128):pgettext('color name','Purple'),
# Translators: the color Red (RGB 255, 0, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,0,0):pgettext('color name','Red'),
# Translators: the color Rosy Brown (RGB 188, 143, 143) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(188,143,143):pgettext('color name','Rosy Brown'),
# Translators: the color Royal Blue (RGB 65, 105, 225) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(65,105,225):pgettext('color name','Royal Blue'),
# Translators: the color Saddle Brown (RGB 139, 69, 19) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(139,69,19):pgettext('color name','Saddle Brown'),
# Translators: the color Salmon (RGB 250, 128, 114) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(250,128,114):pgettext('color name','Salmon'),
# Translators: the color Sandy Brown (RGB 244, 164, 96) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(244,164,96):pgettext('color name','Sandy Brown'),
# Translators: the color Sea Green (RGB 46, 139, 87) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(46,139,87):pgettext('color name','Sea Green'),
# Translators: the color Seashell (RGB 255, 245, 238) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,245,238):pgettext('color name','Seashell'),
# Translators: the color Sienna (RGB 160, 82, 45) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(160,82,45):pgettext('color name','Sienna'),
# Translators: the color Silver (RGB 192, 192, 192) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(192,192,192):pgettext('color name','Silver'),
# Translators: the color Sky Blue (RGB 135, 206, 235) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(135,206,235):pgettext('color name','Sky Blue'),
# Translators: the color Slate Blue (RGB 106, 90, 205) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(106,90,205):pgettext('color name','Slate Blue'),
# Translators: the color Slate Gray (RGB 112, 128, 144) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(112,128,144):pgettext('color name','Slate Gray'),
# Translators: the color Snow (RGB 255, 250, 250) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,250,250):pgettext('color name','Snow'),
# Translators: the color Spring Green (RGB 0, 255, 127) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,255,127):pgettext('color name','Spring Green'),
# Translators: the color Steel Blue (RGB 70, 130, 180) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(70,130,180):pgettext('color name','Steel Blue'),
# Translators: the color Tan (RGB 210, 180, 140) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(210,180,140):pgettext('color name','Tan'),
# Translators: the color Teal (RGB 0, 128, 128) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(0,128,128):pgettext('color name','Teal'),
# Translators: the color Thistle (RGB 216, 191, 216) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(216,191,216):pgettext('color name','Thistle'),
# Translators: the color Tomato (RGB 255, 99, 71) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,99,71):pgettext('color name','Tomato'),
# Translators: the color Turquoise (RGB 64, 224, 208) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(64,224,208):pgettext('color name','Turquoise'),
# Translators: the color Violet (RGB 238, 130, 238) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(238,130,238):pgettext('color name','Violet'),
# Translators: the color Wheat (RGB 245, 222, 179) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(245,222,179):pgettext('color name','Wheat'),
# Translators: the color White (RGB 255, 255, 255) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,255,255):pgettext('color name','White'),
# Translators: the color White Smoke (RGB 245, 245, 245) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(245,245,245):pgettext('color name','White Smoke'),
# Translators: the color Yellow (RGB 255, 255, 0) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(255,255,0):pgettext('color name','Yellow'),
# Translators: the color Yellow Green (RGB 154, 205, 50) from CSS color list at http://www.w3schools.com/cssref/css_colornames.asp
	RGB(154,205,50):pgettext('color name','Yellow Green'),
}
