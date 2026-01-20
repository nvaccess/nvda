# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2025 NV Access Limited, Antoine Haffreingue, Cyrille Bougot
# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt

"""
Types used in the magnifier module.
"""

from enum import Enum, auto
from typing import NamedTuple
from utils.displayString import DisplayStringStrEnum, DisplayStringEnum


class MagnifierParams(NamedTuple):
	"""Named tuple representing magnifier parameters for initialization"""

	zoomLevel: float
	filter: str
	fullscreenMode: str


class Direction(Enum):
	"""Direction for zoom operations"""

	IN = True
	OUT = False


class MagnifierAction(DisplayStringEnum):
	"""Actions that can be performed with the magnifier"""

	ZOOM_IN = auto()
	ZOOM_OUT = auto()
	TOGGLE_FILTER = auto()
	CHANGE_FULLSCREEN_MODE = auto()
	START_SPOTLIGHT = auto()

	@property
	def _displayStringLabels(self) -> dict["MagnifierAction", str]:
		return {
			# Translators: Action description for zooming in.
			self.ZOOM_IN: pgettext("magnifier action", "zoom in"),
			# Translators: Action description for zooming out.
			self.ZOOM_OUT: pgettext("magnifier action", "zoom out"),
			# Translators: Action description for toggling color filters.
			self.TOGGLE_FILTER: pgettext("magnifier action", "toggle filters"),
			# Translators: Action description for changing full-screen mode.
			self.CHANGE_FULLSCREEN_MODE: pgettext("magnifier action", "change full-screen mode"),
			# Translators: Action description for starting spotlight mode.
			self.START_SPOTLIGHT: pgettext("magnifier action", "start spotlight mode"),
		}


class MagnifierType(DisplayStringStrEnum):
	"""Type of magnifier"""

	FULLSCREEN = "fullscreen"
	DOCKED = "docked"
	LENS = "lens"

	@property
	def _displayStringLabels(self) -> dict["MagnifierType", str]:
		return {
			# Translators: Magnifier type - full-screen mode.
			self.FULLSCREEN: pgettext("magnifier", "Fullscreen"),
			# Translators: Magnifier type - docked mode.
			self.DOCKED: pgettext("magnifier", "Docked"),
			# Translators: Magnifier type - lens mode.
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
			# Translators: Magnifier focus mode - center mouse/focus on screen.
			self.CENTER: pgettext("magnifier", "Center"),
			# Translators: Magnifier focus mode - follow focus at screen borders.
			self.BORDER: pgettext("magnifier", "Border"),
			# Translators: Magnifier focus mode - maintain relative position.
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
