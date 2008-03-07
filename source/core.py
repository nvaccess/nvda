#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA core"""

#Bit of a dance to force comtypes generated interfaces in to our directory
import comtypes.client
comtypes.client.gen_dir='.\\comInterfaces'
import comtypes
import sys
sys.modules['comtypes.gen']=comtypes.gen=__import__("comInterfaces",globals(),locals(),[])

import wx
import time
import logging
import globalVars
import winUser

CORE_INITERROR=0
CORE_MAINLOOPERROR=1
CORE_QUIT=2
CORE_RESTART=3

def quit():
	"""
Instructs the GUI that you want to quit. The GUI responds by bringing up a dialog asking you if you want to exit.
"""
	globalVars.log.debug("Calling gui.quit")
	gui.quit()

def resetConfiguration(reportDone=False):
	"""Loads the configuration, installs the correct language support and initialises audio so that it will use the configured synth and speech settings.
@param reportDone: if true then this function will speak when done, if else it won't.
@type reportDone: boolean
"""
	import config
	import speech
	import languageHandler
	globalVars.log.debug("terminating speech")
	speech.terminate()
	globalVars.log.debug("Reloading config")
	config.load()
	#Logging
	levelName=config.conf["general"]["loggingLevel"].upper()
	try:
		logLevel=logging._levelNames[levelName]
		globalVars.log.setLevel(logLevel)
	except:
		globalVars.log.warning("could not set logging to %s"%levelName,exc_info=True)
	#Language
	lang = config.conf["general"]["language"]
	globalVars.log.debug("setting language to %s"%lang)
	languageHandler.setLanguage(lang)
	#Speech
	globalVars.log.debug("initializing speech")
	speech.initialize()
	globalVars.log.debug("Trying to save config...")
	try:
		config.save()
		globalVars.log.debug("config save successfull")
	except:
		pass
	globalVars.log.info("Reverted to saved configuration")
	if reportDone:
		globalVars.log.debug("Reporting success to user")
		speech.speakMessage(_("configuration applied"),wait=True)

def main():
	"""NVDA's core main loop.
This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI. Then it initialises the wx application object and installs the core pump timer, which checks the queues and executes functions every 1 ms. Finally, it starts the wx main loop.
"""
	globalVars.log.debug("Core starting")
	endResult=CORE_QUIT
	try:
		globalVars.log.debug("loading config")
		import config
		config.load()
		globalVars.log.debug("Trying to save config")
		try:
			config.save()
			globalVars.log.debug("save config successfull")
		except:
			pass
		if globalVars.appArgs.logLevel==0:
			levelName=config.conf["general"]["loggingLevel"].upper()
			try:
				logLevel=logging._levelNames[levelName]
				globalVars.log.setLevel(logLevel)
			except:
				globalVars.log.warning("could not set logging to %s"%levelName,exc_info=True)
		try:
			lang = config.conf["general"]["language"]
			import languageHandler
			globalVars.log.debug("setting language to %s"%lang)
			languageHandler.setLanguage(lang)
		except:
			globalVars.log.warning("Could not set language to %s"%lang)
		globalVars.log.debug("Creating wx application instance")
		app = wx.App()
		import queueHandler
		import gui
		globalVars.log.debug("Initializing GUI")
		gui.initialize(app)
		import userDictHandler
		globalVars.log.debug("User Dictionary processing")
		userDictHandler.initialize()
		import speech
		globalVars.log.debug("Initializing speech")
		speech.initialize()
		if not globalVars.appArgs.minimal and (time.time()-globalVars.startTime)>2:
			globalVars.log.warn("Slow starting core")
			speech.speakMessage(_("Loading subsystems, please wait..."))
		import appModuleHandler
		globalVars.log.debug("Initializing appModule Handler")
		appModuleHandler.initialize()
		import JABHandler
		globalVars.log.debug("initializing Java Access Bridge support")
		JABHandler.initialize()
		import charHook
		globalVars.log.debug("Initializing charHook")
		charHook.initialize()
		import IAccessibleHandler
		globalVars.log.debug("Initializing IAccessible support")
		IAccessibleHandler.initialize()
		import keyboardHandler
		globalVars.log.debug("Initializing keyboard handler")
		keyboardHandler.initialize()
		import mouseHandler
		globalVars.log.debug("initializing mouse handler")
		mouseHandler.initialize()
		speech.cancelSpeech()
		if not globalVars.appArgs.minimal:
			speech.speakMessage(_("NVDA started"),wait=True)
			speech.speakMessage(_("You can press insert+n to activate the NVDA menu at any time"),wait=True)

		class CorePump(wx.Timer):
			"Checks the queues and executes functions."
			def __init__(self,*args,**kwargs):
				globalVars.log.debug("Core pump starting")
				wx.Timer.__init__(self,*args,**kwargs)
			def Notify(self):
				try:
					queueHandler.pumpAll()
					IAccessibleHandler.pumpAll()
					mouseHandler.pumpAll()
				except:
					globalVars.log.error("errors in this core pump cycle",exc_info=True)
		globalVars.log.debug("starting core pump")
		pump = CorePump()
		pump.Start(1)
	except:
		globalVars.log.critical("Core initialization error",exc_info=True)
		return CORE_INITERROR
	globalVars.log.info("NVDA initialized")
	globalVars.log.debug("entering wx application main loop")
	res=app.MainLoop()
	if res is not None and res is not 0:
		globalVars.log.critical("wx application main loop stopped with errors, returned %s"%res)
		endResult=CORE_MAINLOOPERROR
	globalVars.log.debug("Shutting down core")
	try:
		if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
			globalVars.log.debug("calling loose focus on object with focus")
			globalVars.focusObject.event_looseFocus()
	except:
		globalVars.log.warn("Loose focus error",exc_info=True)
	try:
		speech.cancelSpeech()
	except:
		pass
	globalVars.log.debug("Terminating IAccessible support")
	try:
		IAccessibleHandler.terminate()
	except:
		globalVars.log.warn("Error terminating IAccessible support",exc_info=True)
	globalVars.log.debug("Terminating Java Access Bridge support")
	try:
		JABHandler.terminate()
	except:
		globalVars.log.warn("Error terminating Java Access Bridge support",exc_info=True)
	globalVars.log.debug("Terminating charHook")
	try:
		charHook.terminate()
	except:
		globalVars.log.warn("Error terminating charHook",exc_info=True)
	globalVars.log.debug("Terminating keyboard handler")
	try:
		keyboardHandler.terminate()
	except:
		globalVars.log.warn("Error terminating keyboard handler")
	globalVars.log.debug("Terminating mouse handler")
	try:
		mouseHandler.terminate()
	except:
		globalVars.log.error("error terminating mouse handler",exc_info=True)
	globalVars.log.debug("Terminating speech")
	try:
		speech.terminate()
	except:
		globalVars.log.error("Error terminating speech",exc_info=True)
	if endResult==CORE_QUIT and globalVars.restart:
		globalVars.restart=False
		endResult=CORE_RESTART
	globalVars.log.debug("Core done, return code %d"%endResult)
	return endResult
