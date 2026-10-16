# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Christos Bouronikos
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Regression tests for MathCAT's SSML speech conversion."""

import unittest
from unittest.mock import Mock, patch

from mathPres.MathCAT import speech as mathCatSpeech
from speech.commands import (
	CharacterModeCommand,
	PitchCommand,
	RateCommand,
	SpeechCommand,
	VolumeCommand,
)


class TestMathCatSpeech(unittest.TestCase):
	"""Check prosody scope restoration without a live synthesizer."""

	def setUp(self) -> None:
		self.synth: Mock = Mock()
		self.synth._get_rate.return_value = 50
		self.synth.supportedCommands = {
			CharacterModeCommand,
			PitchCommand,
			RateCommand,
			VolumeCommand,
		}
		self.enterContext(patch.object(mathCatSpeech, "getSynth", return_value=self.synth))
		self.enterContext(patch.object(mathCatSpeech, "getLanguageToUse", return_value="en"))
		self.enterContext(patch.object(mathCatSpeech, "getCurrentLanguage", return_value="en"))

	def _convert(self, ssml: str) -> list[str | SpeechCommand]:
		# Ignore the converter's word-separating spaces, retaining text/command order.
		return [item for item in mathCatSpeech.convertSSMLTextForNVDA(ssml) if item != " "]

	def test_capitalPitchPreservesEnclosingMathRate(self) -> None:
		"""Text after a capital retains the math rate until the equation ends."""
		self.assertEqual(
			self._convert(
				"<prosody rate='50%'>a<prosody pitch='120%'>"
				"<say-as interpret-as='characters'>A</say-as></prosody>b</prosody>text",
			),
			[
				RateCommand(multiplier=0.5),
				"a",
				PitchCommand(multiplier=120),
				CharacterModeCommand(True),
				"A",
				CharacterModeCommand(False),
				PitchCommand(),
				"b",
				RateCommand(),
				"text",
			],
		)

	def test_nestedRateRestoresEnclosingRate(self) -> None:
		"""An inner rate restores the outer rate rather than the default rate."""
		self.assertEqual(
			self._convert("<prosody rate='50%'>a<prosody rate='80%'>b</prosody>c</prosody>"),
			[
				RateCommand(multiplier=0.5),
				"a",
				RateCommand(multiplier=0.8),
				"b",
				RateCommand(multiplier=0.5),
				"c",
				RateCommand(),
			],
		)

	def test_multipleAttributesRestoreTheirEnclosingValues(self) -> None:
		"""Each changed attribute returns to its enclosing value on tag closure."""
		self.assertEqual(
			self._convert(
				"<prosody pitch='110%' volume='80%' rate='50%'>a"
				"<prosody pitch='120%' volume='60%' rate='70%'>b</prosody>c</prosody>",
			),
			[
				PitchCommand(multiplier=110),
				VolumeCommand(multiplier=0.8),
				RateCommand(multiplier=0.5),
				"a",
				PitchCommand(multiplier=120),
				VolumeCommand(multiplier=0.6),
				RateCommand(multiplier=0.7),
				"b",
				RateCommand(multiplier=0.5),
				VolumeCommand(multiplier=0.8),
				PitchCommand(multiplier=110),
				"c",
				RateCommand(),
				VolumeCommand(),
				PitchCommand(),
			],
		)

	def test_unsupportedPitchDoesNotCloseEnclosingRate(self) -> None:
		"""An ignored pitch tag still has its own scope."""
		self.synth.supportedCommands.remove(PitchCommand)
		self.assertEqual(
			self._convert("<prosody rate='50%'>a<prosody pitch='120%'>A</prosody>b</prosody>"),
			[RateCommand(multiplier=0.5), "a", "A", "b", RateCommand()],
		)

	def test_emptyProsodyDoesNotCloseEnclosingRate(self) -> None:
		"""An attribute-free tag must not consume an outer tag's saved values."""
		self.assertEqual(
			self._convert("<prosody rate='50%'>a<prosody>b</prosody>c</prosody>"),
			[RateCommand(multiplier=0.5), "a", "b", "c", RateCommand()],
		)

	def test_siblingCapitalsPreserveEnclosingMathRate(self) -> None:
		"""Repeated capitals leave the same outer math rate active."""
		self.assertEqual(
			self._convert(
				"<prosody rate='50%'><prosody pitch='120%'>A</prosody>"
				"b<prosody pitch='120%'>B</prosody>c</prosody>",
			),
			[
				RateCommand(multiplier=0.5),
				PitchCommand(multiplier=120),
				"A",
				PitchCommand(),
				"b",
				PitchCommand(multiplier=120),
				"B",
				PitchCommand(),
				"c",
				RateCommand(),
			],
		)

	def test_consecutiveEquationsRestoreDefaultRate(self) -> None:
		"""Separate equations do not leak their rates into intervening text."""
		self.assertEqual(
			self._convert("<prosody rate='50%'>a</prosody>text<prosody rate='80%'>b</prosody>"),
			[
				RateCommand(multiplier=0.5),
				"a",
				RateCommand(),
				"text",
				RateCommand(multiplier=0.8),
				"b",
				RateCommand(),
			],
		)

	def test_nestedPitchRestoresEnclosingPitch(self) -> None:
		"""An inner pitch restores the outer pitch rather than the default pitch."""
		self.assertEqual(
			self._convert("<prosody pitch='110%'>A<prosody pitch='120%'>B</prosody>C</prosody>"),
			[
				PitchCommand(multiplier=110),
				"A",
				PitchCommand(multiplier=120),
				"B",
				PitchCommand(multiplier=110),
				"C",
				PitchCommand(),
			],
		)
