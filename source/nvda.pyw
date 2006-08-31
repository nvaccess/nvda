#Initial logging and debugging code
import sys
import winsound
stderrFile=open("stderr.log","w")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
import debug
debug.start("debug.log")

winsound.Beep(440,100)
try:
	import core
	core.main()
except:
	debug.writeException("nvda.pyw executing core.main")
winsound.Beep(880,100)

