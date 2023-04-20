# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Needed for type hinting CaseInsensitiveDict
# Can be removed in a future version of python (3.8+)
from __future__ import annotations

import dataclasses
import globalVars
import json
import os
import pathlib
from concurrent.futures import (
	Future,
	ThreadPoolExecutor
)
from datetime import datetime, timedelta

from logHandler import log
import requests
from requests.structures import CaseInsensitiveDict

import addonAPIVersion
from typing import (
	cast,
	Optional,
	Dict,
	Callable,
	Tuple,
)
from .models import (
	Channel,
	_createStoreModelFromData,
	_createStoreCollectionFromJson,
	AddonStoreModel,
)

addonDataManager: Optional["_DataManager"] = None


def initialize():
	global addonDataManager
	log.debug("initializing addonStore data manager")
	addonDataManager = _DataManager()


def _getCurrentApiVersionForURL() -> str:
	year, major, minor = addonAPIVersion.CURRENT
	return f"{year}.{major}.{minor}"


def _getAddonStoreURL(channel: Channel, lang: str, nvdaApiVersion: str) -> str:
	_baseURL = "https://nvaccess.org/addonStore/"
	return _baseURL + f"{lang}/{channel.value}/{nvdaApiVersion}.json"


@dataclasses.dataclass
class CachedAddonsModel:
	availableAddons: CaseInsensitiveDict["AddonStoreModel"]
	"""
	Add-ons that have the same ID except differ in casing cause a path collision,
	as add-on IDs are installed to a case insensitive path.
	Therefore addon IDs should be treated as case insensitive.
	"""
	cachedAt: datetime
	nvdaAPIVersion: addonAPIVersion.AddonApiVersionT


class AddonFileDownloader:
	OnCompleteT = Callable[[AddonStoreModel, Optional[os.PathLike]], None]

	def __init__(self, cacheDir: os.PathLike):
		self._cacheDir = cacheDir
		self.progress: Dict[AddonStoreModel, int] = {}  # Number of chunks received
		self._pending: Dict[Future, Tuple[AddonStoreModel, AddonFileDownloader.OnCompleteT]] = {}
		self.complete: Dict[AddonStoreModel, os.PathLike] = {}  # Path to downloaded file
		self._executor = ThreadPoolExecutor(
			max_workers=1,
			thread_name_prefix="AddonDownloader",
		)

	def download(
			self,
			addonData: AddonStoreModel,
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

	def _download(self, addonData: AddonStoreModel) -> Optional[os.PathLike]:
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
			with requests.get(addonData.URL, stream=True) as r:
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
		# TODO: assert SHA256 sum
		return cast(os.PathLike, cacheFilePath)

	@staticmethod
	def _getCacheFilenameForAddon(addonData: AddonStoreModel) -> str:
		return f"{addonData.addonId}-{addonData.addonVersionName}.nvda-addon"

	def __del__(self):
		if self._executor is not None:
			self._executor.shutdown(wait=False)
			self._executor = None


class _DataManager:
	_cacheLatestFilename: str = "_cachedLatestAddons.json"
	_cacheCompatibleFilename: str = "_cachedCompatibleAddons.json"
	_cachePeriod = timedelta(hours=6)

	def __init__(self):
		cacheDirLocation = os.path.join(globalVars.appArgs.configPath, "addonStore")
		self._lang = "en"
		self._preferredChannel = Channel.ALL
		self._cacheLatestFile = os.path.join(cacheDirLocation, _DataManager._cacheLatestFilename)
		self._cacheCompatibleFile = os.path.join(cacheDirLocation, _DataManager._cacheCompatibleFilename)
		self._addonDownloadCacheDir = os.path.join(cacheDirLocation, "_dl")
		self._installedAddonDataCacheDir = os.path.join(cacheDirLocation, "addons")
		# ensure caching dirs exist
		pathlib.Path(cacheDirLocation).mkdir(parents=True, exist_ok=True)
		pathlib.Path(self._addonDownloadCacheDir).mkdir(parents=True, exist_ok=True)
		pathlib.Path(self._installedAddonDataCacheDir).mkdir(parents=True, exist_ok=True)

		self._latestAddonCache = self._getCachedAddonData(self._cacheLatestFile)
		self._compatibleAddonCache = self._getCachedAddonData(self._cacheCompatibleFile)

	def getFileDownloader(self) -> AddonFileDownloader:
		return AddonFileDownloader(self._addonDownloadCacheDir)

	def _getLatestAddonsDataForVersion(self, apiVersion: str) -> Optional[bytes]:
		url = _getAddonStoreURL(self._preferredChannel, self._lang, apiVersion)
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

	def _cacheCompatibleAddons(self, addonData: str, fetchTime: datetime):
		if not addonData:
			return
		cacheData = {
			"cacheDate": fetchTime.isoformat(),
			"data": addonData,
			"nvdaAPIVersion": addonAPIVersion.CURRENT,
		}
		with open(self._cacheCompatibleFile, 'w') as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _cacheLatestAddons(self, addonData: str, fetchTime: datetime):
		if not addonData:
			return
		cacheData = {
			"cacheDate": fetchTime.isoformat(),
			"data": addonData,
			"nvdaAPIVersion": addonAPIVersion.LATEST,
		}
		with open(self._cacheLatestFile, 'w') as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _getCachedAddonData(self, cacheFilePath: str) -> Optional[CachedAddonsModel]:
		if not os.path.exists(cacheFilePath):
			return None
		with open(cacheFilePath, 'r') as cacheFile:
			cacheData = json.load(cacheFile)
		if not cacheData:
			return None
		fetchTime = datetime.fromisoformat(cacheData["cacheDate"])
		return CachedAddonsModel(
			availableAddons=_createStoreCollectionFromJson(cacheData["data"]),
			cachedAt=fetchTime,
			nvdaAPIVersion=cacheData["nvdaAPIVersion"],
		)

	def getLatestCompatibleAddons(self) -> CaseInsensitiveDict["AddonStoreModel"]:
		shouldRefreshData = (
			not self._compatibleAddonCache
			or self._compatibleAddonCache.nvdaAPIVersion != addonAPIVersion.CURRENT
			or _DataManager._cachePeriod < (datetime.now() - self._compatibleAddonCache.cachedAt)
		)
		if shouldRefreshData:
			fetchTime = datetime.now()
			apiData = self._getLatestAddonsDataForVersion(_getCurrentApiVersionForURL())
			if apiData:
				decodedApiData = apiData.decode()
				self._cacheCompatibleAddons(
					addonData=decodedApiData,
					fetchTime=fetchTime,
				)
				self._compatibleAddonCache = CachedAddonsModel(
					availableAddons=_createStoreCollectionFromJson(decodedApiData),
					cachedAt=fetchTime,
					nvdaAPIVersion=addonAPIVersion.CURRENT,
				)
		return self._compatibleAddonCache.availableAddons

	def getLatestAddons(self) -> CaseInsensitiveDict["AddonStoreModel"]:
		shouldRefreshData = (
			not self._latestAddonCache
			or _DataManager._cachePeriod < (datetime.now() - self._latestAddonCache.cachedAt)
		)
		if shouldRefreshData:
			fetchTime = datetime.now()
			apiData = self._getLatestAddonsDataForVersion(addonAPIVersion.LATEST)
			if apiData:
				decodedApiData = apiData.decode()
				self._cacheLatestAddons(
					addonData=decodedApiData,
					fetchTime=fetchTime,
				)
				self._latestAddonCache = CachedAddonsModel(
					availableAddons=_createStoreCollectionFromJson(decodedApiData),
					cachedAt=fetchTime,
					nvdaAPIVersion=addonAPIVersion.LATEST,
				)
		return self._latestAddonCache.availableAddons

	def _cacheInstalledAddon(self, addonData: AddonStoreModel):
		if not addonData:
			return
		addonCachePath = os.path.join(self._installedAddonDataCacheDir, f"{addonData.addonId}.json")
		with open(addonCachePath, 'w') as cacheFile:
			json.dump(addonData.asdict(), cacheFile, ensure_ascii=False)

	def _getCachedInstalledAddonData(self, addonId: str) -> Optional[AddonStoreModel]:
		addonCachePath = os.path.join(self._installedAddonDataCacheDir, f"{addonId}.json")
		if not os.path.exists(addonCachePath):
			return None
		with open(addonCachePath, 'r') as cacheFile:
			cacheData = json.load(cacheFile)
		if not cacheData:
			return None
		return _createStoreModelFromData(cacheData)
