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

### Constants
appTitle = _("NVDA Interface")
#iconPath="images\\NVDAIcon.bmp"
evt_externalCommand = wx.NewEventType()

### Globals
guiThread = None
mainFrame = None

class MainFrame(wx.Frame):

	def __init__(self):
		style=wx.DEFAULT_FRAME_STYLE
		style-=(style&wx.MAXIMIZE_BOX)
		style-=(style&wx.MINIMIZE_BOX)
		wx.Frame.__init__(self, None, wx.ID_ANY, appTitle, wx.DefaultPosition,(300,300), style)
		self.id_onAbortCommand=wx.NewId()
		wx.EVT_COMMAND(self,self.id_onAbortCommand,evt_externalCommand,self.onAbortCommand)
		wx.EVT_COMMAND(self,wx.ID_EXIT,evt_externalCommand,self.onExitCommand)
		self.id_onShowGuiCommand=wx.NewId()
		wx.EVT_COMMAND(self,self.id_onShowGuiCommand,evt_externalCommand,self.onShowGuiCommand)
		wx.EVT_CLOSE(self,self.onHideGuiCommand)
		self.menuBar=wx.MenuBar()
		self.menu_NVDA = wx.Menu()
		self.id_onRevertToSavedConfigurationCommand=wx.NewId()
		self.menu_NVDA.Append(self.id_onRevertToSavedConfigurationCommand,_("&Revert to saved configuration"),_("Reset all setting back to nvda.ini"))
		wx.EVT_MENU(self,self.id_onRevertToSavedConfigurationCommand,self.onRevertToSavedConfigurationCommand)
		self.id_onSaveConfigurationCommand=wx.NewId()
		self.menu_NVDA.Append(self.id_onSaveConfigurationCommand, _("&Save configuration")+"\tctrl+s", _("Write the current configuration to nvda.ini"))
		wx.EVT_MENU(self, self.id_onSaveConfigurationCommand, self.onSaveConfigurationCommand)
		self.menu_NVDA.Append(wx.ID_EXIT, _("E&xit"),_("Exit NVDA"))
		wx.EVT_MENU(self, wx.ID_EXIT, self.onExitCommand)
		self.menuBar.Append(self.menu_NVDA,_("&NVDA"))
		self.menu_preferences=wx.Menu()
		self.id_chooseSynthesizerCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseSynthesizerCommand,_("&Synthesizer")+"...\tctrl+shift+s",_("Choose the synthesizer to use"))
		wx.EVT_MENU(self,self.id_chooseSynthesizerCommand,self.onSynthesizerCommand)
		self.id_chooseVoiceCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseVoiceCommand,_("Voice")+"...\tctrl+shift+v",_("Choose the voice to use"))
		wx.EVT_MENU(self,self.id_chooseVoiceCommand,self.onVoiceCommand)
		self.menuBar.Append(self.menu_preferences,_("&Preferences"))
		self.menu_help = wx.Menu()
		self.menu_help.Append(wx.ID_ABOUT, _("About")+"...", _("About NVDA"))
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		self.menuBar.Append(self.menu_help,_("&Help"))
		self.SetMenuBar(self.menuBar)
		#self.icon=wx.Icon(iconPath,wx.BITMAP_TYPE_BMP)
		#self.SetIcon(self.icon)
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
		d=wx.SingleChoiceDialog(self,_("Choose the voice to use"),_("Voice"),synthDriverHandler.getVoiceNames())
		d.SetSelection(config.conf["speech"][synthDriverHandler.driverName]["voice"]-1)
		if d.ShowModal()==wx.ID_OK:
			core.executeFunction(core.EXEC_CONFIG,synthDriverHandler.setVoice,d.GetSelection()+1)

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
 	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, mainFrame.id_onShowGuiCommand))

def quit():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, wx.ID_EXIT))

def abort():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, mainFrame.id_onAbortCommand))
