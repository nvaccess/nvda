# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited

"""Unit tests for the synthDriverHandler
"""
import config
import languageHandler
import synthDriverHandler
from typing import Callable
import unittest


class MockSynth:
	def __init__(self, name: str):
		self.name = name
		self.availableVoices = {"fooId": synthDriverHandler.VoiceInfo("fooId", "foo language", "foo")}

	def cancel(self):
		pass

	def terminate(self):
		pass

	def initSettings(self):
		pass

	def _getDefaultVoice(self, pickAny: bool = True):
		assert self.name == "oneCore"  # this should only be used when mocking the oneCore synth
		from synthDrivers import oneCore
		return oneCore.SynthDriver._getDefaultVoice(self, pickAny)


class test_synthDriverHandler(unittest.TestCase):
	def setUp(self) -> None:
		self._oldLang = languageHandler.curLang
		self._oldSynthConfig = config.conf["speech"]["synth"]
		self._originalSynth = synthDriverHandler._curSynth
		self._originalGetSynthDriver = synthDriverHandler._getSynthDriver
		synthDriverHandler._curSynth = MockSynth("default")
		synthDriverHandler._getSynthDriver = self._mock_getSynthDriver
		languageHandler.curLang = "foo"

	@staticmethod
	def _mock_getSynthDriver(synthName: str) -> Callable[[], MockSynth]:
		return lambda: MockSynth(synthName)

	def tearDown(self) -> None:
		config.conf["speech"]["synth"] = self._oldSynthConfig
		synthDriverHandler._curSynth = self._originalSynth
		synthDriverHandler._getSynthDriver = self._originalGetSynthDriver
		languageHandler.curLang = self._oldLang

	def test_setSynth(self):
		synthDriverHandler.setSynth("auto")
		autoSynthName = synthDriverHandler.getSynth().name
		self.assertIn(autoSynthName, synthDriverHandler.defaultSynthPriorityList)
		self.assertEqual(config.conf["speech"]["synth"], autoSynthName)
		for synthName in synthDriverHandler.defaultSynthPriorityList:
			synthDriverHandler.setSynth(synthName)
			self.assertEqual(synthName, synthDriverHandler.getSynth().name)
			self.assertEqual(synthName, config.conf["speech"]["synth"])

	def test_setSynth_fallbackMode(self):
		synthDriverHandler.setSynth("auto", isFallback=True)
		self.assertIn(synthDriverHandler.getSynth().name, synthDriverHandler.defaultSynthPriorityList)
		self.assertEqual(self._oldSynthConfig, config.conf["speech"]["synth"])
		for synthName in synthDriverHandler.defaultSynthPriorityList:
			synthDriverHandler.setSynth(synthName, isFallback=True)
			self.assertEqual(synthName, synthDriverHandler.getSynth().name)
			self.assertEqual(self._oldSynthConfig, config.conf["speech"]["synth"])

	def test_setSynth_oneCoreSupportsDefaultLangauge(self):
		synthDriverHandler.setSynth(None)  # reset the synth so there is no fallback
		synthDriverHandler.setSynth("auto")
		self.assertEqual(synthDriverHandler.getSynth().name, "oneCore")
		synthDriverHandler.setSynth(None)  # reset the synth so there is no fallback
		languageHandler.curLang = "bar"  # set the lang so it is not supported
		synthDriverHandler.setSynth("auto")
		self.assertEqual(synthDriverHandler.getSynth().name, "espeak")
