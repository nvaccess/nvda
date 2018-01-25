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

	def test_modifierFirst(self):
		gesture = KeyboardInputGesture.fromName("control+s")
		self.assertEqual(gesture.normalizedIdentifiers[-1], "kb:control+s")