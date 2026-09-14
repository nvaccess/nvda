# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for NVDAObjects.IAccessible.ia2Web."""

from types import SimpleNamespace  # noqa: I001
from typing import cast
import unittest
from unittest.mock import Mock

from comtypes import COMError
from comtypes.hresult import E_NOTIMPL

import IAccessibleHandler  # noqa: F401  # Break the NVDAObjects.IAccessible circular import.
from NVDAObjects.IAccessible.ia2Web import Math


def _makeMath(attributes: dict[str, str], children: list[SimpleNamespace] | None = None) -> Math:
	return cast(
		Math,
		SimpleNamespace(
			IA2Attributes=attributes,
			IAccessibleObject=Mock(),
			children=children or [],
			language=None,
		),
	)


class TestMathMlRetrieval(unittest.TestCase):
	def test_htmlRoleMathContentWithoutMathMlIsNotTreatedAsMathMl(self):
		math = _makeMath(
			{
				"tag": "span",
				"math": '<span aria-hidden="true">x + y</span>',
			},
		)
		math.IAccessibleObject.QueryInterface.return_value.attributesForNames.return_value = None

		with self.assertRaises(LookupError):
			Math._get_mathMl(math)

	def test_nativeMathContentUsesIa2MathAttribute(self):
		math = _makeMath(
			{
				"tag": "math",
				"math": "<mi>x</mi>",
			},
		)

		self.assertEqual("<math><mi>x</mi></math>", Math._get_mathMl(math))
		math.IAccessibleObject.QueryInterface.assert_not_called()

	def test_singleNativeMathChildDoesNotRequireISimpleDOM(self):
		childMathMl = "<math><mi>x</mi></math>"
		child = SimpleNamespace(
			IA2Attributes={"tag": "math"},
			mathMl=childMathMl,
		)
		math = _makeMath(
			{
				"tag": "span",
				"math": "<math><mi>x</mi></math>",
			},
			children=[child],
		)
		math.IAccessibleObject.QueryInterface.side_effect = COMError(E_NOTIMPL, "Not implemented", None)

		self.assertEqual(childMathMl, Math._get_mathMl(math))
