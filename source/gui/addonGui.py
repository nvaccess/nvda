# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2023 NV Access Limited, Beqa Gozalishvili, Joseph Lee,
# Babbage B.V., Ethan Holliger, Arnold Loubriat, Thomas Stivers

import os
from typing import (
	List,
	Optional,
)
import weakref
from locale import strxfrm

import addonAPIVersion
import wx
import core
import config
import gui
from addonHandler import Addon
from logHandler import log
import addonHandler
import globalVars
from . import guiHelper
from . import nvdaControls
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
import gui.contextHelp


def promptUserForRestart():
	restartMessage = _(
		# Translators: A message asking the user if they wish to restart NVDA
		# as addons have been added, enabled/disabled or removed.
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


class ConfirmAddonInstallDialog(nvdaControls.MessageDialog):
	def __init__(self, parent, title, message, showAddonInfoFunction):
		super(ConfirmAddonInstallDialog, self).__init__(
			parent,
			title,
			message,
			dialogType=nvdaControls.MessageDialog.DIALOG_TYPE_WARNING
		)
		self._showAddonInfoFunction = showAddonInfoFunction

	def _addButtons(self, buttonHelper):
		addonInfoButton = buttonHelper.addButton(
			self,
			# Translators: A button in the addon installation warning / blocked dialog which shows
			# more information about the addon
			label=_("&About add-on...")
		)
		addonInfoButton.Bind(wx.EVT_BUTTON, lambda evt: self._showAddonInfoFunction())
		yesButton = buttonHelper.addButton(
			self,
			id=wx.ID_YES,
			# Translators: A button in the addon installation warning dialog which allows the user to agree to installing
			#  the add-on
			label=_("&Yes")
		)
		yesButton.SetDefault()
		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.YES))

		noButton = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the addon installation warning dialog which allows the user to decide not to
			# install the add-on
			label=_("&No")
		)
		noButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.NO))


class ErrorAddonInstallDialog(nvdaControls.MessageDialog):
	def __init__(self, parent, title, message, showAddonInfoFunction):
		super(ErrorAddonInstallDialog, self).__init__(
			parent,
			title,
			message,
			dialogType=nvdaControls.MessageDialog.DIALOG_TYPE_ERROR
		)
		self._showAddonInfoFunction = showAddonInfoFunction

	def _addButtons(self, buttonHelper):
		addonInfoButton = buttonHelper.addButton(
			self,
			# Translators: A button in the addon installation warning / blocked dialog which shows
			# more information about the addon
			label=_("&About add-on...")
		)
		addonInfoButton.Bind(wx.EVT_BUTTON, lambda evt: self._showAddonInfoFunction())

		okButton = buttonHelper.addButton(
			self,
			id=wx.ID_OK,
			# Translators: A button in the addon installation blocked dialog which will dismiss the dialog.
			label=_("OK")
		)
		okButton.SetDefault()
		okButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.OK))


class AddonsDialog(
		DpiScalingHelperMixinWithoutInit,
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog  # wxPython does not seem to call base class initializer, put last in MRO
):
	@classmethod
	def _instance(cls):
		""" type: () -> AddonsDialog
		return None until this is replaced with a weakref.ref object. Then the instance is retrieved
		with by treating that object as a callable.
		"""
		return None

	helpId = "AddonsManager"

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
		# Translators: The title of the Addons Dialog when add-ons are disabled
		titleWhenAddonsAreDisabled = _("Add-ons Manager (add-ons disabled)")
		super().__init__(
			parent,
			title=title if not globalVars.appArgs.disableAddons else titleWhenAddonsAreDisabled,
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
		)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		firstTextSizer = wx.BoxSizer(wx.VERTICAL)
		listAndButtonsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.HORIZONTAL))
		if globalVars.appArgs.disableAddons:
			label = _(
				# Translators: A message in the add-ons manager shown when add-ons are globally disabled.
				"NVDA was started with all add-ons disabled. "
				"You may modify the enabled / disabled state, and install or uninstall add-ons. "
				"Changes will not take effect until after NVDA is restarted."
			)
			addonsDisabledText = wx.StaticText(self, label=label)
			addonsDisabledText.Wrap(self.scaleSize(670))
			firstTextSizer.Add(addonsDisabledText)
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
			),
			flag=wx.EXPAND,
			proportion=1,
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
			flag=wx.ALL | wx.EXPAND,
			proportion=1,
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
		self.incompatAddonsButton = generalActions.addButton(self, label=_("&View incompatible add-ons..."))
		self.incompatAddonsButton.Bind(wx.EVT_BUTTON, self.onIncompatAddonsShowClick)

		mainSizer.Add(
			generalActions.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.LEFT | wx.RIGHT
		)

		mainSizer.Add(
			wx.StaticLine(self),
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND
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
		self.SetMinSize(mainSizer.GetMinSize())
		# Historical initial size, result of L{self.addonsList} being (550, 350) as of commit 1364839447.
		# Setting an initial size on L{self.addonsList} by passing a L{size} argument when
		# creating the control would also set its minimum size and thus block the dialog from being shrunk.
		self.SetSize(self.scaleSize((763, 509)))
		self.CentreOnScreen()
		self.addonsList.SetFocus()

	def onAddClick(self, evt: wx.EVT_BUTTON):
		# Translators: The message displayed in the dialog that allows you to choose an add-on package for installation.
		fd = wx.FileDialog(self, message=_("Choose Add-on Package File"),
		# Translators: the label for the NVDA add-on package file type in the Choose add-on dialog.
		wildcard=(_("NVDA Add-on Package (*.{ext})")+"|*.{ext}").format(ext=addonHandler.BUNDLE_EXTENSION),
		defaultDir="c:", style=wx.FD_OPEN)
		if fd.ShowModal() != wx.ID_OK:
			return
		addonPath = fd.GetPath()
		if installAddon(self, addonPath):
			self.refreshAddonsList(activeIndex=-1)
		else:
			self.refreshAddonsList()

	def onRemoveClick(self, evt: wx.EVT_BUTTON):
		index: int = self.addonsList.GetFirstSelected()
		if index < 0:
			return
		addon = self.curAddons[index]
		from gui._addonStoreGui.controls.messageDialogs import _shouldProceedToRemoveAddonDialog
		if not _shouldProceedToRemoveAddonDialog(addon):
			return
		addon.requestRemove()
		self.refreshAddonsList(activeIndex=index)
		self.addonsList.SetFocus()

	def getAddonStatus(self, addon):
		if addon.isBlocked:
			# Translators: The status shown for an addon when it's not considered compatible with this version of NVDA.
			incompatibleStatus =_("Incompatible")
			# When the addon is incompatible, it can not be enabled/disabled. Its state no longer matters.
			# So, return early.
			return incompatibleStatus

		statusList = []
		if addon.isRunning:
			# Translators: The status shown for an addon when its currently running in NVDA.
			statusList.append(_("Enabled"))
		elif addon.isPendingInstall:
			# Translators: The status shown for a newly installed addon before NVDA is restarted.
			statusList.append(_("Install"))
		# in some cases an addon can be expected to be disabled after install, so we want "install" to take precedence here
		# If add-ons are globally disabled, don't show this status.
		elif addon.isDisabled and not globalVars.appArgs.disableAddons:
			# Translators: The status shown for an addon when its currently suspended do to addons being disabled.
			statusList.append(_("Disabled"))
		if addon.isPendingRemove:
			# Translators: The status shown for an addon that has been marked as removed, before NVDA has been restarted.
			statusList.append(_("Removed after restart"))
		elif addon.isPendingDisable or (
				# yet to be installed, disabled after install
				not addon.isPendingEnable and addon.isPendingInstall and addon.isDisabled
			) or (
				# addons globally disabled, disabled after restart
				globalVars.appArgs.disableAddons and addon.isDisabled and not addon.isPendingEnable
			):
			# Translators: The status shown for an addon when it requires a restart to become disabled
			statusList.append(_("Disabled after restart"))
		elif addon.isPendingEnable or (
				# yet to be installed, enabled after install
				addon.isPendingInstall and not addon.isDisabled
			) or (
				# addons globally disabled, enabled after restart
				globalVars.appArgs.disableAddons and not addon.isDisabled
			):
			# Translators: The status shown for an addon when it requires a restart to become enabled
			statusList.append(_("Enabled after restart"))
		return ", ".join(statusList)

	def refreshAddonsList(self, activeIndex: int = 0) -> None:
		self.addonsList.DeleteAllItems()
		self.curAddons: List[Addon] = []
		anyAddonIncompatible = False
		from _addonStore.dataManager import addonDataManager
		assert addonDataManager
		installedAddons = addonDataManager._installedAddonsCache.installedAddons
		for addon in sorted(installedAddons.values(), key=lambda a: strxfrm(a.manifest['summary'])):
			self.addonsList.Append((
				addon.manifest['summary'],
				self.getAddonStatus(addon),
				addon.manifest['version'],
				addon.manifest['author']
			))
			self.curAddons.append(addon)
			anyAddonIncompatible = (
				anyAddonIncompatible  # once we find one incompatible addon we don't need to continue
				or not addon.isCompatible
			)
		self.incompatAddonsButton.Enable(anyAddonIncompatible)
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

	def onListItemSelected(self, evt: wx.ListEvent) -> None:
		index: int = evt.GetIndex()
		addon: Optional[Addon] = self.curAddons[index] if index >= 0 else None
		# #3090: Change toggle button label to indicate action to be taken if clicked.
		if addon is not None:
			# Translators: The label for a button in Add-ons Manager dialog to enable or disable the selected add-on.
			self.enableDisableButton.SetLabel(_("&Enable add-on") if not self._shouldDisable(addon) else _("&Disable add-on"))
		self.aboutButton.Enable(addon is not None and not addon.isPendingRemove)
		self.helpButton.Enable(bool(addon is not None and not addon.isPendingRemove and addon.getDocFilePath()))
		self.enableDisableButton.Enable(
			addon is not None
			and not addon.isPendingRemove
			and (
				addon.isCompatible
				or addon.overrideIncompatibility
			)
		)
		self.removeButton.Enable(addon is not None and not addon.isPendingRemove)

	def onClose(self, evt: wx.CloseEvent):
		self.DestroyChildren()
		self.Destroy()
		needsRestart = False
		for addon in self.curAddons:
			if addon.requiresRestart:
				log.debug(f"Add-on {addon.name} modified, restart required")
				needsRestart = True
				break
		if needsRestart:
			promptUserForRestart()

	def onAbout(self, evt: wx.EVT_BUTTON):
		index: int = self.addonsList.GetFirstSelected()
		if index<0: return
		addon = self.curAddons[index]
		from gui._addonStoreGui.controls.messageDialogs import _showAddonInfo
		_showAddonInfo(addon._addonGuiModel)

	def onHelp(self, evt):
		index = self.addonsList.GetFirstSelected()
		if index < 0:
			return
		path = self.curAddons[index].getDocFilePath()
		os.startfile(path)

	def onEnableDisable(self, evt: wx.EVT_BUTTON):
		index: int = self.addonsList.GetFirstSelected()
		if index < 0:
			return
		addon = self.curAddons[index]
		shouldDisable = self._shouldDisable(addon)
		try:
			# Counterintuitive, but makes sense when context is taken into account.
			addon.enable(not shouldDisable)
		except addonHandler.AddonError:
			from gui._addonStoreGui.viewModels.store import AddonStoreVM
			log.error("Couldn't change state for %s add-on"%addon.name, exc_info=True)
			if shouldDisable:
				message = AddonStoreVM._disableErrorMessage.format(addon=addon.manifest['summary'])
			else:
				message = AddonStoreVM._enableErrorMessage.format(addon=addon.manifest['summary'])
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
		IncompatibleAddonsDialog(
			parent=self,
			# the defaults from the addon GUI are fine. We are testing against the running version.
		).ShowModal()


# C901 'installAddon' is too complex (16)
# Note: when working on installAddon, look for opportunities to simplify
# and move logic out into smaller helper functions.
def installAddon(parentWindow: wx.Window, addonPath: str) -> bool:  # noqa: C901
	""" Installs the addon at path.
	Any error messages / warnings are presented to the user via a GUI message box.
	If attempting to install an addon that is pending removal, it will no longer be pending removal.
	@return True on success or False on failure.
	@note See also L{_addonStore.install.installAddon}
	"""
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
		return False  # Exit early, can't install an invalid bundle

	if not bundle._hasGotRequiredSupport:
		_showAddonRequiresNVDAUpdateDialog(parentWindow, bundle)
		return False  # Exit early, addon does not have required support
	elif bundle.canOverrideCompatibility:
		from gui._addonStoreGui.controls.messageDialogs import _shouldInstallWhenAddonTooOldDialog
		if _shouldInstallWhenAddonTooOldDialog(parentWindow, bundle._addonGuiModel):
			# Install incompatible version
			bundle.enableCompatibilityOverride()
		else:
			# Exit early, addon is not up to date with the latest API version.
			return False
	elif wx.YES != _showConfirmAddonInstallDialog(parentWindow, bundle):
		return False  # Exit early, User changed their mind about installation.

	from _addonStore.install import _getPreviouslyInstalledAddonById
	prevAddon = _getPreviouslyInstalledAddonById(bundle)
	if prevAddon:
		summary=bundle.manifest["summary"]
		curVersion=prevAddon.manifest["version"]
		newVersion=bundle.manifest["version"]

		# Translators: A title for the dialog asking if the user wishes to update a previously installed
		# add-on with this one.
		messageBoxTitle = _("Add-on Installation")

		overwriteExistingAddonInstallationMessage = _(
			# Translators: A message asking if the user wishes to update an add-on with the same version
			# currently installed according to the version number.
			"You are about to install version {newVersion} of {summary},"
			" which appears to be already installed. "
			"Would you still like to update?"
		).format(summary=summary, newVersion=newVersion)

		updateAddonInstallationMessage = _(
			# Translators: A message asking if the user wishes to update a previously installed
			# add-on with this one.
			"A version of this add-on is already installed. "
			"Would you like to update {summary} version {curVersion} to version {newVersion}?"
		).format(summary=summary, curVersion=curVersion, newVersion=newVersion)

		if gui.messageBox(
			overwriteExistingAddonInstallationMessage if curVersion == newVersion else updateAddonInstallationMessage,
			messageBoxTitle,
			wx.YES|wx.NO|wx.ICON_WARNING
		) != wx.YES:
			return False

	from contextlib import contextmanager

	@contextmanager
	def doneAndDestroy(window):
		try:
			yield window
		except:
			# pass on any exceptions
			raise
		finally:
			# but ensure that done and Destroy are called.
			window.done()
			window.Destroy()

	#  use a progress dialog so users know that something is happening.
	progressDialog = gui.IndeterminateProgressDialog(
		parentWindow,
		# Translators: The title of the dialog presented while an Addon is being installed.
		_("Installing Add-on"),
		# Translators: The message displayed while an addon is being installed.
		_("Please wait while the add-on is being installed.")
	)

	try:
		# Use context manager to ensure that `done` and `Destroy` are called on the progress dialog afterwards
		with doneAndDestroy(progressDialog):
			gui.ExecAndPump(addonHandler.installAddonBundle, bundle)
			if prevAddon:
				prevAddon.requestRemove()
			return True
	except:
		log.error("Error installing  addon bundle from %s" % addonPath, exc_info=True)
		gui.messageBox(
			# Translators: The message displayed when an error occurs when installing an add-on package.
			_("Failed to install add-on from %s") % addonPath,
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"),
			wx.OK | wx.ICON_ERROR
		)
	return False


def handleRemoteAddonInstall(addonPath: str):
	# Add-ons cannot be installed into a Windows store version of NVDA
	if config.isAppX:
		gui.messageBox(
			# Translators: The message displayed when an add-on cannot be installed due to NVDA running as a Windows Store app
			_("Add-ons cannot be installed in the Windows Store version of NVDA"),
			# Translators: The title of a dialog presented when an error occurs.
			_("Error"),
			wx.OK | wx.ICON_ERROR)
		return
	gui.mainFrame.prePopup()
	if installAddon(gui.mainFrame, addonPath):
		wx.CallAfter(promptUserForRestart)
	gui.mainFrame.postPopup()


def _showAddonRequiresNVDAUpdateDialog(
		parent: wx.Window,
		bundle: addonHandler.AddonBundle
) -> None:
	incompatibleMessage = _(
		# Translators: The message displayed when installing an add-on package is prohibited,
		# because it requires a later version of NVDA than is currently installed.
		"Installation of {summary} {version} has been blocked. The minimum NVDA version required for "
		"this add-on is {minimumNVDAVersion}, your current NVDA version is {NVDAVersion}"
	).format(
		summary=bundle.manifest['summary'],
		version=bundle.manifest['version'],
		minimumNVDAVersion=addonAPIVersion.formatForGUI(bundle.minimumNVDAVersion),
		NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
	)
	from gui._addonStoreGui.controls.messageDialogs import _showAddonInfo
	ErrorAddonInstallDialog(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=_("Add-on not compatible"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(bundle._addonGuiModel)
	).ShowModal()


def _showConfirmAddonInstallDialog(
		parent: wx.Window,
		bundle: addonHandler.AddonBundle
) -> int:
	confirmInstallMessage = _(
		# Translators: A message asking the user if they really wish to install an addon.
		"Are you sure you want to install this add-on?\n"
		"Only install add-ons from trusted sources.\n"
		"Addon: {summary} {version}"
	).format(**bundle.manifest)

	from gui._addonStoreGui.controls.messageDialogs import _showAddonInfo
	return ConfirmAddonInstallDialog(
		parent=parent,
		# Translators: Title for message asking if the user really wishes to install an Addon.
		title=_("Add-on Installation"),
		message=confirmInstallMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(bundle._addonGuiModel)
	).ShowModal()


class IncompatibleAddonsDialog(
		DpiScalingHelperMixinWithoutInit,
		gui.contextHelp.ContextHelpMixin,
		wx.Dialog  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""A dialog that lists incompatible addons, and why they are not compatible"""
	@classmethod
	def _instance(cls):
		""" type: () -> IncompatibleAddonsDialog
		return None until this is replaced with a weakref.ref object. Then the instance is retrieved
		with by treating that object as a callable.
		"""
		return None

	helpId = "IncompatibleAddonsManager"
	
	def __new__(cls, *args, **kwargs):
		instance = IncompatibleAddonsDialog._instance()
		if instance is None:
			return super(IncompatibleAddonsDialog, cls).__new__(cls, *args, **kwargs)
		return instance

	def __init__(
			self,
			parent,
			APIVersion = addonAPIVersion.CURRENT,
			APIBackwardsCompatToVersion = addonAPIVersion.BACK_COMPAT_TO
	):
		if IncompatibleAddonsDialog._instance() is not None:
			raise RuntimeError("Attempting to open multiple IncompatibleAddonsDialog instances")
		IncompatibleAddonsDialog._instance = weakref.ref(self)

		self._APIVersion = APIVersion
		self._APIBackwardsCompatToVersion = APIBackwardsCompatToVersion

		self.unknownCompatibilityAddonsList = list(addonHandler.getIncompatibleAddons(
			currentAPIVersion=APIVersion,
			backCompatToAPIVersion=APIBackwardsCompatToVersion
		))
		if not len(self.unknownCompatibilityAddonsList) > 0:
			# this dialog is not designed to show an empty list.
			raise RuntimeError("No incompatible addons.")

		super().__init__(
			parent,
			# Translators: The title of the Incompatible Addons Dialog
			title=_("Incompatible Add-ons"),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
		)

		mainSizer=wx.BoxSizer(wx.VERTICAL)
		settingsSizer=wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		maxControlWidth = 550
		introText = _(
			# Translators: The title of the Incompatible Addons Dialog
			"The following add-ons are incompatible with NVDA version {}."
			" These add-ons can not be enabled."
			" Please contact the add-on author for further assistance."
		).format(addonAPIVersion.formatForGUI(self._APIVersion))
		AddonSelectionIntroLabel=wx.StaticText(self, label=introText)
		AddonSelectionIntroLabel.Wrap(self.scaleSize(maxControlWidth))
		sHelper.addItem(AddonSelectionIntroLabel)
		# Translators: the label for the addons list in the incompatible addons dialog.
		entriesLabel=_("Incompatible add-ons")
		self.addonsList = sHelper.addLabeledControl(
			entriesLabel,
			nvdaControls.AutoWidthColumnListCtrl,
			style=wx.LC_REPORT|wx.LC_SINGLE_SEL,
		)

		# Translators: The label for a column in add-ons list used to identify add-on package name (example: package is OCR).
		self.addonsList.InsertColumn(1, _("Package"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to identify add-on's running status (example: status is running).
		self.addonsList.InsertColumn(2, _("Version"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to provide some explanation about incompatibility
		self.addonsList.InsertColumn(3, _("Incompatible reason"), width=self.scaleSize(180))

		buttonSizer = guiHelper.ButtonHelper(wx.HORIZONTAL)
		# Translators: The label for a button in Add-ons Manager dialog to show information about the selected add-on.
		self.aboutButton = buttonSizer.addButton(self, label=_("&About add-on..."))
		self.aboutButton.Disable()
		self.aboutButton.Bind(wx.EVT_BUTTON, self.onAbout)
		# Translators: The close button on an NVDA dialog. This button will dismiss the dialog.
		button = buttonSizer.addButton(self, label=_("&Close"), id=wx.ID_CLOSE)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		sHelper.addDialogDismissButtons(buttonSizer, separated=True)
		mainSizer.Add(
			settingsSizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND,
			proportion=1
		)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)

		self.SetAffirmativeId(wx.ID_CLOSE)
		self.SetEscapeId(wx.ID_CLOSE)
		button.Bind(wx.EVT_BUTTON, self.onClose)

		self.refreshAddonsList()
		self.SetMinSize(mainSizer.GetMinSize())
		# Historical initial size, result of L{self.addonsList} being (550, 350) as of PR #8006.
		# Setting an initial size on L{self.addonsList} by passing a L{size} argument when
		# creating the control would also set its minimum size and thus block the dialog from being shrunk.
		self.SetSize(self.scaleSize((606, 525)))
		self.CentreOnScreen()
		self.addonsList.SetFocus()

	def refreshAddonsList(self):
		self.addonsList.DeleteAllItems()
		self.curAddons: List[Addon] = []
		for idx, addon in enumerate(self.unknownCompatibilityAddonsList):
			self.addonsList.Append((
				addon.manifest['summary'],
				addon.version,
				addon.getIncompatibleReason(self._APIBackwardsCompatToVersion, self._APIVersion),
			))
			self.curAddons.append(addon)  # onAbout depends on being able to recall the current addon based on selected index
		activeIndex=0
		self.addonsList.Select(activeIndex, on=1)
		self.addonsList.SetItemState(activeIndex, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
		self.aboutButton.Enable(True)

	def onAbout(self, evt: wx.EVT_BUTTON):
		index: int = self.addonsList.GetFirstSelected()
		if index<0: return
		addon = self.curAddons[index]
		from gui._addonStoreGui.controls.messageDialogs import _showAddonInfo
		_showAddonInfo(addon._addonGuiModel)

	def onClose(self, evt):
		evt.Skip()
		self.EndModal(wx.OK)
		self.DestroyLater()  # ensure that the _instance weakref is destroyed.
