#gui/configProfiles.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2013 NV Access Limited
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import wx
import config
import api
import gui
from logHandler import log

class ProfilesDialog(wx.Dialog):

	_instance = None
	def __new__(cls, *args, **kwargs):
		# Make this a singleton.
		if ProfilesDialog._instance is None:
			return super(ProfilesDialog, cls).__new__(cls, *args, **kwargs)
		return ProfilesDialog._instance

	def __init__(self, parent):
		if ProfilesDialog._instance is not None:
			return
		ProfilesDialog._instance = self
		# Translators: The title of the Configuration Profiles dialog.
		super(ProfilesDialog, self).__init__(parent, title=_("Configuration Profiles"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the profile list in the Configuration Profiles dialog.
		sizer.Add(wx.StaticText(self, label=_("&Profile")))
		# Translators: Indicates that no configuration profile is selected.
		# In this case, the user's normal configuration will be used.
		self.profiles = [_("(none)")]
		self.profiles.extend(config.conf.listProfiles())
		item = self.profileList = wx.Choice(self, choices=self.profiles)
		item.Bind(wx.EVT_CHOICE, self.onProfileListChoice)
		if len(config.conf.profiles) == 1:
			item.Selection = 0
		else:
			item.Selection = self.profiles.index(config.conf.profiles[-1].name)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to activate the selected profile.
		item = wx.Button(self, label=_("&Activate"))
		item.Bind(wx.EVT_BUTTON, self.onActivate)
		sizer.Add(item)
		self.AffirmativeId = item.Id
		item.SetDefault()
		# Translators: The label of a button to create a new configuration profile.
		item = wx.Button(self, label=_("&New"))
		item.Bind(wx.EVT_BUTTON, self.onNew)
		sizer.Add(item)
		# Translators: The label of a button to rename a configuration profile.
		item = self.renameButton = wx.Button(self, label=_("&Rename"))
		if self.profileList.Selection == 0:
			item.Disable()
		item.Bind(wx.EVT_BUTTON, self.onRename)
		sizer.Add(item)
		# Translators: The label of a button to delete a configuration profile.
		item = self.deleteButton = wx.Button(self, label=_("&Delete"))
		if self.profileList.Selection == 0:
			item.Disable()
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		# Translators: The label of a button to close a dialog.
		item = wx.Button(self, wx.ID_CLOSE, label=_("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, lambda evt: self.Destroy())
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.profileList.SetFocus()

	def __del__(self):
		ProfilesDialog._instance = None

	def onActivate(self, evt):
		try:
			config.conf.deactivateProfile()
		except IndexError:
			pass
		if self.profileList.Selection != 0:
			try:
				config.conf.activateProfile(self.profiles[self.profileList.Selection])
			except:
				# Translators: An error displayed when activating a profile fails.
				gui.messageBox(_("Error activating profile."),
					_("Error"), wx.OK | wx.ICON_ERROR)
				return
		self.Destroy()

	def onNew(self, evt):
		# Translators: The label of a field to enter the name of a new configuration profile.
		with wx.TextEntryDialog(self, _("Profile name:"),
				# Translators: The title of the dialog to create a new configuration profile.
				_("New Profile")) as d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			name = api.filterFileName(d.Value)
		try:
			config.conf.createProfile(name)
		except ValueError:
			# Translators: An error displayed when the user attempts to create a profile which already exists.
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		except:
			log.debugWarning("", exc_info=True)
			# Translators: An error displayed when creating a profile fails.
			gui.messageBox(_("Error creating profile - probably read only file system."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		self.profiles.append(name)
		self.profileList.Append(name)
		self.profileList.Selection = len(self.profiles) - 1
		self.profileList.SetFocus()

	def onDelete(self, evt):
		index = self.profileList.Selection
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
		except:
			log.debugWarning("", exc_info=True)
			gui.messageBox(_("Error deleting profile."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		del self.profiles[index]
		self.profileList.Delete(index)
		self.profileList.Selection = 0
		self.profileList.SetFocus()

	def onProfileListChoice(self, evt):
		enable = evt.Selection > 0
		self.deleteButton.Enabled = enable
		self.renameButton.Enabled = enable

	def onRename(self, evt):
		index = self.profileList.Selection
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
		except:
			log.debugWarning("", exc_info=True)
			gui.messageBox(_("Error renaming profile."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		self.profiles[index] = newName
		self.profileList.SetString(index, newName)
		self.profileList.Selection = index
		self.profileList.SetFocus()
