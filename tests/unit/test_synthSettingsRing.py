# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, SemTiOne
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for synthSettingsRing"""

import unittest

import config
from autoSettingsUtils.driverSetting import NumericDriverSetting
from synthSettingsRing import SynthSettingsRing

FAKE_SYNTH_NAME = "fakeSynthForRingTests"


class MockSynth:
	def __init__(self, name: str, supportedSettings):
		self.name = name
		self.supportedSettings = supportedSettings
		for s in supportedSettings:
			setattr(self, s.id, s.defaultVal)

	def isSupported(self, settingID: str) -> bool:
		return any(s.id == settingID for s in self.supportedSettings)

	def _get_initialSettingsRingSetting(self):
		supportedSettings = list(self.supportedSettings)
		if not self.isSupported("rate") and len(supportedSettings) > 0:
			for i, s in enumerate(supportedSettings):
				if s.availableInSettingsRing:
					return i
			return None
		for i, s in enumerate(supportedSettings):
			if s.id == "rate":
				return i
		return None

	initialSettingsRingSetting = property(_get_initialSettingsRingSetting)


def _makeRateAndPitchSynth(name: str = FAKE_SYNTH_NAME) -> MockSynth:
	rate = NumericDriverSetting("rate", "&Rate", availableInSettingsRing=True, defaultVal=50)
	pitch = NumericDriverSetting("pitch", "&Pitch", availableInSettingsRing=True, defaultVal=50)
	return MockSynth(name, [rate, pitch])


class InconsistentRateMockSynth(MockSynth):
	def isSupported(self, settingID: str) -> bool:
		if settingID == "rate":
			return True
		return super().isSupported(settingID)


def _makeInconsistentRateSynth(name: str = FAKE_SYNTH_NAME) -> InconsistentRateMockSynth:
	pitch = NumericDriverSetting("pitch", "&Pitch", availableInSettingsRing=True, defaultVal=50)
	return InconsistentRateMockSynth(name, [pitch])


class TestSynthSettingsRingRestoresLastSetting(unittest.TestCase):
	def setUp(self) -> None:
		config.conf["speech"][FAKE_SYNTH_NAME] = {}
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = ""

	def tearDown(self) -> None:
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = ""

	def test_freshRing_noSavedConfig_fallsBackToInitialSetting(self):
		synth = _makeRateAndPitchSynth()
		ring = SynthSettingsRing(synth)
		self.assertEqual(ring.currentSettingName, "Rate")

	def test_freshRing_noConfigSectionForSynth_doesNotRaise(self):
		synth = _makeRateAndPitchSynth(name="synthWithNoConfigSection")
		ring = SynthSettingsRing(synth)
		self.assertEqual(ring.currentSettingName, "Rate")

	def test_freshRing_withSavedConfig_matchingSetting_restoresPosition(self):
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = "pitch"
		synth = _makeRateAndPitchSynth()
		ring = SynthSettingsRing(synth)
		self.assertEqual(ring.currentSettingName, "Pitch")

	def test_freshRing_withSavedConfig_nonMatchingSetting_fallsBackToInitialSetting(self):
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = "someSettingThatDoesNotExist"
		synth = _makeRateAndPitchSynth()
		ring = SynthSettingsRing(synth)
		self.assertEqual(ring.currentSettingName, "Rate")

	def test_freshRing_withSavedConfig_nonMatching_andInconsistentDriver_doesNotRaise(self):
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = "someSettingThatDoesNotExist"
		synth = _makeInconsistentRateSynth()
		ring = SynthSettingsRing(synth)
		self.assertIsNone(ring.currentSettingName)

	def test_freshRing_withSavedConfig_notAvailableInRing_fallsBackToInitialSetting(self):
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = "pitch"
		rate = NumericDriverSetting("rate", "&Rate", availableInSettingsRing=True, defaultVal=50)
		pitch = NumericDriverSetting("pitch", "&Pitch", availableInSettingsRing=False, defaultVal=50)
		ring = SynthSettingsRing(MockSynth(FAKE_SYNTH_NAME, [rate, pitch]))
		self.assertEqual(ring.currentSettingName, "Rate")

	def test_updateSupportedSettings_afterEmptyRing_restoresFromSavedConfig(self):
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = "pitch"
		ring = SynthSettingsRing(MockSynth(FAKE_SYNTH_NAME, []))
		self.assertIsNone(ring.settings)
		ring.updateSupportedSettings(_makeRateAndPitchSynth())
		self.assertEqual(ring.currentSettingName, "Pitch")

	def test_next_persistsSettingID(self):
		synth = _makeRateAndPitchSynth()
		ring = SynthSettingsRing(synth)
		ring.next()
		self.assertEqual(
			config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"],
			"pitch",
		)

	def test_previous_persistsSettingID(self):
		synth = _makeRateAndPitchSynth()
		ring = SynthSettingsRing(synth)
		ring.previous()
		self.assertEqual(
			config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"],
			"pitch",
		)

	def test_inSessionUpdate_ignoresSavedConfig_usesInMemoryPosition(self):
		config.conf["speech"][FAKE_SYNTH_NAME]["lastSettingRingSettingID"] = "pitch"
		synth = _makeRateAndPitchSynth()
		ring = SynthSettingsRing(synth)
		self.assertEqual(ring.currentSettingName, "Pitch")
		ring.next()
		self.assertEqual(ring.currentSettingName, "Rate")
		ring.updateSupportedSettings(synth)
		self.assertEqual(ring.currentSettingName, "Rate")
