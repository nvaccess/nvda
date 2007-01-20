import os
import sys
sys.setcheckinterval(100)
os.environ['PYCHECKER']="--limit 10000 -q --changetypes"
#import pychecker.checker
#Initial logging and debugging code
import sys
stderrFile=open("stderr.log","w")
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
