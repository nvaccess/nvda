import config
import os
import ctypes
import locale
import gettext
import globalVars

#a few Windows locale constants
LOCALE_SLANGUAGE=0x2
LOCALE_SLANGDISPLAYNAME=0x6f

curLang="en"

def getAvailableLanguages():
	"""generates a list of locale names, plus their full localized language and country names.
	@rtype: list of tuples
	"""
	#Make a list of all the locales found in NVDA's locale dir
	l=[x for x in os.listdir('locale') if not x.startswith('.')]
	l=[x for x in l if os.path.isfile('locale/%s/LC_MESSAGES/nvda.mo'%x)]
	#Make sure that en (english) is in the list as it may not have any locale files, but is default
	if 'en' not in l:
		l.append('en')
		l.sort()
	#For each locale, ask Windows for its human readable display name
	d=[]
	for i in l:
		#Windows only excepts full locales (with country included) and uses a dash not underscore
		t=locale.normalize(i)
		if '.' in t:
			t=t.split('.')[0]
		t=t.replace('_','-')
		LCID=ctypes.windll.kernel32.LocaleNameToLCID(unicode(t),0)
		buf=ctypes.create_unicode_buffer(1024)
		#If the original locale didn't have country info (was just language) then make sure we just get language from Windows
		if '_' not in i:
			res=ctypes.windll.kernel32.GetLocaleInfoW(LCID,LOCALE_SLANGDISPLAYNAME,buf,1024)
		else:
			res=0
		if res==0:
			res=ctypes.windll.kernel32.GetLocaleInfoW(LCID,LOCALE_SLANGUAGE,buf,1024)
		sLanguage=buf.value
		label="%s, %s"%(sLanguage,i)
		d.append(label)
	#include a 'user default, windows' language, which just represents the default language for this user account
	l.append("Windows")
	d.append("User default, windows")
	#return a zipped up version of both the lists (a list with tuples of locale,label)
	return zip(l,d)

def setLanguage(lang):
	global curLang
	try:
		if lang=="Windows":
			windowsLCID=ctypes.windll.kernel32.GetUserDefaultLCID()
			localeName=locale.windows_locale[windowsLCID]
			gettext.translation('nvda',localedir='locale',languages=[localeName]).install(True)
			curLang=localeName
		else:
			gettext.translation("nvda", localedir="locale", languages=[lang]).install(True)
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
			#To convert to windows locale, the language must be language_country, not just language
			tempLang=locale.normalize(lang)
			if '.' in tempLang:
				#There was charset info given, wrip that out
				tempLang=tempLang.split('.')[0]
			#Find the windows LC ID for this locale
			LCList=[x[0] for x in locale.windows_locale.iteritems() if x[1]==tempLang]
			if len(LCList)>0:
				ctypes.windll.kernel32.SetThreadLocale(LCList[0])
		config.conf["general"]["language"]=lang
		return True
	except IOError:
		gettext.install("nvda", unicode=True)
		curLang="en"
		return False

def getLanguage():
	return curLang
