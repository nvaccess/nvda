# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
from _localCaptioner.modelDownloader import ModelDownloader
import threading
import wx


def onDownload() -> None:
	modelDownloader = ModelDownloader()
	(success, fail) = modelDownloader.downloadModelsMultithreaded()
	if success:
		wx.CallAfter(openSuccessDialog)
	else:
		wx.CallAfter(openFailDialog)


def openSuccessDialog() -> None:
	confirmation_button = (DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=True),)

	dialog = MessageDialog(
		parent=None,
		# Translators: title of dialog when download successfully
		title=pgettext("imageDesc", "Download successfully"),
		message=pgettext(
			"imageDesc",
			# Translators: label of dialog when downloading image captioning
			"Image captioning installed successfully.",
		),
		dialogType=DialogType.STANDARD,
		buttons=confirmation_button,
	)

	if dialog.ShowModal() == ReturnCode.YES:
		pass


def openFailDialog() -> None:
	confirmation_buttons = (
		DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=True),
		DefaultButton.NO,
	)

	dialog = MessageDialog(
		parent=None,
		# Translators: title of dialog when fail to download
		title=pgettext("imageDesc", "Download failed"),
		message=pgettext(
			"imageDesc",
			# Translators: label of dialog when fail to download image captioning
			"Image captioning download failed. Would you like to retry?",
		),
		dialogType=DialogType.WARNING,
		buttons=confirmation_buttons,
	)

	if dialog.ShowModal() == ReturnCode.YES:
		threading.Thread(target=onDownload).start()


def openDownloadDialog() -> None:
	confirmation_buttons = (
		DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=True),
		DefaultButton.NO,
	)

	dialog = MessageDialog(
		parent=None,
		# Translators: title of dialog when downloading Image captioning
		title=pgettext("imageDesc", "Confirm download"),
		message=pgettext(
			"imageDesc",
			# Translators: label of dialog when downloading image captioning
			"Image captioning not installed. Would you like to install (235 MB)?",
		),
		dialogType=DialogType.WARNING,
		buttons=confirmation_buttons,
	)

	if dialog.ShowModal() == ReturnCode.YES:
		threading.Thread(target=onDownload).start()
