# -*- coding: UTF-8 -*-
#gui/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2015 NV Access Limited, Peter Vágner, Aleksey Sadovoy, Mesar Hameed, Joseph Lee
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
import globalVars
import tones
import ui
from logHandler import log
import config
import versionInfo
import speech
import queueHandler
import core
from settingsDialogs import *
import speechDictHandler
import languageHandler
import logViewer
import speechViewer
import winUser
import api
try:
	import updateCheck
except RuntimeError:
	updateCheck = None

### Constants
NVDA_PATH = os.getcwdu()
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
		if not config.hasUiAccess():
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
		# Therefore, move the mouse to the centre of the screen so that the menu will always pop up there.
		left, top, width, height = api.getDesktopObject().location
		x = width / 2
		y = height / 2
		winUser.setCursorPos(x, y)
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
			# Translators: Message shown when attempting to open another NVDA settings dialog when one is already open (example: when trying to open keyboard settings when general settings dialog is open).
			messageBox(_("An NVDA settings dialog is already open. Please close it first."),_("Error"),style=wx.OK | wx.ICON_ERROR)
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

	def onExitCommand(self, evt):
		if config.conf["general"]["askToExit"]:
			self.prePopup()
			d = ExitDialog(self)
			d.Raise()
			d.Show()
			self.postPopup()
		else:
			wx.GetApp().ExitMainLoop()

	def onGeneralSettingsCommand(self,evt):
		self._popupSettingsDialog(GeneralSettingsDialog)

	def onSynthesizerCommand(self,evt):
		self._popupSettingsDialog(SynthesizerDialog)

	def onVoiceCommand(self,evt):
		self._popupSettingsDialog(VoiceSettingsDialog)

	def onBrailleCommand(self,evt):
		self._popupSettingsDialog(BrailleSettingsDialog)

	def onKeyboardSettingsCommand(self,evt):
		self._popupSettingsDialog(KeyboardSettingsDialog)

	def onMouseSettingsCommand(self,evt):
		self._popupSettingsDialog(MouseSettingsDialog)

	def onReviewCursorCommand(self,evt):
		self._popupSettingsDialog(ReviewCursorDialog)

	def onInputCompositionCommand(self,evt):
		self._popupSettingsDialog(InputCompositionDialog)

	def onObjectPresentationCommand(self,evt):
		self._popupSettingsDialog(ObjectPresentationDialog)

	def onBrowseModeCommand(self,evt):
		self._popupSettingsDialog(BrowseModeDialog)

	def onDocumentFormattingCommand(self,evt):
		self._popupSettingsDialog(DocumentFormattingDialog)

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

	def onToggleSpeechViewerCommand(self, evt):
		if not speechViewer.isActive:
			speechViewer.activate()
			self.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(True)
		else:
			speechViewer.deactivate()
			self.sysTrayIcon.menu_tools_toggleSpeechViewer.Check(False)

	def onPythonConsoleCommand(self, evt):
		import pythonConsole
		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		pythonConsole.activate()

	def onAddonsManagerCommand(self,evt):
		if isInMessageBox:
			return
		self.prePopup()
		from addonGui import AddonsDialog
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

	def onConfigProfilesCommand(self, evt):
		if isInMessageBox:
			return
		self.prePopup()
		from configProfiles import ProfilesDialog
		ProfilesDialog(gui.mainFrame).Show()
		self.postPopup()

class SysTrayIcon(wx.TaskBarIcon):

	def __init__(self, frame):
		super(SysTrayIcon, self).__init__()
		icon=wx.Icon(ICON_PATH,wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon, versionInfo.name)

		self.menu=wx.Menu()
		menu_preferences=self.preferencesMenu=wx.Menu()
		# Translators: The label for the menu item to open general Settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&General settings..."),_("General settings"))
		self.Bind(wx.EVT_MENU, frame.onGeneralSettingsCommand, item)
		# Translators: The label for the menu item to open Synthesizer settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&Synthesizer..."),_("Change the synthesizer to be used"))
		self.Bind(wx.EVT_MENU, frame.onSynthesizerCommand, item)
		# Translators: The label for the menu item to open Voice Settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&Voice settings..."),_("Choose the voice, rate, pitch and volume to use"))
		self.Bind(wx.EVT_MENU, frame.onVoiceCommand, item)
		# Translators: The label for the menu item to open Braille Settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("B&raille settings..."))
		self.Bind(wx.EVT_MENU, frame.onBrailleCommand, item)
		# Translators: The label for the menu item to open Keyboard Settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&Keyboard settings..."),_("Configure keyboard layout, speaking of typed characters, words or command keys"))
		self.Bind(wx.EVT_MENU, frame.onKeyboardSettingsCommand, item)
		# Translators: The label for the menu item to open Mouse Settings dialog.
		item = menu_preferences.Append(wx.ID_ANY, _("&Mouse settings..."),_("Change reporting of mouse shape and object under mouse"))
		self.Bind(wx.EVT_MENU, frame.onMouseSettingsCommand, item)
		# Translators: The label for the menu item to open Review Cursor dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("Review &cursor..."),_("Configure how and when the review cursor moves")) 
		self.Bind(wx.EVT_MENU, frame.onReviewCursorCommand, item)
		# Translators: The label for the menu item to open Input Composition Settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&Input composition settings..."),_("Configure how NVDA reports input composition and candidate selection for certain languages")) 
		self.Bind(wx.EVT_MENU, frame.onInputCompositionCommand, item)
		# Translators: The label for the menu item to open Object Presentation dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&Object presentation..."),_("Change reporting of objects")) 
		self.Bind(wx.EVT_MENU, frame.onObjectPresentationCommand, item)
		# Translators: The label for the menu item to open Browse Mode settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("&Browse mode..."),_("Change virtual buffers specific settings")) 
		self.Bind(wx.EVT_MENU, frame.onBrowseModeCommand, item)
		# Translators: The label for the menu item to open Document Formatting settings dialog.
		item = menu_preferences.Append(wx.ID_ANY,_("Document &formatting..."),_("Change settings of document properties")) 
		self.Bind(wx.EVT_MENU, frame.onDocumentFormattingCommand, item)
		subMenu_speechDicts = wx.Menu()
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open Default speech dictionary dialog.
			item = subMenu_speechDicts.Append(wx.ID_ANY,_("&Default dictionary..."),_("A dialog where you can set default dictionary by adding dictionary entries to the list"))
			self.Bind(wx.EVT_MENU, frame.onDefaultDictionaryCommand, item)
			# Translators: The label for the menu item to open Voice specific speech dictionary dialog.
			item = subMenu_speechDicts.Append(wx.ID_ANY,_("&Voice dictionary..."),_("A dialog where you can set voice-specific dictionary by adding dictionary entries to the list"))
			self.Bind(wx.EVT_MENU, frame.onVoiceDictionaryCommand, item)
		# Translators: The label for the menu item to open Temporary speech dictionary dialog.
		item = subMenu_speechDicts.Append(wx.ID_ANY,_("&Temporary dictionary..."),_("A dialog where you can set temporary dictionary by adding dictionary entries to the edit box"))
		self.Bind(wx.EVT_MENU, frame.onTemporaryDictionaryCommand, item)
		# Translators: The label for a submenu under NvDA Preferences menu to select speech dictionaries.
		menu_preferences.AppendMenu(wx.ID_ANY,_("Speech &dictionaries"),subMenu_speechDicts)
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open Punctuation/symbol pronunciation dialog.
			item = menu_preferences.Append(wx.ID_ANY, _("&Punctuation/symbol pronunciation..."))
			self.Bind(wx.EVT_MENU, frame.onSpeechSymbolsCommand, item)
			# Translators: The label for the menu item to open the Input Gestures dialog.
			item = menu_preferences.Append(wx.ID_ANY, _("I&nput gestures..."))
			self.Bind(wx.EVT_MENU, frame.onInputGesturesCommand, item)
		# Translators: The label for Preferences submenu in NVDA menu.
		self.menu.AppendMenu(wx.ID_ANY,_("&Preferences"),menu_preferences)

		menu_tools = self.toolsMenu = wx.Menu()
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open NVDA Log Viewer.
			item = menu_tools.Append(wx.ID_ANY, _("View log"))
			self.Bind(wx.EVT_MENU, frame.onViewLogCommand, item)
		# Translators: The label for the menu item to toggle Speech Viewer.
		item=self.menu_tools_toggleSpeechViewer = menu_tools.AppendCheckItem(wx.ID_ANY, _("Speech viewer"))
		self.Bind(wx.EVT_MENU, frame.onToggleSpeechViewerCommand, item)
		if not globalVars.appArgs.secure:
			# Translators: The label for the menu item to open NVDA Python Console.
			item = menu_tools.Append(wx.ID_ANY, _("Python console"))
			self.Bind(wx.EVT_MENU, frame.onPythonConsoleCommand, item)
			# Translators: The label of a menu item to open the Add-ons Manager.
			item = menu_tools.Append(wx.ID_ANY, _("Manage &add-ons"))
			self.Bind(wx.EVT_MENU, frame.onAddonsManagerCommand, item)
		if not globalVars.appArgs.secure and getattr(sys,'frozen',None):
			# Translators: The label for the menu item to create a portable copy of NVDA from an installed or another portable version.
			item = menu_tools.Append(wx.ID_ANY, _("Create Portable copy..."))
			self.Bind(wx.EVT_MENU, frame.onCreatePortableCopyCommand, item)
			if not config.isInstalledCopy():
				# Translators: The label for the menu item to install NVDA on the computer.
				item = menu_tools.Append(wx.ID_ANY, _("&Install NVDA..."))
				self.Bind(wx.EVT_MENU, frame.onInstallCommand, item)
		# Translators: The label for the menu item to reload plugins.
		item = menu_tools.Append(wx.ID_ANY, _("Reload plugins"))
		self.Bind(wx.EVT_MENU, frame.onReloadPluginsCommand, item)
		# Translators: The label for the Tools submenu in NVDA menu.
		self.menu.AppendMenu(wx.ID_ANY, _("Tools"), menu_tools)

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
		item = menu_help.Append(wx.ID_ANY, _("We&lcome dialog"))
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
		self.menu.AppendMenu(wx.ID_ANY,_("&Help"),menu_help)
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
		if not globalVars.appArgs.secure:
			self.menu.AppendSeparator()
			# Translators: The label for the menu item to open donate page.
			item = self.menu.Append(wx.ID_ANY, _("Donate"))
			self.Bind(wx.EVT_MENU, lambda evt: os.startfile(DONATE_URL), item)
		self.menu.AppendSeparator()
		item = self.menu.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		self.Bind(wx.EVT_MENU, frame.onExitCommand, item)

		self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.onActivate)
		self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.onActivate)

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

	WELCOME_MESSAGE = _(
		"Welcome to NVDA!\n"
		"Most commands for controlling NVDA require you to hold down the NVDA key while pressing other keys.\n"
		"By default, the numpad insert and main insert keys may both be used as the NVDA key.\n"
		"You can also configure NVDA to use the CapsLock as the NVDA key.\n"
		"Press NVDA+n at any time to activate the NVDA menu.\n"
		"From this menu, you can configure NVDA, get help and access other NVDA functions.\n"
	)

	def __init__(self, parent):
		# Translators: The title of the Welcome dialog when user starts NVDA for the first time.
		super(WelcomeDialog, self).__init__(parent, wx.ID_ANY, _("Welcome to NVDA"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		welcomeText = wx.StaticText(self, wx.ID_ANY, self.WELCOME_MESSAGE)
		mainSizer.Add(welcomeText,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Options")), wx.VERTICAL)
		self.capsAsNVDAModifierCheckBox = wx.CheckBox(self, wx.ID_ANY, _("Use CapsLock as an NVDA modifier key"))
		self.capsAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"])
		optionsSizer.Add(self.capsAsNVDAModifierCheckBox,flag=wx.TOP|wx.LEFT,border=10)
		# Translators: The label of a check box in the Welcome dialog.
		self.startAfterLogonCheckBox = wx.CheckBox(self, label=_("&Automatically start NVDA after I log on to Windows"))
		self.startAfterLogonCheckBox.Value = config.getStartAfterLogon()
		if globalVars.appArgs.secure or not config.isInstalledCopy():
			self.startAfterLogonCheckBox.Disable()
		optionsSizer.Add(self.startAfterLogonCheckBox,flag=wx.TOP|wx.LEFT,border=10)
		# Translators: This is a label for a checkbox in welcome dialog to show welcome dialog at startup.
		self.showWelcomeDialogAtStartupCheckBox = wx.CheckBox(self, wx.ID_ANY, _("Show this dialog when NVDA starts"))
		self.showWelcomeDialogAtStartupCheckBox.SetValue(config.conf["general"]["showWelcomeDialogAtStartup"])
		optionsSizer.Add(self.showWelcomeDialogAtStartupCheckBox,flag=wx.TOP|wx.LEFT,border=10)
		mainSizer.Add(optionsSizer,flag=wx.LEFT|wx.TOP|wx.RIGHT,border=20)
		mainSizer.Add(self.CreateButtonSizer(wx.OK),flag=wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,border=20)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.capsAsNVDAModifierCheckBox.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"] = self.capsAsNVDAModifierCheckBox.IsChecked()
		if self.startAfterLogonCheckBox.Enabled:
			config.setStartAfterLogon(self.startAfterLogonCheckBox.Value)
		config.conf["general"]["showWelcomeDialogAtStartup"] = self.showWelcomeDialogAtStartupCheckBox.IsChecked()
		try:
			config.conf.save()
		except:
			log.debugWarning("could not save",exc_info=True)
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

		# Translators: The label of the license text which will be shown when NVDA installation program starts.
		sizer = wx.StaticBoxSizer(wx.StaticBox(self, label=_("License Agreement")), wx.VERTICAL)
		ctrl = wx.TextCtrl(self, size=(500, 400), style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
		ctrl.Value = codecs.open(getDocFilePath("copying.txt", False), "r", encoding="UTF-8").read()
		sizer.Add(ctrl)
		# Translators: The label for a checkbox in NvDA installation program to agree to the license agreement.
		ctrl = self.licenseAgreeCheckbox = wx.CheckBox(self, label=_("I &agree"))
		ctrl.Value = False
		sizer.Add(ctrl)
		ctrl.Bind(wx.EVT_CHECKBOX, self.onLicenseAgree)
		mainSizer.Add(sizer)

		sizer = wx.GridSizer(rows=2, cols=2)
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
		mainSizer.Add(sizer)
		for ctrl in self.actionButtons:
			ctrl.Disable()

		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

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
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		if globalVars.appArgs.disableAddons:
			# Translators: A message in the exit Dialog shown when all add-ons are disabled.
			addonsDisabledLabel=wx.StaticText(self,-1,label=_("All add-ons are now disabled. They will be re-enabled on the next restart unless you choose to disable them again."))
			mainSizer.Add(addonsDisabledLabel)

		actionSizer=wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for actions list in the Exit dialog.
		actionsLabel=wx.StaticText(self,-1,label=_("What would you like to &do?"))
		actionSizer.Add(actionsLabel)
		actionsListID=wx.NewId()
		self.actions = [
		# Translators: An option in the combo box to choose exit action.
		_("Exit"),
		# Translators: An option in the combo box to choose exit action.
		_("Restart"),
		# Translators: An option in the combo box to choose exit action.
		_("Restart with add-ons disabled")]
		self.actionsList=wx.Choice(self,actionsListID,choices=self.actions)
		self.actionsList.SetSelection(0)
		actionSizer.Add(self.actionsList)
		mainSizer.Add(actionSizer,border=10,flag=wx.CENTER)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.actionsList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		action=self.actionsList.GetSelection()
		if action == 0:
			wx.GetApp().ExitMainLoop()
		elif action == 1:
			queueHandler.queueFunction(queueHandler.eventQueue,core.restart)
		elif action == 2:
			queueHandler.queueFunction(queueHandler.eventQueue,core.restart,True)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

class ExecAndPump(threading.Thread):
	"""Executes the given function with given args and kwargs in a background thread while blocking and pumping in the current thread."""

	def __init__(self,func,*args,**kwargs):
		self.func=func
		self.args=args
		self.kwargs=kwargs
		super(ExecAndPump,self).__init__()
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
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

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
		if self.IsActive():
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
