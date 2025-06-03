# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022-2025 NV Access Limited
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
from .models.status import AvailableAddonStatus, _canUpdateAddon, getStatus, _StatusFilterKey
from .network import (
	_getCurrentApiVersionForURL,
	_getAddonStoreURL,
	_getCacheHashURL,
	_LATEST_API_VER,
)
from .settings import _AddonStoreSettings


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
		self._cacheCompatibleFile = os.path.join(
			WritePaths.addonStoreDir,
			_DataManager._cacheCompatibleFilename,
		)
		self._installedAddonDataCacheDir = WritePaths.addonsDir

		if NVDAState.shouldWriteToDisk():
			# ensure caching dirs exist
			pathlib.Path(WritePaths.addonStoreDir).mkdir(parents=True, exist_ok=True)
			pathlib.Path(self._installedAddonDataCacheDir).mkdir(parents=True, exist_ok=True)

		self.storeSettings = _AddonStoreSettings()
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
		if NVDAState.shouldWriteToDisk():
			self.storeSettings.save()
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
				f"Unable to get data from API ({url}), response ({response.status_code}): {response.content}",
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
				f"Unable to get data from API ({url}), response ({response.status_code}): {response.content}",
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
		with open(self._cacheCompatibleFile, "w", encoding="utf-8") as cacheFile:
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
		with open(self._cacheLatestFile, "w", encoding="utf-8") as cacheFile:
			json.dump(cacheData, cacheFile, ensure_ascii=False)

	def _getCachedAddonData(self, cacheFilePath: str) -> Optional[CachedAddonsModel]:
		if not os.path.exists(cacheFilePath):
			return None
		try:
			with open(cacheFilePath, "r", encoding="utf-8") as cacheFile:
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
	_updateFailureMirrorSuggestion = pgettext(
		"addonStore",
		# Translators: A suggestion of what to do when fetching add-on data from the store fails and a metadata mirror is being used.
		# {url} will be replaced with the mirror URL.
		"Make sure you are connected to the internet, and the Add-on Store mirror URL is valid.\n"
		"Mirror URL: {url}",
	)
	_updateFailureDefaultSuggestion = pgettext(
		"addonStore",
		# Translators: A suggestion of what to do when fetching add-on data from the store fails and the default metadata URL is being used.
		"Make sure you are connected to the internet and try again.",
	)

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
			else:
				self._do_displayError(
					onDisplayableError,
					# Translators: A message shown when fetching add-on data from the store fails
					pgettext("addonStore", "Unable to fetch latest add-on data for compatible add-ons."),
				)

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
			else:
				self._do_displayError(
					onDisplayableError,
					# Translators: A message shown when fetching add-on data from the store fails
					pgettext("addonStore", "Unable to fetch latest add-on data for incompatible add-ons."),
				)

		if self._latestAddonCache is None:
			return _createAddonGUICollection()
		return deepcopy(self._latestAddonCache.cachedAddonData)

	def _do_displayError(
		self,
		onDisplayableError: "DisplayableError.OnDisplayableErrorT | None",
		displayMessage: str,
		titleMessage: str | None = None,
	):
		"""Display a DisplayableMessage if an OnDisplayableError action is given.

		See gui.message.DisplayableError for further information.

		:param onDisplayableError: The displayable error action.
		:param displayMessage: Body of the displayable error.
		:param titleMessage: Title of the displayable error. If None, _updateFailureMessage will be used. Defaults to None.
		"""
		if onDisplayableError is None:
			return
		from gui.message import DisplayableError

		tip = (
			self._updateFailureMirrorSuggestion.format(url=url)
			if (url := config.conf["addonStore"]["baseServerURL"])
			else self._updateFailureDefaultSuggestion
		)
		displayMessage = f"{displayMessage}\n{tip}"
		displayableError = DisplayableError(displayMessage, titleMessage or self._updateFailureMessage)
		callLater(delay=0, callable=onDisplayableError.notify, displayableError=displayableError)

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
		with open(addonCachePath, "w", encoding="utf-8") as cacheFile:
			json.dump(addonData.asdict(), cacheFile, ensure_ascii=False)

	def _getCachedInstalledAddonData(self, addonId: str) -> Optional[InstalledAddonStoreModel]:
		addonCachePath = os.path.join(self._installedAddonDataCacheDir, f"{addonId}.json")
		if not os.path.exists(addonCachePath):
			return None
		try:
			with open(addonCachePath, "r", encoding="utf-8") as cacheFile:
				cacheData = json.load(cacheFile)
		except Exception:
			log.exception(f"Invalid cached installed add-on data: {addonCachePath}")
			return None
		if not cacheData:
			return None
		return _createInstalledStoreModelFromData(cacheData)

	def _addonsPendingUpdate(
		self,
		onDisplayableError: "DisplayableError.OnDisplayableErrorT | None" = None,
	) -> list["_AddonGUIModel"]:
		updatableAddonStatuses = {AvailableAddonStatus.UPDATE}
		addonsPendingUpdate: dict["str", "_AddonGUIModel"] = {}
		if config.conf["addonStore"]["allowIncompatibleUpdates"]:
			updatableAddonStatuses.add(AvailableAddonStatus.UPDATE_INCOMPATIBLE)
			compatibleAddons = self.getLatestAddons(onDisplayableError)
		else:
			compatibleAddons = self.getLatestCompatibleAddons(onDisplayableError)
		for channel in compatibleAddons:
			# Ensure add-on update channel is within the preferred update channels
			for addon in compatibleAddons[channel].values():
				# Ensure add-on is updatable
				if getStatus(addon, _StatusFilterKey.UPDATE) in updatableAddonStatuses:
					if (installedStoreData := addon._addonHandlerModel._addonStoreData) is not None:
						installedChannel = installedStoreData.channel
					else:
						installedChannel = Channel.EXTERNAL
					selectedUpdateChannel = addonDataManager.storeSettings.getAddonSettings(
						addon.addonId,
					).updateChannel
					availableUpdateChannels = selectedUpdateChannel._availableChannelsForAddonWithChannel(
						installedChannel,
					)
					# Ensure add-on channel is valid to update to given update preferences
					if addon.channel in availableUpdateChannels:
						if addon.name in addonsPendingUpdate:
							# See if this version is newer than the currently tracked versions
							if _canUpdateAddon(addon, addonsPendingUpdate[addon.name]):
								addonsPendingUpdate[addon.name] = addon
						else:
							addonsPendingUpdate[addon.name] = addon
		return list(addonsPendingUpdate.values())


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
