#Initial logging and debugging code
import sys
import winsound
stderrFile=open("stderr.log","w")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
sys.stdout=stderrFile

import debug
debug.start("debug.log")

winsound.Beep(440,100)
try:
	import core
	core.main()
except:
	debug.writeException("nvda.pyw executing core.main")
debug.stop()
winsound.Beep(880,100)

