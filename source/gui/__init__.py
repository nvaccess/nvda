import versionInfo
import time
import threading
import wx
import winUser
import globalVars
import api
import debug
import synthDriverHandler
from config import conf
import NVDAThreads

### Constants
appTitle = versionInfo.longName
evt_externalCommand = wx.NewEventType()

### Globals
guiThread = None
mainFrame = None

class MainFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, appTitle)
		wx.EVT_CLOSE(self,self.onExitCommand)
		self.menuBar=wx.MenuBar()
		self.menu_NVDA = wx.Menu()
		self.menu_NVDA.Append(wx.ID_EXIT, "E&xit", "Exit NVDA")
		wx.EVT_MENU(self, wx.ID_EXIT, self.onExitCommand)
		self.menuBar.Append(self.menu_NVDA,"&NVDA")
		self.menu_preferences=wx.Menu()
		self.id_chooseSynthesizerCommand=wx.NewId()
		self.menu_preferences.Append(self.id_chooseSynthesizerCommand,"Synthesizer...","Choose speech synthesizer to use")
		wx.EVT_MENU(self,self.id_chooseSynthesizerCommand,self.onChooseSynthesizerCommand)
		self.menuBar.Append(self.menu_preferences,"&Preferences")
		self.menu_help = wx.Menu()
		self.menu_help.Append(wx.ID_ABOUT, "&About...", "About NVDA")
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		self.menuBar.Append(self.menu_help,"&Help")
		self.SetMenuBar(self.menuBar)
		wx.EVT_COMMAND(self,wx.ID_EXIT,evt_externalCommand,self.onExitCommand)
		self.Show(True)

	def onExitCommand(self, evt):
		self.Raise()
		d = wx.MessageDialog(self, "Are you sure you want to exit NVDA?", "Exit NVDA", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive=False
			self.Destroy()

	def onChooseSynthesizerCommand(self,evt):
		synthList=synthDriverHandler.getSynthDriverList()
		d=wx.SingleChoiceDialog(self,"Choose the speech synthesizer you want to use","Synthesizer",synthList)
		d.SetSelection(synthList.index(synthDriverHandler.current.getName()))
		res=d.ShowModal()
		if res:
			NVDAThreads.executeFunction(synthDriverHandler.load,synthList[d.GetSelection()])

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
