# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
from _localCaptioner.modelDownloader import ModelDownloader

def openDownloadDialog() -> None:
	confirmation_buttons = (
		DefaultButton.YES,
		DefaultButton.NO.value._replace(defaultFocus=True, fallbackAction=True),
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
		downloader = ModelDownloader()
		threading.Thread(target=downloader.downloadModelsMultithreaded).start()
