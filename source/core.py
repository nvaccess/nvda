#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import ctypes
import time
import NVDAThreads
import lang
import globalVars
import winUser
from api import *
from constants import *
import NVDAObjects
import keyboardHandler
import mouseHandler
import MSAAHandler
import appModuleHandler
import audio
import config
import gui

msg=winUser.msgType()

def main():
	try:
		audio.initialize()
		audio.speakMessage("NonVisual Desktop Acces started!",wait=True)
		NVDAThreads.pump() #Need this cause haven't reached the main loop yet
		foregroundWindow=winUser.getForegroundWindow()
		if foregroundWindow==0:
			foregroundWindow=winUser.getDesktopWindow()
		setForegroundObjectByLocator(foregroundWindow,-4,0)
		setFocusObjectByLocator(foregroundWindow,-4,0)
		executeEvent("foreground",foregroundWindow,-4,0)
		MSAAHandler.initialize()
		keyboardHandler.initialize()
		mouseHandler.initialize()
		gui.initialize()
	except:
		debug.writeException("core.py main init")
		try:
			gui.abort()
		except:
			pass
		return False
	try:
		globalVars.stayAlive=True
		while globalVars.stayAlive is True:
			NVDAThreads.pump()
			if winUser.peekMessage(ctypes.byref(msg),0,0,0,1):
				winUser.translateMessage(ctypes.byref(msg))
				winUser.dispatchMessage(ctypes.byref(msg))
			time.sleep(0.001)
	except:
		debug.writeException("core.py main loop")
		audio.speakMessage("Exception in main loop")
		try:
			gui.abort()
		except:
			pass
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		globalVars.focusObject.event_looseFocus()
	MSAAHandler.terminate()
	return True
