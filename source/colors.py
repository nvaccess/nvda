#colors.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from collections import namedtuple
import math

RGB=namedtuple('RGB',('red','green','blue'))

RGBToNames={
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
}

def findColorName(rgb):
	foundName=RGBToNames.get(rgb,None)
	if not foundName:
		closestRGB=sorted(RGBToNames.iterkeys(),key=lambda x: math.sqrt((abs(rgb.red-x.red)*0.3)**2+(abs(rgb.green-x.green)*0.59)**2+(abs(rgb.blue-x.blue)*0.11)**2))[0]
		foundName=RGBToNames[closestRGB]
		RGBToNames[rgb]=foundName
	return foundName


