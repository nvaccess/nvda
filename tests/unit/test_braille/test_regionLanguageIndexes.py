# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NV Access Limited, Leonard de Ruijter
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""Unit tests for Region language index tracking in the braille module."""

import unittest
from unittest.mock import patch

import braille
import textInfos


def _makeTextInfoRegion() -> braille.TextInfoRegion:
	"""Build a TextInfoRegion without going through __init__ (which requires an NVDAObject)."""
	region = braille.TextInfoRegion.__new__(braille.TextInfoRegion)
	braille.Region.__init__(region)
	# Force a deterministic default language so we don't depend on NVDA's configured locale.
	region._languageIndexes = {0: "en"}
	return region


class TestLanguageIndexes(unittest.TestCase):
	def test_freshRegion_defaultLanguageAtAnyPos(self):
		"""A region returns the default language for any non-negative pos."""
		# Stub default language so Region.__init__ doesn't depend on NVDA's configured locale.
		with patch.object(braille.Region, "_getDefaultRegionLanguage", return_value="en"):
			region = braille.Region()
		self.assertEqual(region._getLanguageAtPos(0), "en")
		self.assertEqual(region._getLanguageAtPos(5), "en")
		self.assertEqual(region._getLanguageAtPos(100), "en")

	def test_addFieldText_insertsSwitchAndRestore(self):
		"""_addFieldText inserts a switch entry at len(rawText) and a restore entry at len+textLen when the field language differs."""
		region = _makeTextInfoRegion()
		# Pre-existing raw text to make `len(rawText)` non-zero and exercise the separator logic.
		region.rawText = "hello"
		region.rawTextTypeforms = []
		region._rawToContentPos = list(range(5))
		rawTextLenBefore = len(region.rawText)
		text = "field"
		with patch("braille.languageHandler.getLanguage", return_value="fr"):
			region._addFieldText(text, contentPos=0)
		# `_addFieldText` prepends TEXT_SEPARATOR when `separate=True` and there is pre-existing text.
		addedLen = len(braille.TEXT_SEPARATOR) + len(text)
		self.assertIn(rawTextLenBefore, region._languageIndexes)
		self.assertEqual(region._languageIndexes[rawTextLenBefore], "fr")
		self.assertIn(rawTextLenBefore + addedLen, region._languageIndexes)
		self.assertEqual(region._languageIndexes[rawTextLenBefore + addedLen], "en")

	def test_addTextWithFields_formatChangeInsertsLanguageIndex(self):
		"""Processing a formatChange command whose field has a `language` attribute inserts an index entry."""
		region = _makeTextInfoRegion()
		region.rawText = ""
		region.rawTextTypeforms = []
		region._rawToContentPos = []
		region._currentContentPos = 0
		region._endsWithField = False
		region._isFormatFieldAtStart = True
		region._skipFieldsNotAtStartOfNode = False
		region.cursorPos = None
		region.selectionStart = region.selectionEnd = None

		# Build a minimal list of commands: text, then a formatChange with language=de, then more text.
		field = textInfos.FormatField()
		field["language"] = "de"
		commands = [
			"pre ",
			textInfos.FieldCommand(command="formatChange", field=field),
			"post",
		]

		class FakeObj:
			_brailleFormatFieldAttributesCache: dict = {}

		class FakeInfo:
			isCollapsed = False
			obj = FakeObj()

			def getTextWithFields(self, formatConfig=None):
				return commands

		formatConfig = {
			"reportClickable": False,
		}
		# Stub helpers that would otherwise require a real NVDA environment.
		with (
			patch("braille.getFormatFieldBraille", return_value=""),
			patch.object(
				braille.TextInfoRegion,
				"_getTypeformFromFormatField",
				return_value=0,
			),
		):
			region._addTextWithFields(FakeInfo(), formatConfig)
		# The language switch should have been recorded at len("pre ") == 4.
		self.assertIn(4, region._languageIndexes)
		self.assertEqual(region._languageIndexes[4], "de")

	def test_textInfoRegion_update_resetsLanguageIndexes(self):
		"""TextInfoRegion.update resets _languageIndexes to {0: default} — no stale indexes carry across updates."""
		region = _makeTextInfoRegion()
		# Pollute _languageIndexes with stale entries.
		region._languageIndexes = {0: "en", 10: "de", 30: "en"}

		# Run only the resetting portion of `update` by making `_getSelection` raise immediately,
		# then inspect state. The reset happens before `_getSelection` is called.
		# Using side_effect to halt execution mid-method avoids needing the full NVDA environment
		# that the rest of update() requires.
		with (
			patch.object(braille.TextInfoRegion, "_getDefaultRegionLanguage", return_value="en"),
			patch.object(
				braille.TextInfoRegion,
				"_getReadingUnit",
				return_value=textInfos.UNIT_LINE,
			),
			patch.object(
				braille.TextInfoRegion,
				"_getSelection",
				side_effect=RuntimeError("stop-after-reset"),
			),
		):
			with self.assertRaises(RuntimeError):
				region.update()
		self.assertEqual(region._languageIndexes, {0: "en"})
