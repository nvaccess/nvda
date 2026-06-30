# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025-2026 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Types used in the magnifier module.
"""

from enum import Enum, auto
from typing import NamedTuple
from utils.displayString import DisplayStringStrEnum, DisplayStringEnum


class MagnifierParameters(NamedTuple):
	"""Named tuple representing the size, position and filter of the magnifier"""

	magnifierSize: "Size"
	coordinates: "Coordinates"
	filter: "Filter"


class Direction(Enum):
	"""Direction for zoom operations"""

	IN = True
	OUT = False


class Size(NamedTuple):
	"""Named tuple representing width and height"""

	width: int
	height: int


class MagnifierAction(DisplayStringEnum):
	"""Actions that can be performed with the magnifier"""

	ZOOM_IN = auto()
	ZOOM_OUT = auto()
	PAN_LEFT = auto()
	PAN_RIGHT = auto()
	PAN_UP = auto()
	PAN_DOWN = auto()
	PAN_LEFT_EDGE = auto()
	PAN_RIGHT_EDGE = auto()
	PAN_TOP_EDGE = auto()
	PAN_BOTTOM_EDGE = auto()
	TOGGLE_FILTER = auto()
	CHANGE_MAGNIFIER_VIEW = auto()
	TOGGLE_FOLLOW_SETTINGS = auto()
	CHANGE_FULLSCREEN_MODE = auto()
	START_SPOTLIGHT = auto()
	MOVE_MOUSE_TO_VIEW = auto()

	@property
	def _displayStringLabels(self) -> dict["MagnifierAction", str]:
		return {
			# Translators: Action description for zooming in.
			self.ZOOM_IN: pgettext("magnifier action", "zoom in"),
			# Translators: Action description for zooming out.
			self.ZOOM_OUT: pgettext("magnifier action", "zoom out"),
			# Translators: Action description for panning left.
			self.PAN_LEFT: pgettext("magnifier action", "pan left"),
			# Translators: Action description for panning right.
			self.PAN_RIGHT: pgettext("magnifier action", "pan right"),
			# Translators: Action description for panning up.
			self.PAN_UP: pgettext("magnifier action", "pan up"),
			# Translators: Action description for panning down.
			self.PAN_DOWN: pgettext("magnifier action", "pan down"),
			# Translators: Action description for panning to left edge.
			self.PAN_LEFT_EDGE: pgettext("magnifier action", "pan to left edge"),
			# Translators: Action description for panning to right edge.
			self.PAN_RIGHT_EDGE: pgettext("magnifier action", "pan to right edge"),
			# Translators: Action description for panning to top edge.
			self.PAN_TOP_EDGE: pgettext("magnifier action", "pan to top edge"),
			# Translators: Action description for panning to bottom edge.
			self.PAN_BOTTOM_EDGE: pgettext("magnifier action", "pan to bottom edge"),
			# Translators: Action description for toggling settings.
			self.TOGGLE_FOLLOW_SETTINGS: pgettext("magnifier action", "toggle tracking settings"),
			# Translators: Action description for toggling color filters.
			self.TOGGLE_FILTER: pgettext("magnifier action", "cycle color filters"),
			# Translators: Action description for changing magnifier view.
			self.CHANGE_MAGNIFIER_VIEW: pgettext("magnifier action", "change magnifier view"),
			# Translators: Action description for changing full-screen mode.
			self.CHANGE_FULLSCREEN_MODE: pgettext("magnifier action", "change full-screen mode"),
			# Translators: Action description for move mouse to view
			self.MOVE_MOUSE_TO_VIEW: pgettext("magnifier action", "move mouse to view"),
			# Translators: Action description for showing entire screen overview.
			self.START_SPOTLIGHT: pgettext("magnifier action", "show screen overview"),
		}


class MagnifierTrackingType(DisplayStringEnum):
	"""Tracking the magnifier should follow based on user settings"""

	MOUSE = auto()
	SYSTEM_FOCUS = auto()
	REVIEW = auto()
	NAVIGATOR_OBJECT = auto()

	@property
	def _displayStringLabels(self) -> dict["MagnifierTrackingType", str]:
		return {
			# Translators: Type of item tracked by the Magnifier - mouse cursor.
			self.MOUSE: pgettext("magnifier", "Mouse"),
			# Translators: Type of item tracked by the Magnifier - system focus (active element).
			self.SYSTEM_FOCUS: pgettext("magnifier", "System focus"),
			# Translators: Type of item tracked by the Magnifier - review cursor position.
			self.REVIEW: pgettext("magnifier", "Review cursor"),
			# Translators: Type of item tracked by the Magnifier - navigator object position.
			self.NAVIGATOR_OBJECT: pgettext("magnifier", "Navigator object"),
		}


class MagnifiedView(DisplayStringStrEnum):
	"""Type of magnifier"""

	FULLSCREEN = "fullscreen"
	FIXED = "fixed"
	DOCKED = "docked"
	LENS = "lens"

	@property
	def _displayStringLabels(self) -> dict["MagnifiedView", str]:
		return {
			# Translators: Magnifier view - full-screen mode.
			self.FULLSCREEN: pgettext("magnifier", "Fullscreen"),
			# Translators: Magnifier view - fixed mode.
			self.FIXED: pgettext("magnifier", "Fixed"),
			# Translators: Magnifier view - docked mode.
			self.DOCKED: pgettext("magnifier", "Docked"),
			# Translators: Magnifier view - lens mode.
			self.LENS: pgettext("magnifier", "Lens"),
		}


class Coordinates(NamedTuple):
	"""Named tuple representing x and y coordinates"""

	x: int
	y: int


class ZoomHistory(NamedTuple):
	"""Named tuple representing zoom history entry with zoom level and coordinates"""

	zoomLevel: float
	coordinates: Coordinates


class FullScreenMode(DisplayStringStrEnum):
	CENTER = "center"
	BORDER = "border"
	RELATIVE = "relative"

	@property
	def _displayStringLabels(self) -> dict["FullScreenMode", str]:
		return {
			# Translators: Magnifier tracking mode - center the tracked item on the screen.
			self.CENTER: pgettext("magnifier", "Center"),
			# Translators: Magnifier tracking mode - follow the tracked item only when it reaches screen borders.
			self.BORDER: pgettext("magnifier", "Border"),
			# Translators: Magnifier tracking mode - preserve the tracked item's screen position within the magnified view (same relative screen location).
			self.RELATIVE: pgettext("magnifier", "Relative"),
		}


class Filter(DisplayStringStrEnum):
	NORMAL = "normal"
	GRAYSCALE = "grayscale"
	INVERTED = "inverted"

	@property
	def _displayStringLabels(self) -> dict["Filter", str]:
		return {
			# Translators: Magnifier color filter - no filter applied.
			self.NORMAL: pgettext("magnifier", "Normal"),
			# Translators: Magnifier color filter - grayscale/black and white.
			self.GRAYSCALE: pgettext("magnifier", "Grayscale"),
			# Translators: Magnifier color filter - inverted colors.
			self.INVERTED: pgettext("magnifier", "Inverted"),
		}
