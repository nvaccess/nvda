# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for Sound Split being disabled on secure screens (#19872)."""

import unittest
from unittest import mock

import audio
from gui import settingsDialogs


class TestSoundSplitOnSecureScreen(unittest.TestCase):
	def setUp(self):
		self.soundSplit = mock.MagicMock()
		patchers = (
			mock.patch.object(audio, "soundSplit", self.soundSplit),
			mock.patch.object(audio, "isRunningOnSecureDesktop", return_value=True),
		)
		for patcher in patchers:
			patcher.start()
			self.addCleanup(patcher.stop)

	def test_lifecycleDoesNotTouchApplicationVolumes(self):
		audio.initialize()
		audio.terminate()

		self.soundSplit.initialize.assert_not_called()
		self.soundSplit.terminate.assert_not_called()

	def test_settingStateIsANoOp(self):
		for state in audio.SoundSplitState:
			with self.subTest(state=state):
				self.assertEqual({}, audio._setSoundSplitState(state))
		self.soundSplit._setSoundSplitState.assert_not_called()

	def test_toggleReportsUnavailableOnSecureScreen(self):
		with mock.patch("ui.message") as message:
			audio._toggleSoundSplitState()

		self.soundSplit._toggleSoundSplitState.assert_not_called()
		message.assert_called_once_with("Action unavailable on secure screen")


class TestSoundSplitOnUserDesktop(unittest.TestCase):
	def setUp(self):
		self.soundSplit = mock.MagicMock()
		patchers = (
			mock.patch.object(audio, "soundSplit", self.soundSplit),
			mock.patch.object(audio, "isRunningOnSecureDesktop", return_value=False),
		)
		for patcher in patchers:
			patcher.start()
			self.addCleanup(patcher.stop)

	def test_lifecycleIsForwarded(self):
		audio.initialize()
		audio.terminate()

		self.soundSplit.initialize.assert_called_once_with()
		self.soundSplit.terminate.assert_called_once_with()

	def test_settingStateIsForwarded(self):
		self.soundSplit._setSoundSplitState.return_value = {"foundSessionWithNot2Channels": False}

		result = audio._setSoundSplitState(audio.SoundSplitState.NVDA_LEFT_APPS_RIGHT)

		self.soundSplit._setSoundSplitState.assert_called_once_with(
			audio.SoundSplitState.NVDA_LEFT_APPS_RIGHT,
			False,
		)
		self.assertEqual({"foundSessionWithNot2Channels": False}, result)

	def test_toggleIsForwarded(self):
		audio._toggleSoundSplitState()

		self.soundSplit._toggleSoundSplitState.assert_called_once_with()


@unittest.skipUnless(audio.SOUND_SPLIT_AVAILABLE, "Sound Split dependencies are unavailable")
class TestSoundSplitTerminateWithoutInitialize(unittest.TestCase):
	def test_terminateDoesNotRestoreVolumesWhenNotInitialized(self):
		soundSplit = audio.soundSplit
		with (
			mock.patch.object(soundSplit, "_audioSessionManager", None),
			mock.patch.object(soundSplit, "_setSoundSplitState") as setSoundSplitState,
			mock.patch.object(soundSplit, "_unregisterCallback") as unregisterCallback,
		):
			soundSplit.terminate()

		setSoundSplitState.assert_not_called()
		unregisterCallback.assert_not_called()


class TestSoundSplitSettingsOnSecureScreen(unittest.TestCase):
	def test_controlsAreDisabledWithExplanation(self):
		panel = mock.MagicMock()
		settingsSizerHelper = mock.MagicMock()
		unavailableText = mock.sentinel.unavailableText
		with (
			mock.patch.object(settingsDialogs.audio, "SOUND_SPLIT_AVAILABLE", True),
			mock.patch.object(settingsDialogs, "isRunningOnSecureDesktop", return_value=True),
			mock.patch.object(settingsDialogs.wx, "StaticText", return_value=unavailableText) as staticText,
		):
			settingsDialogs.AudioPanel._updateSoundSplitAvailability(panel, settingsSizerHelper)

		panel.soundSplitComboBox.Disable.assert_called_once_with()
		panel.soundSplitModesList.Disable.assert_called_once_with()
		staticText.assert_called_once_with(panel, label="Sound Split is unavailable on secure screens.")
		settingsSizerHelper.addItem.assert_called_once_with(unavailableText)

	def test_controlsStayEnabledOnUserDesktop(self):
		panel = mock.MagicMock()
		settingsSizerHelper = mock.MagicMock()
		with (
			mock.patch.object(settingsDialogs.audio, "SOUND_SPLIT_AVAILABLE", True),
			mock.patch.object(settingsDialogs, "isRunningOnSecureDesktop", return_value=False),
		):
			settingsDialogs.AudioPanel._updateSoundSplitAvailability(panel, settingsSizerHelper)

		panel.soundSplitComboBox.Disable.assert_not_called()
		panel.soundSplitModesList.Disable.assert_not_called()
		settingsSizerHelper.addItem.assert_not_called()
