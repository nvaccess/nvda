#languageHandler.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2007-2018 NV access Limited, Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Language and localization support.
This module assists in NVDA going global through language services such as converting Windows locale ID's to friendly names and presenting available languages.
"""

import builtins
import os
import sys
import ctypes
import locale
import gettext

#a few Windows locale constants
LOCALE_SLANGUAGE=0x2
LOCALE_SLANGDISPLAYNAME=0x6f
LOCALE_CUSTOM_UNSPECIFIED = 0x1000
#: Returned from L{localeNameToWindowsLCID} when the locale name cannot be mapped to a locale identifier.
#: This might be because Windows doesn't know about the locale (e.g. "an"),
#: because it is not a standardized locale name anywhere (e.g. "zz")
#: or because it is not a legal locale name (e.g. "zzzz").
LCID_NONE = 0 # 0 used instead of None for backwards compatibility.

curLang="en"

def localeNameToWindowsLCID(localeName):
	"""Retreave the Windows locale identifier (LCID) for the given locale name
	@param localeName: a string of 2letterLanguage_2letterCountry or just language (2letterLanguage or 3letterLanguage)
	@type localeName: string
	@returns: a Windows LCID or L{LCID_NONE} if it could not be retrieved.
	@rtype: integer
	""" 
	# Windows Vista (NT 6.0) and later is able to convert locale names to LCIDs.
	# Because NVDA supports Windows 7 (NT 6.1) SP1 and later, just use it directly.
	localeName=localeName.replace('_','-')
	LCID=ctypes.windll.kernel32.LocaleNameToLCID(localeName,0)
	# #6259: In Windows 10, LOCALE_CUSTOM_UNSPECIFIED is returned for any locale name unknown to Windows.
	# This was observed for Aragonese ("an").
	# See https://msdn.microsoft.com/en-us/library/system.globalization.cultureinfo.lcid(v=vs.110).aspx.
	if LCID==LOCALE_CUSTOM_UNSPECIFIED:
		LCID=LCID_NONE
	return LCID

def windowsLCIDToLocaleName(lcid):
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
		desc={
			# Translators: The name of a language supported by NVDA.
			"an":pgettext("languageName","Aragonese"),
			# Translators: The name of a language supported by NVDA.
			"ckb":pgettext("languageName","Central Kurdish"),
			# Translators: The name of a language supported by NVDA.
			"kmr":pgettext("languageName","Northern Kurdish"),
			# Translators: The name of a language supported by NVDA.
			"my":pgettext("languageName","Burmese"),
			# Translators: The name of a language supported by NVDA.
			"so":pgettext("languageName","Somali"),
		}.get(language,None)
	return desc

def getAvailableLanguages(presentational=False):
	"""generates a list of locale names, plus their full localized language and country names.
	@param presentational: whether this is meant to be shown alphabetically by language description
	@type presentational: bool
	@rtype: list of tuples
	"""
	#Make a list of all the locales found in NVDA's locale dir
	locales = [x for x in os.listdir('locale') if not x.startswith('.')]
	locales = [x for x in locales if os.path.isfile('locale/%s/LC_MESSAGES/nvda.mo'%x)]
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
		raise ValueError("%s is Not a GNUTranslations or NullTranslations object"%translations)
	return pgettext

def getWindowsLanguage():
	"""
	Fetches the locale name of the user's configured language in Windows.
	"""
	windowsLCID=ctypes.windll.kernel32.GetUserDefaultUILanguage()
	try:
		localeName=locale.windows_locale[windowsLCID]
	except KeyError:
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

def setLanguage(lang):
	global curLang
	try:
		if lang=="Windows":
			localeName=getWindowsLanguage()
			trans=gettext.translation('nvda',localedir='locale',languages=[localeName])
			curLang=localeName
		else:
			trans=gettext.translation("nvda", localedir="locale", languages=[lang])
			curLang=lang
			localeChanged=False
			#Try setting Python's locale to lang
			try:
				locale.setlocale(locale.LC_ALL,lang)
				localeChanged=True
			except:
				pass
			if not localeChanged and '_' in lang:
				#Python couldn'tsupport the language_country locale, just try language.
				try:
					locale.setlocale(locale.LC_ALL,lang.split('_')[0])
				except:
					pass
			#Set the windows locale for this thread (NVDA core) to this locale.
			LCID=localeNameToWindowsLCID(lang)
			ctypes.windll.kernel32.SetThreadLocale(LCID)
	except IOError:
		trans=gettext.translation("nvda",fallback=True)
		curLang="en"
	trans.install()
	# Install our pgettext function.
	import builtins
	builtins.pgettext = makePgettext(trans)

def getLanguage():
	return curLang

def normalizeLanguage(lang):
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
	140:'gbz'
}
