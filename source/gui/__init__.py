import time
import threading
import wx
import winUser
import globalVars
import debug

### Constants
appTitle = "Nonvisual Desktop Access"

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
		self.SetMenuBar(self.menuBar)
		self.Show(True)

	def onExitCommand(self, evt):
		d = wx.MessageDialog(self, "Are you sure you want to exit NVDA?", "Exit NVDA", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive=False
			self.Destroy()

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





