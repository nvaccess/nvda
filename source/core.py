# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NV Access Limited, Aleksey Sadovoy, Christopher Toth, Joseph Lee, Peter Vágner,
# Derek Riemer, Babbage B.V., Zahari Yurukov, Łukasz Golonka, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""NVDA core"""


from dataclasses import dataclass
from typing import (
	Any,
	List,
	Optional,
)
import comtypes
import sys
import winVersion
import threading
import os
import time
import ctypes
from enum import Enum
import logHandler
import languageHandler
import globalVars
from logHandler import log
import addonHandler
import extensionPoints
import garbageHandler
import NVDAState
from NVDAState import WritePaths


def __getattr__(attrName: str) -> Any:
	"""Module level `__getattr__` used to preserve backward compatibility.
	"""
	if attrName == "post_windowMessageReceipt" and NVDAState._allowDeprecatedAPI():
		from winAPI.messageWindow import pre_handleWindowMessage
		log.warning(
			"core.post_windowMessageReceipt is deprecated, "
			"use winAPI.messageWindow.pre_handleWindowMessage instead."
		)
		return pre_handleWindowMessage
	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")


# Inform those who want to know that NVDA has finished starting up.
postNvdaStartup = extensionPoints.Action()

PUMP_MAX_DELAY = 10

#: The thread identifier of the main thread.
mainThreadId = threading.get_ident()

_pump = None


class _PumpPending(Enum):
	NONE = 0
	DELAYED = 1
	IMMEDIATE = 2

	def __bool__(self):
		return self is not self.NONE


_hasShutdownBeenTriggered = False
_shuttingDownFlagLock = threading.Lock()


def _showAddonsErrors() -> None:
	addonFailureMessages: list[str] = []
	failedUpdates = addonHandler._failedPendingInstalls.intersection(addonHandler._failedPendingRemovals)
	failedInstalls = addonHandler._failedPendingInstalls - failedUpdates
	failedRemovals = addonHandler._failedPendingRemovals - failedUpdates
	if failedUpdates:
		addonFailureMessages.append(
			ngettext(
				# Translators: Shown when one or more add-ons failed to update.
				"The following add-on failed to update: {}.",
				"The following add-ons failed to update: {}.",
				len(failedUpdates)
			).format(", ".join(failedUpdates))
		)
	if failedRemovals:
		addonFailureMessages.append(
			ngettext(
				# Translators: Shown when one or more add-ons failed to be uninstalled.
				"The following add-on failed to uninstall: {}.",
				"The following add-ons failed to uninstall: {}.",
				len(failedRemovals)
			).format(", ".join(failedRemovals))
		)
	if failedInstalls:
		addonFailureMessages.append(
			ngettext(
				# Translators: Shown when one or more add-ons failed to be installed.
				"The following add-on failed to be installed: {}.",
				"The following add-ons failed to be installed: {}.",
				len(failedInstalls)
			).format(", ".join(failedInstalls))
		)

	if addonFailureMessages:
		import wx
		import gui
		gui.messageBox(
			_(
				# Translators: Shown when one or more actions on add-ons failed.
				"Some operations on add-ons failed. See the log file for more details.\n{}"
			).format("\n".join(addonFailureMessages)),
			# Translators: Title of message shown when requested action on add-ons failed.
			_("Error"),
			wx.ICON_ERROR | wx.OK
		)


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
	_showAddonsErrors()


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
	if NVDAState.isRunningAsSource():
		options.append(os.path.basename(sys.argv[0]))
	_startNewInstance(NewNVDAInstance(
		sys.executable,
		subprocess.list2cmdline(options + sys.argv[1:]),
		globalVars.appDir
	))


def restart(disableAddons=False, debugLogging=False):
	"""Restarts NVDA by starting a new copy."""
	if globalVars.appArgs.launcher:
		NVDAState._setExitCode(3)
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
	if NVDAState.isRunningAsSource():
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
	import bdDetect
	import hwIo
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
	log.debug("Terminating background braille display detection")
	bdDetect.terminate()
	log.debug("Terminating background i/o")
	hwIo.terminate()
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
	from addonStore import dataManager
	dataManager.initialize()
	addonHandler.initialize()
	# Hardware background i/o
	log.debug("initializing background i/o")
	hwIo.initialize()
	log.debug("Initializing background braille display detection")
	bdDetect.initialize()
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
			log.debugWarning(
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


def _initializeObjectCaches():
	"""
	Caches the desktop object.
	This may make information from the desktop window available on the lock screen,
	however no known exploit is known for this.

	The desktop object must be used, as setting the object caches has side effects,
	such as focus events.
	Side effects from events generated while setting these objects may require NVDA to be finished initializing.
	E.G. An app module for a lockScreen window.
	The desktop object is an NVDA object without event handlers associated with it.
	"""
	import api
	import NVDAObjects
	import winUser

	desktopObject = NVDAObjects.window.Window(windowHandle=winUser.getDesktopWindow())
	api.setDesktopObject(desktopObject)
	api.setForegroundObject(desktopObject)
	api.setFocusObject(desktopObject)
	api.setNavigatorObject(desktopObject)
	api.setMouseObject(desktopObject)


def _doLoseFocus():
	import api
	focusObject = api.getFocusObject()
	if focusObject and hasattr(focusObject, "event_loseFocus"):
		log.debug("calling lose focus on object with focus")
		try:
			focusObject.event_loseFocus()
		except Exception:
			log.exception("Lose focus error")


def main():
	"""NVDA's core main loop.
	This initializes all modules such as audio, IAccessible, keyboard, mouse, and GUI.
	Then it initialises the wx application object and sets up the core pump,
	which checks the queues and executes functions when requested.
	Finally, it starts the wx main loop.
	"""
	log.debug("Core starting")
	if NVDAState.isRunningAsSource():
		# When running as packaged version, DPI awareness is set via the app manifest.
		from winAPI.dpiAwareness import setDPIAwareness
		setDPIAwareness()

	import config
	if not WritePaths.configDir:
		WritePaths.configDir = config.getUserDefaultConfigPath(
			useInstalledPathIfExists=globalVars.appArgs.launcher
		)
	#Initialize the config path (make sure it exists)
	config.initConfigPath()
	log.info(f"Config dir: {WritePaths.configDir}")
	log.debug("loading config")
	import config
	config.initialize()
	if config.conf['development']['enableScratchpadDir']:
		log.info("Developer Scratchpad mode enabled")
	if languageHandler.isLanguageForced():
		lang = globalVars.appArgs.language
	else:
		lang = config.conf["general"]["language"]
	log.debug(f"setting language to {lang}")
	languageHandler.setLanguage(lang)
	import NVDAHelper
	log.debug("Initializing NVDAHelper")
	NVDAHelper.initialize()
	import nvwave
	log.debug("initializing nvwave")
	nvwave.initialize()
	if not globalVars.appArgs.minimal and config.conf["general"]["playStartAndExitSounds"]:
		try:
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "start.wav"))
		except Exception:
			pass
	logHandler.setLogLevelFromConfig()
	log.info(f"Windows version: {winVersion.getWinVer()}")
	log.info("Using Python version %s"%sys.version)
	log.info("Using comtypes version %s"%comtypes.__version__)
	import configobj
	log.info("Using configobj version %s with validate version %s"%(configobj.__version__,configobj.validate.__version__))
	# Set a reasonable timeout for any socket connections NVDA makes.
	import socket
	socket.setdefaulttimeout(10)
	log.debug("Initializing add-ons system")
	from addonStore import dataManager
	dataManager.initialize()
	addonHandler.initialize()
	if globalVars.appArgs.disableAddons:
		log.info("Add-ons are disabled. Restart NVDA to enable them.")
	import appModuleHandler
	log.debug("Initializing appModule Handler")
	appModuleHandler.initialize()
	log.debug("initializing background i/o")
	import hwIo
	hwIo.initialize()
	log.debug("Initializing background braille display detection")
	import bdDetect
	bdDetect.initialize()
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
	timeSinceStart = time.time() - NVDAState.getStartTime()
	if not globalVars.appArgs.minimal and timeSinceStart > 5:
		log.debugWarning("Slow starting core (%.2f sec)" % timeSinceStart)
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

	from winAPI.messageWindow import _MessageWindow
	import versionInfo
	messageWindow = _MessageWindow(versionInfo.name)

	# initialize wxpython localization support
	wxLocaleObj = wx.Locale()
	wxLang = getWxLangOrNone()
	if not NVDAState.isRunningAsSource():
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

	_initializeObjectCaches()

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

	class CorePump(wx.Timer):
		"Checks the queues and executes functions."
		pending = _PumpPending.NONE
		isPumping = False

		def queueRequest(self):
			isMainThread = threading.get_ident() == mainThreadId
			if self.pending == _PumpPending.DELAYED and isMainThread:
				# We just want to start a timer and we're already on the main thread, so we
				# don't need to queue that.
				self.processRequest()
				return
			wx.CallAfter(self.processRequest)

		def processRequest(self):
			if self.isPumping:
				return  # Prevent re-entry.
			if self.pending == _PumpPending.IMMEDIATE:
				# A delayed pump might have been scheduled. If so, cancel it.
				self.Stop()
				self.Notify()
			elif self.pending == _PumpPending.DELAYED:
				self.Start(PUMP_MAX_DELAY, True)

		def Notify(self):
			assert not self.isPumping, "Must not pump while already pumping"
			if not self.pending:
				log.error("Pumping but pump wasn't pending", stack_info=True)
			self.isPumping = True
			self.pending = _PumpPending.NONE
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
				sessionTracking.pumpAll()
			except Exception:
				log.exception("errors in this core pump cycle")
			try:
				baseObject.AutoPropertyObject.invalidateCaches()
			except Exception:
				log.exception("AutoPropertyObject.invalidateCaches failed")
			watchdog.asleep()
			self.isPumping = False
			# #3803: If another pump was requested during this pump execution, we need
			# to trigger another pump, as our pump is not re-entrant.
			if self.pending == _PumpPending.IMMEDIATE:
				# We don't call processRequest directly because we don't want this to
				# recurse. Recursing can overflow the stack if there are a flood of
				# immediate pumps; e.g. touch exploration.
				self.queueRequest()
			elif self.pending == _PumpPending.DELAYED:
				self.processRequest()
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

	from winAPI import sessionTracking
	sessionTracking.initialize()

	NVDAState._TrackNVDAInitialization.markInitializationComplete()

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

	_doLoseFocus()

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
	_terminate(touchHandler)
	_terminate(keyboardHandler, name="keyboard handler")
	_terminate(mouseHandler)
	_terminate(inputCore)
	_terminate(vision)
	_terminate(brailleInput)
	_terminate(braille)
	_terminate(speech)
	_terminate(bdDetect)
	_terminate(hwIo)
	_terminate(addonHandler)
	_terminate(nvwave)
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
	_terminate(NVDAHelper)
	log.debug("core done")

def _terminate(module, name=None):
	if name is None:
		name = module.__name__
	log.debug("Terminating %s" % name)
	try:
		module.terminate()
	except:
		log.exception("Error terminating %s" % name)


def isMainThread() -> bool:
	return threading.get_ident() == mainThreadId


def requestPump(immediate: bool = False):
	"""Request a core pump.
	This will perform any queued activity.
	@param immediate: If True, the pump will happen as soon as possible. This
		should be used where response time is most important; e.g. user input or
		focus events.
		If False, it is delayed slightly so that queues can implement rate limiting,
		filter extraneous events, etc.
	"""
	if not _pump:
		return
	# We only need to do something if:
	if (
		# There is no pending pump.
		_pump.pending == _PumpPending.NONE
		# There is a pending delayed pump but an immediate pump was just requested.
		or (immediate and _pump.pending == _PumpPending.DELAYED)
	):
		_pump.pending = _PumpPending.IMMEDIATE if immediate else _PumpPending.DELAYED
		_pump.queueRequest()


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
	if isMainThread():
		return wx.CallLater(delay, _callLaterExec, callable, args, kwargs)
	else:
		return wx.CallAfter(wx.CallLater,delay, _callLaterExec, callable, args, kwargs)

def _callLaterExec(callable, args, kwargs):
	import queueHandler
	queueHandler.queueFunction(queueHandler.eventQueue,callable,*args, **kwargs)
