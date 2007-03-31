#nvda.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os
import sys
import tempfile
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

import time
import globalVars
import win32gui
import win32con
globalVars.startTime=time.time()
#Process option arguments
from optparse import OptionParser
parser=OptionParser()
parser.add_option('-q','--quit',action="store_true",dest='quit',default=False,help="Quit already running copy of NVDA")
parser.add_option('-d','--debug-file',dest='debugFileName',default=debugFileName,help="The file where debug messages should be written to")
parser.add_option('-s','--stderr-file',dest='stderrFileName',default=stderrFileName,help="The file where errors not caught by debug should go")
parser.add_option('-m','--minimal',action="store_true",dest='minimal',default=False,help="No sounds, no interface, no start message etc")
(globalVars.appArgs,extraArgs)=parser.parse_args()
#Handle running multiple instances of NVDA
try:
	oldAppWindowHandle=win32gui.FindWindow('wxWindowClassNR','NVDA Interface')
except:
	oldAppWindowHandle=0
if win32gui.IsWindow(oldAppWindowHandle): 
	if globalVars.appArgs.quit:
		win32gui.PostMessage(oldAppWindowHandle,win32con.WM_QUIT,0,0)
	sys.exit(1)

import winKernel
try:
	winKernel.freeConsole()
except:
	pass
#os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker
#Initial logging and debugging code
import codecs
stderrFile=codecs.open(globalVars.appArgs.stderrFileName,"w","utf-8","ignore")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
sys.stdout=stderrFile
import winsound
if not globalVars.appArgs.minimal:
	winsound.PlaySound("waves\\start.wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
import debug
debug.start(globalVars.appArgs.debugFileName)
import gettext
gettext.install("nvda", unicode=True)
try:
	import core
	res=core.main()
	if not res:
		winsound.PlaySound("SystemHand",winsound.SND_ALIAS)
		raise RuntimeError("core has errors")
except:
	debug.writeException("nvda.pyw executing core.main")
debug.stop()
if not globalVars.appArgs.minimal:
	winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
