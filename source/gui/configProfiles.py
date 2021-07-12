# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2013-2018 NV Access Limited, Joseph Lee, Julien Cochuyt, Thomas Stivers
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import wx
import config
import api
import gui
from logHandler import log
import appModuleHandler
import globalVars
from . import guiHelper
import gui.contextHelp


class ProfilesDialog(
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog   # wxPython does not seem to call base class initializer, put last in MRO
):
	shouldSuspendConfigProfileTriggers = True
	helpId = "ConfigurationProfiles"

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
		super().__init__(parent, title=_("Configuration Profiles"))

		self.currentAppName = (gui.mainFrame.prevFocus or api.getFocusObject()).appModule.appName
		self.profileNames = [None]
		self.profileNames.extend(config.conf.listProfiles())

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self,orientation=wx.VERTICAL)
		profilesListGroupSizer = wx.StaticBoxSizer(wx.HORIZONTAL, self)
		profilesListBox = profilesListGroupSizer.GetStaticBox()
		profilesListGroupContents = wx.BoxSizer(wx.HORIZONTAL)

		#contains the profile list and activation button in vertical arrangement.
		changeProfilesSizer = wx.BoxSizer(wx.VERTICAL)
		item = self.profileList = wx.ListBox(
			profilesListBox,
			choices=[self.getProfileDisplay(name, includeStates=True) for name in self.profileNames]
		)
		self.bindHelpEvent("ProfilesBasicManagement", self.profileList)
		item.Bind(wx.EVT_LISTBOX, self.onProfileListChoice)
		item.Selection = self.profileNames.index(config.conf.profiles[-1].name)
		changeProfilesSizer.Add(item, proportion=1.0)

		changeProfilesSizer.AddSpacer(guiHelper.SPACE_BETWEEN_BUTTONS_VERTICAL)

		self.changeStateButton = wx.Button(profilesListBox)
		self.bindHelpEvent("ConfigProfileManual", self.changeStateButton)
		self.changeStateButton.Bind(wx.EVT_BUTTON, self.onChangeState)
		self.AffirmativeId = self.changeStateButton.Id
		self.changeStateButton.SetDefault()
		changeProfilesSizer.Add(self.changeStateButton)
		
		profilesListGroupContents.Add(changeProfilesSizer, flag = wx.EXPAND)
		profilesListGroupContents.AddSpacer(guiHelper.SPACE_BETWEEN_ASSOCIATED_CONTROL_HORIZONTAL)

		buttonHelper = guiHelper.ButtonHelper(wx.VERTICAL)
		# Translators: The label of a button to create a new configuration profile.
		newButton = buttonHelper.addButton(profilesListBox, label=_("&New"))
		self.bindHelpEvent("ProfilesCreating", newButton)
		newButton.Bind(wx.EVT_BUTTON, self.onNew)

		# Translators: The label of a button to rename a configuration profile.
		self.renameButton = buttonHelper.addButton(profilesListBox, label=_("&Rename"))
		self.bindHelpEvent("ProfilesBasicManagement", self.renameButton)
		self.renameButton.Bind(wx.EVT_BUTTON, self.onRename)

		# Translators: The label of a button to delete a configuration profile.
		self.deleteButton = buttonHelper.addButton(profilesListBox, label=_("&Delete"))
		self.bindHelpEvent("ProfilesBasicManagement", self.deleteButton)
		self.deleteButton.Bind(wx.EVT_BUTTON, self.onDelete)

		profilesListGroupContents.Add(buttonHelper.sizer)
		profilesListGroupSizer.Add(profilesListGroupContents, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		sHelper.addItem(profilesListGroupSizer)

		# Translators: The label of a button to manage triggers
		# in the Configuration Profiles dialog.
		# See the Configuration Profiles section of the User Guide for details.
		triggersButton = wx.Button(self, label=_("&Triggers..."))
		self.bindHelpEvent("ConfigProfileTriggers", triggersButton)
		triggersButton.Bind(wx.EVT_BUTTON, self.onTriggers)

		# Translators: The label of a checkbox in the Configuration Profiles dialog.
		self.disableTriggersToggle = wx.CheckBox(self, label=_("Temporarily d&isable all triggers"))
		self.bindHelpEvent("ConfigProfileDisablingTriggers", self.disableTriggersToggle)
		self.disableTriggersToggle.Value = not config.conf.profileTriggersEnabled
		sHelper.addItem(guiHelper.associateElements(triggersButton,self.disableTriggersToggle))

		sHelper.addDialogDismissButtons(wx.CLOSE, separated=True)
		# Not binding wx.EVT_CLOSE here because of https://github.com/wxWidgets/Phoenix/issues/672
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)
		self.EscapeId = wx.ID_CLOSE

		if globalVars.appArgs.secure:
			for item in newButton, triggersButton, self.renameButton, self.deleteButton:
				item.Disable()
		self.onProfileListChoice(None)

		mainSizer.Add(sHelper.sizer, flag=wx.ALL, border=guiHelper.BORDER_FOR_DIALOGS)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.profileList.SetFocus()
		self.CentreOnScreen()

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
			_("This profile will be permanently deleted. This action cannot be undone."),
			# Translators: The title of the confirmation dialog for deletion of a configuration profile.
			_("Confirm Deletion"),
			wx.OK | wx.CANCEL | wx.ICON_QUESTION, self
		) != wx.OK:
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
		while True:
			with RenameProfileDialog(
				self,
				# Translators: The label of a field to enter a new name for a configuration profile.
				_("New name:"),
				# Translators: The title of the dialog to rename a configuration profile.
				caption=_("Rename Profile"),
				value=oldName
			) as d:
				if d.ShowModal() == wx.ID_CANCEL:
					return
			newName = d.Value
			if newName:
				break
			gui.messageBox(
				# Translators: An error displayed when the user attempts to rename a configuration profile
				# with an empty name.
				_("A profile cannot have an empty name."),
				# Translators: The title of an error message dialog.
				caption=_("Error"),
				style=wx.ICON_ERROR,
				parent=self
			)
		newName = api.filterFileName(newName)
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
		# 7077: Nullify the instance flag, otherwise wxWidgets will think the dialog is active when it is gone.
		ProfilesDialog._instance = None

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


class TriggersDialog(
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "ConfigProfileTriggers"

	def __init__(self, parent):
		# Translators: The title of the configuration profile triggers dialog.
		super().__init__(parent, title=_("Profile Triggers"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

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
		for spec, profile in confTrigs.items():
			if spec in processed:
				continue
			if spec.startswith("app:"):
				# Translators: Displayed for a configuration profile trigger for an application.
				# %s is replaced by the application executable name.
				disp = _("%s application") % spec[4:]
			else:
				continue
			triggers.append(TriggerInfo(spec, disp, profile))

		# Translators: The label of the triggers list in the Configuration Profile Triggers dialog.
		triggersText = _("Triggers")
		triggerChoices = [trig.display for trig in triggers]
		self.triggerList = sHelper.addLabeledControl(triggersText, wx.ListBox, choices=triggerChoices)
		self.triggerList.Bind(wx.EVT_LISTBOX, self.onTriggerListChoice)
		self.triggerList.Selection = 0

		# Translators: The label of the profile list in the Configuration Profile Triggers dialog.
		profileText = _("Profile")
		profileChoices = [parent.getProfileDisplay(name) for name in parent.profileNames]
		self.profileList = sHelper.addLabeledControl(profileText, wx.Choice, choices=profileChoices)
		self.profileList.Bind(wx.EVT_CHOICE, self.onProfileListChoice)

		sHelper.addDialogDismissButtons(wx.CLOSE, separated=True)
		# Not binding wx.EVT_CLOSE here because of https://github.com/wxWidgets/Phoenix/issues/672
		self.Bind(wx.EVT_BUTTON, self.onClose, id=wx.ID_CLOSE)
		self.AffirmativeId = wx.ID_CLOSE
		self.EscapeId = wx.ID_CLOSE

		self.onTriggerListChoice(None)

		mainSizer.Add(sHelper.sizer, border = guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.CentreOnScreen()

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


class NewProfileDialog(
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog   # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "ProfilesCreating"

	def __init__(self, parent):
		# Translators: The title of the dialog to create a new configuration profile.
		super().__init__(parent, title=_("New Profile"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: The label of a field to enter the name of a new configuration profile.
		profileNameText = _("Profile name:")
		self.profileName = sHelper.addLabeledControl(profileNameText, wx.TextCtrl)

		# Translators: The label of a radio button to specify that a profile will be used for manual activation
		# in the new configuration profile dialog.
		self.triggers = triggers = [(None, _("Manual activation"), True)]
		triggers.extend(parent.getSimpleTriggers())
		self.triggerChoice = sHelper.addItem(wx.RadioBox(self, label=_("Use this profile for:"),
			choices=[trig[1] for trig in triggers]))
		self.triggerChoice.Bind(wx.EVT_RADIOBOX, self.onTriggerChoice)
		self.autoProfileName = ""
		self.onTriggerChoice(None)

		sHelper.addDialogDismissButtons(wx.OK | wx.CANCEL, separated=True)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		self.AffirmativeId = wx.ID_OK
		self.EscapeId = wx.ID_CANCEL

		mainSizer.Add(sHelper.sizer, border = guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.Sizer = mainSizer
		self.profileName.SetFocus()
		self.CentreOnScreen()

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

		name = self.profileName.Value
		if not name:
			gui.messageBox(
				# Translators: An error displayed when the user attempts to create a configuration profile
				# with an empty name.
				_("You must choose a name for this profile."),
				# Translators: The title of an error message dialog.
				caption=_("Error"),
				style=wx.ICON_ERROR,
				parent=self
			)
			self.profileName.SetFocus()
			return
		name = api.filterFileName(name)
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
		# Also nullify the instance flag as the profiles dialog itself is dead.
		ProfilesDialog._instance = None

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


class RenameProfileDialog(
		gui.contextHelp.ContextHelpMixin,
		wx.TextEntryDialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	helpId = "ProfilesBasicManagement"
