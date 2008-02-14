#gui/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 NVDA Contributors <http://www.nvda-project.org/>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import os
import wx
from wx.lib import newevent
import globalVars
import config
import versionInfo
import speech
import queueHandler
import core
from settingsDialogs import *
import userDictHandler

### Constants
appTitle = "NVDA"
quickStartMessage=_("""NVDA - Quick Start document

NVDA (%(description)s)
Version: %(version)s
URL: %(url)s
Please send bugs and suggestions to: %(maintainer)s <%(maintainer_email)s>.

--- Copyright Info ---
%(copyrightInfo)s
----------------------

This is the NVDA interface window. It enables you to control NVDA's settings, and also to exit NVDA altogether.

To bring this window up at any time, press insert+n. To close this window without exiting NVDA, press alt+f4.

To exit NVDA completely, either press insert+q from anywhere, or choose 'exit' from the NVDA menuin this window. NVDA will then bring up a dialog box asking you if you want to exit, and you can either press the OK or Cancel button.

To set the preferences (such as voice settings, key Settings, reading of tooltips etc),
Use the alt key to move to the menu bar and then use the arrow keys to navigate the menus and find the settings you want to change. Pressing enter on many of the menu items will bring up a dialog box in which you can change the individual settings. Most settings will take effect straight away (such as changing the rate or pitch of the voice) so you can easily find what settings most suit you. However, if you cancel out of the dialog box the settings will go back to what they were before you changed them. 

By default settings are not kept for the next time you run NVDA unless you press ctrl+s or choose 'save configuration' from the NVDA menu. You can set NVDA to automatically save the settings on exit by going to 'general settings...' in the Preferences menu and checking the 'Save configuration on exit' checkbox and press ing ok.

Some usefull key commands when using NVDA are:

General key strokes:
control - interupt/pause speech
shift - unpause speech
NVDA+1 - turns keyboard help on and off
NVDA+upArrow - reports the object with focus
NVDA+downArrow - starts sayAll (press control or any other key to stop)
NVDA+tab - report the object currently in focus
NVDA+t speak title
NVDA+f12 - report time and date
NVDA+2 - turn speaking of typed characters on and off
NVDA+3 turn speaking of typed words on and off
NVDA+4 - turn speaking of typed command keys (such as space, arrows, control and shift combinations) on and off
NVDA+pageUp - increase rate of speech
NVDA+pageDown - decrease rate of speech
NVDA+p - turn reading of punctuation on and off
NVDA+s - toggle speech modes (off, talk and beeps)
NVDA+m - turn  reading of objects under the mouse on and off
NVDA+f - report current font (when in a document)

Object navigation:
NVDA+numpadAdd - Where am I
NVDA+numpad5 - current object
shift+NVDA+numpad5 - dimensions and location of current object
NVDA+numpad8 - parent object
NVDA+numpad4 - previous object
NVDA+numpad6 - next object
NVDA+numpad2 - first child object
NVDA+numpadMinus - move to focus object
NVDA+end - move to statusbar
NVDA+numpadDivide - Move mouse to current navigator object
NVDA+numpadMultiply - move to mouse
nvda+numpadEnter - activate current object

Reviewing the current object:
shift+numpad7 - move to top line
numpad7 - previous line
numpad8 - current line
numpad9 - next line
shift+numpad9 - bottom line
numpad4 - previous word
numpad5 - current word
numpad6 - next word
shift+numpad1 - start of line
numpad1 - previous character
numpad2 - current character
numpad3 - next character
shift+numpad3 - end of line
""")%vars(versionInfo)
 
iconPath="%s/images/icon.png"%os.getcwd()

ExternalCommandEvent, evt_externalCommand = newevent.NewCommandEvent()
id_showGuiCommand=wx.NewId()
id_abortCommand=wx.NewId()
evt_externalExecute = wx.NewEventType()

### Globals
mainFrame = None

class ExternalExecuteEvent(wx.PyCommandEvent):
	def __init__(self, func, args, kwargs, callback):
		super(ExternalExecuteEvent, self).__init__(evt_externalExecute, wx.ID_ANY)
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

class MainFrame(wx.Frame):

	def __init__(self):
		style = wx.DEFAULT_FRAME_STYLE ^ wx.MAXIMIZE_BOX ^ wx.MINIMIZE_BOX | wx.FRAME_NO_TASKBAR
		super(MainFrame, self).__init__(None, wx.ID_ANY, appTitle, size=(500,500), style=style)
		self.Bind(evt_externalCommand, self.onAbortCommand, id=id_abortCommand)
		self.Bind(evt_externalCommand, self.onExitCommand, id=wx.ID_EXIT)
		self.Bind(evt_externalCommand, self.onShowGuiCommand, id=id_showGuiCommand)
		wx.EVT_COMMAND(self,wx.ID_ANY,evt_externalExecute,lambda evt: evt.run())
		self.Bind(wx.EVT_CLOSE, self.onHideGuiCommand)
		menuBar=wx.MenuBar()
		self.sysTrayMenu=wx.Menu()
		menu_NVDA = wx.Menu()
		item = menu_NVDA.Append(wx.ID_ANY, _("&Revert to saved configuration\tCtrl+R"),_("Reset all settings to saved state"))
		self.Bind(wx.EVT_MENU, self.onRevertToSavedConfigurationCommand, item)
		item = menu_NVDA.Append(wx.ID_SAVE, _("&Save configuration\tCtrl+S"), _("Write the current configuration to nvda.ini"))
		self.Bind(wx.EVT_MENU, self.onSaveConfigurationCommand, item)
		subMenu_userDicts = wx.Menu()
		item = subMenu_userDicts.Append(wx.ID_ANY,_("&Default dictionary..."),_("dialog where you can set default dictionary by adding dictionary entries to the list"))
		self.Bind(wx.EVT_MENU, self.onDefaultDictionaryCommand, item)
		item = subMenu_userDicts.Append(wx.ID_ANY,_("&Voice dictionary..."),_("dialog where you can set voice-specific dictionary by adding dictionary entries to the list"))
		self.Bind(wx.EVT_MENU, self.onVoiceDictionaryCommand, item)
		item = subMenu_userDicts.Append(wx.ID_ANY,_("&Temporary dictionary..."),_("dialog where you can set temporary dictionary by adding dictionary entries to the edit box"))
		self.Bind(wx.EVT_MENU, self.onTemporaryDictionaryCommand, item)
		menu_NVDA.AppendMenu(wx.ID_ANY,_("User &dictionaries"),subMenu_userDicts)
		menu_NVDA.AppendSeparator()
		item = menu_NVDA.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		self.Bind(wx.EVT_MENU, self.onExitCommand, item)
		menuBar.Append(menu_NVDA,_("&NVDA"))
		self.sysTrayMenu.AppendMenu(wx.ID_ANY,_("&NVDA"),menu_NVDA)
		menu_preferences=wx.Menu()
		item = menu_preferences.Append(wx.ID_ANY,_("&General settings...\tCtrl+Shift+G"),_("General settings"))
		self.Bind(wx.EVT_MENU, self.onGeneralSettingsCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Synthesizer...\tCtrl+Shift+S"),_(" the synthesizer to use"))
		self.Bind(wx.EVT_MENU, self.onSynthesizerCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Voice settings...\tCtrl+Shift+V"),_("Choose the voice, rate, pitch and volume  to use"))
		self.Bind(wx.EVT_MENU, self.onVoiceCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Keyboard Settings...\tCtrl+K"),_("Configure keyboard layout, speaking of typed characters, words or command keys"))
		self.Bind(wx.EVT_MENU, self.onKeyboardSettingsCommand, item)
		item = menu_preferences.Append(wx.ID_ANY, _("&Mouse settings...\tCtrl+M"),_("Change reporting of mouse sape, object under mouse"))
		self.Bind(wx.EVT_MENU, self.onMouseSettingsCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("&Object presentation...\tCtrl+Shift+O"),_("Change reporting of objects")) 
		self.Bind(wx.EVT_MENU, self.onObjectPresentationCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("Virtual &buffers...\tCtrl+Shift+B"),_("Change virtual buffers specific settings")) 
		self.Bind(wx.EVT_MENU, self.onVirtualBuffersCommand, item)
		item = menu_preferences.Append(wx.ID_ANY,_("Document &formatting...\tCtrl+Shift+F"),_("Change Settings of document properties")) 
		self.Bind(wx.EVT_MENU, self.onDocumentFormattingCommand, item)
		menuBar.Append(menu_preferences,_("&Preferences"))
		self.sysTrayMenu.AppendMenu(wx.ID_ANY,_("&Preferences"),menu_preferences)
		menu_help = wx.Menu()
		item = menu_help.Append(wx.ID_ANY, _("NVDA homepage"), _("Opens NVDA homepage in the default browser"))
		self.Bind(wx.EVT_MENU, self.onHomePageCommand, item)
		item = menu_help.Append(wx.ID_ANY, _("NVDA wiki"), _("Opens NVDA wiki in the default browser"))
		self.Bind(wx.EVT_MENU, self.onNvdaWikiCommand, item)
		item = menu_help.Append(wx.ID_ABOUT, _("About..."), _("About NVDA"))
		self.Bind(wx.EVT_MENU, self.onAboutCommand, item)
		menuBar.Append(menu_help,_("&Help"))
		self.sysTrayMenu.AppendMenu(wx.ID_ANY,_("&Help"),menu_help)
		self.SetMenuBar(menuBar)
		sizer=wx.BoxSizer(wx.VERTICAL)
		textCtrl=wx.TextCtrl(self,wx.ID_ANY,size=(500,500),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(textCtrl)
		sizer.Fit(self)
		self.SetSizer(sizer)
		textCtrl.AppendText(quickStartMessage)
		textCtrl.SetSelection(0,0)
		icon=wx.Icon(iconPath,wx.BITMAP_TYPE_PNG)
		self.SetIcon(icon)
		self.sysTrayButton=wx.TaskBarIcon()
		self.sysTrayButton.SetIcon(icon,_("NVDA"))
		self.sysTrayButton.Bind(wx.EVT_TASKBAR_LEFT_DCLICK,self.onShowGuiCommand)
		self.Center()
		self.Show(True)
		if globalVars.appArgs.minimal or config.conf["general"]["hideInterfaceOnStartup"]:
			self.Show(False)

	def onAbortCommand(self,evt):
		self.Destroy()

	def onShowGuiCommand(self,evt):
		self.Center()
		self.Show(True)
		self.Raise()
		#self.sysTrayButton.PopupMenu(self.sysTrayMenu)

	def onHideGuiCommand(self,evt):
		time.sleep(0.01)
		self.Show(False)

	def onRevertToSavedConfigurationCommand(self,evt):
		queueHandler.queueFunction(queueHandler.interactiveQueue,core.resetConfiguration,reportDone=True)

	def onSaveConfigurationCommand(self,evt):
		try:
			config.save()
			queueHandler.queueFunction(queueHandler.interactiveQueue,speech.speakMessage,_("configuration saved"))
		except:
			speech.speakMessage(_("Could not save configuration - probably read only file system"),wait=True)

	def onDefaultDictionaryCommand(self,evt):
		d=DictionaryDialog(self,-1,_("Default dictionary"),userDictHandler.dictionaries["default"])
		d.Show(True)

	def onVoiceDictionaryCommand(self,evt):
		d=DictionaryDialog(self,-1,_("Voice dictionary (%s)")%userDictHandler.dictionaries["voice"].fileName,userDictHandler.dictionaries["voice"])
		d.Show(True)

	def onTemporaryDictionaryCommand(self,evt):
		d=DictionaryDialog(self,-1,_("Temporary dictionary"),userDictHandler.dictionaries["temp"])
		d.Show(True)

	def onExitCommand(self, evt):
		canExit=False
		if config.conf["general"]["askToExit"]:
			wasShown=self.IsShown()
			if not wasShown:
				self.onShowGuiCommand(None)
			self.Raise()
			self.SetFocus()
			d = wx.MessageDialog(self, _("Are you sure you want to quit NVDA?"), _("Exit NVDA"), wx.YES|wx.NO|wx.ICON_WARNING)
			if d.ShowModal() == wx.ID_YES:
				canExit=True
			elif not wasShown:
				self.onHideGuiCommand(None)
		else:
			canExit=True
		if canExit:
			if config.conf["general"]["saveConfigurationOnExit"]:
				try:
					config.save()
				except:
					globalVars.log.warning("Could not save configuration - probably read only file system", exc_info=True)
			self.Destroy()

	def onGeneralSettingsCommand(self,evt):
		d=generalSettingsDialog(self,-1,_("General settings"))
		d.Show(True)

	def onSynthesizerCommand(self,evt):
		d=synthesizerDialog(self,-1,_("Synthesizer"))
		d.Show(True)

	def onVoiceCommand(self,evt):
		d=voiceSettingsDialog(self,-1,_("Voice settings"))
		d.Show(True)

	def onKeyboardSettingsCommand(self,evt):
		d=keyboardSettingsDialog(self,-1,_("Keyboard Settings"))
		d.Show(True)

	def onMouseSettingsCommand(self,evt):
		d=mouseSettingsDialog(self,-1,_("Mouse settings"))
		d.Show(True)

	def onObjectPresentationCommand(self,evt):
		d=objectPresentationDialog(self,-1,_("Object presentation"))
		d.Show(True)

	def onVirtualBuffersCommand(self,evt):
		d=virtualBuffersDialog(self,-1,_("virtual buffers"))
		d.Show(True)

	def onDocumentFormattingCommand(self,evt):
		d=documentFormattingDialog(self,-1,_("Document formatting"))
		d.Show(True)

	def onHomePageCommand(self,evt):
		os.startfile("http://www.nvda-project.org")

	def onNvdaWikiCommand(self,evt):
		os.startfile("http://wiki.nvda-project.org")

	def onAboutCommand(self,evt):
		try:
			aboutInfo="""%s
%s: %s
%s: %s
%s: %s <%s>
%s: %s"""%(versionInfo.longName,_("version"),versionInfo.version,_("url"),versionInfo.url,_("maintainer"),versionInfo.maintainer,versionInfo.maintainer_email,_("copyright"),versionInfo.copyrightInfo)
			d = wx.MessageDialog(self, aboutInfo, _("About NVDA"), wx.OK)
			d.ShowModal()
		except:
			globalVars.log.error("gui.mainFrame.onAbout", exc_info=True)

def initialize(app):
	global mainFrame
	mainFrame = MainFrame()
	app.SetTopWindow(mainFrame)

def showGui():
 	wx.PostEvent(mainFrame, ExternalCommandEvent(id_showGuiCommand))

def quit():
	wx.PostEvent(mainFrame, ExternalCommandEvent(wx.ID_EXIT))

def abort():
	wx.PostEvent(mainFrame, ExternalCommandEvent(id_abortCommand))

def restart():
	globalVars.restart=True
	wx.PostEvent(mainFrame, ExternalCommandEvent(id_abortCommand))

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
