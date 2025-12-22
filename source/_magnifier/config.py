# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config
from gettext import pgettext
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
	"""
	zoomLevel = config.conf["magnifier"]["defaultZoomLevel"]
	return float(zoomLevel)


def setDefaultZoomLevel(zoomLevel: float):
	"""
	Set default zoom level from settings.

	:param zoomLevel: The zoom level to set.
	"""

	if "magnifier" not in config.conf:
		config.conf["magnifier"] = {}
	config.conf["magnifier"]["defaultZoomLevel"] = zoomLevel


def getDefaultFilter() -> Filter:
	"""
	Get default filter from config.
	"""
	filterStr = config.conf["magnifier"]["defaultFilter"]
	for f in Filter:
		if f.value == filterStr:
			return f


def setDefaultFilter(filter: Filter):
	"""
	Set default filter from settings.

	:param filter: The filter displayString to set.
	"""
	config.conf["magnifier"]["defaultFilter"] = filter.value


def getDefaultFullscreenMode() -> FullScreenMode:
	"""
	Get default full-screen mode from config.
	"""
	modeStr = config.conf["magnifier"]["defaultFullscreenMode"]
	# Find mode by value
	for mode in FullScreenMode:
		if mode.value == modeStr:
			return mode


def setDefaultFullscreenMode(mode: FullScreenMode):
	"""
	Set default full-screen mode from settings.

	:param mode: The full-screen mode displayString to set.
	"""
	config.conf["magnifier"]["defaultFullscreenMode"] = mode.value


def shouldKeepMouseCentered() -> bool:
	"""
	Check if mouse pointer should be kept centered in magnifier view.
	"""
	return config.conf["magnifier"]["keepMouseCentered"]
