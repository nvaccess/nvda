# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
NVDA Magnifier module.
Handles module initialization, configuration and settings interaction.
"""

import config
from dataclasses import dataclass, field
from .utils.types import Filter, FullScreenMode, MagnifierFollowFocusType, MagnifiedView


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
	closestIndex = min(
		range(len(zoomValues)),
		key=lambda i: abs(zoomValues[i] - zoomLevel),
	)
	return zoomStrings[closestIndex]


def setZoomLevel(zoomLevel: float) -> None:
	"""
	Set zoom level from settings.

	:param zoomLevel: The zoom level to set.
	"""
	config.conf["magnifier"]["zoomLevel"] = zoomLevel


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


_FOLLOW_CONFIG_KEYS: dict[MagnifierFollowFocusType, str] = {
	MagnifierFollowFocusType.MOUSE: "followMouse",
	MagnifierFollowFocusType.SYSTEM_FOCUS: "followSystemFocus",
	MagnifierFollowFocusType.REVIEW: "followReviewCursor",
	MagnifierFollowFocusType.NAVIGATOR_OBJECT: "followNavigatorObject",
}


@dataclass
class _FollowStateOverride:
	savedStates: dict[MagnifierFollowFocusType, bool] = field(default_factory=dict)
	isActive: bool = False


_followStateOverride = _FollowStateOverride()


def _ensureSavedStatesInitialized() -> None:
	"""
	Populate _followStateOverride.savedStates from current config if not yet done.
	Called lazily to avoid reading config.conf at module import time.
	"""
	if not _followStateOverride.savedStates:
		saveFollowStates()


def getFollowState(focusType: MagnifierFollowFocusType) -> bool:
	"""
	Get the current follow state for a given focus type.

	:param focusType: The focus type to query.
	:return: True if the magnifier follows the given focus type, False otherwise.
	"""
	return config.conf["magnifier"][_FOLLOW_CONFIG_KEYS[focusType]]


def setFollowState(focusType: MagnifierFollowFocusType, state: bool) -> None:
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
