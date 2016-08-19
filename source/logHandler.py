"""Utilities and classes to manage logging in NVDA"""

import os
import ctypes
import sys
import warnings
from encodings import utf_8
import logging
from logging import _levelNames as levelNames
import inspect
import winsound
import traceback
from types import MethodType, FunctionType
import globalVars

ERROR_INVALID_WINDOW_HANDLE = 1400
ERROR_TIMEOUT = 1460
RPC_S_SERVER_UNAVAILABLE = 1722
RPC_S_CALL_FAILED_DNE = 1727
EPT_S_NOT_REGISTERED = 1753
E_ACCESSDENIED = -2147024891
CO_E_OBJNOTCONNECTED = -2147220995
EVENT_E_ALL_SUBSCRIBERS_FAILED = -2147220991
RPC_E_CALL_REJECTED = -2147418111
RPC_E_DISCONNECTED = -2147417848

def getCodePath(f):
	"""Using a frame object, gets its module path (relative to the current directory).[className.[funcName]]
	@param f: the frame object to use
	@type f: frame
	@returns: the dotted module.class.attribute path
	@rtype: string
	"""
	fn=f.f_code.co_filename
	if fn[0] != "<" and os.path.isabs(fn) and not fn.startswith(sys.path[0] + "\\"):
		# This module is external because:
		# the code comes from a file (fn doesn't begin with "<");
		# it has an absolute file path (code bundled in binary builds reports relative paths); and
		# it is not part of NVDA's Python code (not beneath sys.path[0]).
		path="external:"
	else:
		path=""
	try:
		path+=f.f_globals["__name__"]
	except KeyError:
		path+=fn
	funcName=f.f_code.co_name
	if funcName.startswith('<'):
		funcName=""
	className=""
	#Code borrowed from http://mail.python.org/pipermail/python-list/2000-January/020141.html
	if f.f_code.co_argcount:
		arg0=f.f_locals[f.f_code.co_varnames[0]]
		# #6122: Check if this function is a member of its first argument's class (and specifically which base class if any) 
		# Rather than an instance member of its first argument.
		# This stops infinite recursions if fetching data descriptors,
		# And better reflects the actual source code definition.
		topCls=arg0 if isinstance(arg0,type) else type(arg0)
		# find the deepest class this function's name is reachable as a method from
		if hasattr(topCls,funcName):
			for cls in topCls.__mro__:
				member=cls.__dict__.get(funcName)
				if not member:
					continue
				memberType=type(member)
				if memberType is FunctionType and member.func_code is f.f_code:
					# the function was found as a standard method
					className=cls.__name__
				elif memberType is classmethod and type(member.__func__) is FunctionType and member.__func__.func_code is f.f_code:
					# function was found as a class method
					className=cls.__name__
				elif memberType is property:
					if type(member.fget) is FunctionType and member.fget.func_code is f.f_code:
						# The function was found as a property getter
						className=cls.__name__
					elif type(member.fset) is FunctionType and member.fset.func_code is f.f_code:
						# the function was found as a property setter
						className=cls.__name__
				if className:
					break
	return ".".join([x for x in path,className,funcName if x])

# Function to strip the base path of our code from traceback text to improve readability.
if getattr(sys, "frozen", None):
	# We're running a py2exe build.
	# The base path already seems to be stripped in this case, so do nothing.
	def stripBasePathFromTracebackText(text):
		return text
else:
	BASE_PATH = os.path.split(__file__)[0] + os.sep
	TB_BASE_PATH_PREFIX = '  File "'
	TB_BASE_PATH_MATCH = TB_BASE_PATH_PREFIX + BASE_PATH
	def stripBasePathFromTracebackText(text):
		return text.replace(TB_BASE_PATH_MATCH, TB_BASE_PATH_PREFIX)

class Logger(logging.Logger):
	# Import standard levels for convenience.
	from logging import DEBUG, INFO, WARNING, WARN, ERROR, CRITICAL

	# Our custom levels.
	IO = 12
	DEBUGWARNING = 15

	def _log(self, level, msg, args, exc_info=None, extra=None, codepath=None, activateLogViewer=False, stack_info=None):
		if not extra:
			extra={}

		if not codepath or stack_info is True:
			f=inspect.currentframe().f_back.f_back

		if not codepath:
			codepath=getCodePath(f)
		extra["codepath"] = codepath

		if not globalVars.appArgs or globalVars.appArgs.secure:
			# The log might expose sensitive information and the Save As dialog in the Log Viewer is a security risk.
			activateLogViewer = False

		if activateLogViewer:
			# Import logViewer here, as we don't want to import GUI code when this module is imported.
			from gui import logViewer
			logViewer.activate()
			# Move to the end of the current log text. The new text will be written at this position.
			# This means that the user will be positioned at the start of the new log text.
			# This is why we activate the log viewer before writing to the log.
			logViewer.logViewer.outputCtrl.SetInsertionPointEnd()

		if stack_info:
			if stack_info is True:
				stack_info = traceback.extract_stack(f)
			msg += ("\nStack trace:\n"
				+ stripBasePathFromTracebackText("".join(traceback.format_list(stack_info)).rstrip()))

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

	def exception(self, msg="", exc_info=True, **kwargs):
		"""Log an exception at an appropriate levle.
		Normally, it will be logged at level "ERROR".
		However, certain exceptions which aren't considered errors (or aren't errors that we can fix) are expected and will therefore be logged at a lower level.
		"""
		import comtypes
		import watchdog
		from watchdog import RPC_E_CALL_CANCELED
		if exc_info is True:
			exc_info = sys.exc_info()

		exc = exc_info[1]
		if (
			(isinstance(exc, WindowsError) and exc.winerror in (ERROR_INVALID_WINDOW_HANDLE, ERROR_TIMEOUT, RPC_S_SERVER_UNAVAILABLE, RPC_S_CALL_FAILED_DNE, EPT_S_NOT_REGISTERED, RPC_E_CALL_CANCELED))
			or (isinstance(exc, comtypes.COMError) and (exc.hresult in (E_ACCESSDENIED, CO_E_OBJNOTCONNECTED, EVENT_E_ALL_SUBSCRIBERS_FAILED, RPC_E_CALL_REJECTED, RPC_E_CALL_CANCELED, RPC_E_DISCONNECTED) or exc.hresult & 0xFFFF == RPC_S_SERVER_UNAVAILABLE))
			or isinstance(exc, watchdog.CallCancelled)
		):
			level = self.DEBUGWARNING
		else:
			level = self.ERROR

		if not self.isEnabledFor(level):
			return
		self._log(level, msg, (), exc_info=exc_info, **kwargs)

class RemoteHandler(logging.Handler):

	def __init__(self):
		#Load nvdaHelperRemote.dll but with an altered search path so it can pick up other dlls in lib
		h=ctypes.windll.kernel32.LoadLibraryExW(os.path.abspath(ur"lib\nvdaHelperRemote.dll"),0,0x8)
		self._remoteLib=ctypes.WinDLL("nvdaHelperRemote",handle=h) if h else None
		logging.Handler.__init__(self)

	def emit(self, record):
		msg = self.format(record)
		if self._remoteLib:
			try:
				self._remoteLib.nvdaControllerInternal_logMessage(record.levelno, ctypes.windll.kernel32.GetCurrentProcessId(), msg)
			except WindowsError:
				pass

class FileHandler(logging.StreamHandler):

	def __init__(self, filename, mode):
		# We need to open the file in text mode to get CRLF line endings.
		# Therefore, we can't use codecs.open(), as it insists on binary mode. See PythonIssue:691291.
		# We know that \r and \n are safe in UTF-8, so PythonIssue:691291 doesn't matter here.
		logging.StreamHandler.__init__(self, utf_8.StreamWriter(file(filename, mode)))

	def close(self):
		self.flush()
		self.stream.close()
		logging.StreamHandler.close(self)

	def handle(self,record):
		# versionInfo must be imported after the language is set. Otherwise, strings won't be in the correct language.
		# Therefore, don't import versionInfo if it hasn't already been imported.
		versionInfo = sys.modules.get("versionInfo")
		# Only play the error sound if this is a test version.
		shouldPlayErrorSound = versionInfo and versionInfo.isTestVersion
		if record.levelno>=logging.CRITICAL:
			try:
				winsound.PlaySound("SystemHand",winsound.SND_ALIAS)
			except:
				pass
		elif record.levelno>=logging.ERROR and shouldPlayErrorSound:
			import nvwave
			try:
				nvwave.playWaveFile("waves\\error.wav")
			except:
				pass
		return logging.StreamHandler.handle(self,record)

class Formatter(logging.Formatter):

	def format(self, record):
		s = logging.Formatter.format(self, record)
		if isinstance(s, str):
			# Log text must be unicode.
			# The string is probably encoded according to our thread locale, so use mbcs.
			# If there are any errors, just replace the character, as there's nothing else we can do.
			s = unicode(s, "mbcs", "replace")
		return s

	def formatException(self, ex):
		return stripBasePathFromTracebackText(super(Formatter, self).formatException(ex))

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
	log.exception(exc_info=exc_info, codepath="unhandled exception")

def _showwarning(message, category, filename, lineno, file=None, line=None):
	log.debugWarning(warnings.formatwarning(message, category, filename, lineno, line).rstrip(), codepath="Python warning")

def initialize(shouldDoRemoteLogging=False):
	"""Initialize logging.
	This must be called before any logging can occur.
	@precondition: The command line arguments have been parsed into L{globalVars.appArgs}.
	@var shouldDoRemoteLogging: True if all logging should go to the real NVDA via rpc (for slave)
	@type shouldDoRemoteLogging: bool
	"""
	global log
	logging.addLevelName(Logger.DEBUGWARNING, "DEBUGWARNING")
	logging.addLevelName(Logger.IO, "IO")
	if not shouldDoRemoteLogging:
		logFormatter=Formatter("%(levelname)s - %(codepath)s (%(asctime)s):\n%(message)s", "%H:%M:%S")
		if globalVars.appArgs.secure:
			# Don't log in secure mode.
			logHandler = logging.NullHandler()
			# There's no point in logging anything at all, since it'll go nowhere.
			log.setLevel(100)
		else:
			if not globalVars.appArgs.logFileName:
				globalVars.appArgs.logFileName = _getDefaultLogFilePath()
			# Keep a backup of the previous log file so we can access it even if NVDA crashes or restarts.
			oldLogFileName = os.path.join(os.path.dirname(globalVars.appArgs.logFileName), "nvda-old.log")
			try:
				# We must remove the old log file first as os.rename does replace it.
				if os.path.exists(oldLogFileName):
					os.unlink(oldLogFileName)
				os.rename(globalVars.appArgs.logFileName, oldLogFileName)
			except (IOError, WindowsError):
				pass # Probably log does not exist, don't care.
			# Our FileHandler always outputs in UTF-8.
			logHandler = FileHandler(globalVars.appArgs.logFileName, mode="wt")
	else:
		logHandler = RemoteHandler()
		logFormatter = Formatter("%(codepath)s:\n%(message)s")
	logHandler.setFormatter(logFormatter)
	log.addHandler(logHandler)
	redirectStdout(log)
	sys.excepthook = _excepthook
	warnings.showwarning = _showwarning
	warnings.simplefilter("default", DeprecationWarning)

def setLogLevelFromConfig():
	"""Set the log level based on the current configuration.
	"""
	if globalVars.appArgs.logLevel != 0 or globalVars.appArgs.secure:
		# Log level was overridden on the command line or we're running in secure mode,
		# so don't set it.
		return
	import config
	levelName=config.conf["general"]["loggingLevel"]
	level = levelNames.get(levelName)
	if not level or level > log.INFO:
		log.warning("invalid setting for logging level: %s" % levelName)
		level = log.INFO
		config.conf["general"]["loggingLevel"] = levelNames[log.INFO]
	log.setLevel(level)
