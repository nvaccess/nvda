import os
import debug
from constants import *
from config import conf

def load(language,merge=True):
	l=os.listdir('lang')
	l=filter(lambda x: os.path.splitext(x)[1]==".%s"%language,l)
	debug.writeMessage("lang.load: dirList %s"%l)
	for item in l:    
		f=open("lang\\%s"%item)
		try:
			langDict=eval(f.read())
			entryName=os.path.splitext(item)[0]
			if merge:
				globals()[entryName]=globals().get(entryName,{})
				globals()[entryName].update(langDict)
			else:
				globals()[entryName]=langDict
		except:
			debug.writeException("lang.load: exception loading %s data"%item)

load("enu")
userLang=conf["language"]["language"]
if userLang!="enu":
	load(userLang)

