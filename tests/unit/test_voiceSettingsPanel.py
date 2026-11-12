# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Andrew Johnson
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for the voice settings panel when the synthesizer changes while it is open."""

import unittest
from collections import OrderedDict
from types import SimpleNamespace
from unittest.mock import patch

import config
import synthDriverHandler
import wx
from gui.settingsDialogs import VoiceSettingsPanel
from synthDriverHandler import SynthDriver, VoiceInfo


class _FakeSynthWithoutVariant(SynthDriver):
	name = "fakeSynthWithoutVariant"
	description = "Fake synth without variant"
	supportedSettings = (SynthDriver.RateSetting(), SynthDriver.VolumeSetting())

	def __init__(self):
		super().__init__()
		# The panel reads per-synth config, so register this synth's section as initSettings would.
		if not config.conf["speech"].isSet(self.name):
			config.conf["speech"][self.name] = {}
		config.conf["speech"][self.name].spec.update(self.getConfigSpec())

	@classmethod
	def check(cls):
		return True

	def speak(self, speechSequence):
		pass

	def cancel(self):
		pass

	def loadSettings(self, onlyChanged=False):
		pass

	def saveSettings(self):
		pass


class _FakeSynthWithVariant(_FakeSynthWithoutVariant):
	name = "fakeSynthWithVariant"
	description = "Fake synth with variant"
	supportedSettings = (SynthDriver.VariantSetting(), SynthDriver.RateSetting())
	variant = "v1"

	def _getAvailableVariants(self):
		return OrderedDict((v, VoiceInfo(v, v)) for v in ("v1", "v2"))


class Test_VoiceSettingsPanel_synthChange(unittest.TestCase):
	def setUp(self):
		self.app = wx.App()
		self.frame = wx.Frame(None)
		self._origSynth = synthDriverHandler._curSynth
		self._oldSynth = None
		synthDriverHandler._curSynth = _FakeSynthWithoutVariant()
		# Speech dictionaries are not initialised in unit tests, but the panel needs at least one.
		speechDictPatcher = patch(
			"speechDictHandler.listAvailableSpeechDictDefinitions",
			return_value=[SimpleNamespace(displayName="default", userVisible=True, enabled=True)],
		)
		speechDictPatcher.start()
		self.addCleanup(speechDictPatcher.stop)
		self.panel = VoiceSettingsPanel(self.frame)

	def tearDown(self):
		synthDriverHandler._curSynth = self._origSynth
		# Let fake synths die while wx can still queue the panel's refresh.
		self._oldSynth = None
		self.frame.Destroy()
		self.app.Destroy()

	def _switchSynth(self):
		"""Switch to a synth with different settings, keeping the old instance alive.
		Real synths (e.g. OneCore) can stay alive after termination until the garbage collector runs.
		"""
		self._oldSynth = synthDriverHandler._curSynth
		synthDriverHandler._curSynth = _FakeSynthWithVariant()

	def test_discardAfterSynthChange(self):
		"""Pressing cancel after the synth changed behind the open panel must not fail (#6469).
		For example, reverting to saved configuration with NVDA+control+r.
		"""
		self._switchSynth()
		self.panel.onDiscard()

	def test_controlsReflectNewSynthOnActivation(self):
		self._switchSynth()
		# What SpeechSettingsPanel.onChangeSynth does after the synth selection dialog closes.
		self.panel.onPanelActivated()
		self.assertEqual(set(self.panel.sizerDict), {"variant", "rate"})

	def test_layoutAfterSynthDies(self):
		"""Controls after the synth settings must not be drawn on top of them after a config reload (#6469)."""
		self.frame.Layout()
		synthDriverHandler._curSynth = _FakeSynthWithVariant()
		# The old synth is now garbage, so the panel's weakref callback queues refreshGui.
		self.app.ProcessPendingEvents()
		self.assertEqual(set(self.panel.sizerDict), {"variant", "rate"})
		self.assertGreater(
			self.panel.autoLanguageSwitchingCheckbox.GetPosition().y,
			self.panel.rateSlider.GetPosition().y,
		)
