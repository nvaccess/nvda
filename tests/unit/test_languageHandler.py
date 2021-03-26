# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2021 NV Access Limited

"""Unit tests for the languageHandler module.
"""

import unittest
import languageHandler
from languageHandler import LCID_NONE, windowsPrimaryLCIDsToLocaleNames
import locale
import ctypes

LCID_ENGLISH_US = 0x0409
UNSUPPORTED_PYTHON_LOCALES = {
	"an",
	"arn",
	"arn_CL",
	"ba",
	"ba_RU",
	"bn",
	"bo",
	"bo_BT",
	"ckb",
	"co",
	"co_FR",
	"en_BZ",
	"en_CB",
	"en_JA",
	"en_MY",
	"en_TT",
	"en_US",
	"fil",
	"fy",
	"gbz",
	"gbz_AF",
	"gu",
	"ha",
	"hy",
	"ii",
	"ii_CN",
	"kh",
	"kh_KH",
	"kk",
	"kmr",
	"kok",
	"lb",
	"mn",
	"mn_CN",
	"moh",
	"moh_CA",
	"my",
	"ne",
	"ns",
	"ns_ZA",
	"ps",
	"qut",
	"qut_GT",
	"quz",
	"quz_BO",
	"quz_EC",
	"rm",
	"rm_CH",
	"sa",
	"se_FI",
	"se_SE",
	"so",
	"sw",
	"tk",
	"tmz",
	"tmz_DZ",
	"ug",
	"wen",
	"wen_DE",
	"wo",
	"yo",
}
TRANSLATABLE_LANGS = set(l[0] for l in languageHandler.getAvailableLanguages()) - {"Windows"}
WINDOWS_LANGS = set(locale.windows_locale.values()).union(windowsPrimaryLCIDsToLocaleNames.values())


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


class TestSetLocale(unittest.TestCase):
	"""
	Tests setting the python locale for possible locales set by NVDA user preferences or the System.
	"""

	SUPPORTED_LOCALES = [("en", "en_US"), ("fa-IR", "fa_IR"), ("an-ES", "an_ES")]

	@classmethod
	def tearDownClass(cls):
		languageHandler.setLanguage(languageHandler.curLang)

	def setUp(self):
		languageHandler.setLanguage(languageHandler.curLang)

	def testSupportedLocales(self):
		for localeName in self.SUPPORTED_LOCALES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName[0])
				self.assertEqual(locale.getlocale()[0], localeName[1])

	def testUnsupportedLocales(self):
		original_locale = locale.getlocale()
		for localeName in UNSUPPORTED_PYTHON_LOCALES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				self.assertEqual(locale.getlocale(), original_locale)

	def testAllSupportedLangs(self):
		for localeName in TRANSLATABLE_LANGS - UNSUPPORTED_PYTHON_LOCALES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				current_locale = locale.getlocale()

				if localeName == "uk":
					self.assertEqual(current_locale[0], "English_United Kingdom")
				else:
					pythonLang = current_locale[0].split("_")[0]
					langOnly = localeName.split("_")[0]
					self.assertEqual(
						langOnly,
						pythonLang,
						f"full values: {localeName} {current_locale[0]}",
					)

	def smokeTestAllWindowsLangs(self):
		'''
		We don't know whether python supports a specific windows locale so just ensure locale isn't
		broken after testing these values.
		'''
		for localeName in WINDOWS_LANGS:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				locale.getlocale()


class TestSetLanguage(unittest.TestCase):
	"""
	Tests setting the NVDA language set by NVDA user preferences or the System.
	"""
	UNSUPPORTED_WIN_LANGUAGES = ["an", "kmr"]

	def tearDown(self):
		languageHandler.setLanguage(self._prevLang)

	def __init__(self, *args, **kwargs):
		self._prevLang = languageHandler.getLanguage()

		ctypes.windll.kernel32.SetThreadLocale(0)
		defaultThreadLocale = ctypes.windll.kernel32.GetThreadLocale()
		self._defaultThreadLocaleName = languageHandler.windowsLCIDToLocaleName(
			defaultThreadLocale
		)

		locale.setlocale(locale.LC_ALL, "")
		self._defaultPythonLocale = locale.getlocale()

		languageHandler.setLanguage(self._prevLang)
		super().__init__(*args, **kwargs)

	def testTranslatableLanguages(self):
		for localeName in TRANSLATABLE_LANGS:
			with self.subTest(localeName=localeName):
				langOnly = localeName.split("_")[0]
				languageHandler.setLanguage(localeName)
				# check curLang/translation service is set
				self.assertEqual(languageHandler.curLang, localeName)

				# check Windows thread is set
				threadLocale = ctypes.windll.kernel32.GetThreadLocale()
				threadLocaleName = languageHandler.windowsLCIDToLocaleName(threadLocale)
				threadLocaleLang = threadLocaleName.split("_")[0]
				if localeName in self.UNSUPPORTED_WIN_LANGUAGES:
					self.assertEqual(self._defaultThreadLocaleName, threadLocaleName)
				else:
					# check that the language codes are correctly set
					self.assertEqual(
						langOnly,
						threadLocaleLang,
						f"full values: {localeName} {threadLocaleName}",
					)

				# check that the python locale is set
				python_locale = locale.getlocale()
				if localeName in UNSUPPORTED_PYTHON_LOCALES:
					self.assertEqual(self._defaultPythonLocale, python_locale)
				elif localeName == "uk":
					self.assertEqual(python_locale[0], "English_United Kingdom")
				else:
					pythonLang = python_locale[0].split("_")[0]
					self.assertEqual(
						langOnly, pythonLang, f"full values: {localeName} {python_locale}"
					)

	def smokeTestAllWindowsLangs(self):
		'''
		We don't know whether python or our translator system supports a specific windows locale
		so just ensure the setLanguage process doesn't fail.
		'''
		for localeName in WINDOWS_LANGS:
			with self.subTest(localeName=localeName):
				languageHandler.setLanguage(localeName)
