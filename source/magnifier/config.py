# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config

from .fullscreenMagnifier import FullScreenMagnifier, FullScreenMode
from .utils.filterHandler import Filter

_magnifier: FullScreenMagnifier | None = None

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
		zoomLevel = max(1.0, min(10.0, zoomLevel))
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
		# Find filter by displayString
		for f in Filter:
			if f.displayString == filterStr:
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


def setDefaultFilter(filterDisplayString: str):
	"""
	Set default filter from settings.

	:param filterDisplayString: The filter displayString to set.
	"""
	config.conf["magnifier"]["defaultFilter"] = filterDisplayString


def getDefaultFullscreenMode() -> FullScreenMode:
	"""
	Get default fullscreen mode from config.
	"""
	try:
		modeStr = config.conf["magnifier"]["defaultFullscreenMode"]
		# Find mode by displayString
		for mode in FullScreenMode:
			if mode.displayString == modeStr:
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


def setDefaultFullscreenMode(modeDisplayString: str):
	"""
	Set default fullscreen mode from settings.

	:param modeDisplayString: The fullscreen mode displayString to set.
	"""
	config.conf["magnifier"]["defaultFullscreenMode"] = modeDisplayString

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
