# -*- coding: UTF-8 -*-
#core.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Aleksey Sadovoy, Christopher Toth, Joseph Lee, Peter Vágner, Derek Riemer, Babbage B.V., Zahari Yurukov
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

import extensionPoints

# inform those who want to know that NVDA has finished starting up.
postNvdaStartup = extensionPoints.Action()

PUMP_MAX_DELAY = 10

#: The thread identifier of the main thread.
mainThreadId = thread.get_ident()

#: Notifies when a window message has been received by NVDA.
#: This allows components to perform an action when several system events occur,
#: such as power, screen orientation and hardware changes.
#: Handlers are called with three arguments.
#: @param msg: The window message.
#: @type msg: int
#: @param wParam: Additional message information.
#: @type wParam: int
#: @param lParam: Additional message information.
#: @type lParam: int
post_windowMessageReceipt = extensionPoints.Action()

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
	if config.conf["speechViewer"]["showSpeechViewerAtStartup"]:
		gui.mainFrame.onToggleSpeechViewerCommand(evt=None)
	import inputCore
	if inputCore.manager.userGestureMap.lastUpdateContainedError:
		import wx
		gui.messageBox(_("Your gesture map file contains errors.\n"
				"More details about the errors can be found in the log file."),
			_("gesture map File Error"), wx.OK|wx.ICON_EXCLAMATION)
	try:
		import updateCheck
	except RuntimeError:
		updateCheck=None
	if not globalVars.appArgs.secure and not config.isAppX and not globalVars.appArgs.launcher:
		if updateCheck and not config.conf['update']['askedAllowUsageStats']:
			# a callback to save config after the usage stats question dialog has been answered.
			def onResult(ID):
				import wx
				if ID in (wx.ID_YES,wx.ID_NO):
					try:
						config.conf.save()
					except:
						pass
			# Ask the user if usage stats can be collected.
			gui.runScriptModalDialog(gui.AskAllowUsageStatsDialog(None),onResult)

def restart(disableAddons=False, debugLogging=False):
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
	try:
		sys.argv.remove('--debug-logging')
	except ValueError:
		pass
	if disableAddons:
		options.append('--disable-addons')
	if debugLogging:
		options.append('--debug-logging')
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
	import brailleInput
	import speech
	import languageHandler
	import inputCore
	log.debug("Terminating braille")
	braille.terminate()
	log.debug("Terminating brailleInput")
	brailleInput.terminate()
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
	log.debug("Initializing brailleInput")
	brailleInput.initialize()
	log.debug("Initializing braille")
	braille.initialize()
	log.debug("Reloading user and locale input gesture maps")
	inputCore.manager.loadUserGestureMap()
	inputCore.manager.loadLocaleGestureMap()
	import audioDucking
	if audioDucking.isAudioDuckingSupported():
		audioDucking.handlePostConfigProfileSwitch()
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

	ctypes.windll.user32.SetProcessDPIAware()

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
	import configobj
	log.info("Using configobj version %s with validate version %s"%(configobj.__version__,configobj.validate.__version__))
	# Set a reasonable timeout for any socket connections NVDA makes.
	import socket
	socket.setdefaulttimeout(10)
	log.debug("Initializing add-ons system")
	addonHandler.initialize()
	if globalVars.appArgs.disableAddons:
		log.info("Add-ons are disabled. Restart NVDA to enable them.")
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
	# wxPython 4 no longer has either of these constants (despite the documentation saying so), some add-ons may rely on
	# them so we add it back into wx. https://wxpython.org/Phoenix/docs/html/wx.Window.html#wx.Window.Centre
	wx.CENTER_ON_SCREEN = wx.CENTRE_ON_SCREEN = 0x2
	log.info("Using wx version %s"%wx.version())
	class App(wx.App):
		def OnAssert(self,file,line,cond,msg):
			message="{file}, line {line}:\nassert {cond}: {msg}".format(file=file,line=line,cond=cond,msg=msg)
			log.debugWarning(message,codepath="WX Widgets",stack_info=True)
	app = App(redirect=False)
	# We support queryEndSession events, but in general don't do anything for them.
	# However, when running as a Windows Store application, we do want to request to be restarted for updates
	def onQueryEndSession(evt):
		if config.isAppX:
			# Automatically restart NVDA on Windows Store update
			ctypes.windll.kernel32.RegisterApplicationRestart(None,0)
	app.Bind(wx.EVT_QUERY_END_SESSION, onQueryEndSession)
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
	log.debug("Initializing braille input")
	import brailleInput
	brailleInput.initialize()
	import braille
	log.debug("Initializing braille")
	braille.initialize()
	import displayModel
	log.debug("Initializing displayModel")
	displayModel.initialize()
	log.debug("Initializing GUI")
	import gui
	gui.initialize()
	import audioDucking
	if audioDucking.isAudioDuckingSupported():
		# the GUI mainloop must be running for this to work so delay it
		wx.CallAfter(audioDucking.initialize)

	# #3763: In wxPython 3, the class name of frame windows changed from wxWindowClassNR to wxWindowNR.
	# NVDA uses the main frame to check for and quit another instance of NVDA.
	# To remain compatible with older versions of NVDA, create our own wxWindowClassNR.
	# We don't need to do anything else because wx handles WM_QUIT for all windows.
	import windowUtils
	class MessageWindow(windowUtils.CustomWindow):
		className = u"wxWindowClassNR"
		#Just define these constants here, so we don't have to import win32con
		WM_POWERBROADCAST = 0x218
		WM_DISPLAYCHANGE = 0x7e
		PBT_APMPOWERSTATUSCHANGE = 0xA
		UNKNOWN_BATTERY_STATUS = 0xFF
		AC_ONLINE = 0X1
		NO_SYSTEM_BATTERY = 0X80
		#States for screen orientation
		ORIENTATION_NOT_INITIALIZED = 0
		ORIENTATION_PORTRAIT = 1
		ORIENTATION_LANDSCAPE = 2

		def __init__(self, windowName=None):
			super(MessageWindow, self).__init__(windowName)
			self.oldBatteryStatus = None
			self.orientationStateCache = self.ORIENTATION_NOT_INITIALIZED
			self.orientationCoordsCache = (0,0)
			self.handlePowerStatusChange()

		def windowProc(self, hwnd, msg, wParam, lParam):
			post_windowMessageReceipt.notify(msg=msg, wParam=wParam, lParam=lParam)
			if msg == self.WM_POWERBROADCAST and wParam == self.PBT_APMPOWERSTATUSCHANGE:
				self.handlePowerStatusChange()
			elif msg == self.WM_DISPLAYCHANGE:
				self.handleScreenOrientationChange(lParam)

		def handleScreenOrientationChange(self, lParam):
			import ui
			import winUser
			# Resolution detection comes from an article found at https://msdn.microsoft.com/en-us/library/ms812142.aspx.
			#The low word is the width and hiword is height.
			width = winUser.LOWORD(lParam)
			height = winUser.HIWORD(lParam)
			self.orientationCoordsCache = (width,height)
			if width > height:
				# If the height and width are the same, it's actually a screen flip, and we do want to alert of those!
				if self.orientationStateCache == self.ORIENTATION_LANDSCAPE and self.orientationCoordsCache != (width,height):
					return
				#Translators: The screen is oriented so that it is wider than it is tall.
				ui.message(_("Landscape" ))
				self.orientationStateCache = self.ORIENTATION_LANDSCAPE
			else:
				if self.orientationStateCache == self.ORIENTATION_PORTRAIT and self.orientationCoordsCache != (width,height):
					return
				#Translators: The screen is oriented in such a way that the height is taller than it is wide.
				ui.message(_("Portrait"))
				self.orientationStateCache = self.ORIENTATION_PORTRAIT

		def handlePowerStatusChange(self):
			#Mostly taken from script_say_battery_status, but modified.
			import ui
			import winKernel
			sps = winKernel.SYSTEM_POWER_STATUS()
			if not winKernel.GetSystemPowerStatus(sps) or sps.BatteryFlag is self.UNKNOWN_BATTERY_STATUS:
				return
			if sps.BatteryFlag & self.NO_SYSTEM_BATTERY:
				return
			if self.oldBatteryStatus is None:
				#Just initializing the cache, do not report anything.
				self.oldBatteryStatus = sps.ACLineStatus
				return
			if sps.ACLineStatus == self.oldBatteryStatus:
				#Sometimes, this double fires. This also fires when the battery level decreases by 3%.
				return
			self.oldBatteryStatus = sps.ACLineStatus
			if sps.ACLineStatus & self.AC_ONLINE:
				#Translators: Reported when the battery is plugged in, and now is charging.
				ui.message(_("Charging battery. %d percent") % sps.BatteryLifePercent)
			else:
				#Translators: Reported when the battery is no longer plugged in, and now is not charging.
				ui.message(_("Not charging battery. %d percent") %sps.BatteryLifePercent)

	messageWindow = MessageWindow(unicode(versionInfo.name))

	# initialize wxpython localization support
	locale = wx.Locale()
	lang=languageHandler.getLanguage()
	wxLang=locale.FindLanguageInfo(lang)
	if not wxLang and '_' in lang:
		wxLang=locale.FindLanguageInfo(lang.split('_')[0])
	if hasattr(sys,'frozen'):
		locale.AddCatalogLookupPathPrefix(os.path.join(os.getcwdu(),"locale"))
	# #8064: Wx might know the language, but may not actually contain a translation database for that language.
	# If we try to initialize this language, wx will show a warning dialog.
	# Therefore treat this situation like wx not knowing the language at all.
	if not locale.IsAvailable(wxLang.Language):
		wxLang=None
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
		import gui.installerGui
		wx.CallAfter(gui.installerGui.doSilentInstall,startAfterInstall=not globalVars.appArgs.installSilent)
	elif globalVars.appArgs.portablePath and (globalVars.appArgs.createPortable or globalVars.appArgs.createPortableSilent):
		import gui.installerGui
		wx.CallAfter(gui.installerGui.doCreatePortable,portableDirectory=globalVars.appArgs.portablePath,
			silent=globalVars.appArgs.createPortableSilent,startAfterCreate=not globalVars.appArgs.createPortableSilent)
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
	class CorePump(gui.NonReEntrantTimer):
		"Checks the queues and executes functions."
		def run(self):
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
				# #3803: Another pump was requested during this pump execution.
				# As our pump is not re-entrant, schedule another pump.
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
	postNvdaStartup.notify()

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
	As the call is executed within NVDA's core queue, it is possible that execution will take place slightly after the requested time.
	This function should never be used to execute code that brings up a modal UI as it will cause NVDA's core to block.
	This function can be safely called from any thread.
	"""
	import wx
	if thread.get_ident() == mainThreadId:
		return wx.CallLater(delay, _callLaterExec, callable, args, kwargs)
	else:
		return wx.CallAfter(wx.CallLater,delay, _callLaterExec, callable, args, kwargs)

def _callLaterExec(callable, args, kwargs):
	import queueHandler
	queueHandler.queueFunction(queueHandler.eventQueue,callable,*args, **kwargs)
