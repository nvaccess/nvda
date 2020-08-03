# -*- coding: UTF-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2017-2018 NV Access Limited, Thomas Stivers
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
import os

import gui
import ui
import wx
import wx.html2 as webview
from logHandler import log


class TestPanel(wx.Panel):
	def __init__(self, parent, url):
		wx.Panel.__init__(self, parent)

		sizer = wx.BoxSizer(wx.VERTICAL)
		self.wv: webview.WebView = webview.WebView.New(self)
		self.Bind(webview.EVT_WEBVIEW_NAVIGATING, self.OnWebViewNavigating, self.wv)
		self.Bind(webview.EVT_WEBVIEW_LOADED, self.OnWebViewLoaded, self.wv)
		self.wv.EnableHistory(False)
		self.wv.EnableContextMenu(False)

		sizer.Add(self.wv, flag=wx.EXPAND, proportion=1)
		self.SetSizer(sizer)

		self.wv.LoadURL(url)

	def ShutdownDemo(self):
		# put the frame title back
		pass

	# WebView events
	def OnWebViewNavigating(self, evt):
		pass

	def OnWebViewLoaded(self, evt):
		# The full document has loaded
		self.wv.SetFocus()
		self.wv.RunScript(
			r"document.getElementsByName('NVDASettings').focus()"
		)


class HelpWindow(wx.Dialog):
	def __init__(self, parent, url):
		super().__init__(
			parent,
			# Translators: Title for the context help dialog.
			title=_("NVDA Help"),
			size=(800, 600)
		)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		self.panel = TestPanel(self, url)
		mainSizer.Add(self.panel, flag=wx.EXPAND, proportion=1)
		self.SetSizer(mainSizer)


def showHelp(helpId: str, evt):
	"""Display the corresponding section of the user guide when either the Help
	button in an NVDA dialog is pressed or the F1 key is pressed on a
	recognized control.
	"""
	if not helpId:
		# Translators: Message indicating no context sensitive help is available.
		noHelpMessage = _("No context sensitive help is available here at this time.")
		ui.browseableMessage(noHelpMessage)

	helpFile = gui.getDocFilePath("userGuide.html")
	window = evt.GetEventObject()
	windowId = window.GetId()
	helpText = window.GetHelpText()
	label = window.GetLabel()
	log.debug(
		"Opening help:"
		f"helpId = {helpId}"
		f"\nwindowId = {windowId}"
		f"\nlabel = {label}"
	)

	# Translators: The title for an NVDA help window.
	helpTitle = _("NVDA Help")
	try:
		#os.startfile(f"file://{helpFile}#{helpId}")
		HelpWindow(gui.mainFrame, url=f"file://{helpFile}#{helpId}").Show()
	except KeyError as e:
		ui.browseableMessage(str(e), helpTitle, True)
