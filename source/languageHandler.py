import config
import os
import gettext
import characterSymbols

def getAvailableLanguages():
	l=[x for x in os.listdir('locale') if not x.startswith('.')]
	l=[x for x in l if os.path.isfile('locale/%s/LC_MESSAGES/nvda.mo'%x)]
	if 'enu' not in l:
		l.append('enu')
	return l

def setLanguage(lang):
	try:
		gettext.translation("nvda", localedir="locale", languages=[lang]).install(True)
		config.conf["general"]["language"]=lang
		reload(characterSymbols)
		return True
	except IOError:
		gettext.install("nvda", unicode=True)
		reload(characterSymbols)
		return False
