# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2020 NV Access Limited, Leonard de Ruijter

"""Unit tests for braille display drivers.
"""

import unittest
import braille

class TestGestureMap(unittest.TestCase):
	"""Tests the integrity of braille display driver gesture maps."""

	def test_identifiers(self):
		"""Checks whether all defined braille display gestures contain valid braille display key identifiers."""
		for name, description in braille.getDisplayList(excludeNegativeChecks=False):
			driver=braille._getDisplayDriver(name)
			gmap=driver.gestureMap
			if not gmap:
				continue
			for cls, gesture, scriptName in gmap.getScriptsForAllGestures():
				if gesture.startswith("br"):
					self.assertRegexpMatches(gesture, braille.BrailleDisplayGesture.ID_PARTS_REGEX)


class TestBRLTTY(unittest.TestCase):
	"""Tests the integrity of the bundled brlapi module."""

	def test_brlapi(self):
		try:
			# SUpress Flake8 F401 imported but unused, as we're testing the import
			import brlapi  # noqa: F401
		except Exception:
			self.fail("Couldn't import the brlapi module")
