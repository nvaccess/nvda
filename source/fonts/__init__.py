# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2019 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
from typing import List

import globalVars
from logHandler import log
import os
from ctypes import WinDLL
gdi32 = WinDLL("gdi32.dll")
"""
Loads custom fonts for use in NVDA.
"""

fontsDir = os.path.join(globalVars.appDir, "fonts")


def _isSupportedFontPath(f: str) -> bool:
	return os.path.isfile(f) and (
		f.endswith(".otf")
		or f.endswith(".ttf")
	)


def addFonts(_fontSearchPath) -> List[str]:
	searchPathFiles = [
		os.path.join(_fontSearchPath, f)
		for f in os.listdir(_fontSearchPath)
	]
	fonts = [
		f for f in searchPathFiles
		if _isSupportedFontPath(f)
	]
	log.debug(f"Fonts to load: {fonts}")
	imported = []
	for fontPath in fonts:
		numFontsImported = _addFontResource(fontPath)
		if 0 >= numFontsImported:
			log.error(f"Unable to add font {fontPath}")
		else:
			log.debug(f"Added font resource {fontPath}, imported {numFontsImported} fonts.")
			imported.append(fontPath)
	return imported


def _addFontResource(fontPath: str) -> int:
	# from wingdi.h
	FR_PRIVATE = 0x10
	res = gdi32.AddFontResourceExW(
		fontPath,
		# Only this process can use the font.
		# The system will take care of unloading the font when the process ends.
		FR_PRIVATE,
		# Reserved. Must be zero.
		0
	)
	return res


# Fonts that have been loaded.
_imported: List[str] = []


def importFonts():
	global _imported
	if _imported:
		log.debug("Fonts already loaded.")
		return

	log.debug("Loading fonts.")
	_imported = addFonts(fontsDir)
