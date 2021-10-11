# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited.

"""Unit tests for the displayString submodule.
"""

import unittest
from utils.displayString import DisplayStringEnum


class ExampleEnum(DisplayStringEnum):
	foo = "bar"
	lorem = "ipsum"

	@property
	def _displayStringLabels(self):
		return {self.foo: "this is foo from ExampleEnum"}


class TestDisplayStringEnum(unittest.TestCase):
	def test_displayString(self):
		self.assertEqual(ExampleEnum.foo.displayString, "this is foo from ExampleEnum")
		with self.assertRaises(KeyError):
			ExampleEnum.lorem.displayString
