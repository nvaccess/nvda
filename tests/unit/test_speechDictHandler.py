# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the speechDicthandler module."""

import unittest

from speechDictHandler.types import SpeechDictEntry, EntryType


class TestSpeechDictEntry(unittest.TestCase):
	def test_entryTypeAnywhere_single(self):
		entry = SpeechDictEntry("β", "b", type=EntryType.ANYWHERE)
		expected = "b"
		actual = entry.sub("β")
		self.assertEqual(expected, actual)

	def test_entryTypeAnywhere_partOfString(self):
		entry = SpeechDictEntry("β", "b", type=EntryType.ANYWHERE)
		expected = "bα"
		actual = entry.sub("βα")
		self.assertEqual(expected, actual)

	def test_entryTypeWord_single(self):
		entry = SpeechDictEntry("β", "b", type=EntryType.WORD)
		expected = "b"
		actual = entry.sub("β")
		self.assertEqual(expected, actual)

	def test_entryTypeWord_partOfSentence(self):
		"""Word should match when surrounded by spaces."""
		entry = SpeechDictEntry("β", "b", type=EntryType.WORD)
		expected = "γ b α"
		actual = entry.sub("γ β α")
		self.assertEqual(expected, actual)

	def test_entryTypeWord_partOfWord(self):
		""" "Word should not match when part of another word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.WORD)
		expected = "βα"
		actual = entry.sub("βα")
		self.assertEqual(expected, actual)

	def test_entryTypePartOfWord_single(self):
		"""Should not match when not part of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.PART_OF_WORD)
		expected = "β"
		actual = entry.sub("β")
		self.assertEqual(expected, actual)

	def test_entryTypePartOfWord_partOfWord(self):
		entry = SpeechDictEntry("β", "b", type=EntryType.PART_OF_WORD)
		expected = "bα"
		actual = entry.sub("βα")
		self.assertEqual(expected, actual)

	def test_entryTypePartOfWord_partOfNonWord(self):
		"""Should match when part of a non-word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.PART_OF_WORD)
		expected = "β-"
		actual = entry.sub("β-")
		self.assertEqual(expected, actual)
