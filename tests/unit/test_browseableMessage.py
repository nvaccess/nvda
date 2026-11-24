# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, daarshnicsanjeev
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Tests for ui.browseableMessage line-level element wrapping (Issue #21181)."""

import unittest
from html import escape


class TestBrowseableMessageFormatting(unittest.TestCase):
	def test_plain_multiline_message_wrapped_in_divs(self):
		message = "1\n2\n3\n4\n5"
		lines = message.splitlines(keepends=True)
		divs = "".join(f"<div>{escape(line)}</div>" for line in lines)
		sanitized = f"<pre>{divs}</pre>"

		# Verify each line has its own <div> inside <pre>
		self.assertIn("<pre>", sanitized)
		self.assertIn("</pre>", sanitized)
		self.assertEqual(sanitized.count("<div>"), 5)
		self.assertEqual(sanitized.count("</div>"), 5)
		for line in ["1\n", "2\n", "3\n", "4\n", "5"]:
			self.assertIn(f"<div>{escape(line)}</div>", sanitized)

	def test_single_line_plain_message(self):
		message = "Single line message"
		lines = message.splitlines(keepends=True)
		divs = "".join(f"<div>{escape(line)}</div>" for line in lines)
		sanitized = f"<pre>{divs}</pre>"

		self.assertEqual(sanitized, "<pre><div>Single line message</div></pre>")

	def test_empty_plain_message(self):
		message = ""
		lines = message.splitlines(keepends=True)
		divs = "".join(f"<div>{escape(line)}</div>" for line in lines)
		sanitized = f"<pre>{divs}</pre>"

		self.assertEqual(sanitized, "<pre></pre>")
