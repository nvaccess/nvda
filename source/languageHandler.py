# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2021 NV access Limited, Joseph Lee, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Language and localization support.
This module assists in NVDA going global through language services
such as converting Windows locale ID's to friendly names and presenting available languages.
"""

import builtins
import os
import sys
import ctypes

import weakref

import locale
import gettext
import enum
import globalVars
from logHandler import log
import winKernel
from typing import (
	FrozenSet,
	List,
	Optional,
	Tuple,
	Union,
)

#a few Windows locale constants
LOCALE_USER_DEFAULT = 0x400
LOCALE_CUSTOM_UNSPECIFIED = 0x1000

# A constant returned when asking Windows for a default code page for a given locale
# and its code page is the default code page for non Unicode programs set in Windows.
CP_ACP = "0"

#: Returned from L{localeNameToWindowsLCID} when the locale name cannot be mapped to a locale identifier.
#: This might be because Windows doesn't know about the locale (e.g. "an"),
#: because it is not a standardized locale name anywhere (e.g. "zz")
#: or because it is not a legal locale name (e.g. "zzzz").
LCID_NONE = 0 # 0 used instead of None for backwards compatibility.

LANGS_WITHOUT_TRANSLATIONS: FrozenSet[str] = frozenset(("en",))

installedTranslation: Optional[weakref.ReferenceType] = None
"""Saved copy of the installed translation for ease of wrapping.
"""

LCIDS_TO_TRANSLATED_LOCALES = {
	# Windows maps this to "ku-Arab-IQ", however a translation is added for
	# Central Kurdish in localesData.LANG_NAMES_TO_LOCALIZED_DESCS["ckb"]
	# and NVDA may drop "Arab-IQ" from this locale to get the language.
	1170: 'ckb'
}
"""
Map Windows locale identifiers to language codes.
These are Windows LCIDs that are used in NVDA but are not found in locale.windows_locale.
These have been added when new locales have been introduced to the translation system and
we cannot use the results from the Windows function LCIDToLocaleName.
"""


class LOCALE(enum.IntEnum):
	# Represents NLS constants which can be used with `GetLocaleInfoEx` or `GetLocaleInfoW`
	# Full list of these constants is available at:
	# https://docs.microsoft.com/en-us/windows/win32/intl/locale-information-constants
	SLANGUAGE = 0x2
	SLIST = 0xC
	IMEASURE = 0xD
	SLANGDISPLAYNAME = 0x6f
	SENGLISHLANGUAGENAME = 0x00001001
	SENGLISHCOUNTRYNAME = 0x00001002
	IDEFAULTANSICODEPAGE = 0x00001004


def isNormalizedWin32Locale(localeName: str) -> bool:
	"""Checks if the given locale is in a form which can be used by Win32 locale functions such as
	`GetLocaleInfoEx`. See `normalizeLocaleForWin32` for more comments."""
	hyphensCount = localeName.count("-")
	underscoresCount = localeName.count("_")
	if not hyphensCount and not underscoresCount:
		return True
	if hyphensCount:
		return True
	return False


def normalizeLocaleForWin32(localeName: str) -> str:
	"""Converts given locale to a form which can be used by Win32 locale functions such as
	`GetLocaleInfoEx` unless locale is normalized already.
	Uses hyphen as a language/country separator taking care not to replace underscores used
	as a separator between country name and alternate order specifiers.
	For example locales using alternate sorts see:
	https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-lcid/e6a54e86-9660-44fa-a005-d00da97722f2
	While NVDA does not support locales requiring multiple sorting orders users may still have their Windows
	set to such locale and if all underscores were replaced unconditionally
	we would be unable to generate Python locale from their default UI language.
	"""
	if not isNormalizedWin32Locale(localeName):
		localeName = localeName.replace('_', '-', 1)
	return localeName


def localeNameToWindowsLCID(localeName: str) -> int:
	"""Retrieves the Windows locale identifier (LCID) for the given locale name
	@param localeName: a string of 2letterLanguage_2letterCountry
	or just language (2letterLanguage or 3letterLanguage)
	@returns: a Windows LCID or L{LCID_NONE} if it could not be retrieved.
	"""
	# Windows Vista (NT 6.0) and later is able to convert locale names to LCIDs.
	# Because NVDA supports Windows 7 (NT 6.1) SP1 and later, just use it directly.
	localeName = normalizeLocaleForWin32(localeName)
	LCID=ctypes.windll.kernel32.LocaleNameToLCID(localeName,0)
	# #6259: In Windows 10, LOCALE_CUSTOM_UNSPECIFIED is returned for any locale name unknown to Windows.
	# This was observed for Aragonese ("an").
	# See https://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.lcid(v=vs.110).aspx.
	if LCID==LOCALE_CUSTOM_UNSPECIFIED:
		LCID=LCID_NONE
	return LCID


def windowsLCIDToLocaleName(lcid: int) -> Optional[str]:
	"""
	Gets a normalized locale from a Windows LCID.

	NVDA should avoid relying on LCIDs in future, as they have been deprecated by MS:
	https://docs.microsoft.com/en-us/globalization/locale/locale-names
	"""
	# From the locale.windows_locale in-line code documentation: (#4203)
	# 	This list has been updated to include every locale up to Windows Vista.
	# 	NOTE: this mapping is incomplete.
	localeName = locale.windows_locale.get(lcid)
	# Check a manual mapping before using Windows to look up the correct LCID locale name.
	if not localeName:
		localeName = LCIDS_TO_TRANSLATED_LOCALES.get(lcid)
	if not localeName:
		localeName = winKernel.LCIDToLocaleName(lcid)
	if localeName:
		return normalizeLanguage(localeName)


def getLanguageDescription(language: str) -> Optional[str]:
	"""Finds out the description (localized full name) of a given local name"""
	if language == "Windows":
		# Translators: the label for the Windows default NVDA interface language.
		return _("User default")
	desc=None
	LCID=localeNameToWindowsLCID(language)
	if LCID is not LCID_NONE:
		buf=ctypes.create_unicode_buffer(1024)
		#If the original locale didn't have country info (was just language) then make sure we just get language from Windows
		if '_' not in language:
			res = ctypes.windll.kernel32.GetLocaleInfoW(LCID, LOCALE.SLANGDISPLAYNAME, buf, 1024)
		else:
			res=0
		if res==0:
			res = ctypes.windll.kernel32.GetLocaleInfoW(LCID, LOCALE.SLANGUAGE, buf, 1024)
		desc=buf.value
	if not desc:
		#Some hard-coded descriptions where we know the language fails on various configurations.
		# Imported lazily since langs description are translatable
		# and `languageHandler` is responsible for setting the translation.
		import localesData
		desc = localesData.LANG_NAMES_TO_LOCALIZED_DESCS.get(language, None)
	return desc


def englishLanguageNameFromNVDALocale(localeName: str) -> Optional[str]:
	"""Returns either English name of the given language  using `GetLocaleInfoEx` or None
	if the given locale is not known to Windows."""
	localeName = normalizeLocaleForWin32(localeName)
	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHLANGUAGENAME, None, 0)
	if buffLength:
		buf = ctypes.create_unicode_buffer(buffLength)
		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHLANGUAGENAME, buf, buffLength)
		langName = buf.value
		if "Unknown" in langName:
			# Windows 10 returns 'Unknown' for locales not known to Windows
			# even though documentation states that in case of an unknown locale 0 is returned.
			return None
		try:
			langName.encode("ascii")
			return langName
		except UnicodeEncodeError:
			# The language name cannot be encoded in ASCII which unfortunately means we wonn't be able
			# to set Python's locale to it (Python issue 26024).
			# this has been observed for Norwegian
			# (language name as returned from Windows is 'Norwegian Bokmål').
			# Thankfully keeping just the ASCII part of the string yields the desired result.
			partsList = []
			for part in langName.split():
				try:
					part.encode("ascii")
					partsList.append(part)
				except UnicodeEncodeError:
					continue
			return " ".join(partsList)
	return None


def englishCountryNameFromNVDALocale(localeName: str) -> Optional[str]:
	"""Returns either English name of the given country using GetLocaleInfoEx or None
	if the given locale is not known to Windows."""
	localeName = normalizeLocaleForWin32(localeName)
	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHCOUNTRYNAME, None, 0)
	if buffLength:
		buf = ctypes.create_unicode_buffer(buffLength)
		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.SENGLISHCOUNTRYNAME, buf, buffLength)
		if "Unknown" in buf.value:
			# Windows 10 returns 'Unknown region' for locales not known to Windows
			# even though documentation states that in case of an unknown locale 0 is returned.
			return None
		# Country name can contain dots such as 'Hong Kong S.A.R.'.
		# Python's `setlocale` cannot deal with that.
		# Removing dots works though.
		return buf.value.replace(".", "")
	return None


def ansiCodePageFromNVDALocale(localeName: str) -> Optional[str]:
	"""Returns either ANSI code page for a given locale using GetLocaleInfoEx or None
	if the given locale is not known to Windows."""
	localeName = normalizeLocaleForWin32(localeName)
	# Windows 10 returns English code page (1252) for locales not known to Windows
	# even though documentation states that in case of an unknown locale 0 is returned.
	# This means that it is impossible to differentiate locales that are unknown
	# and locales using 1252 as ANSI code page.
	# Use `englishCountryNameFromNVDALocale` to determine if the given locale is supported or not
	# before attempting to retrieve code page.
	if not englishCountryNameFromNVDALocale(localeName):
		return None
	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.IDEFAULTANSICODEPAGE, None, 0)
	if buffLength:
		buf = ctypes.create_unicode_buffer(buffLength)
		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE.IDEFAULTANSICODEPAGE, buf, buffLength)
		codePage = buf.value
		if codePage == CP_ACP:
			# Some locales such as Hindi are Unicode only i.e. they don't have specific ANSI code page.
			# In such case code page should be set to the default ANSI code page of the system.
			codePage = str(winKernel.kernel32.GetACP())
		return codePage
	return None


def listNVDALocales() -> List[str]:
	# Make a list of all the locales found in NVDA's locale dir
	localesDir = os.path.join(globalVars.appDir, 'locale')
	locales = [
		x for x in os.listdir(localesDir) if os.path.isfile(os.path.join(localesDir, x, 'LC_MESSAGES', 'nvda.mo'))
	]
	# Make sure that en (english) is in the list as it may not have any locale files, but is default
	if 'en' not in locales:
		locales.append('en')
		locales.sort()
	# include a 'user default, windows' language,
	# which just represents the default language for this user account
	locales.insert(0, "Windows")
	return locales


def getAvailableLanguages(presentational: bool = False) -> List[Tuple[str, str]]:
	"""generates a list of locale names, plus their full localized language and country names.
	@param presentational: whether this is meant to be shown alphabetically by language description
	"""
	locales = listNVDALocales()
	# Prepare a 2-tuple list of language code and human readable language description.
	langs = [(lc, getLanguageDescription(lc)) for lc in locales]
	# Translators: The pattern defining how languages are displayed and sorted in in the general
	# setting panel language list. Use "{desc}, {lc}" (most languages) to display first full language

	# name and then ISO; use "{lc}, {desc}" to display first ISO language code and then full language name.
	fullDescPattern = _("{desc}, {lc}")
	isDescFirst = fullDescPattern.find("{desc}") < fullDescPattern.find("{lc}")
	if presentational and isDescFirst:
		langs.sort(key=lambda lang: locale.strxfrm(lang[1] if lang[1] else lang[0]))
	# Make sure that the 'user default' language is first in the list.
	for index, lang in enumerate(langs):
		if lang[0] == "Windows":
			break
	userDefault = langs.pop(index)
	langs = [userDefault] + [
		(lc, (fullDescPattern.format(desc=desc, lc=lc) if desc else lc)) for lc, desc in langs
	]
	return langs


def makePgettext(translations):
	"""Obtaina  pgettext function for use with a gettext translations instance.
	pgettext is used to support message contexts,
	but Python's gettext module doesn't support this,
	so NVDA must provide its own implementation.
	"""
	if isinstance(translations, gettext.GNUTranslations):
		def pgettext(context, message):
			try:
				# Look up the message with its context.
				return translations._catalog[u"%s\x04%s" % (context, message)]
			except KeyError:
				return message
	elif isinstance(translations, gettext.NullTranslations):
		# A language with out a translation catalog, such as English.
		def pgettext(context, message):
			return message
	else:
		raise ValueError("%s is Not a GNUTranslations or NullTranslations object" % translations)
	return pgettext


def getLanguageCliArgs() -> Tuple[str, ...]:
	"""Returns all command line arguments which were used to set current NVDA language
	or an empty tuple if language has not been specified from the CLI."""
	for argIndex, argValue in enumerate(sys.argv):
		if argValue == "--lang":
			# Language was provided in a form `--lang lang_CODE`. The next position in `sys.argv` is a language code.
			# It is impossible not to provide it in this case as it would be flagged as an error
			# during arguments validation.
			return (argValue, sys.argv[argIndex + 1])
		if argValue.startswith("--lang="):
			# Language in a form `--lang=lang_CODE`
			return (argValue,)
	return tuple()


def isLanguageForced() -> bool:
	"""Returns `True` if language is provided from the command line - `False` otherwise."""
	return bool(getLanguageCliArgs())


def getWindowsLanguage():
	"""
	Fetches the locale name of the user's configured language in Windows.
	"""
	windowsLCID=ctypes.windll.kernel32.GetUserDefaultUILanguage()
	localeName = windowsLCIDToLocaleName(windowsLCID)
	if localeName:
		localeName = normalizeLanguage(localeName)
	else:
		localeName = "en"
	return localeName


def _createGettextTranslation(
		localeName: str
) -> Union[None, gettext.GNUTranslations, gettext.NullTranslations]:
	if localeName in LANGS_WITHOUT_TRANSLATIONS:
		globalVars.appArgs.language = localeName
		return gettext.translation("nvda", fallback=True)
	try:
		trans = gettext.translation("nvda", localedir="locale", languages=[localeName])
		globalVars.appArgs.language = localeName
		return trans
	except IOError:
		log.debugWarning(f"couldn't set the translation service locale to {localeName}")
		return None


def setLanguage(lang: str) -> None:
	'''
	Sets the following using `lang` such as "en", "ru_RU", or "es-ES". Use "Windows" to use the system locale
	 - the windows locale for the thread (fallback to system locale)
	 - the translation service (fallback to English)
	 - Current NVDA language (match the translation service)
	 - the python locale for the thread (match the translation service, fallback to system default)
	'''
	if lang == "Windows":
		localeName = getWindowsLanguage()
	else:
		localeName = lang
		# Set the windows locale for this thread (NVDA core) to this locale.
		LCID = localeNameToWindowsLCID(lang)
		if winKernel.kernel32.SetThreadLocale(LCID) == 0:
			log.debugWarning(f"couldn't set windows thread locale to {lang}")

	trans = _createGettextTranslation(localeName)
	if trans is None and "_" in localeName:
		localeName = localeName.split("_")[0]
		trans = _createGettextTranslation(localeName)
	if trans is None:
		trans = _createGettextTranslation("en")

	trans.install()
	setLocale(getLanguage())
	# Install our pgettext function.
	builtins.pgettext = makePgettext(trans)

	global installedTranslation
	installedTranslation = weakref.ref(trans)


def localeStringFromLocaleCode(localeCode: str) -> str:
	"""Given an NVDA locale such as 'en' or or a Windows locale such as 'pl_PL'
	creates a locale representation in a standard form for Win32
	which can be safely passed to Python's `setlocale`.
	The required format is:
	'englishLanguageName_englishCountryName.localeANSICodePage'
	Raises exception if the given locale is not known to Windows.
	"""
	normalizedLocaleCode = normalizeLocaleForWin32(localeCode)
	langName = englishLanguageNameFromNVDALocale(normalizedLocaleCode)
	if langName is None:
		raise ValueError(f"Locale code {localeCode} not supported by Windows")
	countryName = englishCountryNameFromNVDALocale(normalizedLocaleCode)
	codePage = ansiCodePageFromNVDALocale(normalizedLocaleCode)
	return f"{langName}_{countryName}.{codePage}"


def _setPythonLocale(localeString: str) -> bool:
	"""Sets Python locale to a specified one.
	Returns `True` if succesfull `False` if locale cannot be set or retrieved."""
	try:
		locale.setlocale(locale.LC_ALL, localeString)
		locale.getlocale()
		log.debug(f"set python locale to {localeString}")
		return True
	except locale.Error:
		log.debugWarning(f"python locale {localeString} could not be set")
		return False
	except ValueError:
		log.debugWarning(f"python locale {localeString} could not be retrieved with getlocale")
		return False


def setLocale(localeName: str) -> None:
	'''
	Set python's locale using a `localeName` such as "en", "ru_RU", or "es-ES".
	Will fallback on current NVDA language if it cannot be set and finally fallback to the system locale.
	Passing NVDA locales straight to python `locale.setlocale` does now work since it tries to normalize the
	parameter using `locale.normalize` which results in locales unknown to Windows (Python issue 37945).
	For example executing: `locale.setlocale(locale.LC_ALL, "pl")`
	results in locale being set to `('pl_PL', 'ISO8859-2')`
	which is meaningless to Windows,
	'''
	originalLocaleName = localeName
	localeString = ""
	try:
		localeString = localeStringFromLocaleCode(localeName)
		log.debug(f"Win32 locale string from locale code is {localeString}")
	except ValueError:
		log.debugWarning(f"Locale {localeName} not supported by Windows")
	if localeString and _setPythonLocale(localeString):
		return
	# The full form langName_country either cannot be retrieved from Windows
	# or Python cannot be set to that locale.
	# Try just with the language name.
	if "_" in localeName:
		localeName = localeName.split("_")[0]
		try:
			localeString = localeStringFromLocaleCode(localeName)
			log.debug(f"Win32 locale string from locale code is {localeString}")
		except ValueError:
			log.debugWarning(f"Locale {localeName} not supported by Windows")
	if localeString and _setPythonLocale(localeString):
		return
	# As a final fallback try setting locale just to the English name of the given language.
	localeFromLang = englishLanguageNameFromNVDALocale(localeName)
	if localeFromLang and _setPythonLocale(localeFromLang):
		return
	# Either Windows does not know the locale, or Python is unable to handle it.
	# reset to default locale
	if originalLocaleName == getLanguage():
		# reset to system locale default if we can't set the current lang's locale
		locale.setlocale(locale.LC_ALL, "")
		log.debugWarning(f"set python locale to system default")
	else:
		log.debugWarning(f"setting python locale to the current language {getLanguage()}")
		# fallback and try to reset the locale to the current lang
		setLocale(getLanguage())


def getLanguage() -> str:
	return globalVars.appArgs.language


def normalizeLanguage(lang: str) -> Optional[str]:
	"""
	Normalizes a  language-dialect string  in to a standard form we can deal with.
	Converts  any dash to underline, and makes sure that language is lowercase and dialect is upercase.
	"""
	lang=lang.replace('-','_')
	ld=lang.split('_')
	ld[0]=ld[0].lower()
	#Filter out meta languages such as x-western
	if ld[0]=='x':
		return None
	if len(ld)>=2:
		ld[1]=ld[1].upper()
	return "_".join(ld)


def useImperialMeasurements() -> bool:
	"""
	Whether or not measurements should be reported as imperial, rather than metric.
	"""
	bufLength = 2
	buf = ctypes.create_unicode_buffer(bufLength)
	if not winKernel.kernel32.GetLocaleInfoEx(None, LOCALE.IMEASURE, buf, bufLength):
		raise RuntimeError("LOCALE.IMEASURE not supported")
	return buf.value == '1'


