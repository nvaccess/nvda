# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2024 NV Access Limited, Noelia Ruiz Martínez, Leonard de Ruijter

"""Unit tests for the urlUtils submodule."""

import unittest
from source.utils.urlUtils import isSamePageURL


class TestIsSamePageURL(unittest.TestCase):
	def test_samePage_basic(self):
		self.assertTrue(isSamePageURL("http://example.com/page#section", "http://example.com/page"))

	def test_samePageBothHaveFragments(self):
		self.assertTrue(isSamePageURL("http://example.com/page#section", "http://example.com/page#main"))

	def test_differentPage(self):
		self.assertFalse(isSamePageURL("http://example.com/otherpage#section", "http://example.com/page"))

	def test_noFragment(self):
		self.assertTrue(isSamePageURL("http://example.com/page", "http://example.com/page"))

	def test_differentDomain(self):
		self.assertFalse(isSamePageURL("http://other.com/page#section", "http://example.com/page"))

	def test_emptyURLOnPage(self):
		self.assertFalse(isSamePageURL("", "http://example.com/page"))

	def test_emptyPageURL(self):
		self.assertFalse(isSamePageURL("http://example.com/page#section", ""))

	def test_differentScheme(self):
		self.assertTrue(isSamePageURL("http://example.com/page#section", "https://example.com/page"))

	def test_differentQuery(self):
		self.assertFalse(
			isSamePageURL("http://example.com/page?q=3#section", "http://example.com/page?q4#section"),
		)

	def test_fragmentHasPath(self):
		"""URLs whose fragments contain paths are not considered the same page."""
		self.assertFalse(isSamePageURL("http://example.com/page#fragment/path", "http://example.com/page"))

	def test_unusualCharacters(self):
		"""Test URLs with unusual characters."""
		self.assertTrue(isSamePageURL("http://example.com/page#%E2%9C%93", "http://example.com/page"))

	def test_externalLinkInLocalFile(self):
		"""Test external link in local file."""
		self.assertFalse(isSamePageURL("http://example.com/page#section", "file:///file"))

	def test_ftpScheme(self):
		"""Test URLs with different schemes like FTP."""
		self.assertFalse(isSamePageURL("ftp://example.com/page#section", "http://example.com/page"))

	def test_mailtoScheme(self):
		"""Test URLs with different schemes like mailto."""
		self.assertFalse(isSamePageURL("mailto://example.com/page#section", "http://example.com/page"))
