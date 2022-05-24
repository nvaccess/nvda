# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2022 NV Access Limited
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
import enum
from logHandler import log
import requests

import addonAPIVersion
from typing import (
	Optional,
)
from .models import (
	AvailableAddonsModel,
	_createModelFromData,
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


class DataManager:
	def __init__(self):
		self._lang = "en"
		self._availableAddons: AvailableAddonsModel = {}

	def _getLatestAvailableAddonsData(self) -> Optional[str]:
		url = _getAddonStoreURL(Channel.ALL, self._lang, _getCurrentApiVersionForURL())
		response = requests.get(url)
		if response.status_code != requests.codes.OK:
			log.error(
				f"Unable to get data from API ({url}),"
				f" response ({response.status_code}): {response.content}"
			)
			return None
		return response.content

	def getLatestAvailableAddons(self) -> AvailableAddonsModel:
		if not self._availableAddons:
			apiData = self._getLatestAvailableAddonsData()
			if apiData:
				self._availableAddons = _createModelFromData(
					apiData
				)
		return self._availableAddons
