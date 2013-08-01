#gui/__init__.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import config

class ProfilesDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: The title of the Configuration Profiles dialog.
		super(ProfilesDialog, self).__init__(parent, title=_("Configuration Profiles"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the user profile option in the Configuration Profiles dialog.
		sizer.Add(wx.StaticText(self, label=_("&User profile:")))
		# Translators: Indicates that no configuration profile is selected.
		self.profiles = [_("(none)")]
		self.profiles.extend(config.conf.listProfiles())
		item = self.userProfile = wx.Choice(self, choices=self.profiles)
		if len(config.conf.profiles) == 1:
			item.Selection = 0
		else:
			item.Selection = self.profiles.index(config.conf.profiles[-1].name)
		sizer.Add(item)
		mainSizer.Add(sizer)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.userProfile.SetFocus()

	def onOk(self, evt):
		if self.userProfile.Selection == 0:
			config.conf.deactivateProfile()
		else:
			config.conf.activateProfile(self.profiles[self.userProfile.Selection])
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()
