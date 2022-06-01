# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the eSpeak synth driver submodule.
"""

import logging
import unittest
import logHandler
from speech.commands import LangChangeCommand
from source.synthDrivers.espeak import SynthDriver


class FakeESpeakSynthDriver:
	_language = "default"
	_defaultLangToLocale = {"default": "en-gb"}
	availableLanguages = {"fr", "fr-fr", "en-gb", "ta-ta"}


class TestSynthDriver(unittest.TestCase):
	def setUp(self) -> None:
		self._driver = SynthDriver()
	
	def tearDown(self) -> None:
		self._driver.terminate()

	def test_determineLangFromCommand(self):
		"""Test cases for determining a supported eSpeak language from a LangChangeCommand."""
		self.assertEqual(
			"en-gb",
			SynthDriver._determineLangFromCommand(FakeESpeakSynthDriver, LangChangeCommand(None)),
			msg="Default language used if language code not provided"
		)
		self.assertEqual(
			"fr-fr",
			SynthDriver._determineLangFromCommand(FakeESpeakSynthDriver, LangChangeCommand("fr_FR")),
			msg="Language with locale used when available"
		)
		self.assertEqual(
			"en-gb",
			SynthDriver._determineLangFromCommand(FakeESpeakSynthDriver, LangChangeCommand("default")),
			msg="Default eSpeak language mappings used"
		)
		self.assertEqual(
			"fr",
			SynthDriver._determineLangFromCommand(FakeESpeakSynthDriver, LangChangeCommand("fr_FAKE")),
			msg="Language without locale used when available"
		)
		self.assertEqual(
			"ta-ta",
			SynthDriver._determineLangFromCommand(FakeESpeakSynthDriver, LangChangeCommand("ta-gb")),
			msg="Language with any locale used when available"
		)
		with self.assertLogs(logHandler.log, level=logging.DEBUG) as logContext:
			self.assertEqual(
				None,
				SynthDriver._determineLangFromCommand(FakeESpeakSynthDriver, LangChangeCommand("fake")),
				msg="No matching available language returns None"
			)
		self.assertIn(
			"Unable to find an eSpeak language for 'fake'",
			logContext.output[0]
		)

	def test_defaultMappingAvailableLanguage(self):
		"""Confirms language codes remapped by default are supported by eSpeak via integration testing"""
		mappedDefaultLanguages = set(self._driver._defaultLangToLocale.values())
		unexpectedUnsupportedDefaultLanguages = mappedDefaultLanguages.difference(self._driver.availableLanguages)
		self.assertEqual(
			set(),
			unexpectedUnsupportedDefaultLanguages,
			msg=f"Languages mapped by defaults are no longer supported by eSpeak {unexpectedUnsupportedDefaultLanguages}"
		)

		expectedUnsupportedMappedLanguages = set(self._driver._defaultLangToLocale.keys())
		unexpectedSupportedMappedLanguages = expectedUnsupportedMappedLanguages.intersection(self._driver.availableLanguages)
		self.assertEqual(
			set(),
			unexpectedSupportedMappedLanguages,
			msg=f"Languages mapped to eSpeak defaults are now supported by eSpeak: {unexpectedSupportedMappedLanguages}"
		)