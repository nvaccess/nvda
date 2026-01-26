# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config
from .utils.types import Filter, FullScreenMode


class ZoomLevel:
	"""
	Constants and utilities for zoom level management.
	"""

	MAX_ZOOM: float = 10.0
	MIN_ZOOM: float = 1.0
	STEP_FACTOR: float = 0.5

	@classmethod
	def zoom_range(cls) -> list[float]:
		"""
		Return the list of available zoom levels.
		"""
		start = round(cls.MIN_ZOOM / cls.STEP_FACTOR)
		end = round(cls.MAX_ZOOM / cls.STEP_FACTOR)

		return [i * cls.STEP_FACTOR for i in range(start, end + 1)]

	@classmethod
	def zoom_strings(cls) -> list[str]:
		"""
		Return localized zoom level strings.
		"""
		return [
			# Translators: Zoom level string shown in settings and messages.
			pgettext("magnifier", "{zoomLevel}x").format(
				zoomLevel=f"{value:.1f}",
			)
			for value in cls.zoom_range()
		]


def getDefaultZoomLevel() -> float:
	"""
	Get default zoom level from config.

	:return: The default zoom level.
	"""
	zoomLevel = config.conf["magnifier"]["defaultZoomLevel"]
	return zoomLevel


def getDefaultZoomLevelString() -> str:
	"""
	Get default zoom level as a formatted string.

	:return: Formatted zoom level string.
	"""
	zoomLevel = getDefaultZoomLevel()
	zoomValues = ZoomLevel.zoom_range()
	zoomStrings = ZoomLevel.zoom_strings()
	zoomIndex = zoomValues.index(zoomLevel)
	return zoomStrings[zoomIndex]


def setDefaultZoomLevel(zoomLevel: float) -> None:
	"""
	Set default zoom level from settings.

	:param zoomLevel: The zoom level to set.
	"""

	if "magnifier" not in config.conf:
		config.conf["magnifier"] = {}
	config.conf["magnifier"]["defaultZoomLevel"] = zoomLevel


def getDefaultPanValue() -> int:
	"""
	Get default pan value from config.

	:return: The default pan value.
	"""
	return config.conf["magnifier"]["defaultPanValue"]


def setDefaultPanValue(panValue: int) -> None:
	"""
	Set default pan value from settings.

	:param panValue: The pan value to set.
	"""

	if "magnifier" not in config.conf:
		config.conf["magnifier"] = {}
	config.conf["magnifier"]["defaultPanValue"] = panValue


def getDefaultFilter() -> Filter:
	"""
	Get default filter from config.

	:return: The default filter.
	"""
	return Filter(config.conf["magnifier"]["defaultFilter"])


def setDefaultFilter(filter: Filter) -> None:
	"""
	Set default filter from settings.

	:param filter: The filter to set.
	"""
	config.conf["magnifier"]["defaultFilter"] = filter.value


def getDefaultFullscreenMode() -> FullScreenMode:
	"""
	Get default full-screen mode from config.

	:return: The default full-screen mode.
	"""
	return FullScreenMode(config.conf["magnifier"]["defaultFullscreenMode"])


def setDefaultFullscreenMode(mode: FullScreenMode) -> None:
	"""
	Set default full-screen mode from settings.

	:param mode: The full-screen mode to set.
	"""
	config.conf["magnifier"]["defaultFullscreenMode"] = mode.value


def shouldKeepMouseCentered() -> bool:
	"""
	Check if mouse pointer should be kept centered in magnifier view.

	:return: True if mouse should be kept centered, False otherwise.
	"""
	return config.conf["magnifier"]["keepMouseCentered"]
