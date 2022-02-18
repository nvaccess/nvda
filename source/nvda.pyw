# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Aleksey Sadovoy, Babbage B.V., Joseph Lee, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""The NVDA launcher - main / entry point into NVDA.
It can handle some command-line arguments (including help).
It sets up logging, and then starts the core.
"""
import logging
import sys
import os

import typing

import globalVars
import ctypes
from ctypes import wintypes
import monkeyPatches

monkeyPatches.applyMonkeyPatches()

#: logger to use before the true NVDA log is initialised.
# Ideally, all logging would be captured by the NVDA log, however this would introduce contention
# when multiple NVDA processes run simultaneously.
_log = logging.Logger(name="preStartup", level=logging.INFO)
_log.addHandler(logging.NullHandler(level=logging.INFO))

customVenvDetected = False
if getattr(sys, "frozen", None):
	# We are running as an executable.
	# Append the path of the executable to sys so we can import modules from the dist dir.
	sys.path.append(sys.prefix)
	appDir = sys.prefix
else:
	# we are running from source
	# Ensure we are inside the NVDA build system's Python virtual environment.
	nvdaVenv = os.getenv("NVDA_VENV")
	virtualEnv = os.getenv("VIRTUAL_ENV")
	if not virtualEnv or not os.path.isdir(virtualEnv):
		ctypes.windll.user32.MessageBoxW(
			0,
			"NVDA cannot  detect the Python virtual environment. "
			"To run NVDA from source, please use runnvda.bat in the root of this repository.",
			"Error",
			0,
		)
		sys.exit(1)
	customVenvDetected = nvdaVenv != virtualEnv
	import sourceEnv
	#We should always change directory to the location of this module (nvda.pyw), don't rely on sys.path[0]
	appDir = os.path.normpath(os.path.dirname(__file__))
appDir = os.path.abspath(appDir)
os.chdir(appDir)
globalVars.appDir = appDir


import locale
import gettext

try:
	gettext.translation(
		'nvda',
		localedir=os.path.join(globalVars.appDir, 'locale'),
		languages=[locale.getdefaultlocale()[0]]
	).install(True)
except:
	gettext.install('nvda')

import time
import argparse
import globalVars
import config
import logHandler
from logHandler import log
import winUser
import winKernel

# Find out if NVDA is running as a Windows Store application
bufLen=ctypes.c_int()
try:
	GetCurrentPackageFullName=ctypes.windll.kernel32.GetCurrentPackageFullName
except AttributeError:
	config.isAppX=False
else:
	bufLen=ctypes.c_int()
	# Use GetCurrentPackageFullName to detect if we are running as a store app.
	# #8362: error 15700 (not a package) error is returned if this is not a Windows Store package.
	config.isAppX=(GetCurrentPackageFullName(ctypes.byref(bufLen),None)!=15700)

class NoConsoleOptionParser(argparse.ArgumentParser):
	"""A commandline option parser that shows its messages using dialogs,  as this pyw file has no dos console window associated with it"""

	def print_help(self, file=None):
		"""Shows help in a standard Windows message dialog"""
		winUser.MessageBox(0, self.format_help(), u"Help", 0)

	def error(self, message):
		"""Shows an error in a standard Windows message dialog, and then exits NVDA"""
		out = ""
		out = self.format_usage()
		out += "\nerror: %s" % message
		winUser.MessageBox(0, out, u"Error", 0)
		sys.exit(2)

globalVars.startTime=time.time()

# Check OS version requirements
import winVersion
if not winVersion.isSupportedOS():
	winUser.MessageBox(0, ctypes.FormatError(winUser.ERROR_OLD_WIN_VERSION), None, winUser.MB_ICONERROR)
	sys.exit(1)


def stringToBool(string):
	"""Wrapper for configobj.validate.is_boolean to raise the proper exception for wrong values."""
	from configobj.validate import is_boolean, ValidateError
	try:
		return is_boolean(string)
	except ValidateError as e:
		raise argparse.ArgumentTypeError(e.message)


def stringToLang(value: str) -> str:
	"""Perform basic case normalization for ease of use.
	"""
	import languageHandler
	if value.casefold() == "Windows".casefold():
		normalizedLang = "Windows"
	else:
		normalizedLang = languageHandler.normalizeLanguage(value)
	possibleLangNames = languageHandler.listNVDALocales()
	if normalizedLang is not None and normalizedLang in possibleLangNames:
		return normalizedLang
	raise argparse.ArgumentTypeError(
		f"Language code should be one of:\n{', '.join(possibleLangNames)}."
	)


#Process option arguments
parser=NoConsoleOptionParser()
quitGroup = parser.add_mutually_exclusive_group()
quitGroup.add_argument('-q','--quit',action="store_true",dest='quit',default=False,help="Quit already running copy of NVDA")
parser.add_argument('-k','--check-running',action="store_true",dest='check_running',default=False,help="Report whether NVDA is running via the exit code; 0 if running, 1 if not running")
parser.add_argument('-f','--log-file',dest='logFileName',type=str,help="The file where log messages should be written to")
parser.add_argument('-l','--log-level',dest='logLevel',type=int,default=0,choices=[10, 12, 15, 20, 30, 40, 50, 100],help="The lowest level of message logged (debug 10, input/output 12, debugwarning 15, info 20, warning 30, error 40, critical 50, off 100), default is info")
parser.add_argument('-c','--config-path',dest='configPath',default=None,type=str,help="The path where all settings for NVDA are stored")
parser.add_argument(
	'--lang',
	dest='language',
	default="en",
	type=stringToLang,
	help=(
		"Override the configured NVDA language."
		" Set to \"Windows\" for current user default, \"en\" for English, etc."
	)
)
parser.add_argument('-m','--minimal',action="store_true",dest='minimal',default=False,help="No sounds, no interface, no start message etc")
parser.add_argument('-s','--secure',action="store_true",dest='secure',default=False,help="Secure mode (disable Python console)")
parser.add_argument('--disable-addons',action="store_true",dest='disableAddons',default=False,help="Disable all add-ons")
parser.add_argument('--debug-logging',action="store_true",dest='debugLogging',default=False,help="Enable debug level logging just for this run. This setting will override any other log level (--loglevel, -l) argument given, as well as no logging option.")
parser.add_argument('--no-logging',action="store_true",dest='noLogging',default=False,help="Disable logging completely for this run. This setting can be overwritten with other log level (--loglevel, -l) switch or if debug logging is specified.")
parser.add_argument('--no-sr-flag',action="store_false",dest='changeScreenReaderFlag',default=True,help="Don't change the global system screen reader flag")
installGroup = parser.add_mutually_exclusive_group()
installGroup.add_argument('--install',action="store_true",dest='install',default=False,help="Installs NVDA (starting the new copy after installation)")
installGroup.add_argument('--install-silent',action="store_true",dest='installSilent',default=False,help="Installs NVDA silently (does not start the new copy after installation).")
installGroup.add_argument('--create-portable',action="store_true",dest='createPortable',default=False,help="Creates a portable copy of NVDA (starting the new copy after installation)")
installGroup.add_argument('--create-portable-silent',action="store_true",dest='createPortableSilent',default=False,help="Creates a portable copy of NVDA silently (does not start the new copy after installation).")
parser.add_argument('--portable-path',dest='portablePath',default=None,type=str,help="The path where a portable copy will be created")
parser.add_argument('--launcher',action="store_true",dest='launcher',default=False,help="Started from the launcher")
parser.add_argument('--enable-start-on-logon',metavar="True|False",type=stringToBool,dest='enableStartOnLogon',default=None,
	help="When installing, enable NVDA's start on the logon screen")
parser.add_argument(
	'--copy-portable-config',
	action="store_true",
	dest='copyPortableConfig',
	default=False,
	help=(
		"When installing, copy the portable configuration "
		"from the provided path (--config-path, -c) to the current user account"
	)
)
# This option is passed by Ease of Access so that if someone downgrades without uninstalling
# (despite our discouragement), the downgraded copy won't be started in non-secure mode on secure desktops.
# (Older versions always required the --secure option to start in secure mode.)
# If this occurs, the user will see an obscure error,
# but that's far better than a major security hazzard.
# If this option is provided, NVDA will not replace an already running instance (#10179) 
parser.add_argument('--ease-of-access',action="store_true",dest='easeOfAccess',default=False,help="Started by Windows Ease of Access")
(globalVars.appArgs, globalVars.unknownAppArgs) = parser.parse_known_args()
# Make any app args path values absolute
# So as to not be affected by the current directory changing during process lifetime.
pathAppArgs = [
	"configPath",
	"logFileName",
	"portablePath",
]
for name in pathAppArgs:
	origVal = getattr(globalVars.appArgs, name)
	if isinstance(origVal, str):
		newVal = os.path.abspath(origVal)
		setattr(globalVars.appArgs, name, newVal)

def terminateRunningNVDA(window):
	processID,threadID=winUser.getWindowThreadProcessID(window)
	winUser.PostMessage(window,winUser.WM_QUIT,0,0)
	h=winKernel.openProcess(winKernel.SYNCHRONIZE,False,processID)
	if not h:
		# The process is already dead.
		return
	try:
		res=winKernel.waitForSingleObject(h,4000)
		if res==0:
			# The process terminated within the timeout period.
			return
	finally:
		winKernel.closeHandle(h)

	# The process is refusing to exit gracefully, so kill it forcefully.
	h = winKernel.openProcess(winKernel.PROCESS_TERMINATE | winKernel.SYNCHRONIZE, False, processID)
	if not h:
		raise OSError("Could not open process for termination")
	try:
		winKernel.TerminateProcess(h, 1)
		winKernel.waitForSingleObject(h, 2000)
	finally:
		winKernel.closeHandle(h)

#Handle running multiple instances of NVDA
try:
	oldAppWindowHandle=winUser.FindWindow(u'wxWindowClassNR',u'NVDA')
except WindowsError as e:
	_log.info("Can't find existing NVDA via Window Class")
	_log.debug(f"FindWindow error: {e}")
	oldAppWindowHandle=0
if not winUser.isWindow(oldAppWindowHandle):
	oldAppWindowHandle=0

if oldAppWindowHandle and not globalVars.appArgs.easeOfAccess:
	_log.debug(f"NVDA already running. OldAppWindowHandle: {oldAppWindowHandle}")
	if globalVars.appArgs.check_running:
		# NVDA is running.
		_log.debug("Is running check complete: NVDA is running.")
		_log.debug("Exiting")
		sys.exit(0)
	try:
		_log.debug(f"Terminating oldAppWindowHandle: {oldAppWindowHandle}")
		terminateRunningNVDA(oldAppWindowHandle)
	except Exception as e:
		parser.error(f"Couldn't terminate existing NVDA process, abandoning start:\nException: {e}")

if globalVars.appArgs.quit or (oldAppWindowHandle and globalVars.appArgs.easeOfAccess):
	_log.debug("Quitting")
	sys.exit(0)
elif globalVars.appArgs.check_running:
	# NVDA is not running.
	_log.debug("Is running check: NVDA is not running")
	_log.debug("Exiting")
	sys.exit(1)

UOI_NAME = 2
def getDesktopName():
	desktop = ctypes.windll.user32.GetThreadDesktop(ctypes.windll.kernel32.GetCurrentThreadId())
	name = ctypes.create_unicode_buffer(256)
	ctypes.windll.user32.GetUserObjectInformationW(desktop, UOI_NAME, ctypes.byref(name), ctypes.sizeof(name), None)
	return name.value


# Ensure multiple instances are not fully started by using a mutex
desktopName = getDesktopName()
_log.info(f"DesktopName: {desktopName}")


def _acquireMutex(_desktopName: str) -> typing.Optional[wintypes.HANDLE]:
	# From MS docs; "Multiple processes can have handles of the same mutex object"
	# > Two or more processes can call CreateMutex to create the same named mutex.
	# > The first process actually creates the mutex, and subsequent processes with sufficient access rights
	# > simply open a handle to the existing mutex.
	# > This enables multiple processes to get handles of the same mutex, while relieving the user of the
	# > responsibility of ensuring that the creating process is started first.
	# > When using this technique, you should set the bInitialOwner flag to FALSE; otherwise, it can be difficult
	# > to be certain which process has initial ownership.
	# > https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexw
	_mutex = ctypes.windll.kernel32.CreateMutexW(
		None,  # lpMutexAttributes,
		# Don't take initial ownership, use wait to acquire ownership instead.
		# Allows waiting for a prior process to finish exiting.
		False,  # bInitialOwner
		f"Local\\NVDA_{_desktopName}"  # lpName
	)
	createMutexResult = ctypes.windll.kernel32.GetLastError()
	if not _mutex:
		_log.error(f"Unable to create mutex, last error: {createMutexResult}")
		raise winUser.WinError(createMutexResult)
	else:
		if createMutexResult == winKernel.ERROR_ALREADY_EXISTS:
			_log.debug("Waiting for prior NVDA to finish exiting")
		# We didn't ask to be the initial owner,
		waitResult = winKernel.waitForSingleObject(
			_mutex,  # hHandle
			2000  # dwMilliseconds
		)

		_log.debug(f"Wait result: {waitResult}")
		if winKernel.WAIT_OBJECT_0 == waitResult:
			_log.info("Prior NVDA has finished exiting")
			return _mutex  # mutex ownership acquired
		elif winKernel.WAIT_ABANDONED == waitResult:
			_log.error(
				"Prior NVDA exited without releasing mutex, taking ownership."
				" Note: Restarting your system is recommended."
				" This error indicates that NVDA previously did not exit correctly or was terminated"
				" (perhaps by the task manager)."
			)
			return _mutex  # mutex ownership acquired
		else:
			exception = None
			if winKernel.WAIT_TIMEOUT == waitResult:
				exception = Exception("Timeout exceeded waiting for mutex")
			elif winKernel.WAIT_FAILED == waitResult:
				waitError = winUser.GetLastError()
				_log.debug(f"Failed waiting for mutex, error: {waitError}")
				exception = winUser.WinError(waitError)
			releaseResult = ctypes.windll.kernel32.ReleaseMutex(_mutex)
			if 0 == releaseResult:
				releaseError = winUser.GetLastError()
				_log.debug(f"Failed to release mutex, error: {releaseError}")
			closeResult = ctypes.windll.kernel32.CloseHandle(_mutex)
			if 0 == closeResult:
				closeError = winUser.GetLastError()
				_log.debug(f"Failed to close mutex handle, error: {closeError}")
			if exception is not None:
				raise exception
	return None  # unable to acquire mutex, unknown reason.


try:
	mutex = _acquireMutex(desktopName)
except Exception as e:
	_log.error(f"Unable to acquire mutex: {e}")
	sys.exit(1)
if mutex is None:
	_log.error(f"Unknown mutex acquisition error. Exiting")
	sys.exit(1)

isSecureDesktop = desktopName == "Winlogon"
if isSecureDesktop:
	import winreg
	try:
		k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\NVDA")
		if not winreg.QueryValueEx(k, u"serviceDebug")[0]:
			globalVars.appArgs.secure = True
	except WindowsError:
		globalVars.appArgs.secure = True
	globalVars.appArgs.changeScreenReaderFlag = False
	globalVars.appArgs.minimal = True
	globalVars.appArgs.configPath = os.path.join(sys.prefix, "systemConfig")

#os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker

#Initial logging and logging code
# #8516: because config manager isn't ready yet, we must let start and exit messages be logged unless disabled via --no-logging switch.
# However, do log things if debug logging or log level other than 0 (not set) is requested from command line switches.
_log = None
logHandler.initialize()
if logHandler.log.getEffectiveLevel() is log.DEBUG:
	log.debug("Provided arguments: {}".format(sys.argv[1:]))
import buildVersion
log.info("Starting NVDA version %s" % buildVersion.version)
log.debug("Debug level logging enabled")
if customVenvDetected:
	log.warning("NVDA launched using a custom Python virtual environment.")
if globalVars.appArgs.changeScreenReaderFlag:
	winUser.setSystemScreenReaderFlag(True)

# Accept WM_QUIT from other processes, even if running with higher privileges
if not ctypes.windll.user32.ChangeWindowMessageFilter(winUser.WM_QUIT, winUser.MSGFLT.ALLOW):
	log.error("Unable to set the NVDA process to receive WM_QUIT messages from other processes")
	raise winUser.WinError()
# Make this the last application to be shut down and don't display a retry dialog box.
winKernel.SetProcessShutdownParameters(0x100, winKernel.SHUTDOWN_NORETRY)
if not isSecureDesktop and not config.isAppX:
	import easeOfAccess
	easeOfAccess.notify(3)
try:
	import core
	core.main()
except:
	log.critical("core failure",exc_info=True)
	sys.exit(1)
finally:
	if not isSecureDesktop and not config.isAppX:
		easeOfAccess.notify(2)
	if globalVars.appArgs.changeScreenReaderFlag:
		winUser.setSystemScreenReaderFlag(False)

	# From MS docs; "Multiple processes can have handles of the same mutex object"
	# > Use the CloseHandle function to close the handle.
	# > The system closes the handle automatically when the process terminates.
	# > The mutex object is destroyed when its last handle has been closed.
	# https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexw
	releaseResult = ctypes.windll.kernel32.ReleaseMutex(mutex)
	if 0 == releaseResult:
		releaseError = winUser.GetLastError()
		log.debug(f"Failed to release mutex, error: {releaseError}")
	res = ctypes.windll.kernel32.CloseHandle(mutex)
	if 0 == res:
		error = winUser.GetLastError()
		log.error(f"Unable to close mutex handle, last error: {winUser.WinError(error)}")

log.info("NVDA exit")
sys.exit(globalVars.exitCode)
