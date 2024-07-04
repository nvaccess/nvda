# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 NV Access Limited.

"""Unit tests for the eSpeak synth driver submodule."""

import logging
import unittest

from languageHandler import stripLocaleFromLangCode
import logHandler
from speech.commands import LangChangeCommand
from synthDrivers.espeak import SynthDriver
from synthDrivers._espeak import _setVoiceByLanguage
import nvwave


class FakeESpeakSynthDriver:
	_language = "default"
	_defaultLangToLocale = {"default": "en-gb"}
	availableLanguages = {"fr", "fr-fr", "en-gb", "ta-ta"}


class TestSynthDriver_Logic(unittest.TestCase):
	"""Testing of internal logic for the eSpeak driver."""

	def test_normalizeLangCommand(self):
		"""Test cases for determining a supported eSpeak language from a LangChangeCommand."""
		self.assertEqual(
			LangChangeCommand("en-gb"),
			SynthDriver._normalizeLangCommand(FakeESpeakSynthDriver, LangChangeCommand(None)),
			msg="Default language used if language code not provided",
		)
		self.assertEqual(
			LangChangeCommand("fr-fr"),
			SynthDriver._normalizeLangCommand(FakeESpeakSynthDriver, LangChangeCommand("fr_FR")),
			msg="Language with locale used when available",
		)
		self.assertEqual(
			LangChangeCommand("en-gb"),
			SynthDriver._normalizeLangCommand(FakeESpeakSynthDriver, LangChangeCommand("default")),
			msg="Default eSpeak language mappings used",
		)
		self.assertEqual(
			LangChangeCommand("fr"),
			SynthDriver._normalizeLangCommand(FakeESpeakSynthDriver, LangChangeCommand("fr_FAKE")),
			msg="Language without locale used when available",
		)
		self.assertEqual(
			LangChangeCommand("ta-ta"),
			SynthDriver._normalizeLangCommand(FakeESpeakSynthDriver, LangChangeCommand("ta-gb")),
			msg="Language with any locale used when available",
		)
		with self.assertLogs(logHandler.log, level=logging.DEBUG) as logContext:
			self.assertEqual(
				LangChangeCommand(None),
				SynthDriver._normalizeLangCommand(FakeESpeakSynthDriver, LangChangeCommand("fake")),
				msg="No matching available language returns None",
			)
		self.assertIn(
			"Unable to find an eSpeak language for 'fake'",
			logContext.output[0],
		)


class TestSynthDriver_Integration(unittest.TestCase):
	"""Perform integration testing for the eSpeak synth driver."""

	def setUp(self) -> None:
		# Prevent NVWave from causing an exception
		# when running unit tests in AppVeyor
		self._nvwaveOpenOld = nvwave.WavePlayer.open
		nvwave.WavePlayer.open = lambda self: None
		self._driver = SynthDriver()

	def tearDown(self) -> None:
		self._driver.terminate()
		nvwave.WavePlayer.open = self._nvwaveOpenOld

	def test_defaultMappingAvailableLanguage(self):
		"""Confirms language codes remapped by default are supported by eSpeak and are comprehensive."""
		eSpeakAvailableLangs = self._driver.availableLanguages
		mappedDefaultLanguages = set(self._driver._defaultLangToLocale.values())
		unexpectedUnsupportedDefaultLanguages = mappedDefaultLanguages.difference(eSpeakAvailableLangs)
		self.assertEqual(
			set(),
			unexpectedUnsupportedDefaultLanguages,
			msg=(
				"Languages mapped by default are no longer supported by eSpeak: "
				f"{unexpectedUnsupportedDefaultLanguages}"
			),
		)

		expectedUnsupportedMappedLanguages = set(self._driver._defaultLangToLocale.keys())
		unexpectedSupportedMappedLanguages = expectedUnsupportedMappedLanguages.intersection(
			eSpeakAvailableLangs,
		)
		self.assertEqual(
			set(),
			unexpectedSupportedMappedLanguages,
			msg=(
				"Languages mapped to eSpeak defaults are now supported by eSpeak: "
				f"{unexpectedSupportedMappedLanguages}"
			),
		)

		supportedLanguagesWithLocaleStripped = set(
			stripLocaleFromLangCode(lang) for lang in eSpeakAvailableLangs
		)
		unsupportedLanguagesWithoutLocale = supportedLanguagesWithLocaleStripped.difference(
			eSpeakAvailableLangs,
		)
		self.assertEqual(
			expectedUnsupportedMappedLanguages,
			unsupportedLanguagesWithoutLocale,
			msg=(
				"eSpeak has a language with locale supported "
				"but the language without locale is unsupported."
				"Update _defaultLangToLocale to include a new mapping."
			),
		)

	def test_availableLanguagesWithoutLocale(self):
		"""
		Confirms that eSpeak can manually be switched to all of its supported languages with the locale removed.
		This doesn't test automatic language switching.
		"""
		availableLangsWithoutLocale = set(
			stripLocaleFromLangCode(lang) for lang in self._driver.availableLanguages
		)
		for langWithoutLocale in availableLangsWithoutLocale:
			_setVoiceByLanguage(langWithoutLocale)
			self.assertEqual(
				langWithoutLocale,
				self._driver.voice.split("\\")[
					-1
				],  # Language code is the last item, e.g. (gmw\en, roa\fr-CH)
				msg="Language without locale not supported by eSpeak",
			)

	def test_fallbackToBritishEnglish(self):
		"""
		Confirms that eSpeak falls back to en-gb when manually switching to an unknown language
		"""
		_setVoiceByLanguage("fake-lang")
		self.assertEqual(
			"gmw\\en",
			self._driver.voice,
			msg="Language without locale not supported by eSpeak",
		)
