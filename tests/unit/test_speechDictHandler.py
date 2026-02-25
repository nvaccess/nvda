# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the speechDictHandler module."""

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
		"""Word should not match when part of another word."""
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
		"""Should not match when part of a non-word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.PART_OF_WORD)
		expected = "β-"
		actual = entry.sub("β-")
		self.assertEqual(expected, actual)

	def test_entryTypeStartOfWord_single(self):
		"""Should not match when not part of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.START_OF_WORD)
		expected = "β"
		actual = entry.sub("β")
		self.assertEqual(expected, actual)

	def test_entryTypeStartOfWord_startOfWord(self):
		"""Should match at the start of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.START_OF_WORD)
		expected = "bα γ"
		actual = entry.sub("βα γ")
		self.assertEqual(expected, actual)

	def test_entryTypeStartOfWord_endOfWord(self):
		"""Should not match at the end of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.START_OF_WORD)
		expected = "αβ"
		actual = entry.sub("αβ")
		self.assertEqual(expected, actual)

	def test_entryTypeStartOfWord_middleOfWord(self):
		"""Should not match in the middle of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.START_OF_WORD)
		expected = "αβγ"
		actual = entry.sub("αβγ")
		self.assertEqual(expected, actual)

	def test_entryTypeEndOfWord_single(self):
		"""Should not match when not part of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.END_OF_WORD)
		expected = "β"
		actual = entry.sub("β")
		self.assertEqual(expected, actual)

	def test_entryTypeEndOfWord_endOfWord(self):
		"""Should match at the end of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.END_OF_WORD)
		expected = "γ αb"
		actual = entry.sub("γ αβ")
		self.assertEqual(expected, actual)

	def test_entryTypeEndOfWord_startOfWord(self):
		"""Should not match at the start of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.END_OF_WORD)
		expected = "βα"
		actual = entry.sub("βα")
		self.assertEqual(expected, actual)

	def test_entryTypeEndOfWord_middleOfWord(self):
		"""Should not match in the middle of a word."""
		entry = SpeechDictEntry("β", "b", type=EntryType.END_OF_WORD)
		expected = "αβγ"
		actual = entry.sub("αβγ")
		self.assertEqual(expected, actual)

	def test_entryTypeRegex_simplePattern(self):
		"""Should match using regex patterns."""
		entry = SpeechDictEntry(r"\d+", "number", type=EntryType.REGEXP)
		expected = "test number abc"
		actual = entry.sub("test 123 abc")
		self.assertEqual(expected, actual)

	def test_entryTypeRegex_captureGroups(self):
		"""Should support capture groups in replacement."""
		entry = SpeechDictEntry(r"(\w+) (\w+)", r"\2 \1", type=EntryType.REGEXP)
		expected = "world hello"
		actual = entry.sub("hello world")
		self.assertEqual(expected, actual)

	def test_entryTypeRegex_multipleMatches(self):
		"""Should replace all matches."""
		entry = SpeechDictEntry(r"\d", "X", type=EntryType.REGEXP)
		expected = "testXXX"
		actual = entry.sub("test123")
		self.assertEqual(expected, actual)

	def test_entryTypeRegex_noMatch(self):
		"""Should not modify text when pattern doesn't match."""
		entry = SpeechDictEntry(r"\d+", "number", type=EntryType.REGEXP)
		expected = "test abc"
		actual = entry.sub("test abc")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_simpleWildcard(self):
		"""Should match using Unix shell-style wildcards."""
		entry = SpeechDictEntry("test*", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test123")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_questionMark(self):
		"""Should match single character with ?."""
		entry = SpeechDictEntry("t?st", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_noMatch(self):
		"""Should not modify text when pattern doesn't match."""
		entry = SpeechDictEntry("hello*", "replaced", type=EntryType.UNIX)
		expected = "test"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_multipleWildcards(self):
		"""Should handle multiple wildcards."""
		entry = SpeechDictEntry("*β*", "b", type=EntryType.UNIX)
		expected = "b"
		actual = entry.sub("αβγ")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_characterSet(self):
		"""Should match using character sets [abc]."""
		entry = SpeechDictEntry("t[aeiou]st", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_characterSetNoMatch(self):
		"""Should not match when character set doesn't match."""
		entry = SpeechDictEntry("t[xyz]st", "replaced", type=EntryType.UNIX)
		expected = "test"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_characterRange(self):
		"""Should match using character ranges [a-z]."""
		entry = SpeechDictEntry("t[a-z]st", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_negatedCharacterSet(self):
		"""Should match using negated character sets [!abc]."""
		entry = SpeechDictEntry("t[!xyz]st", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_wildcardsInMiddle(self):
		"""Should handle wildcards in the middle of pattern."""
		entry = SpeechDictEntry("test*123", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test_abc_123")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_multipleQuestionMarks(self):
		"""Should handle multiple ? wildcards."""
		entry = SpeechDictEntry("t??t", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_emptyWildcard(self):
		"""Should match empty string with *."""
		entry = SpeechDictEntry("test*", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_partialMatch(self):
		"""Should match partial strings."""
		entry = SpeechDictEntry("*test", "replaced", type=EntryType.UNIX)
		expected = "replaced abc"
		actual = entry.sub("test abc")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_caseSensitive(self):
		"""Should be case sensitive by default."""
		entry = SpeechDictEntry("test*", "replaced", type=EntryType.UNIX, caseSensitive=True)
		expected = "TEST123"
		actual = entry.sub("TEST123")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_caseInsensitive(self):
		"""Should support case insensitive matching."""
		entry = SpeechDictEntry("test*", "replaced", type=EntryType.UNIX, caseSensitive=False)
		expected = "replaced"
		actual = entry.sub("TEST123")
		self.assertEqual(expected, actual)

	def test_entryTypeUnix_specialCharactersEscaped(self):
		"""Should handle patterns with dots and other regex special chars."""
		entry = SpeechDictEntry("test[.]txt", "replaced", type=EntryType.UNIX)
		expected = "replaced"
		actual = entry.sub("test.txt")
		self.assertEqual(expected, actual)
