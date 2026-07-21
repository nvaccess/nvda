# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 Islam Benmebarek

"""Unit tests for Chromium accessibility support."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from NVDAObjects import NVDAObjectTextInfo
from NVDAObjects.IAccessible import chromium, IA2TextTextInfo
from textInfos.offsets import OffsetsTextInfo


class TestChromiumIA2TextTextInfo(unittest.TestCase):
	def _makeTextInfo(self, storyText: str) -> chromium.ChromiumIA2TextTextInfo:
		textInfo = object.__new__(chromium.ChromiumIA2TextTextInfo)
		textInfo._getTextRange = Mock(side_effect=lambda start, end: storyText[start:end])
		return textInfo

	def test_malformedWordOffsetsUseNvdaSegmentation(self) -> None:
		textInfo = self._makeTextInfo("the message after")
		with (
			patch.object(IA2TextTextInfo, "_getWordOffsets", return_value=(4, 13)) as getIa2WordOffsets,
			patch.object(OffsetsTextInfo, "_getWordOffsets", return_value=(4, 12)) as getNvdaWordOffsets,
		):
			result = textInfo._getWordOffsets(6)

		self.assertEqual(result, (4, 12))
		getIa2WordOffsets.assert_called_once_with(6)
		getNvdaWordOffsets.assert_called_once_with(6)

	def test_wordOffsetsEndingMidWordUseNvdaSegmentation(self) -> None:
		textInfo = self._makeTextInfo("ناقشنا خطة")
		with (
			patch.object(IA2TextTextInfo, "_getWordOffsets", return_value=(0, 4)),
			patch.object(OffsetsTextInfo, "_getWordOffsets", return_value=(0, 7)) as getNvdaWordOffsets,
		):
			result = textInfo._getWordOffsets(2)

		self.assertEqual(result, (0, 7))
		getNvdaWordOffsets.assert_called_once_with(2)

	def test_wordOffsetsStartingMidWordUseNvdaSegmentation(self) -> None:
		textInfo = self._makeTextInfo("Finally, this")
		with (
			patch.object(IA2TextTextInfo, "_getWordOffsets", return_value=(1, 8)),
			patch.object(OffsetsTextInfo, "_getWordOffsets", return_value=(0, 8)) as getNvdaWordOffsets,
		):
			result = textInfo._getWordOffsets(3)

		self.assertEqual(result, (0, 8))
		getNvdaWordOffsets.assert_called_once_with(3)

	def test_validWordOffsetsKeepIa2Segmentation(self) -> None:
		textInfo = self._makeTextInfo("the message after")
		with patch.object(IA2TextTextInfo, "_getWordOffsets", return_value=(4, 12)) as getIa2WordOffsets:
			result = textInfo._getWordOffsets(6)

		self.assertEqual(result, (4, 12))
		getIa2WordOffsets.assert_called_once_with(6)

	def test_validWordOffsetsWithPunctuationKeepIa2Segmentation(self) -> None:
		textInfo = self._makeTextInfo("Finally, this")
		with patch.object(IA2TextTextInfo, "_getWordOffsets", return_value=(0, 8)):
			result = textInfo._getWordOffsets(3)

		self.assertEqual(result, (0, 8))

	def test_ia2TextUsesChromiumTextInfo(self) -> None:
		obj = SimpleNamespace(TextInfo=IA2TextTextInfo)

		self.assertIs(chromium._getRawTextInfoClass(obj), chromium.ChromiumIA2TextTextInfo)

	def test_nonIa2TextKeepsObjectTextInfo(self) -> None:
		obj = SimpleNamespace(TextInfo=NVDAObjectTextInfo)

		self.assertIs(chromium._getRawTextInfoClass(obj), NVDAObjectTextInfo)
