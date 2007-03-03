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
globalVars.startTime=time.time()

#os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker
#Initial logging and debugging code
import codecs
stderrFile=codecs.open(stderrFileName,"w","utf-8","ignore")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
sys.stdout=stderrFile
import winsound
winsound.PlaySound("waves\\start.wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
import debug
debug.start(debugFileName)
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
winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
