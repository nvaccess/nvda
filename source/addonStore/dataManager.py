# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2024 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

from copy import deepcopy
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
from json import JSONDecodeError

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
	InstalledAddonStoreModel,
	_createAddonGUICollection,
	_createInstalledStoreModelFromData,
	_createStoreCollectionFromJson,
)
from .models.channel import Channel
from .models.status import AvailableAddonStatus, getStatus, _StatusFilterKey
from .network import (
	_getCurrentApiVersionForURL,
	_getAddonStoreURL,
	_getCacheHashURL,
	_LATEST_API_VER,
)

if TYPE_CHECKING:
	from addonHandler import Addon as AddonHandlerModel  # noqa: F401
	# AddonGUICollectionT must only be imported when TYPE_CHECKING
	from .models.addon import AddonGUICollectionT, _AddonGUIModel, _AddonStoreModel  # noqa: F401
	from gui.addonStoreGui.viewModels.addonList import AddonListItemVM  # noqa: F401
	from gui.message import DisplayableError  # noqa: F401


addonDataManager: Optional["_DataManager"] = None
FETCH_TIMEOUT_S = 120  # seconds


def initialize():
	global addonDataManager
	if config.isAppX:
		log.info("Add-ons not supported when running as a Windows Store application")
		return
	log.debug("initializing addonStore data manager")
	addonDataManager = _DataManager()


def terminate():
	global addonDataManager
	if config.isAppX:
		log.info("Add-ons not supported when running as a Windows Store application")
		return
	addonDataManager.terminate()
	log.debug("terminating addonStore data manager")
	addonDataManager = None


class _DataManager:
	_cacheLatestFilename: str = "_cachedLatestAddons.json"
	_cacheCompatibleFilename: str = "_cachedCompatibleAddons.json"
	_downloadsPendingInstall: Set[Tuple["AddonListItemVM[_AddonStoreModel]", os.PathLike]] = set()
	_downloadsPendingCompletion: Set["AddonListItemVM[_AddonStoreModel]"] = set()

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
		self._initialiseAvailableAddonsThread = threading.Thread(
			target=self.getLatestCompatibleAddons,
			name="initialiseAvailableAddons",
			daemon=True,
		)
		self._initialiseAvailableAddonsThread.start()

	def terminate(self):
		if self._initialiseAvailableAddonsThread.is_alive():
			self._initialiseAvailableAddonsThread.join(timeout=1)
		if self._initialiseAvailableAddonsThread.is_alive():
			log.debugWarning("initialiseAvailableAddons thread did not terminate immediately")

	def _getLatestAddonsDataForVersion(self, apiVersion: str) -> Optional[bytes]:
		url = _getAddonStoreURL(self._preferredChannel, self._lang, apiVersion)
		try:
			log.debug(f"Fetching add-on data from {url}")
			response = requests.get(url, timeout=FETCH_TIMEOUT_S)
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

	def _getCacheHash(self) -> Optional[str]:
		url = _getCacheHashURL()
		try:
			log.debug(f"Fetching add-on data from {url}")
			response = requests.get(url, timeout=FETCH_TIMEOUT_S)
		except requests.exceptions.RequestException as e:
			log.debugWarning(f"Unable to get cache hash: {e}")
			return None
		if response.status_code != requests.codes.OK:
			log.error(
				f"Unable to get data from API ({url}),"
				f" response ({response.status_code}): {response.content}"
			)
			return None
		cacheHash = response.json()
		return cacheHash

	def _cacheCompatibleAddons(self, addonData: str, cacheHash: Optional[str]):
		if not NVDAState.shouldWriteToDisk():
			return
		if not addonData or not cacheHash:
			return
		cacheData = {
			"cacheHash": cacheHash,
			"data": addonData,
			"cachedLanguage": self._lang,
			"nvdaAPIVersion": addonAPIVersion.CURRENT,
		}
		with open(self._cacheCompatibleFile, 'w', encoding='utf-8') as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _cacheLatestAddons(self, addonData: str, cacheHash: Optional[str]):
		if not NVDAState.shouldWriteToDisk():
			return
		if not addonData or not cacheHash:
			return
		cacheData = {
			"cacheHash": cacheHash,
			"data": addonData,
			"cachedLanguage": self._lang,
			"nvdaAPIVersion": _LATEST_API_VER,
		}
		with open(self._cacheLatestFile, 'w', encoding='utf-8') as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _getCachedAddonData(self, cacheFilePath: str) -> Optional[CachedAddonsModel]:
		if not os.path.exists(cacheFilePath):
			return None
		try:
			with open(cacheFilePath, 'r', encoding='utf-8') as cacheFile:
				cacheData = json.load(cacheFile)
		except Exception:
			log.exception("Invalid add-on store cache")
			if NVDAState.shouldWriteToDisk():
				os.remove(cacheFilePath)
			return None
		try:
			data = cacheData["data"]
			cachedAddonData = _createStoreCollectionFromJson(data)
			cacheHash = cacheData["cacheHash"]
			cachedLanguage = cacheData["cachedLanguage"]
			nvdaAPIVersion = cacheData["nvdaAPIVersion"]
		except (KeyError, JSONDecodeError):
			log.exception(f"Invalid add-on store cache:\n{cacheData}")
			if NVDAState.shouldWriteToDisk():
				os.remove(cacheFilePath)
			return None
		return CachedAddonsModel(
			cachedAddonData=cachedAddonData,
			cacheHash=cacheHash,
			cachedLanguage=cachedLanguage,
			nvdaAPIVersion=tuple(nvdaAPIVersion),  # loads as list,
		)

	# Translators: A title of the dialog shown when fetching add-on data from the store fails
	_updateFailureMessage = pgettext("addonStore", "Add-on data update failure")

	def getLatestCompatibleAddons(
			self,
			onDisplayableError: Optional["DisplayableError.OnDisplayableErrorT"] = None,
	) -> "AddonGUICollectionT":
		cacheHash = self._getCacheHash()
		shouldRefreshData = (
			not self._compatibleAddonCache
			or self._compatibleAddonCache.nvdaAPIVersion != addonAPIVersion.CURRENT
			or cacheHash is None
			or self._compatibleAddonCache.cacheHash != cacheHash
			or self._compatibleAddonCache.cachedLanguage != self._lang
		)
		if shouldRefreshData:
			apiData = self._getLatestAddonsDataForVersion(_getCurrentApiVersionForURL())
			if apiData:
				decodedApiData = apiData.decode()
				self._cacheCompatibleAddons(
					addonData=decodedApiData,
					cacheHash=cacheHash,
				)
				self._compatibleAddonCache = CachedAddonsModel(
					cachedAddonData=_createStoreCollectionFromJson(decodedApiData),
					cacheHash=cacheHash,
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
		return deepcopy(self._compatibleAddonCache.cachedAddonData)

	def getLatestAddons(
			self,
			onDisplayableError: Optional["DisplayableError.OnDisplayableErrorT"] = None,
	) -> "AddonGUICollectionT":
		cacheHash = self._getCacheHash()
		shouldRefreshData = (
			not self._latestAddonCache
			or cacheHash is None
			or self._latestAddonCache.cacheHash != cacheHash
			or self._latestAddonCache.cachedLanguage != self._lang
		)
		if shouldRefreshData:
			apiData = self._getLatestAddonsDataForVersion(_LATEST_API_VER)
			if apiData:
				decodedApiData = apiData.decode()
				self._cacheLatestAddons(
					addonData=decodedApiData,
					cacheHash=cacheHash,
				)
				self._latestAddonCache = CachedAddonsModel(
					cachedAddonData=_createStoreCollectionFromJson(decodedApiData),
					cacheHash=cacheHash,
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
		return deepcopy(self._latestAddonCache.cachedAddonData)

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
		with open(addonCachePath, 'w', encoding='utf-8') as cacheFile:
			json.dump(addonData.asdict(), cacheFile, ensure_ascii=False)

	def _getCachedInstalledAddonData(self, addonId: str) -> Optional[InstalledAddonStoreModel]:
		addonCachePath = os.path.join(self._installedAddonDataCacheDir, f"{addonId}.json")
		if not os.path.exists(addonCachePath):
			return None
		try:
			with open(addonCachePath, 'r', encoding='utf-8') as cacheFile:
				cacheData = json.load(cacheFile)
		except Exception:
			log.exception(f"Invalid cached installed add-on data: {addonCachePath}")
			return None
		if not cacheData:
			return None
		return _createInstalledStoreModelFromData(cacheData)

	def _addonsPendingUpdate(self) -> list["_AddonGUIModel"]:
		addonsPendingUpdate: list["_AddonGUIModel"] = []
		compatibleAddons = self.getLatestCompatibleAddons()
		for channel in compatibleAddons:
			for addon in compatibleAddons[channel].values():
				if (
					getStatus(addon, _StatusFilterKey.UPDATE) == AvailableAddonStatus.UPDATE
					# Only consider add-ons that have been installed through the Add-on Store
					and addon._addonHandlerModel._addonStoreData is not None
				):
					# Only consider add-on updates for the same channel
					if addon.channel == addon._addonHandlerModel._addonStoreData.channel:
						addonsPendingUpdate.append(addon)
		return addonsPendingUpdate


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
				addons[Channel.EXTERNAL][addonId] = self.installedAddons[addonId]._addonGuiModel
		return addons
