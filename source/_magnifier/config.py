# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config
from .utils.types import Filter, FullScreenMode, MagnifierType, FixedWindowPosition


class ZoomLevel:
	"""
	Constants and utilities for zoom level management.
	"""

	MAX_ZOOM: float = 10.0
	MIN_ZOOM: float = 1.0
	STEP_FACTOR: float = 0.5
	ZOOM_MESSAGE = pgettext(
		"magnifier",
		# Translators: Message announced when zooming in with {zoomLevel} being the target zoom level.
		"{zoomLevel}x",
	)

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
			cls.ZOOM_MESSAGE.format(
				zoomLevel=f"{value:.1f}",
			)
			for value in cls.zoom_range()
		]


def getZoomLevel() -> float:
	"""
	Get zoom level from config.

	:return: The zoom level.
	"""
	zoomLevel = config.conf["magnifier"]["zoomLevel"]
	return zoomLevel


def getZoomLevelString() -> str:
	"""
	Get zoom level as a formatted string.

	:return: Formatted zoom level string.
	"""
	zoomLevel = getZoomLevel()
	zoomValues = ZoomLevel.zoom_range()
	zoomStrings = ZoomLevel.zoom_strings()
	zoomIndex = zoomValues.index(zoomLevel)
	return zoomStrings[zoomIndex]


def setZoomLevel(zoomLevel: float) -> None:
	"""
	Set zoom level from settings.

	:param zoomLevel: The zoom level to set.
	"""
	config.conf["magnifier"]["zoomLevel"] = zoomLevel


def getMagnifierType() -> MagnifierType:
	"""
	Get magnifier type from config.

	:return: The magnifier type.
	"""
	return MagnifierType(config.conf["magnifier"]["magnifierType"])


def setMagnifierType(magnifierType: MagnifierType) -> None:
	"""
	Set magnifier type from settings.

	:param magnifierType: The magnifier type to set.
	"""
	config.conf["magnifier"]["magnifierType"] = magnifierType.value


def getPanStep() -> int:
	"""
	Get pan value from config.

	:return: The  pan value.
	"""
	return config.conf["magnifier"]["panStep"]


def setPanStep(panStep: int) -> None:
	"""
	Set pan value from settings.

	:param panStep: The pan value to set.
	"""

	if "magnifier" not in config.conf:
		config.conf["magnifier"] = {}
	config.conf["magnifier"]["panStep"] = panStep


def getFilter() -> Filter:
	"""
	Get filter from config.

	:return: The filter.
	"""
	return Filter(config.conf["magnifier"]["filter"])


def setFilter(filter: Filter) -> None:
	"""
	Set filter from settings.

	:param filter: The filter to set.
	"""
	config.conf["magnifier"]["filter"] = filter.value


def isTrueCentered() -> bool:
	"""
	Check if true centered mode is enabled in config.

	:return: True if true centered mode is enabled, False otherwise.
	"""
	return config.conf["magnifier"]["isTrueCentered"]


def shouldKeepMouseCentered() -> bool:
	"""
	Check if mouse pointer should be kept centered in magnifier view.

	:return: True if mouse should be kept centered, False otherwise.
	"""
	return config.conf["magnifier"]["keepMouseCentered"]


def getFullscreenMode() -> FullScreenMode:
	"""
	Get full-screen mode from config.

	:return: The full-screen mode.
	"""
	return FullScreenMode(config.conf["magnifier"]["fullscreenMode"])


def setFullscreenMode(mode: FullScreenMode) -> None:
	"""
	Set full-screen mode from settings.

	:param mode: The full-screen mode to set.
	"""
	config.conf["magnifier"]["fullscreenMode"] = mode.value


def getFixedWindowWidth() -> int:
	"""
	Get fixed magnifier window width from config.

	:return: The fixed magnifier window width.
	"""
	return config.conf["magnifier"]["fixedWindowWidth"]


def setFixedWindowWidth(width: int) -> None:
	"""
	Set fixed magnifier window width from settings.

	:param width: The fixed magnifier window width to set.
	"""
	config.conf["magnifier"]["fixedWindowWidth"] = width


def getFixedWindowHeight() -> int:
	"""
	Get fixed magnifier window height from config.

	:return: The fixed magnifier window height.
	"""
	return config.conf["magnifier"]["fixedWindowHeight"]


def setFixedWindowHeight(height: int) -> None:
	"""
	Set fixed magnifier window height from settings.

	:param height: The fixed magnifier window height to set.
	"""
	config.conf["magnifier"]["fixedWindowHeight"] = height


def getFixedWindowPosition() -> FixedWindowPosition:
	"""
	Get magnifier window position from config.

	:return: The magnifier window position.
	"""
	return FixedWindowPosition(config.conf["magnifier"]["fixedWindowPosition"])


def setFixedWindowPosition(position: FixedWindowPosition) -> None:
	"""
	Set magnifier window position from settings.

	:param position: The magnifier window position to set.
	"""
	config.conf["magnifier"]["fixedWindowPosition"] = position.value
