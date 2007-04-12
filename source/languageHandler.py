import config
import os
import locale
import gettext
import characterSymbols

def getAvailableLanguages():
	l=[x for x in os.listdir('locale') if not x.startswith('.')]
	l=[x for x in l if os.path.isfile('locale/%s/LC_MESSAGES/nvda.mo'%x)]
	if 'en' not in l:
		l.append('en')
	l.append("Windows")
	return l

def setLanguage(lang):
	try:
		if lang=="Windows":
			gettext.translation('nvda',localedir='locale',languages=[locale.getlocale()[0]]).install(True)
		else:
			gettext.translation("nvda", localedir="locale", languages=[lang]).install(True)
		config.conf["general"]["language"]=lang
		reload(characterSymbols)
		return True
	except IOError:
		gettext.install("nvda", unicode=True)
		reload(characterSymbols)
		return False

