#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2008 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA core"""

# Do this first to initialise comtypes.client.gen_dir and the comtypes.gen search path.
import comtypes.client
# Append our comInterfaces directory to the comtypes.gen search path.
import comtypes.gen
import comInterfaces
comtypes.gen.__path__.append(comInterfaces.__path__[0])

import sys
import nvwave
import os
import time
import logHandler
import globalVars
from logHandler import log

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
	logHandler.setLogLevelFromConfig()
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
	log.info("Config dir: %s"%os.path.abspath(globalVars.appArgs.configPath))
	log.debug("loading config")
	import config
	config.load()
	if not globalVars.appArgs.minimal:
		nvwave.playWaveFile("waves\\start.wav")
	log.debug("Trying to save config")
	try:
		config.save()
	except:
		pass
	logHandler.setLogLevelFromConfig()
	try:
		lang = config.conf["general"]["language"]
		import languageHandler
		log.debug("setting language to %s"%lang)
		languageHandler.setLanguage(lang)
	except:
		log.warning("Could not set language to %s"%lang)
	import versionInfo
	log.info("NVDA version %s" % versionInfo.version)
	log.info("Using Windows version %r" % (sys.getwindowsversion(),))
	log.info("Using Python version %s"%sys.version)
	log.info("Using comtypes version %s"%comtypes.__version__)
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
	# HACK: wx currently raises spurious assertion failures when a timer is stopped but there is already an event in the queue for that timer.
	# Unfortunately, these assertion exceptions are raised in the middle of other code, which causes problems.
	# Therefore, disable assertions for now.
	app.SetAssertMode(wx.PYAPP_ASSERT_SUPPRESS)
	# We do support QueryEndSession events, but we don't want to do anything for them.
	app.Bind(wx.EVT_QUERY_END_SESSION, lambda evt: None)
	def onEndSession(evt):
		# NVDA will be terminated as soon as this function returns, so save configuration if appropriate.
		config.saveOnExit()
		if not globalVars.appArgs.minimal:
			nvwave.playWaveFile("waves\\exit.wav",async=False)
		log.info("Windows session ending")
	app.Bind(wx.EVT_END_SESSION, onEndSession)
	import braille
	log.debug("Initializing braille")
	braille.initialize()
	import NVDAHelper
	log.debug("Initializing NVDAHelper")
	NVDAHelper.initialize()
	log.debug("Initializing GUI")
	import gui
	gui.initialize()
	# initialize wxpython localization support
	locale = wx.Locale()
	lang=languageHandler.getLanguage()
	if '_' in lang:
		wxLang=lang.split('_')[0]
	else:
		wxLang=lang
	if hasattr(sys,'frozen'):
		locale.AddCatalogLookupPathPrefix(os.path.join(os.getcwdu(),"locale"))
	try:
		locale.Init(lang,wxLang)
	except:
		pass
	import api
	import winUser
	import NVDAObjects.window
	desktopObject=NVDAObjects.window.Window(windowHandle=winUser.getDesktopWindow())
	api.setDesktopObject(desktopObject)
	api.setFocusObject(desktopObject)
	api.setNavigatorObject(desktopObject)
	api.setMouseObject(desktopObject)
	import appModuleHandler
	log.debug("Initializing appModule Handler")
	appModuleHandler.initialize()
	import JABHandler
	log.debug("initializing Java Access Bridge support")
	JABHandler.initialize()
	import IAccessibleHandler
	log.debug("Initializing IAccessible support")
	IAccessibleHandler.initialize()
	import UIAHandler
	log.debug("Initializing UIA support")
	UIAHandler.initialize()
	import keyboardHandler
	log.debug("Initializing keyboard handler")
	keyboardHandler.initialize()
	import mouseHandler
	log.debug("initializing mouse handler")
	mouseHandler.initialize()
	if not globalVars.appArgs.minimal:
		if config.conf["general"]["showWelcomeDialogAtStartup"]:
			wx.CallAfter(gui.WelcomeDialog.run)
		else:
			import ui
			braille.handler.message(_("NVDA started"))
	if api.getFocusObject()==api.getDesktopObject():
		focusObject=api.getDesktopObject().objectWithFocus()
		import eventHandler
		eventHandler.queueEvent('gainFocus',focusObject)
	import queueHandler
	class CorePump(wx.Timer):
		"Checks the queues and executes functions."
		def __init__(self,*args,**kwargs):
			log.debug("Core pump starting")
			super(CorePump,self).__init__(*args,**kwargs)
		def Notify(self):
			try:
				JABHandler.pumpAll()
				IAccessibleHandler.pumpAll()
				queueHandler.pumpAll()
				mouseHandler.pumpAll()
			except:
				log.error("errors in this core pump cycle",exc_info=True)
	log.debug("starting core pump")
	pump = CorePump()
	pump.Start(1)
	log.info("NVDA initialized")

	log.debug("entering wx application main loop")
	app.MainLoop()

	log.info("Exiting")
	log.debug("Terminating GUI")
	gui.terminate()
	config.saveOnExit()
	try:
		if globalVars.focusObject and hasattr(globalVars.focusObject,"event_loseFocus"):
			log.debug("calling lose focus on object with focus")
			globalVars.focusObject.event_loseFocus()
	except:
		log.error("Lose focus error",exc_info=True)
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
	log.debug("Terminating UIA support")
	try:
		UIAHandler.terminate()
	except:
		log.error("Error terminating UIA support",exc_info=True)
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
	log.debug("Terminating braille")
	try:
		braille.terminate()
	except:
		log.error("Error terminating braille",exc_info=True)
	log.debug("Terminating speech")
	try:
		speech.terminate()
	except:
		log.error("Error terminating speech",exc_info=True)
	if not globalVars.appArgs.minimal:
		nvwave.playWaveFile("waves\\exit.wav",async=False)
	log.debug("core done")
