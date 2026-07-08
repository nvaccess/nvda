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
from . import changeMagnifiedView, getMagnifier, start, stop
from .config import (
	setMagnifiedView,
	getFollowState,
	setFilter,
	setFollowState,
	setFullscreenMode,
	toggleAllFollowStates,
	ZoomLevel,
	_isDebug,
)
from .magnifier import Magnifier
from .fullscreenMagnifier import FullScreenMagnifier
from .utils.types import (
	Filter,
	Direction,
	MagnifiedView,
	FullScreenMode,
	MagnifierAction,
	MagnifierTrackingType,
)
from logHandler import log

PAN_ACTION_TO_EDGE_MESSAGES = {
	MagnifierAction.PAN_LEFT: pgettext(
		"magnifier",
		# Translators: Message announced when already at left edge of the screen while panning the magnified view
		"left edge",
	),
	MagnifierAction.PAN_RIGHT: pgettext(
		"magnifier",
		# Translators: Message announced when already at right edge of the screen while panning the magnified view
		"right edge",
	),
	MagnifierAction.PAN_UP: pgettext(
		"magnifier",
		# Translators: Message announced when already at top edge of the screen while panning the magnified view
		"top edge",
	),
	MagnifierAction.PAN_DOWN: pgettext(
		"magnifier",
		# Translators: Message announced when already at bottom edge of the screen while panning the magnified view
		"bottom edge",
	),
	MagnifierAction.PAN_LEFT_EDGE: pgettext(
		"magnifier",
		# Translators: Message announced when already at left edge of the screen while panning the magnified view
		# to left edge
		"left edge",
	),
	MagnifierAction.PAN_RIGHT_EDGE: pgettext(
		"magnifier",
		# Translators: Message announced when already at right edge of the screen while panning the magnified view
		# to right edge
		"right edge",
	),
	MagnifierAction.PAN_TOP_EDGE: pgettext(
		"magnifier",
		# Translators: Message announced when already at top edge of the screen while panning the magnified view
		# to top edge
		"top edge",
	),
	MagnifierAction.PAN_BOTTOM_EDGE: pgettext(
		"magnifier",
		# Translators: Message announced when already at left edge of the screen while panning the magnified view
		# to left edge
		"bottom edge",
	),
}


def toggleMagnifier() -> None:
	"""Toggle the NVDA magnifier on/off"""
	import screenCurtain

	magnifier: Magnifier | None = getMagnifier()
	if magnifier and magnifier._isActive:
		# Stop magnifier
		stop()
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when stopping the NVDA magnifier.
				"Magnifier disabled",
			),
		)
	# Check if Screen Curtain is active
	elif screenCurtain.screenCurtain and screenCurtain.screenCurtain.enabled:
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when trying to start magnifier while Screen Curtain is active.
				"Cannot start magnifier. Please disable Screen Curtain first.",
			),
		)
	else:
		start()
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when starting the NVDA magnifier.
				"Magnifier enabled",
			),
		)


def zoom(direction: Direction) -> None:
	"""
	Generic zoom function that handles zoom in and zoom out.

	:param direction: The zoom direction (IN or OUT)
	"""
	action = MagnifierAction.ZOOM_IN if direction == Direction.IN else MagnifierAction.ZOOM_OUT
	magnifier: Magnifier = getMagnifier()
	if not (magnifier and magnifier._isActive):
		# Start magnifier if not already running
		if direction == Direction.IN:
			toggleMagnifier()
		else:
			magnifierIsActiveVerify(magnifier, action)
		return
	magnifier._zoom(direction)
	ui.message(
		ZoomLevel.zoomMessage(magnifier.zoomLevel),
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
			ui.message(PAN_ACTION_TO_EDGE_MESSAGES[action])


def moveMouseToView() -> None:
	"""
	Move the mouse cursor to the center of the magnified view.
	"""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(magnifier, MagnifierAction.MOVE_MOUSE_TO_VIEW):
		magnifier.moveMouseToViewCenter()


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
		if magnifier._MAGNIFIED_VIEW == MagnifiedView.FULLSCREEN:
			assert isinstance(magnifier, FullScreenMagnifier)
			fullscreenMagnifier: FullScreenMagnifier = magnifier
			fullscreenMagnifier._applyFilter()
		setFilter(magnifier.filterType)

		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when changing the color filter with {filter} being the new color filter.
				"Color filter {filter}",
			).format(filter=magnifier.filterType.displayString),
		)


def cycleMagnifiedView() -> None:
	"""Cycle through magnifier views (full-screen, fixed, docked, lens)"""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.CHANGE_MAGNIFIER_VIEW,
	):
		views = list(MagnifiedView)
		currentView = magnifier._MAGNIFIED_VIEW
		idx = views.index(currentView)
		newView = views[(idx + 1) % len(views)]
		log.debug(f"Changing magnifier view from {currentView} to {newView}")
		changeMagnifiedView(newView)
		setMagnifiedView(newView)
		magnifier = getMagnifier()
		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when changing the magnifier view with {view} being the new magnifier view.
				"{view} view",
			).format(view=magnifier._MAGNIFIED_VIEW.displayString),
		)


def toggleFollow(focusType: MagnifierTrackingType) -> None:
	"""
	Toggle the specified follow mode setting.

	:param focusType: The follow mode to toggle (mouse, system focus, review cursor, navigator object)
	"""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.TOGGLE_FOLLOW_SETTINGS,
	):
		state = not getFollowState(focusType)
		setFollowState(focusType, state)

		ui.message(
			pgettext(
				"magnifier",
				# Translators: Message announced when toggling a follow setting with {setting} being the name of the setting and {state} being either "enabled" or "disabled".
				"{setting} {state}",
			).format(
				setting=focusType.displayString,
				state=pgettext(
					"magnifier",
					# Translators: State of the follow setting being toggled enabled.
					"enabled",
				)
				if state
				else pgettext(
					"magnifier",
					# Translators: State of the follow setting being toggled disabled.
					"disabled",
				),
			),
		)


def toggleAllFollow() -> None:
	"""Toggle all follow settings at once."""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.TOGGLE_FOLLOW_SETTINGS,
	):
		isDisabledNow = toggleAllFollowStates()
		if isDisabledNow:
			stateMessage = pgettext(
				"magnifier",
				# Translators: State of all follow settings being toggled disabled.
				"All tracking settings disabled",
			)
		else:
			stateMessage = pgettext(
				"magnifier",
				# Translators: State of all follow settings being restored.
				"Tracking settings restored",
			)
		ui.message(stateMessage)


def toggleFullscreenMode() -> None:
	"""Cycle through full-screen modes (center, border, relative)"""
	magnifier: Magnifier = getMagnifier()
	if magnifierIsActiveVerify(
		magnifier,
		MagnifierAction.CHANGE_FULLSCREEN_MODE,
	):
		if magnifierIsFullscreenVerify(
			magnifier,
			MagnifierAction.CHANGE_FULLSCREEN_MODE,
		):
			fullscreenMagnifier: FullScreenMagnifier = magnifier
			modes = list(FullScreenMode)
			currentMode = fullscreenMagnifier._fullscreenMode
			idx = modes.index(currentMode)
			newMode = modes[(idx + 1) % len(modes)]
			log.debug(f"Changing full-screen mode from {currentMode} to {newMode}")
			fullscreenMagnifier._fullscreenMode = newMode
			setFullscreenMode(newMode)
			ui.message(
				pgettext(
					"magnifier",
					# Translators: Message announced when changing the full-screen mode with {mode} being the new full-screen mode.
					"Full-screen mode {mode}",
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
			fullscreenMagnifier: FullScreenMagnifier = magnifier
			if _isDebug():
				log.debug("trying to launch spotlight mode")
			if fullscreenMagnifier._spotlightManager._spotlightIsActive:
				if _isDebug():
					log.debug("found spotlight manager and it is active")
				ui.message(
					pgettext(
						"magnifier",
						# Translators: Message announced when trying to show temporary overview of the screen while it's already active.
						"The screen overview is already active",
					),
				)
			else:
				if _isDebug():
					log.debug("no active spotlight manager found, starting new one")
				fullscreenMagnifier._startSpotlight()
				ui.message(
					pgettext(
						"magnifier",
						# Translators: Message announced when overview of the entire screen is being showed.
						"Showing entire screen",
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
	if magnifier._MAGNIFIED_VIEW == MagnifiedView.FULLSCREEN:
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
