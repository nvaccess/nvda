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
	"ckb",
	"kmr",
	"mn",
	"my",
	"ne",
	"so",
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

	def setUp(self):
		"""
		`setLocale` doesn't change `languageHandler.curLang`, so reset the locale using `setLanguage` to
		the current language for each test.
		"""
		languageHandler.setLanguage(languageHandler.curLang)

	@classmethod
	def tearDownClass(cls):
		"""
		`setLocale` doesn't change `languageHandler.curLang`, so reset the locale using `setLanguage` to
		the current language so the tests can continue normally.
		"""
		languageHandler.setLanguage(languageHandler.curLang)

	def test_SetLocale_SupportedLocale_LocaleIsSet(self):
		"""
		Tests several locale formats that should result in an expected python locale being set.
		"""
		for localeName in self.SUPPORTED_LOCALES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName[0])
				self.assertEqual(locale.getlocale()[0], localeName[1])

	def test_SetLocale_PythonUnsupportedLocale_LocaleUnchanged(self):
		"""
		Tests several locale formats that python doesn't support which will result in a return to the
		current locale
		"""
		original_locale = locale.getlocale()
		for localeName in UNSUPPORTED_PYTHON_LOCALES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				self.assertEqual(locale.getlocale(), original_locale)

	def test_SetLocale_NVDASupportedAndPythonSupportedLocale_LanguageCodeMatches(self):
		"""
	 	Tests all the translatable languages that NVDA shows in the user preferences
		excludes the locales that python doesn't support, as the expected behaviour is different.
		"""
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

	def test_SetLocale_WindowsLang_LocaleCanBeRetrieved(self):
		"""
		We don't know whether python supports a specific windows locale so just ensure locale isn't
		broken after testing these values.
		"""
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
		"""
		Resets the language to whatever it was before the testing suite begun.
		"""
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

	def test_SetLanguage_NVDASupportedLanguages_LanguageIsSetCorrectly(self):
		"""
		Tests languageHandler.setLanguage, using all NVDA supported languages, which should do the following:
		- set the translation service and languageHandler.curLang
		- set the windows locale for the thread (fallback to system default)
		- set the python locale for the thread (match the translation service, fallback to system default)
		"""
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
					# our translatable locale isn't supported by windows
					# check that the system locale is unchanged
					self.assertEqual(self._defaultThreadLocaleName, threadLocaleName)
				else:
					# check that the language codes are correctly set for the thread
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
					# checks that the language codes part of the locales are correct
					pythonLang = python_locale[0].split("_")[0]
					self.assertEqual(
						langOnly, pythonLang, f"full values: {localeName} {python_locale}"
					)

	def test_SetLanguage_WindowsLanguages_NoErrorsThrown(self):
		"""
		We don't know whether python or our translator system supports a specific windows locale
		so just ensure the setLanguage process doesn't fail.
		"""
		for localeName in WINDOWS_LANGS:
			with self.subTest(localeName=localeName):
				languageHandler.setLanguage(localeName)
