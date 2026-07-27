# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for NVDAObjects.UIA."""

import unittest
from unittest.mock import patch

import controlTypes
from NVDAObjects.UIA import MenuItem, UIA
import oleacc
import UIAHandler


class TestMenuItemStates(unittest.TestCase):
	def test_legacyCheckedStateFallback(self) -> None:
		menuItem = object.__new__(MenuItem)
		testCases = (
			(
				set(),
				oleacc.STATE_SYSTEM_CHECKED,
				{controlTypes.State.CHECKABLE, controlTypes.State.CHECKED},
				True,
			),
			(set(), 0, set(), True),
			(
				{controlTypes.State.CHECKABLE},
				oleacc.STATE_SYSTEM_CHECKED,
				{controlTypes.State.CHECKABLE},
				False,
			),
		)
		for uiaStates, legacyState, expectedStates, shouldReadLegacyState in testCases:
			with (
				self.subTest(
					uiaStates=uiaStates,
					legacyState=legacyState,
				),
				patch.object(UIA, "_get_states", return_value=uiaStates.copy()),
				patch.object(
					MenuItem,
					"_getUIACacheablePropertyValue_handlesCOMErrors",
					return_value=legacyState,
				) as getLegacyState,
			):
				self.assertEqual(expectedStates, menuItem._get_states())
				if shouldReadLegacyState:
					getLegacyState.assert_called_once_with(
						UIAHandler.UIA_LegacyIAccessibleStatePropertyId,
						True,
					)
				else:
					getLegacyState.assert_not_called()
