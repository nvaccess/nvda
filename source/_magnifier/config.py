# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config
from dataclasses import dataclass, field
from .utils.types import Filter, FullScreenMode, MagnifierTrackingType, MagnifiedView


def setEnabled(enable: bool) -> None:
	"""
	Set the config for the magnifier state (enable or disabled).

	:param enable: True if the magnifier is enabled, False if it is disabled.
	"""
	config.conf["magnifier"]["enabled"] = enable


def getEnabled() -> bool:
	"""
	Check if the magnifier is enabled in config.

	:return: True if the magnifier is enabled, False otherwise.
	"""
	return config.conf["magnifier"]["enabled"]


class ZoomLevel:
	"""
	Constants and utilities for zoom level management.
	"""

	MAX_ZOOM: int = 5000
	MIN_ZOOM: int = 100
	STEP_FACTOR: int = 50

	@staticmethod
	def zoomMessage(zoomLevel: int) -> str:
		zoomLevel = zoomLevel / 100.0
		return pgettext(
			"magnifier",
			# Translators: Message announced when zooming in with {zoomLevel} being the target zoom level.
			"{zoomLevel}x",
		).format(zoomLevel=f"{zoomLevel:.1f}")


def getZoomLevel() -> int:
	"""
	Get zoom level from config.

	:return: The zoom level (percentage).
	"""
	zoomLevel = config.conf["magnifier"]["zoom"]
	return zoomLevel


def getZoomLevelString() -> str:
	"""
	Get zoom level as a formatted string.

	:return: Formatted zoom level string.
	"""
	zoomLevel = getZoomLevel()
	return ZoomLevel.zoomMessage(zoomLevel)


def roundZoomLevel(zoomLevel: int) -> int:
	"""
	Round a zoom level to the nearest valid step.

	:param zoomLevel: The zoom level to round.
	:return: The rounded zoom level.
	"""
	remainder = zoomLevel % ZoomLevel.STEP_FACTOR
	if remainder >= ZoomLevel.STEP_FACTOR / 2:
		return zoomLevel + (ZoomLevel.STEP_FACTOR - remainder)
	else:
		return zoomLevel - remainder


def setZoomLevel(zoomLevel: int) -> None:
	"""
	Set zoom level from settings.

	:param zoomLevel: The zoom level to set.
	"""
	if not isinstance(zoomLevel, int):
		raise ValueError("Zoom level must be an integer percentage")
	if not (ZoomLevel.MIN_ZOOM <= zoomLevel <= ZoomLevel.MAX_ZOOM):
		raise ValueError(f"Zoom level must be between {ZoomLevel.MIN_ZOOM} and {ZoomLevel.MAX_ZOOM}")
	if zoomLevel % ZoomLevel.STEP_FACTOR != 0:
		raise ValueError(f"Zoom level must be a multiple of {ZoomLevel.STEP_FACTOR}")
	config.conf["magnifier"]["zoom"] = zoomLevel


def getPanStep() -> int:
	"""
	Get pan value from config.

	:return: The pan value.
	"""
	return config.conf["magnifier"]["panStep"]


def setPanStep(panStep: int) -> None:
	"""
	Set pan value from settings.

	:param panStep: The pan value to set.
	"""
	config.conf["magnifier"]["panStep"] = panStep


def getFilter() -> Filter:
	"""
	Get filter from config.

	:return: The filter.
	"""
	return Filter(config.conf["magnifier"]["filter"])


def setFilter(filter: Filter) -> None:
	"""
	Set  filter from settings.

	:param filter: The filter to set.
	"""
	config.conf["magnifier"]["filter"] = filter.value


def getMagnifiedView() -> MagnifiedView:
	"""
	Get magnifier view from config.

	:return: The magnifier view.
	"""
	return MagnifiedView(config.conf["magnifier"]["magnifiedView"])


def setMagnifiedView(magnifiedView: MagnifiedView) -> None:
	"""
	Set magnifier view in settings.

	:param magnifiedView: The magnifier view to set.
	"""
	config.conf["magnifier"]["magnifiedView"] = magnifiedView.value


_FOLLOW_CONFIG_KEYS: dict[MagnifierTrackingType, str] = {
	MagnifierTrackingType.MOUSE: "followMouse",
	MagnifierTrackingType.SYSTEM_FOCUS: "followSystemFocus",
	MagnifierTrackingType.REVIEW: "followReviewCursor",
	MagnifierTrackingType.NAVIGATOR_OBJECT: "followNavigatorObject",
}


@dataclass
class _FollowStateOverride:
	savedStates: dict[MagnifierTrackingType, bool] = field(default_factory=dict)
	isActive: bool = False


_followStateOverride = _FollowStateOverride()


def _ensureSavedStatesInitialized() -> None:
	"""
	Populate _followStateOverride.savedStates from current config if not yet done.
	Called lazily to avoid reading config.conf at module import time.
	"""
	if not _followStateOverride.savedStates:
		saveFollowStates()


def getFollowState(focusType: MagnifierTrackingType) -> bool:
	"""
	Get the current follow state for a given focus type.

	:param focusType: The focus type to query.
	:return: True if the magnifier follows the given focus type, False otherwise.
	"""
	return config.conf["magnifier"][_FOLLOW_CONFIG_KEYS[focusType]]


def setFollowState(focusType: MagnifierTrackingType, state: bool) -> None:
	"""
	Set the follow state for a given focus type.

	:param focusType: The focus type to update.
	:param state: True to enable following, False to disable.
	"""
	config.conf["magnifier"][_FOLLOW_CONFIG_KEYS[focusType]] = state


def saveFollowStates() -> None:
	"""Save current follow states so they can be restored later."""
	for focusType in _FOLLOW_CONFIG_KEYS:
		_followStateOverride.savedStates[focusType] = getFollowState(focusType)


def toggleAllFollowStates() -> bool:
	"""
	Toggle all follow states between forced-disabled and previously saved states.

	:return: True when all follow states are forced disabled after the call, False when restored.
	"""
	_ensureSavedStatesInitialized()
	if _followStateOverride.isActive:
		for focusType, state in _followStateOverride.savedStates.items():
			setFollowState(focusType, state)
		_followStateOverride.isActive = False
	else:
		saveFollowStates()
		for focusType in _FOLLOW_CONFIG_KEYS:
			setFollowState(focusType, False)
		_followStateOverride.isActive = True
	return _followStateOverride.isActive


def isTrueCentered() -> bool:
	"""
	Check if true centered mode is enabled in config.

	:return: True if true centered mode is enabled, False otherwise.
	"""
	return config.conf["magnifier"]["isTrueCentered"]


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


def _isDebug() -> bool:
	return config.conf["debugLog"]["magnifier"]
