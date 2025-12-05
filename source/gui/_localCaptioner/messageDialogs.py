# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from gui.message import MessageDialog, DefaultButton, ReturnCode, DialogType
import gui
from _localCaptioner.modelDownloader import ModelDownloader, ProgressCallback
import threading
from threading import Thread
import wx
import ui
import _localCaptioner


class ImageDescDownloader:
	_downloadThread: Thread | None = None
	isOpening: bool = False

	def __init__(self):
		self.downloadDict: dict[str, tuple[int, int]] = {}
		self.modelDownloader: ModelDownloader | None = None
		self._shouldCancel = False
		self._progressDialog: wx.ProgressDialog | None = None
		self.filesToDownload = [
			"onnx/encoder_model_quantized.onnx",
			"onnx/decoder_model_merged_quantized.onnx",
			"config.json",
			"vocab.json",
			"preprocessor_config.json",
		]

	def onDownload(self, progressCallback: ProgressCallback) -> None:
		self.modelDownloader = ModelDownloader()
		(success, fail) = self.modelDownloader.downloadModelsMultithreaded(
			filesToDownload=self.filesToDownload,
			progressCallback=progressCallback,
		)
		if len(fail) == 0:
			wx.CallAfter(self.openSuccessDialog)
		else:
			wx.CallAfter(self.openFailDialog)

	def openSuccessDialog(self) -> None:
		confirmationButton = (DefaultButton.OK.value._replace(defaultFocus=True, fallbackAction=True),)
		self._stopped()

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
			if not _localCaptioner.isModelLoaded():
				_localCaptioner.toggleImageCaptioning()

	def openFailDialog(self) -> None:
		if self._shouldCancel:
			return

		confirmationButtons = (
			DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=False),
			DefaultButton.NO.value._replace(defaultFocus=False, fallbackAction=True),
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
			self.doDownload()
		else:
			self._stopped()

	def openDownloadDialog(self) -> None:
		if ImageDescDownloader._downloadThread is not None and ImageDescDownloader._downloadThread.is_alive():
			# Translators: message when image captioning is still downloading
			ui.message(pgettext("imageDesc", "image captioning is still downloading, please wait..."))
			return
		if ImageDescDownloader.isOpening:
			return

		confirmationButtons = (
			DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=False),
			DefaultButton.NO.value._replace(defaultFocus=False, fallbackAction=True),
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
		ImageDescDownloader.isOpening = True

		if dialog.ShowModal() == ReturnCode.YES:
			self._progressDialog = wx.ProgressDialog(
				# Translators: The title of the dialog displayed while downloading image descriptioner.
				pgettext("imageDesc", "Downloading Image Descriptioner"),
				# Translators: The progress message indicating that a connection is being established.
				pgettext("imageDesc", "Connecting"),
				style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
				parent=gui.mainFrame,
			)
			self.doDownload()
		else:
			ImageDescDownloader.isOpening = False

	def doDownload(self):
		def progressCallback(
			fileName: str,
			downloadedBytes: int,
			totalBytes: int,
			_percentage: float,
		) -> None:
			"""Callback function to capture progress data."""
			self.downloadDict[fileName] = (downloadedBytes, totalBytes)
			downloadedSum = sum(d for d, _ in self.downloadDict.values())
			totalSum = sum(t for _, t in self.downloadDict.values())
			ratio = downloadedSum / totalSum if totalSum > 0 else 0.0
			totalProgress = int(ratio * 100)
			# update progress when downloading all files to prevent premature stop
			if len(self.downloadDict) == len(self.filesToDownload):
				# Translators: The progress message indicating that a download is in progress.
				cont, skip = self._progressDialog.Update(totalProgress, pgettext("imageDesc", "downloading"))
				if not cont:
					self._shouldCancel = True
					self._stopped()

		ImageDescDownloader._downloadThread = threading.Thread(
			target=self.onDownload,
			name="ModelDownloadMainThread",
			daemon=False,
			args=(progressCallback,),
		)
		ImageDescDownloader._downloadThread.start()

	def _stopped(self):
		self.modelDownloader.requestCancel()
		ImageDescDownloader._downloadThread = None
		self._progressDialog.Hide()
		self._progressDialog.Destroy()
		self._progressDialog = None
		ImageDescDownloader.isOpening = False


def openEnableOnceDialog() -> None:
	confirmationButtons = (
		DefaultButton.YES.value._replace(defaultFocus=True, fallbackAction=False),
		DefaultButton.NO.value._replace(defaultFocus=False, fallbackAction=True),
	)

	dialog = MessageDialog(
		parent=None,
		# Translators: title of dialog when enable image desc
		title=pgettext("imageDesc", "Enable AI image descriptions"),
		message=pgettext(
			"imageDesc",
			# Translators: label of dialog when enable image desc
			"AI image description is not enabled, would you like to enable it right now?",
		),
		dialogType=DialogType.STANDARD,
		buttons=confirmationButtons,
	)

	if dialog.ShowModal() == ReturnCode.YES:
		# load image desc in this session
		if not _localCaptioner.isModelLoaded():
			_localCaptioner.toggleImageCaptioning()
