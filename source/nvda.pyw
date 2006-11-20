#Initial logging and debugging code
import sys
stderrFile=open("stderr.log","w")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
sys.stdout=stderrFile

import winsound
winsound.Beep(440,50)
winsound.Beep((440*4)/3,50)
winsound.Beep(660,50)
winsound.Beep(880,50)
import gettext
gettext.install('nvda')
import debug

import debug
debug.start("debug.log")
try:
	import core
	res=core.main()
	if res:
		winsound.Beep(880,50)
		winsound.Beep(660,50)
		winsound.Beep((440*4)/3,50)
		winsound.Beep(440,50)
	else:
		raise RuntimeError("core has errors")
except:
	debug.writeException("nvda.pyw executing core.main")
	winsound.Beep(700,300)
debug.stop()
