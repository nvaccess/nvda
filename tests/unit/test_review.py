# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the review module."""

import unittest
from unittest.mock import Mock, patch

import api
import review
from comtypes import COMError


class TestSetCurrentMode(unittest.TestCase):
	def test_modeOnlyChangeDoesNotFetchPosition(self) -> None:
		"""#20860: Without updating the review position, no position is fetched, so none can fail."""
		getPosition = Mock(side_effect=COMError(-2147467259, "Unspecified error", None))
		with (
			patch.object(review, "modes", [("object", "Object", getPosition)]),
			patch.object(review, "_currentMode", None),
			patch.object(api, "setReviewPosition") as setReviewPosition,
		):
			self.assertEqual(review.setCurrentMode("object", updateReviewPosition=False), "Object")
			self.assertEqual(review._currentMode, 0)
		getPosition.assert_not_called()
		setReviewPosition.assert_not_called()

	def test_modeChangeChecksPositionIsAvailable(self) -> None:
		getPosition = Mock(return_value=None)
		with (
			patch.object(review, "modes", [("object", "Object", getPosition)]),
			patch.object(review, "_currentMode", None),
			patch.object(api, "getNavigatorObject"),
			patch.object(api, "setReviewPosition") as setReviewPosition,
		):
			self.assertIsNone(review.setCurrentMode("object"))
			self.assertIsNone(review._currentMode)
		getPosition.assert_called_once()
		setReviewPosition.assert_not_called()

	def test_unknownModeRaises(self) -> None:
		with self.assertRaises(LookupError):
			review.setCurrentMode("invalid", updateReviewPosition=False)
