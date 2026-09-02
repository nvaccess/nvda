# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2026 NVDA Contributors
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import unittest
from configparser import ConfigParser
from pathlib import Path

_ADDON_DIRECTORY = Path(__file__).resolve().parents[1] / "nvdaAddon"


class TestSimplifiedChineseLocalization(unittest.TestCase):
	def test_catalogSourceContainsUserInterfaceTranslations(self) -> None:
		catalogPath = _ADDON_DIRECTORY / "locale" / "zh_CN" / "LC_MESSAGES" / "nvda.po"
		catalog = catalogPath.read_text(encoding="utf-8")
		for source, translation in (
			("On-device OCR", "设备端 OCR"),
			(
				"Recognizes the current navigator object using on-device OCR",
				"使用设备端 OCR 识别当前浏览对象",
			),
			(
				"The current navigator object is too large for on-device OCR.",
				"当前浏览对象过大，无法安全地进行设备端 OCR。",
			),
		):
			with self.subTest(source=source):
				self.assertIn(f'msgid "{source}"\nmsgstr "{translation}"', catalog)

	def test_manifestHasSimplifiedChineseMetadata(self) -> None:
		manifestPath = _ADDON_DIRECTORY / "locale" / "zh_CN" / "manifest.ini"
		parser = ConfigParser()
		parser.read_string("[manifest]\n" + manifestPath.read_text(encoding="utf-8"))
		self.assertEqual(parser["manifest"]["summary"], '"设备端 OCR"')
		self.assertIn("离线多语言 OCR", parser["manifest"]["description"])


if __name__ == "__main__":
	unittest.main()
