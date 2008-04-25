import config
import os
import ctypes
import locale
import gettext
import globalVars

curLang="en"

def getAvailableLanguages():
	l=[x for x in os.listdir('locale') if not x.startswith('.')]
	l=[x for x in l if os.path.isfile('locale/%s/LC_MESSAGES/nvda.mo'%x)]
	if 'en' not in l:
		l.append('en')
	l.append("Windows")
	return l

def setLanguage(lang):
	global curLang
	try:
		if lang=="Windows":
			windowsLCID=ctypes.windll.kernel32.GetThreadLocale()
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
