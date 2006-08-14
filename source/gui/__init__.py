import threading
import wx
import win32gui
import globalVars
import debug

### Constants
appTitle = "NVDA"
id_exitCommand = wx.NewId()
evt_externalCommand = wx.NewEventType()
id_showGuiCommand = wx.NewId()

### Globals
guiThread = None
mainFrame = None

class MainFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, appTitle)
		wx.EVT_COMMAND(self, id_showGuiCommand, evt_externalCommand, self.onShowGuiCommand)

	def onShowGuiCommand(self, evt):
		MenuFrame(self)

class MenuFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, wx.ID_ANY, appTitle, wx.GetMousePosition())
		self.menu = wx.Menu()
		self.menu.Append(id_exitCommand, "E&xit", "Exit NVDA")
		wx.EVT_MENU(self, id_exitCommand, self.onExitCommand)
		self.Show(True)
		fg = win32gui.GetForegroundWindow()
		try:
			win32gui.SetForegroundWindow(self.GetHandle())
		except:
			debug.writeException("gui.MenuFrame.__init__")
		self.PopupMenuXY(self.menu, 0, 0)
		self.Close(True)
		try:
			win32gui.SetForegroundWindow(fg)
		except:
			debug.writeException("gui.MenuFrame.__init__")
	
	def onExitCommand(self, evt):
		d = wx.MessageDialog(self, "Are you sure you want to exit NVDA?", "Exit NVDA", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
		if d.ShowModal() == wx.ID_YES:
			globalVars.stayAlive = False

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

def terminate():
	mainFrame.Close(True)

def showGui():
	mainFrame.GetEventHandler().AddPendingEvent(wx.PyCommandEvent(evt_externalCommand, id_showGuiCommand))
