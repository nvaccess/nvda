# -*- coding: UTF-8 -*-
#gui/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2018 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee, Thomas Stivers, Babbage B.V.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import os
import sys
import threading
import codecs
import ctypes
import weakref
import wx
import wx.adv
import globalVars
import tones
import ui
from logHandler import log
import config
import versionInfo
import addonAPIVersion
import speech
import queueHandler
import core
from . import guiHelper
from .settingsDialogs import *
import speechDictHandler
import languageHandler
import keyboardHandler
from . import logViewer
import speechViewer
import winUser
import api
from . import guiHelper
import winVersion

try:
	import updateCheck
except RuntimeError:
	updateCheck = None

### Constants
NVDA_PATH = os.getcwd()
ICON_PATH=os.path.join(NVDA_PATH, "images", "nvda.ico")
DONATE_URL = "http://www.nvaccess.org/donate/"

### Globals
mainFrame = None
isInMessageBox = False

def getDocFilePath(fileName, localized=True):
	if not getDocFilePath.rootPath:
		if hasattr(sys, "frozen"):
			getDocFilePath.rootPath = os.path.join(NVDA_PATH, "documentation")
		else:
			getDocFilePath.rootPath = os.path.abspath(os.path.join("..", "user_docs"))

	if localized:
		lang = languageHandler.getLanguage()
		tryLangs = [lang]
		if "_" in lang:
			# This locale has a sub-locale, but documentation might not exist for the sub-locale, so try stripping it.
			tryLangs.append(lang.split("_")[0])
		# If all else fails, use English.
		tryLangs.append("en")

		fileName, fileExt = os.path.splitext(fileName)
		for tryLang in tryLangs:
			tryDir = os.path.join(getDocFilePath.rootPath, tryLang)
			if not os.path.isdir(tryDir):
				continue

			# Some out of date translations might include .txt files which are now .html files in newer translations.
			# Therefore, ignore the extension and try both .html and .txt.
			for tryExt in ("html", "txt"):
				tryPath = os.path.join(tryDir, "%s.%s" % (fileName, tryExt))
				if os.path.isfile(tryPath):
					return tryPath

	else:
		# Not localized.
		if not hasattr(sys, "frozen") and fileName in ("copying.txt", "contributors.txt"):
			# If running from source, these two files are in the root dir.
			return os.path.join(NVDA_PATH, "..", fileName)
		else:
			return os.path.join(getDocFilePath.rootPath, fileName)
getDocFilePath.rootPath = None

class MainFrame(wx.Frame):

	def __init__(self):
		style = wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX | wx.FRAME_NO_TASKBAR
		super(MainFrame, self).__init__(None, wx.ID_ANY, versionInfo.name, size=(1,1), style=style)
		self.Bind(wx.EVT_CLOSE, self.onExitCommand)
		self.sysTrayIcon = SysTrayIcon(self)
		#: The focus before the last popup or C{None} if unknown.
		#: This is only valid before L{prePopup} is called,
		#: so it should be used as early as possible in any popup that needs it.
		#: @type: L{NVDAObject}
		self.prevFocus = None
		#: The focus ancestors before the last popup or C{None} if unknown.
		#: @type: list of L{NVDAObject}
		self.prevFocusAncestors = None
		# If NVDA has the uiAccess privilege, it can always set the foreground window.
		import systemUtils
		if not systemUtils.hasUiAccess():
			# This makes Windows return to the previous foreground window and also seems to allow NVDA to be brought to the foreground.
			self.Show()
			self.Hide()
			if winUser.isWindowVisible(self.Handle):
				# HACK: Work around a wx bug where Hide() doesn't actually hide the window,
				# but IsShown() returns False and Hide() again doesn't fix it.
				# This seems to happen if the call takes too long.
				self.Show()
				self.Hide()

	def Destroy(self):
		self.sysTrayIcon.Destroy()
		super(MainFrame, self).Destroy()

	def prePopup(self):
		"""Prepare for a popup.
		This should be called before any dialog or menu which should pop up for the user.
		L{postPopup} should be called after the dialog or menu has been shown.
		@postcondition: A dialog or menu may be shown.
		"""
		nvdaPid = os.getpid()
		focus = api.getFocusObject()
		if focus.processID != nvdaPid:
			self.prevFocus = focus
			self.prevFocusAncestors = api.getFocusAncestors()
		if winUser.getWindowThreadProcessID(winUser.getForegroundWindow())[0] != nvdaPid:
			# This process is not the foreground process, so bring it to the foreground.
			self.Raise()

	def postPopup(self):
		"""Clean up after a popup dialog or menu.
		This should be called after a dialog or menu was popped up for the user.
		"""
		self.prevFocus = None
		self.prevFocusAncestors = None
		if not winUser.isWindowVisible(winUser.getForegroundWindow()):
			# The current foreground window is invisible, so we want to return to the previous foreground window.
			# Showing and hiding our main window seems to achieve this.
			self.Show()
			self.Hide()

	def showGui(self):
		# The menu pops up at the location of the mouse, which means it pops up at an unpredictable location.
		# Therefore, move the mouse to the center of the screen so that the menu will always pop up there.
		location = api.getDesktopObject().location
		winUser.setCursorPos(*location.center)
		self.evaluateUpdatePendingUpdateMenuItemCommand()
		self.sysTrayIcon.onActivate(None)

	def onRevertToSavedConfigurationCommand(self,evt):
		queueHandler.queueFunction(queueHandler.eventQueue,core.resetConfiguration)
		# Translators: Reported when last saved configuration has been applied by using revert to saved configuration option in NVDA menu.
		queueHandler.queueFunction(queueHandler.eventQueue,ui.message,_("Configuration applied"))

	def onRevertToDefaultConfigurationCommand(self,evt):
		queueHandler.queueFunction(queueHandler.eventQueue,core.resetConfiguration,factoryDefaults=True)
		# Translators: Reported when configuration has been restored to defaults by using restore configuration to factory defaults item in NVDA menu.
		queueHandler.queueFunction(queueHandler.eventQueue,ui.message,_("Configuration restored to factory defaults"))

	def onSaveConfigurationCommand(self,evt):
		if globalVars.appArgs.secure:
			# Translators: Reported when current configuration cannot be saved while NVDA is running in secure mode such as in Windows login screen.
			queueHandler.queueFunction(queueHandler.eventQueue,ui.message,_("Cannot save configuration - NVDA in secure mode"))
			return
		try:
			config.conf.save()
			# Translators: Reported when current configuration has been saved.
			queueHandler.queueFunction(queueHandler.eventQueue,ui.message,_("Configuration saved"))
		except:
			# Translators: Message shown when current configuration cannot be saved such as when running NVDA from a CD.
			messageBox(_("Could not save configuration - probably read only file system"),_("Error"),wx.OK | wx.ICON_ERROR)

	def _popupSettingsDialog(self, dialog, *args, **kwargs):
		if isInMessageBox:
			return
		self.prePopup()
		try:
			dialog(self, *args, **kwargs).Show()
		except SettingsDialog.MultiInstanceError:
			# Translators: Message shown when attempting to open another NVDA settings dialog when one is already open
			# (example: when trying to open keyboard settings when general settings dialog is open).
			messageBox(_("An NVDA settings dialog is already open. Please close it first."),_("Error"),style=wx.OK | wx.ICON_ERROR)
		except MultiCategorySettingsDialog.CategoryUnavailableError:
			# Translators: Message shown when trying to open an unavailable category of a multi category settings dialog
			# (example: when trying to open touch interaction settings on an unsupported system).
			messageBox(_("The settings panel you tried to open is unavailable on this system."),_("Error"),style=wx.OK | wx.ICON_ERROR)

		self.postPopup()

	def onDefaultDictionaryCommand(self,evt):
		# Translators: Title for default speech dictionary dialog.
		self._popupSettingsDialog(DictionaryDialog,_("Default dictionary"),speechDictHandler.dictionaries["default"])

	def onVoiceDictionaryCommand(self,evt):
		# Translators: Title for voice dictionary for the current voice such as current eSpeak variant.
		self._popupSettingsDialog(DictionaryDialog,_("Voice dictionary (%s)")%speechDictHandler.dictionaries["voice"].fileName,speechDictHandler.dictionaries["voice"])

	def onTemporaryDictionaryCommand(self,evt):
		# Translators: Title for temporary speech dictionary dialog (the voice dictionary that is active as long as NvDA is running).
		self._popupSettingsDialog(DictionaryDialog,_("Temporary dictionary"),speechDictHandler.dictionaries["temp"])

	def onExecuteUpdateCommand(self, evt):
		if updateCheck and updateCheck.isPendingUpdate():
			destPath, version, apiVersion, backCompatToAPIVersion = updateCheck.getPendingUpdate()
			from addonHandler import getIncompatibleAddons
			if any(getIncompatibleAddons(apiVersion, backCompatToAPIVersion)):
				confirmUpdateDialog = updateCheck.UpdateAskInstallDialog(
					parent=gui.mainFrame,
					destPath=destPath,
					version=version,
					apiVersion=apiVersion,
					backCompatTo=backCompatToAPIVersion
				)
				gui.runScriptModalDialog(confirmUpdateDialog)
			else:
				updateCheck.executePendingUpdate()

	def evaluateUpdatePendingUpdateMenuItemCommand(self):
		try:
			self.sysTrayIcon.menu.Remove(self.sysTrayIcon.installPendingUpdateMenuItem)
		except:
			log.debug("Error while removing  pending update menu item", exc_info=True)
			pass
		if not globalVars.appArgs.secure and updateCheck and updateCheck.isPendingUpdate():
			self.sysTrayIcon.menu.Insert(self.sysTrayIcon.installPendingUpdateMenuItemPos,self.sysTrayIcon.installPendingUpdateMenuItem)

	def onExitCommand(self, evt):
		if config.conf["general"]["askToExit"]:
			self.prePopup()
			d = ExitDialog(self)
			d.Raise()
			d.Show()
			self.postPopup()
		else:
			wx.GetApp().ExitMainLoop()

	def onNVDASettingsCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog)

	def onGeneralSettingsCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, GeneralSettingsPanel)

	def onSelectSynthesizerCommand(self,evt):
		self._popupSettingsDialog(SynthesizerSelectionDialog)

	def onSpeechSettingsCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, SpeechSettingsPanel)

	def onSelectBrailleDisplayCommand(self,evt):
		self._popupSettingsDialog(BrailleDisplaySelectionDialog)

	def onBrailleSettingsCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, BrailleSettingsPanel)

	def onKeyboardSettingsCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, KeyboardSettingsPanel)

	def onMouseSettingsCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, MouseSettingsPanel)

	def onTouchInteractionCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, TouchInteractionPanel)

	def onReviewCursorCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, ReviewCursorPanel)

	def onInputCompositionCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, InputCompositionPanel)

	def onObjectPresentationCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, ObjectPresentationPanel)

	def onBrowseModeCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, BrowseModePanel)

	def onDocumentFormattingCommand(self,evt):
		self._popupSettingsDialog(NVDASettingsDialog, DocumentFormattingPanel)

	def onUwpOcrCommand(self, evt):
		self._popupSettingsDialog(NVDASettingsDialog, UwpOcrPanel)

	def onSpeechSymbolsCommand(self, evt):
		self._popupSettingsDialog(SpeechSymbolsDialog)

	def onInputGesturesCommand(self, evt):
		self._popupSettingsDialog(InputGesturesDialog)

	def onAboutCommand(self,evt):
		# Translators: The title of the dialog to show about info for NVDA.
		messageBox(versionInfo.aboutMessage, _("About NVDA"), wx.OK)

	def onCheckForUpdateCommand(self, evt):
		updateCheck.UpdateChecker().check()

	def onViewLogCommand(self, evt):
		logViewer.activate()

	def onSpeechViewerEnabled(self, isEnabled):
		# its possible for this to be called after the sysTrayIcon is destroyed if we are exiting NVDA
		if self.sysTrayIcon and self.sysTrayIcon.menu_tools_toggleSpeechViewer:
			self.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(isEnabled)

	def onToggleSpeechViewerCommand(self, evt):
		if not speechViewer.isActive:
			speechViewer.activate()
		else:
			speechViewer.deactivate()

	def onBrailleViewerChangedState(self, created):
		# its possible for this to be called after the sysTrayIcon is destroyed if we are exiting NVDA
		if self.sysTrayIcon and self.sysTrayIcon.menu_tools_toggleBrailleViewer:
			self.sysTrayIcon.menu_tools_toggleBrailleViewer.Check(created)

	def onToggleBrailleViewerCommand(self, evt):
		import brailleViewer
		if brailleViewer.isBrailleViewerActive():
			brailleViewer.destroyBrailleViewer()
		else:
			brailleViewer.createBrailleViewerTool()

	def onPythonConsoleCommand(self, evt):
		import pythonConsole
		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		pythonConsole.activate()

	def onAddonsManagerCommand(self,evt):
		if isInMessageBox:
			return
		self.prePopup()
		from .addonGui import AddonsDialog
		d=AddonsDialog(gui.mainFrame)
		d.Show()
		self.postPopup()

	def onReloadPluginsCommand(self, evt):
		import appModuleHandler, globalPluginHandler
		from NVDAObjects import NVDAObject
		appModuleHandler.reloadAppModules()
		globalPluginHandler.reloadGlobalPlugins()
		NVDAObject.clearDynamicClassCache()

	def onCreatePortableCopyCommand(self,evt):
		if isInMessageBox:
			return
		self.prePopup()
		import gui.installerGui
		d=gui.installerGui.PortableCreaterDialog(gui.mainFrame)
		d.Show()
		self.postPopup()

	def onInstallCommand(self, evt):
		if isInMessageBox:
			return
		from gui import installerGui
		installerGui.showInstallGui()

	def onRunCOMRegistrationFixesCommand(self, evt):
		if isInMessageBox:
			return
		if gui.messageBox(
			# Translators: A message to warn the user when starting the COM Registration Fixing tool 
			_("You are about to run the COM Registration Fixing tool. This tool will try to fix common system problems that stop NVDA from being able to access content in many programs including Firefox and Internet Explorer. This tool must make changes to the System registry and therefore requires administrative access. Are you sure you wish to proceed?"),
			# Translators: The title of the warning dialog displayed when launching the COM Registration Fixing tool 
			_("Warning"),wx.YES|wx.NO|wx.ICON_WARNING,self
		)==wx.NO:
			return
		progressDialog = IndeterminateProgressDialog(mainFrame,
			# Translators: The title of the dialog presented while NVDA is running the COM Registration fixing tool 
			_("COM Registration Fixing Tool"),
			# Translators: The message displayed while NVDA is running the COM Registration fixing tool 
			_("Please wait while NVDA tries to fix your system's COM registrations.")
		)
		try:
			import systemUtils
			systemUtils.execElevated(config.SLAVE_FILENAME, ["fixCOMRegistrations"])
		except:
			log.error("Could not execute fixCOMRegistrations command",exc_info=True) 
		progressDialog.done()
		del progressDialog
		# Translators: The message displayed when the COM Registration Fixing tool completes.
		gui.messageBox(_("COM Registration Fixing tool complete"),
			# Translators: The title of a dialog presented when the COM Registration Fixing tool is complete. 
			_("COM Registration Fixing Tool"),
			wx.OK)

	def onConfigProfilesCommand(self, evt):
		if isInMessageBox:
			return
		self.prePopup()
		from .configProfiles import ProfilesDialog
		ProfilesDialog(gui.mainFrame).Show()
		self.postPopup()

class SysTrayIcon(wx.adv.TaskBarIcon):

	def __init__(self, frame):
		super(SysTrayIcon, self).__init__()
		icon=wx.Icon(ICON_PATH,wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon, versionInfo.name)

		self.menu=wx.Menu()
		menu_preferences=self.preferencesMenu=wx.Menu()
		item = menu_preferences.Append(wx.ID_ANY,
			# Translators: The label for the menu item to open NVDA Settings dialog.
			_("&Settings..."),
			# Translators: The description for the menu item to open NVDA Settings dialog.
			_("NVDA settings"))
		self.Bind(wx.EVT_MENU, frame.onNVDASettingsCommand, item)
		subMenu_speechDicts = wx.Menu()
		if not globalVars.appArgs.secure:
			item = subMenu_speechDicts.Append(
				wx.ID_ANY,
				# Translators: The label for the menu item to open Default speech dictionary dialog.
				_("&Default dictionary..."),
				# Translators: The help text for the menu item to open Default speech dictionary dialog.
				_("A dialog where you can set default dictionary by adding dictionary entries to the list")
			)
			self.Bind(wx.EVT_MENU, frame.onDefaultDictionaryCommand, item)
			item = subMenu_speechDicts.Append(
				wx.ID_ANY,
				# Translators: The label for the menu item to open Voice specific speech dictionary dialog.
				_("&Voice dictionary..."),
				_(
					# Translators: The help text for the menu item
					# to open Voice specific speech dictionary dialog.
					"A dialog where you can set voice-specific dictionary by adding"
					" dictionary entries to the list"
				)
			)
			self.Bind(wx.EVT_MENU, frame.onVoiceDictionaryCommand, item)
		item = subMenu_speechDicts.Append(
			wx.ID_ANY,
			# Translators: The label for the menu item to open Temporary speech dictionary dialog.
			_("&Temporary dictionary..."),
			# Translators: The help text for the menu item to open Temporary speech dictionary dialog.
			_("A dialog where you can set temporary dictionary by adding dictionary entries to the edit box")
		)
		self.Bind(wx.EVT_MENU, frame.onTemporaryDictionaryCommand, item)
		# Translators: The label for a submenu under NvDA Preferences menu to select speech dictionaries.
		menu_preferences.AppendSubMenu(subMenu_speechDicts,_("Speech &dictionaries"))
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open Punctuation/symbol pronunciation dialog.
			item = menu_preferences.Append(wx.ID_ANY, _("&Punctuation/symbol pronunciation..."))
			self.Bind(wx.EVT_MENU, frame.onSpeechSymbolsCommand, item)
			# Translators: The label for the menu item to open the Input Gestures dialog.
			item = menu_preferences.Append(wx.ID_ANY, _("I&nput gestures..."))
			self.Bind(wx.EVT_MENU, frame.onInputGesturesCommand, item)
		# Translators: The label for Preferences submenu in NVDA menu.
		self.menu.AppendSubMenu(menu_preferences,_("&Preferences"))

		menu_tools = self.toolsMenu = wx.Menu()
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open NVDA Log Viewer.
			item = menu_tools.Append(wx.ID_ANY, _("View log"))
			self.Bind(wx.EVT_MENU, frame.onViewLogCommand, item)
		# Translators: The label for the menu item to toggle Speech Viewer.
		item=self.menu_tools_toggleSpeechViewer = menu_tools.AppendCheckItem(wx.ID_ANY, _("Speech viewer"))
		self.Bind(wx.EVT_MENU, frame.onToggleSpeechViewerCommand, item)

		self.menu_tools_toggleBrailleViewer: wx.MenuItem = menu_tools.AppendCheckItem(
			wx.ID_ANY,
			# Translators: The label for the menu item to toggle Braille Viewer.
			_("Braille viewer")
		)
		item = self.menu_tools_toggleBrailleViewer
		self.Bind(wx.EVT_MENU, frame.onToggleBrailleViewerCommand, item)
		import brailleViewer
		self.menu_tools_toggleBrailleViewer.Check(brailleViewer.isBrailleViewerActive())
		brailleViewer.postBrailleViewerToolToggledAction.register(frame.onBrailleViewerChangedState)

		if not globalVars.appArgs.secure and not config.isAppX:
			# Translators: The label for the menu item to open NVDA Python Console.
			item = menu_tools.Append(wx.ID_ANY, _("Python console"))
			self.Bind(wx.EVT_MENU, frame.onPythonConsoleCommand, item)
			# Translators: The label of a menu item to open the Add-ons Manager.
			item = menu_tools.Append(wx.ID_ANY, _("Manage &add-ons..."))
			self.Bind(wx.EVT_MENU, frame.onAddonsManagerCommand, item)
		if not globalVars.appArgs.secure and not config.isAppX and getattr(sys,'frozen',None):
			# Translators: The label for the menu item to create a portable copy of NVDA from an installed or another portable version.
			item = menu_tools.Append(wx.ID_ANY, _("Create portable copy..."))
			self.Bind(wx.EVT_MENU, frame.onCreatePortableCopyCommand, item)
			if not config.isInstalledCopy():
				# Translators: The label for the menu item to install NVDA on the computer.
				item = menu_tools.Append(wx.ID_ANY, _("&Install NVDA..."))
				self.Bind(wx.EVT_MENU, frame.onInstallCommand, item)
			# Translators: The label for the menu item to run the COM registration fix tool 
			item = menu_tools.Append(wx.ID_ANY, _("Run COM Registration Fixing tool..."))
			self.Bind(wx.EVT_MENU, frame.onRunCOMRegistrationFixesCommand, item)
		if not config.isAppX:
			# Translators: The label for the menu item to reload plugins.
			item = menu_tools.Append(wx.ID_ANY, _("Reload plugins"))
			self.Bind(wx.EVT_MENU, frame.onReloadPluginsCommand, item)
		# Translators: The label for the Tools submenu in NVDA menu.
		self.menu.AppendSubMenu(menu_tools,_("Tools"))

		menu_help = self.helpMenu = wx.Menu()
		if not globalVars.appArgs.secure:
			# Translators: The label of a menu item to open NVDA user guide.
			item = menu_help.Append(wx.ID_ANY, _("&User Guide"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("userGuide.html")), item)
			# Translators: The label of a menu item to open the Commands Quick Reference document.
			item = menu_help.Append(wx.ID_ANY, _("Commands &Quick Reference"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("keyCommands.html")), item)
			# Translators: The label for the menu item to open What's New document.
			item = menu_help.Append(wx.ID_ANY, _("What's &new"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("changes.html")), item)
			item = menu_help.Append(wx.ID_ANY, _("NVDA &web site"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile("http://www.nvda-project.org/"), item)
			# Translators: The label for the menu item to view NVDA License document.
			item = menu_help.Append(wx.ID_ANY, _("L&icense"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("copying.txt", False)), item)
			# Translators: The label for the menu item to view NVDA Contributors list document.
			item = menu_help.Append(wx.ID_ANY, _("C&ontributors"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("contributors.txt", False)), item)
			# Translators: The label for the menu item to open NVDA Welcome Dialog.
			item = menu_help.Append(wx.ID_ANY, _("We&lcome dialog..."))
			self.Bind(wx.EVT_MENU, lambda evt: WelcomeDialog.run(), item)
			menu_help.AppendSeparator()
		if updateCheck:
			# Translators: The label of a menu item to manually check for an updated version of NVDA.
			item = menu_help.Append(wx.ID_ANY, _("&Check for update..."))
			self.Bind(wx.EVT_MENU, frame.onCheckForUpdateCommand, item)
		# Translators: The label for the menu item to open About dialog to get information about NVDA.
		item = menu_help.Append(wx.ID_ABOUT, _("About..."), _("About NVDA"))
		self.Bind(wx.EVT_MENU, frame.onAboutCommand, item)
		# Translators: The label for the Help submenu in NVDA menu.
		self.menu.AppendSubMenu(menu_help,_("&Help"))
		self.menu.AppendSeparator()
		# Translators: The label for the menu item to open the Configuration Profiles dialog.
		item = self.menu.Append(wx.ID_ANY, _("&Configuration profiles..."))
		self.Bind(wx.EVT_MENU, frame.onConfigProfilesCommand, item)
		# Translators: The label for the menu item to revert to saved configuration.
		item = self.menu.Append(wx.ID_ANY, _("&Revert to saved configuration"),_("Reset all settings to saved state"))
		self.Bind(wx.EVT_MENU, frame.onRevertToSavedConfigurationCommand, item)
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to reset settings to default settings.
			# Here, default settings means settings that were there when the user first used NVDA.
			item = self.menu.Append(wx.ID_ANY, _("&Reset configuration to factory defaults"),_("Reset all settings to default state"))
			self.Bind(wx.EVT_MENU, frame.onRevertToDefaultConfigurationCommand, item)
			# Translators: The label for the menu item to save current settings.
			item = self.menu.Append(wx.ID_SAVE, _("&Save configuration"), _("Write the current configuration to nvda.ini"))
			self.Bind(wx.EVT_MENU, frame.onSaveConfigurationCommand, item)
			self.menu.AppendSeparator()
			# Translators: The label for the menu item to open donate page.
			item = self.menu.Append(wx.ID_ANY, _("Donate"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(DONATE_URL), item)
			self.installPendingUpdateMenuItemPos = self.menu.GetMenuItemCount()
			item = self.installPendingUpdateMenuItem = self.menu.Append(wx.ID_ANY,
				# Translators: The label for the menu item to run a pending update.
				_("Install pending &update"),
				# Translators: The description for the menu item to run a pending update.
				_("Execute a previously downloaded NVDA update"))
			self.Bind(wx.EVT_MENU, frame.onExecuteUpdateCommand, item)
		self.menu.AppendSeparator()
		item = self.menu.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		self.Bind(wx.EVT_MENU, frame.onExitCommand, item)

		self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.onActivate)
		self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.onActivate)

	def Destroy(self):
		self.menu.Destroy()
		super(SysTrayIcon, self).Destroy()

	def onActivate(self, evt):
		mainFrame.prePopup()
		import appModules.nvda
		if not appModules.nvda.nvdaMenuIaIdentity:
			# The NVDA app module doesn't know how to identify the NVDA menu yet.
			# Signal that the NVDA menu has just been opened.
			appModules.nvda.nvdaMenuIaIdentity = True
		self.PopupMenu(self.menu)
		if appModules.nvda.nvdaMenuIaIdentity is True:
			# The NVDA menu didn't actually appear for some reason.
			appModules.nvda.nvdaMenuIaIdentity = None
		mainFrame.postPopup()

def initialize():
	global mainFrame
	if mainFrame:
		raise RuntimeError("GUI already initialized")
	mainFrame = MainFrame()
	wx.GetApp().SetTopWindow(mainFrame)

def terminate():
	import brailleViewer
	brailleViewer.destroyBrailleViewer()

	for instance, state in gui.SettingsDialog._instances.items():
		if state is gui.SettingsDialog._DIALOG_DESTROYED_STATE:
			log.error(
				"Destroyed but not deleted instance of settings dialog exists: {!r}".format(instance)
			)
		else:
			log.debug("Exiting NVDA with an open settings dialog: {!r}".format(instance))
	global mainFrame
	# This is called after the main loop exits because WM_QUIT exits the main loop
	# without destroying all objects correctly and we need to support WM_QUIT.
	# Therefore, any request to exit should exit the main loop.
	wx.CallAfter(mainFrame.Destroy)
	# #4460: We need another iteration of the main loop
	# so that everything (especially the TaskBarIcon) is cleaned up properly.
	# ProcessPendingEvents doesn't seem to work, but MainLoop does.
	# Because the top window gets destroyed,
	# MainLoop thankfully returns pretty quickly.
	wx.GetApp().MainLoop()
	mainFrame = None

def showGui():
 	wx.CallAfter(mainFrame.showGui)

def quit():
	wx.CallAfter(mainFrame.onExitCommand, None)

def messageBox(message, caption=wx.MessageBoxCaptionStr, style=wx.OK | wx.CENTER, parent=None):
	"""Display a message dialog.
	This should be used for all message dialogs
	rather than using C{wx.MessageDialog} and C{wx.MessageBox} directly.
	@param message: The message text.
	@type message: str
	@param caption: The caption (title) of the dialog.
	@type caption: str
	@param style: Same as for wx.MessageBox.
	@type style: int
	@param parent: The parent window (optional).
	@type parent: C{wx.Window}
	@return: Same as for wx.MessageBox.
	@rtype: int
	"""
	global isInMessageBox
	wasAlready = isInMessageBox
	isInMessageBox = True
	if not parent:
		mainFrame.prePopup()
	res = wx.MessageBox(message, caption, style, parent or mainFrame)
	if not parent:
		mainFrame.postPopup()
	if not wasAlready:
		isInMessageBox = False
	return res

def runScriptModalDialog(dialog, callback=None):
	"""Run a modal dialog from a script.
	This will not block the caller,
	but will instead call C{callback} (if provided) with the result from the dialog.
	The dialog will be destroyed once the callback has returned.
	@param dialog: The dialog to show.
	@type dialog: C{wx.Dialog}
	@param callback: The optional callable to call with the result from the dialog.
	@type callback: callable
	"""
	def run():
		mainFrame.prePopup()
		res = dialog.ShowModal()
		mainFrame.postPopup()
		if callback:
			callback(res)
		dialog.Destroy()
	wx.CallAfter(run)

class WelcomeDialog(wx.Dialog):
	"""The NVDA welcome dialog.
	This provides essential information for new users, such as a description of the NVDA key and instructions on how to activate the NVDA menu.
	It also provides quick access to some important configuration options.
	This dialog is displayed the first time NVDA is started with a new configuration.
	"""

	WELCOME_MESSAGE_DETAIL = _(
		# Translators: The main message for the Welcome dialog when the user starts NVDA for the first time.
		"Most commands for controlling NVDA require you to hold down"
		" the NVDA key while pressing other keys.\n"
		"By default, the numpad Insert and main Insert keys may both be used as the NVDA key.\n"
		"You can also configure NVDA to use the CapsLock as the NVDA key.\n"
		"Press NVDA+n at any time to activate the NVDA menu.\n"
		"From this menu, you can configure NVDA, get help and access other NVDA functions."
	)

	def __init__(self, parent):
		# Translators: The title of the Welcome dialog when user starts NVDA for the first time.
		super(WelcomeDialog, self).__init__(parent, wx.ID_ANY, _("Welcome to NVDA"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		# Translators: The header for the Welcome dialog when user starts NVDA for the first time. This is in larger,
		# bold lettering 
		welcomeTextHeader = wx.StaticText(self, label=_("Welcome to NVDA!"))
		welcomeTextHeader.SetFont(wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.NORMAL, wx.BOLD))
		mainSizer.AddSpacer(guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		mainSizer.Add(welcomeTextHeader,border=20,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
		mainSizer.AddSpacer(guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		welcomeTextDetail = wx.StaticText(self, wx.ID_ANY, self.WELCOME_MESSAGE_DETAIL)
		mainSizer.Add(welcomeTextDetail,border=20,flag=wx.EXPAND|wx.LEFT|wx.RIGHT)

		optionsSizer = wx.StaticBoxSizer(
			wx.StaticBox(
				self,
				# Translators: The label for a group box containing the NVDA welcome dialog options.
				label=_("Options")
			),
			wx.VERTICAL
		)
		sHelper = guiHelper.BoxSizerHelper(self, sizer=optionsSizer)
		# Translators: The label of a combobox in the Welcome dialog.
		kbdLabelText = _("&Keyboard layout:")
		layouts = keyboardHandler.KeyboardInputGesture.LAYOUTS
		self.kbdNames = sorted(layouts)
		kbdChoices = [layouts[layout] for layout in self.kbdNames]
		self.kbdList = sHelper.addLabeledControl(kbdLabelText, wx.Choice, choices=kbdChoices)
		try:
			index = self.kbdNames.index(config.conf["keyboard"]["keyboardLayout"])
			self.kbdList.SetSelection(index)
		except:
			log.error("Could not set Keyboard layout list to current layout",exc_info=True) 
		# Translators: The label of a checkbox in the Welcome dialog.
		capsAsNVDAModifierText = _("&Use CapsLock as an NVDA modifier key")
		self.capsAsNVDAModifierCheckBox = sHelper.addItem(wx.CheckBox(self, label=capsAsNVDAModifierText))
		self.capsAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"])
		# Translators: The label of a checkbox in the Welcome dialog.
		startAfterLogonText = _("St&art NVDA after I sign in")
		self.startAfterLogonCheckBox = sHelper.addItem(wx.CheckBox(self, label=startAfterLogonText))
		self.startAfterLogonCheckBox.Value = config.getStartAfterLogon()
		if globalVars.appArgs.secure or config.isAppX or not config.isInstalledCopy():
			self.startAfterLogonCheckBox.Disable()
		# Translators: The label of a checkbox in the Welcome dialog.
		showWelcomeDialogAtStartupText = _("&Show this dialog when NVDA starts")
		self.showWelcomeDialogAtStartupCheckBox = sHelper.addItem(wx.CheckBox(self, label=showWelcomeDialogAtStartupText))
		self.showWelcomeDialogAtStartupCheckBox.SetValue(config.conf["general"]["showWelcomeDialogAtStartup"])
		mainSizer.Add(optionsSizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Add(self.CreateButtonSizer(wx.OK), border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL|wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.kbdList.SetFocus()
		self.CentreOnScreen()

	def onOk(self, evt):
		layout = self.kbdNames[self.kbdList.GetSelection()]
		config.conf["keyboard"]["keyboardLayout"] = layout
		config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"] = self.capsAsNVDAModifierCheckBox.IsChecked()
		if self.startAfterLogonCheckBox.Enabled:
			config.setStartAfterLogon(self.startAfterLogonCheckBox.Value)
		config.conf["general"]["showWelcomeDialogAtStartup"] = self.showWelcomeDialogAtStartupCheckBox.IsChecked()
		try:
			config.conf.save()
		except:
			log.debugWarning("Could not save",exc_info=True)
		self.EndModal(wx.ID_OK)

	@classmethod
	def run(cls):
		"""Prepare and display an instance of this dialog.
		This does not require the dialog to be instantiated.
		"""
		mainFrame.prePopup()
		d = cls(mainFrame)
		d.ShowModal()
		d.Destroy()
		mainFrame.postPopup()

class LauncherDialog(wx.Dialog):
	"""The dialog that is displayed when NVDA is started from the launcher.
	This displays the license and allows the user to install or create a portable copy of NVDA.
	"""

	def __init__(self, parent):
		super(LauncherDialog, self).__init__(parent, title=versionInfo.name)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: The label of the license text which will be shown when NVDA installation program starts.
		groupLabel = _("License Agreement")
		sizer = sHelper.addItem(wx.StaticBoxSizer(wx.StaticBox(self, label=groupLabel), wx.VERTICAL))
		licenseTextCtrl = wx.TextCtrl(self, size=(500, 400), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		licenseTextCtrl.Value = codecs.open(getDocFilePath("copying.txt", False), "r", encoding="UTF-8").read()
		sizer.Add(licenseTextCtrl)

		# Translators: The label for a checkbox in NvDA installation program to agree to the license agreement.
		agreeText = _("I &agree")
		self.licenseAgreeCheckbox = sHelper.addItem(wx.CheckBox(self, label=agreeText))
		self.licenseAgreeCheckbox.Value = False
		self.licenseAgreeCheckbox.Bind(wx.EVT_CHECKBOX, self.onLicenseAgree)

		sizer = sHelper.addItem(wx.GridSizer(2, 2, 0, 0))
		self.actionButtons = []
		# Translators: The label of the button in NVDA installation program to install NvDA on the user's computer.
		ctrl = wx.Button(self, label=_("&Install NVDA on this computer"))
		sizer.Add(ctrl)
		ctrl.Bind(wx.EVT_BUTTON, lambda evt: self.onAction(evt, mainFrame.onInstallCommand))
		self.actionButtons.append(ctrl)
		# Translators: The label of the button in NVDA installation program to create a portable version of NVDA.
		ctrl = wx.Button(self, label=_("Create &portable copy"))
		sizer.Add(ctrl)
		ctrl.Bind(wx.EVT_BUTTON, lambda evt: self.onAction(evt, mainFrame.onCreatePortableCopyCommand))
		self.actionButtons.append(ctrl)
		# Translators: The label of the button in NVDA installation program to continue using the installation program as a temporary copy of NVDA.
		ctrl = wx.Button(self, label=_("&Continue running"))
		sizer.Add(ctrl)
		ctrl.Bind(wx.EVT_BUTTON, self.onContinueRunning)
		self.actionButtons.append(ctrl)
		sizer.Add(wx.Button(self, label=_("E&xit"), id=wx.ID_CANCEL))
		# If we bind this on the button, it fails to trigger when the dialog is closed.
		self.Bind(wx.EVT_BUTTON, self.onExit, id=wx.ID_CANCEL)

		for ctrl in self.actionButtons:
			ctrl.Disable()

		mainSizer.Add(sHelper.sizer, border = guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onLicenseAgree(self, evt):
		for ctrl in self.actionButtons:
			ctrl.Enable(evt.IsChecked())

	def onAction(self, evt, func):
		self.Destroy()
		func(evt)

	def onContinueRunning(self, evt):
		self.Destroy()
		core.doStartupDialogs()

	def onExit(self, evt):
		wx.GetApp().ExitMainLoop()

	@classmethod
	def run(cls):
		"""Prepare and display an instance of this dialog.
		This does not require the dialog to be instantiated.
		"""
		mainFrame.prePopup()
		d = cls(mainFrame)
		d.Show()
		mainFrame.postPopup()

class ExitDialog(wx.Dialog):
	_instance = None

	def __new__(cls, parent):
		# Make this a singleton.
		inst = cls._instance() if cls._instance else None
		if not inst:
			return super(cls, cls).__new__(cls, parent)
		return inst

	def __init__(self, parent):
		inst = ExitDialog._instance() if ExitDialog._instance else None
		if inst:
			return
		# Use a weakref so the instance can die.
		ExitDialog._instance = weakref.ref(self)
		# Translators: The title of the dialog to exit NVDA
		super(ExitDialog, self).__init__(parent, title=_("Exit NVDA"))
		dialog = self
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		contentSizerHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		if globalVars.appArgs.disableAddons:
			# Translators: A message in the exit Dialog shown when all add-ons are disabled.
			addonsDisabledText = _("All add-ons are now disabled. They will be re-enabled on the next restart unless you choose to disable them again.")
			contentSizerHelper.addItem(wx.StaticText(self, wx.ID_ANY, label=addonsDisabledText))

		# Translators: The label for actions list in the Exit dialog.
		labelText=_("What would you like to &do?")
		self.actions = [
			# Translators: An option in the combo box to choose exit action.
			_("Exit"),
			# Translators: An option in the combo box to choose exit action.
			_("Restart")
		]
		# Windows Store version of NVDA does not support add-ons yet.
		if not config.isAppX:
			# Translators: An option in the combo box to choose exit action.
			self.actions.append(_("Restart with add-ons disabled"))
		# Translators: An option in the combo box to choose exit action.
		self.actions.append(_("Restart with debug logging enabled"))
		if updateCheck and updateCheck.isPendingUpdate():
			# Translators: An option in the combo box to choose exit action.
			self.actions.append(_("Install pending update"))
		self.actionsList = contentSizerHelper.addLabeledControl(labelText, wx.Choice, choices=self.actions)
		self.actionsList.SetSelection(0)

		contentSizerHelper.addDialogDismissButtons(wx.OK | wx.CANCEL)

		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Add(contentSizerHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.actionsList.SetFocus()
		self.CentreOnScreen()

	def onOk(self, evt):
		action=self.actionsList.GetSelection()
		# Because Windows Store version of NVDA does not support add-ons yet, add 1 if action is 2 or above if this is such a case.
		if action >= 2 and config.isAppX:
			action += 1
		if action == 0:
			wx.GetApp().ExitMainLoop()
		elif action == 1:
			queueHandler.queueFunction(queueHandler.eventQueue,core.restart)
		elif action == 2:
			queueHandler.queueFunction(queueHandler.eventQueue,core.restart,disableAddons=True)
		elif action == 3:
			queueHandler.queueFunction(queueHandler.eventQueue,core.restart,debugLogging=True)
		elif action == 4:
			if updateCheck:
				destPath, version, apiVersion, backCompatTo = updateCheck.getPendingUpdate()
				from addonHandler import getIncompatibleAddons
				if any(getIncompatibleAddons(currentAPIVersion=apiVersion, backCompatToAPIVersion=backCompatTo)):
					confirmUpdateDialog = updateCheck.UpdateAskInstallDialog(
						parent=gui.mainFrame,
						destPath=destPath,
						version=version,
						apiVersion=apiVersion,
						backCompatTo=backCompatTo
					)
					confirmUpdateDialog.ShowModal()
				else:
					updateCheck.executePendingUpdate()
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

class ExecAndPump(threading.Thread):
	"""Executes the given function with given args and kwargs in a background thread while blocking and pumping in the current thread."""

	def __init__(self,func,*args,**kwargs):
		self.func=func
		self.args=args
		self.kwargs=kwargs
		fname = repr(func)
		super().__init__(
			name=f"{self.__class__.__module__}.{self.__class__.__qualname__}({fname})"
		)
		self.threadExc=None
		self.start()
		time.sleep(0.1)
		threadHandle=ctypes.c_int()
		threadHandle.value=ctypes.windll.kernel32.OpenThread(0x100000,False,self.ident)
		msg=ctypes.wintypes.MSG()
		while ctypes.windll.user32.MsgWaitForMultipleObjects(1,ctypes.byref(threadHandle),False,-1,255)==1:
			while ctypes.windll.user32.PeekMessageW(ctypes.byref(msg),None,0,0,1):
				ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
				ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))
		if self.threadExc:
			raise self.threadExc

	def run(self):
		try:
			self.func(*self.args,**self.kwargs)
		except Exception as e:
			self.threadExc=e
			log.debugWarning("task had errors",exc_info=True)

class IndeterminateProgressDialog(wx.ProgressDialog):

	def __init__(self, parent, title, message):
		super(IndeterminateProgressDialog, self).__init__(title, message, parent=parent)
		self._speechCounter = -1
		self.timer = wx.PyTimer(self.Pulse)
		self.timer.Start(1000)
		self.Raise()
		self.CentreOnScreen()

	def Pulse(self):
		super(IndeterminateProgressDialog, self).Pulse()
		# We want progress to be spoken on the first pulse and every 10 pulses thereafter.
		# Therefore, cycle from 0 to 9 inclusive.
		self._speechCounter = (self._speechCounter + 1) % 10
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] == "off":
			return
		if not pbConf["reportBackgroundProgressBars"] and not self.IsActive():
			return
		if pbConf["progressBarOutputMode"] in ("beep", "both"):
			tones.beep(440, 40)
		if pbConf["progressBarOutputMode"] in ("speak", "both") and self._speechCounter == 0:
			# Translators: Announced periodically to indicate progress for an indeterminate progress bar.
			speech.speakMessage(_("Please wait"))

	def IsActive(self):
		#4714: In wxPython 3, ProgressDialog.IsActive always seems to return False.
		return winUser.isDescendantWindow(winUser.getForegroundWindow(), self.Handle)

	def done(self):
		self.timer.Stop()
		pbConf = config.conf["presentation"]["progressBarUpdates"]
		if pbConf["progressBarOutputMode"] in ("beep", "both") and (pbConf["reportBackgroundProgressBars"] or self.IsActive()):
			tones.beep(1760, 40)
		self.Hide()
		self.Destroy()

def shouldConfigProfileTriggersBeSuspended():
	"""Determine whether configuration profile triggers should be suspended in relation to NVDA's GUI.
	For NVDA configuration dialogs, the configuration should remain the same as it was before the GUI was popped up
	so the user can change settings in the correct profile.
	Top-level windows that require this behavior should have a C{shouldSuspendConfigProfileTriggers} attribute set to C{True}.
	Because these dialogs are often opened via the NVDA menu, this applies to the NVDA menu as well.
	"""
	if winUser.getGUIThreadInfo(ctypes.windll.kernel32.GetCurrentThreadId()).flags & 0x00000010:
		# The NVDA menu is active.
		return True
	for window in wx.GetTopLevelWindows():
		if window.IsShown() and getattr(window, "shouldSuspendConfigProfileTriggers", False):
			return True
	return False

class NonReEntrantTimer(wx.Timer):
	"""
	Before WXPython 4, wx.Timer was nonre-entrant, 
	meaning that if code within its callback pumped messages (E.g. called wx.Yield) and this timer was ready to fire again, 
	the timer would not fire until the first callback had completed.
	However, in WXPython 4, wx.Timer is now re-entrant.
	Code in NVDA is not written to handle re-entrant timers, so this class provides a Timer with the old behaviour.
	This should be used in place of wx.Timer and wx.PyTimer where the callback will directly or indirectly call wx.Yield or some how process the Windows window message queue. 
	For example, NVDA's core pump or other timers that run in NVDA's main thread.
	Timers on braille display drivers for key detection don't need to use this as they only queue gestures rather than actually executing them.  
	"""

	def __init__(self, run=None):
		if run is not None:
			self.run = run
		self._inNotify = False
		super(NonReEntrantTimer,self).__init__()

	def run(self):
		"""Subclasses can override or specify in constructor.
		"""
		raise NotImplementedError

	def Notify(self):
		if self._inNotify:
			return
		self._inNotify = True
		try:
			self.run()
		finally:
			self._inNotify = False

def _isDebug():
	return config.conf["debugLog"]["gui"]

class AskAllowUsageStatsDialog(wx.Dialog):
	"""A dialog asking if the user wishes to allow NVDA usage stats to be collected by NV Access."""

	def __init__(self, parent):
		# Translators: The title of the dialog asking if usage data can be collected 
		super(AskAllowUsageStatsDialog, self).__init__(parent, title=_("NVDA  Usage Data Collection"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		# Translators: A message asking the user if they want to allow usage stats gathering
		message=_("In order to improve NVDA in the future, NV Access wishes to collect usage data from running copies of NVDA.\n\n"
			"Data includes Operating System version, NVDA version, language, country of origin, plus certain NVDA configuration such as current synthesizer, braille display and braille table. " 
			"No spoken or braille content will be ever sent to NV Access.  Please refer to the User Guide for a current list of all data collected.\n\n"
			"Do you wish to allow NV Access to periodically collect this data in order to improve NVDA?")
		sText=sHelper.addItem(wx.StaticText(self, label=message))
		# the wx.Window must be constructed before we can get the handle.
		import windowUtils
		self.scaleFactor = windowUtils.getWindowScalingFactor(self.GetHandle())
		sText.Wrap(self.scaleFactor*600) # 600 was fairly arbitrarily chosen by a visual user to look acceptable on their machine.

		bHelper = sHelper.addDialogDismissButtons(guiHelper.ButtonHelper(wx.HORIZONTAL))

		# Translators: The label of a Yes button in a dialog 
		yesButton = bHelper.addButton(self, wx.ID_YES, label=_("&Yes"))
		yesButton.Bind(wx.EVT_BUTTON, self.onYesButton)

		# Translators: The label of a No button in a dialog 
		noButton = bHelper.addButton(self, wx.ID_NO, label=_("&No"))
		noButton.Bind(wx.EVT_BUTTON, self.onNoButton)

		# Translators: The label of a button to remind the user later about performing some action.
		remindMeButton = bHelper.addButton(self, wx.ID_CANCEL, label=_("Remind me &later"))
		remindMeButton.Bind(wx.EVT_BUTTON, self.onLaterButton)
		remindMeButton.SetFocus()

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onYesButton(self,evt):
		log.debug("Usage stats gathering has been allowed")
		config.conf['update']['askedAllowUsageStats']=True
		config.conf['update']['allowUsageStats']=True
		self.EndModal(wx.ID_YES)

	def onNoButton(self,evt):
		log.debug("Usage stats gathering has been disallowed")
		config.conf['update']['askedAllowUsageStats']=True
		config.conf['update']['allowUsageStats']=False
		self.EndModal(wx.ID_NO)

	def onLaterButton(self,evt):
		log.debug("Usage stats gathering question has been deferred")
		# evt.Skip() is called since wx.ID_CANCEL is used as the ID for the Ask Later button, 
		# wx automatically ends the modal itself.
		evt.Skip()
