# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

import unittest
from l10nUtil import _PoChecker


class TestGetInterpolations(unittest.TestCase):
	def setUp(self):
		# _PoChecker requires a po file path, but _getInterpolations only uses regexes and self._messageAlert
		# We'll mock _messageAlert to avoid side effects
		self.checker = _PoChecker.__new__(_PoChecker)
		self.checker._messageAlert = lambda msg, isError: setattr(self, "alerted", msg)
		self.checker.RE_UNNAMED_PERCENT = _PoChecker.RE_UNNAMED_PERCENT
		self.checker.RE_NAMED_PERCENT = _PoChecker.RE_NAMED_PERCENT
		self.checker.RE_FORMAT = _PoChecker.RE_FORMAT

	def test_unnamed_percent(self):
		text = "Hello %s, you have %d messages."
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%s", "%d"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_named_percent(self):
		text = "Hello %(user)s, you have %(count)d messages."
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, {"%(user)s", "%(count)d"})
		self.assertEqual(formats, set())

	def test_brace_format(self):
		text = "Hello {user}, you have {count:d} messages."
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, set())
		self.assertEqual(formats, {"{user}", "{count:d}"})

	def test_mixed_interpolations(self):
		text = "User: %(user)s, Count: %d, Name: {name}"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%d"])
		self.assertEqual(named, {"%(user)s"})
		self.assertEqual(formats, {"{name}"})

	def test_no_interpolations(self):
		text = "No interpolations here."
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_percent_escape(self):
		text = "Discount: 50%% off"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_brace_format_with_colon(self):
		text = "Value: {value:.2f}"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, set())
		self.assertEqual(formats, {"{value:.2f}"})

	def test_unspecified_positional_brace(self):
		text = "Value: {}"
		self.alerted = None
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, set())
		self.assertEqual(formats, {"{}"})
		self.assertEqual(self.alerted, "Unspecified positional argument in brace format")

	def test_complex_percent_formats(self):
		"""Test complex percent format specifiers like %10.2f and %-5s"""
		text = "Value: %10.2f, Name: %-5s"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%10.2f", "%-5s"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_mixed_percent_with_escaped(self):
		"""Test mix of real interpolations and escaped percents"""
		text = "Progress: %d%% complete, file: %s"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%d", "%s"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_various_format_specifiers(self):
		"""Test various format specifiers that should be recognized"""
		text = "Int: %d, Float: %f, String: %s, Hex: %x, Octal: %o"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%d", "%f", "%s", "%x", "%o"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_width_and_precision_formats(self):
		"""Test width and precision specifiers"""
		text = "Width: %10s, Precision: %.2f, Both: %10.2f, Left: %-10s"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%10s", "%.2f", "%10.2f", "%-10s"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_percent_literals_not_matched(self):
		"""Test that literal percent signs followed by words are not matched.
		Note: This tests a common gray area where interpolation could be valid.
		i.e.
		>>> "12.5% gray, 50% off, 100% complete" % (999, 123, 65)
		'12.5 999ray, 50 173ff, 100Aomplete'

		this was a deliberate choice as this form of formatting is rarely going to be a proper string interpolation.
		e.g. there are many english strings like this, that would be incorrectly treated as having 3 interpolations,
		and that the translation will have none.
		"""
		text = "12.5% gray, 50% off, 100% complete"
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, [])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

	def test_format_specifier_with_escaped_percent(self):
		"""Test format specifiers followed by escaped percent signs"""
		text = 'Value: "%s%%"'
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%s"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())

		text = 'Value: "%%%s"'
		unnamed, named, formats = self.checker._getInterpolations(text)
		self.assertEqual(unnamed, ["%s"])
		self.assertEqual(named, set())
		self.assertEqual(formats, set())


if __name__ == "__main__":
	unittest.main()
