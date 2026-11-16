# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Julien Cochuyt
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for keeping the magnifier running while NVDA reloads its configuration (#20786)."""

from unittest.mock import MagicMock, patch

import _magnifier
from _magnifier.fullscreenMagnifier import FullScreenMagnifier
from _magnifier.utils.types import Coordinates, Filter, FullScreenMode, MagnifiedView

from tests.unit.test_magnifier.test_magnifier import _TestMagnifier


class TestConfigReload(_TestMagnifier):
	def setUp(self):
		super().setUp()
		self.fullscreen = FullScreenMagnifier()
		self.fullscreen._startMagnifier()
		self.addCleanup(self._cleanUpFullscreen)
		patcher = patch.object(_magnifier, "_magnifier", self.fullscreen)
		patcher.start()
		self.addCleanup(patcher.stop)
		self.config = {
			"enabled": True,
			"view": MagnifiedView.FULLSCREEN,
			"zoom": 200,
			"filter": Filter.NORMAL,
			"mode": FullScreenMode.CENTER,
		}
		for target, getter in (
			("_magnifier.getEnabled", lambda: self.config["enabled"]),
			("_magnifier.getMagnifiedView", lambda: self.config["view"]),
			("_magnifier.magnifier.getZoomLevel", lambda: self.config["zoom"]),
			("_magnifier.magnifier.getPanStep", lambda: 10),
			("_magnifier.magnifier.getFilter", lambda: self.config["filter"]),
			("_magnifier.fullscreenMagnifier.getFullscreenMode", lambda: self.config["mode"]),
		):
			patcher = patch(target, side_effect=getter)
			patcher.start()
			self.addCleanup(patcher.stop)
		self.fullscreen._applyFilter = MagicMock()
		self.mock_hook_instance.reset_mock()
		self.MockMouseHook.reset_mock()
		self.mock_mag_fs.reset_mock()

	def _cleanUpFullscreen(self) -> None:
		self.fullscreen._stopTimer()
		self.fullscreen._isActive = False

	def _reload(self) -> None:
		_magnifier._suspendForConfigReset()
		_magnifier._resumeAfterConfigReset()

	def test_suspend_keepsTheMagnifiedViewOnScreen(self):
		_magnifier._suspendForConfigReset()
		self.assertIs(_magnifier._magnifier, self.fullscreen)
		self.assertTrue(self.fullscreen._isActive)
		self.assertIsNone(self.fullscreen._timer)
		self.mock_hook_instance.stop.assert_called_once()
		self.mock_mag_fs.MagUninitialize.assert_not_called()
		self.mock_mag_fs.MagSetFullscreenColorEffect.assert_not_called()
		self.mock_mag_fs.MagSetFullscreenTransform.assert_not_called()

	def test_reload_appliesTheSettingsInPlace(self):
		self.config["zoom"] = 400
		self.config["filter"] = Filter.INVERTED
		self.config["mode"] = FullScreenMode.RELATIVE
		self._reload()
		self.assertIs(_magnifier._magnifier, self.fullscreen)
		self.assertTrue(self.fullscreen._isActive)
		self.assertEqual(self.fullscreen.zoomLevel, 400)
		self.assertEqual(self.fullscreen.filterType, Filter.INVERTED)
		self.assertEqual(self.fullscreen._fullscreenMode, FullScreenMode.RELATIVE)
		self.fullscreen._applyFilter.assert_called_once()
		self.mock_mag_fs.MagUninitialize.assert_not_called()
		self.MockMouseHook.return_value.start.assert_called_once()
		self.assertTrue(self.fullscreen._timer.IsRunning())

	def test_reload_withSameFilter_doesNotReapplyIt(self):
		self._reload()
		self.fullscreen._applyFilter.assert_not_called()

	def test_reload_clampsTheViewToTheNewZoomLimits(self):
		with patch("_magnifier.magnifier.isTrueCentered", return_value=False):
			self.fullscreen.zoomLevel = 400
			self.fullscreen.currentCoordinates = Coordinates(0, 0)
			self._reload()
			expected = self.fullscreen._clampCoordinates(Coordinates(0, 0))
		self.assertEqual(self.fullscreen.currentCoordinates, expected)
		self.assertEqual(expected, Coordinates(self.screenWidth // 4, self.screenHeight // 4))

	def test_reload_whenDisabled_restartsThroughInitialize(self):
		self.config["enabled"] = False
		with (
			patch("_magnifier.terminate") as mockTerminate,
			patch("_magnifier.initialize") as mockInitialize,
		):
			self._reload()
		mockTerminate.assert_called_once()
		mockInitialize.assert_called_once()

	def test_reload_withAnotherView_restartsThroughInitialize(self):
		self.config["view"] = MagnifiedView.DOCKED
		with (
			patch("_magnifier.terminate") as mockTerminate,
			patch("_magnifier.initialize") as mockInitialize,
		):
			self._reload()
		mockTerminate.assert_called_once()
		mockInitialize.assert_called_once()

	def test_suspend_whenInactive_terminates(self):
		self.fullscreen._stopMagnifier()
		_magnifier._suspendForConfigReset()
		self.assertIsNone(_magnifier._magnifier)
		with patch("_magnifier.initialize") as mockInitialize:
			_magnifier._resumeAfterConfigReset()
		mockInitialize.assert_called_once()

	def test_suspend_duringScreenOverview_terminates(self):
		self.fullscreen._spotlightManager._spotlightIsActive = True
		_magnifier._suspendForConfigReset()
		self.assertIsNone(_magnifier._magnifier)
		self.assertFalse(self.fullscreen._isActive)

	def test_resume_afterStoppedByCurtain_waitsWithTheReloadedSettings(self):
		self._mockScreenCurtain(enabled=True)
		self.config["zoom"] = 400
		_magnifier._suspendForConfigReset()
		# The screen curtain stops the magnifier when it is enabled by the reloaded configuration.
		self.fullscreen.onScreenCurtainEnabled()
		with patch("_magnifier.initialize") as mockInitialize:
			_magnifier._resumeAfterConfigReset()
		mockInitialize.assert_not_called()
		self.assertIs(_magnifier._magnifier, self.fullscreen)
		self.assertFalse(self.fullscreen._isActive)
		self.assertTrue(self.fullscreen._screenCurtainIsActive)
		self.assertEqual(self.fullscreen.zoomLevel, 400)
		self.MockMouseHook.return_value.start.assert_not_called()

	def test_resume_afterStoppedByCurtain_whenDisabled_restartsThroughInitialize(self):
		self._mockScreenCurtain(enabled=True)
		self.config["enabled"] = False
		_magnifier._suspendForConfigReset()
		self.fullscreen.onScreenCurtainEnabled()
		with (
			patch("_magnifier.terminate") as mockTerminate,
			patch("_magnifier.initialize") as mockInitialize,
		):
			_magnifier._resumeAfterConfigReset()
		mockTerminate.assert_called_once()
		mockInitialize.assert_called_once()

	def test_resume_whenTheCurtainFailedToEnable_restartsThroughInitialize(self):
		self._mockScreenCurtain(enabled=False)
		_magnifier._suspendForConfigReset()
		# The curtain stops the magnifier before trying to enable itself, then fails.
		self.fullscreen.onScreenCurtainEnabled()
		with (
			patch("_magnifier.terminate") as mockTerminate,
			patch("_magnifier.initialize") as mockInitialize,
		):
			_magnifier._resumeAfterConfigReset()
		mockTerminate.assert_called_once()
		mockInitialize.assert_called_once()
