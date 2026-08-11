# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the keyboardHandler module."""

import unittest

import vkCodes
import winUser
from keyboardHandler import KeyboardInputGesture, getNVDAModifierKeys


class TestFromName(unittest.TestCase):
	"""Tests for L{KeyboardInputGesture.fromName}."""

	def test_mainKeyLast(self):
		gesture = KeyboardInputGesture.fromName("control+alt+upArrow")
		vk, ext = vkCodes.byName["uparrow"]
		self.assertEqual(gesture.vkCode, vk)
		self.assertEqual(gesture.isExtended, ext)
		self.assertEqual(
			gesture.modifiers,
			{(winUser.VK_CONTROL, False), (winUser.VK_MENU, False)},
		)

	def test_mainKeyNotLast(self):
		gesture = KeyboardInputGesture.fromName("alt+b+control")
		self.assertEqual(gesture.vkCode, ord("B"))
		self.assertEqual(
			gesture.modifiers,
			{(winUser.VK_CONTROL, False), (winUser.VK_MENU, False)},
		)

	def test_mainKeyFirst(self):
		gesture = KeyboardInputGesture.fromName("upArrow+control+alt")
		vk, ext = vkCodes.byName["uparrow"]
		self.assertEqual(gesture.vkCode, vk)
		self.assertEqual(gesture.isExtended, ext)
		self.assertEqual(
			gesture.modifiers,
			{(winUser.VK_CONTROL, False), (winUser.VK_MENU, False)},
		)

	def test_sameGestureRegardlessOfOrder(self):
		self.assertEqual(
			KeyboardInputGesture.fromName("alt+control+b").normalizedIdentifiers,
			KeyboardInputGesture.fromName("alt+b+control").normalizedIdentifiers,
		)

	def test_modifiersOnly(self):
		gesture = KeyboardInputGesture.fromName("control+alt")
		self.assertEqual(gesture.vkCode, winUser.VK_MENU)
		self.assertEqual(gesture.modifiers, {(winUser.VK_CONTROL, False)})

	def test_singleModifier(self):
		gesture = KeyboardInputGesture.fromName("alt")
		self.assertEqual(gesture.vkCode, winUser.VK_MENU)
		self.assertEqual(gesture.modifiers, set())

	def test_nvdaModifierWithMainKey(self):
		gesture = KeyboardInputGesture.fromName("NVDA+b")
		self.assertEqual(gesture.vkCode, ord("B"))
		self.assertIn(getNVDAModifierKeys()[0], gesture.modifiers)

	def test_multipleMainKeys(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("control+b+c")

	def test_duplicateMainKey(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("control+b+b")

	def test_unknownKeyName(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("control+bogus")

	def test_emptyName(self):
		with self.assertRaises(ValueError):
			KeyboardInputGesture.fromName("")
