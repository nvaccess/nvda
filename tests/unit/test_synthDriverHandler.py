# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2021 NV Access Limited

"""Unit tests for the synthDriverHandler
"""
import config
import synthDriverHandler
import unittest


class MockSynth:
	def __init__(self, name: str):
		self.name = name

	def cancel(self):
		pass

	def terminate(self):
		pass


class test_synthDriverHandler(unittest.TestCase):
	def setUp(self) -> None:
		self._oldSynthConfig = config.conf["speech"]["synth"]
		self._originalSynth = synthDriverHandler._curSynth
		self._originalGetSynthInstance = synthDriverHandler.getSynthInstance
		synthDriverHandler._curSynth = MockSynth("default")
		synthDriverHandler.getSynthInstance = self._mockGetSynthInstance

	@staticmethod
	def _mockGetSynthInstance(synthName: str, asDefault=False):
		return MockSynth(synthName)

	def tearDown(self) -> None:
		config.conf["speech"]["synth"] = self._oldSynthConfig
		synthDriverHandler._curSynth = self._originalSynth
		synthDriverHandler.getSynthInstance = self._originalGetSynthInstance

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
