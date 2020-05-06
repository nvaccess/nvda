# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2020 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

"""This module provides custom asserts for system tests.
"""
from robot.libraries.BuiltIn import BuiltIn
builtIn: BuiltIn = BuiltIn()


# In Robot libraries, class name must match the name of the module. Use caps for both.
class AssertsLib:
	@staticmethod
	def strings_match(actual, expected, ignore_case=False):
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
