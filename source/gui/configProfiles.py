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
		# In this case, the user's normal configuration will be used.
		self.profiles = [_("(none)")]
		self.profiles.extend(config.conf.listProfiles())
		item = self.userProfile = wx.Choice(self, choices=self.profiles)
		item.Bind(wx.EVT_CHOICE, self.onUserProfileChoice)
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
		# Translators: The label of a button to rename a configuration profile.
		item = self.renameButton = wx.Button(self, label=_("&Rename"))
		if self.userProfile.Selection == 0:
			item.Disable()
		item.Bind(wx.EVT_BUTTON, self.onRename)
		sizer.Add(item)
		# Translators: The label of a button to delete a configuration profile.
		item = self.deleteButton = wx.Button(self, label=_("&Delete"))
		if self.userProfile.Selection == 0:
			item.Disable()
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
		if gui.messageBox(
			# Translators: The confirmation prompt displayed when the user requests to delete a configuration profile.
			_("Are you sure you want to delete this profile? This cannot be undone."),
			# Translators: The title of the confirmation dialog for deletion of a configuration profile.
			_("Confirm Deletion"),
			wx.YES | wx.NO | wx.ICON_QUESTION
		) == wx.NO:
			return
		name = self.profiles[index]
		try:
			config.conf.deleteProfile(name)
		except LookupError:
			# The profile hasn't been created yet.
			pass
		del self.profiles[index]
		self.userProfile.Delete(index)
		self.userProfile.Selection = 0
		self.userProfile.SetFocus()

	def onUserProfileChoice(self, evt):
		enable = evt.Selection > 0
		self.deleteButton.Enabled = enable
		self.renameButton.Enabled = enable

	def onRename(self, evt):
		index = self.userProfile.Selection
		oldName = self.profiles[index]
		# Translators: The label of a field to enter a new name for a configuration profile.
		with wx.TextEntryDialog(self, _("New name:"),
				# Translators: The title of the dialog to rename a configuration profile.
				_("Rename Profile"), defaultValue=oldName) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			newName = api.filterFileName(d.Value)
		try:
			config.conf.renameProfile(oldName, newName)
		except ValueError:
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		self.profiles[index] = newName
		self.userProfile.SetString(index, newName)
		self.userProfile.Selection = index
		self.userProfile.SetFocus()
