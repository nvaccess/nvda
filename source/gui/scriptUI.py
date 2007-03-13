"Windows, dialogs and utilities for GUI interaction from scripts."

import queueHandler
import wx
import gui

class ModalDialog:
	def __init__(self, callback):
		self._callback = callback

	def run_gui(self):
		raise NotImplementedError

	def run(self):
		gui.execute(self.run_gui, callback=self._callback)

class MessageDialog(ModalDialog):

	def __init__(self, message, title = _("NVDA"), style=wx.OK, callback=None):
		ModalDialog.__init__(self, callback)
		self._window = wx.MessageDialog(None, message, title, style)

	def run_gui(self):
		ret = self._window.ShowModal()
		self._window.Destroy()
		return ret in (wx.ID_OK, wx.ID_YES)

class TextEntryDialog(ModalDialog):

	def __init__(self, message, title=_("NVDA"), default="", style=wx.OK | wx.CANCEL, callback=None):
		ModalDialog.__init__(self, callback)
		self._makeDialog = lambda: wx.TextEntryDialog(None, message, title, defaultValue=default, style=style)

	def run_gui(self):
		dialog = self._makeDialog()
		dialog.Raise()
		ret = dialog.ShowModal()
		dialog.Destroy()
		if ret == wx.ID_OK:
			return dialog.GetValue()
		else:
			return None

class SingleChoiceDialog(wx.Dialog, ModalDialog):

	def __init__(self, message, title=_("NVDA"), choices=(), default=0, style=wx.OK|wx.CANCEL, callback=None):
		ModalDialog.__init__(self, callback)
		def initDialog():
			wx.Dialog.__init__(self, None, -1, title)
			mainSizer = wx.BoxSizer(wx.VERTICAL)
			mainSizer.Add(wx.StaticText(self, -1, label=message))
			self.list = wx.ListView(self, -1, style=wx.LC_LIST | wx.LC_SINGLE_SEL)
			self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda evt: self.EndModal(wx.ID_OK))
			for index, choice in enumerate(choices):
				self.list.InsertStringItem(index, choice)
			self.list.Focus(default)
			self.list.Select(default)
			mainSizer.Add(self.list)
			mainSizer.Add(self.CreateButtonSizer(style), flag=wx.BOTTOM)
			mainSizer.Fit(self)
			self.SetSizer(mainSizer)
			self.list.SetFocus()
		self._initDialog = initDialog

	def run_gui(self):
		self._initDialog()
		self.Raise()
		ret = self.ShowModal()
		self.Destroy()
		if ret == wx.ID_OK:
			sel = self.list.GetFirstSelected()
			if sel == -1: return None
			return sel, self.list.GetItemText(sel)
		else:
			return None
