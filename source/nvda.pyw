#nvda.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2017 NV Access Limited, Aleksey Sadovoy, Babbage B.V., Joseph Lee
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""The NVDA launcher. It can handle some command-line arguments (including help). It sets up logging, and then starts the core."""

import sys
import os

if getattr(sys, "frozen", None):
	# We are running as an executable.
	# Append the path of the executable to sys so we can import modules from the dist dir.
	sys.path.append(sys.prefix)
	os.chdir(sys.prefix)
else:
	import sourceEnv
	#We should always change directory to the location of this module (nvda.pyw), don't rely on sys.path[0]
	os.chdir(os.path.normpath(os.path.dirname(__file__)))

import pythonMonkeyPatches

import ctypes
import locale
import gettext

#Localization settings
locale.setlocale(locale.LC_ALL,'')
try:
	gettext.translation('nvda',localedir='locale',languages=[locale.getlocale()[0]]).install(True)
except:
	gettext.install('nvda',unicode=True)

import time
import argparse
import win32con
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
	# It returns 0 (success) if in a store app, and an error code otherwise. 
	config.isAppX=(GetCurrentPackageFullName(ctypes.byref(bufLen),None)==0)

class NoConsoleOptionParser(argparse.ArgumentParser):
	"""A commandline option parser that shows its messages using dialogs,  as this pyw file has no dos console window associated with it"""

	def print_help(self, file=None):
		"""Shows help in a standard Windows message dialog"""
		winUser.MessageBox(0, unicode(self.format_help()), u"Help", 0)

	def error(self, message):
		"""Shows an error in a standard Windows message dialog, and then exits NVDA"""
		out = ""
		out = self.format_usage()
		out += "\nerror: %s" % message
		winUser.MessageBox(0, unicode(out), u"Error", 0)
		sys.exit(2)

globalVars.startTime=time.time()

# Check OS version requirements
import winVersion
if not winVersion.isSupportedOS():
	winUser.MessageBox(0, unicode(ctypes.FormatError(winUser.ERROR_OLD_WIN_VERSION)), None, winUser.MB_ICONERROR)
	sys.exit(1)

def decodeMbcs(string):
	"""Decode a multi-byte character set string"""
	return string.decode("mbcs")

#Process option arguments
parser=NoConsoleOptionParser()
quitGroup = parser.add_mutually_exclusive_group()
quitGroup.add_argument('-q','--quit',action="store_true",dest='quit',default=False,help="Quit already running copy of NVDA")
quitGroup.add_argument('-r','--replace',action="store_true",dest='replace',default=False,help="Quit already running copy of NVDA and start this one")
parser.add_argument('-k','--check-running',action="store_true",dest='check_running',default=False,help="Report whether NVDA is running via the exit code; 0 if running, 1 if not running")
parser.add_argument('-f','--log-file',dest='logFileName',type=decodeMbcs,help="The file where log messages should be written to")
parser.add_argument('-l','--log-level',dest='logLevel',type=int,default=0,choices=[10,20,30,40,50],help="The lowest level of message logged (debug 10, info 20, warning 30, error 40, critical 50), default is warning")
parser.add_argument('-c','--config-path',dest='configPath',default=None,type=decodeMbcs,help="The path where all settings for NVDA are stored")
parser.add_argument('-m','--minimal',action="store_true",dest='minimal',default=False,help="No sounds, no interface, no start message etc")
parser.add_argument('-s','--secure',action="store_true",dest='secure',default=False,help="Secure mode (disable Python console)")
parser.add_argument('--disable-addons',action="store_true",dest='disableAddons',default=False,help="Disable all add-ons")
parser.add_argument('--debug-logging',action="store_true",dest='debugLogging',default=False,help="Enable debug level logging just for this run. This setting will override any other log level (--loglevel, -l) argument given.")
parser.add_argument('--no-sr-flag',action="store_false",dest='changeScreenReaderFlag',default=True,help="Don't change the global system screen reader flag")
installGroup = parser.add_mutually_exclusive_group()
installGroup.add_argument('--install',action="store_true",dest='install',default=False,help="Installs NVDA (starting the new copy after installation)")
installGroup.add_argument('--install-silent',action="store_true",dest='installSilent',default=False,help="Installs NVDA silently (does not start the new copy after installation).")
installGroup.add_argument('--create-portable',action="store_true",dest='createPortable',default=False,help="Creates a portable copy of NVDA (starting the new copy after installation)")
installGroup.add_argument('--create-portable-silent',action="store_true",dest='createPortableSilent',default=False,help="Creates a portable copy of NVDA silently (does not start the new copy after installation).")
parser.add_argument('--portable-path',dest='portablePath',default=None,type=decodeMbcs,help="The path where a portable copy will be created")
parser.add_argument('--launcher',action="store_true",dest='launcher',default=False,help="Started from the launcher")
# This option currently doesn't actually do anything.
# It is passed by Ease of Access so that if someone downgrades without uninstalling (despite our discouragement),
# the downgraded copy won't be started in non-secure mode on secure desktops.
# (Older versions always required the --secure option to start in secure mode.)
# If this occurs, the user will see an obscure error,
# but that's far better than a major security hazzard.
parser.add_argument('--ease-of-access',action="store_true",dest='easeOfAccess',default=False,help="Started by Windows Ease of Access")
(globalVars.appArgs,globalVars.appArgsExtra)=parser.parse_known_args()

def terminateRunningNVDA(window):
	processID,threadID=winUser.getWindowThreadProcessID(window)
	winUser.PostMessage(window,win32con.WM_QUIT,0,0)
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
except:
	oldAppWindowHandle=0
if not winUser.isWindow(oldAppWindowHandle):
	oldAppWindowHandle=0
if oldAppWindowHandle and (globalVars.appArgs.quit or globalVars.appArgs.replace):
	try:
		terminateRunningNVDA(oldAppWindowHandle)
	except:
		sys.exit(1)
if globalVars.appArgs.quit or (oldAppWindowHandle and not globalVars.appArgs.replace):
	sys.exit(0)
elif globalVars.appArgs.check_running:
	# NVDA is not running.
	sys.exit(1)

UOI_NAME = 2
def getDesktopName():
	desktop = ctypes.windll.user32.GetThreadDesktop(ctypes.windll.kernel32.GetCurrentThreadId())
	name = ctypes.create_unicode_buffer(256)
	ctypes.windll.user32.GetUserObjectInformationW(desktop, UOI_NAME, ctypes.byref(name), ctypes.sizeof(name), None)
	return name.value

#Ensure multiple instances are not fully started by using a mutex
ERROR_ALREADY_EXISTS=0XB7
desktopName=getDesktopName()
mutex=ctypes.windll.kernel32.CreateMutexW(None,True,u"Local\\NVDA_%s"%desktopName)
if not mutex or ctypes.windll.kernel32.GetLastError()==ERROR_ALREADY_EXISTS:
	if mutex: ctypes.windll.kernel32.CloseHandle(mutex)
	sys.exit(1)

isSecureDesktop = desktopName == "Winlogon"
if isSecureDesktop:
	import _winreg
	try:
		k = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, ur"SOFTWARE\NVDA")
		if not _winreg.QueryValueEx(k, u"serviceDebug")[0]:
			globalVars.appArgs.secure = True
	except WindowsError:
		globalVars.appArgs.secure = True
	globalVars.appArgs.changeScreenReaderFlag = False
	globalVars.appArgs.minimal = True
	globalVars.appArgs.configPath = os.path.join(sys.prefix, "systemConfig")

#os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker

#Initial logging and logging code

logLevel=globalVars.appArgs.logLevel
if logLevel<=0:
	logLevel=log.INFO
if globalVars.appArgs.debugLogging:
	logLevel=log.DEBUG
logHandler.initialize()
logHandler.log.setLevel(logLevel)

log.info("Starting NVDA")
log.debug("Debug level logging enabled")
if globalVars.appArgs.changeScreenReaderFlag:
	winUser.setSystemScreenReaderFlag(True)
#Accept wm_quit from other processes, even if running with higher privilages
if not ctypes.windll.user32.ChangeWindowMessageFilter(win32con.WM_QUIT,1):
	raise WinError()
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
	ctypes.windll.kernel32.CloseHandle(mutex)

log.info("NVDA exit")
sys.exit(globalVars.exitCode)
