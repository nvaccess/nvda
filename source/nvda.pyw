#nvda.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import sys
import codecs
import tempfile
import ctypes
import winsound
import locale
import gettext
import time
import optparse
import win32gui
import win32con
import globalVars
import debug
import winUser

restartByErrorCount=0

class NoConsoleOptionParser(optparse.OptionParser):

	def print_help(self, file=None):
		win32gui.MessageBox(0, self.format_help(), "Help", 0)

	def error(self, msg):
		out = ""
		if self.usage:
			out = self.get_usage()
		out += "\nerror: %s" % msg
		win32gui.MessageBox(0, out, "Error", 0)
		sys.exit(2)

def abortWithError(code):
	debug.writeException("critical error")
	winsound.PlaySound("SystemHand",winsound.SND_ALIAS)
	winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
	winUser.setSystemScreenReaderFlag(False)
	debug.stop()
	sys.exit(code)

globalVars.startTime=time.time()

if getattr(sys, "frozen", None):
	# We are running as an executable.
	# Append the path of the executable to sys so we can import modules from the dist dir.
	sys.path.append(sys.prefix)
	os.chdir(sys.prefix)
	debugFileName='%s\\nvda_debug.log'%tempfile.gettempdir()
	stderrFileName='%s\\nvda_stderr.log'%tempfile.gettempdir()
else:
	os.chdir(sys.path[0])
	debugFileName='debug.log'
	stderrFileName='stderr.log'

#Localization settings
locale.setlocale(locale.LC_ALL,'')
try:
	gettext.translation('nvda',localedir='locale',languages=[locale.getlocale()[0]]).install(True)
except:
	gettext.install('nvda',unicode=True)

#Process option arguments
parser=NoConsoleOptionParser()
parser.add_option('-q','--quit',action="store_true",dest='quit',default=False,help="Quit already running copy of NVDA")
parser.add_option('-d','--debug-file',dest='debugFileName',default=debugFileName,help="The file where debug messages should be written to")
parser.add_option('-s','--stderr-file',dest='stderrFileName',default=stderrFileName,help="The file where errors not caught by debug should go")
parser.add_option('-c','--config-file',dest='configFileName',default="./nvda.ini",help="The file where all settings are stored")
parser.add_option('-m','--minimal',action="store_true",dest='minimal',default=False,help="No sounds, no interface, no start message etc")
(globalVars.appArgs,extraArgs)=parser.parse_args()

#Handle running multiple instances of NVDA
try:
	oldAppWindowHandle=win32gui.FindWindow('wxWindowClassNR','NVDA')
except:
	oldAppWindowHandle=0
if win32gui.IsWindow(oldAppWindowHandle): 
	if globalVars.appArgs.quit:
		win32gui.PostMessage(oldAppWindowHandle,win32con.WM_QUIT,0,0)
	sys.exit(1)

#os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker
#Initial logging and debugging code

stderrFile=codecs.open(globalVars.appArgs.stderrFileName,"w","utf-8","ignore")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
sys.stdout=stderrFile

if not globalVars.appArgs.minimal:
	winsound.PlaySound("waves\\start.wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
debug.start(globalVars.appArgs.debugFileName)
winUser.setSystemScreenReaderFlag(True)
try:
	import core
except:
	abortWithError(3)
res=core.main()
if res in [core.CORE_MAINLOOPERROR,core.CORE_RESTART]:
	winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
	os.spawnv(os.P_NOWAIT,sys.executable,[os.path.basename(sys.executable)]+sys.argv)
	os._exit(0)
elif res==core.CORE_INITERROR:
	abortWithError(4)
winUser.setSystemScreenReaderFlag(False)
debug.stop()
if not globalVars.appArgs.minimal:
	winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
