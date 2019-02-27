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

nrProcSingleTestCases = {}

# English
nrProcSingleTestCases["en"] = {
	"1": "1",
	"11": "1  1",
	"111": "1  1  1",
	# Decimals
	"1.1": "1.1",
	"11.1": "1  1.1",
	"111.1": "1  1  1.1",
	"1.11": "1.1  1",
	"1.111": "1.1  1  1",
	"11.111": "1  1.1  1  1",
	"111.111": "1  1  1.1  1  1",
	# Thousands separator
	"1,234": "1  2  3  4",
	"12,345": "1  2  3  4  5",
	"123,456": "1  2  3  4  5  6",
	"1,234,567": "1  2  3  4  5  6  7",
}

# Dutch
nrProcSingleTestCases["nl"] = {
	"1": "1",
	"11": "1  1",
	"111": "1  1  1",
	# Decimals
	"1,1": "1,1",
	"11,1": "1  1,1",
	"111,1": "1  1  1,1",
	"1,11": "1,1  1",
	"1,111": "1,1  1  1",
	"11,111": "1  1,1  1  1",
	"111,111": "1  1  1,1  1  1",
	# Thousands separator
	"1.234": "1  2  3  4",
	"12.345": "1  2  3  4  5",
	"123.456": "1  2  3  4  5  6",
	"1.234.567": "1  2  3  4  5  6  7",
}

# Swedish
nrProcSingleTestCases["sv"] = {
	"1": "1",
	"11": "1  1",
	"111": "1  1  1",
	# Decimals
	"1,1": "1,1",
	"11,1": "1  1,1",
	"111,1": "1  1  1,1",
	"1,11": "1,1  1",
	"1,111": "1,1  1  1",
	"11,111": "1  1,1  1  1",
	"111,111": "1  1  1,1  1  1",
	# Thousands separator, Swedish uses a non breaking space
	"1\xa0234": "1  2  3  4",
	"12\xa0345": "1  2  3  4  5",
	"123\xa0456": "1  2  3  4  5  6",
	"1\xa0234\xa0567": "1  2  3  4  5  6  7",
}

# German, equal to Dutch
nrProcSingleTestCases["de"] = nrProcSingleTestCases["nl"].copy()

class testNumberPronunciation(unittest.TestCase):
	"""
	Tests the pronunciation of numbers for the several levels of digit reporting,
	(i.e. single digits, double digits, triplle digits).
	Whole numbers isn't tested, as in that case, the number input isn't touched at all.
	"""

	longMessage = True

	def test_singleDigits(self):
		for locale, cases in nrProcSingleTestCases.iteritems():
			processor = characterProcessing._localeSpeechSymbolProcessors.fetchLocaleData(locale)
			for origin, replacement in cases.iteritems():
				self.assertEqual(
					processor.processNumbers(characterProcessing.NR_PROC_SINGLE, origin),
					replacement,
					msg="Locale=%s, origin=%s" % (locale, origin)
				)
