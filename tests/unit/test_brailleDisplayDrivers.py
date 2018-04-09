#tests/unit/test_brailleDisplayDrivers.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Leonard de Ruijter

"""Unit tests for braille display drivers.
"""

import unittest
import braille
from brailleDisplayProvider import InputGesture
import inputCore

def gestureToScriptTestHelper(unit, keys, expectedScriptName, model=None, brailleInput=False):
	"""
	Helper function to ease the execution of single tests.
	It takes the same parameters as a L{brailleDisplayProvider.InputGesture}
	as well as the expected script name.
	It asserts whether the expected and actual script names are equal.
	"""
	gesture = InputGesture(model, keys, brailleInput)
	script = gesture.script
	scriptName = None if not script else script.__name__[7:]
	return unit.assertEqual(scriptName, expectedScriptName)

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

class TestCombinedEmulatedKeys(unittest.TestCase):
	"""Tests combining of emulated system keyboard keys."""

	def tearDown(self):
		"""Ensure that the user gesture map is cleared after every test."""
		inputCore.manager.userGestureMap.clear()

	def test_combinationsWithoutUserGestures(self):
		"""
		Tests combined emulations against the default gesture map for L{brailleDisplayprovider.BrailleDisplay}
		This tests the default situation, i.e. without modifications in the user gesture map.
		"""
		gestureToScriptTestHelper(self, ["fakeControl","fakeEscape"], "kb:control+escape")
		# fakeAlt+fakeEscape is assigned to windows
		gestureToScriptTestHelper(self, ["fakeAlt","fakeControl","fakeEscape"], "kb:control+leftwindows")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeControl","fakeTab"], "kb:alt+control+tab")
