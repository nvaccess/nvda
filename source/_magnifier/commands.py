# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Keyboard commands for the magnifier module.
Contains the command functions and their logic for keyboard shortcuts.
"""

from typing import Literal
import ui
from . import getMagnifier, initialize, terminate
from .config import (
	getDefaultZoomLevelString,
	getDefaultFilter,
	getDefaultFullscreenMode,
	ZoomLevel,
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

PAN_ACTION_TO_EDGE_NAME = {
	MagnifierAction.PAN_LEFT: pgettext(
		"magnifier",
		# Translators: Short name for the left edge, used in messages.
		"left",
	),
	MagnifierAction.PAN_RIGHT: pgettext(
		"magnifier",
		# Translators: Short name for the right edge, used in messages.
		"right",
	),
	MagnifierAction.PAN_UP: pgettext(
		"magnifier",
		# Translators: Short name for the top edge, used in messages.
		"top",
	),
	MagnifierAction.PAN_DOWN: pgettext(
		"magnifier",
		# Translators: Short name for the bottom edge, used in messages.
		"bottom",
	),
	MagnifierAction.PAN_LEFT_EDGE: pgettext(
		"magnifier",
		# Translators: Short name for the left edge, used in messages.
		"left",
	),
	MagnifierAction.PAN_RIGHT_EDGE: pgettext(
		"magnifier",
		# Translators: Short name for the right edge, used in messages.
		"right",
	),
	MagnifierAction.PAN_TOP_EDGE: pgettext(
		"magnifier",
		# Translators: Short name for the top edge, used in messages.
		"top",
	),
	MagnifierAction.PAN_BOTTOM_EDGE: pgettext(
		"magnifier",
		# Translators: Short name for the bottom edge, used in messages.
		"bottom",
	),
}


def toggleMagnifier() -> None:
	"""Toggle the NVDA magnifier on/off"""
	import screenCurtain

	magnifier: Magnifier = getMagnifier()
	if magnifier and magnifier._isActive:
		# Stop magnifier
		terminate()
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when stopping the NVDA magnifier.
				"Exiting magnifier",
			),
		)
	# Check if Screen Curtain is active
	elif screenCurtain.screenCurtain and screenCurtain.screenCurtain.enabled:
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when trying to start magnifier while Screen Curtain is active.
				"Cannot start magnifier: Screen Curtain is active. Please disable Screen Curtain first.",
			),
		)
		return
	else:
		initialize()

		filter = getDefaultFilter()
		fullscreenMode = getDefaultFullscreenMode()

		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when starting the NVDA magnifier.
				"Starting magnifier with {zoomLevel} zoom level, {filter} filter, and {fullscreenMode} full-screen mode",
			).format(
				zoomLevel=getDefaultZoomLevelString(),
				filter=filter.displayString,
				fullscreenMode=fullscreenMode.displayString,
			),
		)


def zoom(direction: Direction) -> None:
	"""
	Generic zoom function that handles zoom in and zoom out.

	:param direction: The zoom direction (IN or OUT)
	"""
	action = MagnifierAction.ZOOM_IN if direction == Direction.IN else MagnifierAction.ZOOM_OUT
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(magnifier, action):
		magnifier._zoom(direction)
		ui.message(
			ZoomLevel.ZOOM_MESSAGE.format(
				zoomLevel=f"{magnifier.zoomLevel:.1f}",
			),
		)


def pan(action: MagnifierAction) -> None:
	"""
	Handles panning the magnifier up/down/left/right and going to each edge.

	:param action: The pan action to perform
	"""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(magnifier, action):
		hasMoved = magnifier._pan(action)
		if not hasMoved:
			edgeName = PAN_ACTION_TO_EDGE_NAME.get(action)
			ui.message(
				pgettext(
					"magnifier",
					# Translators: Message announced when arriving at the {edge} edge.
					"{edge} edge",
				).format(edge=edgeName),
			)


def toggleFilter() -> None:
	"""Cycle through color filters"""
	magnifier: Magnifier = getMagnifier()
	log.debug(f"Toggling filter for magnifier: {magnifier}")
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.TOGGLE_FILTER,
	):
		filters = list(Filter)
		idx = filters.index(magnifier.filterType)
		magnifier.filterType = filters[(idx + 1) % len(filters)]
		if magnifier._magnifierType == MagnifierType.FULLSCREEN:
			magnifier._applyFilter()
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when changing the color filter with {filter} being the new color filter.
				"Color filter changed to {filter}",
			).format(filter=magnifier.filterType.displayString),
		)


def toggleFullscreenMode() -> None:
	"""Cycle through full-screen focus modes (center, border, relative)"""
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
			currentMode = magnifier._fullscreenMode
			idx = modes.index(currentMode)
			newMode = modes[(idx + 1) % len(modes)]
			log.debug(f"Changing full-screen mode from {currentMode} to {newMode}")
			magnifier._fullscreenMode = newMode
			ui.message(
				pgettext(
					"magnifier",
					# Translators: Message announced when changing the full-screen mode with {mode} being the new full-screen mode.
					"Full-screen mode changed to {mode}",
				).format(mode=newMode.displayString),
			)


def startSpotlight() -> None:
	"""Start spotlight mode in full-screen magnifier"""
	magnifier: FullScreenMagnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.START_SPOTLIGHT,
	):
		if magnifierIsFullscreenVerify(
			magnifier,
			MagnifierAction.START_SPOTLIGHT,
		):
			log.debug("trying to launch spotlight mode")
			if magnifier._spotlightManager._spotlightIsActive:
				log.debug("found spotlight manager and it is active")
				ui.message(
					pgettext(
						"magnifier",
						# Translators: Message announced when trying to start spotlight mode while it's already active.
						"Spotlight mode is already active",
					),
				)
			else:
				log.debug("no active spotlight manager found, starting new one")
				magnifier._startSpotlight()
				ui.message(
					pgettext(
						"magnifier",
						# Translators: Message announced when spotlight mode is started.
						"Spotlight mode started",
					),
				)


def magnifierIsActiveVerify(
	magnifier: Magnifier,
	action: MagnifierAction,
) -> bool:
	"""
	Verify that the magnifier is active before performing an action

	:param magnifier: The magnifier instance to check
	:param action: The action being performed, for messaging

	:return: True if the magnifier is active, False otherwise
	"""
	if magnifier and magnifier._isActive:
		return True
	else:
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when the magnifier is not active.
				"Cannot {action} when Magnifier is not active.",
			).format(action=action.displayString),
		)
		return False


def magnifierIsFullscreenVerify(
	magnifier: Magnifier,
	action: Literal[MagnifierAction.CHANGE_FULLSCREEN_MODE, MagnifierAction.START_SPOTLIGHT],
) -> bool:
	"""
	Verify that the magnifier is full-screen before performing an action

	:param magnifier: The magnifier instance to check
	:param action: The action being performed, for messaging

	:return: True if the magnifier is full-screen, False otherwise
	"""
	if magnifier._magnifierType == MagnifierType.FULLSCREEN:
		return True
	else:
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when the magnifier is not full-screen.
				"Cannot {action} when Magnifier is not full-screen.",
			).format(action=action.displayString),
		)
		return False
