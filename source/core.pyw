#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

#Initial logging and debugging code
import sys
stderrFile=open("stderr.log","w")
if stderrFile is None:
	sys.exit()
sys.stderr=stderrFile
import debug
debug.start("debug.log")

import os
import time
import Queue
import win32api
import win32gui
import pythoncom
import cPickle
from constants import *
import dictionaries
import globalVars
from api import *
import keyEventHandler
import mouseEventHandler
import MSAAEventHandler
import appModules
import audio
import config
import gui

def event_appChange(window,objectID,childID):
	accObject=getObjectFromEvent(window,objectID,childID)
	if accObject is None:
		debug.writeError("core.event_appChange: failed to get object from window %d, object ID %d, child ID %d"%(window,objectID,childID))
		return None
	name=getObjectName(accObject)
	#className=getObjectClass(accObject)
	appName = os.path.splitext(getProcessName(getObjectProcessID(accObject)))[0].lower()
	role=getObjectRole(accObject)
	if appModules.load(appName) is False:
		debug.writeError("core.event_appChange(): Error, could not load app module %s"%appName) 
		sys.exit()
	appModules.current.event_foreground(window,objectID,childID)

def quit():
	audio.speakMessage("Exiting NVDA",wait=True)
	gui.terminate()
	try:
		config.save()
	except:
		pass
	MSAAEventHandler.terminate()
	sys.exit()

def main():
	dictionaries.load("characterSymbols")
	dictionaries.load("textSymbols")
	dictionaries.load("roleNames")
	dictionaries.load("stateNames")
	audio.initialize()
	audio.speakMessage("NonVisual Desktop Acces started!")
	foregroundWindow=getForegroundWindow()
	if (foregroundWindow is None) or (foregroundWindow==0):
		debug.writeError("core.main: failed to get foreground window")
		sys.exit()
	event_appChange(foregroundWindow,-4,0)
	MSAAEventHandler.initialize()
	keyEventHandler.initialize()
	mouseEventHandler.initialize()
	gui.initialize()
	globalVars.stayAlive=True
	while globalVars.stayAlive:
		try:
			pythoncom.PumpWaitingMessages()
		except KeyboardInterrupt:
			debug.writeException("core.main: keyboard interupt") 
			quit()
		try:
			keyPress=keyEventHandler.queue_keys.get_nowait()
			if keyPress == (None, "SilenceSpeech"):
				audio.cancel()
			else:
				try:
					appModules.current.keyMap[keyPress](keyPress)
				except:
					audio.speakMessage("Error executing function "+appModules.current.keyMap[keyPress].__name__)
					debug.writeException("while executing function %s bound to key set %s " %
					 (appModules.current.keyMap[keyPress].__name__,str(keyPress)))
		except Queue.Empty:
			pass
		try:
			mouseEvent=mouseEventHandler.queue_events.get_nowait()
			if appModules.current.__dict__.has_key("event_%s"%mouseEvent[0]):
				try:
					appModules.current.__dict__["event_%s"%mouseEvent[0]](mouseEvent[1])
				except:
					debug.writeException("core.main: while executing event_%s in app module"%mouseEvent[0])
			else:
				debug.writeError("core.py: unknown event '%s'"%mouseEvent[0])
		except Queue.Empty:
			pass
		try:
			MSAAEvent=MSAAEventHandler.queue_events.get_nowait()
			if MSAAEvent[0]=="appChange":
				event_appChange(MSAAEvent[1],MSAAEvent[2],MSAAEvent[3])
			elif appModules.current.__dict__.has_key("event_%s"%MSAAEvent[0]):
				try:
					appModules.current.__dict__["event_%s"%MSAAEvent[0]](MSAAEvent[1],MSAAEvent[2],MSAAEvent[3])
				except:
					debug.writeException("core.main: while executing event_%s in app module"%MSAAEvent[0])
			else:
				debug.writeError("core.py: unknown event '%s'"%MSAAEvent[0])
		except Queue.Empty:
			pass
		# If there are no events already waiting, sleep to avoid needlessly hogging the CPU.
		if keyEventHandler.queue_keys.empty() and mouseEventHandler.queue_events.empty() and MSAAEventHandler.queue_events.empty():
			time.sleep(0.001)
	quit()

main()
