# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2021 NV Access Limited, Aleksey Sadovoy, Christopher Toth, Joseph Lee, Peter Vágner,
# Derek Riemer, Babbage B.V., Zahari Yurukov, Łukasz Golonka
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""NVDA core"""


from dataclasses import dataclass
from typing import List, Optional
import comtypes
import sys
import winVersion
import threading
import nvwave
import os
import time
import ctypes
import logHandler
import languageHandler
import globalVars
from logHandler import log
import addonHandler
import extensionPoints
import garbageHandler


# inform those who want to know that NVDA has finished starting up.
postNvdaStartup = extensionPoints.Action()

PUMP_MAX_DELAY = 10

#: The thread identifier of the main thread.
mainThreadId = threading.get_ident()

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

_hasShutdownBeenTriggered = False
_shuttingDownFlagLock = threading.Lock()


def doStartupDialogs():
	import config
	import gui

	def handleReplaceCLIArg(cliArgument: str) -> bool:
		"""Since #9827 NVDA replaces a currently running instance
		and therefore `--replace` command line argument is redundant and no longer supported.
		However for backwards compatibility the desktop shortcut created by installer
		still starts NVDA with the now redundant switch.
		Its presence in command line arguments should not cause a warning on startup."""
		return cliArgument in ("-r", "--replace")

	addonHandler.isCLIParamKnown.register(handleReplaceCLIArg)
	unknownCLIParams: List[str] = list()
	for param in globalVars.unknownAppArgs:
		isParamKnown = addonHandler.isCLIParamKnown.decide(cliArgument=param)
		if not isParamKnown:
			unknownCLIParams.append(param)
	if unknownCLIParams:
		import wx
		gui.messageBox(
			# Translators: Shown when NVDA has been started with unknown command line parameters.
			_("The following command line parameters are unknown to NVDA: {params}").format(
				params=", ".join(unknownCLIParams)
			),
			# Translators: Title of the dialog letting user know
			# that command line parameters they provided are unknown.
			_("Unknown command line parameters"),
			wx.OK | wx.ICON_ERROR
		)
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
		from gui.startupDialogs import WelcomeDialog
		WelcomeDialog.run()
	if config.conf["brailleViewer"]["showBrailleViewerAtStartup"]:
		gui.mainFrame.onToggleBrailleViewerCommand(evt=None)
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
			gui.runScriptModalDialog(gui.startupDialogs.AskAllowUsageStatsDialog(None), onResult)


@dataclass
class NewNVDAInstance:
	filePath: str
	parameters: Optional[str] = None
	directory: Optional[str] = None


def restartUnsafely():
	"""Start a new copy of NVDA immediately.
	Used as a last resort, in the event of a serious error to immediately restart NVDA without running any
	cleanup / exit code.
	There is no dependency on NVDA currently functioning correctly, which is in contrast with L{restart} which
	depends on the internal queue processing (queueHandler).
	Because none of NVDA's shutdown code is run, NVDA is likely to be left in an unclean state.
	Some examples of clean up that may be skipped.
	- Free NVDA's mutex (mutex prevents multiple NVDA instances), leaving it abandoned when this process ends.
	  - However, this situation is handled during mutex acquisition.
	- Remove icons (systray)
	- Saving settings
	"""
	log.info("Restarting unsafely")
	import subprocess
	# Unlike a normal restart, see L{restart}:
	# - if addons are disabled, leave them disabled
	# - if debug logging is set, leave it set.
	# The new instance should operate in the same way (as much as possible) as the old instance.
	for paramToRemove in ("--ease-of-access"):
		try:
			sys.argv.remove(paramToRemove)
		except ValueError:
			pass
	options = []
	if not hasattr(sys, "frozen"):
		options.append(os.path.basename(sys.argv[0]))
	_startNewInstance(NewNVDAInstance(
		sys.executable,
		subprocess.list2cmdline(options + sys.argv[1:]),
		globalVars.appDir
	))


def restart(disableAddons=False, debugLogging=False):
	"""Restarts NVDA by starting a new copy."""
	if globalVars.appArgs.launcher:
		globalVars.exitCode=3
		if not triggerNVDAExit():
			log.error("NVDA already in process of exiting, this indicates a logic error.")
		return
	import subprocess
	for paramToRemove in (
		"--disable-addons", "--debug-logging", "--ease-of-access"
	) + languageHandler.getLanguageCliArgs():
		try:
			sys.argv.remove(paramToRemove)
		except ValueError:
			pass
	options = []
	if not hasattr(sys, "frozen"):
		options.append(os.path.basename(sys.argv[0]))
	if disableAddons:
		options.append('--disable-addons')
	if debugLogging:
		options.append('--debug-logging')

	if not triggerNVDAExit(NewNVDAInstance(
		sys.executable,
		subprocess.list2cmdline(options + sys.argv[1:]),
		globalVars.appDir
	)):
		log.error("NVDA already in process of exiting, this indicates a logic error.")


def resetConfiguration(factoryDefaults=False):
	"""Loads the configuration, installs the correct language support and initialises audio so that it will use the configured synth and speech settings.
	"""
	import config
	import braille
	import brailleInput
	import speech
	import vision
	import inputCore
	import tones
	log.debug("Terminating vision")
	vision.terminate()
	log.debug("Terminating braille")
	braille.terminate()
	log.debug("Terminating brailleInput")
	brailleInput.terminate()
	log.debug("terminating speech")
	speech.terminate()
	log.debug("terminating tones")
	tones.terminate()
	log.debug("terminating addonHandler")
	addonHandler.terminate()
	log.debug("Reloading config")
	config.conf.reset(factoryDefaults=factoryDefaults)
	logHandler.setLogLevelFromConfig()
	# Language
	if languageHandler.isLanguageForced():
		lang = globalVars.appArgs.language
	else:
		lang = config.conf["general"]["language"]
	log.debug("setting language to %s"%lang)
	languageHandler.setLanguage(lang)
	# Addons
	addonHandler.initialize()
	# Tones
	tones.initialize()
	#Speech
	log.debug("initializing speech")
	speech.initialize()
	#braille
	log.debug("Initializing brailleInput")
	brailleInput.initialize()
	log.debug("Initializing braille")
	braille.initialize()
	# Vision
	log.debug("initializing vision")
	vision.initialize()
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


def getWxLangOrNone() -> Optional['wx.LanguageInfo']:
	import wx
	lang = languageHandler.getLanguage()
	wxLocaleObj = wx.Locale()
	wxLang = wxLocaleObj.FindLanguageInfo(lang)
	if not wxLang and '_' in lang:
		wxLang = wxLocaleObj.FindLanguageInfo(lang.split('_')[0])
	# #8064: Wx might know the language, but may not actually contain a translation database for that language.
	# If we try to initialize this language, wx will show a warning dialog.
	# #9089: some languages (such as Aragonese) do not have language info, causing language getter to fail.
	# In this case, wxLang is already set to None.
	# Therefore treat these situations like wx not knowing the language at all.
	if wxLang and not wxLocaleObj.IsAvailable(wxLang.Language):
		wxLang = None
	if not wxLang:
		log.debugWarning("wx does not support language %s" % lang)
	return wxLang


def _startNewInstance(newNVDA: NewNVDAInstance):
	"""
	If something (eg the installer or exit dialog) has requested a new NVDA instance to start, start it.
	Should only be used by calling triggerNVDAExit and after handleNVDAModuleCleanupBeforeGUIExit and
	_closeAllWindows.
	"""
	import shellapi
	from winUser import SW_SHOWNORMAL
	log.debug(f"Starting new NVDA instance: {newNVDA}")
	shellapi.ShellExecute(
		hwnd=None,
		operation=None,
		file=newNVDA.filePath,
		parameters=newNVDA.parameters,
		directory=newNVDA.directory,
		# #4475: ensure that the first window of the new process is not hidden by providing SW_SHOWNORMAL
		showCmd=SW_SHOWNORMAL
	)


def _doShutdown(newNVDA: Optional[NewNVDAInstance]):
	_handleNVDAModuleCleanupBeforeGUIExit()
	_closeAllWindows()
	if newNVDA is not None:
		_startNewInstance(newNVDA)


def triggerNVDAExit(newNVDA: Optional[NewNVDAInstance] = None) -> bool:
	"""
	Used to safely exit NVDA. If a new instance is required to start after exit, queue one by specifying
	instance information with `newNVDA`.
	@return: True if this is the first call to trigger the exit, and the shutdown event was queued.
	"""
	from gui.message import isModalMessageBoxActive
	import queueHandler
	global _hasShutdownBeenTriggered
	with _shuttingDownFlagLock:
		safeToExit = not isModalMessageBoxActive()
		if not safeToExit:
			log.error("NVDA cannot exit safely, ensure open dialogs are closed")
			return False
		elif _hasShutdownBeenTriggered:
			log.debug("NVDA has already been triggered to exit safely.")
			return False
		else:
			# queue this so that the calling process can exit safely (eg a Popup menu)
			queueHandler.queueFunction(queueHandler.eventQueue, _doShutdown, newNVDA)
			_hasShutdownBeenTriggered = True
			log.debug("_doShutdown has been queued")
			return True


def _closeAllWindows():
	"""
	Should only be used by calling triggerNVDAExit and after _handleNVDAModuleCleanupBeforeGUIExit.
	Ensures the wx mainloop is exited by all the top windows being destroyed.
	wx objects that don't inherit from wx.Window (eg sysTrayIcon, Menu) need to be manually destroyed.
	"""
	import gui
	from gui.settingsDialogs import SettingsDialog
	from typing import Dict
	import wx

	app = wx.GetApp()

	# prevent race condition with object deletion
	# prevent deletion of the object while we work on it.
	_SettingsDialog = SettingsDialog
	nonWeak: Dict[_SettingsDialog, _SettingsDialog] = dict(_SettingsDialog._instances)

	for instance, state in nonWeak.items():
		if state is _SettingsDialog.DialogState.DESTROYED:
			log.error(
				"Destroyed but not deleted instance of gui.SettingsDialog exists"
				f": {instance.title} - {instance.__class__.__qualname__} - {instance}"
			)
		else:
			log.debug("Exiting NVDA with an open settings dialog: {!r}".format(instance))

	# wx.Windows destroy child Windows automatically but wx.Menu and TaskBarIcon don't inherit from wx.Window.
	# They must be manually destroyed when exiting the app.
	# Note: this doesn't consistently clean them from the tray and appears to be a wx issue. (#12286, #12238)
	log.debug("destroying system tray icon and menu")
	app.ScheduleForDestruction(gui.mainFrame.sysTrayIcon.menu)
	gui.mainFrame.sysTrayIcon.RemoveIcon()
	app.ScheduleForDestruction(gui.mainFrame.sysTrayIcon)

	wx.Yield()  # processes pending messages
	gui.mainFrame.sysTrayIcon.menu = None
	gui.mainFrame.sysTrayIcon = None

	for window in wx.GetTopLevelWindows():
		if isinstance(window, wx.Dialog) and window.IsModal():
			log.debug(f"ending modal {window} during exit process")
			wx.CallAfter(window.EndModal, wx.ID_CLOSE_ALL)
		elif not isinstance(window, gui.MainFrame):
			log.debug(f"closing window {window} during exit process")
			wx.CallAfter(window.Close)

	wx.Yield()  # creates a temporary event loop and uses it instead to process pending messages
	log.debug("destroying main frame during exit process")
	# the MainFrame has EVT_CLOSE bound to the ExitDialog
	# which calls this function on exit, so destroy this window
	app.ScheduleForDestruction(gui.mainFrame)


def _handleNVDAModuleCleanupBeforeGUIExit():
	""" Terminates various modules that rely on the GUI. This should be used before closing all windows
	and terminating the GUI.
	"""
	import brailleViewer
	import globalPluginHandler
	import watchdog

	try:
		import updateCheck
		# before the GUI is terminated we must terminate the update checker
		_terminate(updateCheck)
	except RuntimeError:
		pass

	# The core is expected to terminate, so we should not treat this as a crash
	_terminate(watchdog)
	# plugins must be allowed to close safely before we terminate the GUI as dialogs may be unsaved
	_terminate(globalPluginHandler)
	# the brailleViewer should be destroyed safely before closing the window
	brailleViewer.destroyBrailleViewer()


def main():
	"""NVDA's core main loop.
	This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI.
	Then it initialises the wx application object and sets up the core pump,
	which checks the queues and executes functions when requested.
	Finally, it starts the wx main loop.
	"""
	log.debug("Core starting")

	ctypes.windll.user32.SetProcessDPIAware()

	import config
	if not globalVars.appArgs.configPath:
		globalVars.appArgs.configPath=config.getUserDefaultConfigPath(useInstalledPathIfExists=globalVars.appArgs.launcher)
	#Initialize the config path (make sure it exists)
	config.initConfigPath()
	log.info(f"Config dir: {globalVars.appArgs.configPath}")
	log.debug("loading config")
	import config
	config.initialize()
	if config.conf['development']['enableScratchpadDir']:
		log.info("Developer Scratchpad mode enabled")
	if not globalVars.appArgs.minimal and config.conf["general"]["playStartAndExitSounds"]:
		try:
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "start.wav"))
		except:
			pass
	logHandler.setLogLevelFromConfig()
	if languageHandler.isLanguageForced():
		lang = globalVars.appArgs.language
	else:
		lang = config.conf["general"]["language"]
	log.debug(f"setting language to {lang}")
	languageHandler.setLanguage(lang)
	log.info(f"Windows version: {winVersion.getWinVer()}")
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
	log.debug("Initializing tones")
	import tones
	tones.initialize()
	import speechDictHandler
	log.debug("Speech Dictionary processing")
	speechDictHandler.initialize()
	import speech
	log.debug("Initializing speech")
	speech.initialize()
	import mathPres
	log.debug("Initializing MathPlayer")
	mathPres.initialize()
	if not globalVars.appArgs.minimal and (time.time()-globalVars.startTime)>5:
		log.debugWarning("Slow starting core (%.2f sec)" % (time.time()-globalVars.startTime))
		# Translators: This is spoken when NVDA is starting.
		speech.speakMessage(_("Loading NVDA. Please wait..."))
	import wx
	import six
	log.info("Using wx version %s with six version %s"%(wx.version(), six.__version__))
	class App(wx.App):
		def OnAssert(self,file,line,cond,msg):
			message="{file}, line {line}:\nassert {cond}: {msg}".format(file=file,line=line,cond=cond,msg=msg)
			log.debugWarning(message,codepath="WX Widgets",stack_info=True)

		def InitLocale(self):
			"""Custom implementation of `InitLocale` which ensures that wxPython does not change the locale.
			The current wx implementation (as of wxPython 4.1.1) sets Python locale to an invalid one
			which triggers Python issue 36792 (#12160).
			The new implementation (wxPython 4.1.2) sets locale to "C" (basic Unicode locale).
			While this is not wrong as such NVDA manages locale themselves using `languageHandler`
			and it is better to remove wx from the equation so this method is a No-op.
			This code may need to be revisited when we update Python / wxPython.
			"""
			pass


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
				nvwave.playWaveFile(
					os.path.join(globalVars.appDir, "waves", "exit.wav"),
					asynchronous=False
				)
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
	import vision
	log.debug("Initializing vision")
	vision.initialize()
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
		# Windows constants for power / display changes
		WM_POWERBROADCAST = 0x218
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
			elif msg == winUser.WM_DISPLAYCHANGE:
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
	import versionInfo
	messageWindow = MessageWindow(versionInfo.name)

	# initialize wxpython localization support
	wxLocaleObj = wx.Locale()
	wxLang = getWxLangOrNone()
	if hasattr(sys,'frozen'):
		wxLocaleObj.AddCatalogLookupPathPrefix(os.path.join(globalVars.appDir, "locale"))
	if wxLang:
		try:
			wxLocaleObj.Init(wxLang.Language)
		except:
			log.error("Failed to initialize wx locale",exc_info=True)
		finally:
			# Revert wx's changes to the python locale
			languageHandler.setLocale(languageHandler.getLanguage())

	log.debug("Initializing garbageHandler")
	garbageHandler.initialize()

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
		log.info("Java Access Bridge support initialized")
	except NotImplementedError:
		log.warning("Java Access Bridge not available")
	except:
		log.error("Error initializing Java Access Bridge support", exc_info=True)
	import winConsoleHandler
	log.debug("Initializing legacy winConsole support")
	winConsoleHandler.initialize()
	import UIAHandler
	log.debug("Initializing UIA support")
	try:
		UIAHandler.initialize()
	except RuntimeError:
		log.warning("UIA disabled in configuration")
	except:
		log.error("Error initializing UIA support", exc_info=True)
	import IAccessibleHandler
	log.debug("Initializing IAccessible support")
	IAccessibleHandler.initialize()
	log.debug("Initializing input core")
	import inputCore
	inputCore.initialize()
	import keyboardHandler
	import watchdog
	log.debug("Initializing keyboard handler")
	keyboardHandler.initialize(watchdog.WatchdogObserver())
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
		wx.CallAfter(
			gui.installerGui.doSilentInstall,
			copyPortableConfig=globalVars.appArgs.copyPortableConfig,
			startAfterInstall=not globalVars.appArgs.installSilent
		)
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
			from gui.startupDialogs import LauncherDialog
			LauncherDialog.run()
			# LauncherDialog will call doStartupDialogs() afterwards if required.
		else:
			wx.CallAfter(doStartupDialogs)
	import queueHandler
	# Queue the handling of initial focus,
	# as API handlers might need to be pumped to get the first focus event.
	queueHandler.queueFunction(queueHandler.eventQueue, _setInitialFocus)
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
				vision.pumpAll()
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

	# Queue the firing of the postNVDAStartup notification.
	# This is queued so that it will run from within the core loop,
	# and initial focus has been reported.
	def _doPostNvdaStartupAction():
		log.debug("Notify of postNvdaStartup action")
		postNvdaStartup.notify()

	queueHandler.queueFunction(queueHandler.eventQueue, _doPostNvdaStartupAction)

	log.debug("entering wx application main loop")
	app.MainLoop()

	log.info("Exiting")
	# If MainLoop is terminated through WM_QUIT, such as starting an NVDA instance older than 2021.1,
	# triggerNVDAExit has not been called yet
	if triggerNVDAExit():
		log.debug(
			"NVDA not already exiting, hit catch-all exit trigger."
			" This likely indicates NVDA is exiting due to WM_QUIT."
		)
		queueHandler.pumpAll()
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
	_terminate(winConsoleHandler, name="Legacy winConsole support")
	_terminate(JABHandler, name="Java Access Bridge support")
	_terminate(appModuleHandler, name="app module handler")
	_terminate(tones)
	_terminate(NVDAHelper)
	_terminate(touchHandler)
	_terminate(keyboardHandler, name="keyboard handler")
	_terminate(mouseHandler)
	_terminate(inputCore)
	_terminate(vision)
	_terminate(brailleInput)
	_terminate(braille)
	_terminate(speech)
	_terminate(addonHandler)
	_terminate(garbageHandler)
	# DMP is only started if needed.
	# Terminate manually (and let it write to the log if necessary)
	# as core._terminate always writes an entry.
	try:
		import diffHandler
		diffHandler._dmp._terminate()
	except Exception:
		log.exception("Exception while terminating DMP")

	if not globalVars.appArgs.minimal and config.conf["general"]["playStartAndExitSounds"]:
		try:
			nvwave.playWaveFile(
				os.path.join(globalVars.appDir, "waves", "exit.wav"),
				asynchronous=False
			)
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
	if threading.get_ident() == mainThreadId:
		_pump.Start(PUMP_MAX_DELAY, True)
		return
	# This isn't the main thread. wx timers cannot be run outside the main thread.
	# Therefore, Have wx start it in the main thread with a CallAfter.
	import wx
	wx.CallAfter(_pump.Start,PUMP_MAX_DELAY, True)


class NVDANotInitializedError(Exception):
	pass


def callLater(delay, callable, *args, **kwargs):
	"""Call a callable once after the specified number of milliseconds.
	As the call is executed within NVDA's core queue, it is possible that execution will take place slightly after the requested time.
	This function should never be used to execute code that brings up a modal UI as it will cause NVDA's core to block.
	This function can be safely called from any thread once NVDA has been initialized.
	"""
	import wx
	if wx.GetApp() is None:
		# If NVDA has not fully initialized yet, the wxApp may not be initialized.
		# wx.CallLater and wx.CallAfter requires the wxApp to be initialized.
		raise NVDANotInitializedError("Cannot schedule callable, wx.App is not initialized")
	if threading.get_ident() == mainThreadId:
		return wx.CallLater(delay, _callLaterExec, callable, args, kwargs)
	else:
		return wx.CallAfter(wx.CallLater,delay, _callLaterExec, callable, args, kwargs)

def _callLaterExec(callable, args, kwargs):
	import queueHandler
	queueHandler.queueFunction(queueHandler.eventQueue,callable,*args, **kwargs)
