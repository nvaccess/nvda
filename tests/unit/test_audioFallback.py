# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited
# This file may be used under the terms of the GNU General Public License, version 2 or later.
# For more details see: https://www.gnu.org/licenses/gpl-2.0.html

import importlib
import sys
import unittest
from unittest import mock

import audio
from gui import settingsDialogs
from utils import mmdevice


class TestUnavailableSoundSplit(unittest.TestCase):
	def test_importHandlesUnavailablePycaw(self):
		soundSplit = audio.soundSplit
		soundSplitAvailable = audio.SOUND_SPLIT_AVAILABLE
		soundSplitModule = sys.modules.pop("audio.soundSplit", None)

		def restoreAudioModule() -> None:
			if soundSplitModule is not None:
				sys.modules["audio.soundSplit"] = soundSplitModule
			audio.soundSplit = soundSplit
			audio.SOUND_SPLIT_AVAILABLE = soundSplitAvailable

		self.addCleanup(restoreAudioModule)
		del audio.soundSplit
		with mock.patch.dict(sys.modules, {"pycaw.utils": None}):
			importlib.reload(audio)
		self.assertFalse(audio.SOUND_SPLIT_AVAILABLE)
		self.assertIsNone(audio.soundSplit)

	def test_lifecycleAndStateChangeAreNoOps(self):
		with mock.patch.object(audio, "soundSplit", None):
			audio.initialize()
			audio.terminate()
			self.assertEqual({}, audio._setSoundSplitState(audio.SoundSplitState.OFF))

	def test_toggleReportsUnavailable(self):
		with (
			mock.patch.object(audio, "soundSplit", None),
			mock.patch("ui.message") as message,
		):
			audio._toggleSoundSplitState()

			message.assert_called_once_with("Sound Split is unavailable.")


class TestUnavailableAudioDeviceEnumeration(unittest.TestCase):
	def test_importHandlesUnavailablePycaw(self):
		self.addCleanup(importlib.reload, mmdevice)
		with mock.patch.dict(sys.modules, {"pycaw.utils": None}):
			importlib.reload(mmdevice)
		self.assertIsNone(mmdevice.AudioUtilities)

	def test_noDevicesAreReturned(self):
		with mock.patch.object(mmdevice, "AudioUtilities", None):
			self.assertEqual([], list(mmdevice.getOutputDevices()))


class TestUnavailableSoundSplitSettings(unittest.TestCase):
	def test_controlsAreDisabledWithExplanation(self):
		panel = mock.MagicMock()
		settingsSizerHelper = mock.MagicMock()
		unavailableText = mock.sentinel.unavailableText
		with (
			mock.patch.object(settingsDialogs.audio, "SOUND_SPLIT_AVAILABLE", False),
			mock.patch.object(settingsDialogs.wx, "StaticText", return_value=unavailableText) as staticText,
		):
			settingsDialogs.AudioPanel._updateSoundSplitAvailability(
				panel,
				settingsSizerHelper,
			)

		panel.soundSplitComboBox.Disable.assert_called_once_with()
		panel.soundSplitModesList.Disable.assert_called_once_with()
		staticText.assert_called_once_with(
			panel,
			label="Sound Split is unavailable because required Windows audio components are missing.",
		)
		settingsSizerHelper.addItem.assert_called_once_with(unavailableText)
