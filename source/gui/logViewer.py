# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2008-2024 NV Access Limited, Cyrille Bougot

"""Provides functionality to view the NVDA log."""

import re  # noqa: I001
import wx
import addonHandler
import globalVars
import gui
import gui.contextHelp
from gui import blockAction


#: The singleton instance of the log viewer UI.
logViewer = None

#: Matches the header line of a log entry, e.g.
#: "IO - inputCore.InputManager.executeGesture (09:17:40.724) - Thread-5 (13576):"
#: Capturing the codepath (e.g. "external:globalPlugins.foo.MyClass.myFunc") in group 1.
_LOG_ENTRY_HEADER_REGEX = re.compile(r"^[A-Z_]+ - (\S+) \(.*?\) - .*:$", re.MULTILINE)


class LogViewer(
	gui.contextHelp.ContextHelpMixin,
	wx.Frame,  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""The NVDA log viewer GUI."""

	helpId = "LogViewer"

	def __init__(self, parent):
		# Translators: The title of the NVDA log viewer window.
		super().__init__(parent, wx.ID_ANY, _("NVDA Log Viewer"))
		self.Bind(wx.EVT_ACTIVATE, self.onActivate)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		filterSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label for a control in the NVDA log viewer to filter log messages by add-on.
		filterLabel = wx.StaticText(self, label=_("&Filter by add-on:"))
		filterSizer.Add(filterLabel, flag=wx.ALIGN_CENTRE_VERTICAL)
		self._addonFilterChoice = wx.Choice(self)
		filterSizer.Add(self._addonFilterChoice)
		mainSizer.Add(filterSizer, flag=wx.EXPAND)
		self._populateAddonFilterChoice()
		self._addonFilterChoice.Bind(wx.EVT_CHOICE, self.onFilterChanged)

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
		self._rawText = ""

		self.refresh()
		self.outputCtrl.SetFocus()

	def _populateAddonFilterChoice(self):
		# index 0 is always "All add-ons" (no filter), represented by None.
		self._filterAddons: list[addonHandler.Addon | None] = [None]
		availableAddons = sorted(
			addonHandler.getAvailableAddons(),
			key=lambda addon: addon.manifest["summary"],
		)
		# Translators: An item in the add-on filter list in the NVDA log viewer meaning no filter is applied.
		choices = [_("All add-ons")]
		for addon in availableAddons:
			self._filterAddons.append(addon)
			choices.append(addon.manifest["summary"])
		self._addonFilterChoice.SetItems(choices)
		self._addonFilterChoice.SetSelection(0)

	def setAddonFilter(self, addon: addonHandler.Addon):
		"""Selects the given add-on in the filter list and re-renders the log to match.
		@param addon: The add-on to filter log entries by.
		"""
		for index, filterAddon in enumerate(self._filterAddons):
			if filterAddon is not None and filterAddon.name == addon.name:
				self._addonFilterChoice.SetSelection(index)
				break
		self._render()

	def onFilterChanged(self, evt):
		self._render()

	def _render(self):
		"""Updates the output control to show the raw log text, filtered to the selected add-on if any."""
		pos = self.outputCtrl.GetInsertionPoint()
		filterAddon = self._filterAddons[self._addonFilterChoice.GetSelection()]
		if filterAddon is None:
			text = self._rawText
		else:
			prefixes = filterAddon.getLogModulePrefixes()
			addonPath = filterAddon.path
			text = "".join(
				entryText
				for codepath, entryText in self._iterLogEntries(self._rawText)
				if self._codepathMatchesPrefixes(codepath, prefixes)
				or self._entryMentionsAddonPath(entryText, addonPath)
			)
		self.outputCtrl.ChangeValue(text)
		self.outputCtrl.SetInsertionPoint(pos)

	@staticmethod
	def _iterLogEntries(text: str):
		"""Splits raw log text into (codepath, entryText) pairs, one per log entry.
		Any text before the first recognised log entry header is discarded.
		@param text: The raw log text to split.
		@return: An iterator of tuples, each containing the entry's codepath and its full text,
			header line included.
		"""
		headerMatches = list(_LOG_ENTRY_HEADER_REGEX.finditer(text))
		for index, headerMatch in enumerate(headerMatches):
			start = headerMatch.start()
			end = headerMatches[index + 1].start() if index + 1 < len(headerMatches) else len(text)
			yield headerMatch.group(1), text[start:end]

	@staticmethod
	def _codepathMatchesPrefixes(codepath: str, prefixes: set[str]) -> bool:
		codepath = codepath.removeprefix("external:")
		return any(codepath == prefix or codepath.startswith(f"{prefix}.") for prefix in prefixes)

	@staticmethod
	def _entryMentionsAddonPath(entryText: str, addonPath: str) -> bool:
		"""Whether the add-on's own install directory appears anywhere in the entry's text.
		This catches entries logged by NVDA's own code on the add-on's behalf, such as a traceback
		logged by the plugin loader when an add-on fails to import, where the codepath points at the
		loader rather than at the add-on.
		"""
		return addonPath.lower() in entryText.lower()

	def refresh(self, evt=None):
		# Ignore if log is not initialized
		if globalVars.appArgs.logFileName is None:
			return
		# Read new text which has been written to the log file since the last refresh.
		try:
			f = open(globalVars.appArgs.logFileName, "r", encoding="UTF-8")  # noqa: SIM115
			f.seek(self._lastFilePos)
			self._rawText += f.read()
			self._lastFilePos = f.tell()
			f.close()
		except OSError:
			return
		self._render()

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
		except OSError as e:
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
def activate(addonFilter: addonHandler.Addon | None = None):
	"""Activate the log viewer.
	If the log viewer has not already been created and opened, this will create and open it.
	Otherwise, it will be brought to the foreground if possible.
	@param addonFilter: If given, the log viewer's add-on filter is set to this add-on.
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
	if addonFilter is not None:
		logViewer.setAddonFilter(addonFilter)
	logViewer.Raise()
	# There is a MAXIMIZE style which can be used on the frame at construction, but it doesn't seem to work the first time it is shown,
	# probably because it was in the background.
	# Therefore, explicitly maximise it here.
	# This also ensures that it will be maximized whenever it is activated, even if the user restored/minimised it.
	logViewer.Maximize()
	logViewer.Show()
