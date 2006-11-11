import time
import threading
import wx
import winUser
import globalVars
import api
import debug
import synthDriverHandler
import config
import versionInfo
import audio

import NVDAThreads

### Constants
appTitle = versionInfo.longName
evt_externalCommand = wx.NewEventType()

### Globals
guiThread = None
mainFrame = None

class MainFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, appTitle, wx.DefaultPosition,wx.DefaultSize, wx.DEFAULT_FRAME_STYLE)
		self.id_onAbortCommand=wx.NewId()
		wx.EVT_COMMAND(self,self.id_onAbortCommand,evt_externalCommand,self.onAbortCommand)
		wx.EVT_COMMAND(self,wx.ID_EXIT,evt_externalCommand,self.onExitCommand)
		wx.EVT_CLOSE(self,self.onExitCommand)
		self.menuBar=wx.MenuBar()
		self.menu_NVDA = wx.Menu()
		self.id_onSaveConfigurationCommand=wx.NewId()
		self.menu_NVDA.Append(self.id_onSaveConfigurationCommand, "&Save configuration\tctrl+s", "Write current configuration to nvda.ini")
		wx.EVT_MENU(self, self.id_onSaveConfigurationCommand, self.onSaveConfigurationCommand)
		self.menu_NVDA.Append(wx.ID_EXIT, "E&xit", "Exit NVDA")
		wx.EVT_MENU(self, wx.ID_EXIT, self.onExitCommand)
		self.menuBar.Append(self.menu_NVDA,"&NVDA")
		self.menu_preferences=wx.Menu()
		self.id_chooseSynthesizerCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseSynthesizerCommand,"&Synthesizer...\tctrl+shift+s","Choose speech synthesizer to use")
		wx.EVT_MENU(self,self.id_chooseSynthesizerCommand,self.onChooseSynthesizerCommand)
		self.id_chooseVoiceCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseVoiceCommand,"&Voice...\tctrl+shift+v","Choose the voice to use")
		wx.EVT_MENU(self,self.id_chooseVoiceCommand,self.onChooseVoiceCommand)
		self.menuBar.Append(self.menu_preferences,"&Preferences")
		self.menu_help = wx.Menu()
		self.menu_help.Append(wx.ID_ABOUT, "&About...", "About NVDA")
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		self.menuBar.Append(self.menu_help,"&Help")
		self.SetMenuBar(self.menuBar)
		self.Show(True)

	def onAbortCommand(self,evt):
		globalVars.stayAlive=False
		self.Destroy()

	def onSaveConfigurationCommand(self,evt):
		config.save()
		NVDAThreads.executeFunction(audio.speakMessage,"Configuration saved")

	def onExitCommand(self, evt):
		self.Raise()
		d = wx.MessageDialog(self, "Are you sure you want to exit NVDA?", "Exit NVDA", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive=False
			self.Destroy()

	def onChooseSynthesizerCommand(self,evt):
		synthList=synthDriverHandler.getDriverList()
		d=wx.SingleChoiceDialog(self,"Choose the speech synthesizer you want to use","Synthesizer",synthList)
		d.SetSelection(synthList.index(synthDriverHandler.driverName))
		if d.ShowModal()==wx.ID_OK:
			NVDAThreads.executeFunction(synthDriverHandler.setDriver,synthList[d.GetSelection()])

	def onChooseVoiceCommand(self,evt):
		d=wx.SingleChoiceDialog(self,"Choose the voice you want to use","Voice",synthDriverHandler.getVoiceNames())
		d.SetSelection(config.getSynthConfig()["voice"]-1)
		if d.ShowModal()==wx.ID_OK:
			NVDAThreads.executeFunction(synthDriverHandler.setVoice,d.GetSelection()+1)

	def onAboutCommand(self,evt):
		aboutInfo="""
%s
Version: %s
URL: %s
%s
"""%(versionInfo.longName,versionInfo.version,versionInfo.url,versionInfo.copyright)
		d = wx.MessageDialog(self, aboutInfo, "About", wx.OK)
		d.ShowModal()

def guiMainLoop():
	global mainFrame
	try:
		app = wx.PySimpleApp()
		mainFrame = MainFrame()
		app.SetTopWindow(mainFrame)
		app.MainLoop()
	except:
		debug.writeException("guiMainLoop")
		audio.speakMessage("Error in GUI main loop")
		globalVars.stayAlive=False

def initialize():
	global guiThread
	guiThread = threading.Thread(target = guiMainLoop)
	guiThread.start()

def exit():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, wx.ID_EXIT))

def abort():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, mainFrame.id_onAbortCommand))
