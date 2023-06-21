# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from concurrent.futures import (
	Future,
	ThreadPoolExecutor,
)
import os
import pathlib
from typing import (
	TYPE_CHECKING,
	cast,
	Callable,
	Dict,
	Optional,
	Tuple,
)

import requests

import addonAPIVersion
from core import callLater
from logHandler import log
import NVDAState
from NVDAState import WritePaths
from utils.security import sha256_checksum

from .models.addon import AddonStoreModel
from .models.channel import Channel


if TYPE_CHECKING:
	from gui.message import DisplayableError


_LATEST_API_VER = "latest"
"""
A string value used in the add-on store to fetch the latest version of all add-ons,
i.e include older incompatible versions.
"""


def _getCurrentApiVersionForURL() -> str:
	year, major, minor = addonAPIVersion.CURRENT
	return f"{year}.{major}.{minor}"


def _getAddonStoreURL(channel: Channel, lang: str, nvdaApiVersion: str) -> str:
	_baseURL = "https://nvaccess.org/addonStore/"
	return _baseURL + f"{lang}/{channel.value}/{nvdaApiVersion}.json"


class AddonFileDownloader:
	OnCompleteT = Callable[[AddonStoreModel, Optional[os.PathLike]], None]

	def __init__(self):
		self.progress: Dict[AddonStoreModel, int] = {}  # Number of chunks received
		self._pending: Dict[
			Future,
			Tuple[
				AddonStoreModel,
				AddonFileDownloader.OnCompleteT,
				"DisplayableError.OnDisplayableErrorT"
			]
		] = {}
		self.complete: Dict[AddonStoreModel, os.PathLike] = {}  # Path to downloaded file
		self._executor = ThreadPoolExecutor(
			max_workers=1,
			thread_name_prefix="AddonDownloader",
		)

		if NVDAState.shouldWriteToDisk():
			# ensure downloads dir exist
			pathlib.Path(WritePaths.addonStoreDownloadDir).mkdir(parents=True, exist_ok=True)

	def download(
			self,
			addonData: AddonStoreModel,
			onComplete: OnCompleteT,
			onDisplayableError: "DisplayableError.OnDisplayableErrorT",
	):
		self.progress[addonData] = 0
		f: Future = self._executor.submit(
			self._download, addonData,
		)
		self._pending[f] = addonData, onComplete, onDisplayableError
		f.add_done_callback(self._done)

	def _done(self, downloadAddonFuture: Future):
		isCancelled = downloadAddonFuture not in self._pending
		addonId = "CANCELLED" if isCancelled else self._pending[downloadAddonFuture][0].addonId
		log.debug(f"Done called for {addonId}")
		if isCancelled:
			log.debug("Download was cancelled, not calling onComplete")
			return
		if not downloadAddonFuture.done() or downloadAddonFuture.cancelled():
			log.error("Logic error with download in BG thread.")
			return
		addonData, onComplete, onDisplayableError = self._pending[downloadAddonFuture]
		downloadAddonFutureException = downloadAddonFuture.exception()
		if downloadAddonFutureException:
			cacheFilePath = None
			from gui.message import DisplayableError
			if not isinstance(downloadAddonFutureException, DisplayableError):
				log.error(f"Unhandled exception in _download", exc_info=downloadAddonFuture.exception())
			else:
				callLater(
					delay=0,
					callable=onDisplayableError.notify,
					displayableError=downloadAddonFutureException
				)
		else:
			cacheFilePath: Optional[os.PathLike] = downloadAddonFuture.result()

		del self._pending[downloadAddonFuture]
		del self.progress[addonData]
		self.complete[addonData] = cacheFilePath
		onComplete(addonData, cacheFilePath)

	def cancelAll(self):
		log.debug("Cancelling all")
		for f in self._pending.keys():
			f.cancel()
		self._executor.shutdown(wait=False)
		self._executor = None
		self.progress.clear()
		self._pending.clear()

	def _downloadAddonToPath(self, addonData: AddonStoreModel, downloadFilePath: str) -> bool:
		"""
		@return: True if the add-on is downloaded successfully,
		False if the download is cancelled
		"""
		if not NVDAState.shouldWriteToDisk():
			return False

		with requests.get(addonData.URL, stream=True) as r:
			with open(downloadFilePath, 'wb') as fd:
				# Most add-ons are small. This value was chosen quite arbitrarily, but with the intention to allow
				# interrupting the download. This is particularly important on a slow connection, to provide
				# a responsive UI when cancelling.
				# A size has been selected attempting to balance the maximum throughput, with responsiveness for
				# users with a slow connection.
				# This could be improved by dynamically adjusting the chunk size based on the time elapsed between
				# chunk, starting with small chunks and increasing up until a maximum wait time is reached.
				chunkSize = 128000
				for chunk in r.iter_content(chunk_size=chunkSize):
					fd.write(chunk)
					if addonData in self.progress:  # Removed when the download should be cancelled.
						self.progress[addonData] += 1
					else:
						log.debug(f"Cancelled download: {addonData.addonId}")
						return False  # The download was cancelled
		return True

	def _download(self, addonData: AddonStoreModel) -> Optional[os.PathLike]:
		from gui.message import DisplayableError
		# Translators: A title for a dialog notifying a user of an add-on download failure.
		_addonDownloadFailureMessageTitle = pgettext("addonStore", "Add-on download failure")

		log.debug(f"starting download: {addonData.addonId}")
		cacheFilePath = addonData.cachedDownloadPath
		if os.path.exists(cacheFilePath):
			log.debug(f"Cache file already exists, deleting {cacheFilePath}")
			os.remove(cacheFilePath)

		inProgressFilePath = addonData.tempDownloadPath
		if addonData not in self.progress:
			log.debug("the download was cancelled before it started.")
			return None  # The download was cancelled
		try:
			if not self._downloadAddonToPath(addonData, inProgressFilePath):
				return None  # The download was cancelled
		except requests.exceptions.RequestException as e:
			log.debugWarning(f"Unable to download addon file: {e}")
			raise DisplayableError(
				pgettext(
					"addonStore",
					# Translators: A message to the user if an add-on download fails
					"Unable to download add-on: {name}"
				).format(name=addonData.displayName),
				_addonDownloadFailureMessageTitle,
			)
		except OSError as e:
			log.debugWarning(f"Unable to save addon file ({inProgressFilePath}): {e}")
			raise DisplayableError(
				pgettext(
					"addonStore",
					# Translators: A message to the user if an add-on download fails
					"Unable to save add-on as a file: {name}"
				).format(name=addonData.displayName),
				_addonDownloadFailureMessageTitle,
			)
		if not self._checkChecksum(inProgressFilePath, addonData):
			os.remove(inProgressFilePath)
			log.debugWarning(f"Cache file deleted, checksum mismatch: {inProgressFilePath}")
			raise DisplayableError(
				pgettext(
					"addonStore",
					# Translators: A message to the user if an add-on download is not safe
					"Add-on download not safe: checksum failed for {name}"
				).format(name=addonData.displayName),
				_addonDownloadFailureMessageTitle,
			)
		log.debug(f"Download complete: {inProgressFilePath}")
		os.rename(src=inProgressFilePath, dst=cacheFilePath)
		log.debug(f"Cache file available: {cacheFilePath}")
		return cast(os.PathLike, cacheFilePath)

	@staticmethod
	def _checkChecksum(addonFilePath: str, addonData: AddonStoreModel) -> Optional[os.PathLike]:
		with open(addonFilePath, "rb") as f:
			sha256Addon = sha256_checksum(f)
		return sha256Addon.casefold() == addonData.sha256.casefold()

	@staticmethod
	def _getCacheFilenameForAddon(addonData: AddonStoreModel) -> str:
		return f"{addonData.addonId}-{addonData.addonVersionName}.nvda-addon"

	def __del__(self):
		if self._executor is not None:
			self._executor.shutdown(wait=False)
			self._executor = None
