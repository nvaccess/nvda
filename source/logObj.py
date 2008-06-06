"""Utilities and classes to manage logging in NVDA"""

import os
import sys
import logging
import inspect
import winsound
from types import MethodType

moduleCache={}

def makeModulePathFromFilePath(path):
	"""calculates the pythonic dotted module path from a file path of a python module.
@param path: the relative or absolute path to the module
@type path: string
@returns: the Pythonic dotted module path 
@rtype: string
"""
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
	"""Using a frame object, gets its module path (relative to the current directory).[className.[funcName]]
@param f: the frame object to use
@type f: frame
@returns: the dotted module.class.attribute path
@rtype: string
"""
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

	def _log(self, level, msg, args, exc_info=None, extra=None, codepath=None, activateLogViewer=False):
		if not extra:
			extra={}
		if not codepath:
			f=inspect.currentframe().f_back.f_back
			codepath=getCodePath(f)
		extra["codepath"] = codepath
		if activateLogViewer:
			# Import logViewer here, as we don't want to import GUI code when this module is imported.
			from gui import logViewer
			logViewer.activate()
			# Move to the end of the current log text. The new text will be written at this position.
			# This means that the user will be positioned at the start of the new log text.
			# This is why we activate the log viewer before writing to the log.
			logViewer.logViewer.outputCtrl.SetInsertionPointEnd()
		res = logging.Logger._log(self,level, msg, args, exc_info, extra)
		if activateLogViewer:
			# Make the log text we just wrote appear in the log viewer.
			logViewer.logViewer.refresh()
		return res

class FileHandler(logging.FileHandler):

	def handle(self,record):
		if record.levelno>=logging.ERROR:
			winsound.PlaySound("waves\\error.wav",winsound.SND_FILENAME|winsound.SND_PURGE|winsound.SND_ASYNC)
		return logging.FileHandler.handle(self,record)

class StreamRedirector(object):
	"""Redirects an output stream to a logger.
	"""

	def __init__(self, name, logger, level):
		"""Constructor.
		@param name: The name of the stream to be used in the log output.
		@param logger: The logger to which to log.
		@type logger: L{Logger}
		@param level: The level at which to log.
		@type level: int
		"""
		self.name = name
		self.logger = logger
		self.level = level

	def write(self, text):
		text = text.rstrip()
		if not text:
			return
		self.logger.log(self.level, text, codepath=self.name)

	def flush(self):
		pass

def redirectStdout(logger):
	"""Redirect stdout and stderr to a given logger.
	@param logger: The logger to which to redirect.
	@type logger: L{Logger}
	"""
	sys.stdout = StreamRedirector("stdout", logger, logging.WARNING)
	sys.stderr = StreamRedirector("stderr", logger, logging.ERROR)
