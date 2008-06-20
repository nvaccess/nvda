#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA core"""

#Bit of a dance to force comtypes generated interfaces in to our directory
import comtypes.client
comtypes.client.gen_dir='.\\comInterfaces'
import sys
sys.modules['comtypes.gen']=comtypes.gen=__import__("comInterfaces",globals(),locals(),[])

import wx
import time
import logging
import globalVars
from logHandler import log

CORE_INITERROR=0
CORE_MAINLOOPERROR=1
CORE_QUIT=2
CORE_RESTART=3

def resetConfiguration(reportDone=False):
	"""Loads the configuration, installs the correct language support and initialises audio so that it will use the configured synth and speech settings.
@param reportDone: if true then this function will speak when done, if else it won't.
@type reportDone: boolean
"""
	import config
	import speech
	import languageHandler
	log.debug("terminating speech")
	speech.terminate()
	log.debug("Reloading config")
	config.load()
	#Logging
	levelName=config.conf["general"]["loggingLevel"].upper()
	try:
		logLevel=logging._levelNames[levelName]
		log.setLevel(logLevel)
	except:
		log.warning("could not set logging to %s"%levelName,exc_info=True)
	#Language
	lang = config.conf["general"]["language"]
	log.debug("setting language to %s"%lang)
	languageHandler.setLanguage(lang)
	#Speech
	log.debug("initializing speech")
	speech.initialize()
	log.debug("Trying to save config...")
	try:
		config.save()
		log.debug("config save successfull")
	except:
		pass
	log.info("Reverted to saved configuration")
	if reportDone:
		log.debug("Reporting success to user")
		speech.speakMessage(_("configuration applied"),wait=True)

def main():
	"""NVDA's core main loop.
This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI. Then it initialises the wx application object and installs the core pump timer, which checks the queues and executes functions every 1 ms. Finally, it starts the wx main loop.
"""
	log.debug("Core starting")
	endResult=CORE_QUIT
	try:
		log.debug("loading config")
		import config
		config.load()
		log.debug("Trying to save config")
		try:
			config.save()
			log.debug("save config successfull")
		except:
			pass
		if globalVars.appArgs.logLevel==0:
			levelName=config.conf["general"]["loggingLevel"].upper()
			try:
				logLevel=logging._levelNames[levelName]
				log.setLevel(logLevel)
			except:
				log.warning("could not set logging to %s"%levelName,exc_info=True)
		try:
			lang = config.conf["general"]["language"]
			import languageHandler
			log.debug("setting language to %s"%lang)
			languageHandler.setLanguage(lang)
		except:
			log.warning("Could not set language to %s"%lang)
		log.debug("Creating wx application instance")
		app = wx.App(redirect=False)
		import queueHandler
		import gui
		log.debug("Initializing GUI")
		gui.initialize(app)
		# initialize wxpython localization support
		locale = wx.Locale()
		lang=languageHandler.getLanguage()
		if '_' in lang:
			wxLang=lang.split('_')[0]
		else:
			wxLang=lang
		try:
			locale.Init(lang,wxLang)
		except:
			pass
		import speechDictHandler
		log.debug("Speech Dictionary processing")
		speechDictHandler.initialize()
		import speech
		log.debug("Initializing speech")
		speech.initialize()
		if not globalVars.appArgs.minimal and (time.time()-globalVars.startTime)>2:
			log.warn("Slow starting core")
			speech.speakMessage(_("Loading subsystems, please wait..."))
		import appModuleHandler
		log.debug("Initializing appModule Handler")
		appModuleHandler.initialize()
		import JABHandler
		log.debug("initializing Java Access Bridge support")
		JABHandler.initialize()
		import charHook
		log.debug("Initializing charHook")
		charHook.initialize()
		import IAccessibleHandler
		log.debug("Initializing IAccessible support")
		IAccessibleHandler.initialize()
		import keyboardHandler
		log.debug("Initializing keyboard handler")
		keyboardHandler.initialize()
		import mouseHandler
		log.debug("initializing mouse handler")
		mouseHandler.initialize()
		speech.cancelSpeech()
		if not globalVars.appArgs.minimal:
			speech.speakMessage(_("NVDA started"))
			speech.speakMessage(_("You can press insert+n to activate the NVDA menu at any time"))

		class CorePump(wx.Timer):
			"Checks the queues and executes functions."
			def __init__(self,*args,**kwargs):
				log.debug("Core pump starting")
				super(CorePump,self).__init__(*args,**kwargs)
			def Notify(self):
				try:
					IAccessibleHandler.pumpAll()
					queueHandler.pumpAll()
					mouseHandler.pumpAll()
				except:
					log.error("errors in this core pump cycle",exc_info=True)
		log.debug("starting core pump")
		pump = CorePump()
		pump.Start(1)
	except:
		log.critical("Core initialization error",exc_info=True)
		return CORE_INITERROR
	log.info("NVDA initialized")
	log.debug("entering wx application main loop")
	app.MainLoop()
	log.debug("Shutting down core")
	try:
		if globalVars.focusObject and hasattr(globalVars.focusObject,"event_looseFocus"):
			log.debug("calling loose focus on object with focus")
			globalVars.focusObject.event_looseFocus()
	except:
		log.warn("Loose focus error",exc_info=True)
	try:
		speech.cancelSpeech()
	except:
		pass
	log.debug("Cleaning up running virtualBuffers")
	try:
		import virtualBufferHandler
		virtualBufferHandler.cleanupVirtualBuffers()
	except:
		log.warn("Error cleaning up virtualBuffers",exc_info=True)
	log.debug("Terminating IAccessible support")
	try:
		IAccessibleHandler.terminate()
	except:
		log.warn("Error terminating IAccessible support",exc_info=True)
	log.debug("Terminating Java Access Bridge support")
	try:
		JABHandler.terminate()
	except:
		log.warn("Error terminating Java Access Bridge support",exc_info=True)
	log.debug("Terminating charHook")
	try:
		charHook.terminate()
	except:
		log.warn("Error terminating charHook",exc_info=True)
	log.debug("Terminating keyboard handler")
	try:
		keyboardHandler.terminate()
	except:
		log.warn("Error terminating keyboard handler")
	log.debug("Terminating mouse handler")
	try:
		mouseHandler.terminate()
	except:
		log.error("error terminating mouse handler",exc_info=True)
	log.debug("Terminating speech")
	try:
		speech.terminate()
	except:
		log.error("Error terminating speech",exc_info=True)
	if endResult==CORE_QUIT and globalVars.restart:
		globalVars.restart=False
		endResult=CORE_RESTART
	log.debug("Core done, return code %d"%endResult)
	return endResult
