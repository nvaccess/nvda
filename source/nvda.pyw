#nvda.pyw
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

#import gc
#gc.set_debug(gc.DEBUG_LEAK)
import time
import globalVars
globalVars.startTime=time.time()

import os
os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker
#Initial logging and debugging code
import sys
import codecs
stderrFile=codecs.open("stderr.log","w","utf-8","ignore")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
sys.stdout=stderrFile
import winsound
winsound.PlaySound("waves\\start.wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
import debug
debug.start("debug.log")
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
