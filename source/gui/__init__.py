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
import lang
from constants import *

import core

### Constants
appTitle = versionInfo.longName
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
		self.id_onSaveConfigurationCommand=wx.NewId()
		self.menu_NVDA.Append(self.id_onSaveConfigurationCommand, lang.gui["menuSaveConfiguration"]+"\tctrl+s", lang.gui["menuDescSaveConfiguration"])
		wx.EVT_MENU(self, self.id_onSaveConfigurationCommand, self.onSaveConfigurationCommand)
		self.menu_NVDA.Append(wx.ID_EXIT, lang.gui["menuExit"],lang.gui["menuDescExit"])
		wx.EVT_MENU(self, wx.ID_EXIT, self.onExitCommand)
		self.menuBar.Append(self.menu_NVDA,lang.gui["menuNVDA"])
		self.menu_preferences=wx.Menu()
		self.id_chooseSynthesizerCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseSynthesizerCommand,lang.gui["menuSynthesizer"]+"...\tctrl+shift+s",lang.gui["menuDescSynthesizer"])
		wx.EVT_MENU(self,self.id_chooseSynthesizerCommand,self.onSynthesizerCommand)
		self.id_chooseVoiceCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseVoiceCommand,lang.gui["menuVoice"]+"...\tctrl+shift+v",lang.gui["menuDescVoice"])
		wx.EVT_MENU(self,self.id_chooseVoiceCommand,self.onVoiceCommand)
		self.menuBar.Append(self.menu_preferences,lang.gui["menuPreferences"])
		self.menu_help = wx.Menu()
		self.menu_help.Append(wx.ID_ABOUT, lang.gui["menuAbout"]+"...", lang.gui["menuDescAbout"])
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		self.menuBar.Append(self.menu_help,lang.gui["menuHelp"])
		self.SetMenuBar(self.menuBar)
		#self.icon=wx.Icon(iconPath,wx.BITMAP_TYPE_BMP)
		#self.SetIcon(self.icon)

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


	def onSaveConfigurationCommand(self,evt):
		config.save()
		core.executeFunction(EXEC_SPEECH,audio.speakMessage,lang.messages["savedConfiguration"])

	def onExitCommand(self, evt):
		d = wx.MessageDialog(None, lang.gui["messageExit"], lang.gui["titleExit"], wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive=False
			self.Destroy()
		elif not shown:
			self.onHideGui(None)

	def onSynthesizerCommand(self,evt):
		synthList=synthDriverHandler.getDriverList()
		choices=[]
		for item in synthList:
			choices.append("%s: %s"%(item,synthDriverHandler.getDriverDescription(item)))
		d=wx.SingleChoiceDialog(self,lang.gui["messageSynthesizer"],lang.gui["titleSynthesizer"],choices)
		d.SetSelection(synthList.index(synthDriverHandler.driverName))
		if d.ShowModal()==wx.ID_OK:
			core.executeFunction(EXEC_CONFIG,synthDriverHandler.setDriver,synthList[d.GetSelection()])

	def onVoiceCommand(self,evt):
		d=wx.SingleChoiceDialog(self,lang.gui["messageVoice"],lang.gui["titleVoice"],synthDriverHandler.getVoiceNames())
		d.SetSelection(config.getSynthConfig()["voice"]-1)
		if d.ShowModal()==wx.ID_OK:
			core.executeFunction(EXEC_CONFIG,synthDriverHandler.setVoice,d.GetSelection()+1)

	def onAboutCommand(self,evt):
		try:
			aboutInfo="""
%s
%s: %s
%s: %s
%s: %s <%s>
%s: %s
"""%(versionInfo.longName,lang.gui["version"],versionInfo.version,lang.gui["url"],versionInfo.url,lang.gui["maintainer"],versionInfo.maintainer,versionInfo.maintainer_email,lang.gui["copyright"],versionInfo.copyright)
			d = wx.MessageDialog(self, aboutInfo, lang.gui["titleAbout"], wx.OK)
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

def exit():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, wx.ID_EXIT))

def abort():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, mainFrame.id_onAbortCommand))
