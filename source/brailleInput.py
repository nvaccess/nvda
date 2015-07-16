#brailleInput.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2013 NV Access Limited, Rui Batista

import os.path
import louis
import braille
import config
from logHandler import log
import winUser
import inputCore

"""Framework for handling braille input from the user.
All braille input is represented by a {BrailleInputGesture}.
Normally, all that is required is to create and execute a L{BrailleInputGesture},
as there are built-in gesture bindings for braille input.
"""

#: The singleton BrailleInputHandler instance.
#: @type: L{BrailleInputHandler}
handler = None

def initialize():
	global handler
	handler = BrailleInputHandler()
	log.info("Braille input initialized")

def terminate():
	global handler
	handler = None

class BrailleInputHandler(object):
	"""Handles braille input.
	"""

	def input(self, dots):
		"""Handle one cell of braille input.
		"""
		# liblouis requires us to set the highest bit for proper use of dotsIO.
		char = unichr(dots | 0x8000)
		text = louis.backTranslate(
			[os.path.join(braille.TABLES_DIR, config.conf["braille"]["inputTable"]),
			"braille-patterns.cti"],
			char, mode=louis.dotsIO)
		chars = text[0]
		if len(chars) > 0:
			self.sendChars(chars)

	def sendChars(self, chars):
		inputs = []
		for ch in chars:
			for direction in (0,winUser.KEYEVENTF_KEYUP): 
				input = winUser.Input()
				input.type = winUser.INPUT_KEYBOARD
				input.ii.ki = winUser.KeyBdInput()
				input.ii.ki.wScan = ord(ch)
				input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE|direction
				inputs.append(input)
		winUser.SendInput(inputs)

class BrailleInputGesture(inputCore.InputGesture):
	"""Input (dots and/or space bar) from a braille keyboard.
	This could either be as part of a braille display or a stand-alone unit.
	L{dots} and L{space} should be set appropriately.
	"""

	#: Bitmask of pressed dots.
	#: @type: int
	dots = 0

	#: Whether the space bar is pressed.
	#: @type: bool
	space = False

	def _get_identifiers(self):
		if self.space and self.dots:
			dotsString = "+".join("dot%d" % (i+1) for i in xrange(8) if self.dots & (1 << i))
			return ("bk:space+%s" % dotsString,
				"bk:space+dots")
		elif self.dots or self.space:
			return ("bk:dots",)
		else:
			return ()

	def _get_displayName(self):
		if not self.dots and not self.space:
			return None
		# Translators: Reported before braille input in input help mode.
		out = [_("braille")]
		if self.space and self.dots:
			# Translators: Reported when braille space is pressed with dots in input help mode.
			out.append(_("space with dot"))
		elif self.dots:
			# Translators: Reported when braille dots are pressed in input help mode.
			out.append(_("dot"))
		elif self.space:
			# Translators: Reported when braille space is pressed in input help mode.
			out.append(_("space"))
		if self.dots:
			for dot in xrange(8):
				if self.dots & (1 << dot):
					out.append(str(dot + 1))
		return " ".join(out)
