#appModules/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import os.path
import debug
import audio

current=None

def load(name):
	global current
	if os.path.isfile(r'%s\appModules\%s.py'%(os.getcwd(),name)):
		try:
			current=__import__(name,globals(),None,[]).appModule()
			debug.writeMessage("Loaded appModule %s"%name)
			return True
		except:
			debug.writeException("Error in appModule %s"%name)
			audio.speakMessage("Error in appModule %s"%name,wait=True)
	if os.path.isfile(r'%s\appModules\_default.py'%os.getcwd()):
		try:
			current=__import__("_default",globals(),None,[]).appModule()
			debug.writeMessage("Loaded appModule _default")
			return True
		except:
			debug.writeException("Error in appModule _default")
			audio.speakMessage("Error in appModule _default") 
			raise ImportError
	else:
		audio.speakMessage("Error: no _default appModule")
		debug.writeError("_default appModule does not exist")
		raise ImportError

