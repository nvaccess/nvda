# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited

"""Unit tests for the synthDriverHandler
"""
import config
import globalVars
import languageHandler
import synthDriverHandler
from synthDrivers.oneCore import SynthDriver as OneCoreSynthDriver
from typing import Callable
import unittest

FAKE_DEFAULT_LANG = "fakeDefault"
FAKE_DEFAULT_SYNTH_NAME = "defaultSynth"


class MockSynth:
	def __init__(self, name: str):
		self.name = name
		self.availableVoices = {"fooId": synthDriverHandler.VoiceInfo("fooId", "foo language", FAKE_DEFAULT_LANG)}

	def cancel(self):
		pass

	def terminate(self):
		pass

	def initSettings(self):
		pass

	def _getDefaultVoice(self, pickAny: bool = True):
		assert self.name == "oneCore"  # this should only be used when mocking the oneCore synth
		return OneCoreSynthDriver._getDefaultVoice(self, pickAny)


class test_synthDriverHandler(unittest.TestCase):

	def setUp(self) -> None:
		self._oldLang = languageHandler.getLanguage()
		self._oldSynthConfig = config.conf["speech"]["synth"]
		self._originalSynth = synthDriverHandler._curSynth
		self._originalGetSynthDriver = synthDriverHandler._getSynthDriver
		config.conf["speech"]["synth"] = FAKE_DEFAULT_LANG
		synthDriverHandler._curSynth = MockSynth(FAKE_DEFAULT_SYNTH_NAME)
		synthDriverHandler._getSynthDriver = self._mock_getSynthDriver
		globalVars.appArgs.language = FAKE_DEFAULT_LANG

	@staticmethod
	def _mock_getSynthDriver(synthName: str) -> Callable[[], MockSynth]:
		return lambda: MockSynth(synthName)

	def tearDown(self) -> None:
		config.conf["speech"]["synth"] = self._oldSynthConfig
		synthDriverHandler._curSynth = self._originalSynth
		synthDriverHandler._getSynthDriver = self._originalGetSynthDriver
		globalVars.appArgs.language = self._oldLang

	def test_setSynth_auto(self):
		"""
		Ensures setSynth("auto") successfully sets a synth in defaultSynthPriorityList, and saves it to config.
		"""
		synthDriverHandler.setSynth("auto")
		autoSynthName = synthDriverHandler.getSynth().name
		self.assertIn(autoSynthName, synthDriverHandler.defaultSynthPriorityList)
		self.assertEqual(config.conf["speech"]["synth"], autoSynthName)

	def test_setSynth_defaultSynths(self):
		"""
		For each synth in the synthDriverHandler.defaultSynthPriorityList, ensure they can be successfully set
		and saved to config.
		"""
		for synthName in synthDriverHandler.defaultSynthPriorityList:
			synthDriverHandler.setSynth(synthName)
			self.assertEqual(synthName, synthDriverHandler.getSynth().name)
			self.assertEqual(synthName, config.conf["speech"]["synth"])

	def test_setSynth_auto_fallbackMode(self):
		"""
		Ensures setSynth("auto") successfully sets a synth in defaultSynthPriorityList, and config is unchanged.
		"""
		synthDriverHandler.setSynth("auto", isFallback=True)
		self.assertIn(synthDriverHandler.getSynth().name, synthDriverHandler.defaultSynthPriorityList)
		self.assertEqual(FAKE_DEFAULT_LANG, config.conf["speech"]["synth"])

	def test_setSynth_defaultSynths_fallbackMode(self):
		"""
		For each synth in the synthDriverHandler.defaultSynthPriorityList, ensure they can be successfully set
		and the config is unchanged.
		"""
		for synthName in synthDriverHandler.defaultSynthPriorityList:
			synthDriverHandler.setSynth(synthName, isFallback=True)
			self.assertEqual(synthName, synthDriverHandler.getSynth().name)
			self.assertEqual(FAKE_DEFAULT_LANG, config.conf["speech"]["synth"])

	@unittest.skipUnless(OneCoreSynthDriver.check(), "Requires oneCore being supported under current OS")
	def test_setSynth_auto_usesOneCore_ifSupportsDefaultLanguage(self):
		"""
		Ensures that if oneCore supports the current language, setSynth("auto") uses "oneCore".
		"""
		# test setup ensures current NVDA language is supported for oneCore
		synthDriverHandler.setSynth(None)  # reset the synth so there is no fallback
		synthDriverHandler.setSynth("auto")
		self.assertEqual(synthDriverHandler.getSynth().name, "oneCore")

	@unittest.skipUnless(OneCoreSynthDriver.check(), "Requires oneCore being supported under current OS")
	def test_setSynth_auto_fallback_ifOneCoreDoesntSupportDefaultLanguage(self):
		"""
		Ensures that if oneCore doesn't support the current language, setSynth("auto") falls back to the
		current synth, or espeak if there is no current synth.
		"""
		globalVars.appArgs.language = "bar"  # set the lang so it is not supported
		synthDriverHandler.setSynth("auto")
		self.assertEqual(synthDriverHandler.getSynth().name, FAKE_DEFAULT_SYNTH_NAME)
		synthDriverHandler.setSynth(None)  # reset the synth so there is no fallback
		synthDriverHandler.setSynth("auto")
		self.assertEqual(synthDriverHandler.getSynth().name, "espeak")
