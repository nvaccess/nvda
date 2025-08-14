# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Multi‑threaded model downloader

Download ONNX / tokenizer assets from *Hugging Face* (or any HTTP host)
with progress callbacks. Refactored to use requests library.
"""

from __future__ import annotations

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Callable

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry
import wx
from wx import Frame, Event

from logHandler import log
import config

# Type definitions
ProgressCallback = Callable[[str, int, int, float], None]

# Constants
CHUNK_SIZE: int = 8_192
MAX_RETRIES: int = 3
BACKOFF_BASE: int = 2 # Base delay (in seconds) for exponential backoff strategy


class ModelDownloader:
	"""Multi-threaded model downloader with progress tracking and retry logic."""

	def __init__(
		self,
		remoteHost: str = "huggingface.co",
		maxWorkers: int = 4,
		maxRetries: int = MAX_RETRIES,
	):
		"""
		Initialize the ModelDownloader.

		:param remoteHost: Remote host URL (default: huggingface.co).
		:param maxWorkers: Maximum number of worker threads.
		:param maxRetries: Maximum retry attempts per file.
		"""
		self.remoteHost = remoteHost
		self.maxWorkers = maxWorkers
		self.maxRetries = maxRetries

		# Thread control
		self.cancelRequested = False
		self.downloadLock = threading.Lock()
		self.activeFutures = set()

		# Configure requests session with retry strategy and automatic redirects
		self.session = requests.Session()

		# Configure retry strategy
		retryStrategy = Retry(
			# Maximum number of retries before giving up
			total=maxRetries,
			# Base factor for calculating delay between retries
			backoff_factor=BACKOFF_BASE,
			# HTTP status codes that trigger a retry
			status_forcelist=[429, 500, 502, 503, 504],
			# HTTP methods allowed to retry
			allowed_methods=["HEAD", "GET", "OPTIONS"],
		)

		adapter = HTTPAdapter(max_retries=retryStrategy)
		self.session.mount("http://", adapter)
		self.session.mount("https://", adapter)

		# Set default headers
		self.session.headers.update(
			{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
		)

	def requestCancel(self) -> None:
		"""Request cancellation of all active downloads."""
		log.info("Cancellation requested")
		self.cancelRequested = True

		# Cancel all active futures
		with self.downloadLock:
			for future in self.activeFutures:
				if not future.done():
					future.cancel()
			self.activeFutures.clear()

	def resetCancellation(self) -> None:
		"""Reset cancellation state for new download session."""
		with self.downloadLock:
			self.cancelRequested = False
			self.activeFutures.clear()

	def ensureModelsDirectory(self) -> str:
		"""
		Ensure the *models* directory exists (``../../models`` relative to *basePath*).

		:return: Absolute path of the *models* directory.
		:raises OSError: When the directory cannot be created.
		"""
		modelsDir = os.path.abspath(config.conf["automatedImageDescriptions"]["defaultModelPath"])

		try:
			Path(modelsDir).mkdir(parents=True, exist_ok=True)
			log.info(f"Models directory ensured: {modelsDir}")
			return modelsDir
		except OSError as err:
			raise OSError(f"Failed to create models directory {modelsDir}: {err}") from err

	def constructDownloadUrl(
		self,
		modelName: str,
		filePath: str,
		resolvePath: str = "/resolve/main",
	) -> str:
		"""
		Construct a full download URL for *Hugging Face‑style* repositories.

		:param modelName: Model repository name, e.g. ``Xenova/vit-gpt2-image-captioning``.
		:param filePath: Path inside the repo.
		:param resolvePath: The branch / ref path, default ``/resolve/main``.
		:return: Complete download URL.
		"""
		remoteHost = self.remoteHost
		if not remoteHost.startswith(("http://", "https://")):
			remoteHost = f"https://{remoteHost}"

		base = remoteHost.rstrip("/")
		model = modelName.strip("/")
		ref = resolvePath.strip("/")
		filePath = filePath.lstrip("/")

		return f"{base}/{model}/{ref}/{filePath}"

	def _getRemoteFileSize(self, url: str) -> int:
		"""
		Get remote file size using HEAD request with automatic redirect handling.

		:param url: Remote URL.
		:return: File size in bytes, 0 if unable to determine.
		"""
		if self.cancelRequested:
			return 0

		try:
			# Use HEAD request with automatic redirect following
			response = self.session.head(url, timeout=30, allow_redirects=True)
			response.raise_for_status()

			contentLength = response.headers.get("Content-Length")
			if contentLength:
				return int(contentLength)

			# If HEAD doesn't work, try GET with range header to get just 1 byte
			response = self.session.get(url, headers={"Range": "bytes=0-0"}, timeout=30, allow_redirects=True)

			if response.status_code == 206:  # Partial content
				contentRange = response.headers.get("Content-Range", "")
				if contentRange and "/" in contentRange:
					return int(contentRange.split("/")[-1])

		except Exception as e:
			if not self.cancelRequested:
				log.warning(f"Failed to get remote file size for {url}: {e}")

		return 0

	def _reportProgress(
		self,
		callback: ProgressCallback | None,
		fileName: str,
		downloaded: int,
		total: int,
		lastReported: int,
	) -> int:
		"""
		Report download progress if conditions are met.

		:param callback: Progress callback function.
		:param fileName: Name of the file being downloaded.
		:param downloaded: Bytes downloaded so far.
		:param total: Total file size in bytes.
		:param lastReported: Last reported download amount.
		:return: New lastReported value.
		"""
		if not callback or total == 0 or self.cancelRequested:
			return lastReported

		percent = downloaded / total * 100

		# Report progress every 1 MiB or 1% or when complete
		if (
			downloaded - lastReported >= 1_048_576  # 1 MiB
			or abs(percent - lastReported / total * 100) >= 1.0
			or downloaded == total
		):
			callback(fileName, downloaded, total, percent)
			return downloaded

		return lastReported

	def downloadSingleFile(
		self,
		url: str,
		localPath: str,
		progressCallback: ProgressCallback | None = None,
	) -> tuple[bool, str]:
		"""
		Download a single file with resume support and automatic redirect handling.

		:param url: Remote URL.
		:param localPath: Destination path.
		:param progressCallback: Optional progress reporter.
		:return: (success, message) tuple.
		"""
		if self.cancelRequested:
			return False, "Download cancelled"

		threadId = threading.current_thread().ident or 0
		fileName = os.path.basename(localPath)

		# Create destination directory
		try:
			Path(os.path.dirname(localPath)).mkdir(parents=True, exist_ok=True)
		except OSError as err:
			return False, f"Failed to create directory {localPath}: {err}"

		# Get remote file size with redirect handling
		remoteSize = self._getRemoteFileSize(url)

		if self.cancelRequested:
			return False, "Download cancelled"

		# Check if file already exists and is complete
		if os.path.exists(localPath):
			localSize = os.path.getsize(localPath)
			log.debug(f"localSize: {localSize}, remoteSize: {remoteSize}")

			if remoteSize > 0:
				if localSize == remoteSize:
					if progressCallback and not self.cancelRequested:
						progressCallback(fileName, localSize, localSize, 100.0)
					log.info(f"[Thread-{threadId}] File already complete: {localPath}")
					return True, f"File already complete: {localPath}"
				elif localSize > remoteSize:
					# Local file is larger than remote, may be corrupted
					log.warning(f"Local file larger than remote, removing: {localPath}")
					try:
						os.remove(localPath)
					except OSError:
						pass
			else:
				# Cannot get remote size, assume file exists if non-empty
				if localSize > 0:
					if progressCallback and not self.cancelRequested:
						progressCallback(fileName, localSize, localSize, 100.0)
					log.info(f"[Thread-{threadId}] File already exists (size unknown): {localPath}")
					return True, f"File already exists: {localPath}"

		# Attempt download with retries
		for attempt in range(self.maxRetries):
			if self.cancelRequested:
				return False, "Download cancelled"

			try:
				log.info(f"[Thread-{threadId}] Downloading (attempt {attempt + 1}/{self.maxRetries}): {url}")

				# Check for existing partial file
				resumePos = 0
				if os.path.exists(localPath):
					resumePos = os.path.getsize(localPath)
					log.info(f"[Thread-{threadId}] Resuming from byte {resumePos}")

				# Set up headers for resume
				headers = {}
				if resumePos > 0:
					headers["Range"] = f"bytes={resumePos}-"

				# Make request with automatic redirect handling
				response = self.session.get(
					url,
					headers=headers,
					stream=True,
					timeout=30,
					allow_redirects=True,
				)

				if self.cancelRequested:
					return False, "Download cancelled"

				# Check if resume is supported
				if resumePos > 0 and response.status_code != 206:
					log.info(f"[Thread-{threadId}] Server doesn't support resume, starting from beginning")
					resumePos = 0
					if os.path.exists(localPath):
						try:
							os.remove(localPath)
						except OSError:
							pass

					if self.cancelRequested:
						return False, "Download cancelled"

					# Make new request without range header
					response = self.session.get(url, stream=True, timeout=30, allow_redirects=True)

				response.raise_for_status()

				# Determine total file size
				if response.status_code == 206:
					# Partial content response
					contentRange = response.headers.get("Content-Range", "")
					if contentRange and "/" in contentRange:
						total = int(contentRange.split("/")[-1])
					else:
						total = int(response.headers.get("Content-Length", "0")) + resumePos
				else:
					total = int(response.headers.get("Content-Length", "0"))

				if total > 0:
					log.info(f"[Thread-{threadId}] Total file size: {total:,} bytes")

				# Download file
				downloaded = resumePos
				lastReported = downloaded
				mode = "ab" if resumePos > 0 else "wb"

				try:
					with open(localPath, mode) as fh:
						for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
							if self.cancelRequested:
								return False, "Download cancelled"

							if chunk:  # filter out keep-alive chunks
								fh.write(chunk)
								downloaded += len(chunk)

								if total > 0:
									lastReported = self._reportProgress(
										progressCallback,
										fileName,
										downloaded,
										total,
										lastReported,
									)
				finally:
					response.close()

				if self.cancelRequested:
					return False, "Download cancelled"

				# Verify download integrity
				actualSize = os.path.getsize(localPath)

				if actualSize == 0:
					return False, "Downloaded file is empty"

				if total > 0 and actualSize != total:
					return False, f"File incomplete: {actualSize}/{total} bytes downloaded"

				# Final progress callback
				if progressCallback and not self.cancelRequested:
					progressCallback(fileName, actualSize, max(total, actualSize), 100.0)

				log.info(f"[Thread-{threadId}] Successfully downloaded: {localPath}")
				return True, "Download completed"

			except requests.exceptions.HTTPError as e:
				if e.response is not None and e.response.status_code == 416:  # Range Not Satisfiable
					if os.path.exists(localPath):
						actualSize = os.path.getsize(localPath)
						if actualSize > 0:
							log.info(f"[Thread-{threadId}] File appears to be complete: {localPath}")
							if progressCallback and not self.cancelRequested:
								progressCallback(fileName, actualSize, actualSize, 100.0)
							return True, "Download completed"

				message = f"HTTP {e.response.status_code if e.response else 'Error'}: {str(e)}"

			except RequestException as e:
				if self.cancelRequested:
					return False, "Download cancelled"
				message = f"Request error: {str(e)}"

			except Exception as e:
				if self.cancelRequested:
					return False, "Download cancelled"
				message = f"Unexpected error: {str(e)}"
				log.error(message)

			if not self.cancelRequested:
				log.info(f"[Thread-{threadId}] {message} – {url}")
				if attempt < self.maxRetries - 1:
					wait = BACKOFF_BASE**attempt
					log.info(f"[Thread-{threadId}] Waiting {wait}s before retry…")
					for _ in range(wait):
						if self.cancelRequested:
							return False, "Download cancelled"
						time.sleep(1)
				else:
					return False, message

		return False, "Maximum retries exceeded"

	def downloadModelsMultithreaded(
		self,
		modelsDir: str,
		modelName: str = "Xenova/vit-gpt2-image-captioning",
		filesToDownload: list[str] | None = None,
		resolvePath: str = "/resolve/main",
		progressCallback: ProgressCallback | None = None,
	) -> tuple[list[str], list[str]]:
		"""
		Download multiple model assets concurrently.

		:param modelsDir: Base *models* directory.
		:param modelName: Repository name.
		:param filesToDownload: Explicit file list; None uses common defaults.
		:param resolvePath: Branch / ref path.
		:param progressCallback: Optional progress callback.
		:return: (successful_paths, failed_paths) tuple.
		"""
		if not self.remoteHost or not modelName:
			raise ValueError("remoteHost and modelName cannot be empty")

		filesToDownload = filesToDownload or [
			"onnx/encoder_model_quantized.onnx",
			"onnx/decoder_model_merged_quantized.onnx",
			"config.json",
			"vocab.json",
		]

		if not filesToDownload:
			raise ValueError("filesToDownload cannot be empty")

		log.info(
			f"Starting download of {len(filesToDownload)} files for model: {modelName}\n"
			f"Remote host: {self.remoteHost}\nMax workers: {self.maxWorkers}",
		)

		localModelDir = os.path.join(modelsDir, modelName)
		successful: list[str] = []
		failed: list[str] = []

		with ThreadPoolExecutor(max_workers=self.maxWorkers) as executor:
			futures = []

			for path in filesToDownload:
				if self.cancelRequested:
					break

				future = executor.submit(
					self.downloadSingleFile,
					self.constructDownloadUrl(modelName, path, resolvePath),
					os.path.join(localModelDir, path),
					progressCallback,
				)
				futures.append((future, path))

				# Track active futures for cancellation
				with self.downloadLock:
					self.activeFutures.add(future)

			# Process completed futures
			for future, filePath in futures:
				if self.cancelRequested:
					# Cancel remaining futures but don't wait for them
					with self.downloadLock:
						for f, _ in futures:
							if not f.done():
								f.cancel()
					break

				# Remove from active futures tracking
				with self.downloadLock:
					self.activeFutures.discard(future)

				try:
					# Use a short timeout to avoid blocking indefinitely
					ok, msg = future.result(timeout=1.0)
					if ok:
						successful.append(filePath)
						log.info("✓ " + filePath)
					else:
						failed.append(filePath)
						log.info(f"✗ {filePath} - {msg}")
				except Exception as err:
					failed.append(filePath)
					log.info(f"✗ {filePath} – {err}")

		# Summary
		if not self.cancelRequested:
			log.info("\n=== Download Summary ===")
			log.info(f"Total: {len(filesToDownload)}")
			log.info(f"Successful: {len(successful)}")
			log.info(f"Failed: {len(failed)}")
			log.info(f"\nLocal model directory: {localModelDir}")
		else:
			log.info("Download cancelled by user")

		return successful, failed

	def getModelFilePaths(self, modelName: str = "Xenova/vit-gpt2-image-captioning") -> dict[str, str]:
		"""
		Return absolute paths for encoder / decoder / config / vocab.

		:param modelName: Repository name.
		:return: Dictionary containing model file paths.
		"""
		modelsDir = self.ensureModelsDirectory()
		localDir = os.path.join(modelsDir, modelName)
		return {
			"encoderPath": os.path.join(localDir, "onnx", "encoder_model_quantized.onnx"),
			"decoderPath": os.path.join(localDir, "onnx", "decoder_model_merged_quantized.onnx"),
			"configPath": os.path.join(localDir, "config.json"),
			"vocabPath": os.path.join(localDir, "vocab.json"),
			"modelDir": localDir,
		}

	def __del__(self):
		"""Clean up the session when the downloader is destroyed."""
		if hasattr(self, "session"):
			self.session.close()


class DownloadDialog(wx.Dialog):

	def __init__(self, parent: Frame, downloader: ModelDownloader):
		"""create default model download dialog
		
		:param parent: parent wx frame
		:param downloader: default model downloader
		"""
		# Translators: title of dialog when downloading default model
		super().__init__(parent, title=pgettext("imageDesc", "AI Image Description"), size=(350, 180))
		self.downloader = downloader
		self.retryRequested = False
		self.downloadThread = None

		vbox = wx.BoxSizer(wx.VERTICAL)

		# Translators: label of dialog when downloading default model
		self.statusText = wx.StaticText(self, label=pgettext("imageDesc", "Download default model?"))
		vbox.Add(self.statusText, 0, wx.ALL | wx.CENTER, 10)

		buttonSizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
		vbox.Add(buttonSizer, 0, wx.ALL | wx.CENTER, 10)

		self.SetSizer(vbox)

		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)
		self.Bind(wx.EVT_CLOSE, self.onClose)

	def onOk(self, event: Event):
		""" on ok event

		:param event:		 wx event when choose ok
		"""
		# Translators: label when downloading model
		self.statusText.SetLabel(pgettext("imageDesc", "Downloading, please wait..."))
		okButton = self.FindWindowById(wx.ID_OK)
		cancelButton = self.FindWindowById(wx.ID_CANCEL)

		if okButton:
			okButton.Disable()
		if cancelButton:
			# Translators: cancel button label
			cancelButton.SetLabel(pgettext("imageDesc", "Cancel"))

		# Reset cancellation state for new download
		self.downloader.resetCancellation()

		self.downloadThread = threading.Thread(target=self.performDownload, daemon=True)
		self.downloadThread.start()

	def onCancel(self, event: Event):
		""" on cancel event

		:param event:		 wx event when choose cancel
		"""

		if self.downloadThread and self.downloadThread.is_alive():
			# Request cancellation
			self.downloader.requestCancel()
			# Translators: Message when cancelling download the model
			self.statusText.SetLabel(pgettext("imageDesc", "Cancelling download..."))

			# Wait briefly for cancellation to take effect
			wx.CallLater(1000, self.checkCancellationComplete)
		else:
			self.EndModal(wx.ID_CANCEL)

	def onClose(self, event: Event):
		""" Handle window close event (X button)

		:param event:		 wx event when choose close
		"""
		if self.downloadThread and self.downloadThread.is_alive():
			self.downloader.requestCancel()
			# Wait briefly for cancellation
			wx.CallLater(1000, lambda: self.Destroy())
		else:
			self.Destroy()

	def checkCancellationComplete(self):
		"""Check if cancellation is complete and close dialog."""
		if not self.downloadThread or not self.downloadThread.is_alive():
			self.EndModal(wx.ID_CANCEL)
		else:
			# Check again in a bit
			wx.CallLater(500, self.checkCancellationComplete)

	def performDownload(self):
		try:
			successful, failed = self.downloader.downloadModelsMultithreaded(modelsDir="models")
			wx.CallAfter(self.onDownloadComplete, successful, failed)
		except Exception as e:
			log.exception("Download error")
			# Translators: message when fail to download 
			wx.CallAfter(self.onDownloadError, pgettext("imageDesc", "download fail"))

	def onDownloadComplete(self, successful: list[str], failed: list[str]):
		""" on download complete
		
		:param success: successful downloaded files
		:param failed: files fail to downloaded  
		"""
		if self.downloader.cancelRequested:
			self.EndModal(wx.ID_CANCEL)
			return

		if failed:
			# Translators: message when fail to download
			msg = pgettext("imageDesc", "Some downloads failed, \nRetry?")
			dlg = wx.MessageDialog(self, msg, "Download Failed", style=wx.YES_NO | wx.ICON_WARNING)
			result = dlg.ShowModal()
			dlg.Destroy()

			if result == wx.ID_YES:
				# Re-enable the OK button and restart download
				okButton = self.FindWindowById(wx.ID_OK)
				cancelButton = self.FindWindowById(wx.ID_CANCEL)

				if okButton:
					okButton.Enable()
				if cancelButton:
					# Translators: cancel downloading model
					cancelButton.SetLabel(pgettext("imageDesc", "Cancel"))

				self.onOk(None)  # Restart download
			else:
				self.EndModal(wx.ID_CANCEL)
		else:
			wx.MessageBox(
				# Translators: Message when successful download the model
				pgettext("imageDesc", "Download completed!"),
				# Translators: title when successful download the model
				pgettext("imageDesc", "Success"),
				wx.OK | wx.ICON_INFORMATION,
			)
			self.EndModal(wx.ID_OK)

	def onDownloadError(self, errorMessage: str):
		wx.MessageBox(f"Download error: {errorMessage}", "Error", wx.OK | wx.ICON_ERROR)
		self.EndModal(wx.ID_CANCEL)


def openDownloadDialog() -> None:
	"""Open the model downloader frame window."""

	def showDialog() -> None:
		"""Show the model dialog window."""
		try:
			frame = wx.Frame(None)
			downloader = ModelDownloader()
			dlg = DownloadDialog(frame, downloader)
			result = dlg.ShowModal()
			dlg.Destroy()
			frame.Destroy()
			return result
		except Exception:
			log.exception("Model downloder")
			return wx.ID_CANCEL

	# Ensure execution in main thread
	wx.CallAfter(showDialog)
