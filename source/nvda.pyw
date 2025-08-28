# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2025 NV Access Limited, Aleksey Sadovoy, Babbage B.V., Joseph Lee, Łukasz Golonka,
# Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""The NVDA launcher - main / entry point into NVDA.
It can handle some command-line arguments (including help).
It sets up logging, and then starts the core.
"""

import logging
import sys
import os

from pathlib import Path
from typing import Any

import winBindings.kernel32
import globalVars
from argsParsing import getParser
import ctypes
from ctypes import wintypes
import monkeyPatches

import NVDAState
import winUser

monkeyPatches.applyMonkeyPatches()

#: logger to use before the true NVDA log is initialised.
# Ideally, all logging would be captured by the NVDA log, however this would introduce contention
# when multiple NVDA processes run simultaneously.
_log = logging.Logger(name="preStartup", level=logging.INFO)
_log.addHandler(logging.NullHandler(level=logging.INFO))

if NVDAState.isRunningAsSource():
	# We should always change directory to the location of this module (nvda.pyw), don't rely on sys.path[0]
	appDir = os.path.abspath(os.path.dirname(__file__))
	# Ensure we are inside the Python virtual environment
	virtualEnv = os.getenv("VIRTUAL_ENV")
	if not virtualEnv or Path(appDir).parent != Path(virtualEnv).parent:
		ctypes.windll.user32.MessageBoxW(
			0,
			"NVDA cannot  detect the Python virtual environment. "
			"To run NVDA from source, please use runnvda.bat in the root of this repository.",
			"Error",
			winUser.MB_ICONERROR,
		)
		sys.exit(1)
else:
	# Append the path of the executable to sys so we can import modules from the dist dir.
	sys.path.append(sys.prefix)
	appDir = os.path.abspath(sys.prefix)

os.chdir(appDir)
globalVars.appDir = appDir
globalVars.appPid = os.getpid()


import config  # noqa: E402
import logHandler  # noqa: E402
from logHandler import log  # noqa: E402
import winKernel  # noqa: E402

# Find out if NVDA is running as a Windows Store application
bufLen = ctypes.c_int()
try:
	GetCurrentPackageFullName = ctypes.windll.kernel32.GetCurrentPackageFullName
except AttributeError:
	config.isAppX = False
else:
	bufLen = ctypes.c_int()
	# Use GetCurrentPackageFullName to detect if we are running as a store app.
	# #8362: error 15700 (not a package) error is returned if this is not a Windows Store package.
	config.isAppX = GetCurrentPackageFullName(ctypes.byref(bufLen), None) != 15700


NVDAState._initializeStartTime()


# Check OS version requirements
import winVersion  # noqa: E402

if not winVersion.isSupportedOS():
	winUser.MessageBox(0, ctypes.FormatError(winUser.ERROR_OLD_WIN_VERSION), None, winUser.MB_ICONERROR)
	sys.exit(1)


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility."""
	if NVDAState._allowDeprecatedAPI():
		if attrName in ("NoConsoleOptionParser", "stringToBool", "stringToLang"):
			import argsParsing

			log.warning(f"__main__.{attrName} is deprecated, use argsParsing.{attrName} instead.")
			return getattr(argsParsing, attrName)
		if attrName == "parser":
			import argsParsing

			log.warning(f"__main__.{attrName} is deprecated, use argsParsing.getParser() instead.")
			return argsParsing.getParser()
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


_parser = getParser()
(globalVars.appArgs, globalVars.unknownAppArgs) = _parser.parse_known_args()
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
	processID, threadID = winUser.getWindowThreadProcessID(window)
	winUser.PostMessage(window, winUser.WM_QUIT, 0, 0)
	h = winKernel.openProcess(winKernel.SYNCHRONIZE, False, processID)
	if not h:
		# The process is already dead.
		return
	try:
		res = winKernel.waitForSingleObject(h, 4000)
		if res == 0:
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


# Handle running multiple instances of NVDA
try:
	oldAppWindowHandle = winUser.FindWindow("wxWindowClassNR", "NVDA")
except WindowsError as e:
	_log.info("Can't find existing NVDA via Window Class")
	_log.debug(f"FindWindow error: {e}")
	oldAppWindowHandle = 0
if not winUser.isWindow(oldAppWindowHandle):
	oldAppWindowHandle = 0

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
		winUser.MessageBox(
			0,
			f"Couldn't terminate existing NVDA process, abandoning start:\nException: {e}",
			"Error",
			winUser.MB_OK,
		)

if globalVars.appArgs.quit or (oldAppWindowHandle and globalVars.appArgs.easeOfAccess):
	_log.debug("Quitting")
	sys.exit(0)
elif globalVars.appArgs.check_running:
	# NVDA is not running.
	_log.debug("Is running check: NVDA is not running")
	_log.debug("Exiting")
	sys.exit(1)


# Suppress E402 (module level import not at top of file)
from utils.security import isRunningOnSecureDesktop  # noqa: E402
from systemUtils import _getDesktopName  # noqa: E402

# Ensure multiple instances are not fully started by using a mutex
desktopName = _getDesktopName()
_log.info(f"DesktopName: {desktopName}")


def _acquireMutex(_desktopName: str) -> wintypes.HANDLE | None:
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
		f"Local\\NVDA_{_desktopName}",  # lpName
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
			2000,  # dwMilliseconds
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
	_log.error("Unknown mutex acquisition error. Exiting")
	sys.exit(1)


if NVDAState._forceSecureModeEnabled():
	globalVars.appArgs.secure = True


if isRunningOnSecureDesktop():
	if not NVDAState._serviceDebugEnabled():
		globalVars.appArgs.secure = True
	globalVars.appArgs.changeScreenReaderFlag = False
	globalVars.appArgs.minimal = True
	globalVars.appArgs.configPath = os.path.join(sys.prefix, "systemConfig")

# os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
# import pychecker.checker

# Initial logging and logging code
# #8516: because config manager isn't ready yet, we must let start and exit messages be logged unless disabled via --no-logging switch.
# However, do log things if debug logging or log level other than 0 (not set) is requested from command line switches.
_log = None
logHandler.initialize()
if logHandler.log.getEffectiveLevel() is log.DEBUG:
	log.debug("Provided arguments: {}".format(sys.argv[1:]))
import buildVersion  # noqa: E402

log.info(f"Starting NVDA version {buildVersion.version} {os.environ['PROCESSOR_ARCHITECTURE']}")
log.debug("Debug level logging enabled")
if globalVars.appArgs.changeScreenReaderFlag:
	winUser.setSystemScreenReaderFlag(True)

# Accept WM_QUIT from other processes, even if running with higher privileges
if not ctypes.windll.user32.ChangeWindowMessageFilter(winUser.WM_QUIT, winUser.MSGFLT.ALLOW):
	log.error("Unable to set the NVDA process to receive WM_QUIT messages from other processes")
	raise winUser.WinError()
# Make this the last application to be shut down and don't display a retry dialog box.
winKernel.SetProcessShutdownParameters(0x100, winKernel.SHUTDOWN_NORETRY)
if not isRunningOnSecureDesktop() and not config.isAppX:
	import easeOfAccess

	easeOfAccess.notify(3)
try:
	import core

	core.main()
except:  # noqa: E722
	log.critical("core failure", exc_info=True)
	sys.exit(1)
finally:
	if not isRunningOnSecureDesktop() and not config.isAppX:
		easeOfAccess.notify(2)
	if globalVars.appArgs.changeScreenReaderFlag:
		winUser.setSystemScreenReaderFlag(False)

	# From MS docs; "Multiple processes can have handles of the same mutex object"
	# > Use the CloseHandle function to close the handle.
	# > The system closes the handle automatically when the process terminates.
	# > The mutex object is destroyed when its last handle has been closed.
	# https://docs.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-createmutexw
	releaseResult = winBindings.kernel32.ReleaseMutex(mutex)
	if 0 == releaseResult:
		releaseError = winUser.GetLastError()
		log.debug(f"Failed to release mutex, error: {releaseError}")
	res = winBindings.kernel32.CloseHandle(mutex)
	if 0 == res:
		error = winUser.GetLastError()
		log.error(f"Unable to close mutex handle, last error: {winUser.WinError(error)}")

log.info("NVDA exit")
sys.exit(NVDAState._getExitCode())
