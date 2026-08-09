# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2024 NV Access Limited, Cyrille Bougot

"""Provides functionality to view the NVDA log."""

import collections
import time

import comtypes
import wx
import comInterfaces.tom
import globalVars
import gui
import gui.contextHelp
import oleacc
import winUser
from gui import blockAction
from logHandler import log


#: The singleton instance of the log viewer UI.
logViewer = None

#: Target upper bound on how long one append may block the event loop, in seconds.
#: Log text is appended to the output control in chunks sized to this budget, yielding to the
#: event loop in between, so that displaying a large log does not block NVDA's core. (#16322)
_APPEND_TIME_BUDGET_SEC = 0.05
#: Bounds for the adaptive append chunk size, in characters.
#: RichEdit append throughput varies by orders of magnitude with content: text requiring font
#: fallback (e.g. CJK, emoji, braille patterns) appends at roughly 0.03 MB/s, plain ASCII at
#: roughly 12 MB/s. The chunk size is therefore adapted to the measured throughput.
_MIN_CHUNK_SIZE = 1_000
_MAX_CHUNK_SIZE = 1_000_000

#: Passing this as both ends of a TOM range yields a collapsed range at the end of the document,
#: as RichEdit clamps out of range character positions.
_TOM_END_OF_DOC = 0x7FFFFFFF

EM_SETREADONLY = 0x00CF


class LogViewer(
	gui.contextHelp.ContextHelpMixin,
	wx.Frame,  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""The NVDA log viewer GUI."""

	helpId = "LogViewer"

	def __init__(self, parent):
		# Translators: The title of the NVDA log viewer window.
		super(LogViewer, self).__init__(parent, wx.ID_ANY, _("NVDA Log Viewer"))
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.outputCtrl = wx.TextCtrl(
			self,
			wx.ID_ANY,
			size=(500, 500),
			style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH,
		)
		font = self.outputCtrl.GetFont()
		# Set a fixed width font so that the error is correctly pointed in Python tracebacks.
		font.SetFaceName("Consolas")
		self.outputCtrl.SetFont(font)
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
		# Translators: The label for a menu item in NVDA log viewer to exit.
		item = menu.Append(wx.ID_EXIT, _("E&xit"))
		self.Bind(wx.EVT_MENU, self.onClose, item)
		# Translators: The title of a menu in NVDA Log Viewer.
		menuBar.Append(menu, _("Log"))
		self.SetMenuBar(menuBar)

		self._lastFilePos = 0
		#: Log text read from the file but not yet appended to the output control.
		#: A C{None} entry is a marker queued by L{moveInsertionPointToEndOfLog}.
		self._pendingText: collections.deque[str | None] = collections.deque()
		self._isPumpScheduled = False
		self._chunkSize = _MIN_CHUNK_SIZE
		try:
			self._tomDoc = oleacc.AccessibleObjectFromWindow(
				self.outputCtrl.GetHandle(),
				winUser.OBJID_NATIVEOM,
				interface=comInterfaces.tom.ITextDocument,
			)
		except (comtypes.COMError, OSError):
			log.debugWarning("Error getting ITextDocument for the log viewer output control", exc_info=True)
			self._tomDoc = None

		self.refresh()
		self.outputCtrl.SetFocus()

	def refresh(self, evt=None):
		# Ignore if log is not initialized
		if globalVars.appArgs.logFileName is None:
			return
		# Queue text which has been written to the log file since the last refresh for display.
		# It is appended to the output control in chunks by L{_pumpPendingText},
		# as appending a large amount of text in one go blocks NVDA's core for its duration. (#16322)
		try:
			with open(globalVars.appArgs.logFileName, "r", encoding="UTF-8") as f:
				f.seek(self._lastFilePos)
				text = f.read()
				self._lastFilePos = f.tell()
		except IOError:
			return
		if text:
			self._pendingText.append(text)
			self._schedulePump()

	def moveInsertionPointToEndOfLog(self) -> None:
		"""Move the insertion point to the end of the log text queued for display so far.
		Text queued after this call will appear after the insertion point,
		thus leaving the user positioned at the start of that new text.
		"""
		self._pendingText.append(None)
		self._schedulePump()

	def _schedulePump(self) -> None:
		if not self._isPumpScheduled:
			self._isPumpScheduled = True
			# Chain with CallLater rather than CallAfter.
			# Posted events starve WM_TIMER, so a CallAfter chain would block timers,
			# including NVDA's core pump, just like a synchronous append.
			wx.CallLater(1, self._pumpPendingText)

	def _pumpPendingText(self) -> None:
		self._isPumpScheduled = False
		if not self:
			# The window was destroyed while a pump was scheduled.
			return
		chunk = ""
		while self._pendingText and len(chunk) < self._chunkSize:
			item = self._pendingText.popleft()
			if item is None:
				# Marker queued by moveInsertionPointToEndOfLog.
				# Flush the chunk first so that the end of the control is the end of the queued text.
				if chunk:
					self._appendText(chunk)
					chunk = ""
				self.outputCtrl.SetInsertionPointEnd()
				continue
			maxLen = self._chunkSize - len(chunk)
			if len(item) > maxLen:
				self._pendingText.appendleft(item[maxLen:])
				item = item[:maxLen]
			chunk += item
		if chunk:
			self._appendText(chunk)
		if self._pendingText:
			self._schedulePump()

	def _appendText(self, text: str) -> None:
		"""Append text to the output control without disturbing the caret or scroll position.
		Also adapts the chunk size for the next append so that appends stay within the time budget.
		"""
		startTime = time.perf_counter()
		if self._tomDoc:
			# Insert with TOM rather than wx.TextCtrl.AppendText.
			# AppendText moves the caret to the end of the document and back,
			# which costs RichEdit layout work proportional to the total document size
			# (tens of ms per append on a multi MB document, however small the appended text),
			# and causes visible scroll flapping.
			# A TOM range insert leaves the caret and scroll position untouched.
			# TOM refuses to modify a read only control, so read only is lifted for the insert.
			handle = self.outputCtrl.GetHandle()
			winUser.sendMessage(handle, EM_SETREADONLY, False, 0)
			try:
				textRange = self._tomDoc.range(_TOM_END_OF_DOC, _TOM_END_OF_DOC)
				textRange.text = text
			finally:
				winUser.sendMessage(handle, EM_SETREADONLY, True, 0)
		else:
			# Fallback if TOM is unavailable: append and restore the caret.
			pos = self.outputCtrl.GetInsertionPoint()
			self.outputCtrl.Freeze()
			try:
				self.outputCtrl.AppendText(text)
				self.outputCtrl.SetInsertionPoint(pos)
			finally:
				self.outputCtrl.Thaw()
		elapsed = time.perf_counter() - startTime
		if elapsed > 0:
			target = int(len(text) * _APPEND_TIME_BUDGET_SEC / elapsed)
			# Grow at most 4x per append so one unrepresentatively fast append can't overshoot.
			self._chunkSize = max(_MIN_CHUNK_SIZE, min(_MAX_CHUNK_SIZE, target, self._chunkSize * 4))

	def onActivate(self, evt):
		if evt.GetActive():
			self.refresh()
		evt.Skip()

	def onClose(self, evt):
		self.Destroy()

	def onSaveAsCommand(self, evt):
		filename = wx.FileSelector(
			# Translators: Label of a menu item in NVDA Log Viewer.
			_("Save As"),
			default_filename="nvda.log",
			flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
			parent=self,
		)
		if not filename:
			return
		try:
			# #9038: work with UTF-8 from the start.
			with open(filename, "w", encoding="UTF-8") as f:
				f.write(self.outputCtrl.GetValue())
				# Include any log text queued for display but not yet appended to the output control.
				f.write("".join(item for item in self._pendingText if item is not None))
		except (IOError, OSError) as e:
			gui.messageBox(
				# Translators: Dialog text presented when NVDA cannot save a log file.
				_("Error saving log: %s") % e.strerror,
				# Translators: the title of an error message dialog
				_("Error"),
				style=wx.OK | wx.ICON_ERROR,
				parent=self,
			)

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
			wx.OK | wx.ICON_ERROR,
		)
		return
	logViewer.Raise()
	# There is a MAXIMIZE style which can be used on the frame at construction, but it doesn't seem to work the first time it is shown,
	# probably because it was in the background.
	# Therefore, explicitly maximise it here.
	# This also ensures that it will be maximized whenever it is activated, even if the user restored/minimised it.
	logViewer.Maximize()
	logViewer.Show()
