import config
import os
import ctypes
import locale
import gettext
import characterSymbols
import debug

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
		config.conf["general"]["language"]=lang
		reload(characterSymbols)
		return True
	except IOError:
		gettext.install("nvda", unicode=True)
		curLang="en"
		reload(characterSymbols)
		return False

def getLanguage():
	return curLang
