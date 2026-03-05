# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2026 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from collections.abc import Collection
import threading
from time import sleep
from typing import (
	TYPE_CHECKING,
	Self,
)
import weakref
import winsound

import wx

import addonAPIVersion

from addonHandler import Addon, getAvailableAddons
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
from gui.addonGui import ConfirmAddonInstallDialog, ErrorAddonInstallDialog, promptUserForRestart
from gui.addonStoreGui.viewModels.addonList import AddonListItemVM
from gui.contextHelp import ContextHelpMixin
from gui.dpiScalingHelper import DpiScalingHelperMixinWithoutInit
from gui.guiHelper import (
	BoxSizerHelper,
	BORDER_FOR_DIALOGS,
	ButtonHelper,
	SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS,
)
from gui.message import DisplayableError, displayDialogAsModal, messageBox, _countAsMessageBox
from gui.nvdaControls import AutoWidthColumnListCtrl
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
		self.CenterOnScreen()

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
		from .actions import _MonoActionsContextMenu
		from .addonList import AddonVirtualList
		from gui.addonStoreGui.viewModels.store import AddonStoreVM

		_storeVM = AddonStoreVM()
		_storeVM._filteredStatusKey = _StatusFilterKey.UPDATE
		_storeVM._filterIncludeIncompatible = config.conf["addonStore"]["allowIncompatibleUpdates"]
		_storeVM.refresh()
		self.addonsList = AddonVirtualList(
			parent=self,
			addonsListVM=_storeVM.listVM,
			actionsContextMenu=_MonoActionsContextMenu(_storeVM),
		)
		self.addonsList.SetMinSize(self.addonsList.scaleSize((500, 100)))
		self.SetMinSize(self.addonsList.scaleSize((500, 100)))
		self.addonsList.Refresh()
		sHelper.addItem(self.addonsList, proportion=1)

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
				AddonStoreDialog._cancelInstallationPromptMsg(numInProgress),
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
				AddonStoreDialog._installationPromptMsg(nAddonsPendingInstall),
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
				# Translators: Message shown when updating add-ons automatically
				wx.CallAfter(ui.message, pgettext("addonStore", "Updating add-ons..."), SpeechPriority.NEXT)
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


class _CopyAddonsDialog(
	DpiScalingHelperMixinWithoutInit,
	ContextHelpMixin,
	wx.Dialog,
):
	"""A dialog which asks the user which add-ons they would like to copy to the system profile."""

	helpId = "CopyAddonsToSystemProfileDialog"

	@classmethod
	def _instance(cls) -> Self | None:
		"""Retrieves the globally unique instance of this class, if any."""
		# Return None until this is replaced with a weakref.ref object.
		# Then the instance is retrieved by treating that object as a callable.
		return None

	def __new__(cls, *args, **kwargs):
		instance = cls._instance()
		if instance is None:
			return super().__new__(cls, *args, **kwargs)
		return instance

	def __init__(self, parent: wx.Window, availableAddons: Collection[Addon], returnList: list[str]):
		"""Initializer.

		:param parent: The dialog's parent window.
		:param availableAddons: The add-ons that are available to be copied to the system profile.
			This must not be empty.
		:param returnList: A list that will be modified in place with the add-on IDs that the user wishes to copy.
		:raises RuntimeError: If an instance of this class already exists.
		:raises ValueError: If ``availableAddons`` is empty.
		"""
		if type(self)._instance() is not None:
			raise RuntimeError("Attempting to open multiple _CopyAddonsDialog instances")
		if len(availableAddons) < 1:
			raise ValueError("Unable to show copy add-ons dialog when there are no add-ons to copy.")
		type(self)._instance = weakref.ref(self)
		super().__init__(
			parent,
			wx.ID_ANY,
			# Translators: The title of the dialog which allows users to select which add-ons to copy to the system profile.
			pgettext("addonStore", "Copy Add-ons to System-wide Configuration"),
		)
		self._availableAddons = availableAddons
		self._returnList = returnList

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = BoxSizerHelper(self, wx.VERTICAL)

		label = wx.StaticText(
			self,
			label=pgettext(
				"addonStore",
				# Translators: Explanatory text in the dialog which allows users to select which add-ons to copy to NVDA's system config.
				"One or more add-ons are currently enabled in your NVDA configuration. "
				"If run on secure screens, they will have unrestricted, higher-than-administrator level access to your entire system. "
				"You are strongly encouraged to copy only add-ons that you absolutely require in order to use NVDA during sign-in and on secure screens."
				"\n\n"
				"Check only the add-ons you wish to copy to the system-wide configuration.",
			),
		)
		label.Wrap(self.scaleSize(self.GetSize().Width))
		sHelper.addItem(label)

		listCtrl = self._addonsList = sHelper.addLabeledControl(
			# Translators: The label of the list which allows users to select which add-ons to copy to the system profile
			pgettext("addonStore", "Add-ons"),
			AutoWidthColumnListCtrl,
			style=wx.LC_REPORT | wx.LC_SINGLE_SEL,
		)
		listCtrl.setResizeColumn(0)
		# Translators: The label for a column in the copy add-ons dialog that displays the name of the add-on
		listCtrl.AppendColumn(pgettext("addonStore", "Name"), width=self.scaleSize(150))
		# Translators: The label for a column in the copy add-ons dialog that displays the add-on's author
		listCtrl.AppendColumn(pgettext("addonStore", "Author"), width=self.scaleSize(180))
		# Translators: The label for a column in the copy add-ons dialog that displays the version of the add-on
		listCtrl.AppendColumn(pgettext("addonStore", "Version"), width=self.scaleSize(150))
		listCtrl.EnableCheckBoxes(True)
		listCtrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self._onSelectionChange)
		listCtrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self._onSelectionChange)
		listCtrl.Bind(wx.EVT_CHAR_HOOK, self._enterActivatesContinue)

		buttonHelper = ButtonHelper(wx.HORIZONTAL)
		# Translators: The label for a button in the copy add-ons dialog to show information about the selected add-on.
		button = self._aboutButton = buttonHelper.addButton(
			self,
			label=pgettext("addonStore", "&About add-on..."),
		)
		button.Disable()
		button.Bind(wx.EVT_BUTTON, self.onAbout)
		# Translators: The label for a button in the copy add-ons dialog which will initiate the copy process
		button = buttonHelper.addButton(self, label=pgettext("addonStore", "&Continue"), id=wx.ID_OK)
		button.SetDefault()
		# Translators: The label for a button in the copy add-ons dialog which will abandon the copy process
		buttonHelper.addButton(self, label=pgettext("addonStore", "Cancel"), id=wx.ID_CANCEL)
		self.Bind(wx.EVT_BUTTON, self.onContinue, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		sHelper.addDialogDismissButtons(buttonHelper, separated=True)
		self._populateAddonsList()

		mainSizer.Add(
			sHelper.sizer,
			border=BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND,
			proportion=1,
		)
		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.CentreOnParent()

	def _populateAddonsList(self):
		self._addonsList.DeleteAllItems()
		for idx, addon in enumerate(self._availableAddons):
			self._addonsList.Append(
				(
					addon.manifest["summary"],
					addon.manifest["author"],
					addon.version,
				),
			)
		activeIndex = 0
		self._addonsList.SetItemState(
			activeIndex,
			wx.LIST_STATE_FOCUSED | wx.LIST_STATE_SELECTED,
			wx.LIST_STATE_FOCUSED | wx.LIST_STATE_SELECTED,
		)

	def _onSelectionChange(self, evt: wx.ListEvent):
		self._aboutButton.Enable(self._addonsList.GetSelectedItemCount() == 1)

	def _enterActivatesContinue(self, evt: wx.KeyEvent):
		if evt.KeyCode in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.ProcessEvent(wx.CommandEvent(wx.wxEVT_COMMAND_BUTTON_CLICKED, wx.ID_OK))
		else:
			evt.Skip()

	def onAbout(self, evt: wx.EVT_BUTTON):
		index: int = self._addonsList.GetFirstSelected()
		if index < 0:
			return
		_showAddonInfo(self._availableAddons[index]._addonGuiModel)

	def onClose(self, evt: wx.CloseEvent):
		if not self.GetReturnCode():
			self.SetReturnCode(wx.ID_CANCEL)
		self.DestroyLater()  # ensure that the _instance weakref is destroyed.

	def onCancel(self, evt: wx.CommandEvent):
		self.EndModal(evt.GetId())
		self.Close()

	def onContinue(self, evt: wx.CommandEvent):
		returnCode = evt.GetId()
		toCopy = tuple(
			addon.name
			for idx, addon in enumerate(self._availableAddons)
			if self._addonsList.IsItemChecked(idx)
		)
		if toCopy:
			match gui.messageBox(
				npgettext(
					"addonStore",
					# Translators: A message to warn the user when attempting to copy add-ons for use on secure screens
					"You have selected to copy {num} add-on to NVDA's system-wide configuration. "
					"Using this add-on during sign-in and on secure screens is a serious security risk.",
					"You have selected to copy {num} add-ons to NVDA's system-wide configuration. "
					"Using these add-ons during sign-in and on secure screens is a serious security risk.",
					len(toCopy),
				).format(num=len(toCopy))
				+ "\n\n"
				+ pgettext(
					"addonStore",
					# Translators: A prompt asking the user to confirm whether to perform an action.
					"Are you sure you want to continue?",
				),
				# Translators: The title of the warning dialog displayed when trying to
				# copy add-ons for use on secure screens.
				pgettext("addonStore", "Warning"),
				wx.YES | wx.NO | wx.CANCEL | wx.NO_DEFAULT | wx.ICON_WARNING,
				self,
			):
				case wx.CANCEL:
					returnCode = wx.CANCEL
				case wx.YES:
					self._returnList.extend(toCopy)
				case _:
					return
		self.EndModal(returnCode)
		self.Close()


def _getAddonsToCopy(parent: wx.Window) -> list[str] | None:
	"""Get a list of add-on IDs to copy to the system profile.

	This function asks the user which add-ons they want to copy to the system profile, and returns the add-on IDs of those they select.
	If no add-ons are enabled, the user is not asked, and no add-on IDs are returned.

	.. warning::
		This function is blocking.

	:param parent: The window to use as the dialog's parent.
	:return: If the user cancels the process, ``None``.
		Otherwise, a list of add-on IDs to copy.
		Note that this list may be empty, in which case there are either no enabled add-ons in the user config, or the user has chosen to copy no add-ons.
	"""
	addonsToCopy: list[str] = []
	enabledAddons: tuple[Addon] = tuple(
		getAvailableAddons(
			filterFunc=lambda addon: getStatus(addon._addonGuiModel, _StatusFilterKey.INSTALLED)
			in (
				AvailableAddonStatus.ENABLED,
				AvailableAddonStatus.RUNNING,
				AvailableAddonStatus.INCOMPATIBLE_ENABLED,
			),
		),
	)
	if (
		len(enabledAddons) > 0
		and _CopyAddonsDialog(parent, enabledAddons, addonsToCopy).ShowModal() != wx.ID_OK
	):
		return None
	return addonsToCopy
