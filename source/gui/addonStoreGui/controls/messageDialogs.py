# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2025 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import threading
from time import sleep
from typing import (
	TYPE_CHECKING,
)
import winsound

import wx

import addonAPIVersion
from addonStore.models.addon import (
	_AddonGUIModel,
	_AddonStoreModel,
	_AddonManifestModel,
)
from addonStore.dataManager import addonDataManager
from addonStore.models.status import _StatusFilterKey, AvailableAddonStatus, getStatus
import config
from config.configFlags import AddonsAutomaticUpdate
import gui
from gui import nvdaControls
from gui.addonGui import ConfirmAddonInstallDialog, ErrorAddonInstallDialog, promptUserForRestart
from gui.addonStoreGui.viewModels.addonList import AddonListItemVM
from gui.contextHelp import ContextHelpMixin
from gui.guiHelper import (
	BoxSizerHelper,
	BORDER_FOR_DIALOGS,
	ButtonHelper,
	SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS,
)
from gui.message import DisplayableError, displayDialogAsModal, messageBox, _countAsMessageBox
from logHandler import log
import NVDAState
from speech.priorities import SpeechPriority
import ui
import windowUtils

if TYPE_CHECKING:
	from addonStore.models.version import SupportsVersionCheck

__all__ = [
	"ErrorAddonInstallDialogWithYesNoButtons",
	"_shouldProceedWhenInstalledAddonVersionUnknown",
	"_shouldProceedToRemoveAddonDialog",
	"_shouldInstallWhenAddonTooOldDialog",
	"_shouldEnableWhenAddonTooOldDialog",
	"_showAddonRequiresNVDAUpdateDialog",
	"_showConfirmAddonInstallDialog",
	"_showAddonInfo",
	"_SafetyWarningDialog",
	"UpdatableAddonsDialog",
]


class ErrorAddonInstallDialogWithYesNoButtons(ErrorAddonInstallDialog):
	def __init__(self, *args, useRememberChoiceCheckbox: bool = False, **kwargs):
		self.useRememberChoiceCheckbox = useRememberChoiceCheckbox
		super().__init__(*args, **kwargs)

	def _addButtons(self, buttonHelper: ButtonHelper) -> None:
		addonInfoButton = buttonHelper.addButton(
			self,
			# Translators: A button in the addon installation warning / blocked dialog which shows
			# more information about the addon
			label=pgettext("addonStore", "&About add-on..."),
		)
		addonInfoButton.Bind(wx.EVT_BUTTON, lambda evt: self._showAddonInfoFunction())

		yesButton = buttonHelper.addButton(
			self,
			id=wx.ID_YES,
			# Translators: A button in the addon installation blocked dialog which will confirm the available action.
			label=pgettext("addonStore", "&Yes"),
		)
		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.YES))

		noButton = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the addon installation blocked dialog which will dismiss the dialog.
			label=pgettext("addonStore", "&No"),
		)
		noButton.SetDefault()
		noButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.NO))

	def _addContents(self, contentsSizer: BoxSizerHelper):
		if self.useRememberChoiceCheckbox:
			self.rememberChoiceCheckbox = wx.CheckBox(
				self,
				# Translators: A checkbox in the dialog to remember the choice made when installing or enabling
				# incompatible add-ons, or when removing add-ons.
				label=pgettext("addonStore", "Remember this choice for subsequent add-ons"),
			)
			contentsSizer.addItem(self.rememberChoiceCheckbox)

	def shouldRememberChoice(self) -> bool:
		if self.useRememberChoiceCheckbox:
			return self.rememberChoiceCheckbox.IsChecked()
		return False


def _shouldProceedWhenInstalledAddonVersionUnknown(
	parent: wx.Window,
	addon: _AddonGUIModel,
	useRememberChoiceCheckbox: bool = False,
) -> tuple[bool, bool]:
	# an installed add-on should have an addon Handler Model
	assert addon._addonHandlerModel
	incompatibleMessage = pgettext(
		"addonStore",
		# Translators: The message displayed when updating an add-on, but the installed version
		# identifier can not be compared with the version to be installed.
		"Warning: add-on installation may result in downgrade: {name}. "
		"The installed add-on version cannot be compared with the add-on store version. "
		"Installed version: {oldVersion}. "
		"Available version: {version}.\n"
		"Proceed with installation anyway? ",
	).format(
		name=addon.displayName,
		version=addon.addonVersionName,
		oldVersion=addon._addonHandlerModel.version,
		lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
		NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT),
	)
	dlg = ErrorAddonInstallDialogWithYesNoButtons(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=pgettext("addonStore", "Install add-on"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon),
		useRememberChoiceCheckbox=useRememberChoiceCheckbox,
	)
	res = displayDialogAsModal(dlg)
	return (res == wx.YES), dlg.shouldRememberChoice()


def _shouldProceedToRemoveAddonDialog(
	parent,
	addon: "SupportsVersionCheck",
	useRememberChoiceCheckbox: bool = False,
) -> tuple[bool, bool]:
	removeMessage = pgettext(
		"addonStore",
		# Translators: Presented when attempting to remove the selected add-on.
		# {addon} is replaced with the add-on name.
		"Are you sure you wish to remove the {addon} add-on from NVDA? This cannot be undone.",
	).format(addon=addon.displayName)
	dlg = ErrorAddonInstallDialogWithYesNoButtons(
		parent=parent,
		# Translators: Title for message asking if the user really wishes to remove the selected Add-on.
		title=pgettext("addonStore", "Remove add-on"),
		message=removeMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon),
		useRememberChoiceCheckbox=useRememberChoiceCheckbox,
	)
	res = displayDialogAsModal(dlg)
	return (res == wx.YES), dlg.shouldRememberChoice()


def _shouldInstallWhenAddonTooOldDialog(
	parent: wx.Window,
	addon: _AddonGUIModel,
	useRememberChoiceCheckbox: bool = False,
) -> tuple[bool, bool]:
	incompatibleMessage = pgettext(
		"addonStore",
		# Translators: The message displayed when installing an add-on package that is incompatible
		# because the add-on is too old for the running version of NVDA.
		"Warning: add-on is incompatible: {name} {version}. "
		"Check for an updated version of this add-on if possible. "
		"This add-on was last tested with NVDA {lastTestedNVDAVersion}. "
		"NVDA requires this add-on to be tested with NVDA {nvdaVersion} or higher. "
		"Installation may cause unstable behavior in NVDA.\n"
		"Proceed with installation anyway? ",
	).format(
		name=addon.displayName,
		version=addon.addonVersionName,
		lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
		nvdaVersion=addonAPIVersion.formatForGUI(addonAPIVersion.BACK_COMPAT_TO),
	)
	dlg = ErrorAddonInstallDialogWithYesNoButtons(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=pgettext("addonStore", "Install add-on"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon),
		useRememberChoiceCheckbox=useRememberChoiceCheckbox,
	)
	res = displayDialogAsModal(dlg)
	return (res == wx.YES), dlg.shouldRememberChoice()


def _shouldEnableWhenAddonTooOldDialog(
	parent: wx.Window,
	addon: _AddonGUIModel,
	useRememberChoiceCheckbox: bool = False,
) -> tuple[bool, bool]:
	incompatibleMessage = pgettext(
		"addonStore",
		# Translators: The message displayed when enabling an add-on package that is incompatible
		# because the add-on is too old for the running version of NVDA.
		"Warning: add-on is incompatible: {name} {version}. "
		"Check for an updated version of this add-on if possible. "
		"This add-on was last tested with NVDA {lastTestedNVDAVersion}. "
		"NVDA requires this add-on to be tested with NVDA {nvdaVersion} or higher. "
		"Enabling may cause unstable behavior in NVDA.\n"
		"Proceed with enabling anyway? ",
	).format(
		name=addon.displayName,
		version=addon.addonVersionName,
		lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
		nvdaVersion=addonAPIVersion.formatForGUI(addonAPIVersion.BACK_COMPAT_TO),
	)
	dlg = ErrorAddonInstallDialogWithYesNoButtons(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=pgettext("addonStore", "Enable add-on"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon),
		useRememberChoiceCheckbox=useRememberChoiceCheckbox,
	)
	res = displayDialogAsModal(dlg)
	return (res == wx.YES), dlg.shouldRememberChoice()


def _showAddonRequiresNVDAUpdateDialog(
	parent: wx.Window,
	addon: _AddonGUIModel,
) -> None:
	incompatibleMessage = _(
		# Translators: The message displayed when installing an add-on package is prohibited,
		# because it requires a later version of NVDA than is currently installed.
		"Installation of {summary} {version} has been blocked. The minimum NVDA version required for "
		"this add-on is {minimumNVDAVersion}, your current NVDA version is {NVDAVersion}",
	).format(
		summary=addon.displayName,
		version=addon.addonVersionName,
		minimumNVDAVersion=addonAPIVersion.formatForGUI(addon.minimumNVDAVersion),
		NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT),
	)
	displayDialogAsModal(
		ErrorAddonInstallDialog(
			parent=parent,
			# Translators: The title of a dialog presented when an error occurs.
			title=pgettext("addonStore", "Add-on installation failure"),
			message=incompatibleMessage,
			showAddonInfoFunction=lambda: _showAddonInfo(addon),
		),
	)


def _showConfirmAddonInstallDialog(
	parent: wx.Window,
	addon: _AddonGUIModel,
) -> int:
	confirmInstallMessage = _(
		# Translators: A message asking the user if they really wish to install an addon.
		"Are you sure you want to install this add-on?\n"
		"Only install add-ons from trusted sources.\n"
		"Addon: {summary} {version}",
	).format(
		summary=addon.displayName,
		version=addon.addonVersionName,
	)

	return displayDialogAsModal(
		ConfirmAddonInstallDialog(
			parent=parent,
			# Translators: Title for message asking if the user really wishes to install an Addon.
			title=pgettext("addonStore", "Add-on Installation"),
			message=confirmInstallMessage,
			showAddonInfoFunction=lambda: _showAddonInfo(addon),
		),
	)


def _showAddonInfo(addon: _AddonGUIModel) -> None:
	message = [
		pgettext(
			"addonStore",
			# Translators: message shown in the Addon Information dialog.
			"{summary} ({name})\nVersion: {version}\nDescription: {description}\n",
		).format(
			summary=addon.displayName,
			name=addon.addonId,
			version=addon.addonVersionName,
			description=addon.description,
		),
	]
	if isinstance(addon, _AddonStoreModel):
		# Translators: the publisher part of the About Add-on information
		message.append(pgettext("addonStore", "Publisher: {publisher}\n").format(publisher=addon.publisher))
	if isinstance(addon, _AddonManifestModel):
		# Translators: the author part of the About Add-on information
		message.append(pgettext("addonStore", "Author: {author}\n").format(author=addon.author))
	if addon.homepage:
		# Translators: the url part of the About Add-on information
		message.append(pgettext("addonStore", "Homepage: {url}\n").format(url=addon.homepage))
	minimumNVDAVersion = addonAPIVersion.formatForGUI(addon.minimumNVDAVersion)
	message.append(
		# Translators: the minimum NVDA version part of the About Add-on information
		pgettext("addonStore", "Minimum required NVDA version: {}\n").format(minimumNVDAVersion),
	)
	lastTestedNVDAVersion = addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion)
	message.append(
		# Translators: the last NVDA version tested part of the About Add-on information
		pgettext("addonStore", "Last NVDA version tested: {}\n").format(lastTestedNVDAVersion),
	)
	# Translators: title for the Addon Information dialog
	title = pgettext("addonStore", "Add-on Information")
	messageBox("\n".join(message), title, wx.OK)


class _SafetyWarningDialog(
	ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""A dialog warning the user about the risks of installing add-ons."""

	helpId = "AddonStoreInstalling"

	def __init__(self, parent: wx.Window):
		# Translators: The warning of a dialog
		super().__init__(parent, title=pgettext("addonStore", "Add-on Store Warning"))
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = BoxSizerHelper(self, orientation=wx.VERTICAL)

		_warningText = pgettext(
			"addonStore",
			# Translators: Warning that is displayed before using the Add-on Store.
			"Add-ons are created by the NVDA community and are not vetted by NV Access. "
			"NV Access cannot be held responsible for add-on behavior. "
			"The functionality of add-ons is unrestricted and can include "
			"accessing your personal data or even the entire system. ",
		)

		sText = sHelper.addItem(wx.StaticText(self, label=_warningText))
		# the wx.Window must be constructed before we can get the handle.
		self.scaleFactor = windowUtils.getWindowScalingFactor(self.GetHandle())
		sText.Wrap(
			# 600 was fairly arbitrarily chosen by a visual user to look acceptable on their machine.
			self.scaleFactor * 600,
		)

		sHelper.sizer.AddSpacer(SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)

		self.dontShowAgainCheckbox = sHelper.addItem(
			wx.CheckBox(
				self,
				label=pgettext(
					"addonStore",
					# Translators: The label of a checkbox in the add-on store warning dialog
					"&Don't show this message again",
				),
			),
		)

		bHelper = sHelper.addDialogDismissButtons(ButtonHelper(wx.HORIZONTAL))

		# Translators: The label of a button in a dialog
		okButton = bHelper.addButton(self, wx.ID_OK, label=pgettext("addonStore", "&OK"))
		okButton.Bind(wx.EVT_BUTTON, self.onOkButton)

		mainSizer.Add(sHelper.sizer, border=BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onOkButton(self, evt: wx.CommandEvent):
		addonDataManager.storeSettings.showWarning = not self.dontShowAgainCheckbox.GetValue()
		self.EndModal(wx.ID_OK)


class UpdatableAddonsDialog(
	ContextHelpMixin,
	wx.Dialog,  # wxPython does not seem to call base class initializer, put last in MRO
):
	"""A dialog notifying users that updatable add-ons are available"""

	helpId = "AutomaticAddonUpdates"
	onDisplayableError = DisplayableError.OnDisplayableErrorT()

	def __init__(self, parent: wx.Window, addonsPendingUpdate: list[_AddonGUIModel]):
		# Translators: The warning of a dialog
		super().__init__(parent, title=pgettext("addonStore", "Add-on updates available"))
		self.addonsPendingUpdate = addonsPendingUpdate
		self._setupUI()
		self.Raise()
		self.SetFocus()

	def _setupUI(self):
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = BoxSizerHelper(self, orientation=wx.VERTICAL)
		self._setupMessage(sHelper)
		self._createAddonsPanel(sHelper)
		self._setupButtons(sHelper)
		mainSizer.Add(sHelper.sizer, border=BORDER_FOR_DIALOGS, flag=wx.ALL)
		self.Sizer = mainSizer
		mainSizer.Fit(self)
		self.CentreOnScreen()

	def onCharHook(self, evt: wx.KeyEvent):
		if evt.KeyCode == wx.WXK_ESCAPE:
			self.Close()
		evt.Skip()

	def _setupMessage(self, sHelper: BoxSizerHelper):
		_message = pgettext(
			"addonStore",
			# Translators: Message displayed when updates are available for some installed add-ons.
			"Updates are available for some of your installed add-ons. ",
		)

		sText = sHelper.addItem(wx.StaticText(self, label=_message))
		# the wx.Window must be constructed before we can get the handle.
		self.scaleFactor = windowUtils.getWindowScalingFactor(self.GetHandle())
		# 600 was fairly arbitrarily chosen by a visual user to look acceptable on their machine.
		sText.Wrap(self.scaleFactor * 600)

	def _setupButtons(self, sHelper: BoxSizerHelper):
		bHelper = sHelper.addDialogDismissButtons(ButtonHelper(wx.HORIZONTAL))

		# Translators: The label of a button in a dialog
		openStoreLabel = pgettext("addonStore", "Open Add-on &Store")
		self.openStoreButton = bHelper.addButton(self, wx.ID_CLOSE, label=openStoreLabel)
		self.openStoreButton.Bind(wx.EVT_BUTTON, self.onOpenStoreButton)

		self.updateAllButton = bHelper.addButton(
			self,
			wx.ID_CLOSE,
			# Translators: The label of a button in a dialog
			label=pgettext("addonStore", "&Update all"),
		)
		self.updateAllButton.Bind(wx.EVT_BUTTON, self.onUpdateAllButton)

		# Translators: The label of a button in a dialog
		closeButton = bHelper.addButton(self, wx.ID_CLOSE, label=pgettext("addonStore", "&Close"))
		closeButton.Bind(wx.EVT_BUTTON, self.onCloseButton)

	def _createAddonsPanel(self, sHelper: BoxSizerHelper):
		# Translators: the label for the addons list in the updatable addons dialog.
		entriesLabel = pgettext("addonStore", "Updatable Add-ons")
		self.addonsList = sHelper.addLabeledControl(
			entriesLabel,
			nvdaControls.AutoWidthColumnListCtrl,
			style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
		)

		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
		nameLabel = pgettext("addonStore", "Name")
		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
		installedVersionLabel = pgettext("addonStore", "Installed version")
		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
		availableVersionLabel = pgettext("addonStore", "Available version")
		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
		channelLabel = pgettext("addonStore", "Channel")
		# Translators: Label for an extra detail field for an add-on. In the add-on store UX.
		statusLabel = pgettext("addonStore", "Status")

		self.addonsList.AppendColumn(nameLabel, width=300)
		self.addonsList.AppendColumn(installedVersionLabel, width=200)
		self.addonsList.AppendColumn(availableVersionLabel, width=200)
		self.addonsList.AppendColumn(channelLabel, width=150)
		self.addonsList.AppendColumn(statusLabel, width=300)
		for addon in self.addonsPendingUpdate:
			self.addonsList.Append(
				(
					addon.displayName,
					addon._addonHandlerModel.version,
					addon.addonVersionName,
					addon.channel.displayString,
					AvailableAddonStatus.UPDATE.displayString,
				),
			)
		self.addonsList.Refresh()

	def onOpenStoreButton(self, evt: wx.CommandEvent):
		"""Open the Add-on Store to update add-ons"""
		# call later so current dialog is dismissed and doesn't block the store from opening
		wx.CallLater(100, gui.mainFrame.onAddonStoreUpdatableCommand, None)
		self.EndModal(wx.ID_CLOSE)

	def onUpdateAllButton(self, evt: wx.CommandEvent):
		from gui.addonStoreGui.viewModels.store import AddonStoreVM

		self.updateAllButton.Disable()
		self.openStoreButton.Disable()

		self.listItemVMs: list[AddonListItemVM] = []
		for addon in self.addonsPendingUpdate:
			listItemVM = AddonListItemVM(addon, status=getStatus(addon, _StatusFilterKey.UPDATE))
			listItemVM.updated.register(self._statusUpdate)
			self.listItemVMs.append(listItemVM)
		AddonStoreVM.getAddons(self.listItemVMs)
		self.addonsList.Refresh()
		# Translators: Message shown when updating add-ons in the updatable add-ons dialog
		ui.message(pgettext("addonStore", "Updating add-ons..."))
		self.addonsList.SetFocus()
		self.addonsList.Focus(0)

	def _statusUpdate(self, addonListItemVM: AddonListItemVM):
		log.debug(f"{addonListItemVM.Id} status: {addonListItemVM.status}")
		index = self.listItemVMs.index(addonListItemVM)
		self.addonsList.SetItem(index, column=4, label=addonListItemVM.status.displayString)

	def onCloseButton(self, evt: wx.CommandEvent):
		self.Close()

	def onClose(self, evt: wx.CloseEvent):
		from gui.addonStoreGui.viewModels.store import AddonStoreVM
		from .storeDialog import AddonStoreDialog

		evt.Veto()

		numInProgress = len(AddonStoreVM._downloader.progress)
		if numInProgress:
			res = gui.messageBox(
				npgettext(
					"addonStore",
					# Translators: Message shown prior to installing add-ons when closing the add-on store dialog
					# The placeholder {} will be replaced with the number of add-ons to be installed
					"Download of {} add-on in progress, cancel downloading?",
					"Download of {} add-ons in progress, cancel downloading?",
					numInProgress,
				).format(numInProgress),
				AddonStoreDialog._installationPromptTitle,
				style=wx.YES_NO,
			)
			if res == wx.YES:
				log.debug("Cancelling the download.")
				AddonStoreVM.cancelDownloads()
				# Continue to installation if any downloads completed
			else:
				# Let the user return to the dialog and inspect add-ons being downloaded.
				return

		if addonDataManager._downloadsPendingInstall:
			nAddonsPendingInstall = len(addonDataManager._downloadsPendingInstall)
			installingDialog = gui.IndeterminateProgressDialog(
				self,
				AddonStoreDialog._installationPromptTitle,
				npgettext(
					"addonStore",
					# Translators: Message shown while installing add-ons after closing the add-on store dialog
					# The placeholder {} will be replaced with the number of add-ons to be installed
					"Installing {} add-on, please wait.",
					"Installing {} add-ons, please wait.",
					nAddonsPendingInstall,
				).format(nAddonsPendingInstall),
			)
			AddonStoreVM.installPending()

			def postInstall():
				installingDialog.done()
				# let the dialog exit.
				self.DestroyLater()
				self.SetReturnCode(wx.ID_CLOSE)
				wx.CallLater(500, promptUserForRestart)

			return wx.CallAfter(postInstall)

		# let the dialog exit.
		self.DestroyLater()
		self.SetReturnCode(wx.ID_CLOSE)

	@staticmethod
	def handleDisplayableError(displayableError: DisplayableError):
		# Fail silently as we don't care if we can't fetch an update.
		log.exception("Error occurred while checking for updatable add-ons", exc_info=displayableError)

	@classmethod
	def _checkForUpdatableAddons(cls):
		if not NVDAState.shouldWriteToDisk() or (
			AddonsAutomaticUpdate.DISABLED == config.conf["addonStore"]["automaticUpdates"]
		):
			log.debug("automatic add-on updates are disabled")
			return
		log.debug("checking for updatable add-ons")

		UpdatableAddonsDialog.onDisplayableError.register(UpdatableAddonsDialog.handleDisplayableError)
		addonsPendingUpdate = addonDataManager._addonsPendingUpdate(UpdatableAddonsDialog.onDisplayableError)
		UpdatableAddonsDialog.onDisplayableError.unregister(UpdatableAddonsDialog.handleDisplayableError)

		if not addonsPendingUpdate:
			log.debug("no updatable add-ons found")
			return

		log.debug("updatable add-ons found")

		match config.conf["addonStore"]["automaticUpdates"]:
			case AddonsAutomaticUpdate.NOTIFY:

				def delayCreateDialog():
					winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
					displayDialogAsModal(cls(gui.mainFrame, addonsPendingUpdate))

				wx.CallAfter(delayCreateDialog)

			case AddonsAutomaticUpdate.UPDATE:
				threading.Thread(
					name="AutomaticAddonUpdate",
					target=_updateAddons,
					args=(addonsPendingUpdate,),
					daemon=True,
				).start()

			case _:
				raise NotImplementedError("Unknown automatic update setting")


@_countAsMessageBox()
def _updateAddons(addonsPendingUpdate: list[_AddonGUIModel]):
	"""Update the add-ons in the background.
	Blocks while downloading occurs.
	This function is treated as message box to prevent NVDA from exiting while the download/install is in progress.
	"""
	from ..viewModels.store import AddonStoreVM

	# Translators: Message shown when updating add-ons automatically
	ui.message(pgettext("addonStore", "Updating add-ons..."), SpeechPriority.NEXT)
	listVMs = {AddonListItemVM(a, status=getStatus(a, _StatusFilterKey.UPDATE)) for a in addonsPendingUpdate}
	AddonStoreVM.getAddons(
		listVMs,
		shouldReplace=True,
		shouldInstallIncompatible=True,
		shouldRememberReplaceChoice=True,
		shouldRememberInstallChoice=True,
	)

	while AddonStoreVM._downloader.progress:
		log.debug(f"Waiting for add-ons to be downloaded {AddonStoreVM._downloader.progress}")
		sleep(0.1)

	def mainThreadCallback():
		# Add-on installations must happen on main thread
		AddonStoreVM.installPending()
		ui.message(
			# Translators: Message shown when updating add-ons automatically
			pgettext("addonStore", "Add-ons updated, restart NVDA to activate changes"),
			SpeechPriority.NEXT,
		)

	wx.CallAfter(mainThreadCallback)
