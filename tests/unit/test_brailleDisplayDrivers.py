#tests/unit/test_brailleDisplayDrivers.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited, Leonard de Ruijter

"""Unit tests for braille display drivers.
"""

import unittest
import braille
from brailleDisplayProvider import *
import inputCore
import globalCommands

def gestureToScriptTestHelper(
	unit, keys, expectedScriptName, model=None, brailleInput=False, source=BrailleDisplayDriver.name):
	"""
	Helper function to ease the execution of single tests.
	It takes the same parameters as a L{brailleDisplayProvider.InputGesture}
	as well as the expected script name.
	It asserts whether the expected and actual script names are equal.
	"""
	gesture = InputGesture(source, model, keys, brailleInput)
	script = gesture.script
	scriptName = None if not script else script.__name__[7:]
	return unit.assertEqual(
		scriptName, expectedScriptName,
		msg="Expected script {expected} for {id}, but bound to {actual}".format(
			expected=expectedScriptName, id=gesture.normalizedIdentifiers[0], actual=scriptName
		)
	)

class TestGestureMaps(unittest.TestCase):
	"""Tests the integrity of braille display driver gesture maps."""

	def test_scriptAssignments(self):
		"""Checks whether all defined braille display gestures are assigned to their expected scripts.
		This also involves testing the validity of gesture identifiers.
		"""
		for name, description in braille.getDisplayList(excludeNegativeChecks=False):
			driver = braille._getDisplayDriver(name)
			gmap = driver.gestureMap
			if not gmap:
				continue

			with fakeInitializedDisplayDriver(driver):
				for cls, gesture, scriptName in gmap.getScriptsForAllGestures():
					if cls is not globalCommands.GlobalCommands or not gesture.startswith("br"):
						continue
					# Make sure the gesture matches the regular expression (i.e. check the identifier validity).
					gestureMatch = braille.BrailleDisplayGesture.ID_PARTS_REGEX.match(gesture)
					self.assertIsNotNone(gestureMatch)
					driverName, model, id = gestureMatch.groups()
					# The driver name in the gesture identifier is in lower case.
					# It should match the name of the driver for which the gesture map is investigated.
					self.assertEqual(driverName, name.lower())
					keys = id.split("+")
					print(scriptName)
					gestureToScriptTestHelper(self, keys, scriptName, model=model, source=name)

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
		# Test whether all expected modifier gestures are retrieved from the map.
		modifierGestures = [(keys, modifiers) for keys, modifiers in braille.handler.display._getModifierGestures()]
		self.assertIn((set(["fakecontrol"]), set(["control"])), modifierGestures)
		self.assertIn((set(["fakeescape", "fakealt"]), set(["leftWindows"])), modifierGestures)
		self.assertIn((set(["fakeshift"]), set(["shift"])), modifierGestures)
		self.assertIn((set(["fakealt"]), set(["alt"])), modifierGestures)
		self.assertNotIn((set(["fakeinsert"]), set(["NVDA"])), modifierGestures)

		gestureToScriptTestHelper(self, ["fakeControl","fakeEscape"], "kb:control+escape")
		# fakeAlt+fakeEscape is assigned to windows
		gestureToScriptTestHelper(self, ["fakeAlt","fakeControl","fakeEscape"], "kb:control+leftwindows")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeControl","fakeTab"], "kb:alt+control+tab")
		# Alt with arrow keys
		gestureToScriptTestHelper(self, ["fakeAlt","fakeUp"], "kb:alt+uparrow")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeDown"], "kb:alt+downarrow")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeLeft"], "kb:alt+leftarrow")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeRight"], "kb:alt+rightarrow")
		# Control with arrow keys
		gestureToScriptTestHelper(self, ["fakeControl","fakeUp"], "kb:control+uparrow")
		gestureToScriptTestHelper(self, ["fakeControl","fakeDown"], "kb:control+downarrow")
		gestureToScriptTestHelper(self, ["fakeControl","fakeLeft"], "kb:control+leftarrow")
		gestureToScriptTestHelper(self, ["fakeControl","fakeRight"], "kb:control+rightarrow")
		# Shift with arrow key combinations are defined in the gesture map.
		gestureToScriptTestHelper(self, ["fakeShift","fakeUp"], "kb:control+home")
		gestureToScriptTestHelper(self, ["fakeShift","fakeDown"], "kb:control+end")
		gestureToScriptTestHelper(self, ["fakeShift","fakeLeft"], "kb:home")
		gestureToScriptTestHelper(self, ["fakeShift","fakeRight"], "kb:end")

	def test_combinationsWithAddedGestures(self):
		"""
		Tests combined emulations against a combination of the default gesture map for L{brailleDisplayprovider.BrailleDisplay}
		and a custom user gesture map with only additions.
		"""
		inputCore.manager.userGestureMap.update({
			"globalCommands.GlobalCommands": {
				"kb:NVDA": ("br(noBraille):fakeInsert",),
				"kb:leftWindows": ("br(noBraille):fakeWindows",),
			}
		})
		# Test whether all expected modifier gestures are retrieved from the maps.
		modifierGestures = [(keys, modifiers) for keys, modifiers in braille.handler.display._getModifierGestures()]
		self.assertIn((set(["fakecontrol"]), set(["control"])), modifierGestures)
		self.assertIn((set(["fakeescape", "fakealt"]), set(["leftWindows"])), modifierGestures)
		self.assertIn((set(["fakeshift"]), set(["shift"])), modifierGestures)
		self.assertIn((set(["fakealt"]), set(["alt"])), modifierGestures)
		self.assertIn((set(["fakeinsert"]), set(["NVDA"])), modifierGestures)

		# fakeAlt+fakeEscape is assigned to windows in the default map
		gestureToScriptTestHelper(self, ["fakeAlt","fakeControl","fakeEscape"], "kb:control+leftwindows")
		# fakeWindows is assigned to windows in the user gesture map
		gestureToScriptTestHelper(self, ["fakeWindows","fakeControl"], "kb:control+leftwindows")
		# NVDA with arrow keys
		gestureToScriptTestHelper(self, ["fakeInsert","fakeUp"], "kb:nvda+uparrow")
		gestureToScriptTestHelper(self, ["fakeInsert","fakeDown"], "kb:downarrow+nvda")
		gestureToScriptTestHelper(self, ["fakeInsert","fakeLeft"], "kb:leftarrow+nvda")
		gestureToScriptTestHelper(self, ["fakeInsert","fakeRight"], "kb:nvda+rightarrow")
		# Windows with arrow keys
		gestureToScriptTestHelper(self, ["fakeWindows","fakeUp"], "kb:leftwindows+uparrow")
		gestureToScriptTestHelper(self, ["fakeWindows","fakeDown"], "kb:downarrow+leftwindows")
		gestureToScriptTestHelper(self, ["fakeWindows","fakeLeft"], "kb:leftarrow+leftwindows")
		gestureToScriptTestHelper(self, ["fakeWindows","fakeRight"], "kb:leftwindows+rightarrow")

	def test_combinationsWithRemovedGestures(self):
		"""
		Tests combined emulations against a combination of the default gesture map for L{brailleDisplayprovider.BrailleDisplay}
		and a custom user gesture map that unbinds some of the gestures in that default map.
		"""
		inputCore.manager.userGestureMap.update({
			"globalCommands.GlobalCommands": {
				None: (
					"br(noBraille):fakeControl",
					"br(noBraille):fakeUp",
				),
			}
		})
		# Test whether all expected modifier gestures are retrieved from the maps.
		modifierGestures = [(keys, modifiers) for keys, modifiers in braille.handler.display._getModifierGestures()]
		self.assertNotIn((set(["fakecontrol"]), set(["control"])), modifierGestures)
		self.assertIn((set(["fakeescape", "fakealt"]), set(["leftWindows"])), modifierGestures)
		self.assertIn((set(["fakeshift"]), set(["shift"])), modifierGestures)
		self.assertIn((set(["fakealt"]), set(["alt"])), modifierGestures)
		self.assertNotIn((set(["fakeinsert"]), set(["NVDA"])), modifierGestures)

		gestureToScriptTestHelper(self, ["fakeControl"], None)
		gestureToScriptTestHelper(self, ["fakeUp"], None)
		gestureToScriptTestHelper(self, ["fakeControl","fakeEscape"], None)
		# fakeControl+fakeTab is still assigned to windows+d
		gestureToScriptTestHelper(self, ["fakeAlt","fakeControl","fakeTab"], "kb:alt+d+windows")
		# Control with arrow keys should no longer work
		gestureToScriptTestHelper(self, ["fakeControl","fakeUp"], None)
		gestureToScriptTestHelper(self, ["fakeControl","fakeDown"], None)
		gestureToScriptTestHelper(self, ["fakeControl","fakeLeft"], None)
		gestureToScriptTestHelper(self, ["fakeControl","fakeRight"], None)
		# Alt with arrow keys should work, exept for upArrow which is unbound by the user map.
		gestureToScriptTestHelper(self, ["fakeAlt","fakeUp"], None)
		gestureToScriptTestHelper(self, ["fakeAlt","fakeDown"], "kb:alt+downarrow")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeLeft"], "kb:alt+leftarrow")
		gestureToScriptTestHelper(self, ["fakeAlt","fakeRight"], "kb:alt+rightarrow")
		# Shift with arrow key combinations are defined in the gesture map.
		gestureToScriptTestHelper(self, ["fakeShift","fakeUp"], "kb:control+home")
		gestureToScriptTestHelper(self, ["fakeShift","fakeDown"], "kb:control+end")
		gestureToScriptTestHelper(self, ["fakeShift","fakeLeft"], "kb:home")
		gestureToScriptTestHelper(self, ["fakeShift","fakeRight"], "kb:end")

