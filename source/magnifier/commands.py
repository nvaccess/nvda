# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Keyboard commands for the magnifier module
Contains the command functions and their logic for keyboard shortcuts
"""

import ui

from . import getMagnifier, initialize, terminate

from .config import (
	getCurrentZoomLevel,
	setDefaultZoomLevel,
	getCurrentFilter,
	setDefaultFilter,
	getCurrentFullscreenMode,
	setDefaultFullscreenMode,
	shouldSaveShortcutChanges,
)

from .magnifier import Magnifier
from .fullscreenMagnifier import FullScreenMagnifier
from .utils.types import (
	Filter,
	Direction,
	MagnifierType,
	FullScreenMode,
	MagnifierAction,
)
from logHandler import log


def toggleMagnifier():
	"""Toggle the NVDA magnifier on/off."""
	magnifier: Magnifier = getMagnifier()
	if magnifier and magnifier.isActive:
		# Stop magnifier
		terminate()
		ui.message(
			_(
				# Translators: Message announced when stopping the NVDA magnifier
				"Exiting magnifier"
			)
		)
	else:
		initialize()
		zoomLevel = getCurrentZoomLevel()
		filter = getCurrentFilter()
		fullscreenMode = getCurrentFullscreenMode()
		ui.message(
			_(
				# Translators: Message announced when starting the NVDA magnifier
				"Starting magnifier with {zoomLevel} zoom level, {filter} filter, and {fullscreenMode} fullscreen mode"
			).format(
				zoomLevel=zoomLevel,
				filter=filter,
				fullscreenMode=fullscreenMode,
			)
		)


def zoomIn():
	"""Zoom in the magnifier."""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.ZOOM_IN,
	):
		magnifier._zoom(Direction.IN)
		if shouldSaveShortcutChanges():
			setDefaultZoomLevel(magnifier.zoomLevel)
		ui.message(
			_(
				# Translators: Message announced when zooming in with {zoomLevel} being the target zoom level
				"Zooming in with {zoomLevel} level"
			).format(zoomLevel=magnifier.zoomLevel)
		)


def zoomOut():
	"""Zoom out the magnifier."""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.ZOOM_OUT,
	):
		magnifier._zoom(Direction.OUT)
		if shouldSaveShortcutChanges():
			setDefaultZoomLevel(magnifier.zoomLevel)
		ui.message(
			_(
				# Translators: Message announced when zooming out with {zoomLevel} being the target zoom level
				"Zooming out with {zoomLevel} level"
			).format(zoomLevel=magnifier.zoomLevel)
		)


def toggleFilter():
	magnifier: Magnifier = getMagnifier()
	log.info(f"Toggling filter for magnifier: {magnifier}")
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.TOGGLE_FILTER,
	):
		filters = list(Filter)
		idx = filters.index(magnifier.filterType)
		magnifier.filterType = filters[(idx + 1) % len(filters)]
		if magnifier.magnifierType == MagnifierType.FULLSCREEN:
			magnifier._applyFilter()

		# Save to config if option is enabled
		if shouldSaveShortcutChanges():
			setDefaultFilter(magnifier.filterType)

		ui.message(
			_(
				# Translators: Message announced when changing the color filter with {filter} being the new color filter
				"Color filter changed to {filter}"
			).format(filter=magnifier.filterType.displayString)
		)


def toggleFullscreenMode():
	"""Cycle through fullscreen focus modes (center, border, relative)."""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.CHANGE_FULLSCREEN_MODE,
	):
		if magnifierIsFullscreenVerify(
			magnifier,
			MagnifierAction.CHANGE_FULLSCREEN_MODE,
		):
			modes = list(FullScreenMode)
			currentMode = magnifier.fullscreenMode
			idx = modes.index(currentMode)
			newMode = modes[(idx + 1) % len(modes)]
			log.info(f"Changing fullscreen mode from {currentMode} to {newMode}")
			magnifier.fullscreenMode = newMode

			# Save to config if option is enabled
			if shouldSaveShortcutChanges():
				setDefaultFullscreenMode(newMode)

			ui.message(
				_(
					# Translators: Message announced when changing the fullscreen mode with {mode} being the new fullscreen mode
					"Fullscreen mode changed to {mode}"
				).format(mode=newMode.displayString)
			)


def startSpotlight():
	magnifier: FullScreenMagnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.START_SPOTLIGHT,
	):
		if magnifierIsFullscreenVerify(
			magnifier,
			MagnifierAction.START_SPOTLIGHT,
		):
			log.info("trying to launch spotlight mode")
			if magnifier._spotlightManager._spotlightIsActive:
				log.info("found spotlight manager and it is active")
				ui.message(
					_(
						# Translators: Message announced when trying to start spotlight mode while it's already active
						"Spotlight mode is already active"
					)
				)
			else:
				log.info("no active spotlight manager found, starting new one")
				magnifier._startSpotlight()
				ui.message(
					_(
						# Translators: Message announced when spotlight mode is started
						"Spotlight mode started"
					)
				)


def magnifierIsActiveVerify(
	magnifier: Magnifier,
	action: MagnifierAction,
) -> bool:
	if magnifier and magnifier.isActive:
		return True
	else:
		ui.message(
			_(
				# Translators: Message announced that the magnifier is not active
				"Magnifier is not active at {action}"
			).format(action=action.displayString)
		)
		return False


def magnifierIsFullscreenVerify(
	magnifier: Magnifier,
	action: MagnifierAction,
) -> bool:
	if magnifier.magnifierType == MagnifierType.FULLSCREEN:
		return True
	else:
		ui.message(
			_(
				# Translators: Message announced that the magnifier is not fullscreen
				"Magnifier is not fullscreen at {action}"
			).format(action=action.displayString)
		)
		return False
