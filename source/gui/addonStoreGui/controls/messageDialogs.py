# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023-2024 NV Access Limited, Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	TYPE_CHECKING,
)

import wx

import addonAPIVersion
from addonStore.models.addon import (
	_AddonGUIModel,
	_AddonStoreModel,
	_AddonManifestModel,
)
import config
from gui.addonGui import ConfirmAddonInstallDialog, ErrorAddonInstallDialog
from gui.contextHelp import ContextHelpMixin
from gui.guiHelper import (
	BoxSizerHelper,
	BORDER_FOR_DIALOGS,
	ButtonHelper,
	SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS,
)
from gui.message import displayDialogAsModal, messageBox
import windowUtils

if TYPE_CHECKING:
	from addonStore.models.version import SupportsVersionCheck


class ErrorAddonInstallDialogWithYesNoButtons(ErrorAddonInstallDialog):
	def __init__(self, *args, useRememberChoiceCheckbox: bool = False, **kwargs):
		self.useRememberChoiceCheckbox = useRememberChoiceCheckbox
		super().__init__(*args, **kwargs)

	def _addButtons(self, buttonHelper: ButtonHelper) -> None:
		addonInfoButton = buttonHelper.addButton(
			self,
			# Translators: A button in the addon installation warning / blocked dialog which shows
			# more information about the addon
			label=pgettext("addonStore", "&About add-on...")
		)
		addonInfoButton.Bind(wx.EVT_BUTTON, lambda evt: self._showAddonInfoFunction())

		yesButton = buttonHelper.addButton(
			self,
			id=wx.ID_YES,
			# Translators: A button in the addon installation blocked dialog which will confirm the available action.
			label=pgettext("addonStore", "&Yes")
		)
		yesButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.YES))

		noButton = buttonHelper.addButton(
			self,
			id=wx.ID_NO,
			# Translators: A button in the addon installation blocked dialog which will dismiss the dialog.
			label=pgettext("addonStore", "&No")
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
		"Proceed with installation anyway? "
		).format(
	name=addon.displayName,
	version=addon.addonVersionName,
	oldVersion=addon._addonHandlerModel.version,
	lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
	NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
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
		"Are you sure you wish to remove the {addon} add-on from NVDA? "
		"This cannot be undone."
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
		"The last tested NVDA version for this add-on is {lastTestedNVDAVersion}, "
		"your current NVDA version is {NVDAVersion}. "
		"Installation may cause unstable behavior in NVDA.\n"
		"Proceed with installation anyway? "
		).format(
	name=addon.displayName,
	version=addon.addonVersionName,
	lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
	NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
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
		"The last tested NVDA version for this add-on is {lastTestedNVDAVersion}, "
		"your current NVDA version is {NVDAVersion}. "
		"Enabling may cause unstable behavior in NVDA.\n"
		"Proceed with enabling anyway? "
		).format(
	name=addon.displayName,
	version=addon.addonVersionName,
	lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
	NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
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
		addon: _AddonGUIModel
) -> None:
	incompatibleMessage = _(
		# Translators: The message displayed when installing an add-on package is prohibited,
		# because it requires a later version of NVDA than is currently installed.
		"Installation of {summary} {version} has been blocked. The minimum NVDA version required for "
		"this add-on is {minimumNVDAVersion}, your current NVDA version is {NVDAVersion}"
		).format(
	summary=addon.displayName,
	version=addon.addonVersionName,
	minimumNVDAVersion=addonAPIVersion.formatForGUI(addon.minimumNVDAVersion),
	NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
	)
	displayDialogAsModal(ErrorAddonInstallDialog(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=pgettext("addonStore", "Add-on installation failure"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon)
	))


def _showConfirmAddonInstallDialog(
		parent: wx.Window,
		addon: _AddonGUIModel
) -> int:
	confirmInstallMessage = _(
		# Translators: A message asking the user if they really wish to install an addon.
		"Are you sure you want to install this add-on?\n"
		"Only install add-ons from trusted sources.\n"
		"Addon: {summary} {version}"
		).format(
	summary=addon.displayName,
	version=addon.addonVersionName,
	)

	return displayDialogAsModal(ConfirmAddonInstallDialog(
		parent=parent,
		# Translators: Title for message asking if the user really wishes to install an Addon.
		title=_("Add-on Installation"),
		message=confirmInstallMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon)
	))



def _showAddonInfo(addon: _AddonGUIModel) -> None:
	message = [
		pgettext(
			"addonStore",
			# Translators: message shown in the Addon Information dialog.
			"{summary} ({name})\n"
			"Version: {version}\n"
			"Description: {description}\n"
			).format(
		summary=addon.displayName,
		name=addon.addonId,
		version=addon.addonVersionName,
		description=addon.description,
		)
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
		pgettext("addonStore", "Minimum required NVDA version: {}\n").format(minimumNVDAVersion)
	)
	lastTestedNVDAVersion = addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion)
	message.append(
		# Translators: the last NVDA version tested part of the About Add-on information
		pgettext("addonStore", "Last NVDA version tested: {}\n").format(lastTestedNVDAVersion)
	)
	# Translators: title for the Addon Information dialog
	title = pgettext("addonStore", "Add-on Information")
	messageBox("\n".join(message), title, wx.OK)


class _SafetyWarningDialog(
		ContextHelpMixin,
		wx.Dialog   # wxPython does not seem to call base class initializer, put last in MRO
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
			"accessing your personal data or even the entire system. "
		)

		sText = sHelper.addItem(wx.StaticText(self, label=_warningText))
		# the wx.Window must be constructed before we can get the handle.
		self.scaleFactor = windowUtils.getWindowScalingFactor(self.GetHandle())
		sText.Wrap(
			# 600 was fairly arbitrarily chosen by a visual user to look acceptable on their machine.
			self.scaleFactor * 600
		)

		sHelper.sizer.AddSpacer(SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)

		self.dontShowAgainCheckbox = sHelper.addItem(
			wx.CheckBox(
				self,
				label=pgettext(
					"addonStore",
					# Translators: The label of a checkbox in the add-on store warning dialog
					"&Don't show this message again"
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
		config.conf["addonStore"]["showWarning"] = not self.dontShowAgainCheckbox.GetValue()
		self.EndModal(wx.ID_OK)
