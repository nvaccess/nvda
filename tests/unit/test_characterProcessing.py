# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2020 NV Access Limited

"""Unit tests for the characterProcessing module.
"""

import unittest
import re
from characterProcessing import SpeechSymbolProcessor
from characterProcessing import SymbolLevel
from characterProcessing import processSpeechSymbols as process


class TestComplex(unittest.TestCase):
	"""Test the complex symbols rules.
	"""

	def _replace_cb(self, replacement, name=None):
		"""Return a regexp callback which replaces matches of the given
		group name (or all groups if no name is given) with the
		replacement string, with support for replacement of group
		references.
		"""
		def replace(m):
			if name is None or m.lastgroup == name:
				return SpeechSymbolProcessor._replaceGroups(self, m, replacement)
			return m.group()
		return replace

	def _replace(self, string, pattern, replacement, name=None):
		"""Perform a pattern-based replacement on a string, for the
		given named group (or all groups if no name is given), with
		support for replacement of group references.
		"""
		regexp = re.compile(pattern, re.UNICODE)
		return regexp.sub(self._replace_cb(replacement, name), string)

	def test_group_replacement(self):
		"""Test that plain text gets properly replaced
		"""
		replaced = self._replace(
			string="1",
			pattern=r"(\d)",
			replacement="a"
		)
		self.assertEqual(replaced, "a")

	def test_backslash_replacement(self):
		"""Test that backslashes get properly replaced
		"""
		replaced = self._replace(
			string="1",
			pattern=r"(\d)",
			replacement=r"\\"
		)
		self.assertEqual(replaced, "\\")

	def test_double_backslash_replacement(self):
		"""Test that double backslashes get properly replaced
		"""
		replaced = self._replace(
			string="1",
			pattern=r"(\d)",
			replacement=r"\\\\"
		)
		self.assertEqual(replaced, r"\\")

	def test_unknown_escape(self):
		"""Test that a non-supported escaped character (i.e. not \\1,
		\\2, ... \\9 and \\\\) in the replacement raises an error
		"""
		with self.assertRaises(LookupError):
			self._replace(
				string="1",
				pattern=r"(\d)",
				replacement=r"\a"
			)

	def test_missing_group(self):
		"""Test that a reference in the replacement to an non-existing
		group raises an error
		"""
		with self.assertRaises(IndexError):
			self._replace(
				string="1",
				pattern=r"(\d)",
				replacement=r"\2"
			)

	def test_unterminated_escape(self):
		"""Test that an escape at the end of replacement raises an
		error, since there is nothing to be escaped there
		"""
		with self.assertRaises(LookupError):
			self._replace(
				string="1",
				pattern=r"(\d)",
				replacement="\\"
			)

	def test_group_replacements(self):
		"""Test that group references get properly replaced
		"""
		replaced = self._replace(
			string="bar.BAT",
			pattern=r"(([a-z]*)\.([A-Z]*))",
			replacement=r"\2>\1"
		)
		self.assertEqual(replaced, "BAT>bar")

	def test_multiple_group_replacement(self):
		"""Test that group indexing is correct with multiple groups
		"""
		replaced = self._replace(
			string="bar.BAT",
			pattern=r"(baz)|(?P<foo>([a-z]*)\.([A-Z]*))",
			replacement=r"\2>\1",
			name="foo"
		)
		self.assertEqual(replaced, "BAT>bar")

	def test_engine(self):
		"""Test inclusion of group replacement in engine
		"""
		replaced = process("fr_FR", "Le 03.04.05.", SymbolLevel.ALL)
		self.assertEqual(replaced, "Le  03 point 04 point 05  point.")
		replaced = process("fr_FR", "Le 03/04/05.", SymbolLevel.ALL)
		self.assertEqual(replaced, "Le  03 barre oblique 04 barre oblique 05  point.")
