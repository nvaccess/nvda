# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited, American Printing House for the Blind

"""Unit tests for Java Access Bridge"""

import unittest
from NVDAObjects import JAB


class TestJavaAccessBridge(unittest.TestCase):
	def test_plainTextNotModified(self):
		plainText = "Some plain text with no HTML tags."
		self.assertEqual(plainText, JAB._processHtml(plainText))

	def test_plainTextWithTagsNotModified(self):
		plainText = "<p>some <b>text</b>.</p>"
		self.assertEqual(plainText, JAB._processHtml(plainText))

	def test_regexNotModified(self):
		regexStr = "(<image[^>\\n]*)\\n([^>]*>)"
		self.assertEqual(regexStr, JAB._processHtml(regexStr))

	def test_htmlStringHasTagsRemoved(self):
		htmlStr = "<html><body><p>Some <b>bold</b> text.</p></body></html>"
		expected = "   Some  bold  text.   "
		self.assertEqual(expected, JAB._processHtml(htmlStr))
