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

import time
import logHandler
import globalVars
from logHandler import log

CORE_INITERROR=0
CORE_MAINLOOPERROR=1
CORE_QUIT=2
CORE_RESTART=3

def resetConfiguration():
	"""Loads the configuration, installs the correct language support and initialises audio so that it will use the configured synth and speech settings.
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
		logLevel=logHandler.levelNames[levelName]
		log.setLevel(logLevel)
	except:
		log.warning("could not set logging to %s"%levelName)
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
	except:
		pass
	log.info("Reverted to saved configuration")

def main():
	"""NVDA's core main loop.
This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI. Then it initialises the wx application object and installs the core pump timer, which checks the queues and executes functions every 1 ms. Finally, it starts the wx main loop.
"""
	log.debug("Core starting")
	log.info("Using Python version %s"%sys.version)
	endResult=CORE_QUIT
	try:
		log.debug("loading config")
		import config
		config.load()
		log.debug("Trying to save config")
		try:
			config.save()
		except:
			pass
		if globalVars.appArgs.logLevel==0:
			levelName=config.conf["general"]["loggingLevel"].upper()
			try:
				logLevel=logHandler.levelNames[levelName]
				log.setLevel(logLevel)
			except:
				log.warning("could not set logging to %s"%levelName)
		try:
			lang = config.conf["general"]["language"]
			import languageHandler
			log.debug("setting language to %s"%lang)
			languageHandler.setLanguage(lang)
		except:
			log.warning("Could not set language to %s"%lang)
		log.debug("Creating wx application instance")
		import speechDictHandler
		log.debug("Speech Dictionary processing")
		speechDictHandler.initialize()
		import speech
		log.debug("Initializing speech")
		speech.initialize()
		if not globalVars.appArgs.minimal and (time.time()-globalVars.startTime)>5:
			log.debugWarning("Slow starting core (%.2f sec)" % (time.time()-globalVars.startTime))
			speech.speakMessage(_("Loading subsystems, please wait..."))
		import wx
		log.info("Using wx version %s"%wx.version())
		app = wx.App(redirect=False)
		import NVDAHelper
		log.debug("Initializing NVDAHelper")
		NVDAHelper.initialize()
		log.debug("Initializing GUI")
		import gui
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
		import appModuleHandler
		log.debug("Initializing appModule Handler")
		appModuleHandler.initialize()
		import JABHandler
		log.debug("initializing Java Access Bridge support")
		JABHandler.initialize()
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
		import queueHandler
		log.info("Using comtypes version %s"%comtypes.__version__)
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
		log.error("Loose focus error",exc_info=True)
	try:
		speech.cancelSpeech()
	except:
		pass
	log.debug("Cleaning up running virtualBuffers")
	try:
		import virtualBufferHandler
		virtualBufferHandler.cleanupVirtualBuffers()
	except:
		log.error("Error cleaning up virtualBuffers",exc_info=True)
	log.debug("Terminating IAccessible support")
	try:
		IAccessibleHandler.terminate()
	except:
		log.error("Error terminating IAccessible support",exc_info=True)
	log.debug("Terminating Java Access Bridge support")
	try:
		JABHandler.terminate()
	except:
		log.error("Error terminating Java Access Bridge support",exc_info=True)
	log.debug("Terminating NVDAHelper")
	try:
		NVDAHelper.terminate()
	except:
		log.error("Error terminating NVDAHelper",exc_info=True)
	log.debug("Terminating keyboard handler")
	try:
		keyboardHandler.terminate()
	except:
		log.error("Error terminating keyboard handler")
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
