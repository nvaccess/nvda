# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the interaction between the magnifier and the screen curtain."""

import unittest
from unittest.mock import MagicMock, patch

from _magnifier.utils.errorHandling import MagnifierStartError
from _magnifier.utils.types import Coordinates
from comtypes import COMError
from screenCurtain._screenCurtain import ScreenCurtain

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

	def testRestartFailureIsSpokenOnce(self):
		self.magnifier._screenCurtainIsActive = True
		self.magnifier._startMagnifier = MagicMock(side_effect=MagnifierStartError("x"))
		with (
			patch("_magnifier.magnifier.ui.message") as mockMessage,
			patch("_magnifier.magnifier.setEnabled"),
		):
			self.magnifier.onScreenCurtainDisabled()
		mockMessage.assert_called_once_with("x")


class TestRestartWithPersistentTrackingFailure(_TestMagnifier):
	"""Disabling the screen curtain must still succeed when the position lookup keeps failing.

	What the update loop does on the following timer ticks is the subject of #20992.
	"""

	def setUp(self):
		super().setUp()
		self.magnifier._screenCurtainIsActive = True
		self.magnifier._focusManager.getCurrentFocusCoordinates = MagicMock(
			side_effect=COMError(-2147023174, "RPC server unavailable", (None,) * 5),
		)
		self.magnifier._doUpdate = MagicMock()
		self.magnifier._startTimer = MagicMock()
		self.curtain = ScreenCurtain.__new__(ScreenCurtain)
		self.curtain._settings = {"enabled": True, "playToggleSounds": False, "warnOnLoad": False}
		self.curtain._enabled = True
		# Prevent __del__ from calling the real Magnification API after the patches are removed.
		self.addCleanup(setattr, self.curtain, "_enabled", False)
		for patcher in (
			patch("screenCurtain._screenCurtain.magnification"),
			patch("_magnifier.getMagnifier", return_value=self.magnifier),
			patch("_magnifier.magnifier.setEnabled"),
			patch("_magnifier.magnifier.log"),
		):
			patcher.start()
			self.addCleanup(patcher.stop)

	def testCurtainIsDisabledAndMagnifierRestartsAtCentre(self):
		with patch("_magnifier.magnifier.ui.message") as mockMessage:
			self.curtain.disable(persist=False)
		self.assertFalse(self.curtain.enabled)
		self.assertTrue(self.magnifier._isActive)
		expected = self.magnifier._clampCoordinates(
			Coordinates(self.screenWidth // 2, self.screenHeight // 2),
		)
		self.assertEqual(self.magnifier.currentCoordinates, expected)
		mockMessage.assert_not_called()


class TestScreenCurtainIsolatesMagnifier(unittest.TestCase):
	def setUp(self):
		self.curtain = ScreenCurtain.__new__(ScreenCurtain)
		self.curtain._settings = {"enabled": False, "playToggleSounds": False, "warnOnLoad": False}
		self.curtain._enabled = False
		# Prevent __del__ from calling the real Magnification API after the patches are removed.
		self.addCleanup(setattr, self.curtain, "_enabled", False)
		self.failingMagnifier = MagicMock()
		self.failingMagnifier.onScreenCurtainEnabled.side_effect = COMError(-1, "injected", (None,) * 5)
		self.failingMagnifier.onScreenCurtainDisabled.side_effect = COMError(-1, "injected", (None,) * 5)
		for patcher in (
			patch("screenCurtain._screenCurtain.magnification"),
			patch("screenCurtain._screenCurtain.isScreenFullyBlack", return_value=True),
			patch("_magnifier.getMagnifier", return_value=self.failingMagnifier),
		):
			patcher.start()
			self.addCleanup(patcher.stop)
		logPatcher = patch("screenCurtain._screenCurtain.log")
		self.mockLog = logPatcher.start()
		self.addCleanup(logPatcher.stop)

	def testDisableSurvivesMagnifierFailure(self):
		self.curtain._enabled = True
		self.curtain.disable(persist=False)
		self.assertFalse(self.curtain.enabled)
		self.mockLog.exception.assert_called_once()

	def testEnableSurvivesMagnifierFailure(self):
		self.curtain.enable(persist=False)
		self.assertTrue(self.curtain.enabled)
		self.mockLog.exception.assert_called_once()
