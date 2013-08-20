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
import appModuleHandler

class ProfilesDialog(wx.Dialog):

	_instance = None
	def __new__(cls, *args, **kwargs):
		# Make this a singleton.
		if ProfilesDialog._instance is None:
			return super(ProfilesDialog, cls).__new__(cls, *args, **kwargs)
		return ProfilesDialog._instance

	def __init__(self, parent, useFocus=False):
		self.focusWhenActivated = api.getFocusObject() if useFocus else None
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
		profiles = [_("(none)")]
		profiles.extend(config.conf.listProfiles())
		item = self.profileList = wx.Choice(self, choices=profiles)
		item.Bind(wx.EVT_CHOICE, self.onProfileListChoice)
		profile = config.conf.getManualProfile()
		if profile:
			item.StringSelection = profile
		else:
			item.Selection = 0
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
		# Translators: The label of a button to configure triggers for a configuration profile.
		item = self.triggersButton = wx.Button(self, label=_("&Triggers..."))
		item.Bind(wx.EVT_BUTTON, self.onTriggers)
		sizer.Add(item)
		# Translators: The label of a button to rename a configuration profile.
		item = self.renameButton = wx.Button(self, label=_("&Rename"))
		item.Bind(wx.EVT_BUTTON, self.onRename)
		sizer.Add(item)
		# Translators: The label of a button to delete a configuration profile.
		item = self.deleteButton = wx.Button(self, label=_("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		self.onProfileListChoice(None)
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
		sel = self.profileList.Selection
		if sel == 0:
			profile = None
		else:
			profile = self.profileList.GetString(sel)
		try:
			config.conf.manualActivateProfile(profile)
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
		self.profileList.Append(name)
		self.profileList.Selection = self.profileList.Count - 1
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
		name = self.profileList.StringSelection
		try:
			config.conf.deleteProfile(name)
		except:
			log.debugWarning("", exc_info=True)
			gui.messageBox(_("Error deleting profile."),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return
		self.profileList.Delete(index)
		self.profileList.Selection = 0
		self.profileList.SetFocus()

	def onProfileListChoice(self, evt):
		enable = self.profileList.Selection > 0
		self.deleteButton.Enabled = enable
		self.renameButton.Enabled = enable
		self.triggersButton.Enabled = enable

	def onRename(self, evt):
		index = self.profileList.Selection
		oldName = self.profileList.GetString(index)
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
		self.profileList.SetString(index, newName)
		self.profileList.Selection = index
		self.profileList.SetFocus()

	def onTriggers(self, evt):
		self.Disable()
		TriggersDialog(self, self.profileList.StringSelection).Show()

class TriggersDialog(wx.Dialog):

	def __init__(self, parent, profile):
		super(TriggersDialog, self).__init__(parent,
			# Translators: The title of the configuration profile triggers dialog.
			# %s will be replaced with the name of the profile.
			title=_("Triggers for Profile %s") % profile)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The caption of the configuration profile triggers dialog.
		mainSizer.Add(wx.StaticText(self, label=_("What should automatically trigger this profile?")))

		self.profile = profile
		triggers = self.triggers = set()
		for trigger, matchProfile in config.conf["profileTriggers"].iteritems():
			if matchProfile == profile:
				triggers.add(trigger)

		# Translators: The label of a group of controls related to applications in the configuration profile triggers dialog.
		group = wx.StaticBoxSizer(wx.StaticBox(self, label=_("&Applications")), wx.HORIZONTAL)
		item = self.appsList = wx.ListBox(self, choices=[trigger[4:] for trigger in triggers if trigger.startswith("app:")])
		item.Selection = 0
		item.Bind(wx.EVT_CHOICE, self.onAppsListChoice)
		group.Add(item)
		sizer = wx.BoxSizer(wx.VERTICAL)
		# Translators: The label of a button to add an application trigger for a configuration profile.
		item = wx.Button(self, label=_("Add"))
		item.Bind(wx.EVT_BUTTON, self.onAddApp)
		sizer.Add(item)
		# Translators: The label of a button to remove an application trigger for a configuration profile.
		item = self.removeAppButton = wx.Button(self, label=_("Remove"))
		item.Bind(wx.EVT_BUTTON, self.onRemoveApp)
		sizer.Add(item)
		group.Add(sizer)
		mainSizer.Add(group)
		self.onAppsListChoice(None)

		# Translators: The label of a check box to specify say all as a trigger for a configuration profile.
		item = self.sayAllToggle = wx.CheckBox(self, label=_("&Say all"))
		if "sayAll" in triggers:
			item.Value = True
		elif "sayAll" in config.conf["profileTriggers"]:
			# This trigger is associated with another profile already.
			item.Disable()
		mainSizer.Add(item)

		item = wx.Button(self, wx.ID_CLOSE, label=_("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Fit(self)
		self.Sizer = mainSizer

	def onClose(self, evt):
		triggers = config.conf["profileTriggers"]
		if self.sayAllToggle.Value:
			triggers["sayAll"] = self.profile
		elif self.sayAllToggle.Enabled:
			try:
				del triggers["sayAll"]
			except KeyError:
				pass

		self.Parent.Enable()
		self.Destroy()

	def onAddApp(self, evt):
		# Translators: The title of a dialog to add an application which triggers a configuration profile.
		d = wx.Dialog(self, title=_("Add Application"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the name of an application to trigger a configuration profile.
		sizer.Add(wx.StaticText(d, label=_("Application executable name (no extension):")))
		# Let the user choose from running app modules.
		item = self.addAppCombo = wx.ComboBox(d, style=wx.CB_DROPDOWN | wx.CB_SORT,
			choices=[mod.appName for mod in appModuleHandler.runningTable.itervalues()])
		if self.Parent.focusWhenActivated:
			item.Value = self.Parent.focusWhenActivated.appModule.appName
		sizer.Add(item)
		mainSizer.Add(sizer)

		mainSizer.Add(d.CreateButtonSizer(wx.OK | wx.CANCEL))

		mainSizer.Fit(d)
		d.Sizer = mainSizer
		self.addAppCombo.SetFocus()

		with d:
			if d.ShowModal() == wx.ID_CANCEL:
				return
			app = self.addAppCombo.Value

		if not app:
			return
		trigger = "app:%s" % app
		if trigger in config.conf["profileTriggers"]:
			# Translators: An error displayed when the user tries to add an application to trigger a configuration profile
			# but that application is already associated with another profile.
			gui.messageBox(_("That application is already associated with another profile"),
				_("Error"), wx.OK | wx.ICON_ERROR)
			return

		config.conf["profileTriggers"][trigger] = self.profile
		self.triggers.add(trigger)
		self.appsList.Append(app)
		self.appsList.Selection = self.appsList.Count - 1
		self.onAppsListChoice(None)
		self.appsList.SetFocus()

	def onRemoveApp(self, evt):
		index = self.appsList.Selection
		app = self.appsList.GetString(index)
		del config.conf["profileTriggers"]["app:%s" % app]
		self.appsList.Delete(index)
		self.appsList.SetFocus()
		self.appsList.Selection = min(index, self.appsList.Count - 1)
		self.onAppsListChoice(None)

	def onAppsListChoice(self, evt):
		self.removeAppButton.Enabled = self.appsList.Selection >= 0
