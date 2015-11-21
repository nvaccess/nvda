"""Provides functionality to view the NVDA log.
"""

import codecs
import wx
import globalVars
import gui
import re

#: The singleton instance of the log viewer UI.
logViewer = None

class FindDialog(wx.Dialog):
	"""A dialog used to specify text to find in the log.
	"""

	def __init__(self, parent, text, caseSensitive, regEx):
		# Translators: Title of a dialog to find text.
		super(FindDialog, self).__init__(parent, wx.ID_ANY, _("Find"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		findSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Dialog text for the log viewer find command.
		textToFind = wx.StaticText(self, wx.ID_ANY, label=_("Type the text you wish to find:"))
		findSizer.Add(textToFind)
		self.findTextField = wx.TextCtrl(self, wx.ID_ANY)
		self.findTextField.SetValue(text)
		findSizer.Add(self.findTextField)
		mainSizer.Add(findSizer,border=20,flag=wx.LEFT|wx.RIGHT|wx.TOP)
		# Translators: An option in find dialog to perform case-sensitive search.
		self.caseSensitiveCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Case &sensitive"))
		self.caseSensitiveCheckBox.SetValue(caseSensitive)
		mainSizer.Add(self.caseSensitiveCheckBox,border=10,flag=wx.BOTTOM)
		# Translators: An option in find dialog to perform regular expressioon search.
		self.regExCheckBox=wx.CheckBox(self,wx.NewId(),label=_("Regular &expression"))
		self.regExCheckBox.SetValue(regEx)
		mainSizer.Add(self.regExCheckBox,border=10,flag=wx.BOTTOM)

		mainSizer.AddSizer(self.CreateButtonSizer(wx.OK|wx.CANCEL))
		self.Bind(wx.EVT_BUTTON,self.onOk,id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON,self.onCancel,id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)
		self.findTextField.SetFocus()

	def onOk(self, evt):
		global logViewer
		text = self.findTextField.GetValue()
		caseSensitive = self.caseSensitiveCheckBox.GetValue()
		regEx = self.regExCheckBox.GetValue()
		wx.CallLater(100, logViewer.doFindText, text, caseSensitive=caseSensitive, regEx=regEx)
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

class LogViewer(wx.Frame):
	"""The NVDA log viewer GUI.
	"""

	def __init__(self, parent):
		self._lastFindText=""
		self._findCaseSensitive=False
		self._findRegEx=False

		# Translators: The title of the NVDA log viewer window.
		super(LogViewer, self).__init__(parent, wx.ID_ANY, _("NVDA Log Viewer"))
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(self, wx.ID_ANY, size=(500, 500), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.TE_RICH)
		self.outputCtrl.Bind(wx.EVT_KEY_DOWN, self.onOutputKeyDown)
		mainSizer.Add(self.outputCtrl, proportion=1, flag=wx.EXPAND)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)

		menuBar = wx.MenuBar()
		menu = wx.Menu()
		# Translators: The label for a menu item in NVDA log viewer to refresh log messages.
		item = menu.Append(wx.ID_ANY, _("&Refresh	F5"))
		self.Bind(wx.EVT_MENU, self.refresh, item)
		item = menu.Append(wx.ID_SAVEAS)
		self.Bind(wx.EVT_MENU, self.onSaveAs, item)
		menu.AppendSeparator()
		# Translators: The label for a menu item in NVDA log viewer to search for text.
		item = menu.Append(wx.ID_ANY, _("&Find	Ctrl+F"))
		self.Bind(wx.EVT_MENU, self.onFind, item)
		# Translators: The label for a menu item in NVDA log viewer to search for the next matching text.
		item = menu.Append(wx.ID_ANY, _("Find &next	F3"))
		self.Bind(wx.EVT_MENU, self.onFindNext, item)
		# Translators: The label for a menu item in NVDA log viewer to search for the previous matching text.
		item = menu.Append(wx.ID_ANY, _("Find &previous	Shift+F3"))
		self.Bind(wx.EVT_MENU, self.onFindPrevious, item)
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

	def onSaveAs(self, evt):
		# Translators: Label of a menu item in NVDA Log Viewer.
		filename = wx.FileSelector(_("Save As"), default_filename="nvda.log", flags=wx.SAVE | wx.OVERWRITE_PROMPT, parent=self)
		if not filename:
			return
		try:
			# codecs.open() forces binary mode, which is bad under Windows because line endings won't be converted to crlf automatically.
			# Therefore, do the encoding manually.
			file(filename, "w").write(self.outputCtrl.GetValue().encode("UTF-8"))
		except (IOError, OSError), e:
			# Translators: Dialog text presented when NVDA cannot save a log file.
			gui.messageBox(_("Error saving log: %s") % e.strerror, _("Error"), style=wx.OK | wx.ICON_ERROR, parent=self)

	def onFind(self, evt):
		self._getFindDialog()

	def onFindNext(self, evt):
		if not self._lastFindText:
			self._getFindDialog()
			return
		self.doFindText(self._lastFindText, caseSensitive=self._findCaseSensitive, regEx=self._findRegEx)

	def onFindPrevious(self, evt):
		if not self._lastFindText:
			self._getFindDialog()
			return
		self.doFindText(self._lastFindText, caseSensitive=self._findCaseSensitive, regEx=self._findRegEx, reverse=True)

	def onOutputKeyDown(self, evt):
		key = evt.GetKeyCode()
		# #3763: WX 3 no longer passes escape via evt_char in richEdit controls. Therefore evt_key_down must be used.
		if key == wx.WXK_ESCAPE:
			self.Close()
			return
		evt.Skip()

	def doFindText(self, text, reverse=False, caseSensitive=False, regEx=False):
		if not text:
			return
		pattern=text if regEx else re.escape(text)
		pos = self.outputCtrl.GetInsertionPoint()
		inText=self.outputCtrl.GetValue().encode("UTF-8")
		if reverse:
			# When searching in reverse, we reverse the text and the pattern, if it is not a regex, and do a forwards search.
			if not regEx:
				pattern=pattern[::-1]
			# Start searching one before the start to avoid finding the current match.
			inText=inText[0:pos][pos::-1]
		else:
			# Start searching one past the start to avoid finding the current match.
			inText=inText[pos+1:]
		m=re.search(pattern,inText,(0 if caseSensitive else re.IGNORECASE)|re.UNICODE)
		if not m:
			wx.CallAfter(gui.messageBox,_('Text "%s" not found.')%text,_("Find Error"),wx.OK|wx.ICON_ERROR)
		else:
			if reverse:
				self.outputCtrl.SetSelection(pos-m.start(),pos-m.end())
			else:
				self.outputCtrl.SetSelection(pos+1+m.start(),pos+1+m.end())
		self._lastFindText=text
		self._findCaseSensitive=caseSensitive
		self._findRegEx=regEx

	def _getFindDialog(self):
		d = FindDialog(self, self._lastFindText, self._findCaseSensitive, self._findRegEx)
		d.Show()

def activate():
	"""Activate the log viewer.
	If the log viewer has not already been created and opened, this will create and open it.
	Otherwise, it will be brought to the foreground if possible.
	"""
	global logViewer
	if globalVars.appArgs.secure:
		# The log might expose sensitive information and the Save As dialog in the Log Viewer is a security risk.
		return
	if not logViewer:
		logViewer = LogViewer(gui.mainFrame)
	logViewer.Raise()
	# There is a MAXIMIZE style which can be used on the frame at construction, but it doesn't seem to work the first time it is shown,
	# probably because it was in the background.
	# Therefore, explicitly maximise it here.
	# This also ensures that it will be maximized whenever it is activated, even if the user restored/minimised it.
	logViewer.Maximize()
	logViewer.Show()
