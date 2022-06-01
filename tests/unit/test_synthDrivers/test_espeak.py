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
from synthDrivers.espeak import SynthDriver


class FakeESpeakSynthDriver:
	_language = "default"
	_defaultLangToLocaleMappings = {"default": "en-gb"}
	availableLanguages = {"fr", "fr-fr", "en-gb", "ta-ta"}


class TestSynthDriver(unittest.TestCase):
	def test_determineLangFromCommand(self):
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
