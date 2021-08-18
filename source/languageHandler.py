# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2021 NV access Limited, Joseph Lee
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Language and localization support.
This module assists in NVDA going global through language services such as converting Windows locale ID's to friendly names and presenting available languages.
"""

import builtins
import os
import sys
import ctypes
import locale
import gettext
import globalVars
from logHandler import log
import winKernel
from typing import Optional

#a few Windows locale constants
LOCALE_SLANGUAGE=0x2
LOCALE_SLIST = 0xC
LOCALE_SLANGDISPLAYNAME=0x6f
LOCALE_USER_DEFAULT = 0x400
LOCALE_CUSTOM_UNSPECIFIED = 0x1000
LOCALE_SENGLISHLANGUAGENAME = 0x00001001
LOCALE_SENGLISHCOUNTRYNAME = 0x00001002
LOCALE_IDEFAULTANSICODEPAGE = 0x00001004

CP_ACP = "0"

#: Returned from L{localeNameToWindowsLCID} when the locale name cannot be mapped to a locale identifier.
#: This might be because Windows doesn't know about the locale (e.g. "an"),
#: because it is not a standardized locale name anywhere (e.g. "zz")
#: or because it is not a legal locale name (e.g. "zzzz").
LCID_NONE = 0 # 0 used instead of None for backwards compatibility.

curLang="en"


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


def localeNameToWindowsLCID(localeName):
	"""Retreave the Windows locale identifier (LCID) for the given locale name
	@param localeName: a string of 2letterLanguage_2letterCountry or just language (2letterLanguage or 3letterLanguage)
	@type localeName: string
	@returns: a Windows LCID or L{LCID_NONE} if it could not be retrieved.
	@rtype: integer
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
	gets a normalized locale from a lcid
	"""
	# Look up a full locale name (language + country)
	try:
		lang = locale.windows_locale[lcid]
	except KeyError:
		# Or at least just a language-only locale name
		lang=windowsPrimaryLCIDsToLocaleNames[lcid]
	if lang:
		return normalizeLanguage(lang)

def getLanguageDescription(language):
	"""Finds out the description (localized full name) of a given local name"""
	desc=None
	LCID=localeNameToWindowsLCID(language)
	if LCID is not LCID_NONE:
		buf=ctypes.create_unicode_buffer(1024)
		#If the original locale didn't have country info (was just language) then make sure we just get language from Windows
		if '_' not in language:
			res=ctypes.windll.kernel32.GetLocaleInfoW(LCID,LOCALE_SLANGDISPLAYNAME,buf,1024)
		else:
			res=0
		if res==0:
			res=ctypes.windll.kernel32.GetLocaleInfoW(LCID,LOCALE_SLANGUAGE,buf,1024)
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
	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE_SENGLISHLANGUAGENAME, None, 0)
	if buffLength:
		buf = ctypes.create_unicode_buffer(buffLength)
		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE_SENGLISHLANGUAGENAME, buf, buffLength)
		langName = buf.value
		if "Unknown" in langName:
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
	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE_SENGLISHCOUNTRYNAME, None, 0)
	if buffLength:
		buf = ctypes.create_unicode_buffer(buffLength)
		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE_SENGLISHCOUNTRYNAME, buf, buffLength)
		if "Unknown" in buf.value:
			return None
		# Country name can contain dots such as 'Hong Kong S.A.R.'.
		# Python's `setlocale` cannot deal with that.
		# Removing dots works though.
		return buf.value.replace(".", "")
	return None


def ansiCodePageFromNVDALocale(localeName: str) -> Optional[str]:
	"""Returns either English name of the given country using GetLocaleInfoEx or None
	if the given locale is not known to Windows."""
	localeName = normalizeLocaleForWin32(localeName)
	if not englishCountryNameFromNVDALocale(localeName):
		return None
	buffLength = winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE_IDEFAULTANSICODEPAGE, None, 0)
	if buffLength:
		buf = ctypes.create_unicode_buffer(buffLength)
		winKernel.kernel32.GetLocaleInfoEx(localeName, LOCALE_IDEFAULTANSICODEPAGE, buf, buffLength)
		codePage = buf.value
		if codePage == CP_ACP:
			# Some locales such as Hindi are Unicode only i.e. they don't have specific ANSI code page.
			# In such case code page should be set to the default ANSI code page of the system.
			codePage = str(winKernel.kernel32.GetACP())
		return codePage
	return None


def getAvailableLanguages(presentational=False):
	"""generates a list of locale names, plus their full localized language and country names.
	@param presentational: whether this is meant to be shown alphabetically by language description
	@type presentational: bool
	@rtype: list of tuples
	"""
	#Make a list of all the locales found in NVDA's locale dir
	localesDir = os.path.join(globalVars.appDir, 'locale')
	locales = [
		x for x in os.listdir(localesDir) if os.path.isfile(os.path.join(localesDir, x, 'LC_MESSAGES', 'nvda.mo'))
	]
	#Make sure that en (english) is in the list as it may not have any locale files, but is default
	if 'en' not in locales:
		locales.append('en')
		locales.sort()
	# Prepare a 2-tuple list of language code and human readable language description.
	langs = [(lc, getLanguageDescription(lc)) for lc in locales]
	# Translators: The pattern defining how languages are displayed and sorted in in the general
	# setting panel language list. Use "{desc}, {lc}" (most languages) to display first full language

	# name and then ISO; use "{lc}, {desc}" to display first ISO language code and then full language name.
	fullDescPattern = _("{desc}, {lc}")
	isDescFirst = fullDescPattern.find("{desc}") < fullDescPattern.find("{lc}")
	if presentational and isDescFirst:
		langs.sort(key=lambda lang: locale.strxfrm(lang[1] if lang[1] else lang[0]))
	langs = [(lc, (fullDescPattern.format(desc=desc, lc=lc) if desc else lc)) for lc, desc in langs]
	#include a 'user default, windows' language, which just represents the default language for this user account
	langs.insert(
		0,
		# Translators: the label for the Windows default NVDA interface language.
		("Windows", _("User default"))
	)
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

def getWindowsLanguage():
	"""
	Fetches the locale name of the user's configured language in Windows.
	"""
	windowsLCID=ctypes.windll.kernel32.GetUserDefaultUILanguage()
	localeName = windowsLCIDToLocaleName(windowsLCID)
	if not localeName:
		# #4203: some locale identifiers from Windows 8 do not exist in Python's list.
		# Therefore use windows' own function to get the locale name.
		# Eventually this should probably be used all the time.
		bufSize=32
		buf=ctypes.create_unicode_buffer(bufSize)
		dwFlags=0
		try:
			ctypes.windll.kernel32.LCIDToLocaleName(windowsLCID,buf,bufSize,dwFlags)
		except AttributeError:
			pass
		localeName=buf.value
		if localeName:
			localeName=normalizeLanguage(localeName)
		else:
			localeName="en"
	return localeName


def setLanguage(lang: str) -> None:
	'''
	Sets the following using `lang` such as "en", "ru_RU", or "es-ES". Use "Windows" to use the system locale
	 - the windows locale for the thread (fallback to system locale)
	 - the translation service (fallback to English)
	 - languageHandler.curLang (match the translation service)
	 - the python locale for the thread (match the translation service, fallback to system default)
	'''
	global curLang
	if lang == "Windows":
		localeName = getWindowsLanguage()
	else:
		localeName = lang
		# Set the windows locale for this thread (NVDA core) to this locale.
		try:
			LCID = localeNameToWindowsLCID(lang)
			ctypes.windll.kernel32.SetThreadLocale(LCID)
		except IOError:
			log.debugWarning(f"couldn't set windows thread locale to {lang}")

	try:
		trans = gettext.translation("nvda", localedir="locale", languages=[localeName])
		curLang = localeName
	except IOError:
		try:
			log.debugWarning(f"couldn't set the translation service locale to {localeName}")
			localeName = localeName.split("_")[0]
			trans = gettext.translation("nvda", localedir="locale", languages=[localeName])
			curLang = localeName
		except IOError:
			log.debugWarning(f"couldn't set the translation service locale to {localeName}")
			trans = gettext.translation("nvda", fallback=True)
			curLang = "en"

	trans.install()
	setLocale(curLang)
	# Install our pgettext function.
	builtins.pgettext = makePgettext(trans)


def localeStringFromLocaleCode(localeCode: str) -> str:
	normalizedLocaleCode = normalizeLocaleForWin32(localeCode)
	langName = englishLanguageNameFromNVDALocale(normalizedLocaleCode)
	if langName is None:
		raise ValueError(f"Locale code {localeCode} not supported by Windows")
	countryName = englishCountryNameFromNVDALocale(normalizedLocaleCode)
	codePage = ansiCodePageFromNVDALocale(normalizedLocaleCode)
	return f"{langName}_{countryName}.{codePage}"


def setLocale(localeName: str) -> None:
	'''
	Set python's locale using a `localeName` such as "en", "ru_RU", or "es-ES".
	Will fallback on `curLang` if it cannot be set and finally fallback to the system locale.
	'''
	originalLocaleName = localeName
	localeString = ""
	try:
		localeString = localeStringFromLocaleCode(localeName)
		log.debug(f"Win32 locale string from locale code is {localeString}")
	except ValueError:
		log.debugWarning(f"Locale {localeName} not supported by Windows")
	if localeString:
		try:
			locale.setlocale(locale.LC_ALL, localeString)
			locale.getlocale()
			log.debug(f"set python locale to {localeString}")
			return
		except locale.Error:
			log.debugWarning(f"python locale {localeString} could not be set")
		except ValueError:
			log.debugWarning(f"python locale {localeString} could not be retrieved with getlocale")
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
	if localeString:
		try:
			locale.setlocale(locale.LC_ALL, localeString)
			locale.getlocale()
			log.debug(f"set python locale to {localeString}")
			return
		except locale.Error:
			log.debugWarning(f"python locale {localeString} could not be set")
		except ValueError:
			log.debugWarning(f"python locale {localeString} could not be retrieved with getlocale")
		localeFromLang = englishLanguageNameFromNVDALocale(localeName)
		if localeFromLang:
			try:
				locale.setlocale(locale.LC_ALL, localeFromLang)
				locale.getlocale()
				log.debug(f"set python locale to {localeFromLang}")
				return
			except locale.Error:
				log.debugWarning(f"python locale {localeFromLang} could not be set")
			except ValueError:
				log.debugWarning(f"python locale {localeFromLang} could not be retrieved with getlocale")
	if not localeString:
		# as the locale may have been changed to something that getlocale() couldn't retrieve
		# reset to default locale
		if originalLocaleName == curLang:
			# reset to system locale default if we can't set the current lang's locale
			locale.setlocale(locale.LC_ALL, "")
			log.debugWarning(f"set python locale to system default")
		else:
			log.debugWarning(f"setting python locale to the current language {curLang}")
			# fallback and try to reset the locale to the current lang
			setLocale(curLang)


def getLanguage() -> str:
	return curLang


def normalizeLanguage(lang) -> Optional[str]:
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

# Map Windows primary locale identifiers to locale names
# Note these are only primary language codes (I.e. no country information)
# For full locale identifiers we use Python's own locale.windows_locale.
# Generated from: {x&0x3ff:y.split('_')[0] for x,y in locale.windows_locale.iteritems()}
windowsPrimaryLCIDsToLocaleNames={
	1:'ar',
	2:'bg',
	3:'ca',
	4:'zh',
	5:'cs',
	6:'da',
	7:'de',
	8:'el',
	9:'en',
	10:'es',
	11:'fi',
	12:'fr',
	13:'he',
	14:'hu',
	15:'is',
	16:'it',
	17:'ja',
	18:'ko',
	19:'nl',
	20:'nb',
	21:'pl',
	22:'pt',
	23:'rm',
	24:'ro',
	25:'ru',
	26:'sr',
	27:'sk',
	28:'sq',
	29:'sv',
	30:'th',
	31:'tr',
	32:'ur',
	33:'id',
	34:'uk',
	35:'be',
	36:'sl',
	37:'et',
	38:'lv',
	39:'lt',
	40:'tg',
	41:'fa',
	42:'vi',
	43:'hy',
	44:'az',
	45:'eu',
	46:'wen',
	47:'mk',
	50:'tn',
	52:'xh',
	53:'zu',
	54:'af',
	55:'ka',
	56:'fo',
	57:'hi',
	58:'mt',
	59:'sms',
	60:'ga',
	62:'ms',
	63:'kk',
	64:'ky',
	65:'sw',
	66:'tk',
	67:'uz',
	68:'tt',
	69:'bn',
	70:'pa',
	71:'gu',
	72:'or',
	73:'ta',
	74:'te',
	75:'kn',
	76:'ml',
	77:'as',
	78:'mr',
	79:'sa',
	80:'mn',
	81:'bo',
	82:'cy',
	83:'kh',
	84:'lo',
	86:'gl',
	87:'kok',
	90:'syr',
	91:'si',
	93:'iu',
	94:'am',
	95:'tmz',
	97:'ne',
	98:'fy',
	99:'ps',
	100:'fil',
	101:'div',
	104:'ha',
	106:'yo',
	107:'quz',
	108:'ns',
	109:'ba',
	110:'lb',
	111:'kl',
	120:'ii',
	122:'arn',
	124:'moh',
	126:'br',
	128:'ug',
	129:'mi',
	130:'oc',
	131:'co',
	132:'gsw',
	133:'sah',
	134:'qut',
	135:'rw',
	136:'wo',
	140: 'gbz',
	1170: 'ckb',
	1109: 'my',
	1143: 'so',
	9242: 'sr',
}
