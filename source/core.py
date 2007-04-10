#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA core"""

import wx
import time
import debug
import globalVars
import winUser
import speech
import config
import queueHandler
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
	#lang = config.conf["general"]["language"]
	#languageHandler.setLanguage(lang)
	#Speech
	speech.initialize()
	try:
		config.save()
	except:
		pass
	debug.writeMessage("core.applyConfiguration: configuration applyed")
	if reportDone:
		speech.speakMessage(_("configuration applyed"),wait=True)

def main():
	"""NVDA's core main loop.
This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI. Then it initialises the wx application object and installs the core pump timer, which checks the queues and executes functions every 1 ms. Finally, it starts the wx main loop.
"""
	try:
		applyConfiguration()
		speech.initialize()
		if not globalVars.appArgs.minimal and (time.time()-globalVars.startTime)>2:
			speech.speakMessage(_("Loading subsystems, please wait..."))
		import gui
		import appModuleHandler
		appModuleHandler.initialize()
		import JABHandler
		JABHandler.initialize()
		import IAccessibleHandler
		IAccessibleHandler.initialize()
		import keyboardHandler
		keyboardHandler.initialize()
		import mouseHandler
		mouseHandler.initialize()
		speech.cancelSpeech()
		try:
			config.save()
		except:
			pass
		if not globalVars.appArgs.minimal:
			speech.speakMessage(_("NVDA started"),wait=True)
	except:
		debug.writeException("core.py main init")
		return False
	app = wx.PySimpleApp()
	gui.initialize(app)
	pump = CorePump()
	pump.Start(1)
	try:
		app.MainLoop()
	except:
		debug.writeException("core.py main loop")
		return False
	if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
		globalVars.focusObject.event_looseFocus()
	IAccessibleHandler.terminate()
	speech.cancelSpeech()
	return True

class CorePump(wx.Timer):
	"Checks the queues and executes functions."

	def Notify(self):
		while True:
			queueHandler.pumpAll()
			if not queueHandler.isPendingItems():
				break
