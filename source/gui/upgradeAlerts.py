#upgradeAlerts.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

"""Dialogs displayed when NVDA starts containing important information about changes to NVDA.
"""

import os
import wx
import gui
import config

class NewLaptopKeyboardLayout(wx.Dialog):
	MESSAGE = _(
		# Translators: Information about NVDA's new laptop keyboard layout.
		"In NVDA 2013.1, the laptop keyboard layout has been completely redesigned in order to make it more intuitive and consistent.\n"
		"If you use the laptop layout, please see the What's New document for more information."
	)

	def __init__(self, parent):
		# Translators: The title of a dialog providing information about NVDA's new laptop keyboard layout.
		super(NewLaptopKeyboardLayout, self).__init__(parent, title=_("New Laptop Keyboard layout"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		item = wx.StaticText(self, label=self.MESSAGE)
		mainSizer.Add(item, border=20, flag=wx.LEFT | wx.RIGHT | wx.TOP)
		# Translators: The label of a button in the New Laptop Keyboard Layout dialog
		# to open the What's New document.
		whatsNewButton = wx.Button(self, label=_("Read What's New"))
		whatsNewButton.Bind(wx.EVT_BUTTON, self.onWhatsNew)
		mainSizer.Add(whatsNewButton)

		mainSizer.Add(self.CreateButtonSizer(wx.OK),flag=wx.TOP|wx.BOTTOM|wx.ALIGN_CENTER_HORIZONTAL,border=20)
		self.Bind(wx.EVT_BUTTON, lambda evt: self.Close(), id=wx.ID_OK)

		self.Bind(wx.EVT_CLOSE, self.onClose)

		whatsNewButton.SetFocus()
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onClose(self, evt):
		config.conf["upgrade"]["newLaptopKeyboardLayout"] = True
		try:
			config.conf.save()
		except:
			pass
		self.EndModal(0)

	def onWhatsNew(self, evt):
		os.startfile(gui.getDocFilePath("changes.html"))
		self.Close()

	@classmethod
	def run(cls):
		"""Prepare and display an instance of this dialog.
		This does not require the dialog to be instantiated.
		"""
		gui.mainFrame.prePopup()
		d = cls(gui.mainFrame)
		d.ShowModal()
		d.Destroy()
		gui.mainFrame.postPopup()
