"""Utilities and classes to manage logging in NVDA"""

import os
import sys
import warnings
import logging
from logging import _levelNames as levelNames
import inspect
import winsound
import nvwave
from types import MethodType
import globalVars

RPC_E_CALL_CANCELED = -2147418110

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
	modPathList = []
	# Work through the path components from right to left.
	curPath = path
	while curPath:
		curPath, curPathCom = os.path.split(curPath)
		if not curPathCom:
			break
		curPathCom = os.path.splitext(curPathCom)[0]
		# __init__ is the root module of a package, so skip it.
		if curPathCom != "__init__":
			modPathList.insert(0, curPathCom)
		if curPath in sys.path:
			# curPath is in the Python search path, so the Pythonic module path is relative to curPath.
			break
	modulePath = ".".join(modPathList)
	if modulePath:
		moduleCache[path] = modulePath
	return modulePath
 
def getCodePath(f):
	"""Using a frame object, gets its module path (relative to the current directory).[className.[funcName]]
	@param f: the frame object to use
	@type f: frame
	@returns: the dotted module.class.attribute path
	@rtype: string
	"""
	path=makeModulePathFromFilePath(os.path.relpath(f.f_code.co_filename))
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
	# Import standard levels for convenience.
	from logging import DEBUG, INFO, WARNING, WARN, ERROR, CRITICAL

	# Our custom levels.
	IO = 12
	DEBUGWARNING = 15

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

	def debugWarning(self, msg, *args, **kwargs):
		"""Log 'msg % args' with severity 'DEBUGWARNING'.
		"""
		if not self.isEnabledFor(self.DEBUGWARNING):
			return
		self._log(log.DEBUGWARNING, msg, args, **kwargs)

	def io(self, msg, *args, **kwargs):
		"""Log 'msg % args' with severity 'IO'.
		"""
		if not self.isEnabledFor(self.IO):
			return
		self._log(log.IO, msg, args, **kwargs)

	def exception(self, msg="", exc_info=True):
		"""Log an exception at an appropriate levle.
		Normally, it will be logged at level "ERROR".
		However, certain exceptions which aren't considered errors (or aren't errors that we can fix) are expected and will therefore be logged at a lower level.
		"""
		import comtypes
		if exc_info is True:
			exc_info = sys.exc_info()

		exc = exc_info[1]
		if isinstance(exc, comtypes.COMError) and exc.hresult == RPC_E_CALL_CANCELED:
			level = self.DEBUGWARNING
		else:
			level = self.ERROR

		self._log(level, msg, (), exc_info=exc_info)

class FileHandler(logging.FileHandler):

	def handle(self,record):
		if record.levelno>=logging.CRITICAL:
			winsound.PlaySound("SystemHand",winsound.SND_ALIAS)
		elif record.levelno>=logging.ERROR:
			try:
				nvwave.playWaveFile("waves\\error.wav")
			except:
				pass
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

#: The singleton logger instance.
#: @type: L{Logger}
log = Logger("nvda")

def _getDefaultLogFilePath():
	if getattr(sys, "frozen", None):
		import tempfile
		return os.path.join(tempfile.gettempdir(), "nvda.log")
	else:
		return ".\\nvda.log"

def _excepthook(*exc_info):
	log.error("", exc_info=exc_info, codepath="unhandled exception")

def _showwarning(message, category, filename, lineno, file=None, line=None):
	log.debugWarning(warnings.formatwarning(message, category, filename, lineno, line).rstrip(), codepath="Python warning")

def initialize():
	"""Initialize logging.
	This must be called before any logging can occur.
	@precondition: The command line arguments have been parsed into L{globalVars.appArgs}.
	"""
	global log
	logging.addLevelName(Logger.DEBUGWARNING, "DEBUGWARNING")
	logging.addLevelName(Logger.IO, "IO")
	if not globalVars.appArgs.logFileName:
		globalVars.appArgs.logFileName = _getDefaultLogFilePath()
	# HACK: Don't specify an encoding, as a bug in Python 2.6's logging module causes problems if we do.
	logHandler = FileHandler(globalVars.appArgs.logFileName, "w")
	logFormatter=logging.Formatter("%(levelname)s - %(codepath)s (%(asctime)s):\n%(message)s", "%H:%M:%S")
	logHandler.setFormatter(logFormatter)
	log.addHandler(logHandler)
	redirectStdout(log)
	sys.excepthook = _excepthook
	warnings.showwarning = _showwarning

def setLogLevelFromConfig():
	"""Set the log level based on the current configuration.
	"""
	if globalVars.appArgs.logLevel != 0:
		# Log level was overridden on the command line, so don't set it.
		return
	import config
	levelName=config.conf["general"]["loggingLevel"]
	level = levelNames.get(levelName)
	if not level or level > log.INFO:
		log.warning("invalid setting for logging level: %s" % levelName)
		level = log.INFO
		config.conf["general"]["loggingLevel"] = levelNames[log.INFO]
	log.setLevel(level)
