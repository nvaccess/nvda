# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2026 NV Access Limited, Cary-rowen
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

from concurrent.futures import (
	Future,
	ThreadPoolExecutor,
)
import os
import pathlib
import shutil
from typing import (
	TYPE_CHECKING,
	cast,
	Callable,
	NamedTuple,
)

import requests

import addonAPIVersion
from core import callLater
from logHandler import log
import NVDAState
from NVDAState import WritePaths
import threading
from utils.security import sha256_checksum
from config import conf

from .models.addon import (
	_AddonGUIModel,
	_AddonStoreModel,
)
from .models.channel import Channel


if TYPE_CHECKING:
	from gui.message import DisplayableError
	from gui.addonStoreGui.viewModels.addonList import AddonListItemVM


_DEFAULT_BASE_URL = "https://addonStore.nvaccess.org"
_LATEST_API_VER = "latest"
"""
A string value used in the add-on store to fetch the latest version of all add-ons,
i.e include older incompatible versions.
"""


def _getBaseURL() -> str:
	if url := conf["addonStore"]["baseServerURL"]:
		return url
	return _DEFAULT_BASE_URL


def _getCurrentApiVersionForURL() -> str:
	year, major, minor = addonAPIVersion.CURRENT
	return f"{year}.{major}.{minor}"


def _getAddonStoreURL(channel: Channel, lang: str, nvdaApiVersion: str) -> str:
	return f"{_getBaseURL()}/{lang}/{channel.value}/{nvdaApiVersion}.json"


def _getCacheHashURL() -> str:
	return f"{_getBaseURL()}/cacheHash.json"


_TempDownloadPathT = str


class _PendingDownload(NamedTuple):
	addonData: "AddonListItemVM[_AddonStoreModel]"
	tempDownloadPath: _TempDownloadPathT
	onComplete: Callable[
		["AddonListItemVM[_AddonStoreModel]", os.PathLike | None],
		None,
	]
	onDisplayableError: "DisplayableError.OnDisplayableErrorT"


class AddonFileDownloader:
	OnCompleteT = Callable[
		["AddonListItemVM[_AddonStoreModel]", os.PathLike | None],
		None,
	]

	DOWNLOAD_LOCK = threading.RLock()
	"""Used to protect cross-thread download management.

	Notably:
	- tracking download progress: AddonFileDownloader.progress
	- writes/reads to temporary add-on download files
	"""

	def __init__(self):
		self.progress: dict["AddonListItemVM[_AddonStoreModel]", int] = {}
		"""
		Counts chunks received in a download of an add-on.

		Usage should be protected by AddonFileDownloader.DOWNLOAD_LOCK.
		"""

		self._activeDownloadPaths: dict["AddonListItemVM[_AddonStoreModel]", _TempDownloadPathT] = {}
		"""
		Tracks the temporary path for the current download attempt for an add-on.

		Usage should be protected by AddonFileDownloader.DOWNLOAD_LOCK.
		"""

		self._pending: dict[Future[os.PathLike | None], _PendingDownload] = {}
		self.complete: dict[
			"AddonListItemVM[_AddonStoreModel]",
			# Path to downloaded file
			os.PathLike | None,
		] = {}
		self._executor: ThreadPoolExecutor | None = self._createExecutor()
		self._downloadAttemptCount: int = 0
		self._prepareDownloadDir(shouldClearExisting=True)

	@staticmethod
	def _createExecutor() -> ThreadPoolExecutor:
		return ThreadPoolExecutor(
			max_workers=10,
			thread_name_prefix="AddonDownloader",
		)

	@staticmethod
	def _prepareDownloadDir(shouldClearExisting: bool = False) -> None:
		"""Ensure the temporary download directory exists, optionally clearing stale contents."""
		with AddonFileDownloader.DOWNLOAD_LOCK:
			if not NVDAState.shouldWriteToDisk():
				return
			if shouldClearExisting and os.path.exists(WritePaths.addonStoreDownloadDir):
				try:
					shutil.rmtree(WritePaths.addonStoreDownloadDir)
				except OSError:
					log.error(
						f"Failed to remove addon store download directory: {WritePaths.addonStoreDownloadDir}",
						exc_info=True,
					)
			pathlib.Path(WritePaths.addonStoreDownloadDir).mkdir(parents=True, exist_ok=True)

	def _ensureDownloadResources(self) -> None:
		"""Recreate downloader resources after cancellation so the instance can be reused."""
		with self.DOWNLOAD_LOCK:
			if self._executor is None:
				self._executor = self._createExecutor()
			if not os.path.exists(WritePaths.addonStoreDownloadDir):
				self._prepareDownloadDir()

	def _createTempDownloadPath(
		self,
		addonData: "AddonListItemVM[_AddonStoreModel]",
	) -> _TempDownloadPathT:
		self._downloadAttemptCount += 1
		return f"{addonData.model.tempDownloadPath}.{self._downloadAttemptCount}"

	def _isDownloadActive(
		self,
		addonData: "AddonListItemVM[_AddonStoreModel]",
		tempDownloadPath: _TempDownloadPathT,
	) -> bool:
		return addonData in self.progress and self._activeDownloadPaths.get(addonData) == tempDownloadPath

	def _removeActiveDownloadPath(self, pendingDownload: _PendingDownload) -> None:
		if self._activeDownloadPaths.get(pendingDownload.addonData) == pendingDownload.tempDownloadPath:
			self._activeDownloadPaths.pop(pendingDownload.addonData, None)

	def _cleanupCancelledDownload(self, pendingDownload: _PendingDownload) -> None:
		try:
			with self.DOWNLOAD_LOCK:
				# If the download was cancelled, the file may have been partially downloaded.
				os.remove(pendingDownload.tempDownloadPath)
		except FileNotFoundError:
			pass
		except Exception:
			log.exception("Error while deleting partially downloaded file")

	def download(
		self,
		addonData: "AddonListItemVM[_AddonStoreModel]",
		onComplete: OnCompleteT,
		onDisplayableError: "DisplayableError.OnDisplayableErrorT",
	):
		with self.DOWNLOAD_LOCK:
			self._ensureDownloadResources()
			tempDownloadPath = self._createTempDownloadPath(addonData)
			# Initialize progress for this download before submitting the task,
			# so the download can still be cancelled before the worker starts.
			self.progress[addonData] = 0
			self._activeDownloadPaths[addonData] = tempDownloadPath
			assert self._executor is not None
			f: Future[os.PathLike | None] = self._executor.submit(
				self._download,
				addonData,
				tempDownloadPath,
			)
			self._pending[f] = _PendingDownload(
				addonData=addonData,
				tempDownloadPath=tempDownloadPath,
				onComplete=onComplete,
				onDisplayableError=onDisplayableError,
			)
			f.add_done_callback(self._done)

	def _done(self, downloadAddonFuture: Future[os.PathLike | None]):
		with self.DOWNLOAD_LOCK:
			pendingDownload = self._pending.pop(downloadAddonFuture, None)
			isCancelled = (
				pendingDownload is None
				or downloadAddonFuture.cancelled()
				or not self._isDownloadActive(
					pendingDownload.addonData,
					pendingDownload.tempDownloadPath,
				)
			)
		addonId = (
			"CANCELLED" if isCancelled or pendingDownload is None else pendingDownload.addonData.model.addonId
		)
		log.debug(f"Done called for {addonId}")

		if not downloadAddonFuture.done():
			log.error("Logic error with download in BG thread.")
			isCancelled = True

		if isCancelled:
			log.debug("Download was cancelled, not calling onComplete")
			if pendingDownload is not None:
				with self.DOWNLOAD_LOCK:
					self._removeActiveDownloadPath(pendingDownload)
				self._cleanupCancelledDownload(pendingDownload)
			return

		assert pendingDownload is not None
		addonData = pendingDownload.addonData
		downloadAddonFutureException = downloadAddonFuture.exception()
		cacheFilePath: os.PathLike | None
		if downloadAddonFutureException:
			cacheFilePath = None
			from gui.message import DisplayableError

			if not isinstance(downloadAddonFutureException, DisplayableError):
				log.exception("Unhandled exception in _download", exc_info=downloadAddonFutureException)
			else:
				callLater(
					delay=0,
					callable=pendingDownload.onDisplayableError.notify,
					displayableError=downloadAddonFutureException,
				)
		else:
			cacheFilePath = downloadAddonFuture.result()

		# If canceled after our previous isCancelled check,
		# then _activeDownloadPaths will contain a different download attempt or be empty.
		with self.DOWNLOAD_LOCK:
			if not self._isDownloadActive(addonData, pendingDownload.tempDownloadPath):
				log.debug("Download was cancelled, not calling onComplete")
				self._cleanupCancelledDownload(pendingDownload)
				return
			self._removeActiveDownloadPath(pendingDownload)
			self.progress.pop(addonData, None)
			self.complete[addonData] = cacheFilePath
		pendingDownload.onComplete(addonData, cacheFilePath)

	def cancelAll(self):
		log.debug("Cancelling all")
		with self.DOWNLOAD_LOCK:
			futuresCopy = tuple(self._pending.keys())
			for f in futuresCopy:
				f.cancel()
			if self._executor is not None:
				self._executor.shutdown(wait=False)
				self._executor = None
			self._activeDownloadPaths.clear()
			self.progress.clear()
			if NVDAState.shouldWriteToDisk() and os.path.exists(WritePaths.addonStoreDownloadDir):
				try:
					shutil.rmtree(WritePaths.addonStoreDownloadDir)
				except OSError:
					log.error(
						f"Failed to remove addon store download directory: {WritePaths.addonStoreDownloadDir}",
						exc_info=True,
					)

	def _downloadAddonToPath(
		self,
		addonData: "AddonListItemVM[_AddonStoreModel]",
		tempDownloadPath: _TempDownloadPathT,
	) -> bool:
		"""
		@return: True if the add-on is downloaded successfully,
		False if the download is cancelled
		"""
		if not NVDAState.shouldWriteToDisk():
			log.error("Should not write to disk, cancelling download")
			return False

		# Some add-ons are quite large, so we need to allow for a long download time.
		# 1GB at 0.5 MB/s takes 4.5hr to download.
		MAX_ADDON_DOWNLOAD_TIME = 60 * 60 * 6  # 6 hours
		with requests.get(addonData.model.URL, stream=True, timeout=MAX_ADDON_DOWNLOAD_TIME) as r:
			with open(tempDownloadPath, "wb") as fd:
				# Most add-ons are small. This value was chosen quite arbitrarily, but with the intention to allow
				# interrupting the download. This is particularly important on a slow connection, to provide
				# a responsive UI when cancelling.
				# A size has been selected attempting to balance the maximum throughput, with responsiveness for
				# users with a slow connection.
				# This could be improved by dynamically adjusting the chunk size based on the time elapsed between
				# chunk, starting with small chunks and increasing up until a maximum wait time is reached.
				chunkSize = 128000
				for chunk in r.iter_content(chunk_size=chunkSize):
					with self.DOWNLOAD_LOCK:
						if not self._isDownloadActive(addonData, tempDownloadPath):
							log.debug(f"Cancelled download: {addonData.model.addonId}")
							return False  # The download was cancelled
						fd.write(chunk)
						self.progress[addonData] += 1
		return True

	def _download(
		self,
		listItem: "AddonListItemVM[_AddonStoreModel]",
		tempDownloadPath: _TempDownloadPathT,
	) -> os.PathLike | None:
		from gui.message import DisplayableError

		# Translators: A title for a dialog notifying a user of an add-on download failure.
		_addonDownloadFailureMessageTitle = pgettext("addonStore", "Add-on download failure")

		addonData = listItem.model
		log.debug(f"starting download: {addonData.addonId}")
		cacheFilePath = addonData.cachedDownloadPath
		inProgressFilePath = tempDownloadPath
		with self.DOWNLOAD_LOCK:
			if not self._isDownloadActive(listItem, tempDownloadPath):
				log.debug("the download was cancelled before it started.")
				return None  # The download was cancelled
			if os.path.exists(cacheFilePath):
				log.debug(f"Cache file already exists, deleting {cacheFilePath}")
				os.remove(cacheFilePath)
		try:
			if not self._downloadAddonToPath(listItem, tempDownloadPath):
				return None  # The download was cancelled
		except requests.exceptions.RequestException as e:
			log.debugWarning(f"Unable to download addon file: {e}")
			raise DisplayableError(
				pgettext(
					"addonStore",
					# Translators: A message to the user if an add-on download fails
					"Unable to download add-on: {name}",
				).format(name=addonData.displayName),
				_addonDownloadFailureMessageTitle,
			)
		except OSError as e:
			log.debugWarning(f"Unable to save addon file ({inProgressFilePath}): {e}")
			raise DisplayableError(
				pgettext(
					"addonStore",
					# Translators: A message to the user if an add-on download fails
					"Unable to save add-on as a file: {name}",
				).format(name=addonData.displayName),
				_addonDownloadFailureMessageTitle,
			)
		with self.DOWNLOAD_LOCK:
			if not self._isDownloadActive(listItem, tempDownloadPath):
				log.debug(f"Cancelled download: {addonData.addonId}")
				return None
		if not self._checkChecksum(inProgressFilePath, addonData):
			with self.DOWNLOAD_LOCK:
				os.remove(inProgressFilePath)
			log.debugWarning(f"Cache file deleted, checksum mismatch: {inProgressFilePath}")
			raise DisplayableError(
				pgettext(
					"addonStore",
					# Translators: A message to the user if an add-on download is not safe
					"Add-on download not safe: checksum failed for {name}",
				).format(name=addonData.displayName),
				_addonDownloadFailureMessageTitle,
			)
		log.debug(f"Download complete: {inProgressFilePath}")
		with self.DOWNLOAD_LOCK:
			if not self._isDownloadActive(listItem, tempDownloadPath):
				log.debug(f"Cancelled download: {addonData.addonId}")
				return None
			os.replace(src=inProgressFilePath, dst=cacheFilePath)
		log.debug(f"Cache file available: {cacheFilePath}")
		return cast(os.PathLike, cacheFilePath)

	@staticmethod
	def _checkChecksum(addonFilePath: str, addonData: _AddonStoreModel) -> bool:
		with AddonFileDownloader.DOWNLOAD_LOCK:
			with open(addonFilePath, "rb") as f:
				sha256Addon = sha256_checksum(f)
		return sha256Addon.casefold() == addonData.sha256.casefold()

	@staticmethod
	def _getCacheFilenameForAddon(addonData: _AddonGUIModel) -> str:
		return f"{addonData.addonId}-{addonData.addonVersionName}.nvda-addon"

	def __del__(self):
		if self._executor is not None:
			self._executor.shutdown(wait=False)
			self._executor = None
