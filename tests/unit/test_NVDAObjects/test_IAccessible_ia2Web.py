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

import controlTypes
import IAccessibleHandler  # noqa: F401  # Break the NVDAObjects.IAccessible circular import.
from NVDAObjects.IAccessible import IAccessible
from NVDAObjects.IAccessible.ia2Web import Ia2Web, Math


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


class _MockIa2Web(Ia2Web):
	windowHandle = 0
	processID = 0
	appModule = Mock()

	def __init__(
		self,
		role: controlTypes.Role,
		parent: SimpleNamespace | None = None,
		ia2Attributes: dict[str, str] | None = None,
	):
		self.role = role
		self.parent = parent
		self.IA2Attributes = ia2Attributes or {}
		self.linkType = None


class TestIa2WebStates(unittest.TestCase):
	def test_spinbuttonInheritsReadonlyFromReadonlyInputAncestor(self):
		inputAncestor = SimpleNamespace(
			role=controlTypes.Role.GROUPING,
			states={controlTypes.State.READONLY, controlTypes.State.FOCUSABLE},
			IA2Attributes={"tag": "input"},
		)
		groupingWrapper1 = SimpleNamespace(
			role=controlTypes.Role.GROUPING,
			states=set(),
			parent=inputAncestor,
			IA2Attributes={"tag": "div"},
		)
		groupingWrapper2 = SimpleNamespace(
			role=controlTypes.Role.GROUPING,
			states=set(),
			parent=groupingWrapper1,
			IA2Attributes={"tag": "div"},
		)
		spinObj = _MockIa2Web(
			role=controlTypes.Role.SPINBUTTON,
			parent=groupingWrapper2,
			ia2Attributes={"tag": "span"},
		)

		with unittest.mock.patch.object(
			IAccessible,
			"states",
			new_callable=unittest.mock.PropertyMock,
		) as mockStates:
			mockStates.return_value = {controlTypes.State.FOCUSABLE}
			resultStates = spinObj._get_states()

		self.assertIn(controlTypes.State.READONLY, resultStates)

	def test_spinbuttonDoesNotInheritReadonlyWhenAncestorNotReadonly(self):
		inputAncestor = SimpleNamespace(
			role=controlTypes.Role.GROUPING,
			states={controlTypes.State.FOCUSABLE},
			IA2Attributes={"tag": "input"},
		)
		sectionWrapper = SimpleNamespace(
			role=controlTypes.Role.SECTION,
			states=set(),
			parent=inputAncestor,
			IA2Attributes={"tag": "div"},
		)
		spinObj = _MockIa2Web(
			role=controlTypes.Role.SPINBUTTON,
			parent=sectionWrapper,
			ia2Attributes={"tag": "span"},
		)

		with unittest.mock.patch.object(
			IAccessible,
			"states",
			new_callable=unittest.mock.PropertyMock,
		) as mockStates:
			mockStates.return_value = {controlTypes.State.FOCUSABLE}
			resultStates = spinObj._get_states()

		self.assertNotIn(controlTypes.State.READONLY, resultStates)

	def test_spinbuttonDoesNotInheritReadonlyFromDocument(self):
		docAncestor = SimpleNamespace(
			role=controlTypes.Role.DOCUMENT,
			states={controlTypes.State.READONLY},
			IA2Attributes={"tag": "#document"},
		)
		spinObj = _MockIa2Web(
			role=controlTypes.Role.SPINBUTTON,
			parent=docAncestor,
			ia2Attributes={"tag": "div"},
		)

		with unittest.mock.patch.object(
			IAccessible,
			"states",
			new_callable=unittest.mock.PropertyMock,
		) as mockStates:
			mockStates.return_value = {controlTypes.State.FOCUSABLE}
			resultStates = spinObj._get_states()

		self.assertNotIn(controlTypes.State.READONLY, resultStates)


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
