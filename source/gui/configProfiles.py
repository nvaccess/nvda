#gui/configProfiles.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import config
import api
import gui

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

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to create a new configuration profile.
		item = wx.Button(self, label=_("&New"))
		item.Bind(wx.EVT_BUTTON, self.onNew)
		sizer.Add(item)
		# Translators: The label of a button to delete a configuration profile.
		item = wx.Button(self, label=_("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.userProfile.SetFocus()

	def onOk(self, evt):
		try:
			config.conf.deactivateProfile()
		except IndexError:
			pass
		if self.userProfile.Selection != 0:
			config.conf.activateProfile(self.profiles[self.userProfile.Selection])
		self.Destroy()

	def onCancel(self, evt):
		self.Destroy()

	def onNew(self, evt):
		# Translators: The label of a field to enter the name of a new configuration profile.
		with wx.TextEntryDialog(self, _("Profile name:"),
				# Translators: The title of the dialog to create a new configuration profile.
				_("New Profile")) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			name = api.filterFileName(d.Value)
		if name in self.profiles:
			# Translators: An error displayed when the user attempts to create a profile which already exists.
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		self.profiles.append(name)
		self.userProfile.Append(name)
		self.userProfile.Selection = len(self.profiles) - 1
		self.userProfile.SetFocus()

	def onDelete(self, evt):
		index = self.userProfile.Selection
		if index == 0:
			return
		if gui.messageBox(
			# Translators: The confirmation prompt displayed when the user requests to delete a configuration profile.
			_("Are you sure you want to delete this profile? This cannot be undone."),
			# Translators: The title of the confirmation dialog for deletion of a configuration profile.
			_("Confirm Deletion"),
			wx.YES | wx.NO | wx.ICON_QUESTION
		) == wx.NO:
			return
		name = self.profiles[index]
		config.conf.deleteProfile(name)
		del self.profiles[index]
		self.userProfile.Delete(index)
		self.userProfile.Selection = 0
