# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2021 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides custom asserts for system tests.
"""
from robot.libraries.BuiltIn import BuiltIn
builtIn: BuiltIn = BuiltIn()


# In Robot libraries, class name must match the name of the module. Use caps for both.
class AssertsLib:
	@staticmethod
	def strings_match(actual, expected, ignore_case=False, comparison="speech", message=""):
		message += '\n' if message else ''
		# Include expected text in robot test report so that the actual behavior
		# can be determined entirely from the report, even when the test passes.
		builtIn.log(
			f"{message}assert {comparison} string matches (ignore case: {ignore_case}):  '{expected}'",
			level="INFO"
		)
		try:
			builtIn.should_be_equal_as_strings(
				actual,
				expected,
				msg=f"{message}{comparison} Actual != Expected",
				ignore_case=ignore_case
			)
		except AssertionError:
			# Occasionally on assert failure the repr of the string makes it easier to determine the differences.
			builtIn.log(
				"repr of ({}) actual vs expected (ignore_case={}):\n{}\nvs\n{}".format(
					comparison,
					ignore_case,
					repr(actual),
					repr(expected)
				),
				level="DEBUG"
			)
			raise

	@staticmethod
	def speech_matches(actual, expected, ignore_case=False, message=""):
		AssertsLib.strings_match(actual, expected, ignore_case, comparison="speech", message=message)

	@staticmethod
	def braille_matches(actual, expected, ignore_case=False, message=""):
		AssertsLib.strings_match(actual, expected, ignore_case, comparison="braille", message=message)
