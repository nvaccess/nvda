import os
import debug
from constants import *
from config import conf

def load():
	dirList=filter(lambda x: os.path.splitext('.\\lang')[1]==conf["language"]["language"],os.listdir('.\\lang'))
	for item in dirList:    
		f=open(".\\lang\\%s"%item)
		try:
			globals()[os.path.splitext('.\\lang\\%s'%item)[0]]=eval(f.read())
		except:
			debug.writeException("lang.load: exception loading %s data"%item)

load()
