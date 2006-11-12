import os
import debug
from constants import *
from config import conf

def load():
	l=os.listdir('lang')
	l=filter(lambda x: os.path.splitext(x)[1]==".%s"%conf["language"]["language"],l)
	debug.writeMessage("lang.load: dirList %s"%l)
	for item in l:    
		f=open("lang\\%s"%item)
		try:
			globals()[os.path.splitext('%s'%item)[0]]=eval(f.read())
		except:
			debug.writeException("lang.load: exception loading %s data"%item)

load()
