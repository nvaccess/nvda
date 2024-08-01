# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 NV Access Limited, Cyrille Bougot

"""Unit tests for the speech.shortcutKeys module."""

import unittest
from unittest.mock import patch

from speech.shortcutKeys import (
	_getKeyboardShortcutSpeech,
	getKeyboardShortcutsSpeech,
)
import speech.shortcutKeys  # noqa F401 - Used by unittest.mock.patch
from speech.commands import CharacterModeCommand


class Test_getKeyboardShortcutSpeech(unittest.TestCase):
	@patch("speech.shortcutKeys.shouldUseSpellingFunctionality", lambda: True)
	def test_simpleLetterKey(self):
		"""A shortcut consisting in only one letter."""

		expected = repr(
			[
				CharacterModeCommand(True),
				"A",
				CharacterModeCommand(False),
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="A",
		)
		self.assertEqual(repr(output), expected)

	@patch("speech.shortcutKeys.shouldUseSpellingFunctionality", lambda: False)
	def test_simpleLetterKeyWithSpellingFunctionalityDisabled(self):
		"""A shortcut consisting in only one letter in the case where "Use spelling functionality" is disabled
		(see #15566).
		"""

		expected = repr(["A"])
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="A",
		)
		self.assertEqual(repr(output), expected)

	def test_simpleSymbolKey(self):
		"""A shortcut consisting in only one symbol present in symbols.dic."""

		expected = repr(
			[
				"question",
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="?",
		)
		self.assertEqual(repr(output), expected)

	def test_simpleKeyName(self):
		"""A shortcut consisting in only a key name."""

		expected = repr(
			[
				"Space",
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="Space",
		)
		self.assertEqual(repr(output), expected)

	@patch("speech.shortcutKeys.shouldUseSpellingFunctionality", lambda: True)
	def test_modifiersAndLetterKey(self):
		"""A shortcut consisting in modifiers and a letter key."""

		expected = repr(
			[
				"Ctrl",
				"+",
				"Shift",
				"+",
				CharacterModeCommand(True),
				"A",
				CharacterModeCommand(False),
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="Ctrl+Shift+A",
		)
		self.assertEqual(repr(output), expected)

	def test_modifierAndSymbolKey(self):
		"""A shortcut consisting in modifiers and a symbol present in symbols.dic."""

		expected = repr(
			[
				"Ctrl",
				"+",
				"slash",
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="Ctrl+/",
		)
		self.assertEqual(repr(output), expected)

	def test_modifierAndPlusKey(self):
		"""A shortcut consisting in modifiers and the + (plus) key in last position."""

		expected = repr(
			[
				"Ctrl",
				"+",
				"plus",
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="Ctrl++",
		)
		self.assertEqual(repr(output), expected)

	def test_modifierAndPlusKeyDescription(self):
		"""A shortcut consisting in a modifier and the description of the + (plus) key both joined with
		a plus surrounded by spaces. (found in Windows Magnifier)
		"""

		expected = repr(
			[
				"Touche de logo Windows",
				" + ",
				"Plus (+)",
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="Touche de logo Windows + Plus (+)",
		)
		self.assertEqual(repr(output), expected)

	@patch("speech.shortcutKeys.shouldUseSpellingFunctionality", lambda: True)
	def test_sequentialShortcutCombiningSpacesAndCommas(self):
		"""A sequential shortcut found in ribbons (e.g. Word)."""

		expected = repr(
			[
				"Alt",
				", ",
				CharacterModeCommand(True),
				"L",
				CharacterModeCommand(False),
				", ",
				CharacterModeCommand(True),
				"M",
				CharacterModeCommand(False),
				" ",
				CharacterModeCommand(True),
				"F",
				CharacterModeCommand(False),
			],
		)
		output = _getKeyboardShortcutSpeech(
			keyboardShortcut="Alt, L, M F",
		)
		self.assertEqual(repr(output), expected)


class Test_getKeyboardShortcutsSpeech(unittest.TestCase):
	@patch("speech.shortcutKeys.shouldUseSpellingFunctionality", lambda: True)
	def test_twoShortcutKeys(self):
		"""A shortcut key indication indicating two shortcut keys (a sequential one and a simultaneous one)
		as found in ribbons (e.g. Word).
		"""

		expected = repr(
			[
				"Alt, ",
				CharacterModeCommand(True),
				"L",
				CharacterModeCommand(False),
				", ",
				CharacterModeCommand(True),
				"C",
				CharacterModeCommand(False),
				"  Ctrl+",
				CharacterModeCommand(True),
				"C",
				CharacterModeCommand(False),
			],
		)
		output = getKeyboardShortcutsSpeech(
			keyboardShortcutsStr="Alt, L, C  Ctrl+C",
		)
		self.assertEqual(repr(output), expected)
