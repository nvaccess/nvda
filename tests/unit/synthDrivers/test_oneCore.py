#tests/unit/synthDrivers/test_oneCore.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the oneCore synth driver.
"""

import unittest
from synthDrivers import oneCore
import speech

class TestConvertLangChangeCommand(unittest.TestCase):
	"""Tests handling of invalid language codes (and languages Windows doesn't know about).
	This only needs to verify whether the result is None (invalid language) or not None (valid language),
	as the implementation calls speechXml.SsmlConverter for valid languages.
	"""

	def setUp(self):
		self.converter = oneCore._OcSsmlConverter("en_US", 50, 50, 100)

	def test_validLang(self):
		out = self.converter.convertLangChangeCommand(speech.LangChangeCommand("en"))
		self.assertIsNotNone(out)

	def test_invalidLang(self):
		out = self.converter.convertLangChangeCommand(speech.LangChangeCommand("us"))
		self.assertIsNone(out)

	def test_windowsUnknownLang(self):
		# "an" is a valid language code, but Windows doesn't know about it.
		out = self.converter.convertLangChangeCommand(speech.LangChangeCommand("an"))
		self.assertIsNone(out)
