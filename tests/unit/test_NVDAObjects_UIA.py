# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for NVDAObjects.UIA."""

import unittest
from unittest.mock import patch

from NVDAObjects.UIA import MenuItem, UIA


class TestMenuItemDescription(unittest.TestCase):
	def test_legacyDescriptionFallback(self) -> None:
		menuItem = object.__new__(MenuItem)
		menuItem.name = "Name"
		notSupportedValue = object()
		testCases = (
			("UIA description", "Legacy description", "UIA description", False),
			("", "Legacy description", "Legacy description", True),
			("Name", "Legacy description", "Legacy description", True),
			("Name", "Name", None, True),
			("Name", notSupportedValue, None, True),
		)
		for uiaDescription, legacyDescription, expectedDescription, shouldReadLegacyDescription in testCases:
			with (
				self.subTest(
					uiaDescription=uiaDescription,
					legacyDescription=legacyDescription,
				),
				patch.object(UIA, "_get_description", return_value=uiaDescription),
				patch.object(
					MenuItem,
					"_getUIACacheablePropertyValue_handlesCOMErrors",
					return_value=legacyDescription,
				) as getLegacyDescription,
			):
				self.assertEqual(expectedDescription, menuItem._get_description())
				if shouldReadLegacyDescription:
					getLegacyDescription.assert_called_once()
				else:
					getLegacyDescription.assert_not_called()
