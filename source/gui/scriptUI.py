"Windows, dialogs and utilities for GUI interaction from scripts."

import queueHandler
import wx
import gui

class ModalDialog:
	"""Base class for modal script dialogs.
	Subclasses should override L{__init__}, L{makeDialog} and L{getResponse}.
	@ivar selfIsDialog: C{True} if the instance itself is the dialog, C{False} if the dialog is contained in self.dialog.
	@type selfIsDialog: bool
	@ivar dialog: The dialog if L{selfIsDialog} is C{False}.
	@type dialog: wx.Dialog
"""

	selfIsDialog = False

	def __init__(self, callback):
		"""Constructor.
		Subclasses should override this, but they must call C{ModalDialog.__init__(self, callback)}.
		@param callback: A function which takes the response from the dialog as its only argument.
		@type callback: callable
	"""
		self._callback = callback

	def getResponse(self, response):
		"""Obtain the response to supply to the callback.
		@param response: The response from the dialog's C{ShowModal} method.
		@return: The response to supply to the callback.
	"""
		return response

	def _run_gui(self):
		if self.selfIsDialog:
			self.makeDialog()
			dialog = self
		else:
			dialog = self.dialog = self.makeDialog()
		dialog.Raise()
		ret = self.getResponse(dialog.ShowModal())
		dialog.Destroy()
		return ret

	def run(self):
		"""Run this dialog.
		This displays the dialog and calls the callback with the relevant response once the user has dismissed the dialog.
	"""
		gui.execute(self._run_gui, callback=self._callback)

class MessageDialog(ModalDialog):

	def __init__(self, message, title = _("NVDA"), style=wx.OK, callback=None):
		ModalDialog.__init__(self, callback)
		self.makeDialog = lambda: wx.MessageDialog(None, message, title, style)

	def getResponse(self, response):
		return response in (wx.ID_OK, wx.ID_YES)

class TextEntryDialog(ModalDialog):

	def __init__(self, message, title=_("NVDA"), default="", style=wx.OK | wx.CANCEL, callback=None):
		ModalDialog.__init__(self, callback)
		self.makeDialog = lambda: wx.TextEntryDialog(None, message, title, defaultValue=default, style=style)

	def getResponse(self, response):
		if response == wx.ID_OK:
			return self.dialog.GetValue()
		else:
			return None

class SingleChoiceDialog(wx.Dialog, ModalDialog):

	selfIsDialog = True
	def __init__(self, message, title=_("NVDA"), choices=(), default=0, style=wx.OK|wx.CANCEL, callback=None):
		ModalDialog.__init__(self, callback)
		def makeDialog():
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
		self.makeDialog = makeDialog

	def getResponse(self, response):
		if response == wx.ID_OK:
			sel = self.list.GetFirstSelected()
			if sel == -1: return None
			return sel, self.list.GetItemText(sel)
		else:
			return None
