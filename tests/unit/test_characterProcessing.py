# -*- coding: UTF-8 -*-
#tests/unit/test_characterProcessing.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2019 NV Access Limited, Leonard de Ruijter

from __future__ import unicode_literals

"""Unit tests for the characterProcessing module.
"""

import unittest
import characterProcessing
from collections import namedtuple

NrProcTestCase = namedtuple("NrProcTestCase", ("origin", "single", "double", "triple"))

nrProcTestCases = {}


# English
nrProcTestCases["en"] = [
	NrProcTestCase(origin="1",
		single="1",
		double="",
		triple=""),
	NrProcTestCase(origin="11",
		single="1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="111",
		single="1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="1111",
		single="1  1  1  1",
		double="",
		triple=""),
	# Decimals
	NrProcTestCase(origin="1.1",
		single="1.1",
		double="",
		triple=""),
	NrProcTestCase(origin="11.1",
		single="1  1.1",
		double="",
		triple=""),
	NrProcTestCase(origin="111.1",
		single="1  1  1.1",
		double="",
		triple=""),
	NrProcTestCase(origin="1111.1",
		single="1  1  1  1.1",
		double="",
		triple=""),
	NrProcTestCase(origin="1.11",
		single="1.1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="1.111",
		single="1.1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="1.1111",
		single="1.1  1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="11.111",
		single="1  1.1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="11.1111",
		single="1  1.1  1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="111.111",
		single="1  1  1.1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="1111.1111",
		single="1  1  1  1.1  1  1  1",
		double="",
		triple=""),
	# Thousands separator
	NrProcTestCase(origin="1,234",
		single="1  2  3  4",
		double="",
		triple=""),
	NrProcTestCase(origin="12,345",
		single="1  2  3  4  5",
		double="",
		triple=""),
	NrProcTestCase(origin="123,456",
		single="1  2  3  4  5  6",
		double="",
		triple=""),
	NrProcTestCase(origin="1,234,567",
		single="1  2  3  4  5  6  7",
		double="",
		triple=""),
	# Mixed with letters
	NrProcTestCase(origin="a1b2c3",
		single="a1b2c3",
		double="",
		triple=""), # Untouched
	NrProcTestCase(origin="a12b34c56",
		single="a1  2b3  4c5  6",
		double="",
		triple=""),
	NrProcTestCase(origin="a123b456c789",
		single="a1  2  3b4  5  6c7  8  9",
		double="",
		triple=""),
	NrProcTestCase(origin="a1234b5678c9012",
		single="a1  2  3  4b5  6  7  8c9  0  1  2",
		double="",
		triple=""),
	# Thousands separator with letters
	NrProcTestCase(origin="1a,234b",
		single="1a,2  3  4b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a,2,345b",
		single="1a,2  3  4  5b",
		double="",
		triple=""),
	# Decimal with letters
	NrProcTestCase(origin="1a.234b",
		single="1a.2  3  4b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a.2.345b",
		single="1a.2.3  4  5b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a.2.3456b",
		single="1a.2.3  4  5  6b",
		double="",
		triple=""),
]

# Dutch
nrProcTestCases["nl"] = [
	NrProcTestCase(origin="1",
		single="1",
		double="",
		triple=""),
	NrProcTestCase(origin="11",
		single="1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="111",
		single="1  1  1",
		double="",
		triple=""),
	# Decimals
	NrProcTestCase(origin="1,1",
		single="1,1",
		double="",
		triple=""),
	NrProcTestCase(origin="11,1",
		single="1  1,1",
		double="",
		triple=""),
	NrProcTestCase(origin="111,1",
		single="1  1  1,1",
		double="",
		triple=""),
	NrProcTestCase(origin="1,11",
		single="1,1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="1,111",
		single="1,1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="11,111",
		single="1  1,1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="111,111",
		single="1  1  1,1  1  1",
		double="",
		triple=""),
	# Thousands separator
	NrProcTestCase(origin="1.234",
		single="1  2  3  4",
		double="",
		triple=""),
	NrProcTestCase(origin="12.345",
		single="1  2  3  4  5",
		double="",
		triple=""),
	NrProcTestCase(origin="123.456",
		single="1  2  3  4  5  6",
		double="",
		triple=""),
	NrProcTestCase(origin="1.234.567",
		single="1  2  3  4  5  6  7",
		double="",
		triple=""),
	# Mixed with letters
	NrProcTestCase(origin="a1b2c3",
		single="a1b2c3",
		double="",
		triple=""), # Untouched
	NrProcTestCase(origin="a12b34c56",
		single="a1  2b3  4c5  6",
		double="",
		triple=""),
	NrProcTestCase(origin="a123b456c789",
		single="a1  2  3b4  5  6c7  8  9",
		double="",
		triple=""),
	# Thousands separator with letters
	NrProcTestCase(origin="1a.234b",
		single="1a.2  3  4b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a.2.345b",
		single="1a.2  3  4  5b",
		double="",
		triple=""),
	# Decimal with letters
	NrProcTestCase(origin="1a,234b",
		single="1a,2  3  4b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a,2,345b",
		single="1a,2,3  4  5b",
		double="",
		triple=""),
]

# Swedish
nrProcTestCases["sv"] = [
	NrProcTestCase(origin="1",
		single="1",
		double="",
		triple=""),
	NrProcTestCase(origin="11",
		single="1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="111",
		single="1  1  1",
		double="",
		triple=""),
	# Decimals
	NrProcTestCase(origin="1,1",
		single="1,1",
		double="",
		triple=""),
	NrProcTestCase(origin="11,1",
		single="1  1,1",
		double="",
		triple=""),
	NrProcTestCase(origin="111,1",
		single="1  1  1,1",
		double="",
		triple=""),
	NrProcTestCase(origin="1,11",
		single="1,1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="1,111",
		single="1,1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="11,111",
		single="1  1,1  1  1",
		double="",
		triple=""),
	NrProcTestCase(origin="111,111",
		single="1  1  1,1  1  1",
		double="",
		triple=""),
	# Thousands separator, Swedish uses a non breaking space
	NrProcTestCase(origin="1\xa0234",
		single="1  2  3  4",
		double="",
		triple=""),
	NrProcTestCase(origin="12\xa0345",
		single="1  2  3  4  5",
		double="",
		triple=""),
	NrProcTestCase(origin="123\xa0456",
		single="1  2  3  4  5  6",
		double="",
		triple=""),
	NrProcTestCase(origin="1\xa0234\xa0567",
		single="1  2  3  4  5  6  7",
		double="",
		triple=""),
	# Mixed with letters
	NrProcTestCase(origin="a1b2c3",
		single="a1b2c3",
		double="",
		triple=""), # Untouched
	NrProcTestCase(origin="a12b34c56",
		single="a1  2b3  4c5  6",
		double="",
		triple=""),
	NrProcTestCase(origin="a123b456c789",
		single="a1  2  3b4  5  6c7  8  9",
		double="",
		triple=""),
	# Thousands separator with letters
	NrProcTestCase(origin="1a\xa0234b",
		single="1a\xa02  3  4b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a\xa02\xa0345b",
		single="1a\xa02  3  4  5b",
		double="",
		triple=""),
	# Decimal with letters
	NrProcTestCase(origin="1a,234b",
		single="1a,2  3  4b",
		double="",
		triple=""),
	NrProcTestCase(origin="1a,2,345b",
		single="1a,2,3  4  5b",
		double="",
		triple=""),
]

# German, equal to Dutch
nrProcTestCases["de"] = nrProcTestCases["nl"]

class testNumberPronunciation(unittest.TestCase):
	"""
	Tests the pronunciation of numbers for the several levels of digit reporting,
	(i.e. single digits, double digits, triplle digits).
	Whole numbers isn't tested, as in that case, the number input isn't touched at all.
	"""

	longMessage = True

	MODE_TO_TYPE_STRING_MAP = {
		characterProcessing.NR_PROC_FULL: "origin",
		characterProcessing.NR_PROC_SINGLE: "single",
		characterProcessing.NR_PROC_DOUBLE: "double",
		characterProcessing.NR_PROC_TRIPLE: "triple",
	}

	def _testDigitsHelper(self, mode):
		modeStr = self.MODE_TO_TYPE_STRING_MAP[mode]
		for locale, cases in nrProcTestCases.iteritems():
			processor = characterProcessing._localeSpeechSymbolProcessors.fetchLocaleData(locale)
			for case in cases:
				self.assertEqual(
					processor.processNumbers(mode, case.origin),
					getattr(case, modeStr),
					msg="Locale=%s, mode=%s, origin=%s" % (locale, modeStr, case.origin)
				)

	def test_singleDigits(self):
		self._testDigitsHelper(characterProcessing.NR_PROC_SINGLE)

#	def test_doubleDigits(self):
#		self._testDigitsHelper(characterProcessing.NR_PROC_DOUBLE)
