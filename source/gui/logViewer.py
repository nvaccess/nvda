# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2022 NV Access Limited

"""Provides functionality to view the NVDA log.
"""

import wx
import globalVars
import gui
import gui.contextHelp
from gui import blockAction


#: The singleton instance of the log viewer UI.
logViewer = None


class LogViewer(
		gui.contextHelp.ContextHelpMixin,
		wx.Frame  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""The NVDA log viewer GUI.
	"""
	
	helpId = "LogViewer"

	def __init__(self, parent):
		# Translators: The title of the NVDA log viewer window.
		super(LogViewer, self).__init__(parent, wx.ID_ANY, _("NVDA Log Viewer"))
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE | wx.TE_READONLY|wx.TE_RICH)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		mainSizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

		menuBar = wx.MenuBar()
		menu = wx.Menu()
		# Translators: The label for a menu item in NVDA log viewer to refresh log messages.
		item = menu.Append(wx.ID_ANY, _("Refresh	F5"))
		self.Bind(wx.EVT_MENU, self.refresh, item)
		# Translators: The label for a menu item in NVDA log viewer to save log file.
		item = menu.Append(wx.ID_SAVEAS, _("Save &as...	Ctrl+S"))
		self.Bind(wx.EVT_MENU, self.onSaveAsCommand, item)
		menu.AppendSeparator()
		item = menu.Append(wx.ID_EXIT, _("E&xit"))
		self.Bind(wx.EVT_MENU, self.onClose, item)
		# Translators: The title of a menu in NVDA Log Viewer.
		menuBar.Append(menu, _("Log"))
		self.SetMenuBar(menuBar)

		self._lastFilePos = 0

		self.refresh()
		self.outputCtrl.SetFocus()

	def refresh(self, evt=None):
		# Ignore if log is not initialized
		if(globalVars.appArgs.logFileName is None):
			return
		pos = self.outputCtrl.GetInsertionPoint()
		# Append new text to the output control which has been written to the log file since the last refresh.
		try:
			f = open(globalVars.appArgs.logFileName, "r", encoding="UTF-8")
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
		# Translators: Label of a menu item in NVDA Log Viewer.
		filename = wx.FileSelector(_("Save As"), default_filename="nvda.log", flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, parent=self)
		if not filename:
			return
		try:
			# #9038: work with UTF-8 from the start.
			with open(filename, "w", encoding="UTF-8") as f:
				f.write(self.outputCtrl.GetValue())
		except (IOError, OSError) as e:
			# Translators: Dialog text presented when NVDA cannot save a log file.
			gui.messageBox(_("Error saving log: %s") % e.strerror, _("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def onOutputKeyDown(self, evt):
		key = evt.GetKeyCode()
		# #3763: WX 3 no longer passes escape via evt_char in richEdit controls. Therefore evt_key_down must be used.
		if key == wx.WXK_ESCAPE:
			self.Close()
			return
		evt.Skip()


# The log might expose sensitive information and the Save As dialog in the Log Viewer is a security risk.
@blockAction.when(blockAction.Context.SECURE_MODE)
def activate():
	"""Activate the log viewer.
	If the log viewer has not already been created and opened, this will create and open it.
	Otherwise, it will be brought to the foreground if possible.
	"""
	global logViewer
	if not logViewer:
		logViewer = LogViewer(gui.mainFrame)
	# Check if log was properly initialized
	if globalVars.appArgs.logFileName is None:
		wx.CallAfter(
			gui.messageBox,
			# Translators: A message indicating that log cannot be loaded to LogViewer.
			_("Log is unavailable"),
			# Translators: The title of an error message dialog.
			_("Error"),
			wx.OK | wx.ICON_ERROR
		)
		return
	logViewer.Raise()
	# There is a MAXIMIZE style which can be used on the frame at construction, but it doesn't seem to work the first time it is shown,
	# probably because it was in the background.
	# Therefore, explicitly maximise it here.
	# This also ensures that it will be maximized whenever it is activated, even if the user restored/minimised it.
	logViewer.Maximize()
	logViewer.Show()
