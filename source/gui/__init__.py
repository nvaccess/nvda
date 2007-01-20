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
		#icon=wx.Icon(iconPath,wx.BITMAP_TYPE_BMP)
		#self.SetIcon(icon)
		self.Show(True)
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
		winsound.PlaySound("SystemExclamation",winsound.SND_ALIAS|winsound.SND_ASYNC)
		self.Raise()
		self.SetFocus()
		d = wx.MessageDialog(self, _("Do you really want to exit NVDA?"), _("Exit NVDA"), wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive=False
			self.Destroy()
		elif not wasShown:
			self.onHideGuiCommand(None)

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
