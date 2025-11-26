# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Keyboard commands for the magnifier module.
Contains the command functions and their logic for keyboard shortcuts.
"""

import ui
from . import (
	getMagnifier,
	setMagnifier,
	getDefaultZoomLevel,
	setDefaultZoomLevel,
	getDefaultFilter,
	getDefaultFullscreenMode,
	shouldSaveShortcutChanges,
	setDefaultFilter,
	setDefaultFullscreenMode,
)
from .magnifier import Magnifier, MagnifierType
from .fullscreenMagnifier import FullScreenMagnifier, FullScreenMode
from .utils.filterHandler import filter
from logHandler import log


def toggleMagnifier():
	"""Toggle the NVDA magnifier on/off."""
	magnifier: Magnifier = getMagnifier()
	if magnifier and magnifier.isActive:
		# Stop magnifier
		magnifier._stopMagnifier()
		setMagnifier(None)
		ui.message(
			_(
				# Translators: Message announced when stopping the NVDA magnifier
				"Stopping NVDA Fullscreen magnifier"
			)
		)
	else:
		# Start magnifier with zoom level from config
		defaultZoomLevel = getDefaultZoomLevel()
		defaultFilter = getDefaultFilter()

		# Logic to change when adding other type of magnifier
		defaultFullscreenMode = getDefaultFullscreenMode()
		magnifier = FullScreenMagnifier(
			zoomLevel=defaultZoomLevel, filter=defaultFilter, fullscreenMode=defaultFullscreenMode
		)
		setMagnifier(magnifier)
		ui.message(
			_(
				# Translators: Message announced when starting the NVDA magnifier
				"Starting NVDA Fullscreen magnifier"
			)
		)

def zoomIn():
	"""Zoom in the magnifier."""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(magnifier, "trying to zoom in"):
		magnifier._zoom(True)
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
	if magnifierIsActiveVerify(magnifier, "trying to zoom out"):
		magnifier._zoom(False)
		if shouldSaveShortcutChanges():
			# Save to config if option is enabled
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
	if magnifierIsActiveVerify(magnifier, "trying to toggle filters"):
		filters = list(filter)
		idx = filters.index(magnifier.filter)
		magnifier.filter = filters[(idx + 1) % len(filters)]
		if True:
			# if magnifier.magnifierType == MagnifierType.FULLSCREEN:
			magnifier._applyFilter()

		# Save to config if option is enabled
		if shouldSaveShortcutChanges():
			setDefaultFilter(magnifier.filter.name.lower())

		ui.message(
			_(
				# Translators: Message announced when changing the color filter with {filter} being the new color filter
				"Color filter changed to {filter}"
			).format(filter=magnifier.filter.name.lower())
		)

def toggleFullscreenMode():
	"""Cycle through fullscreen focus modes (center, border, relative)."""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(magnifier, "trying to change fullscreen mode"):
		if magnifierIsFullscreenVerify(magnifier, "trying to change fullscreen mode"):
			modes = list(FullScreenMode)
			currentMode = magnifier.fullscreenMode
			idx = modes.index(currentMode)
			newMode = modes[(idx + 1) % len(modes)]
			log.info(f"Changing fullscreen mode from {currentMode} to {newMode}")
			magnifier.fullscreenMode = newMode

			# Save to config if option is enabled
			if shouldSaveShortcutChanges():
				setDefaultFullscreenMode(newMode.name.lower())

			ui.message(
				_(
					# Translators: Message announced when changing the fullscreen mode with {mode} being the new fullscreen mode
					"Fullscreen mode changed to {mode}"
				).format(mode=newMode.name.lower())
			)

def startSpotlight():
	magnifier: FullScreenMagnifier = getMagnifier()
	if magnifierIsActiveVerify(magnifier, "trying to start spotlight mode"):
		if magnifierIsFullscreenVerify(magnifier, "trying to start spotlight mode"):
			log.info("trying to launch spotlight mode")
			if magnifier._spotlightManager._spotlightIsActive:
				log.info('found spotlight manager and it is active')
				ui.message(
					_(
						# Translators: Message announced when trying to start spotlight mode while it's already active
						"Spotlight mode is already active"
					)
				)
			else:
				log.info('no active spotlight manager found, starting new one')
				magnifier._startSpotlight()
				ui.message(
					_(
						# Translators: Message announced when spotlight mode is started
						"Spotlight mode started"
					)
				)


def magnifierIsActiveVerify(magnifier: Magnifier, action: str = "") -> bool:
	if magnifier.isActive:
		return True
	else:
		ui.message(
			_(
				# Translators: Message announced that the magnifier is not active
				"Magnifier is not active at {action}"
			).format(action=action)
		)
		return False

def magnifierIsFullscreenVerify(magnifier: Magnifier, action: str = "") -> bool:
	if magnifier._magnifierType == MagnifierType.FULLSCREEN:
		return True
	else:
		ui.message(
			_(
				# Translators: Message announced that the magnifier is not fullscreen
				"Magnifier is not fullscreen at {action}"
			).format(action=action)
		)
		return False
