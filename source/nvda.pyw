#nvda.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""The NVDA launcher. It can handle some command-line arguments (including help). It sets up logging, and then starts the core. it also handles the playing of the startup and exit sounds."""
 
import os
import sys
import tempfile
import winsound
import locale
import gettext
import time
import optparse
import win32gui
import win32con
import globalVars
import logHandler
from logHandler import log
import winUser
import winKernel

class NoConsoleOptionParser(optparse.OptionParser):
	"""A commandline option parser that shows its messages using dialogs,  as this pyw file has no dos console window associated with it"""

	def print_help(self, file=None):
		"""Shows help in a standard Windows message dialog"""
		win32gui.MessageBox(0, self.format_help(), "Help", 0)

	def error(self, msg):
		"""Shows an error in a standard Windows message dialog, and then exits NVDA"""
		out = ""
		if self.usage:
			out = self.get_usage()
		out += "\nerror: %s" % msg
		win32gui.MessageBox(0, out, "Error", 0)
		sys.exit(2)

globalVars.startTime=time.time()

if getattr(sys, "frozen", None):
	# We are running as an executable.
	# Append the path of the executable to sys so we can import modules from the dist dir.
	sys.path.append(sys.prefix)
	os.chdir(sys.prefix)
	logFileName='%s\\nvda.log'%tempfile.gettempdir()
else:
	os.chdir(sys.path[0])
	logFileName='nvda.log'

#Localization settings
locale.setlocale(locale.LC_ALL,'')
try:
	gettext.translation('nvda',localedir='locale',languages=[locale.getlocale()[0]]).install(True)
except:
	gettext.install('nvda',unicode=True)

#Process option arguments
parser=NoConsoleOptionParser()
parser.add_option('-q','--quit',action="store_true",dest='quit',default=False,help="Quit already running copy of NVDA")
parser.add_option('-r','--replace',action="store_true",dest='replace',default=False,help="Quit already running copy of NVDA and start this one")
parser.add_option('-f','--log-file',dest='logFileName',default=logFileName,help="The file where log messages should be written to")
parser.add_option('-l','--log-level',type="int",dest='logLevel',default=0,help="The lowest level of message logged (debug 10, info 20, warning 30, error 40, critical 50), default is warning") 
parser.add_option('-c','--config-file',dest='configFileName',default="./nvda.ini",help="The file where all settings are stored")
parser.add_option('-m','--minimal',action="store_true",dest='minimal',default=False,help="No sounds, no interface, no start message etc")
(globalVars.appArgs,extraArgs)=parser.parse_args()

#Handle running multiple instances of NVDA
try:
	oldAppWindowHandle=win32gui.FindWindow('wxWindowClassNR','NVDA')
except:
	oldAppWindowHandle=0
if not win32gui.IsWindow(oldAppWindowHandle):
	oldAppWindowHandle=0
if oldAppWindowHandle:
	processID,threadID=winUser.getWindowThreadProcessID(oldAppWindowHandle)
	if globalVars.appArgs.quit or globalVars.appArgs.replace:
		win32gui.PostMessage(oldAppWindowHandle,win32con.WM_QUIT,0,0)
		h=winKernel.openProcess(winKernel.SYNCHRONIZE,False,processID)
		if h:
			res=winKernel.waitForSingleObject(h,10000)
			if res!=0:
				win32gui.MessageBox(0, "Error quitting NVDA", "Error", 0)
				sys.exit(1)
if globalVars.appArgs.quit or (oldAppWindowHandle and not globalVars.appArgs.replace):
	sys.exit(0)

#os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker
#Initial logging and logging code

logLevel=globalVars.appArgs.logLevel
if logLevel<=0:
	logLevel=log.INFO
logHandler.initialize()
logHandler.log.setLevel(logLevel)

log.info("Starting NVDA")

if not globalVars.appArgs.minimal:
	winsound.PlaySound("waves\\start.wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
winUser.setSystemScreenReaderFlag(True)
try:
	import core
	core.main()
except:
	log.critical("core failure",exc_info=True)
	sys.exit(1)
finally:
	winUser.setSystemScreenReaderFlag(False)
	if not globalVars.appArgs.minimal:
		winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
if globalVars.restart:
	os.spawnv(os.P_NOWAIT,sys.executable,[os.path.basename(sys.executable)]+sys.argv)
	sys.exit(0)

log.info("NVDA exit")
