# brailleViewer.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from logHandler import log
import os
"""
Loads custom fonts for use in NVDA.
"""


def _isSupportedFontPath(f: str) -> bool:
	return os.path.isfile(f) and (
		f.endswith("otf")
		or f.endswith("ttf")
	)


# Fonts that have been loaded. Also used to ensure we don't load fonts twice.
_importedFonts = []


def importFonts():
	if _importedFonts:
		# fonts already loaded, exit early.
		return
	fontsDir = "fonts"
	from ctypes import WinDLL
	import os.path
	gdi32 = WinDLL("gdi32.dll")
	fonts = [f for f in os.listdir(fontsDir) if _isSupportedFontPath(f)]
	for fontPath in fonts:
		res = gdi32.AddFontResourceW(fontPath)
		if 0 >= res:
			log.error(f"Unable to import font, {fontPath}")
		else:
			log.debug(f"Importing font {fontPath}, imported {res} fonts.")
			_importedFonts.append(fontPath)
