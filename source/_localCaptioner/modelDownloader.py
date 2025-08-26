# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, tianze
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Multi‑threaded model downloader

Download ONNX / tokenizer assets from *Hugging Face* (or any HTTP host)
with progress callbacks. Refactored to use requests library.
"""

import os
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from collections.abc import Callable

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
from urllib3.util.retry import Retry

from logHandler import log
import config
from NVDAState import _WritePaths

# Type definitions
ProgressCallback = Callable[[str, int, int, float], None]

# Constants
CHUNK_SIZE: int = 8_192
MAX_RETRIES: int = 3
BACKOFF_BASE: int = 2  # Base delay (in seconds) for exponential backoff strategy


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

		:param url: Remote URL to download from.
		:param localPath: Local file path to save the downloaded file.
		:param progressCallback: Optional callback function for progress reporting.
		:return: Tuple of (success_flag, status_message).
		:raises OSError: When directory creation fails.
		:raises requests.exceptions.RequestException: When network request fails.
		:raises Exception: When unexpected errors occur during download.
		"""
		if self.cancelRequested:
			return False, "Download cancelled"

		threadId = threading.current_thread().ident or 0
		fileName = os.path.basename(localPath)

		# Create destination directory
		success, message = self._createDestinationDirectory(localPath)
		if not success:
			return False, message

		# Get remote file size with redirect handling
		remoteSize = self._getRemoteFileSize(url)

		if self.cancelRequested:
			return False, "Download cancelled"

		# Check if file already exists and is complete
		success, message = self._checkExistingFile(
			localPath, remoteSize, fileName, progressCallback, threadId
		)
		if success is not None:
			return success, message

		# Attempt download with retries
		return self._downloadWithRetries(url, localPath, fileName, threadId, progressCallback)

	def _createDestinationDirectory(self, localPath: str) -> tuple[bool, str]:
		"""
		Create destination directory if it doesn't exist.

		:param localPath: Local file path to create directory for.
		:return: Tuple of (success_flag, error_message).
		:raises OSError: When directory creation fails due to permissions or disk space.
		"""
		try:
			Path(os.path.dirname(localPath)).mkdir(parents=True, exist_ok=True)
			return True, ""
		except OSError as err:
			return False, f"Failed to create directory {localPath}: {err}"

	def _checkExistingFile(
		self,
		localPath: str,
		remoteSize: int,
		fileName: str,
		progressCallback: ProgressCallback | None,
		threadId: int,
	) -> tuple[bool | None, str]:
		"""
		Check if file already exists and is complete.

		:param localPath: Local file path to check.
		:param remoteSize: Size of remote file in bytes.
		:param fileName: Base name of the file for progress reporting.
		:param progressCallback: Optional callback function for progress reporting.
		:param threadId: Current thread identifier for logging.
		:return: Tuple of (completion_status, status_message). None status means download should continue.
		:raises OSError: When file operations fail.
		"""
		if not os.path.exists(localPath):
			return None, ""

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

		return None, ""

	def _downloadWithRetries(
		self,
		url: str,
		localPath: str,
		fileName: str,
		threadId: int,
		progressCallback: ProgressCallback | None,
	) -> tuple[bool, str]:
		"""
		Attempt download with retry logic and exponential backoff.

		:param url: Remote URL to download from.
		:param localPath: Local file path to save the downloaded file.
		:param fileName: Base name of the file for progress reporting.
		:param threadId: Current thread identifier for logging.
		:param progressCallback: Optional callback function for progress reporting.
		:return: Tuple of (success_flag, status_message).
		:raises requests.exceptions.HTTPError: When HTTP request fails.
		:raises requests.exceptions.RequestException: When network request fails.
		:raises Exception: When unexpected errors occur.
		"""
		for attempt in range(self.maxRetries):
			if self.cancelRequested:
				return False, "Download cancelled"

			try:
				log.info(f"[Thread-{threadId}] Downloading (attempt {attempt + 1}/{self.maxRetries}): {url}")

				success, message = self._performSingleDownload(
					url, localPath, fileName, threadId, progressCallback
				)
				if success:
					return True, message

			except requests.exceptions.HTTPError as e:
				message = self._handleHttpError(e, localPath, fileName, progressCallback, threadId)
				if message.startswith("Download completed"):
					return True, message

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
					success = self._waitForRetry(attempt, threadId)
					if not success:
						return False, "Download cancelled"
				else:
					return False, message

		return False, "Maximum retries exceeded"

	def _performSingleDownload(
		self,
		url: str,
		localPath: str,
		fileName: str,
		threadId: int,
		progressCallback: ProgressCallback | None,
	) -> tuple[bool, str]:
		"""
		Perform a single download attempt with resume support.

		:param url: Remote URL to download from.
		:param localPath: Local file path to save the downloaded file.
		:param fileName: Base name of the file for progress reporting.
		:param threadId: Current thread identifier for logging.
		:param progressCallback: Optional callback function for progress reporting.
		:return: Tuple of (success_flag, status_message).
		:raises requests.exceptions.HTTPError: When HTTP request fails.
		:raises requests.exceptions.RequestException: When network request fails.
		:raises Exception: When file operations or unexpected errors occur.
		"""
		# Check for existing partial file
		resumePos = self._getResumePosition(localPath, threadId)

		# Get response with resume support
		response = self._getDownloadResponse(url, resumePos, localPath, threadId)

		if self.cancelRequested:
			return False, "Download cancelled"

		try:
			# Determine total file size
			total = self._calculateTotalSize(response, resumePos)

			if total > 0:
				log.info(f"[Thread-{threadId}] Total file size: {total:,} bytes")

			# Download file content
			success, message = self._downloadFileContent(
				response,
				localPath,
				fileName,
				resumePos,
				total,
				progressCallback,
			)

			if not success:
				return False, message

			# Verify download integrity
			return self._verifyDownloadIntegrity(localPath, fileName, total, progressCallback, threadId)

		finally:
			response.close()

	def _getResumePosition(self, localPath: str, threadId: int) -> int:
		"""
		Get resume position for partial download.

		:param localPath: Local file path to check.
		:param threadId: Current thread identifier for logging.
		:return: Byte position to resume from.
		:raises OSError: When file operations fail.
		"""
		resumePos = 0
		if os.path.exists(localPath):
			resumePos = os.path.getsize(localPath)
			log.info(f"[Thread-{threadId}] Resuming from byte {resumePos}")
		return resumePos

	def _getDownloadResponse(self, url: str, resumePos: int, localPath: str, threadId: int):
		"""
		Get download response with resume support and redirect handling.

		:param url: Remote URL to download from.
		:param resumePos: Byte position to resume from.
		:param localPath: Local file path for cleanup if needed.
		:param threadId: Current thread identifier for logging.
		:return: HTTP response object.
		:raises requests.exceptions.HTTPError: When HTTP request fails.
		:raises requests.exceptions.RequestException: When network request fails.
		:raises Exception: When download is cancelled.
		"""
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

		# Check if resume is supported
		if resumePos > 0 and response.status_code != 206:
			log.info(f"[Thread-{threadId}] Server doesn't support resume, starting from beginning")
			if os.path.exists(localPath):
				try:
					os.remove(localPath)
				except OSError:
					pass

			if self.cancelRequested:
				response.close()
				raise Exception("Download cancelled")

			# Make new request without range header
			response.close()
			response = self.session.get(url, stream=True, timeout=30, allow_redirects=True)

		response.raise_for_status()
		return response

	def _calculateTotalSize(self, response, resumePos: int) -> int:
		"""
		Calculate total file size from HTTP response headers.

		:param response: HTTP response object.
		:param resumePos: Byte position resumed from.
		:return: Total file size in bytes.
		:raises ValueError: When Content-Range header is malformed.
		"""
		if response.status_code == 206:
			# Partial content response
			contentRange = response.headers.get("Content-Range", "")
			if contentRange and "/" in contentRange:
				return int(contentRange.split("/")[-1])
			else:
				return int(response.headers.get("Content-Length", "0")) + resumePos
		else:
			return int(response.headers.get("Content-Length", "0"))

	def _downloadFileContent(
		self,
		response,
		localPath: str,
		fileName: str,
		resumePos: int,
		total: int,
		progressCallback: ProgressCallback | None,
	) -> tuple[bool, str]:
		"""
		Download file content with progress reporting and cancellation support.

		:param response: HTTP response object to read from.
		:param localPath: Local file path to write to.
		:param fileName: Base name of the file for progress reporting.
		:param resumePos: Byte position resumed from.
		:param total: Total file size in bytes.
		:param progressCallback: Optional callback function for progress reporting.
		:return: Tuple of (success_flag, error_message).
		:raises OSError: When file write operations fail.
		:raises Exception: When download is cancelled or unexpected errors occur.
		"""
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
		except Exception as e:
			return False, f"Failed to write file: {str(e)}"

		return True, ""

	def _verifyDownloadIntegrity(
		self,
		localPath: str,
		fileName: str,
		total: int,
		progressCallback: ProgressCallback | None,
		threadId: int,
	) -> tuple[bool, str]:
		"""
		Verify download integrity and report final progress.

		:param localPath: Local file path to verify.
		:param fileName: Base name of the file for progress reporting.
		:param total: Expected total file size in bytes.
		:param progressCallback: Optional callback function for progress reporting.
		:param threadId: Current thread identifier for logging.
		:return: Tuple of (success_flag, status_message).
		:raises OSError: When file operations fail.
		"""
		if self.cancelRequested:
			return False, "Download cancelled"

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

	def _handleHttpError(
		self,
		e: requests.exceptions.HTTPError,
		localPath: str,
		fileName: str,
		progressCallback: ProgressCallback | None,
		threadId: int,
	) -> str:
		"""
		Handle HTTP errors with special handling for range not satisfiable.

		:param e: HTTP error exception.
		:param localPath: Local file path to check for completion.
		:param fileName: Base name of the file for progress reporting.
		:param progressCallback: Optional callback function for progress reporting.
		:param threadId: Current thread identifier for logging.
		:return: Error message or completion status.
		:raises OSError: When file operations fail.
		"""
		if e.response is not None and e.response.status_code == 416:  # Range Not Satisfiable
			if os.path.exists(localPath):
				actualSize = os.path.getsize(localPath)
				if actualSize > 0:
					log.info(f"[Thread-{threadId}] File appears to be complete: {localPath}")
					if progressCallback and not self.cancelRequested:
						progressCallback(fileName, actualSize, actualSize, 100.0)
					return "Download completed"

		return f"HTTP {e.response.status_code if e.response else 'Error'}: {str(e)}"

	def _waitForRetry(self, attempt: int, threadId: int) -> bool:
		"""
		Wait for retry with exponential backoff and cancellation support.

		:param attempt: Current retry attempt number.
		:param threadId: Current thread identifier for logging.
		:return: True if wait completed, False if cancelled.
		"""
		wait = BACKOFF_BASE**attempt
		log.info(f"[Thread-{threadId}] Waiting {wait}s before retry...")

		for _ in range(wait):
			if self.cancelRequested:
				return False
			time.sleep(1)

		return True

	def downloadModelsMultithreaded(
		self,
		modelsDir: str = _WritePaths().modelsDir,
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
			"preprocessor_config.json",
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

	def __del__(self):
		"""Clean up the session when the downloader is destroyed."""
		if hasattr(self, "session"):
			self.session.close()
