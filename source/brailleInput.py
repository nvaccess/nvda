#brailleInput.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012 NV Access Limited
#Copyright (C) 2012 Rui Batista


import os.path
import louis

import braille
import config
from logHandler import log
import winUser


handler = None

def initialize():
	global handler
	handler = BrailleInputHandler()
	log.info("Braille input initialized")

def terminate():
	global handler
	handler = None


class BrailleInputHandler(object):
	def input(self, dots):
		log.info(str(dots))
		char = unichr(dots & 0xff)
		text = louis.backTranslate(
			[os.path.join(braille.TABLES_DIR, config.conf["braille"]["translationTable"]),
			"braille-patterns.cti"],
			char, mode=louis.dotsIO)
		chars = text[0]
		if len(chars) > 0:
			self.sendChars(chars)

	def sendChars(self, chars):
		inputs = []
		for ch in chars:
			input = winUser.Input()
			input.type = winUser.INPUT_KEYBOARD
			input.ii.ki = winUser.KeyBdInput()
			input.ii.ki.wScan = ord(ch)
			input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE
			inputs.append(input)
		winUser.SendInput(inputs)
