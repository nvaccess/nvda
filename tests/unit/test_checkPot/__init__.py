# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""Unit tests for the checkPot test."""

from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import os.path
import unittest
from typing import Tuple


class TestCheckPot(unittest.TestCase):
	"""Tests that checkPot works as expected."""

	def setUp(self):
		from ... import checkPot
		self.checkPot = checkPot
		self.saved_EXPECTED_MESSAGES_WITHOUT_COMMENTS = checkPot.EXPECTED_MESSAGES_WITHOUT_COMMENTS
		checkPot.EXPECTED_MESSAGES_WITHOUT_COMMENTS = {
			"Expected message without comment #1",
			"Expected message without comment #2",
		}

	def tearDown(self):
		self.checkPot.EXPECTED_MESSAGES_WITHOUT_COMMENTS = self.saved_EXPECTED_MESSAGES_WITHOUT_COMMENTS

	def doCheckPot(self, fileName: str) -> Tuple[int, str]:
		"""Run checkPot against the specified test POT file and returns its error count and status line."""
		filePath = os.path.join(os.path.dirname(__file__), fileName)
		bufOut = StringIO()
		bufErr = StringIO()
		with redirect_stdout(bufOut), redirect_stderr(bufErr):
			errorCount = self.checkPot.checkPot(filePath)
		self.assertTrue(bufOut.tell(), "No standard output")
		self.assertFalse(bufErr.tell(), "Non-empty standard error output")
		outLines = bufOut.getvalue().split("\n")
		self.assertGreaterEqual(len(outLines), 2, "Less than two lines of standard output")
		self.assertFalse(outLines[-1], "Standard output does not end with an empty line.")
		statusLine = outLines[-2]
		return errorCount, statusLine

	def test_checkPot_allOk(self):
		"""Test that no error is reported when every message has translators comment."""
		self.assertEqual(
			self.doCheckPot("allOk.pot"),
			(
				2,
				(
					"0 errors, 0 unexpected successes, 0 expected errors, "
					"2 messages marked as expected errors not present in the source code"
				)
			),
			"checkPot error count and/or status message do not meet expectations."
		)

	def test_checkPot_firstMessage(self):
		"""Test that missing translators comment on the first message are reported."""
		self.assertEqual(
			self.doCheckPot("firstMessage.pot"),
			(
				3,
				(
					"1 errors, 0 unexpected successes, 0 expected errors, "
					"2 messages marked as expected errors not present in the source code"
				)
			),
			"checkPot error count and/or status message do not meet expectations."
		)

	def test_checkPot_lastMessage(self):
		"""Test that missing translators comment on the last message are reported."""
		self.assertEqual(
			self.doCheckPot("lastMessage.pot"),
			(
				3,
				(
					"1 errors, 0 unexpected successes, 0 expected errors, "
					"2 messages marked as expected errors not present in the source code"
				)
			),
			"checkPot error count and/or status message do not meet expectations."
		)

	def test_checkPot_shortMessages(self):
		"""Test that missing translators comment on short messages are reported."""
		self.assertEqual(
			self.doCheckPot("shortMessages.pot"),
			(
				5,
				(
					"3 errors, 0 unexpected successes, 0 expected errors, "
					"2 messages marked as expected errors not present in the source code"
				)
			),
			"checkPot error count and/or status message do not meet expectations."
		)

	def test_checkPot_longMessages(self):
		"""Test that missing translators comment on long messages are reported."""
		self.assertEqual(
			self.doCheckPot("longMessages.pot"),
			(
				5,
				(
					"3 errors, 0 unexpected successes, 0 expected errors, "
					"2 messages marked as expected errors not present in the source code"
				)
			)
		)

	def test_checkPot_expectedErrors(self):
		"""Test that expected errors are reported as such."""
		self.assertEqual(
			self.doCheckPot("expectedErrors.pot"),
			(
				1,
				(
					"0 errors, 0 unexpected successes, 2 expected errors, "
					"1 messages marked as expected errors not present in the source code"
				)
			),
			"checkPot error count and/or status message do not meet expectations."
		)

	def test_checkPot_unexpectedSuccesses(self):
		"""Test that unexpected successes are reported as such."""
		self.assertEqual(
			self.doCheckPot("unexpectedSuccesses.pot"),
			(
				3,
				(
					"0 errors, 2 unexpected successes, 0 expected errors, "
					"1 messages marked as expected errors not present in the source code"
				)
			),
			"checkPot error count and/or status message do not meet expectations."
		)
