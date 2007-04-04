#gui/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import time
import winsound
import os
import wx
import globalVars
import debug
import config
import versionInfo
import audio
import queueHandler
import pythoncom
import core
from settingsDialogs import *

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

To bring this window up at any time, press insert+n. To close this window with out exiting NVDA, press alt+f4.

To exit NVDA completely, either press insert+q from anywhere, or choose 'exit' from the NVDA menuin this window. NVDA will then bring up a dialog box asking you if you want to exit, and you can either press the yes or no button.

To set the preferences (such as voice settings, key echo, reading of tooltips etc),
Use the alt key to move to the menu bar and then use the arrow keys to navigate the menus and find the settings you want to change. Pressing enter on many of the menu items will bring up a dialog box in which you can change the individual settings. Most settings will take effect straight away (such as changing the rate or pitch of the voice) so you can easily find what settings most suit you. However, if you cancel out of the dialog box the settings will go back to what they were before you changed them. 

By default settings are not kept for the next time you run NVDA unless you press ctrl+s or choose 'save configuration' from the NVDA menu. You can set NVDA to automatically save the settings on exit by going to 'user interface...' in the Preferences menu and checking the 'Save configuration on exit' checkbox and press ing ok.

Some usefull key commands when using NVDA are:

General key strokes:
control - interupt speech
insert+1 - turns keyboard help on and off
insert+upArrow - reports the object with focus
insert+downArrow - starts sayAll (press control or any other key to stop)
insert+t speak title
insert+f12 - report time and date
insert+2 - turn speaking of typed characters on and off
insert+3 turn speaking of typed words on and off
insert+4 - turn speaking of typed command keys (such as space, arrows, control and shift combinations) on and off
insert+pageUp - increase rate of speech
insert+pageDown - decrease rate of speech
insert+p - turn reading of punctuation on and off
insert+s - toggle speech modes (off, talk and beeps)
insert+m - turn  reading of objects under the mouse on and off
insert+f - report current font (when in a document)

Object navigation:
insert+numpadAdd - Where am I
insert+numpad5 - current object
shift+insert+numpad5 - dimensions and location of current object
insert+numpad8 - parent object
insert+numpad4 - previous object
insert+numpad6 - next object
insert+numpad2 - first child object
insert+numpadMinus - move to focus object
 insert+end - move to statusbar
insert+numpadDivide - Move mouse to current navigator object
insert+numpadMultiply - move to mouse
insert+numpadEnter - activate current object

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
evt_externalCommand = wx.NewEventType()
id_onShowGuiCommand=wx.NewId()
id_onAbortCommand=wx.NewId()
evt_externalExecute = wx.NewEventType()

### Globals
mainFrame = None

class ExternalExecuteEvent(wx.PyCommandEvent):
	def __init__(self, func, args, kwargs, callback):
		wx.PyCommandEvent.__init__(self, evt_externalExecute, -1)
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
		style=wx.DEFAULT_FRAME_STYLE
		style-=(style&wx.MAXIMIZE_BOX)
		style-=(style&wx.MINIMIZE_BOX)
		style+=wx.FRAME_NO_TASKBAR
		wx.Frame.__init__(self, None, wx.ID_ANY, appTitle, wx.DefaultPosition,(500,500), style)
		wx.EVT_COMMAND(self,id_onAbortCommand,evt_externalCommand,self.onAbortCommand)
		wx.EVT_COMMAND(self,wx.ID_EXIT,evt_externalCommand,self.onExitCommand)
		wx.EVT_COMMAND(self,id_onShowGuiCommand,evt_externalCommand,self.onShowGuiCommand)
		wx.EVT_COMMAND(self,-1,evt_externalExecute,lambda evt: evt.run())
		wx.EVT_CLOSE(self,self.onHideGuiCommand)
		menuBar=wx.MenuBar()
		self.sysTrayMenu=wx.Menu()
		menu_NVDA = wx.Menu()
		id_onRevertToSavedConfigurationCommand=wx.NewId()
		menu_NVDA.Append(id_onRevertToSavedConfigurationCommand,_("&Revert to saved configuration\tctrl+r"),_("Reset all setting back to nvda.ini"))
		wx.EVT_MENU(self,id_onRevertToSavedConfigurationCommand,self.onRevertToSavedConfigurationCommand)
		menu_NVDA.Append(wx.ID_SAVE, _("&Save configuration\tctrl+s"), _("Write the current configuration to nvda.ini"))
		wx.EVT_MENU(self, wx.ID_SAVE, self.onSaveConfigurationCommand)
		menu_NVDA.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		wx.EVT_MENU(self, wx.ID_EXIT, self.onExitCommand)
		menuBar.Append(menu_NVDA,_("&NVDA"))
		self.sysTrayMenu.AppendMenu(-1,_("&NVDA"),menu_NVDA)
		menu_preferences=wx.Menu()
		id_interfaceSettingsCommand=wx.NewId()
		menu_preferences.Append(id_interfaceSettingsCommand,_("&User interface...\tctrl+shift+u"),_("Change user interface settings"))
		wx.EVT_MENU(self,id_interfaceSettingsCommand,self.onInterfaceSettingsCommand)
		id_SynthesizerCommand=wx.NewId()
		menu_preferences.Append(id_SynthesizerCommand,_("&Synthesizer...\tctrl+shift+s"),_(" the synthesizer to use"))
		wx.EVT_MENU(self,id_SynthesizerCommand,self.onSynthesizerCommand)
		id_VoiceCommand=wx.NewId()
		menu_preferences.Append(id_VoiceCommand,_("Voice settings...\tctrl+shift+v"),_("Choose the voice, rate, pitch and volume  to use"))
		wx.EVT_MENU(self,id_VoiceCommand,self.onVoiceCommand)
		id_onKeyboardEchoCommand=wx.NewId()
		menu_preferences.Append(id_onKeyboardEchoCommand,_("&Keyboard echo...\tctrl+e"),_("Configure speaking of typed characters, words or command keys"))
		wx.EVT_MENU(self,id_onKeyboardEchoCommand,self.onKeyboardEchoCommand)
		id_mouseSettingsCommand=wx.NewId()
		menu_preferences.Append(id_mouseSettingsCommand,_("&Mouse settings...\tctrl+m"),_("Change reporting of mouse sape, object under mouse"))
		wx.EVT_MENU(self,id_mouseSettingsCommand,self.onMouseSettingsCommand)
		id_objectPresentationCommand=wx.NewId()
		menu_preferences.Append(id_objectPresentationCommand,_("&Object presentation...\tctrl+shift+o"),_("Change reporting of objects")) 
		wx.EVT_MENU(self,id_objectPresentationCommand,self.onObjectPresentationCommand)
		id_virtualBuffersCommand=wx.NewId()
		menu_preferences.Append(id_virtualBuffersCommand,_("Virtual &buffers...\tctrl+shift+b"),_("Change virtual buffers specific settings")) 
		wx.EVT_MENU(self,id_virtualBuffersCommand,self.onVirtualBuffersCommand)
		id_documentFormattingCommand=wx.NewId()
		menu_preferences.Append(id_documentFormattingCommand,_("Document &formatting...\tctrl+shift+f"),_("Change echo of document properties")) 
		wx.EVT_MENU(self,id_documentFormattingCommand,self.onDocumentFormattingCommand)
		menuBar.Append(menu_preferences,_("&Preferences"))
		self.sysTrayMenu.AppendMenu(-1,_("&Preferences"),menu_preferences)
		menu_help = wx.Menu()
		menu_help.Append(wx.ID_ABOUT, _("About..."), _("About NVDA"))
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		menuBar.Append(menu_help,_("&Help"))
		self.sysTrayMenu.AppendMenu(-1,_("&Help"),menu_help)
		self.SetMenuBar(menuBar)
		sizer=wx.BoxSizer(wx.VERTICAL)
		textCtrl=wx.TextCtrl(self,-1,size=(500,500),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
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
		core.applyConfiguration(reportDone=True)

	def onSaveConfigurationCommand(self,evt):
		try:
			config.save()
			audio.speakMessage(_("configuration saved"))
		except:
			audio.speakMessage(_("Could not save configuration - probably read only file system"),wait=True)

	def onExitCommand(self, evt):
		wasShown=self.IsShown()
		if not wasShown:
			self.onShowGuiCommand(None)
		self.Raise()
		self.SetFocus()
		d = wx.MessageDialog(self, _("Press OK to quit NVDA"), _("Exit NVDA"), wx.OK|wx.CANCEL|wx.ICON_WARNING)
		if d.ShowModal() == wx.ID_OK:
			if config.conf["general"]["saveConfigurationOnExit"]:
				config.save()
			self.Destroy()
		elif not wasShown:
			self.onHideGuiCommand(None)

	def onInterfaceSettingsCommand(self,evt):
		d=interfaceSettingsDialog(self,-1,_("User interface settings"))
		d.Show(True)

	def onSynthesizerCommand(self,evt):
		d=synthesizerDialog(self,-1,_("Synthesizer"))
		d.Show(True)

	def onVoiceCommand(self,evt):
		d=voiceSettingsDialog(self,-1,_("Voice settings"))
		d.Show(True)

	def onKeyboardEchoCommand(self,evt):
		d=keyboardEchoDialog(self,-1,_("Keyboard echo settings"))
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
			debug.writeException("gui.mainFrame.onAbout")

def initialize(app):
	global mainFrame
	mainFrame = MainFrame()
	app.SetTopWindow(mainFrame)

def showGui():
 	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, id_onShowGuiCommand))

def quit():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, wx.ID_EXIT))

def abort():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, id_onAbortCommand))

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
	mainFrame.GetEventHandler().AddPendingEvent(ExternalExecuteEvent(func, args, kwargs, callback))
