# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter

"""Unit tests for the urlUtils submodule."""

import unittest
from utils.urlUtils import isSamePageUrl


class TestIsSamePageUrl(unittest.TestCase):
	def test_samePage_basic(self):
		self.assertTrue(isSamePageUrl("http://example.com/page#section", "http://example.com/page"))

	def test_samePage_bothHaveFragments(self):
		self.assertTrue(isSamePageUrl("http://example.com/page#section", "http://example.com/page#main"))

	def test_differentPage(self):
		self.assertFalse(isSamePageUrl("http://example.com/otherpage#section", "http://example.com/page"))

	def test_noFragment(self):
		"""URLs without fragments are not considered the same page."""
		self.assertFalse(isSamePageUrl("http://example.com/page", "http://example.com/page"))

	def test_differentDomain(self):
		self.assertFalse(isSamePageUrl("http://other.com/page#section", "http://example.com/page"))

	def test_empty_urlOnPage(self):
		self.assertFalse(isSamePageUrl("", "http://example.com/page"))

	def test_empty_pageUrl(self):
		self.assertFalse(isSamePageUrl("http://example.com/page#section", ""))

	def test_differentScheme(self):
		self.assertFalse(isSamePageUrl("http://example.com/page#section", "https://example.com/page"))

	def test_differentQuery(self):
		self.assertFalse(
			isSamePageUrl("http://example.com/page?q=3#section", "http://example.com/page?q4#section"),
		)
