# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import dataclasses
import enum
import json
import os
import shutil
from datetime import datetime, timedelta

from logHandler import log
import requests

import addonAPIVersion
from typing import (
	Optional,
	List,
)
from .models import (
	_createModelFromData,
	AddonDetailsModel,
)


class Channel(str, enum.Enum):
	STABLE = "stable"
	BETA = "beta"
	ALL = "all"


def _getCurrentApiVersionForURL() -> str:
	currentVersion = addonAPIVersion.CURRENT
	year, major, minor = currentVersion
	return f"{year}.{major}.{minor}"


def _getAddonStoreURL(channel: Channel, lang: str, nvdaApiVersion: str) -> str:
	_baseURL = "https://nvaccess.org/addonStore/"
	return _baseURL + f"{lang}/{channel.value}/{nvdaApiVersion}.json"


@dataclasses.dataclass
class CachedAddonModel:
	availableAddons: List[AddonDetailsModel]
	cachedAt: datetime


class DataManager:
	_cacheFilename: str = "_cachedLatestAvailableAddons.json"
	_cachePeriod = timedelta(hours=6)

	def __init__(self, cacheDirLocation: os.PathLike):
		self._lang = "en"
		self._preferredChannel = Channel.ALL
		self._cacheFile = os.path.join(cacheDirLocation, DataManager._cacheFilename)
		self._addonDownloadCacheDir = cacheDirLocation
		self._availableAddonCache: Optional[CachedAddonModel] = self._getCachedAddonData()

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

	def _getCacheFilenameForAddon(self, addonData: AddonDetailsModel) -> str:
		return f"{addonData.addonId}-{addonData.versionName}.nvda-addon"

	def downloadAddonFile(self, addonData: AddonDetailsModel):
		localFilePath = os.path.join(
			self._addonDownloadCacheDir,
			self._getCacheFilenameForAddon(addonData)
		)
		try:
			with requests.get(addonData.addonURL, stream=True) as r:
				with open(localFilePath, 'wb') as f:
					shutil.copyfileobj(r.raw, f)
		except requests.exceptions.RequestException as e:
			log.debugWarning(f"Unable to download addon file: {e}")
			return None
		except OSError as e:
			log.debugWarning(f"Unable to save addon file ({localFilePath}): {e}")
			return None
		return localFilePath
