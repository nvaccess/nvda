# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from typing import (
	TYPE_CHECKING,
)

import wx

import addonAPIVersion
from addonStore.models import AddonDetailsModel
from gui.addonGui import ErrorAddonInstallDialog
from gui.message import messageBox

if TYPE_CHECKING:
	from addonHandler import SupportsVersionCheck
	from guiHelper import ButtonHelper


class ErrorAddonInstallDialogWithCancelButton(ErrorAddonInstallDialog):
	def _addButtons(self, buttonHelper: "ButtonHelper") -> None:
		super()._addButtons(buttonHelper)
		cancelButton = buttonHelper.addButton(
			self,
			id=wx.ID_CANCEL,
			# Translators: A button in the addon installation blocked dialog which will dismiss the dialog.
			label=_("Cancel")
		)
		cancelButton.SetDefault()
		cancelButton.Bind(wx.EVT_BUTTON, lambda evt: self.EndModal(wx.CANCEL))


def _shouldProceedWhenInstalledAddonVersionUnknown(
		parent: wx.Window,
		addon: AddonDetailsModel
) -> bool:
	incompatibleMessage = _(
		# Translators: The message displayed when installing an incompatible add-on package,
		# because it requires a new version than is currently installed.
		"Warning: add-on installation may result in downgrade: {name}. "
		"The installed add-on version cannot be compared with the add-on store version. "
		"Installed version: {oldVersion}. "
		"Available version: {version}. "
		"Proceed with installation anyway? "
		).format(
	name=addon.displayName,
	version=addon.addonVersionName,
	oldVersion=addon._addonHandlerModel.version,
	lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
	NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
	)
	return ErrorAddonInstallDialogWithCancelButton(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=_("Add-on not compatible"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon)
	).ShowModal() == wx.OK


def _shouldProceedToRemoveAddonDialog(
		addon: "SupportsVersionCheck"
) -> bool:
	return messageBox(
		(_(
			# Translators: Presented when attempting to remove the selected add-on.
			# {addon} is replaced with the add-on name.
			"Are you sure you wish to remove the {addon} add-on from NVDA? "
			"This cannot be undone."
		)).format(addon=addon.name),
		# Translators: Title for message asking if the user really wishes to remove the selected Addon.
		_("Remove Add-on"),
		wx.YES_NO | wx.NO_DEFAULT | wx.ICON_WARNING
	) == wx.YES


def _shouldProceedWhenAddonTooOldDialog(
		parent: wx.Window,
		addon: AddonDetailsModel
) -> bool:
	incompatibleMessage = _(
		# Translators: The message displayed when installing an incompatible add-on package,
		# because it requires a new version than is currently installed.
		"Warning: add-on is incompatible: {name} {version}. "
		"Check for an updated version of this add-on if possible. "
		"The last tested NVDA version for this add-on is {lastTestedNVDAVersion}, "
		"your current NVDA version is {NVDAVersion}. "
		"Installation may cause unstable behavior in NVDA. "
		"Proceed with installation anyway? "
		).format(
	name=addon.displayName,
	version=addon.addonVersionName,
	lastTestedNVDAVersion=addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion),
	NVDAVersion=addonAPIVersion.formatForGUI(addonAPIVersion.CURRENT)
	)
	return ErrorAddonInstallDialogWithCancelButton(
		parent=parent,
		# Translators: The title of a dialog presented when an error occurs.
		title=_("Add-on not compatible"),
		message=incompatibleMessage,
		showAddonInfoFunction=lambda: _showAddonInfo(addon)
	).ShowModal() == wx.OK


def _showAddonInfo(addon: AddonDetailsModel) -> None:
	message = [
		_(
			# Translators: message shown in the Addon Information dialog.
			"{summary} ({name})\n"
			"Version: {version}\n"
			"Publisher: {publisher}\n"
			"Description: {description}\n"
			).format(
		summary=addon.displayName,
		name=addon.addonId,
		version=addon.addonVersionName,
		publisher=addon.publisher,
		description=addon.description,
		)
	]
	if addon.homepage:
		# Translators: the url part of the About Add-on information
		message.append(_("Homepage: {url}").format(url=addon.homepage))
	minimumNVDAVersion = addonAPIVersion.formatForGUI(addon.minimumNVDAVersion)
	message.append(
		# Translators: the minimum NVDA version part of the About Add-on information
		_("Minimum required NVDA version: {}").format(minimumNVDAVersion)
	)
	lastTestedNVDAVersion = addonAPIVersion.formatForGUI(addon.lastTestedNVDAVersion)
	message.append(
		# Translators: the last NVDA version tested part of the About Add-on information
		_("Last NVDA version tested: {}").format(lastTestedNVDAVersion)
	)
	# Translators: title for the Addon Information dialog
	title = _("Add-on Information")
	messageBox("\n".join(message), title, wx.OK)
