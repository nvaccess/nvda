#tests/unit/contentRecog/test_uwpOcr.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the contentRecog.uwpOcr module.
"""

import unittest
from contentRecog import uwpOcr

class TestGetInitialLanguage(unittest.TestCase):
	LANGS = ["de-DE", "en-US"]

	def test_fullLangFullMatch(self):
		actual = uwpOcr._getInitialLanguage("en_US", self.LANGS)
		self.assertEqual(actual, "en-US")

	def test_primaryLangPrimaryMatch(self):
		actual = uwpOcr._getInitialLanguage("en", self.LANGS)
		self.assertEqual(actual, "en-US")

	def test_fullLangPrimaryMatch(self):
		actual = uwpOcr._getInitialLanguage("en_AU", self.LANGS)
		self.assertEqual(actual, "en-US")

	def test_fullLangNoMatch(self):
		"""Test fall back to first available language if no match.
		"""
		actual = uwpOcr._getInitialLanguage("it_IT", self.LANGS)
		self.assertEqual(actual, "de-DE")

	def test_primaryLangNoMatch(self):
		"""Test fall back to first available language if no match.
		"""
		actual = uwpOcr._getInitialLanguage("it", self.LANGS)
		self.assertEqual(actual, "de-DE")
