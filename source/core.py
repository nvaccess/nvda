#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA core"""

import pythoncom
import time
import debug
import globalVars
import winUser
import audio
import config
import languageHandler

def quit():
	"""
Instructs the GUI that you want to quit. The GUI responds by bringing up a dialog asking you if you want to exit.
"""
	gui.quit()

def applyConfiguration(reportDone=False):
	"""Loads the configuration, installs the correct language support and initialises audio so that it will use the configured synth and speech settings.
@param reportDone: if true then this function will speak when done, if else it won't.
@type reportDone: boolean
"""
	config.load()
	#Language
	lang = config.conf["general"]["language"]
	languageHandler.setLanguage(lang)
	#Speech
	audio.initialize()
	config.save()
	debug.writeMessage("core.applyConfiguration: configuration applyed")
	if reportDone:
		audio.speakMessage(_("configuration applyed"))

def main():
	"""NVDA's core main loop. This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI. Then it loops continuously, checking the queues and executing functions, plus pumping window messages, and sleeping when possible.
"""
	try:
		applyConfiguration()
		audio.initialize()
		if (time.time()-globalVars.startTime)>2:
			audio.speakMessage(_("Loading subsystems, please wait..."))
		import gui
		gui.initialize()
		import appModuleHandler
		appModuleHandler.initialize()
		import IAccessibleHandler
		IAccessibleHandler.initialize()
		import keyboardHandler
		keyboardHandler.initialize()
		import mouseHandler
		mouseHandler.initialize()
		import queueHandler
		audio.cancel()
		config.save()
		audio.speakMessage(_("NVDA started"),wait=True)
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
			gui.pumpLock.acquire()
			pythoncom.PumpWaitingMessages()
			gui.pumpLock.release()
			debug.writeMessage("queue start")
			queueHandler.pumpAll()
			debug.writeMessage("queue end")
			if not queueHandler.isPendingItems(): 
				time.sleep(0.001)
	except:
		debug.writeException("core.py main loop")
		try:
			gui.abort()
		except:
			pass
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		globalVars.focusObject.event_looseFocus()
	IAccessibleHandler.terminate()
	audio.cancel()
	return True
