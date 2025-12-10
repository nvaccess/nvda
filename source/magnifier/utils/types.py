# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
"""
Types used in the magnifier module.
"""

from typing import NamedTuple
from enum import Enum
from utils.displayString import DisplayStringStrEnum
from gettext import pgettext


class MagnifierParams(NamedTuple):
	"""Named tuple representing magnifier parameters for initialization"""

	zoomLevel: float
	filter: str
	fullscreenMode: str


class Direction(Enum):
	"""Direction for zoom operations"""

	IN = True
	OUT = False


class MagnifierAction(DisplayStringStrEnum):
	"""Actions that can be performed with the magnifier"""

	ZOOM_IN = "zoom_in"
	ZOOM_OUT = "zoom_out"
	TOGGLE_FILTER = "toggle_filter"
	CHANGE_FULLSCREEN_MODE = "change_fullscreen_mode"
	START_SPOTLIGHT = "start_spotlight"

	@property
	def _displayStringLabels(self) -> dict["MagnifierAction", str]:
		return {
			# Translators: Action description for zooming in
			self.ZOOM_IN: pgettext("magnifier action", "trying to zoom in"),
			# Translators: Action description for zooming out
			self.ZOOM_OUT: pgettext("magnifier action", "trying to zoom out"),
			# Translators: Action description for toggling color filters
			self.TOGGLE_FILTER: pgettext("magnifier action", "trying to toggle filters"),
			# Translators: Action description for changing fullscreen mode
			self.CHANGE_FULLSCREEN_MODE: pgettext("magnifier action", "trying to change fullscreen mode"),
			# Translators: Action description for starting spotlight mode
			self.START_SPOTLIGHT: pgettext("magnifier action", "trying to start spotlight mode"),
		}


class MagnifierType(DisplayStringStrEnum):
	"""Type of magnifier"""

	FULLSCREEN = "fullscreen"
	DOCKED = "docked"
	LENS = "lens"

	@property
	def _displayStringLabels(self) -> dict["MagnifierType", str]:
		return {
			# Translators: Magnifier type - fullscreen mode
			self.FULLSCREEN: pgettext("magnifier", "Fullscreen"),
			# Translators: Magnifier type - docked mode
			self.DOCKED: pgettext("magnifier", "Docked"),
			# Translators: Magnifier type - lens mode
			self.LENS: pgettext("magnifier", "Lens"),
		}


class FocusType(Enum):
	"""Type of focus being tracked by the magnifier"""

	MOUSE = "mouse"
	NVDA = "nvda"


class MagnifierPosition(NamedTuple):
	"""Named tuple representing the position and size of the magnifier window"""

	left: int
	top: int
	visibleWidth: int
	visibleHeight: int


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
			# Translators: Magnifier focus mode - center mouse/focus on screen
			self.CENTER: pgettext("magnifier", "Center"),
			# Translators: Magnifier focus mode - follow focus at screen borders
			self.BORDER: pgettext("magnifier", "Border"),
			# Translators: Magnifier focus mode - maintain relative position
			self.RELATIVE: pgettext("magnifier", "Relative"),
		}


class Filter(DisplayStringStrEnum):
	NORMAL = "normal"
	GRAYSCALE = "grayscale"
	INVERTED = "inverted"

	@property
	def _displayStringLabels(self) -> dict["Filter", str]:
		return {
			# Translators: Magnifier color filter - no filter applied
			self.NORMAL: pgettext("magnifier", "Normal"),
			# Translators: Magnifier color filter - grayscale/black and white
			self.GRAYSCALE: pgettext("magnifier", "Grayscale"),
			# Translators: Magnifier color filter - inverted colors
			self.INVERTED: pgettext("magnifier", "Inverted"),
		}
