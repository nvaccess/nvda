#tests/unit/test_keyboardHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2018 NV Access Limited, Babbage B.V.

"""Unit tests for the keyboardHandler module.
"""

import unittest
from keyboardHandler import *

class TestKeyboardInputGestureFromNVDAKey(unittest.TestCase):

	def test_gestureFromNVDAKey(self):
		gesture = KeyboardInputGesture.fromName("NVDA")
		self.assertTrue(gesture.isNVDAModifierKey)

	def test_getNVDAModifierKeys(self):
		for vk, ext in getNVDAModifierKeys():
			gesture = KeyboardInputGesture(modifiers=[], vkCode=vk, scanCode=0, isExtended=ext)
			self.assertTrue(gesture.isNVDAModifierKey)

class TestKeyboardInputGestureFromName(unittest.TestCase):
	""""Tests several fromName cases as well as proper ordering and format of normalized identifiers.
	For refference, normalized gesture identifiers have their key names sorted alphabetically.
	"""

	def test_modifierFirst(self):
		gesture = KeyboardInputGesture.fromName("control+s")
		self.assertEqual(gesture.normalizedIdentifiers[-1], "kb:control+s")

	def test_modifierLast(self):
		gesture = KeyboardInputGesture.fromName("s+control")
		self.assertEqual(gesture.normalizedIdentifiers[-1], "kb:control+s")

	def test_testMultipleNonmodifiers(self):
		self.assertRaises(ValueError, KeyboardInputGesture.fromName, "control+s+a")

	def test_modifiersOnly(self):
		gesture = KeyboardInputGesture.fromName("control+alt+shift+nvda")
		self.assertEqual(gesture.normalizedIdentifiers[-1], "kb:alt+control+nvda+shift")

	def test_upperCase(self):
		gesture = KeyboardInputGesture.fromName("S")
		self.assertEqual(gesture.normalizedIdentifiers[-1], "kb:s+shift")

	def test_malformed(self):
		# ctrl is unsupported, one should use control.
		self.assertRaises(ValueError, KeyboardInputGesture.fromName, "ctrl+s")
