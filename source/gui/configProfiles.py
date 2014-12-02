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
import globalVars

class ProfilesDialog(wx.Dialog):
	shouldSuspendConfigProfileTriggers = True

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

		self.currentAppName = (gui.mainFrame.prevFocus or api.getFocusObject()).appModule.appName
		self.profileNames = [None]
		self.profileNames.extend(config.conf.listProfiles())

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the profile list in the Configuration Profiles dialog.
		sizer.Add(wx.StaticText(self, label=_("&Profile")))
		item = self.profileList = wx.ListBox(self,
			choices=[self.getProfileDisplay(name, includeStates=True) for name in self.profileNames])
		item.Bind(wx.EVT_LISTBOX, self.onProfileListChoice)
		item.Selection = self.profileNames.index(config.conf.profiles[-1].name)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		item = self.changeStateButton = wx.Button(self)
		item.Bind(wx.EVT_BUTTON, self.onChangeState)
		sizer.Add(item)
		self.AffirmativeId = item.Id
		item.SetDefault()
		# Translators: The label of a button to create a new configuration profile.
		item = newButton = wx.Button(self, label=_("&New"))
		item.Bind(wx.EVT_BUTTON, self.onNew)
		sizer.Add(item)
		# Translators: The label of a button to rename a configuration profile.
		item = self.renameButton = wx.Button(self, label=_("&Rename"))
		item.Bind(wx.EVT_BUTTON, self.onRename)
		sizer.Add(item)
		# Translators: The label of a button to delete a configuration profile.
		item = self.deleteButton = wx.Button(self, label=_("&Delete"))
		item.Bind(wx.EVT_BUTTON, self.onDelete)
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a button to manage triggers
		# in the Configuration Profiles dialog.
		# See the Configuration Profiles section of the User Guide for details.
		triggersButton = wx.Button(self, label=_("&Triggers..."))
		triggersButton.Bind(wx.EVT_BUTTON, self.onTriggers)
		sizer.Add(triggersButton)
		# Translators: The label of a checkbox in the Configuration Profiles dialog.
		item = self.disableTriggersToggle = wx.CheckBox(self, label=_("Temporarily d&isable all triggers"))
		item.Value = not config.conf.profileTriggersEnabled
		sizer.Add(item)
		mainSizer.Add(sizer)

		# Translators: The label of a button to close a dialog.
		item = wx.Button(self, wx.ID_CLOSE, label=_("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		if globalVars.appArgs.secure:
			for item in newButton, triggersButton, self.renameButton, self.deleteButton:
				item.Disable()
		self.onProfileListChoice(None)

		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.profileList.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def __del__(self):
		ProfilesDialog._instance = None

	def getProfileDisplay(self, name, includeStates=False):
		# Translators: The item to select the user's normal configuration
		# in the profile list in the Configuration Profiles dialog.
		disp = name if name else _("(normal configuration)")
		if includeStates:
			disp += self.getProfileStates(name)
		return disp

	def getProfileStates(self, name):
		try:
			profile = config.conf.getProfile(name)
		except KeyError:
			return ""
		states = []
		editProfile = config.conf.profiles[-1]
		if profile is editProfile:
			# Translators: Reported for a profile which is being edited
			# in the Configuration Profiles dialog.
			states.append(_("editing"))
		if name:
			# This is a profile (not the normal configuration).
			if profile.manual:
				# Translators: Reported for a profile which has been manually activated
				# in the Configuration Profiles dialog.
				states.append(_("manual"))
			if profile.triggered:
				# Translators: Reported for a profile which is currently triggered
				# in the Configuration Profiles dialog.
				states.append(_("triggered"))
		if states:
			return " (%s)" % ", ".join(states)
		return ""

	def isProfileManual(self, name):
		if not name:
			return False
		try:
			profile = config.conf.getProfile(name)
		except KeyError:
			return False
		return profile.manual

	def onChangeState(self, evt):
		sel = self.profileList.Selection
		profile = self.profileNames[sel]
		if self.isProfileManual(profile):
			profile = None
		try:
			config.conf.manualActivateProfile(profile)
		except:
			# Translators: An error displayed when activating a configuration profile fails.
			gui.messageBox(_("Error activating profile."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		self.Close()

	def onNew(self, evt):
		self.Disable()
		NewProfileDialog(self).Show()

	def onDelete(self, evt):
		index = self.profileList.Selection
		if gui.messageBox(
			# Translators: The confirmation prompt displayed when the user requests to delete a configuration profile.
			_("Are you sure you want to delete this profile? This cannot be undone."),
			# Translators: The title of the confirmation dialog for deletion of a configuration profile.
			_("Confirm Deletion"),
			wx.YES | wx.NO | wx.ICON_QUESTION, self
		) == wx.NO:
			return
		name = self.profileNames[index]
		try:
			config.conf.deleteProfile(name)
		except:
			log.debugWarning("", exc_info=True)
			# Translators: An error displayed when deleting a configuration profile fails.
			gui.messageBox(_("Error deleting profile."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		del self.profileNames[index]
		self.profileList.Delete(index)
		self.profileList.SetString(0, self.getProfileDisplay(None, includeStates=True))
		self.profileList.Selection = 0
		self.onProfileListChoice(None)
		self.profileList.SetFocus()

	def onProfileListChoice(self, evt):
		sel = self.profileList.Selection
		enable = sel > 0
		name = self.profileNames[sel]
		if self.isProfileManual(name):
			# Translators: The label of the button to manually deactivate the selected profile
			# in the Configuration Profiles dialog.
			label = _("Manual deactivate")
		else:
			# Translators: The label of the button to manually activate the selected profile
			# in the Configuration Profiles dialog.
			label = _("Manual activate")
		self.changeStateButton.Label = label
		self.changeStateButton.Enabled = enable
		if globalVars.appArgs.secure:
			return
		self.deleteButton.Enabled = enable
		self.renameButton.Enabled = enable

	def onRename(self, evt):
		index = self.profileList.Selection
		oldName = self.profileNames[index]
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
			# Translators: An error displayed when renaming a configuration profile
			# and a profile with the new name already exists.
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		except:
			log.debugWarning("", exc_info=True)
			gui.messageBox(_("Error renaming profile."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		self.profileNames[index] = newName
		self.profileList.SetString(index, self.getProfileDisplay(newName, includeStates=True))
		self.profileList.Selection = index
		self.profileList.SetFocus()

	def onTriggers(self, evt):
		self.Disable()
		TriggersDialog(self).Show()

	def getSimpleTriggers(self):
		# Yields (spec, display, manualEdit)
		yield ("app:%s" % self.currentAppName,
			# Translators: Displayed for the configuration profile trigger for the current application.
			# %s is replaced by the application executable name.
			_("Current application (%s)") % self.currentAppName,
			False)
		# Translators: Displayed for the configuration profile trigger for say all.
		yield "sayAll", _("Say all"), True

	def onClose(self, evt):
		if self.disableTriggersToggle.Value:
			config.conf.disableProfileTriggers()
		else:
			config.conf.enableProfileTriggers()
		self.Destroy()

	def saveTriggers(self, parentWindow=None):
		try:
			config.conf.saveProfileTriggers()
		except:
			log.debugWarning("", exc_info=True)
			# Translators: An error displayed when saving configuration profile triggers fails.
			gui.messageBox(_("Error saving configuration profile triggers - probably read only file system."),
				_("Error"), wx.OK | wx.ICON_ERROR, parent=parentWindow)

class TriggerInfo(object):
	__slots__ = ("spec", "display", "profile")

	def __init__(self, spec, display, profile):
		self.spec = spec
		self.display = display
		self.profile = profile

class TriggersDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: The title of the configuration profile triggers dialog.
		super(TriggersDialog, self).__init__(parent, title=_("Profile Triggers"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		processed = set()
		triggers = self.triggers = []
		confTrigs = config.conf.triggersToProfiles
		# Handle simple triggers.
		for spec, disp, manualEdit in parent.getSimpleTriggers():
			try:
				profile = confTrigs[spec]
			except KeyError:
				profile = None
			triggers.append(TriggerInfo(spec, disp, profile))
			processed.add(spec)
		# Handle all other triggers.
		for spec, profile in confTrigs.iteritems():
			if spec in processed:
				continue
			if spec.startswith("app:"):
				# Translators: Displayed for a configuration profile trigger for an application.
				# %s is replaced by the application executable name.
				disp = _("%s application") % spec[4:]
			else:
				continue
			triggers.append(TriggerInfo(spec, disp, profile))

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the triggers list in the Configuration Profile Triggers dialog.
		sizer.Add(wx.StaticText(self, label=_("Triggers")))
		item = self.triggerList = wx.ListBox(self, choices=[trig.display for trig in triggers])
		item.Bind(wx.EVT_LISTBOX, self.onTriggerListChoice)
		item.Selection = 0
		sizer.Add(item)
		mainSizer.Add(sizer)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of the profile list in the Configuration Profile Triggers dialog.
		sizer.Add(wx.StaticText(self, label=_("Profile")))
		item = self.profileList = wx.Choice(self,
			choices=[parent.getProfileDisplay(name) for name in parent.profileNames])
		item.Bind(wx.EVT_CHOICE, self.onProfileListChoice)
		sizer.Add(item)
		mainSizer.Add(sizer)

		item = wx.Button(self, wx.ID_CLOSE, label=_("&Close"))
		item.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(item)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.AffirmativeId = wx.ID_CLOSE
		item.SetDefault()
		self.EscapeId = wx.ID_CLOSE

		self.onTriggerListChoice(None)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onTriggerListChoice(self, evt):
		trig = self.triggers[self.triggerList.Selection]
		try:
			self.profileList.Selection = self.Parent.profileNames.index(trig.profile)
		except ValueError:
			log.error("Trigger %s: invalid profile %s"
				% (trig.spec, trig.profile))
			self.profileList.Selection = 0
			trig.profile = None

	def onProfileListChoice(self, evt):
		trig = self.triggers[self.triggerList.Selection]
		trig.profile = self.Parent.profileNames[evt.Selection]

	def onClose(self, evt):
		confTrigs = config.conf.triggersToProfiles
		for trig in self.triggers:
			if trig.profile:
				confTrigs[trig.spec] = trig.profile
			else:
				try:
					del confTrigs[trig.spec]
				except KeyError:
					pass
		self.Parent.saveTriggers(parentWindow=self)

		self.Parent.Enable()
		self.Destroy()

class NewProfileDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: The title of the dialog to create a new configuration profile.
		super(NewProfileDialog, self).__init__(parent, title=_("New Profile"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the name of a new configuration profile.
		sizer.Add(wx.StaticText(self, label=_("Profile name:")))
		item = self.profileName = wx.TextCtrl(self)
		sizer.Add(item)
		mainSizer.Add(sizer)

		# Translators: The label of a radio button to specify that a profile will be used for manual activation
		# in the new configuration profile dialog.
		self.triggers = triggers = [(None, _("Manual activation"), True)]
		triggers.extend(parent.getSimpleTriggers())
		item = self.triggerChoice = wx.RadioBox(self, label=_("Use this profile for:"),
			choices=[trig[1] for trig in triggers])
		item.Bind(wx.EVT_RADIOBOX, self.onTriggerChoice)
		self.autoProfileName = ""
		self.onTriggerChoice(None)
		mainSizer.Add(item)

		mainSizer.Add(self.CreateButtonSizer(wx.OK | wx.CANCEL))
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.profileName.SetFocus()
		self.Center(wx.BOTH | wx.CENTER_ON_SCREEN)

	def onOk(self, evt):
		confTrigs = config.conf.triggersToProfiles
		spec, disp, manualEdit = self.triggers[self.triggerChoice.Selection]
		if spec in confTrigs and gui.messageBox(
			# Translators: The confirmation prompt presented when creating a new configuration profile
			# and the selected trigger is already associated.
			_("This trigger is already associated with another profile. "
				"If you continue, it will be removed from that profile and associated with this one.\n"
				"Are you sure you want to continue?"),
			_("Warning"), wx.ICON_WARNING | wx.YES | wx.NO, self
		) == wx.NO:
			return

		name = api.filterFileName(self.profileName.Value)
		if not name:
			return
		try:
			config.conf.createProfile(name)
		except ValueError:
			# Translators: An error displayed when the user attempts to create a configuration profile which already exists.
			gui.messageBox(_("That profile already exists. Please choose a different name."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			return
		except:
			log.debugWarning("", exc_info=True)
			# Translators: An error displayed when creating a configuration profile fails.
			gui.messageBox(_("Error creating profile - probably read only file system."),
				_("Error"), wx.OK | wx.ICON_ERROR, self)
			self.onCancel(evt)
			return
		if spec:
			confTrigs[spec] = name
			self.Parent.saveTriggers(parentWindow=self)

		parent = self.Parent
		if manualEdit:
			if gui.messageBox(
				# Translators: The prompt asking the user whether they wish to
				# manually activate a configuration profile that has just been created.
				_("To edit this profile, you will need to manually activate it. "
					"Once you have finished editing, you will need to manually deactivate it to resume normal usage.\n"
					"Do you wish to manually activate it now?"),
				# Translators: The title of the confirmation dialog for manual activation of a created profile.
				_("Manual Activation"), wx.YES | wx.NO | wx.ICON_QUESTION, self
			) == wx.YES:
				config.conf.manualActivateProfile(name)
			else:
				# Return to the Profiles dialog.
				parent.profileNames.append(name)
				parent.profileList.Append(name)
				parent.profileList.Selection = parent.profileList.Count - 1
				parent.onProfileListChoice(None)
				parent.profileList.SetFocus()
				parent.Enable()
				self.Destroy()
				return
		else:
			# Ensure triggers are enabled so the user can edit the profile.
			config.conf.enableProfileTriggers()

		# The user is done with the Profiles dialog;
		# let them get on with editing the profile.
		parent.Destroy()

	def onCancel(self, evt):
		self.Parent.Enable()
		self.Destroy()

	def onTriggerChoice(self, evt):
		spec, disp, manualEdit = self.triggers[self.triggerChoice.Selection]
		if not spec:
			# Manual activation shouldn't guess a name.
			name = ""
		elif spec.startswith("app:"):
			name = spec[4:]
		else:
			name = disp
		if self.profileName.Value == self.autoProfileName:
			# The user hasn't changed the automatically filled value.
			self.profileName.Value = name
			self.profileName.SelectAll()
		self.autoProfileName = name
