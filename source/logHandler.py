# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2007-2020 NV Access Limited, Rui Batista, Joseph Lee, Leonard de Ruijter, Babbage B.V.,
# Accessolutions, Julien Cochuyt
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""Utilities and classes to manage logging in NVDA"""

import os
import ctypes
import sys
import warnings
import logging
import inspect
import winsound
import traceback
from types import FunctionType
import globalVars
import winKernel
import buildVersion
from typing import Optional
import exceptions
import RPCConstants

ERROR_INVALID_WINDOW_HANDLE = 1400
ERROR_TIMEOUT = 1460
EPT_S_NOT_REGISTERED = 1753
E_ACCESSDENIED = -2147024891
CO_E_OBJNOTCONNECTED = -2147220995
EVENT_E_ALL_SUBSCRIBERS_FAILED = -2147220991
LOAD_WITH_ALTERED_SEARCH_PATH=0x8

def isPathExternalToNVDA(path):
	""" Checks if the given path is external to NVDA (I.e. not pointing to built-in code). """
	if path[0] != "<" and os.path.isabs(path) and not path.startswith(sys.path[0] + "\\"):
		# This module is external because:
		# the code comes from a file (fn doesn't begin with "<");
		# it has an absolute file path (code bundled in binary builds reports relative paths); and
		# it is not part of NVDA's Python code (not beneath sys.path[0]).
		return True
	return False

def getCodePath(f):
	"""Using a frame object, gets its module path (relative to the current directory).[className.[funcName]]
	@param f: the frame object to use
	@type f: frame
	@returns: the dotted module.class.attribute path
	@rtype: string
	"""
	fn=f.f_code.co_filename
	if isPathExternalToNVDA(fn):
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
		f_locals = f.f_locals
		arg0 = f_locals[f.f_code.co_varnames[0]]
		if f.f_code.co_flags & inspect.CO_NEWLOCALS:
			# Fetching of Frame.f_locals causes a function frames's locals to be cached on the frame for ever.
			# If an Exception is currently stored as a local variable on that frame,
			# A reference cycle will be created, holding the frame and all its variables.
			# Therefore clear f_locals manually.
			f_locals.clear()
		del f_locals
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
				if memberType is FunctionType and member.__code__ is f.f_code:
					# the function was found as a standard method
					className=cls.__name__
				elif memberType is classmethod and type(member.__func__) is FunctionType and member.__func__.__code__ is f.f_code:
					# function was found as a class method
					className=cls.__name__
				elif memberType is property:
					if type(member.fget) is FunctionType and member.fget.__code__ is f.f_code:
						# The function was found as a property getter
						className=cls.__name__
					elif type(member.fset) is FunctionType and member.fset.__code__ is f.f_code:
						# the function was found as a property setter
						className=cls.__name__
				if className:
					break
	return ".".join(x for x in (path,className,funcName) if x)


def shouldPlayErrorSound() -> bool:
	"""Indicates if an error sound should be played when an error is logged.
	"""
	import nvwave
	if nvwave.isInError():
		if nvwave._isDebugForNvWave():
			log.debug("No beep for log; nvwave is in error state")
		return False

	import config
	# Only play the error sound if this is a test version or if the config states it explicitly.
	return (
		buildVersion.isTestVersion
		# Play error sound: 1 = Yes
		or (config.conf is not None and config.conf["featureFlag"]["playErrorSound"] == 1)
	)


# Function to strip the base path of our code from traceback text to improve readability.
if getattr(sys, "frozen", None):
	# We're running a py2exe build.
	stripBasePathFromTracebackText = lambda text: text
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
	OFF = 100

	#: The start position of a fragment of the log file as marked with
	#: L{markFragmentStart} for later retrieval using L{getFragment}.
	#: @type: C{long}
	fragmentStart = None

	def _log(self, level, msg, args, exc_info=None, extra=None, codepath=None, activateLogViewer=False, stack_info=None):
		if not extra:
			extra={}

		if not codepath or stack_info is True:
			f=inspect.currentframe().f_back.f_back

		if not codepath:
			codepath=getCodePath(f)
		extra["codepath"] = codepath

		if globalVars.appArgs.secure:
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

		res = super()._log(level, msg, args, exc_info, extra)

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
		"""Log an exception at an appropriate level.
		Normally, it will be logged at level "ERROR".
		However, certain exceptions which aren't considered errors (or aren't errors that we can fix) are expected and will therefore be logged at a lower level.
		"""
		import comtypes
		if exc_info is True:
			exc_info = sys.exc_info()

		exc = exc_info[1]
		if (
			(
				isinstance(exc, WindowsError)
				and exc.winerror in (
					ERROR_INVALID_WINDOW_HANDLE,
					ERROR_TIMEOUT,
					RPCConstants.RPC.S_SERVER_UNAVAILABLE,
					RPCConstants.RPC.S_CALL_FAILED_DNE,
					EPT_S_NOT_REGISTERED,
					RPCConstants.RPC.E_CALL_CANCELED
				)
			)
			or (
				isinstance(exc, comtypes.COMError)
				and (
					exc.hresult in (
						E_ACCESSDENIED,
						CO_E_OBJNOTCONNECTED,
						EVENT_E_ALL_SUBSCRIBERS_FAILED,
						RPCConstants.RPC.E_CALL_REJECTED,
						RPCConstants.RPC.E_CALL_CANCELED,
						RPCConstants.RPC.E_DISCONNECTED
					) or exc.hresult & 0xFFFF == RPCConstants.RPC.S_SERVER_UNAVAILABLE))
			or isinstance(exc, exceptions.CallCancelled)
		):
			level = self.DEBUGWARNING
		else:
			level = self.ERROR

		if not self.isEnabledFor(level):
			return
		self._log(level, msg, (), exc_info=exc_info, **kwargs)

	def markFragmentStart(self):
		"""Mark the current end of the log file as the start position of a
		fragment to be later retrieved by L{getFragment}.
		@returns: Whether a log file is in use and a position could be marked
		@rtype: bool
		"""
		if (
			globalVars.appArgs.secure
			or not globalVars.appArgs.logFileName
			or not isinstance(logHandler, FileHandler)
		):
			return False
		with open(globalVars.appArgs.logFileName, "r", encoding="UTF-8") as f:
			# _io.TextIOWrapper.seek: whence=2 -- end of stream
			f.seek(0, 2)
			self.fragmentStart = f.tell()
			return True

	def getFragment(self):
		"""Retrieve a fragment of the log starting from the position marked using
		L{markFragmentStart}.
		If L{fragmentStart} does not point to the current end of the log file, it
		is reset to C{None} after reading the fragment.
		@returns: The text of the fragment, or C{None} if L{fragmentStart} is None.
		@rtype: str
		"""
		if (
			self.fragmentStart is None
			or globalVars.appArgs.secure
			or not globalVars.appArgs.logFileName
			or not isinstance(logHandler, FileHandler)
		):
			return None
		with open(globalVars.appArgs.logFileName, "r", encoding="UTF-8") as f:
			f.seek(self.fragmentStart)
			fragment = f.read()
			if fragment:
				self.fragmentStart = None
			return fragment

class RemoteHandler(logging.Handler):

	def __init__(self):
		#Load nvdaHelperRemote.dll but with an altered search path so it can pick up other dlls in lib
		path = os.path.join(globalVars.appDir, "lib", buildVersion.version, "nvdaHelperRemote.dll")
		h=ctypes.windll.kernel32.LoadLibraryExW(path,0,LOAD_WITH_ALTERED_SEARCH_PATH)
		if not h:
			raise OSError("Could not load %s"%path) 
		self._remoteLib=ctypes.WinDLL("nvdaHelperRemote",handle=h)
		logging.Handler.__init__(self)

	def emit(self, record):
		msg = self.format(record)
		try:
			self._remoteLib.nvdaControllerInternal_logMessage(record.levelno, ctypes.windll.kernel32.GetCurrentProcessId(), msg)
		except WindowsError:
			pass

class FileHandler(logging.FileHandler):

	def handle(self,record):
		if record.levelno>=logging.CRITICAL:
			try:
				winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)
			except:
				pass
		elif record.levelno >= logging.ERROR and shouldPlayErrorSound():
			import nvwave
			try:
				nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "error.wav"))
			except:
				pass
		return super().handle(record)

class Formatter(logging.Formatter):
	default_time_format = "%H:%M:%S"
	default_msec_format = "%s.%03d"

	def formatException(self, ex):
		return stripBasePathFromTracebackText(super(Formatter, self).formatException(ex))

	def formatTime(self, record: logging.LogRecord, datefmt: Optional[str] = None) -> str:
		"""Custom implementation of `formatTime` which avoids `time.localtime`
		since it causes a crash under some versions of Universal CRT when Python locale
		is set to a Unicode one (#12160, Python issue 36792)
		"""
		timeAsFileTime = winKernel.time_tToFileTime(record.created)
		timeAsSystemTime = winKernel.SYSTEMTIME()
		winKernel.FileTimeToSystemTime(timeAsFileTime, timeAsSystemTime)
		timeAsLocalTime = winKernel.SYSTEMTIME()
		winKernel.SystemTimeToTzSpecificLocalTime(None, timeAsSystemTime, timeAsLocalTime)
		res = f"{timeAsLocalTime.wHour:02d}:{timeAsLocalTime.wMinute:02d}:{timeAsLocalTime.wSecond:02d}"
		return self.default_msec_format % (res, record.msecs)


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

# Register our logging class as the class for all loggers.
logging.setLoggerClass(Logger)
#: The singleton logger instance.
log: Logger = logging.getLogger("nvda")
#: The singleton log handler instance.
logHandler: Optional[logging.Handler] = None

def _getDefaultLogFilePath():
	if getattr(sys, "frozen", None):
		import tempfile
		return os.path.join(tempfile.gettempdir(), "nvda.log")
	else:
		return os.path.join(globalVars.appDir, "nvda.log")

def _excepthook(*exc_info):
	log.exception(exc_info=exc_info, codepath="unhandled exception")

def _showwarning(message, category, filename, lineno, file=None, line=None):
	log.debugWarning(warnings.formatwarning(message, category, filename, lineno, line).rstrip(), codepath="Python warning")


def _shouldDisableLogging() -> bool:
	"""Disables logging based on command line options and if secure mode is active.
	See NoConsoleOptionParser in nvda.pyw, #TODO and #8516.

	Secure mode disables logging.
	Logging on secure screens could allow keylogging of passwords and retrieval from the SYSTEM user.

	* `--secure` overrides any logging preferences by disabling logging.
	* `--debug-logging` or `--log-level=X` overrides the user config log level setting.
	* `--debug-logging` and `--log-level=X` override `--no-logging`.
	"""
	logLevelOverridden = globalVars.appArgs.debugLogging or not globalVars.appArgs.logLevel == 0
	noLoggingRequested = globalVars.appArgs.noLogging and not logLevelOverridden
	return globalVars.appArgs.secure or noLoggingRequested


def initialize(shouldDoRemoteLogging=False):
	"""Initialize logging.
	This must be called before any logging can occur.
	@precondition: The command line arguments have been parsed into L{globalVars.appArgs}.
	@var shouldDoRemoteLogging: True if all logging should go to the real NVDA via rpc (for slave)
	@type shouldDoRemoteLogging: bool
	"""
	global log, logHandler
	logging.addLevelName(Logger.DEBUGWARNING, "DEBUGWARNING")
	logging.addLevelName(Logger.IO, "IO")
	logging.addLevelName(Logger.OFF, "OFF")
	if not shouldDoRemoteLogging:
		# This produces log entries such as the following:
		# IO - inputCore.InputManager.executeGesture (09:17:40.724) - Thread-5 (13576):
		# Input: kb(desktop):v
		logFormatter = Formatter(
			fmt="{levelname!s} - {codepath!s} ({asctime}) - {threadName} ({thread}):\n{message}",
			style="{"
		)
		if _shouldDisableLogging():
			logHandler = logging.NullHandler()
			# There's no point in logging anything at all, since it'll go nowhere.
			log.root.setLevel(Logger.OFF)
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
			try:
				logHandler = FileHandler(globalVars.appArgs.logFileName, mode="w", encoding="utf-8")
			except IOError:
				# if log cannot be opened, we use NullHandler to avoid logging preserving logger behaviour
				# and set log filename to None to inform logViewer about it
				globalVars.appArgs.logFileName = None
				logHandler = logging.NullHandler()
				log.error("Faile to open log file, redirecting to standard output")
			logLevel = globalVars.appArgs.logLevel
			if globalVars.appArgs.debugLogging:
				logLevel = Logger.DEBUG
			elif logLevel <= 0:
				logLevel = Logger.INFO
			log.setLevel(logLevel)
			log.root.setLevel(max(logLevel, logging.WARN))
	else:
		logHandler = RemoteHandler()
		logFormatter = Formatter(
			fmt="{codepath!s}:\n{message}",
			style="{"
		)
	logHandler.setFormatter(logFormatter)
	log.root.addHandler(logHandler)
	redirectStdout(log)
	sys.excepthook = _excepthook
	warnings.showwarning = _showwarning
	warnings.simplefilter("default", DeprecationWarning)


def isLogLevelForced() -> bool:
	"""Check if the log level was overridden either from the command line or because of secure mode.
	"""
	return (
		globalVars.appArgs.secure
		or globalVars.appArgs.debugLogging
		or globalVars.appArgs.logLevel != 0
		or globalVars.appArgs.noLogging
	)


def setLogLevelFromConfig():
	"""Set the log level based on the current configuration.
	"""
	if isLogLevelForced():
		return
	import config
	levelName=config.conf["general"]["loggingLevel"]
	# logging.getLevelName can give you a level number if given a name.
	level = logging.getLevelName(levelName)
	# The lone exception to level higher than INFO is "OFF" (100).
	# Setting a log level to something other than options found in the GUI is unsupported.
	if level not in (log.DEBUG, log.IO, log.DEBUGWARNING, log.INFO, log.OFF):
		log.warning("invalid setting for logging level: %s" % levelName)
		level = log.INFO
		config.conf["general"]["loggingLevel"] = logging.getLevelName(log.INFO)
	log.setLevel(level)
	log.root.setLevel(max(level, logging.WARN))
