# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2023 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Needed for type hinting CaseInsensitiveDict
# Can be removed in a future version of python (3.8+)
from __future__ import annotations

from datetime import datetime, timedelta
import json
import os
import pathlib
import threading
from typing import (
	TYPE_CHECKING,
	Optional,
	Set,
	Tuple,
)

import requests
from requests.structures import CaseInsensitiveDict

import addonAPIVersion
from baseObject import AutoPropertyObject
import config
from core import callLater
import languageHandler
from logHandler import log
import NVDAState
from NVDAState import WritePaths

from .models.addon import (
	AddonStoreModel,
	CachedAddonsModel,
	_createAddonGUICollection,
	_createStoreModelFromData,
	_createStoreCollectionFromJson,
)
from .models.channel import Channel
from .network import (
	_getAddonStoreURL,
	_getCurrentApiVersionForURL,
	_LATEST_API_VER,
)

if TYPE_CHECKING:
	from addonHandler import Addon as AddonHandlerModel  # noqa: F401
	# AddonGUICollectionT must only be imported when TYPE_CHECKING
	from .models.addon import AddonGUICollectionT  # noqa: F401
	from gui._addonStoreGui.viewModels.addonList import AddonListItemVM  # noqa: F401
	from gui.message import DisplayableError  # noqa: F401


addonDataManager: Optional["_DataManager"] = None


def initialize():
	global addonDataManager
	if config.isAppX:
		log.info("Add-ons not supported when running as a Windows Store application")
		return
	log.debug("initializing addonStore data manager")
	addonDataManager = _DataManager()


class _DataManager:
	_cacheLatestFilename: str = "_cachedLatestAddons.json"
	_cacheCompatibleFilename: str = "_cachedCompatibleAddons.json"
	_cachePeriod = timedelta(hours=6)
	_downloadsPendingInstall: Set[Tuple["AddonListItemVM", os.PathLike]] = set()

	def __init__(self):
		self._lang = languageHandler.getLanguage()
		self._preferredChannel = Channel.ALL
		self._cacheLatestFile = os.path.join(WritePaths.addonStoreDir, _DataManager._cacheLatestFilename)
		self._cacheCompatibleFile = os.path.join(WritePaths.addonStoreDir, _DataManager._cacheCompatibleFilename)
		self._installedAddonDataCacheDir = WritePaths.addonsDir

		if NVDAState.shouldWriteToDisk():
			# ensure caching dirs exist
			pathlib.Path(WritePaths.addonStoreDir).mkdir(parents=True, exist_ok=True)
			pathlib.Path(self._installedAddonDataCacheDir).mkdir(parents=True, exist_ok=True)

		self._latestAddonCache = self._getCachedAddonData(self._cacheLatestFile)
		self._compatibleAddonCache = self._getCachedAddonData(self._cacheCompatibleFile)
		self._installedAddonsCache = _InstalledAddonsCache()
		# Fetch available add-ons cache early
		threading.Thread(
			target=self.getLatestCompatibleAddons,
			name="initialiseAvailableAddons",
		).start()

	def _getLatestAddonsDataForVersion(self, apiVersion: str) -> Optional[bytes]:
		url = _getAddonStoreURL(self._preferredChannel, self._lang, apiVersion)
		try:
			response = requests.get(url)
		except requests.exceptions.RequestException as e:
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
		if not NVDAState.shouldWriteToDisk():
			return
		if not addonData:
			return
		cacheData = {
			"cacheDate": fetchTime.isoformat(),
			"data": addonData,
			"cachedLanguage": self._lang,
			"nvdaAPIVersion": addonAPIVersion.CURRENT,
		}
		with open(self._cacheCompatibleFile, 'w') as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _cacheLatestAddons(self, addonData: str, fetchTime: datetime):
		if not NVDAState.shouldWriteToDisk():
			return
		if not addonData:
			return
		cacheData = {
			"cacheDate": fetchTime.isoformat(),
			"data": addonData,
			"cachedLanguage": self._lang,
			"nvdaAPIVersion": _LATEST_API_VER,
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
			cachedAddonData=_createStoreCollectionFromJson(cacheData["data"]),
			cachedAt=fetchTime,
			cachedLanguage=cacheData["cachedLanguage"],
			nvdaAPIVersion=tuple(cacheData["nvdaAPIVersion"]),  # loads as list
		)

	# Translators: A title of the dialog shown when fetching add-on data from the store fails
	_updateFailureMessage = pgettext("addonStore", "Add-on data update failure")

	def getLatestCompatibleAddons(
			self,
			onDisplayableError: Optional[DisplayableError.OnDisplayableErrorT] = None,
	) -> "AddonGUICollectionT":
		shouldRefreshData = (
			not self._compatibleAddonCache
			or self._compatibleAddonCache.nvdaAPIVersion != addonAPIVersion.CURRENT
			or _DataManager._cachePeriod < (datetime.now() - self._compatibleAddonCache.cachedAt)
			or self._compatibleAddonCache.cachedLanguage != self._lang
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
					cachedAddonData=_createStoreCollectionFromJson(decodedApiData),
					cachedAt=fetchTime,
					cachedLanguage=self._lang,
					nvdaAPIVersion=addonAPIVersion.CURRENT,
				)
			elif onDisplayableError is not None:
				from gui.message import DisplayableError
				displayableError = DisplayableError(
					# Translators: A message shown when fetching add-on data from the store fails
					pgettext("addonStore", "Unable to fetch latest add-on data for compatible add-ons."),
					self._updateFailureMessage,
				)
				callLater(delay=0, callable=onDisplayableError.notify, displayableError=displayableError)

		if self._compatibleAddonCache is None:
			return _createAddonGUICollection()
		return self._compatibleAddonCache.cachedAddonData

	def getLatestAddons(
			self,
			onDisplayableError: Optional[DisplayableError.OnDisplayableErrorT] = None,
	) -> "AddonGUICollectionT":
		shouldRefreshData = (
			not self._latestAddonCache
			or _DataManager._cachePeriod < (datetime.now() - self._latestAddonCache.cachedAt)
			or self._latestAddonCache.cachedLanguage != self._lang
		)
		if shouldRefreshData:
			fetchTime = datetime.now()
			apiData = self._getLatestAddonsDataForVersion(_LATEST_API_VER)
			if apiData:
				decodedApiData = apiData.decode()
				self._cacheLatestAddons(
					addonData=decodedApiData,
					fetchTime=fetchTime,
				)
				self._latestAddonCache = CachedAddonsModel(
					cachedAddonData=_createStoreCollectionFromJson(decodedApiData),
					cachedAt=fetchTime,
					cachedLanguage=self._lang,
					nvdaAPIVersion=_LATEST_API_VER,
				)
			elif onDisplayableError is not None:
				from gui.message import DisplayableError
				displayableError = DisplayableError(
					# Translators: A message shown when fetching add-on data from the store fails
					pgettext("addonStore", "Unable to fetch latest add-on data for incompatible add-ons."),
					self._updateFailureMessage
				)
				callLater(delay=0, callable=onDisplayableError.notify, displayableError=displayableError)

		if self._latestAddonCache is None:
			return _createAddonGUICollection()
		return self._latestAddonCache.cachedAddonData

	def _deleteCacheInstalledAddon(self, addonId: str):
		addonCachePath = os.path.join(self._installedAddonDataCacheDir, f"{addonId}.json")
		if pathlib.Path(addonCachePath).exists():
			os.remove(addonCachePath)

	def _cacheInstalledAddon(self, addonData: AddonStoreModel):
		if not NVDAState.shouldWriteToDisk():
			return
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


class _InstalledAddonsCache(AutoPropertyObject):
	cachePropertiesByDefault = True

	installedAddons: CaseInsensitiveDict["AddonHandlerModel"]
	installedAddonGUICollection: "AddonGUICollectionT"

	def _get_installedAddons(self) -> CaseInsensitiveDict["AddonHandlerModel"]:
		"""
		Add-ons that have the same ID except differ in casing cause a path collision,
		as add-on IDs are installed to a case insensitive path.
		Therefore addon IDs should be treated as case insensitive.
		"""
		from addonHandler import getAvailableAddons
		return CaseInsensitiveDict({a.name: a for a in getAvailableAddons()})

	def _get_installedAddonGUICollection(self) -> "AddonGUICollectionT":
		addons = _createAddonGUICollection()
		for addonId in self.installedAddons:
			addonStoreData = self.installedAddons[addonId]._addonStoreData
			if addonStoreData:
				addons[addonStoreData.channel][addonId] = addonStoreData
			else:
				addons[Channel.STABLE][addonId] = self.installedAddons[addonId]._addonGuiModel
		return addons
