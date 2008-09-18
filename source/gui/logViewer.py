"""Provides functionality to view the NVDA log.
"""

import codecs
import wx
import globalVars
import gui

#: The singleton instance of the log viewer UI.
logViewer = None

class LogViewer(wx.Frame):
	"""The NVDA log viewer GUI.
	"""

	def __init__(self, parent):
		super(LogViewer, self).__init__(parent, wx.ID_ANY, _("NVDA Log Viewer"))
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE | wx.TE_READONLY|wx.TE_RICH)
		mainSizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

		menuBar = wx.MenuBar()
		menu = wx.Menu()
		item = menu.Append(wx.ID_ANY, _("Refresh	F5"))
		self.Bind(wx.EVT_MENU, self.refresh, item)
		item = menu.Append(wx.ID_SAVEAS)
		self.Bind(wx.EVT_MENU, self.onSaveAsCommand, item)
		menu.AppendSeparator()
		item = menu.Append(wx.ID_EXIT, _("E&xit"))
		self.Bind(wx.EVT_MENU, self.onClose, item)
		menuBar.Append(menu, _("Log"))
		self.SetMenuBar(menuBar)

		self._lastFilePos = 0

		self.refresh()
		self.outputCtrl.SetFocus()

	def refresh(self, evt=None):
		pos = self.outputCtrl.GetInsertionPoint()
		# Append new text to the output control which has been written to the log file since the last refresh.
		try:
			f = codecs.open(globalVars.appArgs.logFileName, "r", encoding="UTF-8")
			f.seek(self._lastFilePos)
			self.outputCtrl.AppendText(f.read())
			self._lastFilePos = f.tell()
			self.outputCtrl.SetInsertionPoint(pos)
			f.close()
		except IOError:
			pass

	def onActivate(self, evt):
		if evt.GetActive():
			self.refresh()
		evt.Skip()

	def onClose(self, evt):
		self.Destroy()

	def onSaveAsCommand(self, evt):
		filename = wx.FileSelector(_("Save As"), default_filename="nvda.log", flags=wx.SAVE | wx.OVERWRITE_PROMPT, parent=self)
		if not filename:
			return
		try:
			# codecs.open() forces binary mode, which is bad under Windows because line endings won't be converted to crlf automatically.
			# Therefore, do the encoding manually.
			file(filename, "w").write(self.outputCtrl.GetValue().encode("UTF-8"))
		except (IOError, OSError), e:
			wx.MessageBox(_("Error saving log: %s") % e.strerror, _("Error"), style=wx.OK | wx.ICON_ERROR)

def activate():
	"""Activate the log viewer.
	If the log viewer has not already been created and opened, this will create and open it.
	Otherwise, it will be brought to the foreground if possible.
	"""
	global logViewer
	if not logViewer:
		logViewer = LogViewer(gui.mainFrame)
	logViewer.Raise()
	logViewer.Show()
