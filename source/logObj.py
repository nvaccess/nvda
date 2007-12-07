import os
import logging
import inspect
import winsound
from types import *

moduleCache={}

def getLogLevelNames():
	return ["debug","info","warning","error","critical"]

def nameToLevel(name):
	try:
		return getattr(logging,name.upper())
	except:
		return 0

def makeModulePathFromFilePath(path):
	if path in moduleCache:
		return moduleCache[path]
	curPath=path
	if os.path.isfile(curPath):
		curPath=os.path.splitext(curPath)[0]
	modList=[]
	while curPath:
		left,right=os.path.split(curPath)
		modList.append(os.path.splitext(right)[0])
		isPackage=False
		for ext in ('py','pyc','pyo','pyd'):
			if os.path.isfile(os.path.join(left,"__init__.%s")):
				isPackage=True
				break
		if isPackage:
			curPath=left
		else:
			curPath=None
	modulePath=".".join(modList)
	if modulePath:
		moduleCache[path]=modulePath
	return modulePath
 
#Using a frame object, gets current module path (relative to current directory).[className.[funcName]]
def getCodePath(f):
	path=makeModulePathFromFilePath(f.f_code.co_filename)
	funcName=f.f_code.co_name
	if funcName.startswith('<'):
		funcName=""
	className=""
	#Code borrowed from http://mail.python.org/pipermail/python-list/2000-January/020141.html
	if f.f_code.co_argcount:
		arg0=f.f_locals[f.f_code.co_varnames[0]]
		attr=getattr(arg0,funcName,None)
		if attr and type(attr) is MethodType and attr.im_func.func_code is f.f_code:
			className=arg0.__class__.__name__
	return ".".join([x for x in path,className,funcName if x])

class Logger(logging.Logger):

	def _log(self, level, msg, args, exc_info=None, extra=None):
		if not extra:
			extra={}
		f=inspect.currentframe().f_back.f_back
		extra["codepath"]=getCodePath(f)
		return logging.Logger._log(self,level, msg, args, exc_info, extra)

class FileHandler(logging.FileHandler):

	def handle(self,record):
		if record.levelno>=logging.ERROR:
			winsound.PlaySound("waves\\error.wav",winsound.SND_FILENAME|winsound.SND_PURGE|winsound.SND_ASYNC)
		return logging.FileHandler.handle(self,record)
