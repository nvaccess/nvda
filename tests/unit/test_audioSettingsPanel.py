# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Yashu16
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the white noise volume control in the Audio settings panel."""

import unittest
from unittest.mock import patch

import config
import wx
from gui.settingsDialogs import AudioPanel


class Test_AudioPanel_whiteNoiseVolume(unittest.TestCase):
	def setUp(self):
		self.app = wx.App()
		self.frame = wx.Frame(None)
		self._origVolume = config.conf["audio"]["whiteNoiseVolume"]
		self.addCleanup(self._restoreVolume)
		# Unit tests have no audio hardware, so avoid enumerating real output devices.
		defaultDevice = config.conf.getConfigValidation(("audio", "outputDevice")).default
		devicePatcher = patch(
			"gui.settingsDialogs.mmdevice.getOutputDevices",
			return_value=[(defaultDevice, "Default")],
		)
		devicePatcher.start()
		self.addCleanup(devicePatcher.stop)
		# Saving the panel also applies sound split and ducking settings, which need audio hardware.
		for target in (
			"gui.settingsDialogs.audio._setSoundSplitState",
			"gui.settingsDialogs.audioDucking.setAudioDuckingMode",
		):
			patcher = patch(target)
			patcher.start()
			self.addCleanup(patcher.stop)

	def _restoreVolume(self):
		config.conf["audio"]["whiteNoiseVolume"] = self._origVolume
		self.frame.Destroy()
		self.app.Destroy()

	def test_controlShowsSavedVolume(self):
		"""The control is created and starts at the saved white noise volume."""
		config.conf["audio"]["whiteNoiseVolume"] = 25
		panel = AudioPanel(self.frame)
		self.assertEqual(panel.whiteNoiseVolumeEdit.GetValue(), 25)

	def test_controlRangeMatchesConfigSpec(self):
		"""The control accepts exactly the range that the configuration allows."""
		panel = AudioPanel(self.frame)
		validation = config.conf.getConfigValidation(("audio", "whiteNoiseVolume"))
		self.assertEqual(panel.whiteNoiseVolumeEdit.GetMin(), int(validation.kwargs["min"]))
		self.assertEqual(panel.whiteNoiseVolumeEdit.GetMax(), int(validation.kwargs["max"]))

	def test_saveWritesVolumeToConfig(self):
		"""Saving the panel stores the value from the control in the configuration."""
		config.conf["audio"]["whiteNoiseVolume"] = 0
		panel = AudioPanel(self.frame)
		panel.whiteNoiseVolumeEdit.SetValue(40)
		panel.onSave()
		self.assertEqual(config.conf["audio"]["whiteNoiseVolume"], 40)
