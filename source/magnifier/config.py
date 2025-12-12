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


_magnifier = None


class ZoomLevel:
	"""
	Constants and utilities for zoom level management.
	"""

	MAX_ZOOM: float = 10.0
	MIN_ZOOM: float = 1.0
	STEP_FACTOR: float = 0.5
	zoomRange: list[float] = [i * 0.5 for i in range(2, 21)]  # 1.0 to 10.0 with 0.5 steps
	zoomStrings: list[str] = [
		pgettext("magnifier", "{zoomLevel}x").format(zoomLevel=f"{value:.1f}") for value in zoomRange
	]


def getDefaultZoomLevel() -> float:
	"""
	Get default zoom level from config.
	"""
	try:
		zoomLevel = config.conf["magnifier"]["defaultZoomLevel"]
		# Ensure it's a float
		return float(zoomLevel)
	except (KeyError, ValueError, TypeError):
		return 2.0


def getCurrentZoomLevel() -> float:
	"""
	Get current zoom level for settings.
	"""
	global _magnifier
	if _magnifier and _magnifier.isActive:
		return float(_magnifier.zoomLevel)  # Ensure float
	return getDefaultZoomLevel()


def setDefaultZoomLevel(zoomLevel: float):
	"""
	Set default zoom level from settings.

	:param zoomLevel: The zoom level to set.
	"""
	# Validate zoom level and ensure it's a float
	try:
		zoomLevel = float(zoomLevel)
		zoomLevel = max(ZoomLevel.MIN_ZOOM, min(ZoomLevel.MAX_ZOOM, zoomLevel))
	except (ValueError, TypeError):
		zoomLevel = 2.0

	# Ensure config section exists
	if "magnifier" not in config.conf:
		config.conf["magnifier"] = {}

	# Save to config as float
	config.conf["magnifier"]["defaultZoomLevel"] = zoomLevel


def getDefaultFilter() -> Filter:
	"""
	Get default filter from config.
	"""
	try:
		filterStr = config.conf["magnifier"]["defaultFilter"]
		# Find filter by value
		for f in Filter:
			if f.value == filterStr:
				return f
		return Filter.NORMAL
	except (KeyError, AttributeError):
		return Filter.NORMAL


def getCurrentFilter() -> str:
	"""
	Get current filter for settings.
	"""
	global _magnifier
	if _magnifier and _magnifier.isActive:
		# Return filter name as string for settings
		return _magnifier.filterType.displayString
	# Return default filter name as string
	return getDefaultFilter().displayString


def setDefaultFilter(filter: Filter):
	"""
	Set default filter from settings.

	:param filter: The filter displayString to set.
	"""
	config.conf["magnifier"]["defaultFilter"] = filter.value


def getDefaultFullscreenMode() -> FullScreenMode:
	"""
	Get default fullscreen mode from config.
	"""
	try:
		modeStr = config.conf["magnifier"]["defaultFullscreenMode"]
		# Find mode by value
		for mode in FullScreenMode:
			if mode.value == modeStr:
				return mode
		return FullScreenMode.CENTER
	except (KeyError, AttributeError):
		return FullScreenMode.CENTER


def getCurrentFullscreenMode() -> str:
	"""
	Get current fullscreen mode for settings.
	"""
	global _magnifier
	if _magnifier and _magnifier.isActive:
		# Return fullscreen mode name as string for settings
		return _magnifier.fullscreenMode.displayString
	# Return default fullscreen mode name as string
	return getDefaultFullscreenMode().displayString


def setDefaultFullscreenMode(mode: FullScreenMode):
	"""
	Set default fullscreen mode from settings.

	:param mode: The fullscreen mode displayString to set.
	"""
	config.conf["magnifier"]["defaultFullscreenMode"] = mode.value


def shouldKeepMouseCentered() -> bool:
	"""
	Check if mouse pointer should be kept centered in magnifier view.
	"""
	try:
		return config.conf["magnifier"]["keepMouseCentered"]
	except (KeyError, AttributeError):
		return False


def shouldSaveShortcutChanges() -> bool:
	"""
	Check if shortcut changes should be saved to config.
	"""
	try:
		return config.conf["magnifier"]["saveShortcutChanges"]
	except (KeyError, AttributeError):
		return False
