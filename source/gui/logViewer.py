"""Provides functionality to view the NVDA log.
"""

import logging
import wx
import globalVars
import gui

class LogViewer(wx.Frame):
	"""The NVDA log viewer GUI.
	"""

	def __init__(self):
		super(LogViewer, self).__init__(None, wx.ID_ANY, _("NVDA Log Viewer"))
		gui.topLevelWindows.append(self)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE | wx.TE_READONLY)
		mainSizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

		# Populate the output control with the contents of the log file.
		try:
			self.outputCtrl.SetValue(file(globalVars.appArgs.logFileName, "r").read())
		except IOError:
			pass

		# Install a log handler to direct future output to the output control.
		# wx.TextCtrl does not support flush(), so fudge it.
		self.outputCtrl.flush = lambda: None
		self.logHandler = logging.StreamHandler(self.outputCtrl)
		self.logHandler.setFormatter(globalVars.log.handlers[0].formatter)
		globalVars.log.addHandler(self.logHandler)

		self.outputCtrl.SetFocus()

	def onClose(self, evt):
		self.Destroy()

	def Destroy(self):
		gui.topLevelWindows.remove(self)
		globalVars.log.removeHandler(self.logHandler)
		self.logHandler.close()
		super(LogViewer, self).Destroy()
