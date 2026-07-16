# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2026 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Gestures for braille input."""

import inputCore

from .constants import DOT7, DOT8


def formatDotNumbers(dots: int):
	out = []
	for dot in range(8):
		if dots & (1 << dot):
			out.append(str(dot + 1))
	return " ".join(out)


class BrailleInputGesture(inputCore.InputGesture):
	"""Input (dots and/or space bar) from a braille keyboard.
	This could either be as part of a braille display or a stand-alone unit.
	L{dots} and L{space} should be set appropriately.
	"""

	dots: int = 0
	"""Bitmask of pressed dots."""

	space: bool = False
	"""Whether the space bar is pressed."""

	shouldPreventSystemIdle = True

	def _makeDotsId(self):
		items = ["dot%d" % (i + 1) for i in range(8) if self.dots & (1 << i)]
		if self.space:
			items.append("space")
		return "bk:" + "+".join(items)

	GENERIC_ID_SPACE_DOTS = inputCore.normalizeGestureIdentifier("bk:space+dots")
	"""The generic gesture identifier for space plus any dots.
	This could be used to bind many braille commands to a single script.
	"""

	GENERIC_ID_DOTS = inputCore.normalizeGestureIdentifier("bk:dots")
	"""The generic gesture identifier for any dots.
	This is used to bind entry of braille text to a single script.
	"""

	def _get_identifiers(self):
		if self.space and self.dots:
			return (self._makeDotsId(), self.GENERIC_ID_SPACE_DOTS)
		elif self.dots in (DOT7, DOT8, DOT7 | DOT8):
			# Allow bindings to dots 7 and/or 8 by themselves.
			return (self._makeDotsId(), self.GENERIC_ID_DOTS)
		elif self.dots or self.space:
			return (self.GENERIC_ID_DOTS,)
		else:
			return ()

	@classmethod
	def _makeDisplayText(cls, dots: int, space: bool):
		out = ""
		if space and dots:
			# Translators: Reported when braille space is pressed with dots in input help mode.
			out = _("space with dot")
		elif dots:
			# Translators: Reported when braille dots are pressed in input help mode.
			out = _("dot")
		elif space:
			# Translators: Reported when braille space is pressed in input help mode.
			out = _("space")
		if dots:
			out += " " + formatDotNumbers(dots)
		return out

	def _get_displayName(self):
		if not self.dots and not self.space:
			return None
		return self._makeDisplayText(self.dots, self.space)

	@classmethod
	def getDisplayTextForIdentifier(cls, identifier: str):
		assert isinstance(identifier, str)
		# Translators: Used when describing keys on a braille keyboard.
		source = _("braille keyboard")
		if identifier == cls.GENERIC_ID_SPACE_DOTS:
			# Translators: Used to describe the press of space
			# along with any dots on a braille keyboard.
			return (source, _("space with any dots"))
		if identifier == cls.GENERIC_ID_DOTS:
			# Translators: Used to describe the press of any dots
			# on a braille keyboard.
			return (source, _("any dots"))
		# Example identifier: bk:space+dot1+dot2
		# Strip the bk: prefix.
		partsStr = identifier.split(":", 1)[1]
		parts = partsStr.split("+")
		dots = 0
		space = False
		for part in parts:
			if part == "space":
				space = True
			else:
				# Example part: "dot1"
				# Get the dot number and make it 0 based instead of 1 based.
				dot = int(part[3]) - 1
				# Update the dots bitmask.
				dots += 1 << dot
		return (source, cls._makeDisplayText(dots, space))
