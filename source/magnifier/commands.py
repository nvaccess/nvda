# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Keyboard commands for the magnifier module.
Contains the command functions and their logic for keyboard shortcuts.
"""

import ui
from . import getMagnifier, setMagnifier, getDefaultZoomLevel, getDefaultFilter
from .fullscreenMagnifier import FullScreenMagnifier
from .utils.filterHandler import filter
from logHandler import log


def toggleMagnifier():
	"""Toggle the NVDA magnifier on/off."""
	magnifier = getMagnifier()
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
		magnifier = FullScreenMagnifier(zoomLevel=defaultZoomLevel, filter=defaultFilter)
		setMagnifier(magnifier)
		ui.message(
			_(
				# Translators: Message announced when starting the NVDA magnifier
				"Starting NVDA Fullscreen magnifier"
			)
		)


def zoomIn():
	"""Zoom in the magnifier."""
	magnifier = getMagnifier()
	if magnifier and magnifier.isActive:
		magnifier._zoom(True)
		ui.message(
			_(
				# Translators: Message announced when zooming in with {zoomLevel} being the target zoom level
				"Zooming in with {zoomLevel} level"
			).format(zoomLevel=magnifier.zoomLevel)
		)
	else:
		magnifierNotActiveMessage("trying to zoom in")


def zoomOut():
	"""Zoom out the magnifier."""
	magnifier = getMagnifier()
	if magnifier and magnifier.isActive:
		magnifier._zoom(False)
		ui.message(
			_(
				# Translators: Message announced when zooming out with {zoomLevel} being the target zoom level
				"Zooming out with {zoomLevel} level"
			).format(zoomLevel=magnifier.zoomLevel)
		)
	else:
		magnifierNotActiveMessage("trying to zoom out")


def toggleFilter():
	magnifier = getMagnifier()
	log.info(f"Toggling filter for magnifier: {magnifier}")
	if magnifier and magnifier.isActive:
		filters = list(filter)
		idx = filters.index(magnifier.filter)
		magnifier.filter = filters[(idx + 1) % len(filters)]
		if True:
			# if magnifier.magnifierType == MagnifierType.FULLSCREEN:
			magnifier._applyFilter()
		ui.message(
			_(
				# Translators: Message announced when changing the color filter with {filter} being the new color filter
				"Color filter changed to {filter}"
			).format(filter=magnifier.filter.name.lower())
		)
	else:
		magnifierNotActiveMessage("trying to toggle filters")


def magnifierNotActiveMessage(action: str = ""):
	ui.message(
		_(
			# Translators: Message announced that the magnifier is not active
			"Magnifier is not active {action}"
		).format(action=action)
	)
