# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import dataclasses
import enum
import json
import os
import pathlib
from concurrent.futures import (
	Future,
	ThreadPoolExecutor
)
from datetime import datetime, timedelta

import buildVersion
from logHandler import log
import requests

import addonAPIVersion
import typing
from typing import (
	Optional,
	List,
	Dict,
	Callable,
	Tuple,
)
from .models import (
	_createModelFromData,
	AddonDetailsModel,
)


class Channel(str, enum.Enum):
	STABLE = "stable"
	BETA = "beta"
	ALL = "all"


def _workAroundForDevNVDAVersion() -> addonAPIVersion.AddonApiVersionT:
	"""When a 'latest' endpoint is created, this workaround method can be removed.
	"""
	log.debugWarning(
		"Workaround for Dev NVDA Version support with add-on store still in-place."
		"This workaround should be removed before merging to master / beta / rc"
	)
	version = buildVersion.version
	isNotPreMergeVersion = version[0].isdigit() or "alpha" in version or "beta" in version
	if isNotPreMergeVersion:
		# check if this gets merged accidentally.
		log.error("Fix the addonStore version used for API endpoint")
	return 2022, 2, 0  # hard-code for testing purposes.


def _getCurrentApiVersionForURL() -> str:
	# todo: replace with `currentVersion = addonAPIVersion.CURRENT`
	# The version is manually overridden until a 'latest' endpoint can be used for 'pre-release' versions
	# of NVDA
	currentVersion = _workAroundForDevNVDAVersion()
	year, major, minor = currentVersion
	return f"{year}.{major}.{minor}"


def _getAddonStoreURL(channel: Channel, lang: str, nvdaApiVersion: str) -> str:
	_baseURL = "https://nvaccess.org/addonStore/"
	return _baseURL + f"{lang}/{channel.value}/{nvdaApiVersion}.json"


@dataclasses.dataclass
class CachedAddonModel:
	availableAddons: List[AddonDetailsModel]
	cachedAt: datetime


class AddonFileDownloader:
	OnCompleteT = Callable[[AddonDetailsModel, Optional[os.PathLike]], None]

	def __init__(self, cacheDir: os.PathLike):
		self._cacheDir = cacheDir
		self.progress: Dict[AddonDetailsModel, int] = {}  # Number of chunks received
		self._pending: Dict[Future, Tuple[AddonDetailsModel, AddonFileDownloader.OnCompleteT]] = {}
		self.complete: Dict[AddonDetailsModel, os.PathLike] = {}  # Path to downloaded file
		self._executor = ThreadPoolExecutor(
			max_workers=1,
			thread_name_prefix="AddonDownloader",
		)

	def download(
			self,
			addonData: AddonDetailsModel,
			onComplete: OnCompleteT
	):
		self.progress[addonData] = 0
		f: Future = self._executor.submit(
			self._download, addonData,
		)
		self._pending[f] = addonData, onComplete
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
		if downloadAddonFuture.exception():
			log.error(f"Unhandled exception in _download", exc_info=downloadAddonFuture.exception())
			return
		addonData, onComplete = self._pending.pop(downloadAddonFuture)
		del self.progress[addonData]
		cacheFilePath: Optional[os.PathLike] = downloadAddonFuture.result()
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

	def _download(self, addonData: AddonDetailsModel) -> Optional[os.PathLike]:
		log.debug(f"starting download: {addonData.addonId}")
		cacheFilePath = os.path.join(
			self._cacheDir,
			self._getCacheFilenameForAddon(addonData)
		)
		inProgressFilePath = cacheFilePath + ".download"
		if addonData not in self.progress:
			log.debug("the download was cancelled before it started.")
			return None  # The download was cancelled
		try:
			with requests.get(addonData.addonURL, stream=True) as r:
				with open(inProgressFilePath, 'wb') as fd:
					# Most add-ons are small. This value was chosen quite arbitrarily, but with the intention to allow
					# interrupting the download. This is particularly important on a slow connection, to provide
					# a responsive UI when cancelling.
					# A size has been selected attempting to balance the maximum throughput, with responsiveness for
					# users with a slow connection.
					# This could be improved by dynamically adjusting the chunk size based on the time elapsed between
					# chunk, starting with small chunks and increasing up until a maximum wait time is reached.
					chunkSize = 128000
					for chunk in r.iter_content(chunk_size=chunkSize):
						log.debug(f"Chunk download: {addonData.addonId}")
						fd.write(chunk)
						if addonData in self.progress:  # Removed when the download should be cancelled.
							self.progress[addonData] += 1
						else:
							log.debug(f"Cancelled download: {addonData.addonId}")
							return None  # The download was cancelled
		except requests.exceptions.RequestException as e:
			log.debugWarning(f"Unable to download addon file: {e}")
			return None
		except OSError as e:
			log.debugWarning(f"Unable to save addon file ({inProgressFilePath}): {e}")
			return None
		log.debug(f"Download complete: {inProgressFilePath}")
		if os.path.exists(cacheFilePath):
			log.debug(f"Cache file already exists, deleting prior to rename: {cacheFilePath}")
			os.remove(cacheFilePath)
		os.rename(src=inProgressFilePath, dst=cacheFilePath)
		log.debug(f"Cache file available: {cacheFilePath}")
		return typing.cast(os.PathLike, cacheFilePath)

	@staticmethod
	def _getCacheFilenameForAddon(addonData: AddonDetailsModel) -> str:
		return f"{addonData.addonId}-{addonData.versionName}.nvda-addon"

	def __del__(self):
		if self._executor is not None:
			self._executor.shutdown(wait=False)
			self._executor = None


class DataManager:
	_cacheFilename: str = "_cachedLatestAvailableAddons.json"
	_cachePeriod = timedelta(hours=6)

	def __init__(self, userConfigLocation: os.PathLike):
		cacheDirLocation = os.path.join(userConfigLocation, "addonStore")
		self._lang = "en"
		self._preferredChannel = Channel.ALL
		self._cacheFile = os.path.join(cacheDirLocation, DataManager._cacheFilename)
		self._addonDownloadCacheDir = os.path.join(cacheDirLocation, "_dl")
		# ensure caching dirs exist
		pathlib.Path(cacheDirLocation).mkdir(parents=True, exist_ok=True)
		pathlib.Path(self._addonDownloadCacheDir).mkdir(parents=True, exist_ok=True)

		self._availableAddonCache: Optional[CachedAddonModel] = self._getCachedAddonData()

	def getFileDownloader(self) -> AddonFileDownloader:
		return AddonFileDownloader(self._addonDownloadCacheDir)

	def _getLatestAvailableAddonsData(self) -> Optional[bytes]:
		url = _getAddonStoreURL(self._preferredChannel, self._lang, _getCurrentApiVersionForURL())
		try:
			response = requests.get(url)
		except requests.exceptions.ConnectionError as e:
			log.debugWarning(f"Unable to fetch addon data: {e}")
			return None
		if response.status_code != requests.codes.OK:
			log.error(
				f"Unable to get data from API ({url}),"
				f" response ({response.status_code}): {response.content}"
			)
			return None
		return response.content

	def _cacheAddons(self, addonData: str, fetchTime: datetime):
		if not addonData:
			return
		cacheData = {
			"cacheDate": fetchTime.isoformat(),
			"data": addonData
		}
		with open(self._cacheFile, 'w') as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _getCachedAddonData(self) -> Optional[CachedAddonModel]:
		if not os.path.exists(self._cacheFile):
			return None
		with open(self._cacheFile, 'r') as cacheFile:
			cacheData = json.load(cacheFile)
		if not cacheData:
			return None
		fetchTime = datetime.fromisoformat(cacheData["cacheDate"])
		return CachedAddonModel(
			availableAddons=_createModelFromData(cacheData["data"]),
			cachedAt=fetchTime,
		)

	def getLatestAvailableAddons(self) -> List[AddonDetailsModel]:
		shouldRefreshData = (
			not self._availableAddonCache
			or DataManager._cachePeriod < (datetime.now() - self._availableAddonCache.cachedAt)
		)
		if shouldRefreshData:
			fetchTime = datetime.now()
			apiData = self._getLatestAvailableAddonsData()
			if apiData:
				decodedApiData = apiData.decode()
				self._cacheAddons(addonData=decodedApiData, fetchTime=fetchTime)
				self._availableAddonCache = CachedAddonModel(
					availableAddons=_createModelFromData(decodedApiData),
					cachedAt=fetchTime,
				)
		return self._availableAddonCache.availableAddons
