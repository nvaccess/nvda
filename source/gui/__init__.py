#gui/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import os
import sys
import wx
from wx.lib import newevent
import globalVars
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
import winUser
import api

### Constants
appTitle = "NVDA"
NVDA_PATH = os.getcwdu()
ICON_PATH=os.path.join(NVDA_PATH, "images", "nvda.ico")

ExternalCommandEvent, evt_externalCommand = newevent.NewCommandEvent()
id_showGuiCommand=wx.NewId()
evtid_externalExecute = wx.NewEventType()
evt_externalExecute = wx.PyEventBinder(evtid_externalExecute, 1)

### Globals
mainFrame = None
isExitDialog=False
#: A list of top level windows excluding L{mainFrame} which are currently instantiated and which should be destroyed on exit.

class ExternalExecuteEvent(wx.PyCommandEvent):
	def __init__(self, func, args, kwargs, callback):
		super(ExternalExecuteEvent, self).__init__(evtid_externalExecute, wx.ID_ANY)
		self._func = func
		self._args = args
		self._kwargs = kwargs
		self._callback = callback

	def run(self):
		ret = self._func(*self._args, **self._kwargs)
		if self._callback:
			queueHandler.registerGeneratorObject(self._callback_gen(ret))

	def _callback_gen(self, ret):
		for n in xrange(20):
			yield None
		self._callback(ret)

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
		super(MainFrame, self).__init__(None, wx.ID_ANY, appTitle, size=(1,1), style=style)
		self.Bind(wx.EVT_CLOSE, self.onExitCommand)
		self.Bind(evt_externalCommand, self.onExitCommand, id=wx.ID_EXIT)
		self.Bind(evt_externalCommand, self.onShowGuiCommand, id=id_showGuiCommand)
		self.Bind(evt_externalExecute,lambda evt: evt.run())
		self.sysTrayIcon = SysTrayIcon(self)
		# This makes Windows return to the previous foreground window and also seems to allow NVDA to be brought to the foreground.
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
		if winUser.getWindowThreadProcessID(winUser.getForegroundWindow())[0] != os.getpid():
			# This process is not the foreground process, so bring it to the foreground.
			self.Raise()

	def postPopup(self):
		"""Clean up after a popup dialog or menu.
		This should be called after a dialog or menu was popped up for the user.
		"""
		if not winUser.isWindowVisible(winUser.getForegroundWindow()):
			# The current foreground window is invisible, so we want to return to the previous foreground window.
			# Showing and hiding our main window seems to achieve this.
			self.Show()
			self.Hide()

	def onShowGuiCommand(self,evt):
		# The menu pops up at the location of the mouse, which means it pops up at an unpredictable location.
		# Therefore, move the mouse to the centre of the screen so that the menu will always pop up there.
		left, top, width, height = api.getDesktopObject().location
		x = width / 2
		y = height / 2
		winUser.setCursorPos(x, y)
		self.sysTrayIcon.onActivate(None)

	def onRevertToSavedConfigurationCommand(self,evt):
		queueHandler.queueFunction(queueHandler.eventQueue,core.resetConfiguration)
		queueHandler.queueFunction(queueHandler.eventQueue,ui.message,_("configuration applied"))

	def onSaveConfigurationCommand(self,evt):
		try:
			config.save()
			queueHandler.queueFunction(queueHandler.eventQueue,ui.message,_("configuration saved"))
		except:
			self.prePopup()
			wx.MessageDialog(self,_("Could not save configuration - probably read only file system"),_("Error"),style=wx.OK | wx.ICON_ERROR).ShowModal()
			self.postPopup()

	def _popupSettingsDialog(self, dialog, *args, **kwargs):
		self.prePopup()
		dialog(self, *args, **kwargs).Show()
		self.postPopup()

	def onDefaultDictionaryCommand(self,evt):
		self._popupSettingsDialog(DictionaryDialog,_("Default dictionary"),speechDictHandler.dictionaries["default"])

	def onVoiceDictionaryCommand(self,evt):
		self._popupSettingsDialog(DictionaryDialog,_("Voice dictionary (%s)")%speechDictHandler.dictionaries["voice"].fileName,speechDictHandler.dictionaries["voice"])

	def onTemporaryDictionaryCommand(self,evt):
		self._popupSettingsDialog(DictionaryDialog,_("Temporary dictionary"),speechDictHandler.dictionaries["temp"])

	def onExitCommand(self, evt):
		global isExitDialog
		canExit=False
		if config.conf["general"]["askToExit"]:
			self.prePopup()
			isExitDialog=True
			d = wx.MessageDialog(self, _("Are you sure you want to quit NVDA?"), _("Exit NVDA"), wx.YES|wx.NO|wx.ICON_WARNING)
			if d.ShowModal() == wx.ID_YES:
				canExit=True
			isExitDialog=False
			self.postPopup()
		else:
			canExit=True
		if canExit:
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

	def onObjectPresentationCommand(self,evt):
		self._popupSettingsDialog(ObjectPresentationDialog)

	def onVirtualBuffersCommand(self,evt):
		self._popupSettingsDialog(VirtualBuffersDialog)

	def onDocumentFormattingCommand(self,evt):
		self._popupSettingsDialog(DocumentFormattingDialog)

	def onAboutCommand(self,evt):
		try:
			aboutInfo="""%s
%s: %s
%s: %s
%s: %s"""%(versionInfo.longName,_("version"),versionInfo.version,_("url"),versionInfo.url,_("copyright"),versionInfo.copyrightInfo)
			self.prePopup()
			d = wx.MessageDialog(self, aboutInfo, _("About NVDA"), wx.OK)
			d.ShowModal()
			self.postPopup()
		except:
			log.error("gui.mainFrame.onAbout", exc_info=True)

	def onViewLogCommand(self, evt):
		logViewer.activate()

	def onPythonConsoleCommand(self, evt):
		import pythonConsole
		if not pythonConsole.consoleUI:
			pythonConsole.initialize()
		pythonConsole.activate()

class SysTrayIcon(wx.TaskBarIcon):

	def __init__(self, frame):
		super(SysTrayIcon, self).__init__()
		icon=wx.Icon(ICON_PATH,wx.BITMAP_TYPE_ICO)
		self.SetIcon(icon, appTitle)

		self.menu=wx.Menu()
		menu_preferences=wx.Menu()
		item = menu_preferences.Append(wx.ID_ANY,_("&General settings..."),_("General settings"))
		self.Bind(wx.EVT_MENU, frame.onGeneralSettingsCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Synthesizer..."),_(" the synthesizer to use"))
		self.Bind(wx.EVT_MENU, frame.onSynthesizerCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Voice settings..."),_("Choose the voice, rate, pitch and volume  to use"))
		self.Bind(wx.EVT_MENU, frame.onVoiceCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("B&raille settings..."))
		self.Bind(wx.EVT_MENU, frame.onBrailleCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Keyboard Settings..."),_("Configure keyboard layout, speaking of typed characters, words or command keys"))
		self.Bind(wx.EVT_MENU, frame.onKeyboardSettingsCommand, item)
		item = menu_preferences.Append(wx.ID_ANY, _("&Mouse settings..."),_("Change reporting of mouse shape and object under mouse"))
		self.Bind(wx.EVT_MENU, frame.onMouseSettingsCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Object presentation..."),_("Change reporting of objects")) 
		self.Bind(wx.EVT_MENU, frame.onObjectPresentationCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("Virtual &buffers..."),_("Change virtual buffers specific settings")) 
		self.Bind(wx.EVT_MENU, frame.onVirtualBuffersCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("Document &formatting..."),_("Change Settings of document properties")) 
		self.Bind(wx.EVT_MENU, frame.onDocumentFormattingCommand, item)
		subMenu_speechDicts = wx.Menu()
		item = subMenu_speechDicts.Append(wx.ID_ANY,_("&Default dictionary..."),_("dialog where you can set default dictionary by adding dictionary entries to the list"))
		self.Bind(wx.EVT_MENU, frame.onDefaultDictionaryCommand, item)
		item = subMenu_speechDicts.Append(wx.ID_ANY,_("&Voice dictionary..."),_("dialog where you can set voice-specific dictionary by adding dictionary entries to the list"))
		self.Bind(wx.EVT_MENU, frame.onVoiceDictionaryCommand, item)
		item = subMenu_speechDicts.Append(wx.ID_ANY,_("&Temporary dictionary..."),_("dialog where you can set temporary dictionary by adding dictionary entries to the edit box"))
		self.Bind(wx.EVT_MENU, frame.onTemporaryDictionaryCommand, item)
		menu_preferences.AppendMenu(wx.ID_ANY,_("Speech &dictionaries"),subMenu_speechDicts)
		self.menu.AppendMenu(wx.ID_ANY,_("&Preferences"),menu_preferences)

		menu_tools = wx.Menu()
		item = menu_tools.Append(wx.ID_ANY, _("View log"))
		self.Bind(wx.EVT_MENU, frame.onViewLogCommand, item)
		item = menu_tools.Append(wx.ID_ANY, _("Python console"))
		self.Bind(wx.EVT_MENU, frame.onPythonConsoleCommand, item)
		self.menu.AppendMenu(wx.ID_ANY, _("Tools"), menu_tools)

		menu_help = wx.Menu()
		item = menu_help.Append(wx.ID_ANY, _("User guide"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("user guide.html")), item)
		item = menu_help.Append(wx.ID_ANY, _("Key Command Quick Reference"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("key commands.txt")), item)
		item = menu_help.Append(wx.ID_ANY, _("What's &new"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("whats new.txt")), item)
		item = menu_help.Append(wx.ID_ANY, _("Web site"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile("http://www.nvda-project.org/"), item)
		item = menu_help.Append(wx.ID_ANY, _("Readme"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("readme.txt")), item)
		item = menu_help.Append(wx.ID_ANY, _("License"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("copying.txt", False)), item)
		item = menu_help.Append(wx.ID_ANY, _("Contributors"))
		self.Bind(wx.EVT_MENU, lambda evt: os.startfile(getDocFilePath("contributors.txt", False)), item)
		item = menu_help.Append(wx.ID_ANY, _("We&lcome dialog"))
		self.Bind(wx.EVT_MENU, lambda evt: WelcomeDialog.run(), item)
		menu_help.AppendSeparator()
		item = menu_help.Append(wx.ID_ABOUT, _("About..."), _("About NVDA"))
		self.Bind(wx.EVT_MENU, frame.onAboutCommand, item)
		self.menu.AppendMenu(wx.ID_ANY,_("&Help"),menu_help)
		self.menu.AppendSeparator()
		item = self.menu.Append(wx.ID_ANY, _("&Revert to saved configuration"),_("Reset all settings to saved state"))
		self.Bind(wx.EVT_MENU, frame.onRevertToSavedConfigurationCommand, item)
		item = self.menu.Append(wx.ID_SAVE, _("&Save configuration"), _("Write the current configuration to nvda.ini"))
		self.Bind(wx.EVT_MENU, frame.onSaveConfigurationCommand, item)
		self.menu.AppendSeparator()
		item = self.menu.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		self.Bind(wx.EVT_MENU, frame.onExitCommand, item)

		self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.onActivate)

	def Destroy(self):
		self.menu.Destroy()
		super(SysTrayIcon, self).Destroy()

	def onActivate(self, evt):
		mainFrame.prePopup()
		self.PopupMenu(self.menu)
		mainFrame.postPopup()

def initialize():
	global mainFrame
	mainFrame = MainFrame()
	wx.GetApp().SetTopWindow(mainFrame)

def terminate():
	global mainFrame
	mainFrame.Destroy()

def showGui():
 	wx.PostEvent(mainFrame, ExternalCommandEvent(id_showGuiCommand))

def quit():
	global isExitDialog
	if not isExitDialog:
		wx.PostEvent(mainFrame, ExternalCommandEvent(wx.ID_EXIT))

def execute(func, callback=None, *args, **kwargs):
	"""Execute a function in the GUI thread.
	This should be used when scripts need to interact with the user via the GUI.
	For example, a frame or dialog can be created and this function can then be used to execute its Show method.
	@param func: The function to execute.
	@type func: callable
	@param callback: A function to call in the main thread when C{func} returns. The function will be passed the return value as its only argument.
	@type callback: callable
	@param args: Arguments for the function.
	@param kwargs: Keyword arguments for the function.
"""
	wx.PostEvent(mainFrame, ExternalExecuteEvent(func, args, kwargs, callback))

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
		super(WelcomeDialog, self).__init__(parent, wx.ID_ANY, _("Welcome to NVDA"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		welcomeText = wx.StaticText(self, wx.ID_ANY, self.WELCOME_MESSAGE)
		mainSizer.Add(welcomeText,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		optionsSizer = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, _("Options")), wx.HORIZONTAL)
		self.capsAsNVDAModifierCheckBox = wx.CheckBox(self, wx.ID_ANY, _("Use CapsLock as an NVDA modifier key"))
		self.capsAsNVDAModifierCheckBox.SetValue(config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"])
		optionsSizer.Add(self.capsAsNVDAModifierCheckBox,flag=wx.TOP|wx.RIGHT,border=10)
		self.showWelcomeDialogAtStartupCheckBox = wx.CheckBox(self, wx.ID_ANY, _("Show this dialog when NVDA starts"))
		self.showWelcomeDialogAtStartupCheckBox.SetValue(config.conf["general"]["showWelcomeDialogAtStartup"])
		optionsSizer.Add(self.showWelcomeDialogAtStartupCheckBox,flag=wx.TOP|wx.LEFT,border=10)
		mainSizer.Add(optionsSizer,flag=wx.LEFT|wx.TOP|wx.RIGHT,border=20)
		mainSizer.Add(self.CreateButtonSizer(wx.OK),flag=wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,border=20)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)

		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		self.capsAsNVDAModifierCheckBox.SetFocus()

	def onOk(self, evt):
		config.conf["keyboard"]["useCapsLockAsNVDAModifierKey"] = self.capsAsNVDAModifierCheckBox.IsChecked()
		config.conf["general"]["showWelcomeDialogAtStartup"] = self.showWelcomeDialogAtStartupCheckBox.IsChecked()
		try:
			config.save()
		except:
			pass
		self.Destroy()

	@classmethod
	def run(cls):
		"""Prepare and display an instance of this dialog.
		This does not require the dialog to be instantiated.
		"""
		mainFrame.prePopup()
		cls(mainFrame).ShowModal()
		mainFrame.postPopup()

class ConfigFileErrorDialog(wx.Dialog):
	"""A configuration file error dialog.
	This dialog tells the user that their configuration file is broken.
	"""

	MESSAGE=_("""Your configuration file contains errors. 
Press 'Ok' to fix these errors, or press 'Cancel' if you wish to manually edit your config file at a later stage to make corrections. More details about the errors can be found in the log file.
""")

	def __init__(self, parent):
		super(ConfigFileErrorDialog, self).__init__(parent, wx.ID_ANY, _("Configuration File Error"))
		mainSizer=wx.BoxSizer(wx.VERTICAL)
		messageText = wx.StaticText(self, wx.ID_ANY, self.MESSAGE)
		mainSizer.Add(messageText,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		mainSizer.Add(self.CreateButtonSizer(wx.OK|wx.CANCEL),flag=wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,border=20)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

	def onOk(self, evt):
		globalVars.configFileError=None
		config.save()
		self.Destroy()

	@classmethod
	def run(cls):
		"""Prepare and display an instance of this dialog.
		This does not require the dialog to be instantiated.
		"""
		mainFrame.prePopup()
		cls(mainFrame).ShowModal()
		mainFrame.postPopup()
