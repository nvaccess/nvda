# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2026 Islam Benmebarek

"""Regression tests for word expansion in mixed-direction Chromium editors."""

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from config.featureFlagEnums import WordNavigationUnitFlag
from NVDAObjects.IAccessible import chromium, IA2TextTextInfo


class TestChromiumRtlWordNavigation(unittest.TestCase):
	def _getWord(self, line: str, offset: int) -> str:
		textInfo = object.__new__(chromium.ChromiumIA2TextTextInfo)
		textInfo.wordSegConf = SimpleNamespace(calculated=lambda: WordNavigationUnitFlag.UNISCRIBE)
		textInfo._getLineOffsets = Mock(return_value=(0, len(line)))
		textInfo._getTextRange = Mock(return_value=line)

		with patch.object(IA2TextTextInfo, "_getWordOffsets", return_value=(0, len(line))):
			start, end = textInfo._getWordOffsets(offset)
		return line[start:end]

	def test_mixedArabicEnglishLine(self) -> None:
		line = "هذه رسالة طويلة لاختبار NVDA project داخل فقرة عربية mixed text."

		self.assertEqual(self._getWord(line, line.index("رسالة")), "رسالة ")
		self.assertEqual(self._getWord(line, line.index("NVDA")), "NVDA ")
		self.assertEqual(self._getWord(line, line.index("project")), "project ")
		self.assertEqual(self._getWord(line, line.index("داخل")), "داخل ")
