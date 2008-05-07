"""Windows, dialogs and utilities for GUI interaction from scripts.
"""

import queueHandler
import wx
import gui

class ModalDialog(object):
	"""Base class for modal script dialogs.
	Subclasses should override L{__init__}, L{makeDialog} and L{getResponse}.
	@ivar dialog: The dialog or C{None} if it has not yet been created.
	@type dialog: wx.Dialog
	"""

	def __init__(self, callback):
		"""Constructor.
		Subclasses should extend this; i.e. they must call this base class method.
		@param callback: A function which takes the response from the dialog as its only argument.
		@type callback: callable
		"""
		self._callback = callback

	def makeDialog(self):
		"""Make the dialog.
		@return: The dialog.
		@rtype: wx.Dialog
		"""
		raise NotImplementedError

	def getResponse(self, response):
		"""Obtain the response to supply to the callback.
		@param response: The response from the dialog's C{ShowModal} method.
		@return: The response to supply to the callback.
	"""
		return response

	def _run_gui(self):
		gui.mainFrame.prePopup()
		dialog = self.dialog = self.makeDialog()
		ret = self.getResponse(dialog.ShowModal())
		gui.mainFrame.postPopup()
		dialog.Destroy()
		return ret

	def run(self):
		"""Run this dialog.
		This displays the dialog and calls the callback with the relevant response once the user has dismissed the dialog.
		"""
		gui.execute(self._run_gui, callback=self._callback)

class MessageDialog(ModalDialog):

	def __init__(self, message, title = _("NVDA"), style=wx.OK, callback=None):
		self.makeDialog = lambda: wx.MessageDialog(gui.mainFrame, message, title, style)
		super(MessageDialog, self).__init__(callback)

	def getResponse(self, response):
		return response in (wx.ID_OK, wx.ID_YES)

class TextEntryDialog(ModalDialog):

	def __init__(self, message, title=_("NVDA"), default="", style=wx.OK | wx.CANCEL, callback=None):
		self.makeDialog = lambda: wx.TextEntryDialog(gui.mainFrame, message, title, defaultValue=default, style=style)
		super(TextEntryDialog, self).__init__(callback)

	def getResponse(self, response):
		if response == wx.ID_OK:
			return self.dialog.GetValue()
		else:
			return None

class SingleChoiceDialog(ModalDialog):

	def __init__(self, message, title=_("NVDA"), choices=(), default=0, style=wx.OK|wx.CANCEL, callback=None):
		def makeDialog():
			dialog = wx.Dialog(gui.mainFrame, wx.ID_ANY, title)
			mainSizer = wx.BoxSizer(wx.VERTICAL)
			mainSizer.Add(wx.StaticText(dialogD_ANY, label=message))
			self.list = wx.ListView(dialog, wx.ID_ANY, style=wx.LC_LIST | wx.LC_SINGLE_SEL)
			self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda evt: dialog.EndModal(wx.ID_OK))
			for index, choice in enumerate(choices):
				self.list.InsertStringItem(index, choice)
			self.list.Focus(default)
			self.list.Select(default)
			mainSizer.Add(self.list)
			mainSizer.Add(dialog.CreateButtonSizer(style), flag=wx.BOTTOM)
			mainSizer.Fit(dialog)
			dialog.SetSizer(mainSizer)
			self.list.SetFocus()
			return dialog
		self.makeDialog = makeDialog
		super(SingleChoiceDialog, self).__init__(callback)

	def getResponse(self, response):
		if response == wx.ID_OK:
			sel = self.list.GetFirstSelected()
			if sel == -1:
				return None
			return sel, self.list.GetItemText(sel)
		else:
			return None

class LinksListDialog(ModalDialog):
	ID_MOVETO = 1000
	ID_ACTIVATE = wx.ID_OK

	def __init__(self, choices, default=0, callback=None):
		def makeDialog():
			dialog = wx.Dialog(gui.mainFrame, wx.ID_ANY, _("Links List"))
			mainSizer = wx.BoxSizer(wx.VERTICAL)
			self.list = wx.ListView(dialog, wx.ID_ANY, style=wx.LC_LIST | wx.LC_SINGLE_SEL)
			self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, lambda evt: dialog.EndModal(wx.ID_OK))
			for index, choice in enumerate(choices):
				self.list.InsertStringItem(index, choice)
			self.list.Focus(default)
			self.list.Select(default)
			mainSizer.Add(self.list)
			buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
			# Activate is our OK button, so need for an event.
			buttonSizer.Add(wx.Button(dialog, self.ID_ACTIVATE, _("&Activate Link")))
			movetoButton = wx.Button(dialog, self.ID_MOVETO, _("&Move to link"))
			movetoButton.Bind(wx.EVT_BUTTON, lambda evt: dialog.EndModal(self.ID_MOVETO))
			buttonSizer.Add(movetoButton)
			buttonSizer.Add(wx.Button(dialog, wx.ID_CANCEL))
			mainSizer.Add(buttonSizer)
			mainSizer.Fit(dialog)
			dialog.SetSizer(mainSizer)
			self.list.SetFocus()
			return dialog
		self.makeDialog = makeDialog
		super(LinksListDialog, self).__init__(callback)

	def getResponse(self, response):
		if response != wx.ID_CANCEL:
			sel = self.list.GetFirstSelected()
			if sel == -1:
				return None
			return response == self.ID_ACTIVATE, sel, self.list.GetItemText(sel)
		else:
			return None
