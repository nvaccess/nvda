# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2017-2022 NV Access Limited, Łukasz Golonka

"""Unit tests for the languageHandler module.
"""

import unittest
import languageHandler
from languageHandler import LCID_NONE, LCIDS_TO_TRANSLATED_LOCALES
from localesData import LANG_NAMES_TO_LOCALIZED_DESCS
import locale
import ctypes


def generateUnsupportedWindowsLocales():
	"""Generates list of languages which are not supported under the current version of Windows.
	Uses `localesData.LANG_NAMES_TO_LOCALIZED_DESCS` as a base but filters further
	since unsupported languages are different under different systems."""
	unsupportedLangs = set()
	for localeName in LANG_NAMES_TO_LOCALIZED_DESCS.keys():
		# `languageHandler.englishCountryNameFromNVDALocale` returns `None` for locale unknown to Windows.
		if not languageHandler.englishCountryNameFromNVDALocale(localeName):
			unsupportedLangs.add(localeName)
	return unsupportedLangs


LCID_ENGLISH_US = 0x0409
UNSUPPORTED_WIN_LANGUAGES = generateUnsupportedWindowsLocales()
TRANSLATABLE_LANGS = set(l[0] for l in languageHandler.getAvailableLanguages()) - {"Windows"}
WINDOWS_LANGS = set(locale.windows_locale.values()).union(LCIDS_TO_TRANSLATED_LOCALES.values())


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


class Test_Normalization_For_Win32(unittest.TestCase):

	def test_isNormalizedWin32LocaleNormalizedLocale(self):
		self.assertTrue(languageHandler.isNormalizedWin32Locale("en"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("ro"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("so"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("ckb"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("de-CH"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("pl-PL"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("de-DE_phoneb"))
		self.assertTrue(languageHandler.isNormalizedWin32Locale("mn-Mong-CN"))

	def test_isNormalizedWin32LocaleInvalidLocales(self):
		self.assertFalse(languageHandler.isNormalizedWin32Locale("pl_PL"))
		self.assertFalse(languageHandler.isNormalizedWin32Locale("de_CH"))
		self.assertFalse(languageHandler.isNormalizedWin32Locale("ru_RU"))

	def test_localeNormalizationForWin32(self):
		self.assertEqual(languageHandler.normalizeLocaleForWin32("en"), "en")
		self.assertEqual(languageHandler.normalizeLocaleForWin32("en-US"), "en-US")
		self.assertEqual(languageHandler.normalizeLocaleForWin32("en_US"), "en-US")
		self.assertEqual(languageHandler.normalizeLocaleForWin32("de-DE_phoneb"), "de-DE_phoneb")
		self.assertEqual(languageHandler.normalizeLocaleForWin32("de_DE_phoneb"), "de-DE_phoneb")


class Test_GetLocaleInfoEx_Wrappers(unittest.TestCase):
	"""Set of tests for wrappers around `GetLocaleInfoEx` from `languageHandler`"""

	POSSIBLE_CODE_PAGES_FOR_UNICODE_ONLY_LOCALES = {str(ctypes.windll.kernel32.GetACP()), "65001"}

	def test_ValidEnglishLangNamesAreReturned(self):
		"""Smoke tests `languageHandler.englishLanguageNameFromNVDALocale` with some known locale names"""
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("en"), "English")
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("de"), "German")
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("ne"), "Nepali")
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("pt-BR"), "Portuguese")
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("de_CH"), "German")

	def test_noLangNameFromUnknownLocale(self):
		"""Smoke tests `languageHandler.englishLanguageNameFromNVDALocale`
		with locale names unknown to Windows"""
		self.assertIsNone(languageHandler.englishLanguageNameFromNVDALocale("an"))
		self.assertIsNone(languageHandler.englishLanguageNameFromNVDALocale("kmr"))

	def test_englishLanguageNameFromNVDALocaleNonASCIILangNames(self):
		"""Ensures that `languageHandler.englishLanguageNameFromNVDALocale`
		can deal with non ASCII language names returned from Windows."""
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("nb"), "Norwegian")
		self.assertEqual(languageHandler.englishLanguageNameFromNVDALocale("nb_NO"), "Norwegian")

	def test_ValidEnglishCountryNamesAreReturned(self):
		"""Smoke tests `languageHandler.englishCountryNameFromNVDALocale` with some known locale names"""
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("en"), "United States")
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("de"), "Germany")
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("ne"), "Nepal")
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("pt-BR"), "Brazil")
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("pt-PT"), "Portugal")
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("de_CH"), "Switzerland")

	def test_noCountryNameFromUnknownLocale(self):
		"""Smoke tests `languageHandler.englishCountryNameFromNVDALocale`
		with locale names unknown to Windows"""
		self.assertIsNone(languageHandler.englishCountryNameFromNVDALocale("an"))
		self.assertIsNone(languageHandler.englishCountryNameFromNVDALocale("kmr"))

	def test_englishCountryNameFromNVDALocaleLocaleWithDot(self):
		"""Ensures that `languageHandler.englishCountryNameFromNVDALocale` removes all dots
		from the affected country names."""
		self.assertEqual(languageHandler.englishCountryNameFromNVDALocale("zh_HK"), "Hong Kong SAR")

	def test_validAnsiCodePagesAreReturned(self):
		"""Smoke tests `languageHandler.ansiCodePageFromNVDALocale` with some known
		not Unicode only locale names"""
		self.assertEqual(languageHandler.ansiCodePageFromNVDALocale("en"), "1252")
		self.assertEqual(languageHandler.ansiCodePageFromNVDALocale("pl_PL"), "1250")
		self.assertEqual(languageHandler.ansiCodePageFromNVDALocale("ja_JP"), "932")
		self.assertEqual(languageHandler.ansiCodePageFromNVDALocale("de-CH"), "1252")

	def test_noCodePageFromUnknownLocale(self):
		"""Smoke tests `languageHandler.ansiCodePageFromNVDALocale`
		with locale names unknown to Windows"""
		self.assertIsNone(languageHandler.ansiCodePageFromNVDALocale("an"))
		self.assertIsNone(languageHandler.ansiCodePageFromNVDALocale("kmr"))

	def test_validAnsiCodePagesAreReturnedUnicodeOnlyLocales(self):
		"""Smoke tests `languageHandler.ansiCodePageFromNVDALocale` with some known
		Unicode only locale names"""
		self.assertIn(
			languageHandler.ansiCodePageFromNVDALocale("hi"),
			self.POSSIBLE_CODE_PAGES_FOR_UNICODE_ONLY_LOCALES
		)
		self.assertIn(
			languageHandler.ansiCodePageFromNVDALocale("Ne"),
			self.POSSIBLE_CODE_PAGES_FOR_UNICODE_ONLY_LOCALES
		)


class Test_languageHandler_setLocale(unittest.TestCase):
	"""Tests for the function languageHandler.setLocale"""

	SUPPORTED_LOCALES = [
		("en", 'English_United States.1252'),
		("fa-IR", "Persian_Iran.1256"),
		("pl_PL", "Polish_Poland.1250")
	]

	def setUp(self):
		"""
		`setLocale` doesn't change current NVDA language, so reset the locale using `setLanguage` to
		the current language for each test.
		"""
		languageHandler.setLanguage(languageHandler.getLanguage())

	@classmethod
	def tearDownClass(cls):
		"""
		`setLocale` doesn't change current NVDA language, so reset the locale using `setLanguage` to
		the current language so the tests can continue normally.
		"""
		languageHandler.setLanguage(languageHandler.getLanguage())

	def test_SupportedLocale_LocaleIsSet(self):
		"""
		Tests several locale formats that should result in an expected python locale being set.
		"""
		for localeName in self.SUPPORTED_LOCALES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName[0])
				self.assertEqual(locale.setlocale(locale.LC_ALL), localeName[1])

	def test_PythonUnsupportedLocale_LocaleUnchanged(self):
		"""
		Tests several locale formats that python doesn't support which will result in a return to the
		current locale
		"""
		original_locale = locale.setlocale(locale.LC_ALL)
		for localeName in UNSUPPORTED_WIN_LANGUAGES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				self.assertEqual(locale.setlocale(locale.LC_ALL), original_locale)

	def test_NVDASupportedAndPythonSupportedLocale_LanguageCodeMatches(self):
		"""
	 	Tests all the translatable languages that NVDA shows in the user preferences
		excludes the locales that python doesn't support, as the expected behaviour is different.
		"""
		for localeName in TRANSLATABLE_LANGS - UNSUPPORTED_WIN_LANGUAGES:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				current_locale = locale.setlocale(locale.LC_ALL)
				# check that the language codes are correctly set for python
				# They can be set to the exact locale that was requested, to the locale gotten
				# from the language name if language_country cannot be set
				# or just to English name of the language.
				lang_country = languageHandler.localeStringFromLocaleCode(localeName)
				possibleVariants = {lang_country}
				if "65001" in lang_country:
					# Python normalizes Unicode Windows code page to 'utf8'
					possibleVariants.add(lang_country.replace("65001", "utf8"))
				if "_" in lang_country:
					possibleVariants.add(languageHandler.localeStringFromLocaleCode(localeName.split("_")[0]))
				possibleVariants.add(languageHandler.englishLanguageNameFromNVDALocale(localeName))
				self.assertIn(
					current_locale,
					possibleVariants,
					f"full values: {localeName} {current_locale}",
				)

	def test_WindowsLang_LocaleCanBeRetrieved(self):
		"""
		We don't know whether python supports a specific windows locale so just ensure locale isn't
		broken after testing these values.
		Even though we cannot use `locale.getlocale` when checking if the correct locale has been set
		in all other tests since it normalizes locale making it impossible to do comparisons
		it is important that whatever is being set can be retrieved with `getlocale`
		since some parts of Python standard library such as `time.strptime` relies on `getlocale`
		being able to return current locale.
		"""
		for localeName in WINDOWS_LANGS:
			with self.subTest(localeName=localeName):
				languageHandler.setLocale(localeName)
				locale.getlocale()


class Test_LanguageHandler_SetLanguage(unittest.TestCase):
	"""Tests for the function languageHandler.setLanguage"""

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
		self._defaultPythonLocale = locale.setlocale(locale.LC_ALL)

		languageHandler.setLanguage(self._prevLang)
		super().__init__(*args, **kwargs)

	def test_NVDASupportedLanguages_LanguageIsSetCorrectly(self):
		"""
		Tests languageHandler.setLanguage, using all NVDA supported languages, which should do the following:
		- set the translation service and current NVDA language
		- set the windows locale for the thread (fallback to system default)
		- set the python locale for the thread (match the translation service, fallback to system default)
		"""
		for localeName in TRANSLATABLE_LANGS:
			with self.subTest(localeName=localeName):
				langOnly = localeName.split("_")[0]
				languageHandler.setLanguage(localeName)
				# check current NVDA language/translation service is set
				self.assertEqual(languageHandler.getLanguage(), localeName)

				# check Windows thread is set
				threadLocale = ctypes.windll.kernel32.GetThreadLocale()
				threadLocaleName = languageHandler.windowsLCIDToLocaleName(threadLocale)
				threadLocaleLang = threadLocaleName.split("_")[0]
				if localeName in UNSUPPORTED_WIN_LANGUAGES:
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
				python_locale = locale.setlocale(locale.LC_ALL)
				if localeName in UNSUPPORTED_WIN_LANGUAGES:
					# our translatable locale isn't supported by python
					# check that the system locale is unchanged
					self.assertEqual(self._defaultPythonLocale, python_locale)
				else:
					# check that the language codes are correctly set for python
					# They can be set to the exact locale that was requested, to the locale gotten
					# from the language name if language_country cannot be set
					# or just to English name of the language.
					lang_country = languageHandler.localeStringFromLocaleCode(localeName)
					possibleVariants = {lang_country}
					if "65001" in lang_country:
						# Python normalizes Unicode Windows code page to 'utf8'
						possibleVariants.add(lang_country.replace("65001", "utf8"))
					if "_" in lang_country:
						possibleVariants.add(languageHandler.localeStringFromLocaleCode(localeName.split("_")[0]))
					possibleVariants.add(languageHandler.englishLanguageNameFromNVDALocale(localeName))
					self.assertIn(
						locale.setlocale(locale.LC_ALL),
						possibleVariants,
						f"full values: {localeName} {python_locale}"
					)

	def test_WindowsLanguages_NoErrorsThrown(self):
		"""
		We don't know whether python or our translator system supports a specific windows locale
		so just ensure the setLanguage process doesn't fail.
		"""
		for localeName in WINDOWS_LANGS:
			with self.subTest(localeName=localeName):
				languageHandler.setLanguage(localeName)


class Test_language_Normalization_for_NVDA(unittest.TestCase):
	"""Set of unit tests for `languageHandler.normalizeLanguage`."""

	def test_normalization_no_country_info(self):
		"""Makes sure that if no country info is provided language is normalized to lower case."""
		self.assertEqual("en", languageHandler.normalizeLanguage("en"))
		self.assertEqual("en", languageHandler.normalizeLanguage("EN"))
		self.assertEqual("kmr", languageHandler.normalizeLanguage("kmr"))

	def test_underscore_used_as_separator_after_normalization(self):
		"""Ensures that underscore is used to separate country info from language.
		Also implicitly test the fact that country code is converted to upper case."""
		self.assertEqual("pt_BR", languageHandler.normalizeLanguage("pt_BR"))
		self.assertEqual("pt_BR", languageHandler.normalizeLanguage("pt-BR"))

	def test_meta_languages_no_normalization(self):
		"""Ensures that for meta languages such as x-western `None` is returned."""
		self.assertIsNone(languageHandler.normalizeLanguage("x-western"))


class test_getAvailableLanguages(unittest.TestCase):
	"""Set of unit tests for `languageHandler.getAvailableLanguages`"""

	def test_langsListExpectedFormat(self):
		"""Ensures that for all languages except user default each element of the returned list consists of
		language code, and language  description containing language code
		(necessary since lang descriptions are localized to the default Windows language)."""
		for langCode, langDesc in languageHandler.getAvailableLanguages()[1:]:
			self.assertIn(langCode, langDesc)
			self.assertIn(languageHandler.getLanguageDescription(langCode), langDesc)

	def test_knownLanguageCodesInList(self):
		"""Ensure that expected languages are in the list."""
		langCodes = [lang[0] for lang in languageHandler.getAvailableLanguages()]
		self.assertIn("pl", langCodes)
		self.assertIn("ru", langCodes)
		self.assertIn("zh_TW", langCodes)
		self.assertIn("kmr", langCodes)

	def test_langsWithOutTranslationsNotInList(self):
		"""Ensure that languages which do  not have a translations
		(i.e. only symbol  files are present) are excluded ."""
		langCodes = [lang[0] for lang in languageHandler.getAvailableLanguages()]
		self.assertNotIn("be", langCodes)
		self.assertNotIn("te", langCodes)
		self.assertNotIn("zh", langCodes)
		self.assertNotIn("kok", langCodes)

	def test_manuallyAddedLocalesPresentInList(self):
		"""Some locales do not have translations, yet they should be  present in the list."""
		langCodes = [lang[0] for lang in languageHandler.getAvailableLanguages()]
		self.assertEqual("Windows", langCodes[0])
		self.assertIn("en", langCodes)

	def test_noDuplicates(self):
		seenLangCodes = set()
		seenLangDescs = set()
		for langCode, langDesc in languageHandler.getAvailableLanguages():
			self.assertNotIn(langCode, seenLangCodes)
			seenLangCodes.add(langCode)
			self.assertNotIn(langDesc, seenLangDescs)
			seenLangDescs.add(langDesc)

	def test_userDefaultDescriptionIsCorrect(self):
		"""Description for the 'user default' should not contain a language code."""
		userDefaultLangCode, userDefaultLangDesc = languageHandler.getAvailableLanguages()[0]
		self.assertEqual(userDefaultLangCode, "Windows")
		self.assertNotIn(userDefaultLangCode, userDefaultLangDesc)
