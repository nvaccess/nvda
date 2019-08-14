# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2018 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This file provides general robot library functions for system tests.
This is in contrast with nvdaRobotLib.py which contains helpers related to starting and stopping NVDA for system
tests, or with systemTestSpy which contains methods for extracting information about NVDA's behaviour during system
tests.
"""
from robot.libraries.BuiltIn import BuiltIn
builtIn = BuiltIn()  # type: BuiltIn

def assert_strings_are_equal( actual, expected, ignore_case=False):
	try:
		builtIn.should_be_equal_as_strings(
			actual,
			expected,
			msg="Actual speech != Expected speech",
			ignore_case=ignore_case
		)
	except AssertionError:
		builtIn.log(
			"repr of actual vs expected (ignore_case={}):\n{}\nvs\n{}".format(
				ignore_case,
				repr(actual),
				repr(expected)
			)
		)
		raise


def catenate_double_space(*args):
	return "  ".join(args)