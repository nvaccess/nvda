# -*- coding: UTF-8 -*-
#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited, Aleksey Sadovoy, Christopher Toth, Joseph Lee, Peter Vágner
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""NVDA core"""

# Do this first to initialise comtypes.client.gen_dir and the comtypes.gen search path.
import comtypes.client
# Append our comInterfaces directory to the comtypes.gen search path.
import comtypes.gen
import comInterfaces
comtypes.gen.__path__.append(comInterfaces.__path__[0])

#Apply several monky patches to comtypes
import comtypesMonkeyPatches

import sys
import winVersion
import thread
import nvwave
import os
import time
import ctypes
import logHandler
import globalVars
from logHandler import log
import addonHandler

PUMP_MAX_DELAY = 10

#: The thread identifier of the main thread.
mainThreadId = thread.get_ident()

_pump = None
_isPumpPending = False

def doStartupDialogs():
	import config
	import gui
	# Translators: The title of the dialog to tell users that there are erros in the configuration file.
	if config.conf.baseConfigError:
		import wx
		gui.messageBox(
			# Translators: A message informing the user that there are errors in the configuration file.
			_("Your configuration file contains errors. "
				"Your configuration has been reset to factory defaults.\n"
				"More details about the errors can be found in the log file."),
			# Translators: The title of the dialog to tell users that there are errors in the configuration file.
			_("Configuration File Error"),
			wx.OK | wx.ICON_EXCLAMATION)
	if config.conf["general"]["showWelcomeDialogAtStartup"]:
		gui.WelcomeDialog.run()
	import inputCore
	if inputCore.manager.userGestureMap.lastUpdateContainedError:
		import wx
		gui.messageBox(_("Your gesture map file contains errors.\n"
				"More details about the errors can be found in the log file."),
			_("gesture map File Error"), wx.OK|wx.ICON_EXCLAMATION)

def restart(disableAddons=False):
	"""Restarts NVDA by starting a new copy with -r."""
	if globalVars.appArgs.launcher:
		import wx
		globalVars.exitCode=3
		wx.GetApp().ExitMainLoop()
		return
	import subprocess
	import winUser
	import shellapi
	options=[]
	if "-r" not in sys.argv:
		options.append("-r")
	try:
		sys.argv.remove('--disable-addons')
	except ValueError:
		pass
	if disableAddons:
		options.append('--disable-addons')
	try:
		sys.argv.remove("--ease-of-access")
	except ValueError:
		pass
	shellapi.ShellExecute(None, None,
		sys.executable.decode("mbcs"),
		subprocess.list2cmdline(sys.argv + options).decode("mbcs"),
		None,
		# #4475: ensure that the first window of the new process is not hidden by providing SW_SHOWNORMAL
		winUser.SW_SHOWNORMAL)

def resetConfiguration(factoryDefaults=False):
	"""Loads the configuration, installs the correct language support and initialises audio so that it will use the configured synth and speech settings.
	"""
	import config
	import braille
	import speech
	import languageHandler
	import inputCore
	log.debug("Terminating braille")
	braille.terminate()
	log.debug("terminating speech")
	speech.terminate()
	log.debug("terminating addonHandler")
	addonHandler.terminate()
	log.debug("Reloading config")
	config.conf.reset(factoryDefaults=factoryDefaults)
	logHandler.setLogLevelFromConfig()
	#Language
	lang = config.conf["general"]["language"]
	log.debug("setting language to %s"%lang)
	languageHandler.setLanguage(lang)
	# Addons
	addonHandler.initialize()
	#Speech
	log.debug("initializing speech")
	speech.initialize()
	#braille
	log.debug("Initializing braille")
	braille.initialize()
	log.debug("Reloading user and locale input gesture maps")
	inputCore.manager.loadUserGestureMap()
	inputCore.manager.loadLocaleGestureMap()
	log.info("Reverted to saved configuration")

def _setInitialFocus():
	"""Sets the initial focus if no focus event was received at startup.
	"""
	import eventHandler
	import api
	if eventHandler.lastQueuedFocusObject:
		# The focus has already been set or a focus event is pending.
		return
	try:
		focus = api.getDesktopObject().objectWithFocus()
		if focus:
			eventHandler.queueEvent('gainFocus', focus)
	except:
		log.exception("Error retrieving initial focus")

def main():
	"""NVDA's core main loop.
This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI. Then it initialises the wx application object and sets up the core pump, which checks the queues and executes functions when requested. Finally, it starts the wx main loop.
"""
	log.debug("Core starting")

	try:
		# Windows >= Vista
		ctypes.windll.user32.SetProcessDPIAware()
	except AttributeError:
		pass

	import config
	if not globalVars.appArgs.configPath:
		globalVars.appArgs.configPath=config.getUserDefaultConfigPath(useInstalledPathIfExists=globalVars.appArgs.launcher)
	#Initialize the config path (make sure it exists)
	config.initConfigPath()
	log.info("Config dir: %s"%os.path.abspath(globalVars.appArgs.configPath))
	log.debug("loading config")
	import config
	config.initialize()
	if not globalVars.appArgs.minimal and config.conf["general"]["playStartAndExitSounds"]:
		try:
			nvwave.playWaveFile("waves\\start.wav")
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
	log.info("Using Windows version %s" % winVersion.winVersionText)
	log.info("Using Python version %s"%sys.version)
	log.info("Using comtypes version %s"%comtypes.__version__)
	# Set a reasonable timeout for any socket connections NVDA makes.
	import socket
	socket.setdefaulttimeout(10)
	log.debug("Initializing addons system.")
	addonHandler.initialize()
	import appModuleHandler
	log.debug("Initializing appModule Handler")
	appModuleHandler.initialize()
	import NVDAHelper
	log.debug("Initializing NVDAHelper")
	NVDAHelper.initialize()
	import speechDictHandler
	log.debug("Speech Dictionary processing")
	speechDictHandler.initialize()
	import speech
	log.debug("Initializing speech")
	speech.initialize()
	if not globalVars.appArgs.minimal and (time.time()-globalVars.startTime)>5:
		log.debugWarning("Slow starting core (%.2f sec)" % (time.time()-globalVars.startTime))
		# Translators: This is spoken when NVDA is starting.
		speech.speakMessage(_("Loading NVDA. Please wait..."))
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
		speech.cancelSpeech()
		if not globalVars.appArgs.minimal and config.conf["general"]["playStartAndExitSounds"]:
			try:
				nvwave.playWaveFile("waves\\exit.wav",async=False)
			except:
				pass
		log.info("Windows session ending")
	app.Bind(wx.EVT_END_SESSION, onEndSession)
	import braille
	log.debug("Initializing braille")
	braille.initialize()
	log.debug("Initializing braille input")
	import brailleInput
	brailleInput.initialize()
	import displayModel
	log.debug("Initializing displayModel")
	displayModel.initialize()
	log.debug("Initializing GUI")
	import gui
	gui.initialize()

	# #3763: In wxPython 3, the class name of frame windows changed from wxWindowClassNR to wxWindowNR.
	# NVDA uses the main frame to check for and quit another instance of NVDA.
	# To remain compatible with older versions of NVDA, create our own wxWindowClassNR.
	# We don't need to do anything else because wx handles WM_QUIT for all windows.
	import windowUtils
	class MessageWindow(windowUtils.CustomWindow):
		className = u"wxWindowClassNR"
	messageWindow = MessageWindow(unicode(versionInfo.name))

	# initialize wxpython localization support
	locale = wx.Locale()
	lang=languageHandler.getLanguage()
	wxLang=locale.FindLanguageInfo(lang)
	if not wxLang and '_' in lang:
		wxLang=locale.FindLanguageInfo(lang.split('_')[0])
	if hasattr(sys,'frozen'):
		locale.AddCatalogLookupPathPrefix(os.path.join(os.getcwdu(),"locale"))
	if wxLang:
		try:
			locale.Init(wxLang.Language)
		except:
			log.error("Failed to initialize wx locale",exc_info=True)
	else:
		log.debugWarning("wx does not support language %s" % lang)

	import api
	import winUser
	import NVDAObjects.window
	desktopObject=NVDAObjects.window.Window(windowHandle=winUser.getDesktopWindow())
	api.setDesktopObject(desktopObject)
	api.setFocusObject(desktopObject)
	api.setNavigatorObject(desktopObject)
	api.setMouseObject(desktopObject)
	import JABHandler
	log.debug("initializing Java Access Bridge support")
	try:
		JABHandler.initialize()
	except NotImplementedError:
		log.warning("Java Access Bridge not available")
	except:
		log.error("Error initializing Java Access Bridge support", exc_info=True)
	import winConsoleHandler
	log.debug("Initializing winConsole support")
	winConsoleHandler.initialize()
	import UIAHandler
	log.debug("Initializing UIA support")
	try:
		UIAHandler.initialize()
	except NotImplementedError:
		log.warning("UIA not available")
	except:
		log.error("Error initializing UIA support", exc_info=True)
	import IAccessibleHandler
	log.debug("Initializing IAccessible support")
	IAccessibleHandler.initialize()
	log.debug("Initializing input core")
	import inputCore
	inputCore.initialize()
	import keyboardHandler
	log.debug("Initializing keyboard handler")
	keyboardHandler.initialize()
	import mouseHandler
	log.debug("initializing mouse handler")
	mouseHandler.initialize()
	import touchHandler
	log.debug("Initializing touchHandler")
	try:
		touchHandler.initialize()
	except NotImplementedError:
		pass
	import globalPluginHandler
	log.debug("Initializing global plugin handler")
	globalPluginHandler.initialize()
	if globalVars.appArgs.install or globalVars.appArgs.installSilent:
		import wx
		import gui.installerGui
		wx.CallAfter(gui.installerGui.doSilentInstall,startAfterInstall=not globalVars.appArgs.installSilent)
	elif not globalVars.appArgs.minimal:
		try:
			# Translators: This is shown on a braille display (if one is connected) when NVDA starts.
			braille.handler.message(_("NVDA started"))
		except:
			log.error("", exc_info=True)
		if globalVars.appArgs.launcher:
			gui.LauncherDialog.run()
			# LauncherDialog will call doStartupDialogs() afterwards if required.
		else:
			wx.CallAfter(doStartupDialogs)
	import queueHandler
	# Queue the handling of initial focus,
	# as API handlers might need to be pumped to get the first focus event.
	queueHandler.queueFunction(queueHandler.eventQueue, _setInitialFocus)
	import watchdog
	import baseObject

	# Doing this here is a bit ugly, but we don't want these modules imported
	# at module level, including wx.
	log.debug("Initializing core pump")
	class CorePump(wx.Timer):
		"Checks the queues and executes functions."
		def Notify(self):
			global _isPumpPending
			_isPumpPending = False
			watchdog.alive()
			try:
				if touchHandler.handler:
					touchHandler.handler.pump()
				JABHandler.pumpAll()
				IAccessibleHandler.pumpAll()
				queueHandler.pumpAll()
				mouseHandler.pumpAll()
				braille.pumpAll()
			except:
				log.exception("errors in this core pump cycle")
			baseObject.AutoPropertyObject.invalidateCaches()
			watchdog.asleep()
			if _isPumpPending and not _pump.IsRunning():
				# #3803: A pump was requested, but the timer was ignored by a modal loop
				# because timers aren't re-entrant.
				# Therefore, schedule another pump.
				_pump.Start(PUMP_MAX_DELAY, True)
	global _pump
	_pump = CorePump()
	requestPump()

	log.debug("Initializing watchdog")
	watchdog.initialize()
	try:
		import updateCheck
	except RuntimeError:
		updateCheck=None
		log.debug("Update checking not supported")
	else:
		log.debug("initializing updateCheck")
		updateCheck.initialize()
	log.info("NVDA initialized")

	log.debug("entering wx application main loop")
	app.MainLoop()

	log.info("Exiting")
	if updateCheck:
		_terminate(updateCheck)

	_terminate(watchdog)
	_terminate(globalPluginHandler, name="global plugin handler")
	_terminate(gui)
	config.saveOnExit()

	try:
		if globalVars.focusObject and hasattr(globalVars.focusObject,"event_loseFocus"):
			log.debug("calling lose focus on object with focus")
			globalVars.focusObject.event_loseFocus()
	except:
		log.exception("Lose focus error")
	try:
		speech.cancelSpeech()
	except:
		pass

	import treeInterceptorHandler
	_terminate(treeInterceptorHandler)
	_terminate(IAccessibleHandler, name="IAccessible support")
	_terminate(UIAHandler, name="UIA support")
	_terminate(winConsoleHandler, name="winConsole support")
	_terminate(JABHandler, name="Java Access Bridge support")
	_terminate(appModuleHandler, name="app module handler")
	_terminate(NVDAHelper)
	_terminate(touchHandler)
	_terminate(keyboardHandler, name="keyboard handler")
	_terminate(mouseHandler)
	_terminate(inputCore)
	_terminate(brailleInput)
	_terminate(braille)
	_terminate(speech)
	_terminate(addonHandler)

	if not globalVars.appArgs.minimal and config.conf["general"]["playStartAndExitSounds"]:
		try:
			nvwave.playWaveFile("waves\\exit.wav",async=False)
		except:
			pass
	# #5189: Destroy the message window as late as possible
	# so new instances of NVDA can find this one even if it freezes during exit.
	messageWindow.destroy()
	log.debug("core done")

def _terminate(module, name=None):
	if name is None:
		name = module.__name__
	log.debug("Terminating %s" % name)
	try:
		module.terminate()
	except:
		log.exception("Error terminating %s" % name)

def requestPump():
	"""Request a core pump.
	This will perform any queued activity.
	It is delayed slightly so that queues can implement rate limiting,
	filter extraneous events, etc.
	"""
	global _isPumpPending
	if not _pump or _isPumpPending:
		return
	_isPumpPending = True
	if thread.get_ident() == mainThreadId:
		_pump.Start(PUMP_MAX_DELAY, True)
		return
	# This isn't the main thread. wx timers cannot be run outside the main thread.
	# Therefore, Have wx start it in the main thread with a CallAfter.
	import wx
	wx.CallAfter(_pump.Start,PUMP_MAX_DELAY, True)

def callLater(delay, callable, *args, **kwargs):
	"""Call a callable once after the specified number of milliseconds.
	This is currently a thin wrapper around C{wx.CallLater},
	but this should be used instead for calls which aren't just for UI,
	as it notifies watchdog appropriately.
	"""
	import wx
	return wx.CallLater(delay, _callLaterExec, callable, args, kwargs)

def _callLaterExec(callable, args, kwargs):
	import watchdog
	watchdog.alive()
	try:
		return callable(*args, **kwargs)
	finally:
		watchdog.asleep()
