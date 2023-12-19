# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2012-2023 NV Access Limited, Beqa Gozalishvili, Joseph Lee,
# Babbage B.V., Ethan Holliger, Arnold Loubriat, Thomas Stivers

import weakref

import addonAPIVersion
import wx
import core
import config
import gui
from addonHandler import Addon
from logHandler import log
import addonHandler
from . import guiHelper
from . import nvdaControls
from .message import displayDialogAsModal
from .dpiScalingHelper import DpiScalingHelperMixinWithoutInit
import gui.contextHelp
import ui
import systemUtils


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
		if gui.message.isModalMessageBoxActive():
			# For unknown reasons speech doesn't occur unless this is called with a delay
			wx.CallLater(500, ui.message, gui.blockAction.Context.MODAL_DIALOG_OPEN.translatedMessage)
		else:
			core.restart()


class ConfirmAddonInstallDialog(nvdaControls.MessageDialog):
	def __init__(self, parent, title, message, showAddonInfoFunction):
		super().__init__(
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
		super().__init__(
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
		displayDialogAsModal(IncompatibleAddonsDialog(
			parent=self,
			# the defaults from the addon GUI are fine. We are testing against the running version.
		))


# C901 'installAddon' is too complex (16)
# Note: when working on installAddon, look for opportunities to simplify
# and move logic out into smaller helper functions.
def installAddon(parentWindow: wx.Window, addonPath: str) -> bool:  # noqa: C901
	""" Installs the addon bundle at path.
	Only used for installing external add-on bundles.
	Any error messages / warnings are presented to the user via a GUI message box.
	If attempting to install an addon that is pending removal, it will no longer be pending removal.
	@return True on success or False on failure.
	@note See also L{addonStore.install.installAddon}
	"""
	from gui.addonStoreGui.controls.messageDialogs import (
		_showAddonRequiresNVDAUpdateDialog,
		_showConfirmAddonInstallDialog,
		_shouldInstallWhenAddonTooOldDialog,
	)
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
		_showAddonRequiresNVDAUpdateDialog(parentWindow, bundle._addonGuiModel)
		return False  # Exit early, addon does not have required support
	elif bundle.canOverrideCompatibility:
		shouldInstall, rememberChoice = _shouldInstallWhenAddonTooOldDialog(parentWindow, bundle._addonGuiModel)
		if shouldInstall:
			# Install incompatible version
			bundle.enableCompatibilityOverride()
		else:
			# Exit early, addon is not up to date with the latest API version.
			return False
	elif wx.YES != _showConfirmAddonInstallDialog(parentWindow, bundle._addonGuiModel):
		return False  # Exit early, User changed their mind about installation.

	from addonStore.install import _getPreviouslyInstalledAddonById
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
			systemUtils.ExecAndPump(addonHandler.installAddonBundle, bundle)
			if prevAddon:
				from addonStore.dataManager import addonDataManager
				assert addonDataManager
				# External install should remove cached add-on
				addonDataManager._deleteCacheInstalledAddon(prevAddon.name)
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
		self.addonsList.AppendColumn(_("Package"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to identify add-on's running status (example: status is running).
		self.addonsList.AppendColumn(_("Version"), width=self.scaleSize(150))
		# Translators: The label for a column in add-ons list used to provide some explanation about incompatibility
		self.addonsList.AppendColumn(_("Incompatible reason"), width=self.scaleSize(180))

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
		self.curAddons: list[Addon] = []
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
		from gui.addonStoreGui.controls.messageDialogs import _showAddonInfo
		_showAddonInfo(addon._addonGuiModel)

	def onClose(self, evt):
		evt.Skip()
		self.EndModal(wx.OK)
		self.DestroyLater()  # ensure that the _instance weakref is destroyed.
