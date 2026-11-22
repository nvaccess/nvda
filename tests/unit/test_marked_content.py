# Tests for marked / highlighted content reporting (Issue #21167)
# This file is covered by the GNU General Public License.

import unittest
from controlTypes import OutputReason
import config
import textInfos
from textInfos import UNIT_LINE, UNIT_CHARACTER, UNIT_WORD, UNIT_PARAGRAPH
import speech.speech as speechModule

class TestMarkedContentReporting(unittest.TestCase):
	def setUp(self):
		self.formatConfig = dict.fromkeys(config.conf["documentFormatting"], False)
		self.formatConfig["reportHighlight"] = True

	def test_sayall_reports_marked_and_suppresses_not_marked(self):
		"""Verify that Say All announces 'marked' on enter, but suppresses 'not marked' on exit."""
		attrsCache = {}
		# Enter marked text
		enter_field = textInfos.FormatField({"marked": True})
		enter_speech = speechModule.getFormatFieldSpeech(
			enter_field,
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.SAYALL,
			unit=UNIT_LINE,
		)
		self.assertIn("marked", enter_speech)

		# Exit marked text
		exit_field = textInfos.FormatField({})
		exit_speech = speechModule.getFormatFieldSpeech(
			exit_field,
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.SAYALL,
			unit=UNIT_LINE,
		)
		self.assertNotIn("not marked", exit_speech)
		self.assertEqual(exit_speech, [])

	def test_line_navigation_suppresses_not_marked(self):
		"""Verify that line navigation suppresses 'not marked' when exiting marked content."""
		attrsCache = {}
		# Enter marked
		enter_speech = speechModule.getFormatFieldSpeech(
			textInfos.FormatField({"marked": True}),
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.CARET,
			unit=UNIT_LINE,
		)
		self.assertIn("marked", enter_speech)

		# Exit marked
		exit_speech = speechModule.getFormatFieldSpeech(
			textInfos.FormatField({}),
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.CARET,
			unit=UNIT_LINE,
		)
		self.assertNotIn("not marked", exit_speech)
		self.assertEqual(exit_speech, [])

	def test_paragraph_navigation_suppresses_not_marked(self):
		"""Verify that paragraph navigation suppresses 'not marked' on exit."""
		attrsCache = {"marked": True}
		exit_speech = speechModule.getFormatFieldSpeech(
			textInfos.FormatField({}),
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.CARET,
			unit=UNIT_PARAGRAPH,
		)
		self.assertNotIn("not marked", exit_speech)
		self.assertEqual(exit_speech, [])

	def test_character_navigation_reports_not_marked(self):
		"""Verify that character navigation explicitly reports 'not marked' when moving out of marked text."""
		attrsCache = {"marked": True}
		exit_speech = speechModule.getFormatFieldSpeech(
			textInfos.FormatField({}),
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.CARET,
			unit=UNIT_CHARACTER,
		)
		self.assertIn("not marked", exit_speech)

	def test_color_highlight_continuous_reading_suppresses_not_highlighted(self):
		"""Verify that color highlighting suppresses 'not highlighted' during continuous reading."""
		attrsCache = {"highlight-color": "yellow"}
		exit_speech = speechModule.getFormatFieldSpeech(
			textInfos.FormatField({}),
			attrsCache=attrsCache,
			formatConfig=self.formatConfig,
			reason=OutputReason.SAYALL,
			unit=UNIT_LINE,
		)
		self.assertNotIn("not highlighted", exit_speech)
		self.assertEqual(exit_speech, [])
