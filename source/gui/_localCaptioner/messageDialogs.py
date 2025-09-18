# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
from _localCaptioner.modelDownloader import ModelDownloader
import threading
from threading import Thread
import wx
import ui

_downloadThread: Thread | None = None


def onDownload() -> None:
	modelDownloader = ModelDownloader()
	(success, fail) = modelDownloader.downloadModelsMultithreaded()
	if success:
		wx.CallAfter(openSuccessDialog)
	else:
		wx.CallAfter(openFailDialog)


def openSuccessDialog() -> None:
	confirmationButton = (DefaultButton.OK.value._replace(defaultFocus=True, fallbackAction=True),)

	dialog = MessageDialog(
		parent=None,
		# Translators: title of dialog when download successfully
		title=pgettext("imageDesc", "Download successful"),
		message=pgettext(
			"imageDesc",
			# Translators: label of dialog when downloading image captioning
			"Image captioning installed successfully.",
		),
		dialogType=DialogType.STANDARD,
		buttons=confirmationButton,
	)

	if dialog.ShowModal() == ReturnCode.OK:
		# load image desc after successful download
		import _localCaptioner		
		
		if not _localCaptioner.isModelLoaded():
			_localCaptioner.toggleImageCaptioning()



def openFailDialog() -> None:
	confirmationButtons = (
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
		buttons=confirmationButtons,
	)

	if dialog.ShowModal() == ReturnCode.YES:
		global _downloadThread
		_downloadThread = threading.Thread(target=onDownload, name="ModelDownloadMainThread", daemon=False)
		_downloadThread.start()


def openDownloadDialog() -> None:
	global _downloadThread
	if _downloadThread is not None and _downloadThread.is_alive():
		# Translators: message when image captioning is still downloading
		ui.message(pgettext("imageDesc", "image captioning is still downloading, please wait..."))
		return

	confirmationButtons = (
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
		buttons=confirmationButtons,
	)

	if dialog.ShowModal() == ReturnCode.YES:
		_downloadThread = threading.Thread(target=onDownload, name="ModelDownloadMainThread", daemon=False)
		_downloadThread.start()
