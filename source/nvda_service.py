import win32serviceutil
import servicemanager
import pythoncom
import codecs
import time
import sys
import winsound
import gettext
import os
import debug
import globalVars

# This won't work if running as a py2exe service.
if os.path.basename(sys.argv[0]).lower() == "pythonservice.exe":
	# We are running as a service.
	os.chdir(sys.path[-1])
else:
	os.chdir(sys.path[0])

gettext.install('nvda',localedir='locale',unicode=True)
globalVars.startTime=time.time()

import core

class NVDAService(win32serviceutil.ServiceFramework):

	_svc_name_="nvda"
	_svc_display_name_="nonVisual Desktop Access"

	def SvcDoRun(self):
		stderrFile=codecs.open("stderr.log","w","utf-8","ignore")
		sys.stderr=stderrFile
		sys.stdout=stderrFile
		debug.start('debug.log')
		winsound.PlaySound("waves\\start.wav",winsound.SND_FILENAME|winsound.SND_ASYNC)
		try:
			res=core.main()
 			if not res:
				raise RuntimeError("core crash")
		except:
			winsound.PlaySound("SystemHand",winsound.SND_ALIAS)
			debug.writeException("nvda.pyw executing core.main")
			return False
		winsound.PlaySound("waves\\exit.wav",winsound.SND_FILENAME)
		return True

	def SvcStop(self):
		globalVars.keepAlive=False

if __name__=='__main__':
	win32serviceutil.HandleCommandLine(NVDAService)
