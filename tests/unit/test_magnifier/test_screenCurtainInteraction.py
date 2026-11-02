# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the interaction between the magnifier and the screen curtain."""

from unittest.mock import MagicMock, patch

from _magnifier.utils.types import Coordinates
from comtypes import COMError

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier


class TestStartWhenTrackingFails(_TestMagnifier):
	def _assertStartedAtCentre(self, error: Exception) -> None:
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(side_effect=error)
		with patch("_magnifier.magnifier.log") as mockLog:
			self.magnifier._startMagnifier()
		self.assertTrue(self.magnifier._isActive)
		expected = self.magnifier._clampCoordinates(
			Coordinates(self.screenWidth // 2, self.screenHeight // 2),
		)
		self.assertEqual(self.magnifier.currentCoordinates, expected)
		self.mock_hook_instance.start.assert_called_once()
		mockLog.warning.assert_called_once()

	def testStartSurvivesComError(self):
		self._assertStartedAtCentre(COMError(-2147023174, "RPC server unavailable", (None,) * 5))

	def testStartSurvivesLookupError(self):
		self._assertStartedAtCentre(LookupError("location unavailable"))

	def testStartDoesNotSwallowProgrammingErrors(self):
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(side_effect=AttributeError("bug"))
		with self.assertRaises(AttributeError):
			self.magnifier._startMagnifier()
