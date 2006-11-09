import versionInfo
import time
import threading
import wx
import winUser
import globalVars
import debug

### Constants
appTitle = versionInfo.longName

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
		self.menu_help = wx.Menu()
		self.menu_help.Append(wx.ID_ABOUT, "&About...", "About NVDA")
		wx.EVT_MENU(self, wx.ID_ABOUT, self.onAboutCommand)
		self.menuBar.Append(self.menu_help,"&Help")
		self.SetMenuBar(self.menuBar)
		self.Show(True)

	def onExitCommand(self, evt):
		d = wx.MessageDialog(self, "Are you sure you want to exit NVDA?", "Exit NVDA", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive=False
			self.Destroy()

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
	app = wx.PySimpleApp()
	mainFrame = MainFrame()
	app.SetTopWindow(mainFrame)
	app.MainLoop()

def initialize():
	global guiThread
	guiThread = threading.Thread(target = guiMainLoop)
	guiThread.start()

def exit():
	mainFrame.Close(True)





