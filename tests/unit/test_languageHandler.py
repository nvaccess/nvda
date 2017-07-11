#tests/unit/test_languageHandler.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2017 NV Access Limited

"""Unit tests for the languageHandler module.
"""

import unittest
import languageHandler
from languageHandler import LCID_NONE

LCID_ENGLISH_US = 0x0409

class TestLocaleNameToWindowsLCID(unittest.TestCase):

	def test_knownLocale(self):
		lcid = languageHandler.localeNameToWindowsLCID("en")
		self.assertEqual(lcid, LCID_ENGLISH_US)

	def test_windowsUnknownLocale(self):
		# "an" is the locale name for Aragonese, but Windows doesn't know about it.
		lcid = languageHandler.localeNameToWindowsLCID("an")
		self.assertEqual(lcid, LCID_NONE)

	def test_nonStandardLocale(self):
		lcid = languageHandler.localeNameToWindowsLCID("us")
		self.assertEqual(lcid, LCID_NONE)

	def test_invalidLocale(self):
		lcid = languageHandler.localeNameToWindowsLCID("zzzz")
		self.assertEqual(lcid, LCID_NONE)
