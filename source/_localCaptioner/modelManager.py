# -*- coding: UTF-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
import wx
import threading
from typing import List, Optional
import winsound  # Windows sound API for audio notifications

# Assume modelDownloader.py is in the same directory
try:
	from .modelDownloader import downloadModelsMultithreaded, ensureModelsDirectory
except ImportError:
	from modelDownloader import downloadModelsMultithreaded, ensureModelsDirectory


try:
	from logHandler import log
	import addonHandler

	addonHandler.initTranslation()
except:
	_ = format


class AdvancedSettingsDialog(wx.Dialog):
	"""Advanced Settings Dialog for model download configuration.

	This dialog allows users to configure advanced settings for model downloads,
	including model name, file selection, resolve path, and mirror usage.
	"""

	def __init__(
		self,
		parent,
		modelName: str = "Xenova/vit-gpt2-image-captioning",
		filesList: Optional[List[str]] = None,
		resolvePath: str = "/resolve/main",
		useMirror: bool = False,
	):
		"""Initialize the Advanced Settings Dialog.

		Args:
			parent: Parent window
			modelName: Name of the model to download
			filesList: List of files to download
			resolvePath: Path resolution string
			useMirror: Whether to use HuggingFace mirror
		"""
		# Translators: A message presented in the settings panel
		super().__init__(
			parent,
			title=_("Advanced Settings"),
			size=(500, 400),
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER,
		)

		self.modelName = modelName
		self.filesList = filesList or [
			"onnx/encoder_model_quantized.onnx",
			"onnx/decoder_model_merged_quantized.onnx",
			"config.json",
			"vocab.json",
		]
		self.resolvePath = resolvePath
		self.useMirror = useMirror

		self._initUI()
		self._bindEvents()

	def _initUI(self):
		"""Initialize the user interface components."""
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Create notebook control for grouping
		notebook = wx.Notebook(self)

		# Model configuration page
		modelPanel = wx.Panel(notebook)
		modelSizer = wx.BoxSizer(wx.VERTICAL)

		# Model name
		# Translators: Label for model name input field
		modelSizer.Add(wx.StaticText(modelPanel, label=_("Model Name:")), 0, wx.ALL, 5)
		self.modelNameCtrl = wx.TextCtrl(modelPanel, value=self.modelName, size=(400, -1))
		modelSizer.Add(self.modelNameCtrl, 0, wx.ALL | wx.EXPAND, 5)

		# Resolve path
		# Translators: Label for resolve path input field
		modelSizer.Add(wx.StaticText(modelPanel, label=_("Resolve Path:")), 0, wx.ALL, 5)
		self.resolvePathCtrl = wx.TextCtrl(modelPanel, value=self.resolvePath, size=(400, -1))
		modelSizer.Add(self.resolvePathCtrl, 0, wx.ALL | wx.EXPAND, 5)

		# Use mirror
		# Translators: Checkbox label for using HuggingFace mirror
		self.useMirrorCb = wx.CheckBox(modelPanel, label=_("Use HuggingFace Mirror"))
		self.useMirrorCb.SetValue(self.useMirror)
		modelSizer.Add(self.useMirrorCb, 0, wx.ALL, 5)

		modelPanel.SetSizer(modelSizer)
		# Translators: Tab label for model configuration
		notebook.AddPage(modelPanel, _("Model Config"))

		# File list page
		filesPanel = wx.Panel(notebook)
		filesSizer = wx.BoxSizer(wx.VERTICAL)

		# Translators: Label for file list section
		filesSizer.Add(wx.StaticText(filesPanel, label=_("Files to Download:")), 0, wx.ALL, 5)

		# File list control
		self.filesListbox = wx.ListBox(
			filesPanel,
			choices=self.filesList,
			style=wx.LB_MULTIPLE | wx.LB_HSCROLL,
		)
		# Select all files by default
		for i in range(len(self.filesList)):
			self.filesListbox.SetSelection(i)
		filesSizer.Add(self.filesListbox, 1, wx.ALL | wx.EXPAND, 5)

		# File operation buttons
		fileBtnSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Button label for adding a file
		self.addFileBtn = wx.Button(filesPanel, label=_("Add File"))
		# Translators: Button label for removing a file
		self.removeFileBtn = wx.Button(filesPanel, label=_("Remove File"))
		fileBtnSizer.Add(self.addFileBtn, 0, wx.ALL, 2)
		fileBtnSizer.Add(self.removeFileBtn, 0, wx.ALL, 2)
		filesSizer.Add(fileBtnSizer, 0, wx.ALL | wx.CENTER, 5)

		filesPanel.SetSizer(filesSizer)
		# Translators: Tab label for file list
		notebook.AddPage(filesPanel, _("File List"))

		mainSizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 10)

		# Dialog buttons
		btnSizer = wx.StdDialogButtonSizer()
		# Translators: OK button text
		okBtn = wx.Button(self, wx.ID_OK, _("OK"))
		# Translators: Cancel button text
		cancelBtn = wx.Button(self, wx.ID_CANCEL, _("Cancel"))
		btnSizer.AddButton(okBtn)
		btnSizer.AddButton(cancelBtn)
		btnSizer.Realize()

		mainSizer.Add(btnSizer, 0, wx.ALL | wx.CENTER, 10)

		self.SetSizer(mainSizer)

	def _bindEvents(self):
		"""Bind UI events to their handlers."""
		self.addFileBtn.Bind(wx.EVT_BUTTON, self.onAddFile)
		self.removeFileBtn.Bind(wx.EVT_BUTTON, self.onRemoveFile)

	def onAddFile(self, event):
		"""Handle add file button click event.

		Args:
			event: Button click event
		"""
		# Translators: Dialog title for adding a file
		# Translators: Prompt text for entering file path
		dlg = wx.TextEntryDialog(self, _("Enter file path:"), _("Add File"))
		if dlg.ShowModal() == wx.ID_OK:
			filePath = dlg.GetValue().strip()
			if filePath and filePath not in self.filesList:
				self.filesList.append(filePath)
				self.filesListbox.Append(filePath)
				# Select the newly added file
				self.filesListbox.SetSelection(len(self.filesList) - 1)
		dlg.Destroy()

	def onRemoveFile(self, event):
		"""Handle remove file button click event.

		Args:
			event: Button click event
		"""
		selection = self.filesListbox.GetSelections()
		if selection != wx.NOT_FOUND:
			for s in sorted(selection, reverse=True):
				self.filesList.pop(s)
				self.filesListbox.Delete(s)

	def getSettings(self) -> dict:
		"""Get current settings from the dialog.

		Returns:
			Dictionary containing all current settings
		"""
		# Get selected files
		selectedFiles = []
		for i in range(self.filesListbox.GetCount()):
			if self.filesListbox.IsSelected(i):
				selectedFiles.append(self.filesList[i])

		return {
			"modelName": self.modelNameCtrl.GetValue().strip(),
			"filesToDownload": selectedFiles,
			"resolvePath": self.resolvePathCtrl.GetValue().strip(),
			"useMirror": self.useMirrorCb.GetValue(),
		}


class SoundNotification:
	"""Sound notification manager using Windows standard library.

	This class provides methods to play different types of system sounds
	for various download events using the Windows winsound module.
	"""

	@staticmethod
	def playStart():
		"""Play download start sound using system information sound."""
		try:
			# Play system information sound
			winsound.MessageBeep(winsound.MB_ICONASTERISK)
		except Exception as e:
			log.error(e)
			pass  # Silently fail if sound unavailable

	@staticmethod
	def playSuccess():
		"""Play success sound using system default sound."""
		try:
			# Play system default sound
			winsound.MessageBeep(winsound.MB_OK)
		except Exception as e:
			log.error(e)
			pass

	@staticmethod
	def playError():
		"""Play error sound using system error sound."""
		try:
			# Play system error sound
			winsound.MessageBeep(winsound.MB_ICONHAND)
		except Exception as e:
			log.error(e)
			pass

	@staticmethod
	def playWarning():
		"""Play warning sound using system warning sound."""
		try:
			# Play system warning sound
			winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
		except Exception as e:
			log.error(e)
			pass


class ModelManagerFrame(wx.Frame):
	"""Model Manager Main Frame.

	This is the main application window that provides the interface for
	managing model downloads. It includes path selection, advanced settings,
	download progress tracking, and logging functionality.
	"""

	def __init__(self):
		"""Initialize the Model Manager Frame."""
		# Translators: Main window title
		super().__init__(None, title=_("Model Manager"), size=(600, 450))

		# Default settings
		self.downloadPath = ""
		self.modelName = "Xenova/vit-gpt2-image-captioning"
		self.filesToDownload = [
			"onnx/encoder_model_quantized.onnx",
			"onnx/decoder_model_merged_quantized.onnx",
			"config.json",
			"vocab.json",
		]
		self.resolvePath = "/resolve/main"
		self.useMirror = False

		# Download related
		self.downloadThread = None
		self.downloadCancelled = False

		self._initUI()
		self._initDefaultPath()
		self._bindEvents()

		# Center display
		self.Centre()

	def _initUI(self):
		"""Initialize the main user interface components."""
		panel = wx.Panel(self)
		mainSizer = wx.BoxSizer(wx.VERTICAL)

		# Title
		# Translators: Main application title text
		titleText = wx.StaticText(panel, label=_("Model Download Manager"))
		titleFont = titleText.GetFont()
		titleFont.PointSize += 4
		titleFont = titleFont.Bold()
		titleText.SetFont(titleFont)
		mainSizer.Add(titleText, 0, wx.ALL | wx.CENTER, 15)

		# Download path selection
		# Translators: Group box label for download settings
		pathBox = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Download Settings")), wx.VERTICAL)

		pathSizer = wx.BoxSizer(wx.HORIZONTAL)
		# Translators: Label for download path field
		pathSizer.Add(wx.StaticText(panel, label=_("Download Path:")), 0, wx.ALL | wx.CENTER, 5)

		self.pathCtrl = wx.TextCtrl(panel, size=(350, -1))
		pathSizer.Add(self.pathCtrl, 1, wx.ALL | wx.EXPAND, 5)

		# Translators: Button label for browsing directory
		self.browseBtn = wx.Button(panel, label=_("Browse..."))
		pathSizer.Add(self.browseBtn, 0, wx.ALL, 5)

		pathBox.Add(pathSizer, 0, wx.ALL | wx.EXPAND, 5)
		mainSizer.Add(pathBox, 0, wx.ALL | wx.EXPAND, 10)

		# Model information display
		# Translators: Group box label for model information
		infoBox = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Model Information")), wx.VERTICAL)

		# Translators: Model name display format
		self.modelInfoText = wx.StaticText(
			panel,
			label=_("Model: {modelName}").format(modelName=self.modelName),
		)
		infoBox.Add(self.modelInfoText, 0, wx.ALL, 5)

		# Translators: File count display format
		self.filesInfoText = wx.StaticText(
			panel,
			label=_("File Count: {count}").format(count=len(self.filesToDownload)),
		)
		infoBox.Add(self.filesInfoText, 0, wx.ALL, 5)

		mainSizer.Add(infoBox, 0, wx.ALL | wx.EXPAND, 10)

		# Operation buttons
		btnSizer = wx.BoxSizer(wx.HORIZONTAL)

		# Translators: Button label for advanced settings
		self.advancedBtn = wx.Button(panel, label=_("Advanced Settings..."))
		btnSizer.Add(self.advancedBtn, 0, wx.ALL, 5)

		btnSizer.AddStretchSpacer(1)

		# Translators: Button label for starting download
		self.downloadBtn = wx.Button(panel, label=_("Start Download"), size=(120, 35))
		self.downloadBtn.SetBackgroundColour(wx.Colour(0, 120, 215))
		self.downloadBtn.SetForegroundColour(wx.Colour(255, 255, 255))
		btnSizer.Add(self.downloadBtn, 0, wx.ALL, 5)

		mainSizer.Add(btnSizer, 0, wx.ALL | wx.EXPAND, 10)

		# Status bar
		# Translators: Initial status text
		self.statusText = wx.StaticText(panel, label=_("Ready"))
		mainSizer.Add(self.statusText, 0, wx.ALL | wx.EXPAND, 10)

		# Log area
		# Translators: Group box label for download log
		logBox = wx.StaticBoxSizer(wx.StaticBox(panel, label=_("Download Log")), wx.VERTICAL)
		self.logText = wx.TextCtrl(
			panel,
			style=wx.TE_MULTILINE | wx.TE_READONLY,
			size=(550, 150),
		)
		logBox.Add(self.logText, 1, wx.ALL | wx.EXPAND, 5)
		mainSizer.Add(logBox, 1, wx.ALL | wx.EXPAND, 10)

		panel.SetSizer(mainSizer)

	def _initDefaultPath(self):
		"""Initialize default download path."""
		try:
			defaultPath = ensureModelsDirectory()
			self.downloadPath = defaultPath
			self.pathCtrl.SetValue(defaultPath)
			# Translators: Log message for default path initialization
			self.log(_("Default download path: {path}").format(path=defaultPath))
		except Exception as e:
			# Translators: Log message for path initialization failure
			self.log(_("Failed to initialize path: {error}").format(error=e))

	def _bindEvents(self):
		"""Bind UI events to their handlers."""
		self.browseBtn.Bind(wx.EVT_BUTTON, self.onBrowsePath)
		self.advancedBtn.Bind(wx.EVT_BUTTON, self.onAdvancedSettings)
		self.downloadBtn.Bind(wx.EVT_BUTTON, self.onDownload)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		# Bind ESC key to close
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyDown)

	def onKeyDown(self, event):
		"""Handle key press events.

		Args:
			event: Key press event
		"""
		if event.GetKeyCode() == wx.WXK_ESCAPE:
			self.Close()
		else:
			event.Skip()

	def log(self, message: str):
		"""Add log information in a thread-safe manner.

		Args:
			message: Log message to add
		"""
		wx.CallAfter(self._logSafe, message)

	def _logSafe(self, message: str):
		"""Thread-safe log addition.

		Args:
			message: Log message to add
		"""
		if not self.IsBeingDeleted():
			self.logText.AppendText(f"{message}\n")
			self.logText.SetInsertionPointEnd()

	def updateStatus(self, status: str):
		"""Update status display in a thread-safe manner.

		Args:
			status: Status message to display
		"""
		wx.CallAfter(self._updateStatusSafe, status)

	def _updateStatusSafe(self, status: str):
		"""Thread-safe status update.

		Args:
			status: Status message to display
		"""
		if not self.IsBeingDeleted():
			self.statusText.SetLabel(status)

	def updateProgress(self, fileName: str, downloaded: int, total: int, progressPercent: float):
		"""Update download progress information.

		Args:
			fileName: Name of the file being downloaded
			downloaded: Number of bytes downloaded
			total: Total number of bytes to download
			progressPercent: Download progress percentage
		"""
		# Translators: Progress log message format
		self.log(
			_("file: {fileName}  progress: {progress:.2f}%").format(
				fileName=fileName,
				progress=progressPercent,
			),
		)

	def onBrowsePath(self, event):
		"""Handle browse path button click event.

		Args:
			event: Button click event
		"""
		# Translators: Directory selection dialog title
		dlg = wx.DirDialog(self, _("Select Download Directory"), defaultPath=self.downloadPath)
		if dlg.ShowModal() == wx.ID_OK:
			self.downloadPath = dlg.GetPath()
			self.pathCtrl.SetValue(self.downloadPath)
			# Translators: Log message for path change
			self.log(_("Download path changed to: {path}").format(path=self.downloadPath))
		dlg.Destroy()

	def onAdvancedSettings(self, event):
		"""Handle advanced settings button click event.

		Args:
			event: Button click event
		"""
		dlg = AdvancedSettingsDialog(
			self,
			self.modelName,
			self.filesToDownload,
			self.resolvePath,
			self.useMirror,
		)
		if dlg.ShowModal() == wx.ID_OK:
			settings = dlg.getSettings()
			self.modelName = settings["modelName"]
			self.filesToDownload = settings["filesToDownload"]
			self.resolvePath = settings["resolvePath"]
			self.useMirror = settings["useMirror"]

			# Update display information
			# Translators: Model name display format
			self.modelInfoText.SetLabel(_("Model: {modelName}").format(modelName=self.modelName))
			# Translators: File count display format
			self.filesInfoText.SetLabel(_("File Count: {count}").format(count=len(self.filesToDownload)))

			# Translators: Mirror usage indicator
			mirrorInfo = _(" (using mirror)") if self.useMirror else ""
			# Translators: Settings update log message
			self.log(
				_("Settings updated: {modelName}{mirrorInfo}, {count} files").format(
					modelName=self.modelName,
					mirrorInfo=mirrorInfo,
					count=len(self.filesToDownload),
				),
			)

		dlg.Destroy()

	def onDownload(self, event):
		"""Handle start download button click event.

		Args:
			event: Button click event
		"""
		if self.downloadThread and self.downloadThread.is_alive():
			# Translators: Log message when download is already in progress
			self.log(_("Download in progress..."))
			return

		if not self.filesToDownload:
			# Use gentle notification instead of message box
			SoundNotification.playError()
			# Translators: Error message for no files selected
			self.log(_("❌ Error: Please select files to download in Advanced Settings"))
			# Translators: Status message for no files selected
			self.updateStatus(_("Error: No files selected"))
			return

		# Disable download button
		self.downloadBtn.Enable(False)
		self.downloadCancelled = False

		# Play start sound
		SoundNotification.playStart()

		# Start download thread
		self.downloadThread = threading.Thread(target=self._downloadWorker)
		self.downloadThread.daemon = True
		self.downloadThread.start()

	def _downloadWorker(self):
		"""Download worker thread function."""
		try:
			# Translators: Status message during download
			self.updateStatus(_("Downloading..."))
			# Translators: Log message for download start
			self.log(_("Starting model file download..."))

			# Determine remote host
			remoteHost = "hf-mirror.com" if self.useMirror else "huggingface.co"

			# Translators: Log message for remote host
			self.log(_("Remote host: {host}").format(host=remoteHost))
			# Translators: Log message for model name
			self.log(_("Model name: {name}").format(name=self.modelName))
			self.downloadPath = self.pathCtrl.GetValue()
			# Translators: Log message for download path
			self.log(_("Download path: {path}").format(path=self.downloadPath))
			# Translators: Log message for file count
			self.log(_("File count: {count}").format(count=len(self.filesToDownload)))
			# Translators: Log message for download progress
			self.log(_("Downloading... please wait"))

			# Call download function
			try:
				successful, failed = downloadModelsMultithreaded(
					modelsDir=self.downloadPath,
					remoteHost=remoteHost,
					modelName=self.modelName,
					filesToDownload=self.filesToDownload,
					resolvePath=self.resolvePath,
					maxWorkers=4,
					progressCallback=self.updateProgress,
				)
			except Exception as e:
				log.error(e)

			# Process results
			if not self.downloadCancelled:
				self._handleDownloadResult(successful, failed)

		except Exception as e:
			# Translators: Log message for download error
			self.log(_("Error during download: {error}").format(error=e))
			# Translators: Status message for download failure
			self.updateStatus(_("Download failed"))
			SoundNotification.playError()
		finally:
			wx.CallAfter(self._downloadFinished)

	def _handleDownloadResult(self, successful: List[str], failed: List[str]):
		"""Handle download results and provide appropriate feedback.

		Args:
			successful: List of successfully downloaded files
			failed: List of files that failed to download
		"""
		total = len(successful) + len(failed)

		if not failed:
			# All successful
			# Translators: Success message for all files downloaded
			self.log(
				_("✅ All files downloaded successfully! ({success}/{total})").format(
					success=len(successful),
					total=total,
				),
			)
			# Translators: Status message for completed download
			self.updateStatus(_("Download completed"))
			SoundNotification.playSuccess()
		elif not successful:
			# All failed
			# Translators: Error message for all files failed
			self.log(
				_("❌ All files download failed! ({failed}/{total})").format(
					failed=len(failed),
					total=total,
				),
			)
			# Translators: Log message for failed files list
			self.log(_("Failed files: {files}").format(files=", ".join(failed)))
			# Translators: Status message for download failure
			self.updateStatus(_("Download failed"))
			SoundNotification.playError()
		else:
			# Partial success
			# Translators: Warning message for partial download success
			self.log(
				_("⚠️ Partial download success ({success}/{total})").format(
					success=len(successful),
					total=total,
				),
			)
			# Translators: Log message for successful files count
			self.log(_("Successful: {count} files").format(count=len(successful)))
			# Translators: Log message for failed files count and list
			self.log(
				_("Failed: {count} files - {files}").format(
					count=len(failed),
					files=", ".join(failed),
				),
			)
			# Translators: Status message for partial completion
			self.updateStatus(_("Partially completed"))
			SoundNotification.playWarning()

	def _downloadFinished(self):
		"""Clean up after download completion."""
		self.downloadBtn.Enable(True)

	def onClose(self, event):
		"""Handle window close event.

		Args:
			event: Close event
		"""
		if self.downloadThread and self.downloadThread.is_alive():
			self.downloadCancelled = True
			# Translators: Confirmation dialog message for exit during download
			# Translators: Confirmation dialog title for exit
			dlg = wx.MessageDialog(
				self,
				_("Download is in progress. Are you sure you want to exit?"),
				_("Confirm Exit"),
				wx.YES_NO | wx.ICON_QUESTION,
			)
			if dlg.ShowModal() != wx.ID_YES:
				dlg.Destroy()
				return
			dlg.Destroy()

		self.Destroy()


