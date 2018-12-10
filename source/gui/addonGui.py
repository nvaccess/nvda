#gui/addonGui.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2012-2018 NV Access Limited, Beqa Gozalishvili, Joseph Lee, Babbage B.V., Ethan Holliger

import os
import weakref

import wx
import core
import config
import gui
from addonHandler import addonVersionCheck, compatValues
from addonHandler.addonVersionCheck import CURRENT_NVDA_VERSION, AddonCompatibilityState
from logHandler import log
import addonHandler
import globalVars
import buildVersion
import guiHelper
import nvdaControls
from dpiScalingHelper import DpiScalingHelperMixin

def promptUserForRestart():
	# Translators: A message asking the user if they wish to restart NVDA as addons have been added, enabled/disabled or removed.
	restartMessage = _(
		"Changes were made to add-ons. "
		"You must restart NVDA for these changes to take effect. "
		"Would you like to restart now?"
	)
	# Translators: Title for message asking if the user wishes to restart NVDA as addons have been added or removed.
	restartTitle = _("Restart NVDA")
	result = gui.messageBox(
		message=restartMessage,
		caption=restartTitle,
		style=wx.YES | wx.NO | wx.ICON_WARNING
	)
	if wx.YES == result:
		core.restart()

class ConfirmAddonInstallDialog(wx.Dialog, DpiScalingHelperMixin):
	def __init__(self, parent, title, message,
			userConfirmationMessage=None,
			errorDialog=False,
			showAddonInfoFunction=None
	):
		wx.Dialog.__init__(self, parent, title=title)
		DpiScalingHelperMixin.__init__(self, self.GetHandle())

		iconID = wx.ART_WARNING if not errorDialog else wx.ART_ERROR
		icon = wx.ArtProvider.GetIcon(iconID, client=wx.ART_MESSAGE_BOX)
		self.SetIcon(icon)

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		contentsSizer = guiHelper.BoxSizerHelper(parent=self, orientation=wx.VERTICAL)

		text = wx.StaticText(self, label=message)
		text.Wrap(self.scaleSize(self.GetSize().Width))
		contentsSizer.addItem(text)

		if userConfirmationMessage:
			confirmedCheckbox = wx.CheckBox(
					parent=self,
					label=userConfirmationMessage
				)
			contentsSizer.addItem(confirmedCheckbox)
			confirmedCheckbox.Bind(wx.EVT_CHECKBOX, self._toggleEnabledStateOfAffirmativeAction)
			self.confirmedCheckbox = confirmedCheckbox

		buttonHelper = guiHelper.ButtonHelper(wx.HORIZONTAL)
		if showAddonInfoFunction:
			addonInfoButton = buttonHelper.addButton(
				self,
				# Translators: A button in the addon installation warning / blocked dialog which shows
				# more information about the addon
				label=_("&About add-on...")
			)
			addonInfoButton.Bind(wx.EVT_BUTTON, lambda evt: showAddonInfoFunction())
		if errorDialog:
			okButton = buttonHelper.addButton(
				self,
				id=wx.ID_OK,
				# Translators: A button in the addon installation blocked dialog which will dismiss the dialog.
				label=_("OK")
			)
			okButton.SetDefault()
			okButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.OK))
		else:
			yesButton = buttonHelper.addButton(
				self,
				id=wx.ID_YES,
				# Translators: A button in the addon installation warning dialog which allows the user to agree to installing
				#  the add-on
				label=_("Yes")
			)
			yesButton.SetDefault()
			yesButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.YES))
			if userConfirmationMessage:
				yesButton.Disable()
			self.yesButton = yesButton
			noButton = buttonHelper.addButton(
				self,
				id=wx.ID_NO,
				# Translators: A button in the addon installation warning dialog which allows the user to decide not to
				# install the add-on
				label=_("No")
			)
			noButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.NO))
		contentsSizer.addDialogDismissButtons(buttonHelper)

		mainSizer.Add(
			contentsSizer.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL
		)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

	def _toggleEnabledStateOfAffirmativeAction(self, evt):
		self.yesButton.Enable(self.confirmedCheckbox.IsChecked())

class AddonsDialog(wx.Dialog, DpiScalingHelperMixin):
	@classmethod
	def _instance(cls):
		# type: () -> AddonsDialog
		return None

	def __new__(cls, *args, **kwargs):
		instance = AddonsDialog._instance()
		if instance is None:
			return super(AddonsDialog, cls).__new__(cls, *args, **kwargs)
		return instance

	def __init__(self, parent):
		if AddonsDialog._instance() is not None:
			return
		# #7077: _instance must not be kept alive once the dialog is closed or there can be issues
		# when add-ons manager reopens or another add-on is installed remotely.
		AddonsDialog._instance = weakref.ref(self)
		# Translators: The title of the Addons Dialog
		title = _("Add-ons Manager")
		wx.Dialog.__init__(self, parent, title=title)
		DpiScalingHelperMixin.__init__(self, self.GetHandle())

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		firstTextSizer = wx.BoxSizer(wx.VERTICAL)
		listAndButtonsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.HORIZONTAL))
		if globalVars.appArgs.disableAddons:
			# Translators: A message in the add-ons manager shown when all add-ons are disabled.
			label = _("All add-ons are currently disabled. To enable add-ons you must restart NVDA.")
			firstTextSizer.Add(wx.StaticText(self, label=label))
		# Translators: the label for the installed addons list in the addons manager.
		entriesLabel = _("Installed Add-ons")
		firstTextSizer.Add(wx.StaticText(self, label=entriesLabel))
		mainSizer.Add(
			firstTextSizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.TOP|wx.LEFT|wx.RIGHT
		)
		self.addonsList = listAndButtonsSizerHelper.addItem(
			nvdaControls.AutoWidthColumnListCtrl(
				parent=self,
				style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
				size=self.scaleSize((550, 350))
			)
		)
		# Translators: The label for a column in add-ons list used to identify add-on package name (example: package is OCR).
		self.addonsList.InsertColumn(0, _("Package"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to identify add-on's running status (example: status is running).
		self.addonsList.InsertColumn(1, _("Status"), width=self.scaleSize(50))
		# Translators: The label for a column in add-ons list used to identify add-on's version (example: version is 0.3).
		self.addonsList.InsertColumn(2, _("Version"), width=self.scaleSize(50))
		# Translators: The label for a column in add-ons list used to identify add-on's author (example: author is NV Access).
		self.addonsList.InsertColumn(3, _("Author"), width=self.scaleSize(300))
		self.addonsList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemSelected)

		# this is the group of buttons that affects the currently selected addon
		entryButtonsHelper=guiHelper.ButtonHelper(wx.VERTICAL)
		# Translators: The label for a button in Add-ons Manager dialog to show information about the selected add-on.
		self.aboutButton = entryButtonsHelper.addButton(self, label=_("&About add-on..."))
		self.aboutButton.Disable()
		self.aboutButton.Bind(wx.EVT_BUTTON, self.onAbout)
		# Translators: The label for a button in Add-ons Manager dialog to show the help for the selected add-on.
		self.helpButton = entryButtonsHelper.addButton(self, label=_("Add-on &help"))
		self.helpButton.Disable()
		self.helpButton.Bind(wx.EVT_BUTTON, self.onHelp)
		# Translators: The label for a button in Add-ons Manager dialog to enable or disable the selected add-on.
		self.enableDisableButton = entryButtonsHelper.addButton(self, label=_("&Disable add-on"))
		self.enableDisableButton.Disable()
		self.enableDisableButton.Bind(wx.EVT_BUTTON, self.onEnableDisable)
		# Translators: The label for a button to remove either:
		# Remove the selected add-on in Add-ons Manager dialog.
		# Remove a speech dictionary entry.
		self.removeButton = entryButtonsHelper.addButton(self, label=_("&Remove"))
		self.removeButton.Disable()
		self.removeButton.Bind(wx.EVT_BUTTON, self.onRemoveClick)
		listAndButtonsSizerHelper.addItem(entryButtonsHelper.sizer)

		mainSizer.Add(
			listAndButtonsSizerHelper.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL
		)

		# the following buttons are more general and apply regardless of the current selection.
		generalActions=guiHelper.ButtonHelper(wx.HORIZONTAL)
		# Translators: The label of a button in Add-ons Manager to open the Add-ons website and get more add-ons.
		self.getAddonsButton = generalActions.addButton(self, label=_("&Get add-ons..."))
		self.getAddonsButton.Bind(wx.EVT_BUTTON, self.onGetAddonsClick)
		# Translators: The label for a button in Add-ons Manager dialog to install an add-on.
		self.addButton = generalActions.addButton(self, label=_("&Install..."))
		self.addButton.Bind(wx.EVT_BUTTON, self.onAddClick)
		# Translators: The label of a button in the Add-ons Manager to open the list of incompatible add-ons.
		self.incompatAddonsButton = generalActions.addButton(self, label=_("&Manage incompatible add-ons..."))
		self.incompatAddonsButton.Bind(wx.EVT_BUTTON, self.onIncompatAddonsShowClick)

		mainSizer.Add(
			generalActions.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.LEFT | wx.RIGHT
		)

		mainSizer.Add(
			wx.StaticLine(self),
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.TOP | wx.BOTTOM | wx.EXPAND
		)

		# Translators: The label of a button to close the Addons dialog.
		closeButton = wx.Button(self, label=_("&Close"), id=wx.ID_CLOSE)
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(
			closeButton,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.CENTER | wx.ALIGN_RIGHT
		)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.refreshAddonsList()
		self.addonsList.SetFocus()
		self.CentreOnScreen()

	def onAddClick(self, evt):
		# Translators: The message displayed in the dialog that allows you to choose an add-on package for installation.
		fd = wx.FileDialog(self, message=_("Choose Add-on Package File"),
		# Translators: the label for the NVDA add-on package file type in the Choose add-on dialog.
		wildcard=(_("NVDA Add-on Package (*.{ext})")+"|*.{ext}").format(ext=addonHandler.BUNDLE_EXTENSION),
		defaultDir="c:", style=wx.FD_OPEN)
		if fd.ShowModal() != wx.ID_OK:
			return
		addonPath = fd.GetPath()
		self.installAddon(addonPath)

	def _showAddonRequiresNVDAUpdateDialog(self, bundle):
		# Translators: Displayed in the compatibility message when a version is unknown.
		unknownVersionString = _("unknown")
		# Translators: The message displayed when installing an add-on package is prohibited, because it requires
		# a later version of NVDA than is currently installed.
		incompatibleMessage = _(
			"Installation of {summary} {version} has been blocked. The minimum NVDA version required for "
			"this add-on is {minimumNVDAVersion}, your current NVDA version is {NVDAVersion}"
		).format(
			summary=bundle.manifest['summary'],
			version=bundle.manifest['version'],
			NVDAVersion="%d.%d (%s)" % (buildVersion.version_year, buildVersion.version_major, buildVersion.version),
			minimumNVDAVersion=bundle.manifest['minimumNVDAVersion'] or unknownVersionString
		)
		ConfirmAddonInstallDialog(
			parent=self,
			# Translators: The title of a dialog presented when an error occurs.
			title=_("Error"),
			message=incompatibleMessage,
			errorDialog=True,
			showAddonInfoFunction=lambda: self._showAddonInfo(bundle.manifest)
		).ShowModal()

	def _showAddonUntestedDialog(self, bundle):
		# Translators: A message asking the user to confirm they understand the risks of installing an untested addon
		confirmInstallMessage = _(
			"{summary} {version} has not been tested with this version of NVDA, "
			"installing this add-on is not recommended.\n\n"
			"Are you sure you want to install this add-on?\n"
			"Only install add-ons from trusted sources.\n"
		).format(**bundle.manifest)
		# Translators: A message asking the user to confirm that they are aware that this addon has not been tested.
		confirmAddonNotTestedMessage = _("I understand that this add-on has not been tested with my version of NVDA")

		return ConfirmAddonInstallDialog(
			parent=self,
			# Translators: Title for message asking if the user really wishes to install an Addon.
			title=_("Warning: Untested Add-on Installation"),
			message=confirmInstallMessage,
			userConfirmationMessage=confirmAddonNotTestedMessage,
			showAddonInfoFunction=lambda: self._showAddonInfo(bundle.manifest)
		).ShowModal()

	def _showConfirmAddonInstallDialog(self, bundle):
		# Translators: A message asking the user if they really wish to install an addon.
		confirmInstallMessage = _(
			"Are you sure you want to install this add-on?\n"
			"Only install add-ons from trusted sources.\n"
			"Addon: {summary} {version}"
		).format(**bundle.manifest)

		return ConfirmAddonInstallDialog(
			parent=self,
			# Translators: Title for message asking if the user really wishes to install an Addon.
			title=_("Add-on Installation"),
			message=confirmInstallMessage,
			showAddonInfoFunction=lambda: self._showAddonInfo(bundle.manifest)
		).ShowModal()

	def installAddon(self, addonPath, closeAfter=False):
		try:
			try:
				bundle = addonHandler.AddonBundle(addonPath)
			except:
				log.error("Error opening addon bundle from %s" % addonPath, exc_info=True)
				gui.messageBox(
					# Translators: The message displayed when an error occurs when opening an add-on package for adding.
					_("Failed to open add-on package file at %s - missing file or invalid file format") % addonPath,
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR
				)
				return

			if not addonVersionCheck.hasAddonGotRequiredSupport(bundle):
				self._showAddonRequiresNVDAUpdateDialog(bundle)
				return

			if not addonVersionCheck.isAddonTested(bundle):
				if wx.YES != self._showAddonUntestedDialog(bundle):
					return
				AddonCompatibilityState.setAddonCompatibility(
					addon=bundle,
					compatibilityStateValue=compatValues.MANUALLY_SET_COMPATIBLE
				)
			elif wx.YES != self._showConfirmAddonInstallDialog(bundle):
				return

			prevAddon=None
			for addon in self.curAddons:
				if not addon.isPendingRemove and bundle.name==addon.manifest['name']:
					prevAddon=addon
					break
			if prevAddon:
				summary=bundle.manifest["summary"]
				curVersion=prevAddon.manifest["version"]
				newVersion=bundle.manifest["version"]
				if gui.messageBox(
					# Translators: A message asking if the user wishes to update an add-on with the same version currently installed according to the version number.
					_("You are about to install version {newVersion} of {summary}, which appears to be already installed. Would you still like to update?").format(
						summary=summary,
						newVersion=newVersion
					)
					if curVersion==newVersion else
					# Translators: A message asking if the user wishes to update a previously installed add-on with this one.
					_("A version of this add-on is already installed. Would you like to update {summary} version {curVersion} to version {newVersion}?").format(
						summary=summary,
						curVersion=curVersion,
						newVersion=newVersion
					),
					# Translators: A title for the dialog  asking if the user wishes to update a previously installed add-on with this one.
					_("Add-on Installation"),
					wx.YES|wx.NO|wx.ICON_WARNING)!=wx.YES:
						return
				prevAddon.requestRemove()
			progressDialog = gui.IndeterminateProgressDialog(gui.mainFrame,
			# Translators: The title of the dialog presented while an Addon is being installed.
			_("Installing Add-on"),
			# Translators: The message displayed while an addon is being installed.
			_("Please wait while the add-on is being installed."))
			try:
				gui.ExecAndPump(addonHandler.installAddonBundle,bundle)
			except:
				log.error("Error installing  addon bundle from %s"%addonPath,exc_info=True)
				self.refreshAddonsList()
				progressDialog.done()
				del progressDialog
				# Translators: The message displayed when an error occurs when installing an add-on package.
				gui.messageBox(_("Failed to install add-on  from %s")%addonPath,
					# Translators: The title of a dialog presented when an error occurs.
					_("Error"),
					wx.OK | wx.ICON_ERROR)
				return
			else:
				self.refreshAddonsList(activeIndex=-1)
				progressDialog.done()
				del progressDialog
		finally:
			if closeAfter:
				# #4460: If we do this immediately, wx seems to drop the WM_QUIT sent if the user chooses to restart.
				# This seems to have something to do with the wx.ProgressDialog.
				# The CallLater seems to work around this.
				wx.CallLater(1, self.Close)

	def onRemoveClick(self,evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		# Translators: Presented when attempting to remove the selected add-on.
		if gui.messageBox(_("Are you sure you wish to remove the selected add-on from NVDA?"),
			# Translators: Title for message asking if the user really wishes to remove the selected Addon.
			_("Remove Add-on"), wx.YES_NO|wx.ICON_WARNING) != wx.YES: return
		addon=self.curAddons[index]
		addon.requestRemove()
		self.refreshAddonsList(activeIndex=index)
		self.addonsList.SetFocus()

	def getAddonStatus(self,addon):
		statusList = []
		if addon.isRunning:
			# Translators: The status shown for an addon when its currently running in NVDA.
			statusList.append(_("Enabled"))
		elif addon.isPendingInstall:
			# Translators: The status shown for a newly installed addon before NVDA is restarted.
			statusList.append(_("Install"))
		# in some cases an addon can be expected to be disabled after install, so we want "install" to take precedence here
		elif globalVars.appArgs.disableAddons or addon.isDisabled:
			# Translators: The status shown for an addon when its currently suspended do to addons being disabled.
			statusList.append(_("Disabled"))
		if addon.isPendingRemove:
			# Translators: The status shown for an addon that has been marked as removed, before NVDA has been restarted.
			statusList.append(_("Removed after restart"))
		elif addon.isPendingDisable or (not addon.isPendingEnable and addon.isPendingInstall and addon.isDisabled):
			# Translators: The status shown for an addon when it requires a restart to become disabled
			statusList.append(_("Disabled after restart"))
		elif addon.isPendingEnable or (addon.isPendingInstall and not addon.isDisabled):
			# Translators: The status shown for an addon when it requires a restart to become enabled
			statusList.append(_("Enabled after restart"))
		if addonVersionCheck.isAddonConsideredIncompatible(addon):
			# Translators: The status shown for an addon when it's not considered compatible with this version of NVDA.
			statusList.append(_("Incompatible"))
		elif addonVersionCheck.isCompatSetManually(addon):
			# Translators: The status shown for an addon when it's added to the whitelist.
			statusList.append(_("Compatibility set manually"))
		return ", ".join(statusList)

	def refreshAddonsList(self,activeIndex=0):
		self.addonsList.DeleteAllItems()
		self.curAddons=[]
		shouldEnableIncompatAddonsButton = False
		for addon in addonHandler.getAvailableAddons():
			self.addonsList.Append((
				addon.manifest['summary'],
				self.getAddonStatus(addon),
				addon.manifest['version'],
				addon.manifest['author']
			))
			self.curAddons.append(addon)
			shouldEnableIncompatAddonsButton = (
				shouldEnableIncompatAddonsButton or (
					addonVersionCheck.hasAddonGotRequiredSupport(addon, version=addonVersionCheck.CURRENT_NVDA_VERSION)
					and not addonVersionCheck.isAddonTested(addon, version=addonVersionCheck.CURRENT_NVDA_VERSION)
				)
			)
		self.incompatAddonsButton.Enable(shouldEnableIncompatAddonsButton)
		# select the given active addon or the first addon if not given
		curAddonsLen=len(self.curAddons)
		if curAddonsLen>0:
			if activeIndex==-1:
				activeIndex=curAddonsLen-1
			elif activeIndex<0 or activeIndex>=curAddonsLen:
				activeIndex=0
			self.addonsList.Select(activeIndex,on=1)
			self.addonsList.SetItemState(activeIndex,wx.LIST_STATE_FOCUSED,wx.LIST_STATE_FOCUSED)
		else:
			self.aboutButton.Disable()
			self.helpButton.Disable()
			self.removeButton.Disable()

	def _shouldDisable(self, addon):
		return not (addon.isPendingDisable or (addon.isDisabled and not addon.isPendingEnable))

	def onListItemSelected(self, evt):
		index=evt.GetIndex()
		addon=self.curAddons[index] if index>=0 else None
		# #3090: Change toggle button label to indicate action to be taken if clicked.
		if addon is not None:
			# Translators: The label for a button in Add-ons Manager dialog to enable or disable the selected add-on.
			self.enableDisableButton.SetLabel(_("&Enable add-on") if not self._shouldDisable(addon) else _("&Disable add-on"))
		self.aboutButton.Enable(addon is not None and not addon.isPendingRemove)
		self.helpButton.Enable(bool(addon is not None and not addon.isPendingRemove and addon.getDocFilePath()))
		self.enableDisableButton.Enable(
			addon is not None and
			not addon.isPendingRemove and
			not addonVersionCheck.isAddonConsideredIncompatible(addon)
		)
		self.removeButton.Enable(addon is not None and not addon.isPendingRemove)

	def onClose(self,evt):
		self.DestroyChildren()
		self.Destroy()
		needsRestart = False
		for addon in self.curAddons:
			if (addon.isPendingInstall or addon.isPendingRemove
				or addon.isDisabled and addon.isPendingEnable
				or addon.isRunning and addon.isPendingDisable):
				needsRestart = True
				break
		if needsRestart:
			promptUserForRestart()

	def onAbout(self,evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		manifest=self.curAddons[index].manifest
		self._showAddonInfo(manifest)

	def _showAddonInfo(self, manifest):
		# Translators: message shown in the Addon Information dialog.
		message=[_(
			"{summary} ({name})\n"
			"Version: {version}\n"
			"Author: {author}\n"
			"Description: {description}\n"
		).format(**manifest)]
		url=manifest.get('url')
		if url:
			# Translators: the url part of the About Add-on information
			message.append(_("URL: {url}").format(url=url))
		# Translators: shown when a version is unknown in the about add-on dialog
		unknownVersion = _("unknown")
		minimumNVDAVersion = manifest.get('minimumNVDAVersion', default=unknownVersion)
		message.append(
			# Translators: the minimum NVDA version part of the About Add-on information
			_("Minimum required NVDA version: {version}").format(version=minimumNVDAVersion)
		)
		lastTestedNVDAVersion = manifest.get('lastTestedNVDAVersion', unknownVersion)
		message.append(
			# Translators: the last NVDA version tested part of the About Add-on information
			_("Last NVDA version tested: {version}").format(version=lastTestedNVDAVersion)
		)
		# Translators: title for the Addon Information dialog
		title=_("Add-on Information")
		gui.messageBox("\n".join(message), title, wx.OK)

	def onHelp(self, evt):
		index = self.addonsList.GetFirstSelected()
		if index < 0:
			return
		path = self.curAddons[index].getDocFilePath()
		os.startfile(path)

	def onEnableDisable(self, evt):
		index=self.addonsList.GetFirstSelected()
		if index<0: return
		addon=self.curAddons[index]
		shouldDisable = self._shouldDisable(addon)
		try:
			# Counterintuitive, but makes sense when context is taken into account.
			addon.enable(not shouldDisable)
		except addonHandler.AddonError:
			log.error("Couldn't change state for %s add-on"%addon.name, exc_info=True)
			if shouldDisable:
				# Translators: The message displayed when the add-on cannot be disabled.
				message = _("Could not disable the {description} add-on.").format(
					description=addon.manifest['summary'])
			else:
				# Translators: The message displayed when the add-on cannot be enabled.
				message = _("Could not enable the {description} add-on.").format(
					description=addon.manifest['summary'])
			gui.messageBox(
				message,
				# Translators: The title of a dialog presented when an error occurs.
				_("Error"),
				wx.OK | wx.ICON_ERROR
			)
			return

		self.enableDisableButton.SetLabel(_("&Enable add-on") if shouldDisable else _("&Disable add-on"))
		self.refreshAddonsList(activeIndex=index)

	def onGetAddonsClick(self, evt):
		ADDONS_URL = "http://addons.nvda-project.org"
		os.startfile(ADDONS_URL)

	def onIncompatAddonsShowClick(self, evt):
		incompatibleAddons = IncompatibleAddonsDialog(
			parent=self,
			NVDAVersion=buildVersion.getCurrentVersionTuple()
		)
		def afterDialog(res):
			# here we need to check if the compatibility has changed.
			# addons that have become incompat should be disabled, and a restart prompt shown
			# addons that have become compat should be visible, but not enabled unless they already were.
			from addonHandler.compatValues import MANUALLY_SET_INCOMPATIBLE
			getAddonCompatibility = AddonCompatibilityState.getAddonCompatibility
			manuallySetIncompatibleAddons = addonHandler.getAvailableAddons(
				filterFunc=lambda addon: ( MANUALLY_SET_INCOMPATIBLE == getAddonCompatibility(addon, CURRENT_NVDA_VERSION))
			)
			for addon in manuallySetIncompatibleAddons:
				addon.enable(shouldEnable=False)
			self.refreshAddonsList()

		from gui import runScriptModalDialog
		runScriptModalDialog(incompatibleAddons, afterDialog)

	@classmethod
	def handleRemoteAddonInstall(cls, addonPath):
		# Add-ons cannot be installed into a Windows store version of NVDA
		if config.isAppX:
			# Translators: The message displayed when an add-on cannot be installed due to NVDA running as a Windows Store app
			gui.messageBox(_("Add-ons cannot be installed in the Windows Store version of NVDA"),
				# Translators: The title of a dialog presented when an error occurs.
				_("Error"),
				wx.OK | wx.ICON_ERROR)
			return
		closeAfter = AddonsDialog._instance() is None
		dialog = AddonsDialog(gui.mainFrame)
		dialog.installAddon(addonPath, closeAfter=closeAfter)
		del dialog


class IncompatibleAddonsDialog(wx.Dialog, DpiScalingHelperMixin):
	"""A dialog that allows one to blacklist or whitelist add-ons that are incompatible
	with a current or new version of NVDA."""
	@classmethod
	def _instance(cls):
		# type: () -> IncompatibleAddonsDialog
		return None

	def __new__(cls, *args, **kwargs):
		instance = IncompatibleAddonsDialog._instance()
		if instance is None:
			return super(IncompatibleAddonsDialog, cls).__new__(cls, *args, **kwargs)
		return instance

	def __init__(
			self,
			parent,
			NVDAVersion=CURRENT_NVDA_VERSION
	):
		if IncompatibleAddonsDialog._instance() is not None:
			raise RuntimeError("Attempting to open multiple IncompatibleAddonsDialog instances")
		IncompatibleAddonsDialog._instance = weakref.ref(self)

		self.unknownCompatibilityAddonsList = list(addonHandler.getAddonsWithoutKnownCompatibility(NVDAVersion))
		if not len(self.unknownCompatibilityAddonsList) > 0:
			raise RuntimeError("No unknown compat addons.")

		# Translators: The title of the Incompatible Addons Dialog
		wx.Dialog.__init__(self, parent, title=_("Incompatible Add-ons"))
		DpiScalingHelperMixin.__init__(self, self.GetHandle())

		self.NVDAVersion = NVDAVersion

		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		maxControlWidth = 550
		# Translators: The title of the Incompatible Addons Dialog
		introText = _(
			"The compatibility of the following add-ons is not known, they have not been tested against NVDA version {}. "
			"Please use the checkboxes to indicate add-ons that should remain available.\n\n"
			"Warning: Untested add-ons may cause instability while using NVDA. "
			"Please contact the add-on author for further assistance."
		).format("%s.%s.%s" % NVDAVersion)
		AddonSelectionIntroLabel=wx.StaticText(self, label=introText)
		AddonSelectionIntroLabel.Wrap(self.scaleSize(maxControlWidth))
		sHelper.addItem(AddonSelectionIntroLabel)
		# Translators: the label for the addons list in the addon selection dialog.
		entriesLabel=_("Untested add-ons")
		self.addonsList = sHelper.addLabeledControl(
			entriesLabel,
			nvdaControls.AutoWidthColumnCheckListCtrl,
			style=wx.LC_REPORT|wx.LC_SINGLE_SEL,
			size=self.scaleSize((maxControlWidth, 350))
		)

		# Translators: The label for a column in add-ons list used to check / uncheck whether the add-on is manually set  compatible
		self.addonsList.InsertColumn(0, _("Available"), width=self.scaleSize(70))
		# Translators: The label for a column in add-ons list used to identify add-on package name (example: package is OCR).
		self.addonsList.InsertColumn(1, _("Package"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to identify add-on's running status (example: status is running).
		self.addonsList.InsertColumn(2, _("Version"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to identify the last version of NVDA
		# this add-on has been tested with.
		self.addonsList.InsertColumn(3, _("Last tested NVDA version"), width=self.scaleSize(180))

		buttonSizer = guiHelper.ButtonHelper(wx.HORIZONTAL)
		continueID = wx.ID_OK
		# Translators: The continue button on a NVDA dialog. This button will accept any changes and dismiss the dialog.
		button = buttonSizer.addButton(self, label=_("Continue"), id=continueID)
		sHelper.addDialogDismissButtons(buttonSizer)
		mainSizer.Add(settingsSizer, border=20, flag=wx.ALL)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

		self.SetAffirmativeId(continueID)
		self.SetEscapeId(continueID)
		button.Bind(wx.EVT_BUTTON, self.onContinue)

		self.refreshAddonsList()
		self.addonsList.SetFocus()
		self.CentreOnScreen()

	def refreshAddonsList(self,activeIndex=0):
		self.addonsList.DeleteAllItems()
		self.curAddons=[]
		for idx, addon in enumerate(self.unknownCompatibilityAddonsList):
			self.addonsList.Append((
				"",  # check box field
				addon.manifest['summary'],
				addon.version,
				addon.manifest.get('lastTestedNVDAVersion') or
				# Translators: Displayed for add-ons in the incompatible add-ons dialog
				# if the last tested NVDA version is not specified.
				_("not specified")
			))
			compatValue = AddonCompatibilityState.getAddonCompatibility(addon, CURRENT_NVDA_VERSION)
			shouldCheck = compatValue == compatValues.MANUALLY_SET_COMPATIBLE
			self.addonsList.CheckItem(idx, check=shouldCheck)
		# select the given active addon, the last addon (after an addon is installed), or the first addon if not given
		curAddonsLen=len(self.unknownCompatibilityAddonsList)
		if curAddonsLen>0:  # No addons to select
			if activeIndex==-1:  # Special value, select last addon (newly installed)
				activeIndex=curAddonsLen-1
			elif activeIndex<0 or activeIndex>=curAddonsLen:  # Index invalid, select first addon.
				activeIndex=0
			self.addonsList.Select(activeIndex,on=1)
			self.addonsList.SetItemState(activeIndex,wx.LIST_STATE_FOCUSED,wx.LIST_STATE_FOCUSED)

	def saveState(self):
		for itemIndex in xrange(len(self.unknownCompatibilityAddonsList)):
			checked = self.addonsList.IsChecked(itemIndex)
			compatValue = compatValues.MANUALLY_SET_COMPATIBLE if checked else compatValues.MANUALLY_SET_INCOMPATIBLE
			addon = self.unknownCompatibilityAddonsList[itemIndex]
			AddonCompatibilityState.setAddonCompatibility(addon, compatibilityStateValue=compatValue)

	def onContinue(self, evt):
		try:
			self.saveState()
		except:
			log.debug("unable to save state", exc_info=True)
		finally:
			self.EndModal(wx.OK)

	def Destroy(self):
		super(IncompatibleAddonsDialog, self).Destroy()
		# for some reason we have to manually call Destroy on addonList, wx does not do this for us.
		self.addonsList.Destroy()
