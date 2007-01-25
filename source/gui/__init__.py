import time
import winsound
import threading
import wx
import globalVars
import debug
import synthDriverHandler
import config
import versionInfo
import audio
import core
from settingsDialogs import *

### Constants
appTitle = _("NVDA Interface")
quickStartMessage=_("""NVDA Quick-Start

This is the NVDA interface window. It enables you to control NVDA's settings, and also to exit NVDA altogether.

To bring this window up at any time, press insert+n. To close this window with out exiting NVDA, press alt+f4 when on this window.

To exit NVDA completely, either press insert+q from anywhere, or choose 'exit' from the NVDA menu in this window. NVDA will then bring up a dialog box asking you if you want to exit, and you can either press the yes or no button.

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
""")
 
#iconPath="images\\NVDAIcon.bmp"
evt_externalCommand = wx.NewEventType()
id_onShowGuiCommand=wx.NewId()
id_onAbortCommand=wx.NewId()

### Globals
guiThread = None
mainFrame = None

class MainFrame(wx.Frame):

	def __init__(self):
		style=wx.DEFAULT_FRAME_STYLE
		style-=(style&wx.MAXIMIZE_BOX)
		style-=(style&wx.MINIMIZE_BOX)
		wx.Frame.__init__(self, None, wx.ID_ANY, appTitle, wx.DefaultPosition,(300,300), style)
		wx.EVT_COMMAND(self,id_onAbortCommand,evt_externalCommand,self.onAbortCommand)
		wx.EVT_COMMAND(self,wx.ID_EXIT,evt_externalCommand,self.onExitCommand)
		wx.EVT_COMMAND(self,id_onShowGuiCommand,evt_externalCommand,self.onShowGuiCommand)
		wx.EVT_CLOSE(self,self.onHideGuiCommand)
		menuBar=wx.MenuBar()
		menu_NVDA = wx.Menu()
		id_onRevertToSavedConfigurationCommand=wx.NewId()
		menu_NVDA.Append(id_onRevertToSavedConfigurationCommand,_("&Revert to saved configuration\tctrl+r"),_("Reset all setting back to nvda.ini"))
		wx.EVT_MENU(self,id_onRevertToSavedConfigurationCommand,self.onRevertToSavedConfigurationCommand)
		menu_NVDA.Append(wx.ID_SAVE, _("&Save configuration\tctrl+s"), _("Write the current configuration to nvda.ini"))
		wx.EVT_MENU(self, wx.ID_SAVE, self.onSaveConfigurationCommand)
		menu_NVDA.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		wx.EVT_MENU(self, wx.ID_EXIT, self.onExitCommand)
		menuBar.Append(menu_NVDA,_("&NVDA"))
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
		menuBar.Append(menu_preferences,_("&Preferences"))
		menu_help = wx.Menu()
		menu_help.Append(wx.ID_ABOUT, _("About..."), _("About NVDA"))
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		menuBar.Append(menu_help,_("&Help"))
		self.SetMenuBar(menuBar)
		sizer=wx.BoxSizer(wx.VERTICAL)
		textCtrl=wx.TextCtrl(self,-1,size=(300,300),style=wx.TE_RICH2|wx.TE_READONLY|wx.TE_MULTILINE)
		sizer.Add(textCtrl)
		sizer.Fit(self)
		self.SetSizer(sizer)
		textCtrl.AppendText(quickStartMessage)
		textCtrl.SetSelection(0,0)
		#icon=wx.Icon(iconPath,wx.BITMAP_TYPE_BMP)
		#self.SetIcon(icon)
		self.Center()
		self.Show(True)
		if config.conf["general"]["hideInterfaceOnStartup"]:
			self.Show(False)

	def onAbortCommand(self,evt):
		globalVars.stayAlive=False
		self.Destroy()

	def onShowGuiCommand(self,evt):
		self.Center()
		self.Show(True)
		self.Raise()

	def onHideGuiCommand(self,evt):
		time.sleep(0.01)
		self.Show(False)

	def onRevertToSavedConfigurationCommand(self,evt):
		core.executeFunction(core.EXEC_CONFIG,core.applyConfiguration,reportDone=True)

	def onSaveConfigurationCommand(self,evt):
		config.save()
		core.executeFunction(core.EXEC_SPEECH,audio.speakMessage,_("configuration saved"))

	def onExitCommand(self, evt):
		wasShown=self.IsShown()
		if not wasShown:
			self.onShowGuiCommand(None)
		#winsound.PlaySound("SystemExclamation",winsound.SND_ALIAS|winsound.SND_ASYNC)
		self.Raise()
		self.SetFocus()
		d = wx.MessageDialog(self, _("Do you really want to exit NVDA?"), _("Exit NVDA"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			if config.conf["general"]["saveConfigurationOnExit"]:
				config.save()
			globalVars.stayAlive=False
			self.Destroy()
		elif not wasShown:
			self.onHideGuiCommand(None)

	def onInterfaceSettingsCommand(self,evt):
		oldHide=config.conf["general"]["hideInterfaceOnStartup"]
		d=interfaceSettingsDialog(self,-1,_("User interface settings"))
		if d.ShowModal()!=wx.ID_OK:
			config.conf["general"]["hideInterfaceOnStartup"]=oldHide


	def onSynthesizerCommand(self,evt):
		synthList=synthDriverHandler.getDriverList()
		choices=[]
		for item in synthList:
			choices.append("%s: %s"%(item,synthDriverHandler.getDriverDescription(item)))
		d=wx.SingleChoiceDialog(self,_("Choose the synthesizer to use"),_("Synthesizer"),choices)
		debug.writeMessage("onSynthesizerCommand: current: %s, list: %s"%(synthDriverHandler.driverName,choices))
		d.SetSelection(synthList.index(synthDriverHandler.driverName))
		if d.ShowModal()==wx.ID_OK:
			core.executeFunction(core.EXEC_CONFIG,synthDriverHandler.setDriver,synthList[d.GetSelection()])

	def onVoiceCommand(self,evt):
		oldVoice=synthDriverHandler.getVoice()
		oldRate=synthDriverHandler.getRate()
		oldPitch=synthDriverHandler.getPitch()
		oldVolume=synthDriverHandler.getVolume()
		oldPunctuation=config.conf["speech"]["speakPunctuation"]
		oldCaps=config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]
		d=voiceSettingsDialog(self,-1,"Voice settings")
		if d.ShowModal()!=wx.ID_OK:
			synthDriverHandler.setVoice(oldVoice)
			synthDriverHandler.setRate(oldRate)
			synthDriverHandler.setPitch(oldPitch)
			synthDriverHandler.setVolume(oldVolume)
			config.conf["speech"]["speakPunctuation"]=oldPunctuation
			config.conf["speech"][synthDriverHandler.driverName]["sayCapForCapitals"]=oldCaps

	def onKeyboardEchoCommand(self,evt):
		oldChars=config.conf["keyboard"]["speakTypedCharacters"]
		oldWords=config.conf["keyboard"]["speakTypedWords"]
		oldCommandKeys=config.conf["keyboard"]["speakCommandKeys"]
		d=keyboardEchoDialog(self,-1,_("Keyboard echo settings"))
		if d.ShowModal()!=wx.ID_OK:
			config.conf["keyboard"]["speakTypedCharacters"]=oldChars
			config.conf["keyboard"]["speakTypedWords"]=oldWords
			config.conf["keyboard"]["speakCommandKeys"]=oldCommandKeys

	def onMouseSettingsCommand(self,evt):
		oldShape=config.conf["mouse"]["reportMouseShapeChanges"]
		oldObject=config.conf["mouse"]["reportObjectUnderMouse"]
		d=mouseSettingsDialog(self,-1,_("Mouse settings"))
		if d.ShowModal()!=wx.ID_OK:
			config.conf["mouse"]["reportMouseShapeChanges"]=oldShape
			config.conf["mouse"]["reportObjectUnderMouse"]=oldObject

	def onObjectPresentationCommand(self,evt):
		oldTooltip=config.conf["presentation"]["reportTooltips"]
		oldBalloon=config.conf["presentation"]["reportHelpBalloons"]
		oldShortcut=config.conf["presentation"]["reportKeyboardShortcuts"]
		oldGroup=config.conf["presentation"]["reportObjectGroupNames"]
		oldStateFirst=config.conf["presentation"]["sayStateFirst"]
		oldProgressBeep=config.conf["presentation"]["beepOnProgressBarUpdates"]
		d=objectPresentationDialog(self,-1,_("Object presentation"))
		if d.ShowModal()!=wx.ID_OK:
			config.conf["presentation"]["reportTooltips"]=oldTooltip
			config.conf["presentation"]["reportHelpBalloons"]=oldBalloon
			config.conf["presentation"]["reportKeyboardShortcuts"]=oldShortcut
			config.conf["presentation"]["reportObjectGroupNames"]=oldGroup
			config.conf["presentation"]["sayStateFirst"]=oldStateFirst
			config.conf["presentation"]["beepOnProgressBarUpdates"]=oldProgressBeep

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

def guiMainLoop():
	global mainFrame
	try:
		app = wx.PySimpleApp()
		mainFrame = MainFrame()
		app.SetTopWindow(mainFrame)
		app.MainLoop()
	except:
		debug.writeException("guiMainLoop")
		globalVars.stayAlive=False

def initialize():
	global guiThread
	guiThread = threading.Thread(target = guiMainLoop)
	guiThread.start()

def showGui():
 	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, id_onShowGuiCommand))

def quit():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, wx.ID_EXIT))

def abort():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, id_onAbortCommand))
